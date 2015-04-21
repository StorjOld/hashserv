import sqlite3
from flask import Flask, g

# Application imports
from hashserv.MerkleTree import MerkleTree


# Initialize the Flask application
app = Flask(__name__)
app.config['DATABASE'] = '/db/hashserv.db'


# Database code
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


class DataBlock:
    def __init__(self, block_num):
        """Validating and inserting data hashes into the database."""
        self.block_num = block_num

    def find_items(self):
        # Connect
        g.db = connect_db()

        """Get the items for this block."""
        query = 'SELECT * FROM hash_table where block=?'
        # ORDER BY id DESC
        cur = g.db.execute(query, (self.block_num,))

        items = []
        for row in cur.fetchall():
            items.append(row[1])
        return items

    def get_merkle_root(self):
        tree = MerkleTree()
        tree.leaves = self.find_items()
        return tree.merkle_root()

    def __str__(self):
        output = "Merkle Root:<br>"
        output += self.get_merkle_root()
        output += "<br><br>Hashes:<br>"
        for item in self.find_items():
            output += item
            output += "<br>"
        return output
