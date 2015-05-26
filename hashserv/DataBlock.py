from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('config.py')

from btctxstore import BtcTxStore
from hashserv.Database import latest_hash
from hashserv.Database import latest_block
from hashserv.MerkleTree import MerkleTree


class DataBlock:
    def __init__(self, block_num, conn=None):
        """Validating and inserting data hashes into the database."""
        self.conn = conn

        self.block_num = int(block_num)
        self.merkle_tree = MerkleTree()
        self.closed = False
        self.tx_id = None

    def close(self):
        """Close block, so a Merkle root can be generated."""
        self.closed = True

    def generate_block(self):
        """Close the current block, and generate a new one."""

        try:
            last_block = latest_block(self.conn)
            last_hash = latest_hash(self.conn)

            # Get Merkle Root
            self.find_leaves()
            self.close()
            merkle_root = self.merkle_root()

            # Get TXID
            hexdata = merkle_root
            privatekeys = app.config["PRIVATE_KEYS"]
            changeaddress = app.config["CHANGE_ADDRESS"]
            fee = app.config["FEE"]
            testnet = app.config["TESTNET"]
            blockchain = BtcTxStore(testnet=testnet)
            tx_id = blockchain.storenulldata(hexdata, privatekeys, 
                                             changeaddress=changeaddress,
                                             fee=fee)

            # Close current block
            c = self.conn.cursor()
            query1 = "UPDATE block_table SET end_hash=?, closed=?, merkle_root=?, tx_id=? WHERE id=?"
            c.execute(query1, (last_hash, True, merkle_root, tx_id, last_block))

            # Start new block
            query2 = "INSERT INTO block_table (start_hash) VALUES (?)"
            c.execute(query2, (last_hash,))

            self.conn.commit()
            self.conn.close()
            return 'Block {0} Built.'.format(last_block)
        except LookupError:
            return 'Block Empty.'

    def is_closed(self):
        query = 'SELECT closed FROM block_table where id=?'
        cur = self.conn.execute(query, (self.block_num,))
        block = cur.fetchone()
        self.closed = block[0]
        return self.closed

    def find_leaves(self):
        """Load the leaves for this block."""
        query = 'SELECT * FROM hash_table where block=? ORDER BY id DESC'
        cur = self.conn.execute(query, (self.block_num,))

        hashes = cur.fetchall()
        if len(hashes) > 0:
            for row in hashes:
                self.add_hash(row[1])
        else:
            raise LookupError("Empty Block.")

        self.is_closed()

    def add_hash(self, ahash):
        """Add hashes to the Merkle Tree."""
        if not self.closed:
            self.merkle_tree.add_hash(ahash)

    def merkle_root(self):
        """Find the data Merkle root."""
        if self.closed:
            return self.merkle_tree.merkle_root()

    def merkle_proof(self, target):
        """Find the Merkle proof of a target."""
        self.find_leaves()
        if self.is_closed():
            return self.merkle_tree.merkle_proof(target)

    def get_tx_id(self):
        query = 'SELECT tx_id FROM block_table where id=?'
        cur = self.conn.execute(query, (self.block_num,))
        block = cur.fetchone()
        self.tx_id = block[0]
        return self.tx_id

    def to_json(self):
        """For the API."""
        block_data = {
            'block_num': self.block_num,
            'closed': bool(self.closed),
            'merkle_root': self.merkle_root(),
            'tx_id': self.tx_id,
            'leaves': self.merkle_tree.leaves
        }

        return block_data
