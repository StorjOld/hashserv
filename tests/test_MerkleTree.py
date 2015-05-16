import unittest
from hashserv.MerkleTree import sha256
from hashserv.MerkleTree import MerkleTree
from hashserv.MerkleTree import MerkleBranch
from hashserv.MerkleTree import MerkleProof


class MerkleTreeTest(unittest.TestCase):
    def test_simple_sha256(self):
        tree = MerkleTree()
        result = tree.hash_f("test")
        ans = '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08'
        self.assertEqual(result, ans)

    def test_two_even_items(self):
        tree = MerkleTree()
        tree.add_content("test")
        tree.add_hash(tree.hash_f("test2"))
        result = tree.merkle_root()

        ans = '694299f8eb01a328732fb21f4163fbfaa8f60d5662f04f52ad33bec63953ec7f'
        self.assertEqual(result, ans)

    def test_tree_odd_items(self):
        tree = MerkleTree()
        tree.add_content("test")
        tree.add_content("test2")
        tree.add_content("test3")
        result = tree.merkle_root()

        ans = 'd49e815a91a26d399f8c2fba429e6ef7e472e54b6eb1e04341d207eee219f6c0'
        self.assertEqual(result, ans)

    def test_large_tree(self):
        tree = MerkleTree()
        for i in range(10000):
            tree.add_content(str(i))
        ans = 'a048d580177b80a60cbd31355400a0c9eabb5d2d3a4704fc9c86bae277f985c7'
        self.assertEqual(tree.merkle_root(), ans)

    def test_merkle_branch(self):
        left = sha256("test")
        right = sha256("test2")
        branch = MerkleBranch(left, right)

        ans = '694299f8eb01a328732fb21f4163fbfaa8f60d5662f04f52ad33bec63953ec7f'
        self.assertEqual(branch.get_parent(), ans)

    def test_proof_true(self):
        tree = MerkleTree()

        tree.add_content("test")
        tree.add_content("test2")
        tree.add_content("test3")

        proof = tree.merkle_proof(sha256("test"))
        self.assertTrue(proof.is_valid())

    def test_proof_false1(self):
        tree = MerkleTree()

        tree.add_content("test1")
        tree.add_content("test2")
        tree.add_content("test3")

        proof = tree.merkle_proof(sha256("test"))
        self.assertFalse(proof.is_valid())

    def test_proof_false2(self):
        tree = MerkleTree()

        tree.add_content("test")
        tree.add_content("test2")
        tree.add_content("test3")

        proof = tree.merkle_proof(sha256("test4"))
        self.assertFalse(proof.is_valid())

    def test_proof_single_true(self):
        tree = MerkleTree()
        tree.add_content("test")
        proof = tree.merkle_proof(sha256("test"))
        self.assertTrue(proof.is_valid())

    def test_proof_single_false(self):
        tree = MerkleTree()
        tree.add_content("test")
        proof = tree.merkle_proof(sha256("test9"))
        self.assertFalse(proof.is_valid())

    def test_merkle_proof_simple_true(self):
        tree = MerkleTree()
        tree.add_content("test")
        tree.add_content("test2")

        left = sha256("test")
        right = sha256("test2")
        branch = MerkleBranch(left, right)

        target = left
        proof = MerkleProof(target, tree)
        proof.add(branch)
        self.assertTrue(proof.is_valid())

    def test_merkle_proof_simple_false(self):
        tree = MerkleTree()
        tree.add_content("test")
        tree.add_content("test2")

        left = sha256("test")
        right = sha256("test2")
        branch = MerkleBranch(left, right)

        target = sha256("notinproof")
        proof = MerkleProof(target, tree)
        proof.add(branch)
        self.assertFalse(proof.is_valid())
