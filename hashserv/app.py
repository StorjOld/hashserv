import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import sqlite3
from contextlib import closing
from flask import Flask, jsonify, render_template, make_response

# Application imports
from hashserv.DataHash import DataHash
from hashserv.DataBlock import DataBlock
from hashserv.DataBlock import latest_block


# Initialize the Flask application
app = Flask(__name__)
app.config.from_pyfile('config.py')


# Database code
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


# Routes
@app.route('/')
def index():
    """Displays a searchable list of blocks."""
    num_blocks = latest_block(connect_db())
    if num_blocks <= 5:
        num_show = 0
    else:
        num_show = num_blocks - 5
    return render_template('index.html', num_blocks=num_blocks, num_show=num_show)


@app.route('/api/submit/<sha256_hash>')
def submit(sha256_hash):
    """Submit a SHA256 hash to an most recent open block."""
    datahash = DataHash(sha256_hash, connect_db())
    if not datahash.is_sha256():
        return make_response("400: Invalid SHA256 Hash.", 400)
    else:
        return make_response(str(datahash.to_db()), 200)


@app.route('/api/proof/<sha256_hash>')
def proof(sha256_hash):
    """Get the Merkle proof for the hash."""
    conn = connect_db()

    datahash = DataHash(sha256_hash, conn)
    num_block = datahash.check_db()

    if num_block is None:
        return make_response("Hash Not Found.", 404)
    else:
        block = DataBlock(int(num_block[2]), conn)
        hash_proof = block.merkle_proof(sha256_hash)

        if not block.is_closed():
            return "Block Not Closed."

        json_proof = {
            'target': sha256_hash,
            'merkle_root': block.merkle_root(),
            'proof': hash_proof.get_json(),
            'tx_id': block.get_tx_id()
        }
        return make_response(jsonify(json_proof), 200)


@app.route('/api/block/generate')
def close_block():
    """Closes the current block and starts a new one."""
    conn = connect_db()
    last_block = latest_block(conn)
    block = DataBlock(last_block, conn)
    return str(block.generate_block())


@app.route('/api/block/<int:block_num>')
def show_block(block_num):
    """Shows the metadata for a particular block."""
    try:
        block = DataBlock(block_num, connect_db())
        block.find_leaves()  # load object from db
        block.get_tx_id()
        return make_response(jsonify(block.to_json()), 200)
    except LookupError:
        return make_response("Empty Block.", 204)
    except ValueError:
        return make_response("Invalid Parameter.", 400)
    except OverflowError:
        return make_response("Invalid Parameter. Integer Too Large.", 400)


@app.route('/api/block/latest')
def latest():
    """Returns the latest block number."""
    return str(latest_block(connect_db()))


if __name__ == '__main__':
    # Run the Flask app
    app.run(
        host="0.0.0.0",
        port=int("5000"),
        debug=True
    )
