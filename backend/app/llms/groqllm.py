from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

class GroqLLM:
    def __init__(self):
        load_dotenv()
        self.groq_api_key = os.getenv("GROQ_API_KEY")

    def get_llm(self, model: str | None = None):
        try:
            if not self.groq_api_key:
                raise ValueError("GROQ_API_KEY is not set")
            selected_model = model or "llama-3.1-8b-instant"
            os.environ["GROQ_API_KEY"] = self.groq_api_key
            llm = ChatGroq(api_key=self.groq_api_key, model=selected_model)
            return llm
        except Exception as e:
            raise ValueError(f"Error occurred with exception: {e}")
