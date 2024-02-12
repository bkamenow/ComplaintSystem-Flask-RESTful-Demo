import json

from flask_testing import TestCase

from config import create_app
from db import db


class TestApp(TestCase):
    def create_app(self):
        return create_app("config.TestingConfig")

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_protected(self):
        for method, url in [
            ("PUT", "/approvers/complaints/1/approve"),
            ("PUT", "/approvers/complaints/1/reject"),
            ("GET", "/complainers/complaints"),
            ("POST", "/complainers/complaints"),
        ]:
            if method == "POST":
                resp = self.client.post(url, data=json.dumps({}),)
            elif method == "GET":
                resp = self.client.get(url)
            elif method == "PUT":
                resp = self.client.put(url, data=json.dumps({}),)
            else:
                resp = self.client.delete(url)
            self.assert401(resp, {'message': 'Invalid or missing token'})
