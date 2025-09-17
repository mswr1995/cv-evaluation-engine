.PHONY: help install dev test lint type-check clean

help:		## Show this help message
    @grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:	## Install dependencies with UV
    uv sync --all-extras

dev:		## Start development server
    uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

test:		## Run test suite
    uv run pytest tests/ -v

lint:		## Run code linting and formatting
    uv run black app/ tests/
    uv run ruff check app/ tests/ --fix

type-check:	## Run type checking
    uv run mypy app/

clean:		## Clean temporary files
    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete
    rm -rf .pytest_cache/
    rm -rf .mypy_cache/

.env:		## Copy environment template
    cp .env.example .env