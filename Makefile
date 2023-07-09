.PHONY: format
format:
	black --line-length=140 .

.PHONY: genmodels
genmodels:
	python tools/genmodels.py --schema json/vehicle-features.v1.schema.json  --class VehicleList --file vehicle_list

.PHONY: unit-test
unit-test: genmodels
	coverage run -m pytest tests/unit/ -W error::UserWarning --capture=no

.PHONY: coverage
coverage: unit-test
	coverage report
