# Migration Guide

## Summary

This project migrated from a Streamlit UI to a React+Redux frontend while retaining FastAPI backend and LangGraph orchestration.

## Changes

- UI: `src/ui/BlogUi.py` → `frontend/` React app
- Backend: `app.py` adds CORS, health checks, request model, logging
- LLM: `GroqLLM` no longer prints secrets; accepts dynamic model
- Graph: English language pass-through node added
- Tests: Added `tests/` for API, nodes, graph; frontend unit test
- Docker: Added `backend/Dockerfile`, `frontend/Dockerfile`, `docker-compose.yml`
- CI: Added GitHub Actions for backend, frontend, and Docker build

## Step-by-step

1. Set `GROQ_API_KEY` and optionally `LANGCHAIN_API_KEY`
2. Backend: `uv run uvicorn app:app --reload`
3. Frontend: `cd frontend && npm ci && npm run dev`
4. Use `POST /blogs` with body `{ topic, language, llm, model }`

## Compatibility

- All original business logic preserved: title, content, translation
- Streamlit UI is deprecated; use React app

## Notes

- Extend LLM providers by expanding `LLMFactory`
- Add more languages by extending graph conditional edges
