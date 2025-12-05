import uvicorn
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.graphs.graph_builder import GraphBuilder
from app.services.llm_factory import LLMFactory
from app.common.logger import logger

load_dotenv()

app = FastAPI(title="AI Blog Generator", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")

class BlogRequest(BaseModel):
    topic: str
    language: str | None = None
    llm: str | None = None
    model: str | None = None

@app.get("/health", tags=["system"], summary="Health check")
def health():
    logger.info("health endpoint called")
    return {"status": "ok"}

@app.post("/blogs", tags=["blogs"], summary="Generate a blog")
def create_blogs(payload: BlogRequest):
    if not payload.topic:
        raise HTTPException(status_code=400, detail="topic is required")

    logger.info(f"generate blog request: topic={payload.topic} language={payload.language} provider={payload.llm} model={payload.model}")
    llm = LLMFactory().create(provider=payload.llm, model=payload.model)

    graph_builder = GraphBuilder(llm)
    if payload.language:
        graph = graph_builder.setup_graph(usecase="language")
        state = graph.invoke({"topic": payload.topic, "current_language": (payload.language or "").lower()})
    else:
        graph = graph_builder.setup_graph(usecase="topic")
        state = graph.invoke({"topic": payload.topic})

    logger.info("blog generated successfully")
    return {"data": state}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
