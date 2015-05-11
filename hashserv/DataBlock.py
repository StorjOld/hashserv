from hashserv.DataHash import DataHash
from hashserv.MerkleTree import MerkleTree


def latest_block(conn):
    """Give us the lastest block number."""
    query = "SELECT Count(*) FROM block_table"
    cur = conn.execute(query)
    return int(cur.fetchone()[0])


class DataBlock:
    def __init__(self, block_num, conn=None):
        """Validating and inserting data hashes into the database."""
        self.block_num = int(block_num)
        self.merkle_tree = MerkleTree()
        self.closed = False
        self.tx_id = None

        self.conn = conn

    def close(self):
        """Close block, so a Merkle root can be generated."""
        self.closed = True

    def generate_block(self):
        """Close the current block, and generate a new one."""

        try:
            last_block = DataHash(None, self.conn).latest_block()
            latest_hash = DataHash(None, self.conn).latest_hash()

            # Get Merkle Root
            self.close()
            self.find_leaves()

            # Close current block
            c = self.conn.cursor()
            query1 = "UPDATE block_table SET end_hash=?, closed=?, merkle_root=? WHERE id=?"
            c.execute(query1, (latest_hash, True, self.merkle_root(), last_block))

            # Start new block
            query2 = "INSERT INTO block_table (start_hash) VALUES (?)"
            c.execute(query2, (latest_hash,))

            self.conn.commit()
            self.conn.close()
            return 'Block ' + str(last_block) + " Built."
        except LookupError:
            return 'Block ' + str(last_block) + " Empty."

    def is_closed(self):
        query = 'SELECT * FROM block_table where id=?'
        cur = self.conn.execute(query, (self.block_num,))
        block = cur.fetchone()
        self.closed = block[3]
        return self.closed

    def find_leaves(self):
        """Find leaves from database and generate tree."""

        """Get the items for this block."""
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
        """As long as its not closed add hash."""
        self.merkle_tree.add_hash(ahash)

    def merkle_root(self):
        """Find the data Merkle root."""
        if self.closed:
            return self.merkle_tree.merkle_root()

    def merkle_proof(self, target):
        """Find the Merkle proof of a target."""
        if self.closed:
            return self.merkle_tree.merkle_proof(target)

    def to_json(self):
        """For the API."""
        block_data = {
            'block_num': self.block_num,
            'closed': self.closed,
            'merkle_root': self.merkle_root(),
            'tx_id': self.tx_id,
            'leaves': self.merkle_tree.leaves
        }

        return block_data