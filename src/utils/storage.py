import json
import os
from typing import Dict
from werkzeug.utils import secure_filename

from utils.singleton import Singleton


class Storage(object, metaclass=Singleton):
    def __init__(self, storage_folder: str = "./") -> None:
        self.storage_folder = secure_filename(f"{storage_folder}").rstrip("/")

        if os.path.exists(self.storage_folder) is False:
            os.makedirs(self.storage_folder)

    def save_entity(self, user_id: str = None, key: str = None, json_data: Dict = None) -> bool:
        if user_id is None:
            return False

        entity_id = json_data.get(key, None)
        if entity_id is None:
            return False

        if json_data is None:
            json_data = {}

        user_id = secure_filename(user_id)
        user_path = f"{self.storage_folder}/{user_id}".rstrip("/")
        if os.path.exists(user_path) is False:
            os.makedirs(user_path)

        entity_id = secure_filename(entity_id)
        entity_path = f"{user_path}/{entity_id}.json"

        saved = False
        try:
            with open(entity_path, "w") as outfile:
                json.dump(json_data, outfile)
        except TypeError:  # if the JSON data can't be serialized in some way
            saved = False
        except (OSError, FileExistsError, FileNotFoundError):  # if some error on the OS / File-system level
            saved = False
        else:
            saved = True
        finally:
            return saved
