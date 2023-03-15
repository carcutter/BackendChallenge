from flask_script import Manager
from unittest import TestCase
from src.core.challenge_api import create_app


class FuncTest(TestCase):
    def setUp(self):
        self.app = create_app(config="test")
        self.client = self.app.test_client()

    def test_index(self):
        with open("json/vehicle-features.v1.example.json") as data:
            res = self.client.post("/challenge", data=data, content_type="application/json")
            assert res.status_code == 200


manager = Manager(create_app)
manager.add_option("-c", "--config", dest="config", required=False)
