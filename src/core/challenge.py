from flask import Blueprint, make_response
from utils.api_decorators import ApiDecorators

api = Blueprint("flutter_api", __name__)


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

    return make_response("OK", 200)
