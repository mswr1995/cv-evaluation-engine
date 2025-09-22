# Makefile for CV Evaluation Engine

.PHONY: help install run test lint docker-build docker-run docker-stop clean

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install dependencies with uv"
	@echo "  run          - Run the application locally"
	@echo "  test         - Run tests"
	@echo "  lint         - Run linters (black + ruff)"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run   - Run with Docker Compose"
	@echo "  docker-stop  - Stop Docker services"
	@echo "  clean        - Clean up temporary files"

# Install dependencies
install:
	uv sync

# Run locally
run:
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Run tests
test:
	uv run pytest tests/ -v

# Run linters
lint:
	uv run black app/ tests/
	uv run ruff check app/ tests/ --fix

# Docker commands
docker-build:
	docker compose build

docker-run:
	docker compose up --build

docker-stop:
	docker compose down

# Clean up
clean:
	rm -rf temp_uploads/*
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
