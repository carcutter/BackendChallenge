from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from http import HTTPStatus
import json
import pytest

from src.core.challenge_api import api as backend_challenge_api


DOTENV_PATH = "./.env.test"  # use path from root folder


@pytest.fixture()
def test_app():
    # load and parse the .env.cli file to environment variables
    load_dotenv(dotenv_path=DOTENV_PATH)

    app = Flask("Backend Challenge API Test")
    app.testing = True
    CORS(app)
    app.register_blueprint(backend_challenge_api, url_prefix="/backend")
    yield app


def test_api_endpoint_valid_data_case(test_app):
    with open("json/vehicle-features.v1.example.json", "r") as file:
        json_data = file.read()

    with test_app.test_client() as test_client:
        response = test_client.post("/backend/challenge", json=json.loads(json_data))
        assert response.status_code == HTTPStatus.CREATED.value
        assert response.text == HTTPStatus.CREATED.phrase


def test_api_endpoint_invalid_data_case_1(test_app):
    with open("json/vehicle-features.v2.example.json", "r") as file:
        json_data = file.read()

    with test_app.test_client() as test_client:
        response = test_client.post("/backend/challenge", json=json.loads(json_data))
        assert response.status_code == HTTPStatus.BAD_REQUEST.value
        assert response.text == "{\"error\":\"Vehicles (['VIN1', 'VIN1']) are not unique by 'id'\"}\n"


def test_api_endpoint_invalid_data_case_2(test_app):
    with open("json/vehicle-features.v3.example.json", "r") as file:
        json_data = file.read()

    with test_app.test_client() as test_client:
        response = test_client.post("/backend/challenge", json=json.loads(json_data))
        assert response.status_code == HTTPStatus.BAD_REQUEST.value
        assert response.text == '{"error":"Max vehicles count is 10, but 12 found"}\n'
