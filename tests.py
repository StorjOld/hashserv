import unittest
from hashserv import *
from tests import MerkleTree_test

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(MerkleTree_test)
	unittest.TextTestRunner(verbosity=2).run(suite)