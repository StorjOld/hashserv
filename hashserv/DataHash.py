class DataHash:
    def __init__(self, ahash, conn=None):
        """Validating and inserting data hashes into the database."""
        self.conn = conn
        self.ahash = ahash

    def is_sha256(self):
        """Make sure this is actually an valid SHA256 hash."""
        digits58 = '0123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        for i in range(len(self.ahash)):
            if not self.ahash[i] in digits58:
                return False
        return len(self.ahash) == 64

    def to_db(self):
        """Insert hash into the database."""
        # Check for duplicates
        block_num = self.check_db()

        # If not duplicate then insert
        if block_num is None:
            query = "INSERT INTO hash_table (hash, block) VALUES (?, ?)"
            self.conn.execute(query, (self.ahash, 1,))
            self.conn.commit()
            return "1"  # magic int
        else:
            return block_num[2]

    def check_db(self):
        """Make sure there is no duplicate hash."""
        query = "SELECT * FROM hash_table WHERE hash=?"
        cur = self.conn.execute(query, (self.ahash,))
        return cur.fetchone()