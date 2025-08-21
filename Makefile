# Makefile for AI Security Suite

# Default shell
SHELL := /bin/bash

# ==============================================================================
# Docker Compose Commands
# ==============================================================================

.PHONY: up
up:
	@echo "Starting all services with Docker Compose..."
	docker-compose up --build -d

.PHONY: down
down:
	@echo "Stopping all services..."
	docker-compose down

.PHONY: logs
logs:
	@echo "Tailing logs for all services..."
	docker-compose logs -f

.PHONY: logs-backend
logs-backend:
	@echo "Tailing logs for backend service..."
	docker-compose logs -f backend

.PHONY: logs-frontend
logs-frontend:
	@echo "Tailing logs for frontend service..."
	docker-compose logs -f frontend

# ==============================================================================
# Database Commands
# ==============================================================================

.PHONY: migrate
migrate:
	@echo "Running database migrations..."
	docker-compose exec backend alembic upgrade head

.PHONY: migrate-down
migrate-down:
	@echo "Downgrading database by one revision..."
	docker-compose exec backend alembic downgrade -1

.PHONY: make-migration
make-migration:
	@echo "Creating new database migration..."
	docker-compose exec backend alembic revision --autogenerate -m "$(m)"

# ==============================================================================
# Development and Tooling Commands
# ==============================================================================

.PHONY: shell-backend
shell-backend:
	@echo "Opening a shell into the backend container..."
	docker-compose exec backend /bin/bash

.PHONY: format-backend
format-backend:
	@echo "Formatting backend Python code..."
	docker-compose exec backend ruff format app
	docker-compose exec backend ruff check --fix app

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
