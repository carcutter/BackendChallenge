import json
import pytest
from flask import Flask
from io import BytesIO
from src.core.challenge_api import api as backend_challenge_api


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(backend_challenge_api, url_prefix="/backend")
    client = app.test_client()

    yield client


def test_vehicle_features_post_success(client):
    data = {
        "vehicles": [
            {
                "id": "1234",
                "features": [{"feature": "air-conditioning", "description": {"short": "AC", "long": "Air conditioning for hot days"}}],
            }
        ]
    }

    response = client.post("/backend/challenge", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 200
    assert json.loads(response.data)["success"] == True


def test_vehicle_features_post_missing_vehicles(client):
    data = {}

    response = client.post("/backend/challenge", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    assert json.loads(response.data)["error"] == "Missing required field 'vehicles'"


def test_vehicle_features_post_missing_id(client):
    data = {
        "vehicles": [
            {
                "features": [{"feature": "air-conditioning", "description": {"short": "AC"}}],
            }
        ]
    }

    response = client.post("/backend/challenge", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    assert json.loads(response.data)["error"] == "Vehicle id missing"


def test_vehicle_features_post_invalid_content_type(client):
    data = {
        "vehicles": [
            {
                "id": "1234",
                "features": [{"feature": "air-conditioning", "description": {"short": "AC"}}],
            }
        ]
    }

    response = client.post("/backend/challenge", data=json.dumps(data), content_type="text/plain")
    assert response.status_code == 400
    assert json.loads(response.data)["error"] == "Invalid content type: text/plain"


def test_vehicle_features_post_multipart_form_data(client):
    data = {
        "vehicles": [
            {
                "id": "1234",
                "features": [{"feature": "air-conditioning", "description": {"short": "AC"}}],
            }
        ]
    }
    data_str = json.dumps(data)
    data_bytes = BytesIO(data_str.encode("utf-8"))
    response = client.post("/backend/challenge", content_type="multipart/form-data", data={"data": (data_bytes, "data.json")})

    assert response.status_code == 200
    assert json.loads(response.data)["success"] == True
