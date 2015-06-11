from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


# Initialize the Flask application
app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)


class DataHash(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uhash = db.Column(db.String(128), unique=True)
    block = db.Column(db.Integer)

    def __init__(self, uhash, block=None):
        """A hashed data object."""
        self.uhash = uhash
        self.block = block

    def __repr__(self):
        return '<Hash: %r>' % self.uhash

    def is_sha256(self):
        """Make sure this is actually an valid SHA256 hash."""
        digits58 = '0123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        for i in range(len(self.uhash)):
            if not self.uhash[i] in digits58:
                return False
        return len(self.uhash) == 64

    def check_db(self):
        """Make sure there is no duplicate hash."""
        return self.query.filter_by(uhash=self.uhash).first()

    def to_db(self):
        """Insert hash into the database."""

        # Check for duplicates and get latest block number
        block_num = self.check_db()
        last_block = 0  # latest_block(self.conn)

        # If not duplicate then insert
        if block_num is None:
            db.session.add(self)
            db.session.commit()
            return last_block
        else:
            # It is a duplicate so return its block number
            return block_num.block
