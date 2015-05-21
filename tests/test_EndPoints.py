import time
import random
import unittest
import urllib.request
from hashserv.MerkleTree import sha256


url = "http://localhost:5000/"


class EndPointsTest(unittest.TestCase):
    def run_api(self, api):
        return urllib.request.urlopen(url.format(api))

    def test_check_connection(self):
        try:
            self.run_api("")
            self.assertTrue(True)
        except urllib.error.URLError:
            self.assertTrue(False)
