from flask import Blueprint, make_response, request, abort
from utils.api_decorators import ApiDecorators
from core.value_objects import CustomerId
from core.vehicle_list import VehicleList

from flask import current_app


api = Blueprint("challenge_api", __name__)


# TODO: could use werkzeug custom converters here
# TODO: POST, PUT, PATCH - one or more, depending on the business case/rules
@api.route("/challenge/<customer_id>", methods=["POST"])
@ApiDecorators.require_customer_id
def vehicle_features_post(customer_id: CustomerId):
    """
    Please see the README.md
    Also see `json/vehicle-features.v1.schema.json` and `json/vehicle-features.v1.example.json`

    Customers will post some json data to this route, and we want to store each `Vehicle` in the `Vehicle-List` to a single file.
    This file should be stored to a folder named like the `user_id` and the filename should be the `id` with a ".json" extension.

    :param user_id: The id of the customer sending the request
    :return: ???
    """
    raw_json = request.json

    try:
        vehicle_list = VehicleList(raw_json)
    except:
        return abort(500)

    current_app.logger.info(f"REQ: {raw_json}")

    # TODO Implement the challenge

    return make_response("OK", 200)
