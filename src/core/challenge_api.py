from flask import Blueprint, make_response, request
from flask.wrappers import Response
from http import HTTPStatus
from os import getenv

from utils.storage import Storage
from utils.api_decorators import ApiDecorators
from utils.debug import debug

api = Blueprint("challenge_api", __name__)


@api.route("/challenge", methods=["POST"])
@ApiDecorators.require_customer_id
@ApiDecorators.validate_json_data("json/vehicle-features.v1.schema.json")
@ApiDecorators.validate_uniqueness("vehicles", "id")
@ApiDecorators.validate_max_count("vehicles", "id", int(getenv("MAX_VEHICLES_COUNT", default=10)))
def vehicle_features_post(user_id: str) -> Response:
    """
    Customers will post some json data to this route, and we want to store each `Vehicle` in the `Vehicle-List`
    to a single file.
    This file should be stored to a folder named like the `user_id` and the filename should be the `id`
    with a ".json" extension.

    :param user_id:     The id of the customer sending the request
    :type:              str

    :return:            Response from API-route
    :rtype:             Response
    """

    json_data = request.get_json()

    storage = Storage(storage_folder=getenv("VEHICLES_STORAGE_FOLDER", default="./"))

    stored_vehicles = 0
    for vehicle in json_data.get("vehicles", []):
        if storage.save_entity(user_id=user_id, key="id", json_data=vehicle) is True:
            stored_vehicles += 1
        else:
            debug(f"Error: Vehicle for customer '{user_id}' could not be stored")
            return make_response(HTTPStatus.INTERNAL_SERVER_ERROR.phrase, HTTPStatus.INTERNAL_SERVER_ERROR.value)

    debug(f"Stored vehicles for customer '{user_id}': {stored_vehicles}")

    return make_response(HTTPStatus.CREATED.phrase, HTTPStatus.CREATED.value)
