from hashserv.MerkleTree import MerkleTree


class DataBlock:
    def __init__(self, block_num, conn=None):
        """Validating and inserting data hashes into the database."""
        self.block_num = int(block_num)
        self.merkle_tree = MerkleTree()
        self.closed = False
        self.tx_id = None
        self.conn = conn

    def close(self):
        """Close block, and generate Merkle root."""
        self.closed = True

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

    def generate(self):
        pass