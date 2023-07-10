.PHONY: format
format:
	black --line-length=140 .

.PHONY: genmodels
genmodels:
	python tools/genmodels.py --schema json/vehicle-features.v1.schema.json  --class GeneratedVehicleList --file generated_vehicle_list

.PHONY: unit-test
unit-test: genmodels
	coverage run -m pytest tests/unit/ -W error::UserWarning --capture=no

.PHONY: integration-test
integration-test: genmodels
	coverage run -m pytest tests/integration/ -W error::UserWarning --capture=no

.PHONY: coverage
coverage: unit-test integration-test
	coverage report
