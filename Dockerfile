# ---- Build image ----
FROM python:3.11-slim as base

# System deps
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy project files
COPY . .

# Install uv (fast Python package manager)
RUN pip install --no-cache-dir uv

# Install dependencies
RUN uv pip install --system --no-cache-dir .

# Expose port
EXPOSE 8000

# Entrypoint
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# ---- Ollama is NOT included in this image ----
# Ollama is provided as a separate service via docker-compose.yml
# Do NOT run Ollama in this container. Use `docker compose up` to start both services.
