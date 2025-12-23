.PHONY: help build up down logs restart clean test shell

# Default target
help:
	@echo "MLOps Student Performance - Docker Commands"
	@echo "============================================"
	@echo "make build       - Build Docker image"
	@echo "make up          - Start containers in detached mode"
	@echo "make down        - Stop and remove containers"
	@echo "make logs        - View container logs"
	@echo "make restart     - Restart containers"
	@echo "make clean       - Remove containers, volumes, and images"
	@echo "make test        - Run tests inside container"
	@echo "make shell       - Open bash shell in container"
	@echo "make prod-up     - Start production containers"
	@echo "make prod-down   - Stop production containers"
	@echo "make rebuild     - Rebuild without cache"

# Development commands
build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

restart:
	docker-compose restart

clean:
	docker-compose down -v
	docker rmi mlops-student-performance 2>/dev/null || true
	docker system prune -f

test:
	docker-compose exec mlops-app pytest

shell:
	docker-compose exec mlops-app bash

rebuild:
	docker-compose build --no-cache
	docker-compose up -d

# Production commands
prod-up:
	docker-compose -f docker-compose.prod.yml up -d

prod-down:
	docker-compose -f docker-compose.prod.yml down

prod-logs:
	docker-compose -f docker-compose.prod.yml logs -f

# Development workflow
dev: build up logs

# Production workflow
prod: prod-up prod-logs
