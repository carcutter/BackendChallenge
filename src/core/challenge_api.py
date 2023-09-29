from flask import Blueprint, make_response, request, current_app
from utils.api_decorators import ApiDecorators
import os
import json
import jsonschema

api = Blueprint("challenge_api", __name__)


# if the schema need loading we do it
def load_schema():
    path = current_app.config["SCHEMA_PATH"]
    schema = current_app.config.get("CHALLENGE_SCHEMA")
    if not schema:
        with open(path, "r") as schema_file:
            schema = json.load(schema_file)
            current_app.config["CHALLENGE_SCHEMA"] = schema
            return schema
    else:
        return current_app.config["CHALLENGE_SCHEMA"]


@api.route("/challenge", methods=["POST"])
@ApiDecorators.require_customer_id
def vehicle_features_post(user_id: str):
    """
    Customers will post some json data to this route, and we want to store each `Vehicle` in the `Vehicle-List` to a single file.
    This file is stored to a folder named like the `user_id` and the filename is the `id` with a ".json" extension.
    The folders will be placed it the path set in the config under FILE_PATH.
    The posted json is validated against the schema under SCHEMA_PATH in the config.

    The max length of the posted json can be enforced by setting MAX_LENGHT in the config to a positive amount of bytes.

    :param user_id: The id of the customer sending the request
    :return: OK or an error string
    """

    # check that we don't get a too big request data
    #  not sure this is actually needed but just in case
    max_length = current_app.config["MAX_LENGHT"]
    if max_length > 0 and request.content_length > max_length:
        current_app.logger.error(f"too long request payload: {request.content_length}, max allowed: {max_length}")
        return make_response("content too long", 400)

    data = request.get_json(cache=False)

    # validate the content
    schema = load_schema()
    try:
        jsonschema.validate(data, schema)
    except jsonschema.exceptions.ValidationError as e:
        current_app.logger.error(f"invalid JSON content: {e}")
        return make_response("invalid JSON content", 400)

    # create folder if needed
    dir = os.path.join(current_app.config["FILE_PATH"], user_id)

    if not os.path.exists(dir):
        try:
            os.makedirs(dir)
            current_app.logger.debug(f"created {dir}")
        except os.error as e:
            current_app.logger.error(f"error creating folder {dir}: {e}")
            return make_response("Internal Error, oops", 500)

    # if valid against the schema we always have at least 1 item
    vlist = data.get("vehicles")
    for v in vlist:
        fpath = os.path.join(dir, v.get("id")) + ".json"
        try:
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(v, f, ensure_ascii=False, indent=2)
        except IOError as e:
            current_app.logger.error(f"error opening file  {fpath}: {e}")
            return make_response("Internal Error, oops", 500)

    return make_response("OK", 200)
