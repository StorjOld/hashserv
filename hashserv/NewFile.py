import os
import shutil
import hashlib
import sqlite3
from flask import Flask, g


# Initialize the Flask application
app = Flask(__name__)
app.config['DATABASE'] = '/db/hashserv.db'

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

class NewFile:
	def __init__(self, filepath, debug = False):
		self.filepath = filepath
		self.hash = None
		self.processed = False
		self.debug = debug
		self.size = 0

	def get_hash(self):
		"""Get the SHA256 hash of the file."""
		hasher = hashlib.sha256()
		with open(self.filepath, 'rb') as afile:
			buf = afile.read()
			hasher.update(buf)
		return hasher.hexdigest()

	def process(self, data_folder):
		"""Press and move to data folder."""
		try:
			self.hash = self.get_hash()

			# Generate path and filename for data folder
			data_path = os.path.join(data_folder, self.hash)

			# Get size of the file
			self.size = os.path.getsize(self.filepath)

			# Move the file from processing to data
			if not self.debug:
				shutil.move(self.filepath, data_path)

			# Update the new filepath
			self.filepath = data_path

			# File processed without error
			self.processed = True

			# Insert into DB
			self.to_db()
		except FileNotFoundError: 
			self.processed = False


	def to_db(self):
		# Connect to Database
		g.db = connect_db()

		# Do Query
		query = "insert into hash_table (hash, block) values (?, ?)"
		g.db.execute(query, (self.hash, 1,))
		g.db.commit()