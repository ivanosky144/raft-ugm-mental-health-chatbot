from config.config import Settings
from chatbot_engine.llm_client import GPTClient
from chatbot_engine.retriever import Retriever

import os
import json

settings = Settings.load()

class ChatbotEngine:
    def __init__(self):
        self.fine_tuned_model_client = GPTClient(
            api_key=settings.OPENAI_API_KEY,
            model=settings.FINE_TUNED_MODEL
        )
        self.retriever = Retriever()
        return
    
    def generate_response(self, user_query):
        user_answer = user_query.get("user_answer", "")
        group_id = user_query.get("group_id", "")
        section = user_query.get("section", "")

        conversation_type = "Opening" if section == "" else "Survey"
        BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "..")
        grouped_mental_health_screening = os.path.join(BASE_DIR, "external_data", "grouped_mental_health_screening.json")

        with open(grouped_mental_health_screening, "r") as f:
            grouped_questions = json.load(f)

        next_questions = []
        scoring_system = []

        for item in grouped_questions:
            if item["section"] == section:
                scoring_system = item.get("scoring_system", [])
                for group in item["grouped_questions"]:
                    if group["group_id"] == group_id:
                        next_questions = group.get("questions", [])

        content_payload = {
            "type": conversation_type,
            "section": section,
            "user_answer": user_answer,
            "next_questions": next_questions,
            "scoring_system": scoring_system
        }

        user_message = {
            "role": "user",
            "content": json.dumps(content_payload)
        }

        response = self.fine_tuned_model_client.run_prompt(
            "",
            json.dumps(user_message),
        )

        return response