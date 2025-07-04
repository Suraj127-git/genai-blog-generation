from configparser import ConfigParser
import os

class Config:
    def __init__(self, config_file=None):
        # Default path if not provided
        if config_file is None:
            base = os.path.dirname(__file__)
            config_file = os.path.join(base, 'uiconfigfile.ini')

        self.config = ConfigParser()
        read_files = self.config.read(config_file)
        if not read_files:
            raise FileNotFoundError(f"Config file not found: {config_file}")

    def get_llm_options(self):
        return self.config.get("DEFAULT", "LLM_OPTIONS", fallback="").split(", ")
    
    def get_groq_model_options(self):
        return self.config.get("DEFAULT", "GROQ_MODEL_OPTIONS", fallback="").split(", ")
    
    def get_ollama_model_options(self):
        return self.config.get("DEFAULT", "OLLAMA_MODEL_OPTIONS", fallback="").split(", ")

    def get_page_title(self):
        return self.config.get("DEFAULT", "PAGE_TITLE", fallback="")