from flask import Flask, jsonify

# Application imports
from hashserv.DataHash import DataHash
from hashserv.DataBlock import DataBlock

# Initialize the Flask application
app = Flask(__name__)


@app.route('/')
def index():
    return "hello world."


@app.route('/api/submit/<sha256_hash>')
def submit(sha256_hash):
    """Submit a hash to the queue."""
    datahash = DataHash(sha256_hash)
    if not datahash.is_sha256():
        return "400: Invalid SHA256 Hash."
    else:
        return datahash.to_db()


@app.route('/api/block/<block_num>')
def show_block(block_num):
    """Shows the metadata for a particular block."""
    block = DataBlock(block_num)
    return jsonify(block.to_json())


if __name__ == '__main__':
    # Run the Flask app
    app.run(
        host="0.0.0.0",
        port=int("5000"),
        debug=True
    )