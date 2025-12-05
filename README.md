# AI Blog Generator (FastAPI + React + LangGraph)

Modern, performant blog generation platform using FastAPI, React+Redux, Tailwind CSS, and Groq LLMs orchestrated with LangGraph and instrumented with LangSmith.

## Features

- React frontend with Redux and Tailwind CSS
- FastAPI backend with automatic OpenAPI docs
- LangGraph orchestration for title, content, and optional translation
- Groq LLM integration via LangChain
- Dockerized dev environment with health checks and CORS
- CI pipelines for backend and frontend

## Project Structure

```
backend/               # FastAPI backend, tests, Dockerfile
  app/                 # All backend application logic (API, graphs, nodes, services)
    main.py            # FastAPI entrypoint
    common/            # Logging
    graphs/            # LangGraph builders
    nodes/             # Content nodes
    services/          # LLM factory and services
    states/            # Typed state models
  tests/               # Backend tests
frontend/              # React + Redux + Tailwind frontend app
docker-compose.yml     # Local dev orchestration
```

## Prerequisites

- Python 3.13 (managed via `uv`)
- Node.js 20 (for frontend)
- Docker (optional for compose)

## Setup (uv)

```bash
uv sync --frozen --no-dev
cd backend
uv run uvicorn app.main:app --reload
```

## Frontend Dev

```bash
cd frontend
npm ci
npm run dev
# open http://localhost:3000
```

## Docker Compose

```bash
docker compose up --build
# frontend: http://localhost:3000, backend: http://localhost:8000
```

Set environment variables (backend):

- `GROQ_API_KEY`
- `LANGCHAIN_API_KEY`

## API

- `GET /health` → health probe
- `POST /blogs` → generate a blog
  - body: `{ topic: string, language?: string, llm?: string, model?: string }`

Interactive docs: `http://localhost:8000/docs`

## Tests

Backend:

```bash
uv run pytest -q
```

Frontend:

```bash
cd frontend && npm run test -- --run
```

## Migration

See `MIGRATION.md` for detailed steps from Streamlit UI to React app and backend changes.

## Architecture

See `ARCHITECTURE.md` for component design, patterns, and data flow.
