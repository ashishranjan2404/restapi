# Run on mac.
DOCKER              ?=$(shell which docker)
NAMESPACE           ?=webapi
PROJECT             ?=webapi
VERSION             ?=$(shell git describe --tags --always)
CONTAINER_PREFIX    ?=$(NAMESPACE)/$(PROJECT)
WEBAPI_INSTANCE     ?=docker_webapi_1
PASS                ?=$(shell openssl rand -base64 14)
ENV_EXISTS          ?=$(shell [ -e .env ] && echo 1 || echo 0)


# Devtools params.
COMPOSE_BIN         =/usr/local/bin/docker-compose
COMPOSE_FILE        =devops/docker/docker-compose-$*.yaml
SERVICENAME         =$*

# Credentials management.
DB_PASSWORD=$(PASS)
ADMIN_PASSWORD=$(PASS)

### Compose targets

.PHONY: docker-compose-up-%
docker-compose-up-%:
	$(COMPOSE_BIN) -f $(COMPOSE_FILE) up -d

.PHONY: docker-compose-restart-%
docker-compose-restart-%:
	$(MAKE) docker-compose-down-$*
	$(MAKE) docker-compose-up-$*

.PHONY: docker-compose-down-%
docker-compose-down-%:
	$(COMPOSE_BIN) -f $(COMPOSE_FILE) down


### Deploy targets

.PHONY: local
local: docker-compose-down-local docker-compose-up-local

.PHONY: local-down
local-down: docker-compose-down-local

.PHONY: clean
clean:
	sudo git clean -fdx -e .env -e devops/docker/var/auto -e .tox -e .venv