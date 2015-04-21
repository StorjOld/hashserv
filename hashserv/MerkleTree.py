import hashlib

class MerkleProof:
	def __init__(self, left, right):
		pass

class MerkleTree:

	def __init__(self):
		"""Simplistic merkle tree. Defaults to sha256."""
		self.leaves = []

	def sha256(self, content):
		"""Finds the sha256 hash of the content."""
		content = content.encode('utf-8')
		return hashlib.sha256(content).hexdigest()

	def hash_f(self, content):
		"""Calcuate the hash of the content."""
		return self.sha256(content)

	def add_content(self, content):
		"""Hashes a content string and adds to the leaves."""
		self.leaves.append(self.hash_f(content))

	def add_hash(self, ahash):
		"""Adds a single hash to the to the leaves."""
		self.leaves.append(ahash)

	def merkle_root(self):
		"""Take a list of hashes, and return the root merkle hash."""
		# Generate list we can mutate
		hashes = self.leaves

		# Reduce list till we have a merkle root
		while len(hashes) > 1:
			hashes = self.merkle_pair(hashes)
		return hashes[0]

	def merkle_pair(self, hashes, target = None):
		"""
		Take a list of hashes, and return the parent row in the tree
		of merkle hashes. Optionally takes a target, in which case it
		will return a branch of the proof.
		"""
		# if odd then append first entry to the end of the list
		if len(hashes) % 2 == 1:
			hashes = list(hashes)
			hashes.append(hashes[-1])
		l = []
		for i in range(0, len(hashes), 2):
			l.append(self.hash_f(hashes[i] + hashes[i+1]))
			if target == hashes[i] or target == hashes[i+1]:
				new_target = self.hash_f(hashes[i] + hashes[i+1])
				return (new_target, hashes[i], hashes[i+1])
		return l

	def merkle_proof(self, target):
		"""Gives the merkle proof of a particular leaf in the root."""
		# Generate list we can mutate
		hashes = self.leaves
		proof = []

		# Reduce list till we have a merkle root, but extra target
		while len(hashes) > 1:
			pair = self.merkle_pair(hashes, target)
			proof.append(pair)
			target = pair[0]
			hashes = self.merkle_pair(hashes)

		return proof