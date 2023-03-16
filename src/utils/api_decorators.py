from functools import wraps
from uuid import uuid4
from jsonschema import Draft4Validator
from flask import request, jsonify
from werkzeug.utils import secure_filename

import json


class ApiDecorators:
    def require_customer_id(f):
        """
        Check does request contain user_id parameter
        """

        @wraps(f)
        def wrapped(*args, **kwargs):
            if "user_id" in request.args and request.args["user_id"] is not None:
                # best practice not to trust client
                # TODO: discuss should we secure the user_id
                # !!! securing the user_id can change it !!!
                secure_user_id = secure_filename(request.args["user_id"])
                return f(secure_user_id, *args, **kwargs)
            else:
                response = jsonify(dict(success=False, message="invalid parameter, user_id is missing"))
                # Not Acceptable
                response.status_code = 406
                return response

        return wrapped

    def validate_vehicle_schema(schema):
        """
        Check does json payload comply to vehicle schema
        :param schema: Schema to validate payload against
        """
        validator = Draft4Validator(schema)

        def wrapper(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                input = request.get_json(force=True)
                errors = [error.message for error in validator.iter_errors(input)]
                # return errors response
                if errors:
                    response = jsonify(dict(success=False, message="Invalid payload", errors=errors))
                    # Not Acceptable
                    response.status_code = 406
                    return response
                # proceed to the function
                else:
                    return f(*args, **kwargs)

            return wrapped

        return wrapper

    def limit_vehicle_number(max_vehicle_count):
        """
        Check does json payload contain more vehicles in the list than acceptable
        :param max_vehicle_count: Maximum number of vehicles in vehicle list
        """

        def wrapper(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                data = request.get_json()
                if data is not None and len(data["vehicles"]) > max_vehicle_count:
                    response = jsonify(dict(success=False, message=f"Invalid payload. Max number of vehicles is {max_vehicle_count}"))
                    # Payload Too Large
                    response.status_code = 413
                    return response
                return f(*args, **kwargs)

            return wrapped

        return wrapper
