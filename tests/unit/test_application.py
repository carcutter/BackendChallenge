from flask import Flask
from flask_cors import CORS

from src.core.challenge_api import api as backend_challenge_api
from src.applications.api_server import vehicle_features

import json


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(backend_challenge_api, url_prefix="/backend")
    return app


def test_posting_invalid_data():
    app = create_app()
    with app.test_client() as client:
        response = client.post("/backend/challenge")
        assert response.status_code == 400
        response = client.post("/backend/challenge", json={"vehicles": [{"id": "","features": [{"feature": "ENGINE","description": {"short": "5.2 Liter V8"}}]}]})
        assert response.status_code == 400

def test_posting_valid_data():
	app = create_app()
	with app.test_client() as client:
		with open('json/vehicle-features.v1.example.json', 'r') as f:
			json_data = json.load(f)
		response = client.post("/backend/challenge", json=json_data)
		assert response.status_code == 201
		
