import unittest
from hashserv.MerkleTree import MerkleTree

class MerkleTree_Test(unittest.TestCase):

	def test_simple_sha256(self):
		tree = MerkleTree()
		result = tree.sha256("test")
		result2 = tree.hash_f("test")
		ans = '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08'
		self.assertEqual(result, ans)
		self.assertEqual(result2, ans)

	def test_two_even_items(self):
		tree = MerkleTree()
		tree.add_content("test")
		tree.add_content("test2")
		result = tree.merkle_root()
	
		ans = '694299f8eb01a328732fb21f4163fbfaa8f60d5662f04f52ad33bec63953ec7f'
		self.assertEqual(result, ans)

		target = tree.hash_f("test")
		proof = tree.merkle_proof(target)
		self.assertEqual(proof[0][0], ans)

	def test_tree_odd_items(self):
		tree = MerkleTree()
		tree.add_content("test")
		tree.add_content("test2")
		tree.add_content("test3")
		result = tree.merkle_root()
	
		ans = 'd49e815a91a26d399f8c2fba429e6ef7e472e54b6eb1e04341d207eee219f6c0'
		self.assertEqual(result, ans)

		target = tree.hash_f("test3")
		proof = tree.merkle_proof(target)
		self.assertEqual(proof[1][0], ans)