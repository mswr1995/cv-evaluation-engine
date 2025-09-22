# LLM CV Evaluation Engine

A modern, AI-powered CV evaluation system using FastAPI and Ollama (Llama 3) for intelligent, automated resume analysis.

---

## Features

- **LLM-Powered Analysis**: Uses Llama 3 via Ollama for deep, contextual CV evaluation.
- **Multi-format Support**: Upload and analyze PDF, DOCX, or TXT resumes.
- **Skill & Experience Detection**: Extracts skills, experience, education, and provides detailed feedback.
- **REST API**: Simple endpoints for file upload and evaluation.
- **Dockerized**: Easy to run locally or in production with Docker Compose.

---

## Quick Start

### Prerequisites

- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/)
- (Optional for local dev) [Python 3.11+](https://www.python.org/downloads/) and [uv](https://github.com/astral-sh/uv)

---

### 1. Clone the Repository

```bash
git clone <repository-url>
cd cv-evaluation-engine
```

---

### 2. Run with Docker Compose (Recommended)

This will start both the Ollama LLM server and the FastAPI app:

```bash
docker compose up --build
```

- FastAPI API: [http://localhost:8000](http://localhost:8000)
- API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Ollama LLM server: [http://localhost:11434](http://localhost:11434)

---

### 3. Development (without Docker)

If you want to run the app locally for development:

1. Install Python 3.11+ and [uv](https://github.com/astral-sh/uv)
2. Install dependencies:
   ```bash
   uv sync
   ```
3. Start the FastAPI server:
   ```bash
   uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
4. **You must also have Ollama running locally** (see [Ollama Quickstart](https://github.com/ollama/ollama)).

---

## API Usage

- Open [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API documentation (Swagger UI).
- You can upload a CV file (PDF, DOCX, TXT) or submit raw text for evaluation directly from the docs UI.
- The API will return a detailed, LLM-powered analysis of the CV, including scores, skills, experience, and recommendations.

---

## Project Structure

```
cv-evaluation-engine/
├── app/
│   ├── main.py              # FastAPI app entrypoint
│   ├── config.py            # App settings
│   ├── api/v1/endpoints/    # API endpoints (evaluation, health)
│   ├── core/                # LLM, text extraction, analysis
│   ├── models/              # Data models
│   └── services/            # Business logic
├── tests/                   # Unit and integration tests
├── Dockerfile               # FastAPI app container
├── docker-compose.yml       # Multi-service orchestration (Ollama + API)
└── .dockerignore            # Docker build exclusions
```

---

## Development & Testing

- **Run tests:**
  ```bash
  uv run pytest tests/ -v
  ```
- **Code formatting & linting:**
  ```bash
  uv run black app/ tests/
  uv run ruff check app/ tests/ --fix
  ```

---

## API Endpoints

- `POST /api/v1/evaluation/evaluate-file` — Upload and evaluate a CV file
- `POST /api/v1/evaluation/evaluate-text` — Evaluate raw CV text
- `GET /api/v1/evaluation/model-status` — Check LLM model status
- `GET /api/v1/evaluation/supported-formats` — Supported file types
- `GET /api/v1/health` — Health check

Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Notes

- **Ollama LLM server** runs as a separate service (see `docker-compose.yml`). The FastAPI app connects to it via HTTP.
- **Model downloads**: The first LLM request may take longer as Ollama downloads the model.
- **File size limit**: 10MB per file.

---

## License

MIT License — see LICENSE for details.