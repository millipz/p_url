##########################
#                        #
#   Makefile for p_url   #
#                        #
##########################

PROJECT_NAME = p_url
PYTHON_INTERPRETER = python
WD=$(shell pwd)
PYTHONPATH=${WD}
SHELL := /bin/bash

## Install dependencies using uv
install:
	uv pip install -e .

## Install dev dependencies
dev-setup:
	uv pip install -e ".[dev]"

## Run the security test (bandit + pip-audit)
security-test:
	uv run pip-audit
	uv run bandit -r . -x ./.venv,./tests,./build

## Run the black code formatter
run-black:
	uv run black ./

## Run the flake8 code check
run-flake8:
	uv run flake8 --exclude .venv

## Run the unit tests
unit-test:
	uv run pytest

## Run the coverage check
check-coverage:
	uv run pytest --cov=src tests --cov-report term-missing

## Run all checks
run-checks: security-test run-black run-flake8 check-coverage

## Clean up
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete