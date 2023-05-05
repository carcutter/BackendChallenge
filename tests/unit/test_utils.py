from src.utils.utils import ValidateUniqueValues, UserValidator, store, Logger, LogLevel

import json
from uuid import uuid4
import os
from datetime import datetime


def test_validating_required_data():
    data = json.loads('{"vehicles": [{"id": "VIN1","features": [{"feature": "","description": {"short": "5.2 Liter V8"}}]}]}')
    assert ValidateUniqueValues(data) == False
    data = json.loads('{"vehicles": [{"id": "VIN1","features": [{"feature": "ENGINE","description": {"short": ""}}]}]}')
    assert ValidateUniqueValues(data) == False
    data = json.loads(
        '{"vehicles": [{"id": "VIN1","features": [{ "feature": "ENGINE", "description": { "short": "5.2 Liter V8" } },{ "feature": "ENGINE", "description": { "short": "19 Felgen" } }]}]}'
    )
    assert ValidateUniqueValues(data) == False


def test_validating_id():
    data = json.loads('{"vehicles": [{"id": "VIN1","features": [{"feature": "ENGINE","description": {"short": "5.2 Liter V8"}}]}]}')
    assert ValidateUniqueValues(data) == True
    data = json.loads('{"vehicles": [{"id": ".","features": [{"feature": "ENGINE","description": {"short": "5.2 Liter V8"}}]}]}')
    assert ValidateUniqueValues(data) == False
    data = json.loads('{"vehicles": [{"id": "..","features": [{"feature": "ENGINE","description": {"short": "5.2 Liter V8"}}]}]}')
    assert ValidateUniqueValues(data) == False
    data = json.loads('{"vehicles": [{"id": "/","features": [{"feature": "ENGINE","description": {"short": "5.2 Liter V8"}}]}]}')
    assert ValidateUniqueValues(data) == True
    data = json.loads('{"vehicles": [{"id": "","features": [{"feature": "ENGINE","description": {"short": "5.2 Liter V8"}}]}]}')
    assert ValidateUniqueValues(data) == False
    data = json.loads('{"vehicles": [{"id": "","features": [{"feature": "ENGINE","description": {"short": "5.2 Liter V8"}}]}]}')
    assert ValidateUniqueValues(data) == False


def test_validate_userid():
    userid = str(uuid4())
    assert UserValidator(userid) == True
    userid = "123456"
    assert UserValidator(userid) == False
    userid = ""
    assert UserValidator(userid) == False


def test_file_storage():
    userid = str(uuid4())
    vehicleId = "VIN1"
    validData = json.loads('{"vehicles": [{"id": "VIN1","features": [{"feature": "ENGINE","description": {"short": "5.2 Liter V8"}}]}]}')
    assert store(userid, validData) == True
    assert os.path.exists(userid) == True
    assert os.path.exists(f"{userid}/{vehicleId}.json") == True
    try:
        os.remove(f"{userid}/{vehicleId}.json")
        os.rmdir(userid)
    except:
        pass


def test_logger():
    message = "Testing logger"
    level = LogLevel.DEBUG
    Logger(level, message)
    assert os.path.exists("logs") == True
    assert os.path.exists(f"logs/{datetime.now().date()}.log") == True
    with open(f"logs/{datetime.now().date()}.log", "r") as f:
        assert f'{datetime.now().strftime("%H:%M:%S")} {level.name}: {message}\n' in f.read()
