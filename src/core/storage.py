import pathlib
from core.vehicle_list import VehicleList


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

    def saveVehicleList(self, vehicle_list: VehicleList):
        directory = self.getCustomerDir()
        return True
