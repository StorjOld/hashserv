import unittest
from flask import Flask
from hashserv.DataHash import db
from hashserv.DataHash import DataHash


class DataHashTest(unittest.TestCase):

    # start up
    def setUp(self):
        db.create_all()
        #block = DataBlock(1, 1)
        #db.session.add(block)
        #db.session.commit()

    def tearDown(self):
        db.session.remove()
        #db.drop_all()

    # test cases
    def test_valid_sha256(self):
        valid_hash = '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08'
        data = DataHash(valid_hash)
        self.assertTrue(data.is_sha256())

        invalid_hash = 'notarealhash'
        data = DataHash(invalid_hash)
        self.assertFalse(data.is_sha256())

    def test_insertion(self):
        valid_hash = '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08'

        data = DataHash(valid_hash)
        db.session.add(data)
        db.session.commit()

        # make sure the object is in session
        self.assertTrue(data in db.session)

        # save object to db
        data.to_db()

        print(data.check_db())
