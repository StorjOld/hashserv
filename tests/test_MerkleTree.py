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

    # generic test from @maraoz
    def generic_content_test(self, data, ans):
        tree = MerkleTree()
        for datum in data:
            tree.add_content(datum)
        result = tree.merkle_root()
        self.assertEqual(result, ans)

    def generic_hash_test(self, data, ans):
        tree = MerkleTree()
        for datum in data:
            tree.add_hash(datum)
        result = tree.merkle_root()
        self.assertEqual(result, ans)

    def test_merkle_bitcoin_vectors(self):
        # merkletree for livenet block 000000000003ba27aa200b1cecaad478d2b00432346c3f1f3986da1afd33e506
        txs = [
            "8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87",
            "fff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4",
            "6359f0868171b1d194cbee1af2f16ea598ae8fad666d9b012c8ed2b79a236ec4",
            "e9a66845e05d5abc0ad04ec80f774a7e585c6e8db975962d069a522137b80c1d",
        ]

        ans = 'f3e94742aca4b5ef85488dc37c06c3282295ffec960994b2c0d5ac2a25a95766'
        self.generic_hash_test(txs, ans)

    def test_merkle_node_vectors(self):
        # see https://github.com/maraoz/merkle/blob/sha256/test/main.js#L32
        data = ['a', 'b', 'c', 'd', 'e']
        ans = '16e6beb3e080910740a2923d6091618caa9968aead8a52d187d725d199548e2c'
        self.generic_content_test(data, ans)
