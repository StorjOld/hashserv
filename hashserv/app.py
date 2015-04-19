from flask import Flask, abort

# Application imports
from DataHash import DataHash

# Initialize the Flask application
app = Flask(__name__)

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation.
@app.route('/api/submit/<sha256_hash>')
def index(sha256_hash):
	
	datahash = DataHash(sha256_hash)
	if not datahash.is_sha256():
		return "400: Invalid SHA256 Hash."
	else:
		return datahash.to_db()

if __name__ == '__main__':
	# Run the Flask app
	app.run(
		host="0.0.0.0",
		port=int("5000"),
		debug=True
	)