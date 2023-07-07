from flask import Blueprint, make_response, request
from utils.api_decorators import ApiDecorators
from http import HTTPStatus
from utils.validation import validate_json
import aiofiles
import logging
import asyncio
import sys
import json
import os

api = Blueprint("challenge_api", __name__)
logging.basicConfig(stream=sys.stderr, level=logging.ERROR)


async def save_vehicle_async(user_id, vehicle):
    folder_path = os.path.join(os.getcwd(), user_id)
    os.makedirs(folder_path, exist_ok=True)

    file_name = f"{vehicle['id']}.json"
    file_path = os.path.join(folder_path, file_name)

    try:
        async with aiofiles.open(file_path, "w") as file:
            await file.write(json.dumps(vehicle))
    except Exception as e:
        logging.error(f"Error saving vehicle {vehicle['id']}: {e}")


def save_vehicle(user_id, vehicle_list):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [save_vehicle_async(user_id, vehicle) for vehicle in vehicle_list]
    loop.run_until_complete(asyncio.gather(*tasks))


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

    errors = validate_json(request)
    if errors:
        logging.error(errors)
        return make_response(
            HTTPStatus.BAD_REQUEST.phrase,
            HTTPStatus.BAD_REQUEST.value,
        )

    data = request.get_json()
    vehicle_list = data.get("vehicles")

    if user_id and vehicle_list:
        save_vehicle(user_id, vehicle_list)
        return make_response(HTTPStatus.CREATED.phrase, HTTPStatus.CREATED.value)
    else:
        return make_response(
            HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )
