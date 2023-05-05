import os
from uuid import UUID
from flask import make_response
from datetime import datetime
import json
from enum import Enum


def ValidateUniqueValues(data):
    """
    Verify unique fields existence and required strings length.

    :param dict data: Posted JSON data
    :return: Validation result
    """
    validity = True
    ids = []
    vehicles = data["vehicles"]
    for vehicle in vehicles:
        ids.append(vehicle["id"])
        validity &= len(str(vehicle["id"]).lstrip(".").replace("\\", "")) > 0
        features = []
        for feature in vehicle["features"]:
            features.append(feature["feature"])
            validity &= len(features) == len(set(features))
            validity &= len(feature["description"]["short"]) > 0
            validity &= len(feature["feature"]) > 0
    validity &= len(ids) == len(set(ids))
    return validity


def UserValidator(user_id):
    """
    Verify specified user ID.

    :param str user_id: Specified UID
    :return: Validation result
    """
    try:
        UUID(user_id)
        return True
    except ValueError:
        return False


def store(user_id, data):
    """
    Store posted JSON data under specified user ID directory,
    in files named after specified vehicle ID.

    Parameters
    ----------
    :param str user_id: Specified UID
    :param dict data: Posted JSON data

    raises OSError: if not able to handle directory

    :return: operation result
    """

    try:
        if not os.path.isdir(user_id):
            os.makedirs(user_id)
            Logger(LogLevel.INFO, f"Created {user_id} dir")
    except OSError:
        Logger(LogLevel.ERROR, f"Failed creating {user_id} dir")
        raise ("Error creating directory")

    try:
        for vehicle in data["vehicles"]:
            NormalizedFilename = str(vehicle["id"]).replace("/", "-").lstrip(".").replace("\\", "")
            if NormalizedFilename != vehicle["id"]:
                Logger(LogLevel.WARNING, f"Normalized data posted by {user_id}")
            file = f"{user_id}/{NormalizedFilename}.json"
            if os.path.exists(file):
                os.rename(file, f"{user_id}/{NormalizedFilename} - {datetime.now()}.json")
                Logger(LogLevel.INFO, f"Renamed {file} to {user_id}/{NormalizedFilename} - {datetime.now()}.json")
            with open(file, "w") as file:
                json.dump(vehicle, file, ensure_ascii=False)
                Logger(LogLevel.INFO, f"Successfully stored {user_id}'s data")
    except Exception as e:
        Logger(LogLevel.ERROR, str(e))
        return False
    return True


class LogLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3


def Logger(level, message):
    """
    Used to store application logs.

    Parameters
    ----------
    :param str level: Log level
    :param str message: Log message

    raises OSError: if not able to create logs directory
    """
    try:
        if not os.path.isdir("logs"):
            os.makedirs("logs")
    except OSError:
        print("Error creating logs directory")
    with open(f"logs/{datetime.now().date()}.log", "a") as f:
        f.write(f'{datetime.now().strftime("%H:%M:%S")} {level.name}: {message}\n')
