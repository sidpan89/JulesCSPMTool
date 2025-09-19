# Makefile for AI Security Suite

# Default shell
SHELL := /bin/bash

# ==============================================================================
# Docker Compose Commands
# ==============================================================================

# Prefer the modern Docker Compose V2 plugin, but fall back to the legacy
# docker-compose binary if it is the only option available. This prevents
# runtime errors (e.g. "ContainerConfig") that occur when the deprecated
# docker-compose CLI talks to newer Docker Engine releases.
DOCKER_COMPOSE := $(shell \
        if docker compose version >/dev/null 2>&1; then \
                echo "docker compose"; \
        elif command -v docker-compose >/dev/null 2>&1; then \
                echo "docker-compose"; \
        else \
                echo "docker compose"; \
        fi)

.PHONY: up
up:
	@echo "Starting all services with Docker Compose..."
	$(DOCKER_COMPOSE) up --build -d

.PHONY: down
down:
	@echo "Stopping all services..."
	$(DOCKER_COMPOSE) down

.PHONY: logs
logs:
	@echo "Tailing logs for all services..."
	$(DOCKER_COMPOSE) logs -f

.PHONY: logs-backend
logs-backend:
	@echo "Tailing logs for backend service..."
	$(DOCKER_COMPOSE) logs -f backend

.PHONY: logs-frontend
logs-frontend:
	@echo "Tailing logs for frontend service..."
	$(DOCKER_COMPOSE) logs -f frontend

# ==============================================================================
# Database Commands
# ==============================================================================

.PHONY: migrate
migrate:
	@echo "Running database migrations..."
	$(DOCKER_COMPOSE) exec backend alembic upgrade head

.PHONY: migrate-down
migrate-down:
	@echo "Downgrading database by one revision..."
	$(DOCKER_COMPOSE) exec backend alembic downgrade -1

.PHONY: make-migration
make-migration:
	@echo "Creating new database migration..."
	$(DOCKER_COMPOSE) exec backend alembic revision --autogenerate -m "$(m)"

# ==============================================================================
# Development and Tooling Commands
# ==============================================================================

.PHONY: shell-backend
shell-backend:
	@echo "Opening a shell into the backend container..."
	$(DOCKER_COMPOSE) exec backend /bin/bash

.PHONY: format-backend
format-backend:
	@echo "Formatting backend Python code..."
	$(DOCKER_COMPOSE) exec backend ruff format app
	$(DOCKER_COMPOSE) exec backend ruff check --fix app

# ==============================================================================
# Kubernetes / Helm Commands (Optional)
# ==============================================================================

.PHONY: deploy
deploy:
	@echo "Deploying to Kubernetes via Helm..."
	@helm upgrade --install ai-sec-suite ./infra/helm/ai-sec-suite --namespace ai-sec-suite --create-namespace -f ./infra/helm/ai-sec-suite/values.yaml

.PHONY: uninstall
uninstall:
	@echo "Uninstalling from Kubernetes..."
	@helm uninstall ai-sec-suite --namespace ai-sec-suite

# ==============================================================================
# Helper
# ==============================================================================

.PHONY: help
help:
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
