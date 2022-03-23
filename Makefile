VENV := ./.venv
BIN := $(VENV)/bin
PYTHON := $(BIN)/python

.PHONY: help
help: ## Show this help
	@grep -Eh '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: venv
venv: ## Make a new virtual environment
	python3 -m venv .venv

.PHONY: install
install: venv ## Install python project requirements
	$(VENV)/bin/pip install -r backend/requirements.txt
	$(VENV)/bin/pip install -r frontend/requirements.txt

backend/models: ## Download the model files
	./download_models.sh

.PHONY: dockerbuild
dockerbuild: ## build docker images
	docker-compose build

.PHONY: dockerup
dockerup: ## Run docker frontend and backend container
	docker-compose up -d

.PHONY: docker_restart
docker_restart: ## Rebuild docker images and run frontend and backend container
	make dockerbuild
	make dockerup

.PHONY: docker_down
docker_down: ## Remove docker containers
	docker-compose down
