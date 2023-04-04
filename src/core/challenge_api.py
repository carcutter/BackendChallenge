from flask import Blueprint, make_response, request, current_app
from utils.api_decorators import ApiDecorators
from pathlib import Path
import logging
import os
import json

api = Blueprint("challenge_api", __name__)


@api.route("/challenge", methods=["POST"])
@ApiDecorators.require_customer_id
def vehicle_features_post(user_id: str):
    """
    Please see the README.md
    Also see `json/vehicle-features.v1.schema.json` and `json/vehicle-features.v1.example.json`

    Customers will post some json data to this route, and we want to store each `Vehicle` in the `Vehicle-List` to a single file.
    This file should be stored to a folder named like the `user_id` and the filename should be the `id` with a ".json" extension.

    :param user_id: The id of the customer sending the request
    :return: ???
    """

    # TODO Implement the challenge

    try:
        data = request.json
    except:
        # fallback to parse request.data
        try:
            jsn = '{"vehicle"' + request.data.decode("utf-8").split('"vehicle"', 1)[1].split("--------------")[0]
            data = json.loads(jsn)
        except Exception as e:
            logging.warning(f"Non-JSON input received!: {str(e)}")
            return make_response("Error parsing JSON!", 400)

    try:
        Path(user_id).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        # or some more advanced error handling
        logging.warning(f"Creating directory {os.getcwd()}/{user_id} failed! : {str(e)}")
        return make_response("Internal Server Error", 500)

    for vehicle in data["vehicle"]:
        if "id" in vehicle:
            filename = user_id + "/" + vehicle["id"] + ".json"
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(vehicle, f, ensure_ascii=False, indent=4)
            except Exception as e:
                # or some more advanced error handling
                logging.warning(f"Creating file {os.getcwd()}/{filename} failed! : {str(e)}")
                return make_response("Internal Server Error", 500)
        else:
            return make_response("Error parsing JSON, {id} field missing}!", 400)

    data = filename if current_app.testing else "OK"  # to allow testing if file exists

    return make_response(data, 200)
