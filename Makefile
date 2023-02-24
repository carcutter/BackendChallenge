.PHONY: format
format:
	black --line-length=140 .

.PHONY: unit-test
unit-test:
	coverage run -m pytest tests/unit/

.PHONY: coverage
coverage: unit-test
	coverage report
