# Architecture Overview

## Components

- Backend: FastAPI (`app.py`) orchestrating LangGraph graphs
- LLM: Groq via LangChain (`src/llms/groqllm.py`) behind `LLMFactory`
- Graph: `GraphBuilder` composes nodes and conditional edges
- Nodes: `BlogNode` with title, content, translation, routing
- Frontend: React+Redux+Tailwind in `frontend/`

## Patterns

- Factory: `LLMFactory` selects provider/model
- Strategy (routing): graph conditional edges based on `current_language`
- Observer: CI pipelines and health checks monitor build/runtime

## Data Flow

1. Frontend dispatches `generateBlog` with topic/language/model
2. Backend validates input, creates LLM via factory
3. Graph executes: title → content → (route) → translation (or pass-through)
4. Response returns `{ data: { blog: { title, content } } }`

## Error Handling & Logging

- Input validation via Pydantic models
- Structured logging via `src/common/logger.py`, optional Logtail
- HTTP 400 for missing topic

## Security

- Secrets via environment (`GROQ_API_KEY`)
- CORS enabled for frontend dev

## Performance

- Sequential node execution; can scale with FastAPI workers
- Optional caching and streaming can be added later
