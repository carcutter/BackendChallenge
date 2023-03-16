from threading import Thread
from flask import Blueprint, make_response, current_app as app, request
from utils.api_decorators import ApiDecorators
from werkzeug.utils import secure_filename

from pathlib import Path
import json, os

# used low number for easy the testing, otherwise this numbers could be in 100 000s
MAX_VEHICLE_COUNT = 10

api = Blueprint("challenge_api", __name__)

challenge_schema_filename = "schemas/vehicle-features.v1.schema.json"
challenge_schema_abs_path = os.path.join(api.root_path, challenge_schema_filename)

with open(challenge_schema_abs_path, "r") as f:
    vehicle_feature_schema = json.load(f)


def save_vehicle_to_json_file(filename, json_data):
    # Overwrite the file
    with open(filename, "w") as outfile:
        json.dump(json_data, outfile, ensure_ascii=False)


@api.route("/challenge", methods=["POST"])
@ApiDecorators.require_customer_id
@ApiDecorators.validate_vehicle_schema(vehicle_feature_schema)
# Actually it would be better to limit the content length, this is just for demonstration purpose
# By default, there is no limit, but huge file could crash the server
@ApiDecorators.limit_vehicle_number(MAX_VEHICLE_COUNT)
def vehicle_features_post(user_id: str):
    """
    Please see the README.md
    Also see `json/vehicle-features.v1.schema.json` and `json/vehicle-features.v1.example.json`

    Customers will post some json data to this route, and we want to store each `Vehicle` in the `Vehicle-List` to a single file.
    This file should be stored to a folder named like the `user_id` and the filename should be the `id` with a ".json" extension.

    :param user_id: The id of the customer sending the request
    :return: Dict of vehicle file(s) created/updated

    """
    # I added this parent folder to make it clearer where are the stored folders
    STORED_VEHICLES_FOLDER = os.path.join(api.root_path, "stored_vehicles_per_user_id", user_id)
    if not os.path.exists(STORED_VEHICLES_FOLDER):
        os.makedirs(STORED_VEHICLES_FOLDER)

    # message contains files and status of file "Updated" or "Created"
    log_message = {}
    data = request.get_json()
    app.logger.info("%d number of vehicle", len(data["vehicles"]))

    for vehicle in data["vehicles"]:
        # best practice not to trust client
        secure_vehicle_id = secure_filename(f'{vehicle["id"]}.json')
        vehicle_file_name = os.path.join(STORED_VEHICLES_FOLDER, secure_vehicle_id)
        if os.path.exists(vehicle_file_name):
            log_message[vehicle["id"]] = {"filename": vehicle_file_name, "status": "Updated"}
        else:
            log_message[vehicle["id"]] = {"filename": vehicle_file_name, "status": "Created"}
        # if we were certain that the ids are unique, we could use multithreading for io task in parallel
        save_vehicle_to_json_file(vehicle_file_name, vehicle)

    app.logger.info("%d number of vehicles with unique id: ", len(log_message))
    app.logger.info(log_message)
    message = {"message": "The item(s) was created successfully"}
    response = app.response_class(response=json.dumps(message), status=201, mimetype="application/json")
    return response
