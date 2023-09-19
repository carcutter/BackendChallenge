from flask import Blueprint, make_response, request, jsonify
import json
import os
from utils.api_decorators import ApiDecorators

api = Blueprint("challenge_api", __name__)


@api.route("/challenge", methods=["POST"])
@ApiDecorators.require_customer_id
def vehicle_features_post(user_id: str):
    try:
        data = None

        # Handle 'application/json' content type
        if request.content_type == "application/json":
            data = request.get_json()

        # Handle 'multipart/form-data' content type
        elif request.content_type.startswith("multipart/form-data"):
            file_str = request.files["data"].read().decode("utf-8")
            data = json.loads(file_str)

        if data is None:
            return make_response(jsonify({"error": f"Invalid content type: {request.content_type}"}), 400)

        vehicles = data.get("vehicles")

        if not vehicles:
            return make_response(jsonify({"error": "Missing required field 'vehicles'"}), 400)

        directory = f"./{user_id}"
        if not os.path.exists(directory):
            os.makedirs(directory)

        for vehicle in vehicles:
            vehicle_id = vehicle.get("id")
            if not vehicle_id:
                return make_response(jsonify({"error": "Vehicle id missing"}), 400)

            with open(f"{directory}/{vehicle_id}.json", "w") as f:
                json.dump(vehicle, f)

        return make_response(jsonify({"success": True}), 200)

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)
