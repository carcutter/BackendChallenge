from flask import Blueprint, make_response, request
import json
import os

from utils.api_decorators import ApiDecorators
from utils.schema import schema

DATA_DIRECTORY = "uploaded_data"

api = Blueprint("challenge_api", __name__)

with open("json/vehicle-features.v1.schema.json") as f:
    vehicle_features_schema = json.load(f)


@api.route("/challenge", methods=["POST"])
@schema.validate(vehicle_features_schema)
@ApiDecorators.require_customer_id
def vehicle_features_post(user_id: str):
    """
    Please see the README.md
    Also see `json/vehicle-features.v1.schema.json` and `json/vehicle-features.v1.example.json`

    Customers will post some json data to this route, and we want to store each `Vehicle` in the `Vehicle-List` to a single file.
    This file should be stored to a folder named like the `user_id` and the filename should be the `id` with a ".json" extension.

    :param user_id: The id of the customer sending the request
    :return: json dict with vehiclesSaved set as the number of vehicles saved
    """

    file_path = os.path.join(DATA_DIRECTORY, user_id)

    if not os.path.exists(file_path):
        os.makedirs(file_path)

    request_json = request.get_json()

    for vehicle in request_json["vehicles"]:
        with open(os.path.join(file_path, f'{vehicle["id"]}.json'), "w") as vehicle_file:
            json.dump(vehicle, vehicle_file)

    return make_response({"vehiclesSaved": len(request_json["vehicles"])}, 201)
