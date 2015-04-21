import sqlite3

from flask import Flask, g


# Initialize the Flask application
app = Flask(__name__)
app.config['DATABASE'] = '/db/hashserv.db'


# Database code
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


class DataHash:
    def __init__(self, ahash):
        """Validating and inserting data hashes into the database."""
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
        # Connect
        g.db = connect_db()

        # Check for duplicates

        block_num = self.check_db()
        if block_num is None:
            query = "insert into hash_table (hash, block) values (?, ?)"
            g.db.execute(query, (self.ahash, 1,))
            g.db.commit()
            return "1"
        else:
            return block_num[2]

    def check_db(self):
        """Make sure there is no duplicate hash."""
        # Find duplicate
        query = "SELECT * FROM hash_table WHERE hash=?"
        cur = g.db.execute(query, (self.ahash,))
        return cur.fetchone()