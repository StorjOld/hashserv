import unittest
from hashserv.MerkleTree import sha256
from hashserv.DataBlock import DataBlock

class DataBlockTest(unittest.TestCase):

    def test_create_data_block(self):
        block = DataBlock(1)

        block.merkle_tree.add_hash(sha256("test"))
        block.merkle_tree.add_hash(sha256("test2"))
        block.merkle_tree.add_hash(sha256("test3"))

        ans = 'd49e815a91a26d399f8c2fba429e6ef7e472e54b6eb1e04341d207eee219f6c0'

        block.close()
        self.assertEqual(block.merkle_root(), ans)