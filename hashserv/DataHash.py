from hashserv.Database import latest_block


class DataHash:
    def __init__(self, ahash, conn=None):
        """A hashed data object."""
        self.conn = conn
        self.ahash = ahash

    def is_sha256(self):
        """Make sure this is actually an valid SHA256 hash."""
        digits58 = '0123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        for i in range(len(self.ahash)):
            if not self.ahash[i] in digits58:
                return False
        return len(self.ahash) == 64

    def check_db(self):
        """Make sure there is no duplicate hash."""
        query = "SELECT * FROM hash_table WHERE hash=?"
        cur = self.conn.execute(query, (self.ahash,))
        return cur.fetchone()

    def to_db(self):
        """Insert hash into the database."""

        # Check for duplicates and get latest block number
        block_num = self.check_db()
        last_block = latest_block(self.conn)

        # If not duplicate then insert
        if block_num is None:
            query = "INSERT INTO hash_table (hash, block) VALUES (?, ?)"
            self.conn.execute(query, (self.ahash, last_block,))
            self.conn.commit()
            return last_block
        else:
            # It is a duplicate so return its block number
            return block_num[2]
