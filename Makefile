##########################
#                        #
#   Makefile for p_url   #
#                        #
##########################
include common/variables.mk

BACKEND_DIR := backend
FRONTEND_DIR := frontend

.PHONY: install test lint audit build-backend build-frontend

environment:
	@echo "Installing dependencies..."
	cd $(BACKEND_DIR) && uv venv


install:
	@echo "Installing dependencies..."
	cd $(BACKEND_DIR) && uv pip install -e .

install-dev:
	@echo "Installing dev dependencies..."
	cd $(BACKEND_DIR) && uv pip install -e ".[dev]"

test:
	@echo "Running tests..."
	cd $(BACKEND_DIR) && uv run pytest

lint:
	@echo "Linting code..."
	cd $(BACKEND_DIR) && uv run black .
	cd $(BACKEND_DIR) && uv run flake8

audit:
	@echo "Running security audit..."
	cd $(BACKEND_DIR) && uv run pip-audit

build-backend:
	docker build -t myproject/backend -f $(BACKEND_DIR)/Dockerfile .

all:environment install install-dev test lint audit build-backend

run-backend:
	docker run -p 8000:8000 myproject/backend