import unittest
import urllib.request
from hashserv.app import app
from hashserv.app import init_db


url = "http://localhost:5000/"


class EndPointsTest(unittest.TestCase):
    def run_api(self, api):
        return urllib.request.urlopen(url.format(api))

    def setUp(self):
        # create database
        init_db()

    #def test_check_connection(self):
    #    try:
    #        self.run_api("")
    #        self.assertTrue(True)
    #    except ConnectionRefusedError:
    #        self.assertTrue(False)
    #    except urllib.error.URLError:
    #        self.assertTrue(False)