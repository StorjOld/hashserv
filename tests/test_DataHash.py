import unittest
from hashserv.DataHash import DataHash

class DataHash_Test(unittest.TestCase):

	def test_valid_sha256(self):
		valid_hash = '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08'
		data = DataHash(valid_hash)
		self.assertTrue(data.is_sha256())

		invalid_hash = 'notarealhash'
		data = DataHash(invalid_hash)
		self.assertFalse(data.is_sha256())

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(DataHash_Test)
	unittest.TextTestRunner(verbosity=2).run(suite)