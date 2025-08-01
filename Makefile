# Library Management System - Docker Commands

.PHONY: help build up down restart logs clean dev prod import-books test

# Default target
help:
	@echo "Library Management System - Available Commands:"
	@echo ""
	@echo "  build        Build Docker images"
	@echo "  up           Start all services"
	@echo "  down         Stop all services"
	@echo "  restart      Restart all services"
	@echo "  logs         Show logs from all services"
	@echo "  clean        Remove all containers, networks, and volumes"
	@echo ""
	@echo "  dev          Start in development mode (with pgAdmin)"
	@echo "  prod         Start in production mode"
	@echo ""
	@echo "  import-books Import sample book data"
	@echo "  db-shell     Connect to PostgreSQL shell"
	@echo "  app-shell    Connect to FastAPI container shell"
	@echo ""
	@echo "  test         Run tests (when implemented)"
	@echo "  check        Check if services are healthy"

# Build Docker images
build:
	docker-compose build --no-cache

# Start services
up:
	docker-compose up -d
	@echo "Services started. API docs available at: http://localhost:8000/docs"

# Stop services
down:
	docker-compose down

# Restart services
restart: down up

# Show logs
logs:
	docker-compose logs -f

# Clean everything
clean:
	docker-compose down -v --rmi all --remove-orphans
	docker system prune -f

# Development mode (includes pgAdmin)
dev:
	docker-compose -f docker-compose.yaml -f docker-compose.dev.yaml up -d
	@echo "Development mode started."
	@echo "API docs: http://localhost:8000/docs"
	@echo "pgAdmin: http://localhost:5050 (admin@library.com / admin123)"

# Production mode
prod:
	docker-compose up -d --scale pgadmin=0
	@echo "Production mode started. API docs: http://localhost:8000/docs"

# Import sample books
import-books:
	docker-compose exec web python import_books.py --clear

# Database shell
db-shell:
	docker-compose exec db psql -U admin -d practice_fastapi

# Application shell
app-shell:
	docker-compose exec web bash

# Check service health
check:
	@echo "Checking service health..."
	@docker-compose ps
	@echo ""
	@echo "API Health:"
	@curl -s http://localhost:8000/health | python -m json.tool || echo "API not responding"

# Run tests (placeholder for future implementation)
test:
	docker-compose exec web python -m pytest tests/ -v
