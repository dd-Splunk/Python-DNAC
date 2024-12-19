.SILENT:
.PHONY: up logs down clean env
# Check Docker version and set the compose command accordingly
# Suppress Warnings ( like environent variables not set )
ifneq (, $(shell docker compose version 2>/dev/null))
    DC=docker --log-level error compose
else
    DC=docker-compose --log-level ERROR
endif
SHELL := /bin/bash

ENV := development
# Define the command to retrieve secrets from 1Password
GET_SECRETS = op run --env-file="./config/tpl.env" -- 

env: .env
	op inject -f -i config/tpl.env -o .env

up:
	@$(GET_SECRETS) \
	$(DC) up -d
logs:
	$(DC) logs -f
down:
	$(DC) down

clean:
	$(DC) down -v
	rm -rf .env
