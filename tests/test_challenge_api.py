import json
from flask import Flask
import os
import pytest

from src.core.challenge_api import api as backend_challenge_api


@pytest.fixture()
def app():
    app = Flask("Backend Challenge API")
    app.testing = True
    app.register_blueprint(backend_challenge_api, url_prefix="/backend")
    yield app


def test_vehicle_features_post(app):
    print()
    # testing normal cases
    with open("json/vehicle-features.v1.example.json", "r") as file:
        data = file.read()

    with app.test_client() as tc:
        print("testing post with json")
        response = tc.post("/backend/challenge", json=json.loads(data))
        assert response.status_code == 200
        assert os.path.isfile(response.data)

        print("testing post with data")
        response = tc.post("/backend/challenge", data=data)
        assert response.status_code == 200
        assert os.path.isfile(response.data)


def test_vehicle_features_post_broken(app):
    # testing invalid JSON handling
    with open("json/vehicle-features.v1.example.broken.json", "r") as file:
        data = file.read()

    with app.test_client() as tc:
        print("testing post with broken json")
        response = tc.post("/backend/challenge", data=data)
        assert response.status_code == 400
        assert not os.path.isfile(response.data)


def test_vehicle_features_post_invalid_vin(app):
    # testing file creation exception
    with open("json/vehicle-features.v1.example.invalid_vin.json", "r") as file:
        data = file.read()

    with app.test_client() as tc:
        print("testing post with invalid vin")
        response = tc.post("/backend/challenge", data=data)
        assert response.status_code == 500
        assert not os.path.isfile(response.data)
