from typing import Optional
from app.llms.groqllm import GroqLLM

class LLMFactory:
    def __init__(self):
        pass

    def create(self, provider: Optional[str] = None, model: Optional[str] = None):
        prov = (provider or "groq").lower()
        if prov == "groq":
            return GroqLLM().get_llm(model=model)
        raise ValueError(f"Unsupported LLM provider: {provider}")

