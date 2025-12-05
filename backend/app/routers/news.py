from fastapi import APIRouter, HTTPException
from app.schemas import NewsRequest, NewsResponse
from src.langgraphagenticai.services.news_service import NewsService
from src.langgraphagenticai.common.logger import logger

router = APIRouter(prefix="/news", tags=["news"])

@router.post("/summary", response_model=NewsResponse)
def news_summary(req: NewsRequest):
    try:
        service = NewsService(embedding_model=req.embedding_model)
        result = service.run(req.timeframe)
        summary = result.get("summary", "")
        saved_file = result.get("filename") or result.get("saved_file")
        from_cache = result.get("from_cache", False)
        return NewsResponse(summary=summary, saved_file=saved_file, from_cache=from_cache)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail=str(e))
