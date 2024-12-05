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

all:environment install install-dev test lint audit build-backend

layer:
	rm -rf build/tmp-layer-dir/
	mkdir -p build/tmp-layer-dir
	cd backend && uv pip compile pyproject.toml -o ../build/layer-requirements.txt
	cd build/tmp-layer-dir && uv venv && uv pip install -r ../layer-requirements.txt
	rm -rf build/layer
	mkdir build/layer && mkdir build/layer/python
	cp -r build/tmp-layer-dir/.venv/lib build/layer/python
	rm -rf build/tmp-layer-dir

init-terraform:
	@echo "------- $(PURPLE) 👷‍♀️ Initialising Terraform $(RESET)------- "
	@cd terraform && terraform init -input=false

deploy-infrastructure: layer
	@echo "------- $(PURPLE) 🧱 Deploying Terraform $(RESET)------- "
	@cd terraform && terraform apply -auto-approve

destroy-infrastructure:
	@echo "------- $(PURPLE) 🏗️ Destroying Terraform $(RESET)------- "
	@cd terraform && terraform destroy -auto-approve
