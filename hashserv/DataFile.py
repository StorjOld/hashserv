import mimetypes

class DataFile:
	def __init__(self, filehash):
		self.hash = filehash

	def check_sha256(self):
		"""Make sure this is actually an SHA256 hash."""
		digits58 = '0123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
		for i in range(len(self.hash)):
			if not self.hash[i] in digits58: return False
		return len(self.hash) == 64

	def find_ext(self, extension):
		"""Find mimtype from passed extension."""
		try:
			mimetypes.init()
			mapped_mimetype = mimetypes.types_map["." + extension]
		except KeyError:
			return "415 Unsupported Media Type."

	def get_hash(self):
		return self.hash

if __name__ == "__main__":
	ahash = '5bdc1ba967bfb21c6b558323b009fccbfc60e75caf07d7df82bf14060489fa74'
	print(len(ahash))
	data = DataFile(ahash)
	print(data.check_sha256())