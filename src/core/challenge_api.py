import json
import os
from flask import Blueprint, make_response, Flask
from flask import request
from json import *
from jsonschema import Draft7Validator

try:
    from utils.api_decorators import ApiDecorators
except:
    from src.utils.api_decorators import ApiDecorators

api = Blueprint("challenge_api", __name__)


def create_app(config="dev"):
    app = Flask(__name__)
    app.register_blueprint(api)
    return app


class Vehicle:
    def __init__(self, vehicle_id, vehicle_features, user_id):
        self.id = vehicle_id
        self.features = vehicle_features
        self.user_id = user_id
        self.folder_path = f"database/{self.user_id}"
        self.file_path = f"{self.folder_path}/{self.id}.json"

    def __str__(self):
        return self.id

    def save(self):
        json_data = dict(id=self.id, features=self.features)
        if not os.path.isdir(self.folder_path):
            os.mkdir(self.folder_path)
        if not os.path.isfile(self.file_path):
            out_file = open(f"{self.file_path}", "w")
            json.dump(json_data, out_file)
            out_file.close()

    def get(self):
        try:
            file_json = open(f"{self.file_path}", "r")
            data_json = json.load(file_json)
            file_json.close()
            return data_json
        except FileNotFoundError:
            print("Error: The file does not exist")

    def delete(self):
        print(f"Deleting vehicle {self.id} of user: {self.user_id}, are you sure ? YES/no")
        if input() == "YES":
            try:
                os.remove(self.file_path)
                print("Vehicle deleted successfully")
            except FileNotFoundError:
                print("Error: The file does not exist")
        else:
            print("Aborted")


@api.route("/challenge", methods=["POST"])
@ApiDecorators.require_customer_id
def vehicle_features_post(user_id):
    vehicles = clean_input_data()  # format input data
    if is_valid(vehicles):  # validate JSON schema
        try:
            saving_vehicles(vehicles, user_id)  # save vehicle to JSON
            return make_response("200", 200)
        except FileExistsError:
            return make_response("400", 400)
        except:
            return make_response("500", 500)
    else:
        return make_response("400", 400)


def clean_input_data():
    input_data = dict()
    try:
        input_data = request.get_json()
    except:
        input_data = request.get_data(as_text=True)
        input_data = input_data[input_data.find("{") : input_data.rfind("}") + 1]
        input_data = json.loads(input_data)
    finally:
        input_data["vehicles"] = input_data.pop("vehicle")
        return input_data


def is_valid(input_data):
    with open("json/vehicle-features.v1.schema.json") as sc:
        schema = load(sc)
    validator = Draft7Validator(schema)
    if validator.is_valid(input_data):
        return True


def saving_vehicles(vehicles, user_id):
    list1 = list()
    for vehicle in vehicles["vehicles"]:
        if vehicle["id"] in list1:
            raise FileExistsError
        else:
            list1.append(vehicle["id"])
    for vehicle in vehicles["vehicles"]:
        Vehicle(vehicle["id"], vehicle["features"], user_id).save()
