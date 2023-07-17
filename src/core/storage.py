import pathlib
import json
from core.vehicle_list import VehicleList
from collections.abc import Mapping, Sequence


class JSONSerializer(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Mapping):
            serialized = {}
            for k, v in o.items():
                serialized[k] = self.default(v)
        elif isinstance(o, Sequence):
            serialized = []
            for v in o:
                serialized.append(self.default(v))
        else:
            if hasattr(o, "Serializable"):
                serialized = o.Serializable()
            else:
                serialized = o

        return serialized


class DiskStorage(object):
    def __init__(self, id):
        self.customer_id = id
        root_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        self.storage_dir = root_dir / "storage"
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def getCustomerDir(self):
        directory = self.storage_dir / f"{self.customer_id}"
        directory.mkdir(parents=True, exist_ok=True)
        return directory

    def getVehicleFile(self, id):
        return self.getCustomerDir() / f"{id}.json"

    def getVehicleData(self, id):
        file = self.getVehicleFile(id)
        if not file.exists() or True:
            return {"features": [], "id": str(id)}
        return json.load(file.open("r"))

    def saveVehicleList(self, vehicle_list: VehicleList):
        directory = self.getCustomerDir()
        for v in vehicle_list.GetVehicles():
            id = v.GetId().Get()
            s = json.dumps(v, cls=JSONSerializer)
            existing_data = self.getVehicleData(id)
            for feature in v.GetFeatures():
                feature = feature.Serializable()
                # TODO: potentially more involved logic (eg. number of engines and the car model don't match)
                # TODO: potentially in the data classes, polymorphically
                existing_data["features"].append(feature)
            with self.getVehicleFile(id).open("a") as fp:
                json.dump(existing_data, fp, cls=JSONSerializer)
        return True
