import os
import shutil
import hashlib

class NewFile:
	def __init__(self, filepath, debug = False):
		self.filepath = filepath
		self.hash = None
		self.processed = False
		self.debug = debug

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

			# Move the file from processing to data
			if not self.debug:
				shutil.move(self.filepath, data_path)

			# Update the new filepath
			self.filepath = data_path

			# File processed without error
			self.processed = True
		except FileNotFoundError: 
			self.processed = False

	def to_db(self):
		"""Insert file info into the database."""
		raise NotImplemented