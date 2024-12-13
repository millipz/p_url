##########################
#                        #
#   Makefile for p_url   #
#                        #
##########################
include common/variables.mk

BACKEND_DIR := backend
FRONTEND_DIR := frontend

# Frontend
frontend-environment:
	@echo "Installing dependencies..."
	cd $(FRONTEND_DIR) && bun install

frontend-install: frontend-environment

frontend-install-dev: frontend-environment

frontend-test:
	cd $(FRONTEND_DIR) && bun test

frontend-lint:
	@echo "Linting and fixing code..."
	cd $(FRONTEND_DIR) && bun run format
	cd $(FRONTEND_DIR) && bun run lint --fix

frontend-audit:
	@echo "Running security audit..."
	cd $(FRONTEND_DIR) && bunx snyk test

frontend-all: frontend-install frontend-test frontend-lint frontend-audit

frontend-run:
	@echo "Starting Svelte frontend..."
	cd $(FRONTEND_DIR) && bun run dev


# Backend
backend-environment:
	@echo "Installing dependencies..."
	cd $(BACKEND_DIR) && uv venv

backend-install:
	@echo "Installing dependencies..."
	cd $(BACKEND_DIR) && uv pip install -e .

backend-install-dev:
	@echo "Installing dev dependencies..."
	cd $(BACKEND_DIR) && uv pip install -e ".[dev]"

backend-test:
	@echo "Running tests..."
	cd $(BACKEND_DIR) && uv run pytest

backend-lint:
	@echo "Linting code..."
	cd $(BACKEND_DIR) && uv run black .
	cd $(BACKEND_DIR) && uv run flake8

backend-audit:
	@echo "Running security audit..."
	cd $(BACKEND_DIR) && uv run pip-audit

backend-all: backend-environment backend-install backend-install-dev backend-test backend-lint backend-audit

# Backend Deployment
backend-layer:
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

deploy-infrastructure: init-terraform backend-layer
	@echo "------- $(PURPLE) 🧱 Deploying Terraform $(RESET)------- "
	@cd terraform && terraform apply -auto-approve

destroy-infrastructure:
	@echo "------- $(PURPLE) 🏗️ Destroying Terraform $(RESET)------- "
	@cd terraform && terraform destroy -auto-approve