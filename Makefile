.PHONY: help install dev test lint clean docker-build docker-run

help:       ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:    ## Install dependencies with UV
	uv sync

dev:        ## Start development server
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

test:       ## Run test suite
	uv run pytest tests/ -v

lint:       ## Run code linting and formatting
	uv run black app/ tests/
	uv run ruff check app/ tests/ --fix

clean:      ## Clean temporary files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/

# Docker targets
docker-build: ## Build Docker image
	docker build -t llm-cv-evaluator .

docker-run: ## Run Docker container
	docker run --rm -p 8000:8000 --env-file .env llm-cv-evaluator