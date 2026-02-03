from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.config import settings
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self, model: Optional[str] = None):
        self.model = model or settings.groq_default_model
        self.llm = self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialize GroqAI LLM"""
        try:
            llm = ChatGroq(
                api_key=settings.groq_api_key,
                model=self.model,
                temperature=0.7,
                max_tokens=4096
            )
            logger.info(f"Initialized GroqAI LLM with model: {self.model}")
            return llm
        except Exception as e:
            logger.error(f"Error initializing LLM: {e}")
            raise
    
    async def generate_blog_title(self, topic: str) -> str:
        """Generate blog title from topic"""
        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are an expert blog writer. Generate a catchy, engaging blog title."),
                ("human", "Generate a compelling blog title for the topic: {topic}\n\nProvide only the title, nothing else.")
            ])
            
            chain = prompt | self.llm | StrOutputParser()
            title = await chain.ainvoke({"topic": topic})
            
            logger.info(f"Generated title for topic: {topic}")
            return title.strip()
        except Exception as e:
            logger.error(f"Error generating title: {e}")
            raise
    
    async def generate_blog_content(self, title: str, topic: str, context: Optional[str] = None) -> str:
        """Generate blog content"""
        try:
            if context:
                prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are an expert blog writer. Create comprehensive, well-structured blog content based on the given context."),
                    ("human", """Write a detailed blog post with the following:
Title: {title}
Topic: {topic}

Context from documents:
{context}

Create a well-structured blog post with:
1. An engaging introduction
2. Multiple sections with clear headings
3. Detailed explanations and examples
4. A compelling conclusion

Format the content in Markdown.""")
                ])
                
                chain = prompt | self.llm | StrOutputParser()
                content = await chain.ainvoke({
                    "title": title,
                    "topic": topic,
                    "context": context
                })
            else:
                prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are an expert blog writer. Create comprehensive, well-structured blog content."),
                    ("human", """Write a detailed blog post with the following:
Title: {title}
Topic: {topic}

Create a well-structured blog post with:
1. An engaging introduction
2. Multiple sections with clear headings
3. Detailed explanations and examples
4. A compelling conclusion

Format the content in Markdown.""")
                ])
                
                chain = prompt | self.llm | StrOutputParser()
                content = await chain.ainvoke({
                    "title": title,
                    "topic": topic
                })
            
            logger.info(f"Generated content for topic: {topic}")
            return content.strip()
        except Exception as e:
            logger.error(f"Error generating content: {e}")
            raise
    
    async def translate_content(self, content: str, target_language: str) -> str:
        """Translate blog content to target language"""
        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", f"You are an expert translator. Translate the following content to {target_language} while maintaining the formatting and structure."),
                ("human", "{content}")
            ])
            
            chain = prompt | self.llm | StrOutputParser()
            translated = await chain.ainvoke({"content": content})
            
            logger.info(f"Translated content to {target_language}")
            return translated.strip()
        except Exception as e:
            logger.error(f"Error translating content: {e}")
            raise
    
    async def analyze_document(self, document_content: str) -> Dict:
        """Analyze document and extract key information"""
        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a document analyzer. Extract key topics and summaries from documents."),
                ("human", """Analyze the following document and provide:
1. Main topics (comma-separated)
2. A brief summary (2-3 sentences)

Document:
{content}

Respond in JSON format:
{{
    "topics": "topic1, topic2, topic3",
    "summary": "Brief summary here"
}}""")
            ])
            
            chain = prompt | self.llm | StrOutputParser()
            result = await chain.ainvoke({"content": document_content[:4000]})  # Limit for context
            
            logger.info("Analyzed document")
            
            # Parse JSON response
            import json
            return json.loads(result)
        except Exception as e:
            logger.error(f"Error analyzing document: {e}")
            return {"topics": "", "summary": ""}


def get_llm_service(model: Optional[str] = None) -> LLMService:
    """Get LLM service instance"""
    return LLMService(model=model)
