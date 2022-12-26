.PHONY: default deps build stop shell run

export SERVICE_NAME := shopping-lists

# Required for the `deps` task
SHELL := $(shell which bash)

DOCKER := $(shell command -v docker)
COMPOSE := $(shell command -v docker-compose)

COMPOSE_ENV := $(COMPOSE) -f build/docker-compose.yml
COMPOSE_CMD := $(COMPOSE_ENV) run --rm $(SERVICE_NAME)

export GID := $(shell id -g)
export UID := $(shell id -u)

deps:
ifndef DOCKER
	@echo "Docker is not available. Please install docker"
	@exit 1
endif
ifndef COMPOSE
	@echo "docker-compose is not available. Please install docker-compose"
	@exit 1
endif

build: deps
	$(COMPOSE) -f build/docker-compose.yml build

stop:
	$(COMPOSE_ENV) stop
	$(COMPOSE_ENV) rm -f -v

shell: build
	$(COMPOSE_CMD) /bin/bash

run: build
	$(COMPOSE_ENV) run --rm --service-ports $(SERVICE_NAME);$(COMPOSE_ENV) stop
