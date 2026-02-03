from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Optional, List
from app.services.llm_service import LLMService
from app.database.chromadb import get_chroma_client
import logging

logger = logging.getLogger(__name__)


class BlogState(TypedDict):
    """State for blog generation graph"""
    topic: str
    title: Optional[str]
    content: Optional[str]
    language: str
    document_ids: List[str]
    context: Optional[str]
    error: Optional[str]


class GraphService:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
        self.chroma_client = get_chroma_client()
    
    async def retrieve_context(self, state: BlogState) -> BlogState:
        """Retrieve context from documents if document_ids provided"""
        if not state.get("document_ids") or len(state["document_ids"]) == 0:
            state["context"] = None
            return state
        
        try:
            # Query ChromaDB for relevant content
            results = self.chroma_client.query_documents(
                query_texts=[state["topic"]],
                n_results=5,
                where={"doc_id": {"$in": state["document_ids"]}}
            )
            
            # Combine document content as context
            if results and "documents" in results and len(results["documents"]) > 0:
                context = "\n\n".join(results["documents"][0])
                state["context"] = context
                logger.info(f"Retrieved context from {len(results['documents'][0])} document chunks")
            else:
                state["context"] = None
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            state["context"] = None
        
        return state
    
    async def generate_title(self, state: BlogState) -> BlogState:
        """Generate blog title"""
        try:
            title = await self.llm_service.generate_blog_title(state["topic"])
            state["title"] = title
            logger.info(f"Generated title: {title}")
        except Exception as e:
            logger.error(f"Error in title generation: {e}")
            state["error"] = str(e)
        
        return state
    
    async def generate_content(self, state: BlogState) -> BlogState:
        """Generate blog content"""
        try:
            content = await self.llm_service.generate_blog_content(
                title=state["title"],
                topic=state["topic"],
                context=state.get("context")
            )
            state["content"] = content
            logger.info("Generated blog content")
        except Exception as e:
            logger.error(f"Error in content generation: {e}")
            state["error"] = str(e)
        
        return state
    
    async def translate_if_needed(self, state: BlogState) -> BlogState:
        """Translate content if language is not English"""
        if state["language"].lower() == "english":
            return state
        
        try:
            translated_title = await self.llm_service.translate_content(
                state["title"],
                state["language"]
            )
            translated_content = await self.llm_service.translate_content(
                state["content"],
                state["language"]
            )
            
            state["title"] = translated_title
            state["content"] = translated_content
            logger.info(f"Translated to {state['language']}")
        except Exception as e:
            logger.error(f"Error in translation: {e}")
            state["error"] = str(e)
        
        return state
    
    def build_blog_generation_graph(self) -> StateGraph:
        """Build LangGraph workflow for blog generation"""
        graph = StateGraph(BlogState)
        
        # Add nodes
        graph.add_node("retrieve_context", self.retrieve_context)
        graph.add_node("generate_title", self.generate_title)
        graph.add_node("generate_content", self.generate_content)
        graph.add_node("translate", self.translate_if_needed)
        
        # Add edges
        graph.add_edge(START, "retrieve_context")
        graph.add_edge("retrieve_context", "generate_title")
        graph.add_edge("generate_title", "generate_content")
        graph.add_edge("generate_content", "translate")
        graph.add_edge("translate", END)
        
        return graph.compile()
    
    async def generate_blog(
        self,
        topic: str,
        language: str = "english",
        document_ids: List[str] = None
    ) -> BlogState:
        """Generate blog using LangGraph workflow"""
        graph = self.build_blog_generation_graph()
        
        initial_state: BlogState = {
            "topic": topic,
            "title": None,
            "content": None,
            "language": language,
            "document_ids": document_ids or [],
            "context": None,
            "error": None
        }
        
        result = await graph.ainvoke(initial_state)
        return result


def get_graph_service(llm_service: LLMService) -> GraphService:
    """Get graph service instance"""
    return GraphService(llm_service)
