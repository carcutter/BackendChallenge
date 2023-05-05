from flask import Blueprint, make_response, request

try:
    from utils.api_decorators import ApiDecorators
    from utils.utils import UserValidator, ValidateUniqueValues, store, LogLevel, Logger
except:
    from src.utils.api_decorators import ApiDecorators
    from src.utils.utils import UserValidator, ValidateUniqueValues, store, LogLevel, Logger
from flask_expects_json import expects_json
import json

api = Blueprint("challenge_api", __name__)

with open("json/vehicle-features.v1.schema.json") as file:
    file_contents = file.read()
parsed_schema = json.loads(file_contents)


@api.route("/challenge", methods=["POST"])
@ApiDecorators.require_customer_id
@expects_json(parsed_schema)
def vehicle_features_post(user_id: str):
    """
    Customers will post some json data to this route, and we want to store each `Vehicle` in the `Vehicle-List` to a single file.
    This file should be stored to a folder named like the `user_id` and the filename should be the `id` with a ".json" extension.

    :param str user_id: The id of the customer sending the request
    :return: 201 if successful, 40x if bad request, 500 if internal server error
    """

    data = request.get_json()

    if not ValidateUniqueValues(data):
        Logger(LogLevel.INFO, f"Failed validation for {user_id}'s posted data")
        return make_response("Bad request", 400)

    if not UserValidator(user_id):
        Logger(LogLevel.WARNING, f"Failed authentication on {user_id}'s posted data")
        return make_response("Unauthorized", 401)

    try:
        store(user_id, data)
    except Exception as e:
        Logger(LogLevel.ERROR, f"Failed storing {user_id}'s posted data")
        return make_response("Internal server error", 500)

    return make_response("OK", 201)
