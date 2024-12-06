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
	cd $(FRONTEND_DIR) && uv venv

frontend-install:
	@echo "Installing dependencies..."
	cd $(FRONTEND_DIR) && uv pip install -e .

frontend-install-dev:
	@echo "Installing dev dependencies..."
	cd $(FRONTEND_DIR) && uv pip install -e ".[dev]"

frontend-test:
	# TODO - Frontend tests

frontend-lint:
	@echo "Linting code..."
	cd $(FRONTEND_DIR) && uv run black .
	cd $(FRONTEND_DIR) && uv run flake8

frontend-audit:
	@echo "Running security audit..."
	cd $(FRONTEND_DIR) && uv run pip-audit

frontend-all: frontend-environment frontend-install frontend-install-dev frontend-test frontend-lint frontend-audit

frontend-run:
	@echo "Spinning up Streamlit frontend..."
	cd $(FRONTEND_DIR) && \
	uv run streamlit run app/main.py \
	--server.enableCORS=false \
	--server.enableXsrfProtection=false


# Backend
backend-environment:
	@echo "Installing dependencies..."
	cd $(BACKEND_DIR) && uv venv
	cd $(FRONTEND_DIR) && uv venv

backend-install:
	@echo "Installing dependencies..."
	cd $(BACKEND_DIR) && uv pip install -e .
	cd $(FRONTEND_DIR) && uv pip install -e .

backend-install-dev:
	@echo "Installing dev dependencies..."
	cd $(BACKEND_DIR) && uv pip install -e ".[dev]"
	cd $(FRONTEND_DIR) && uv pip install -e ".[dev]"

backend-test:
	@echo "Running tests..."
	cd $(BACKEND_DIR) && uv run pytest
	# Pending frontend tests

backend-lint:
	@echo "Linting code..."
	cd $(BACKEND_DIR) && uv run black .
	cd $(BACKEND_DIR) && uv run flake8
	cd $(FRONTEND_DIR) && uv run black .
	cd $(FRONTEND_DIR) && uv run flake8

backend-audit:
	@echo "Running security audit..."
	cd $(BACKEND_DIR) && uv run pip-audit
	cd $(FRONTEND_DIR) && uv run pip-audit

backend-all: backend-environment backend-install backend-install-dev backend-test lbackend-int backend-audit

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

deploy-infrastructure: init-terraform layer
	@echo "------- $(PURPLE) 🧱 Deploying Terraform $(RESET)------- "
	@cd terraform && terraform apply -auto-approve

destroy-infrastructure:
	@echo "------- $(PURPLE) 🏗️ Destroying Terraform $(RESET)------- "
	@cd terraform && terraform destroy -auto-approve