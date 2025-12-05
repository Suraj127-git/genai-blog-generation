from fastapi import APIRouter, HTTPException
from src.langgraphagenticai.services.chat_service import ChatService
from app.schemas import ChatRequest, ChatResponse
from src.langgraphagenticai.common.logger import logger

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        service = ChatService(provider=req.provider, model=req.model, embedding_model=req.embedding_model)
        result = service.run(req.usecase, req.message)
        if req.usecase == "AI News":
            raise HTTPException(status_code=400, detail="Use /news/summary for AI News")
        messages = result.get("messages")
        if hasattr(messages, "content"):
            content = messages.content
        elif isinstance(messages, list) and len(messages) > 0:
            last = messages[-1]
            content = last.content if hasattr(last, "content") else str(last)
        else:
            content = str(messages)
        from_cache = False
        if isinstance(content, str) and "[This response was retrieved from previous similar questions]" in content:
            from_cache = True
        return ChatResponse(content=content, from_cache=from_cache)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail=str(e))
