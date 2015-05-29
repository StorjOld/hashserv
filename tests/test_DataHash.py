from flask import Flask
from hashserv.DataHash import DataHash
from flask.ext.testing import TestCase

from hashserv.DataHash import db


class DataHashTest(TestCase):

    SQLALCHEMY_DATABASE_URI = "sqlite:///C:/db/hashserv_test.db"
    TESTING = True

    def test_valid_sha256(self):
        valid_hash = '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08'
        data = DataHash(valid_hash)
        self.assertTrue(data.is_sha256())

        invalid_hash = 'notarealhash'
        data = DataHash(invalid_hash)
        self.assertFalse(data.is_sha256())

    def create_app(self):
        # pass in test configuration
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

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