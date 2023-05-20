from flask import jsonify, request
from functools import wraps
from http import HTTPStatus
from typing import Any, Callable, Dict, List, Tuple, Union

from core.customer import Customer
from utils.validator import Validator
from utils.debug import debug


class ApiDecorators:
    @staticmethod
    def require_customer_id(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args: Union[List, Tuple], **kwargs: Dict) -> Any:
            customer_id = Customer.get_id()

            return f(customer_id, *args, **kwargs)

        return decorated_function

    @staticmethod
    def validate_json_data(schema_path: str) -> Callable:
        def decorator(f: Callable) -> Callable:
            @wraps(f)
            def wrapper(*args: Union[List, Tuple], **kwargs: Dict) -> Any:
                validator = Validator()
                try:
                    validator.validate_json_data(schema_path=schema_path, data=request.get_json())
                except (Exception,) as e:
                    debug(f"Error: {str(e)}")
                    return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST.value
                return f(*args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def validate_uniqueness(entities_name: str, key: str) -> Callable:
        def decorator(f: Callable) -> Callable:
            @wraps(f)
            def wrapper(*args: Union[List, Tuple], **kwargs: Dict) -> Any:
                validator = Validator()
                try:
                    validator.validate_uniqueness(entities_name, key, data=request.get_json())
                except (Exception,) as e:
                    debug(f"Error: {str(e)}")
                    return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST.value
                return f(*args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def validate_max_count(entities_name: str, key: str, max_count: int) -> Callable:
        def decorator(f: Callable) -> Callable:
            @wraps(f)
            def wrapper(*args: Union[List, Tuple], **kwargs: Dict) -> Any:
                validator = Validator()
                try:
                    validator.validate_max_count(entities_name, key, max_count, data=request.get_json())
                except (Exception,) as e:
                    debug(f"Error: {str(e)}")
                    return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST.value
                return f(*args, **kwargs)

            return wrapper

        return decorator
