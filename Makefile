SHELL:=/usr/bin/env bash

.PHONY: lint
lint:
	poetry run doc8 -q docs
	poetry run black crome_synthesis tests/**/*.py
	poetry run pyupgrade
	poetry run pycln crome_synthesis tests/**/*.py --all
	poetry run autoflake .
	poetry run isort .
	poetry run autopep8 --in-place -r crome_synthesis tests/**/*.py
	poetry run docformatter --in-place -r crome_synthesis tests/**/*.py
	poetry run yapf -ir .
# 	poetry run mypy crome_synthesis tests/**/*.py
# 	poetry run bandit -r crome_synthesis
	poetry run flake8 crome_synthesis

.PHONY: unit
unit:
	poetry run pytest

.PHONY: package
package:
	poetry check
	poetry run pip check
	poetry run safety check --full-report

.PHONY: test
test: lint package unit
