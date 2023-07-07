from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema
import json
import os

schema_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), "../../json/vehicle-features.v1.schema.json"
    )
)

with open(schema_path) as schema_file:
    schema = json.load(schema_file)


class MyInputs(Inputs):
    json = [JsonSchema(schema=schema)]


def validate_json(request):
    inputs = MyInputs(request)
    if inputs.validate():
        return None
    else:
        return inputs.errors
