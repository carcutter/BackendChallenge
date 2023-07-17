import json
import pytest
from flask import Flask
from flask_cors import CORS
from src.core.challenge_api import api as backend_challenge_api


@pytest.fixture
def create_successes():
    success_fixtures = [
        ("tests/fixtures/small-valid.json", 200, "a2840615-26d9-4bf7-8fc4-0bf769dd1a01", False),
    ]
    for (json_path, http_code, customer_id, expected_exception) in success_fixtures:
        app = Flask("Backend Challenge API Test")
        app.testing = True
        CORS(app)
        app.register_blueprint(backend_challenge_api, url_prefix="/backend")
        with open(json_path, "r") as json_fh:
            json_data = json.load(json_fh)

        yield (app, json_data, http_code, customer_id, expected_exception)
        # TODO: add finalizer to tear down the app


@pytest.fixture
def create_failures():
    success_fixtures = [
        ("json/vehicle-features.v1.example.json", 500, "a2840615-26d9-4bf7-8fc4-0bf769dd1a01", False),
    ]
    for (json_path, http_code, customer_id, expected_exception) in success_fixtures:
        app = Flask("Backend Challenge API Test")
        app.testing = True
        CORS(app)
        app.register_blueprint(backend_challenge_api, url_prefix="/backend")
        with open(json_path, "r") as json_fh:
            json_data = json.load(json_fh)

        yield (app, json_data, http_code, customer_id, expected_exception)
        # TODO: add finalizer to tear down the app


def test_successes(create_successes):
    (app, json_fixture, code, customer_id, exception) = create_successes
    with app.test_client() as client:
        # TODO: get url from app
        resp = client.post(f"/backend/challenge/{customer_id}", json=json_fixture)
        assert resp.status_code == code


def test_failures(create_failures):
    (app, json_fixture, code, customer_id, exception) = create_failures
    with app.test_client() as client:
        # TODO: get url from app
        resp = client.post(f"/backend/challenge/{customer_id}", json=json_fixture)
        assert resp.status_code == code
