import unittest
from hashserv.NewFile import NewFile

class NewFile_Test(unittest.TestCase):

	def test_success(self):
		newfile = NewFile('tests/random.txt', True)

		# Testing success
		ch = '969a5145d8b6ed3228e493fb7a66d07d3253be89af6094cf510986ebcd7d2fbd'
		newfile.process('tests/')
		self.assertTrue(newfile.processed)
		self.assertTrue(newfile.hash == ch)

	def test_fail(self):
		newfile = NewFile('tests/nothere.txt', True)

		# Testing fail
		newfile.process('tests/')
		self.assertTrue(not newfile.processed)


if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TestNewFile)
	unittest.TextTestRunner(verbosity=2).run(suite)