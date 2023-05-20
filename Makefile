.PHONY: format
format:
	black --line-length=140 .

.PHONY: unit-test
unit-test:
	coverage run -m pytest tests/unit/

.PHONY: coverage
coverage: unit-test
	coverage report

.PHONY: py-version
py-version:
	python --version

.PHONY: api-run
api-run:
	python src/cli.py api-server vehicle-features
