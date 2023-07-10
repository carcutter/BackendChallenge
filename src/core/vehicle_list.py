from utils.generated_vehicle_list import GeneratedVehicleList


class VehicleList(GeneratedVehicleList):
    class VehiclesProperty (GeneratedVehicleList.VehiclesProperty):
        class Item(GeneratedVehicleList.VehiclesProperty.Item):
            class IdProperty(GeneratedVehicleList.VehiclesProperty.Item.IdProperty):
                @staticmethod
                def _Validate(value):
                    super(VehicleList.VehiclesProperty.Item.IdProperty, VehicleList.VehiclesProperty.Item.IdProperty)._Validate(value)
                    if len(value) != 17:
                        raise ValueError(f"invalid VIN: {value}")
                    # TODO: more validation here with checksums etc
