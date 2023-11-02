# Container's default name
NAME=dash-template
PORT=8091

# Docker image default name
IMAGE=$(NAME)

# Mount localfile system for local development
LOCAL_OPTS=--rm -v $(shell pwd):/usr/src/$(NAME) -e APP_NAME=$(NAME) -p $(PORT):8050

# SERVER_OPTS=-v $(shell pwd)/data:/usr/src/$(NAME)/data


.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo
	@echo "Targets:"
	@echo "  help          Print this help"
	@echo "  setup         Create required directories and build docker images"
	@echo "  run           Run Dash App"
	@echo "  runi          Run Dash Container with interactive shell"
	@echo "  exec          Open interactive shell on running container"
	@echo "  logs          Tail conainter logs"
	@echo "  stop          Stop Dash App"
	@echo "  test         Run tests"

setup: Dockerfile
	@echo "--> Building $(NAME)"
	docker image build -t $(IMAGE) .

.PHONY: run
run:
	@echo "--> Starting $(NAME)"
	docker run -d $(LOCAL_OPTS) --name $(NAME) -it $(IMAGE) python index.py

.PHONY: stop
stop:
	@echo "--> Stopping $(NAME)"
	docker stop $(NAME)

.PHONY: runi
runi:
	@echo "--> Starting $(NAME)"
	docker run $(LOCAL_OPTS) --name $(NAME) -it $(IMAGE) /bin/bash
	#
# Open shell on running container
.PHONY: exec
exec:
	@echo "--> Opening shell on $(NAME) container"
	docker exec -it $(NAME) bash

# Tail logs on running container
.PHONY: logs
logs:
	@echo "--> Reading container logs"
	docker logs -f $(NAME)

# Run Unit Tests
.PHONY: unit-tests
unit-tests:
	@echo "--> Running unit Tests on $(NAME)"
	docker exec $(NAME) bash -c 'pytest'

# Run all tests
.PHONY: test
test: unit-tests
