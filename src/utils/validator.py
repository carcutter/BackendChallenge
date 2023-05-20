import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import os
from typing import Dict

from utils.singleton import Singleton


class Validator(object, metaclass=Singleton):
    @staticmethod
    def validate_json_data(schema_path: str = None, data: Dict = None) -> None:
        if schema_path is not None and os.path.exists(schema_path) is True:
            with open(schema_path, "r") as json_file:
                schema = json.load(json_file)
            if data is not None:
                try:
                    validate(data, schema)
                except ValidationError:
                    raise ValueError("Not valid JSON data")
            else:
                raise ValueError("Empty data")
        else:
            raise ValueError("Wrong JSON schema")

    @staticmethod
    def validate_uniqueness(entities_name: str, key: str, data: Dict = None) -> None:
        if data is not None:
            entities = []
            for item in data.get(entities_name, []):
                if isinstance(item, dict) is True and key in item:
                    entities.append(item.get(key))
            if len(entities) != len(set(entities)):
                raise ValueError(f"{entities_name.capitalize()} ({entities}) are not unique by '{key}'")
        else:
            raise ValueError("Empty data")

    @staticmethod
    def validate_max_count(entities_name: str, key: str, max_count: int = 0, data: Dict = None) -> None:
        if data is not None:
            entities = []
            for item in data.get(entities_name, []):
                if isinstance(item, dict) is True and key in item:
                    entities.append(item.get(key))
            if max_count < len(entities):
                raise ValueError(f"Max {entities_name} count is {max_count}, but {len(entities)} found")
        else:
            raise ValueError("Empty data")
