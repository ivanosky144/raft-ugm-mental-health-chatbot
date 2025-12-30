from config.config import Settings
from chatbot_engine.llm_client import GPTClient
from chatbot_engine.retriever import Retriever

settings = Settings.load()

class ChatbotEngine:
    def __init__(self):
        self.gpt_client = GPTClient(
            api_key=settings.OPENAI_API_KEY,
            model=settings.FINE_TUNED_MODEL
        )
        self.retriever = Retriever()
        return
    
    def generate_response(self, user_query):
        return