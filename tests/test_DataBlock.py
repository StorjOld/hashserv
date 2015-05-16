import unittest

from hashserv.MerkleTree import sha256
from hashserv.DataBlock import DataBlock


class DataBlockTest(unittest.TestCase):
    def test_create_empty_block(self):
        block = DataBlock(1)
        block.close()
        self.assertRaises(LookupError, block.merkle_root)

    def test_create_data_block(self):
        block = DataBlock(1)

        block.add_hash(sha256("test"))
        block.close()

        ans = '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08'
        self.assertEqual(block.merkle_root(), ans)

    def test_data_block_json(self):
        block = DataBlock(1)

        block.add_hash(sha256("test"))
        block.add_hash(sha256("test2"))
        block.add_hash(sha256("test3"))

        json_data = block.to_json()

        self.assertEqual(json_data['block_num'], 1)
        self.assertFalse(json_data['closed'])
        self.assertEqual(json_data['merkle_root'], None)
        self.assertEqual(json_data['tx_id'], None)
        self.assertEqual(len(json_data['leaves']), 3)

        # close block and try again
        block.close()

        json_data = block.to_json()
        ans = 'd49e815a91a26d399f8c2fba429e6ef7e472e54b6eb1e04341d207eee219f6c0'

        self.assertEqual(json_data['block_num'], 1)
        self.assertTrue(json_data['closed'])
        self.assertEqual(json_data['merkle_root'], ans)
        self.assertEqual(json_data['tx_id'], None)
        self.assertEqual(len(json_data['leaves']), 3)
