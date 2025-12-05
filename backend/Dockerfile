FROM ghcr.io/astral-sh/uv:python3.13-bookworm

WORKDIR /app

COPY backend/pyproject.toml ./pyproject.toml
RUN uv sync --no-dev

COPY backend/. ./

ENV PYTHONPATH=/app
EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
