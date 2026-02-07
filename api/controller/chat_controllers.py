import json
import os
from flask import Blueprint, request, jsonify
from datetime import datetime
from api.service.chat_service import ChatService
from chatbot_engine.engine import ChatbotEngine

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")

class ChatController:
    def __init__(self):
        self.chatbot_engine = ChatbotEngine()

    @staticmethod
    @chat_bp.get("/aspect-progress")
    def get_aspect_progress(self):
        chat_id = request.args.get("chat_id")
        BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "..")
        grouped_questions_dir = os.path.join(BASE_DIR, "external_data", "grouped_mental_health_screening.json")

        latest_chat = ChatService.get_latest_chat_item(chat_id=chat_id)
        if not latest_chat:
            return jsonify({
                "error": "No chat items found for the given chat ID"
            }), 404
        
        with open(grouped_questions_dir, "r") as f:
            grouped_questions = json.load(f)
        
        results = []

        for item in grouped_questions:
            section = item["section"]

            total = 0
            answered = 0

            for group in item["grouped_questions"]:
                total += len(group["questions"])
                answered += sum(1 for q in group["questions"] if q.get("answered", False))

            percentage = (answered / total * 100) if total > 0 else 0

            results.append({
                "section": section,
                "answered": answered,
                "total": total,
                "percentage": round(percentage, 1)
            })

        return jsonify({"data": results}), 200

    # @staticmethod
    # @chat_bp.post("/process-user-answer")
    # def process_user_answer():
    #     return

    @staticmethod
    @chat_bp.post("/simulate-aspect-progress")
    def simulate_aspect_progress(self):
        data = request.get_json()

        group_id = int(data.get("group_id", 0))
        section = data.get("section")

        section_group_map = {
            "Depression": 2,
            "Anger": 2,
            "Mania": 4,
            "Anxiety": 2,
            "Somatic": 6,
            "Suicidal": 2,
            "Psychosis": 7,
            "Sleep Disturbance": 1,
            "Memory": 5,
            "Dissociation": 6,
            "Substance Use": 4,
            "Repetitive Thought": 3
        }

        sections = list(section_group_map.keys())
        current_index = sections.index(section) if section in sections else -1

        results = []

        for i, sec in enumerate(sections):
            total = section_group_map[sec]

            # previous sections → completed
            if i < current_index:
                answered = total

            # current section → partial
            elif i == current_index:
                answered = min(group_id, total)

            # next sections → not started
            else:
                answered = 0

            percentage = (answered / total * 100) if total > 0 else 0

            results.append({
                "section": sec,
                "answered": answered,
                "total": total,
                "percentage": round(percentage, 1)
            })

        return jsonify({"data": results}), 200
    
    @staticmethod
    @chat_bp.post("/simulate-conversation")
    def simulate_conversation(self):
        data = request.get_json()
        BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "..")
        conversation_simulation = os.path.join(BASE_DIR, "external_data", "conversation_simulation.json")

        with open(conversation_simulation, "r") as f:
            conversations = json.load(f)
        
        current_group_id = data.get("group_id")
        current_section = data.get("section")

        if current_section == "Opening":
            convo = conversations[1]
            payload = {
                "next_group_id": 1,
                "next_section": "Depression",
                "assistant_content": convo["content"]["assistant_question"]
            }
            return jsonify({
                "data": payload
            })
        
        section_group_map = {
            "Depression": 2,
            "Anger": 2,
            "Mania": 4,
            "Anxiety": 2,
            "Somatic": 6,
            "Suicidal": 2,
            "Psychosis": 7,
            "Sleep Disturbance": 1,
            "Memory": 5,
            "Dissociation": 6,
            "Substance Use": 4,
            "Repetitive Thought": 3
        }

        sections = list(section_group_map.keys())

        for i, convo in enumerate(conversations):

            if convo.get("role") != "user":
                continue

            content = convo.get("content", {})

            if (
                content.get("section") == current_section and
                content.get("group_id") == current_group_id
            ):

                max_group = section_group_map.get(current_section)
                current_index = sections.index(current_section)

                next_item = conversations[i + 1] if i + 1 < len(conversations) else None

                assistant_content = ""
                scores = []

                if next_item and next_item.get("role") == "assistant":
                    assistant_content = next_item.get("content", {}).get("assistant_question", "")
                    scores = next_item.get("content", {}).get("scores", [])

                if current_group_id >= max_group:
                    next_group_id = 1
                    next_section = (
                        sections[current_index + 1]
                        if current_index + 1 < len(sections)
                        else "Ending"
                    )
                else:
                    next_group_id = current_group_id + 1
                    next_section = current_section

                payload = {
                    "next_group_id": next_group_id,
                    "next_section": next_section,
                    "assistant_content": assistant_content,
                    "scores": scores
                }

                return jsonify({"data": payload}), 200   


            
    @staticmethod
    @chat_bp.post("/start-new-chat")
    def start_new_chat(self):
        data = request.get_json()

        user_id = data.get("user_id")
        if not user_id:
            return jsonify({
                "error": "User ID is required"
            }), 400
        
        chat = ChatService.start_new_chat(user_id=user_id)
        
        data = {
            "chat_id": str(chat._id),
            "start_time": chat.start_time,
        }

        return jsonify({
            "data": data
        }), 201

    @chat_bp.post("/process-chat")
    def add_chat_item(self):

        data = request.get_json()
        required_fields = ["chat_id", "mental_health_aspect", "group_id", "user_answer"]
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "error": f"{field} is required"
                }), 400
            
        user_query = {
            "section": data["mental_health_aspect"],
            "group_id": data["group_id"],
            "user_answer": data["user_answer"],
        }

        model_response = self.chatbot_engine.generate_response(user_query)

        is_a_survey = data["mental_health_aspect"] not in ["Opening", "Ending"]
        
        chat_type = "Survey" if is_a_survey else data["mental_health_aspect"]
        
        chat_item = ChatService.add_chat_item(
            section=data["mental_health_aspect"],
            type=chat_type,
            chat_id=data["chat_id"],
            user_answer=data["user_answer"],
            ai_response=model_response.get("assistant_question", ""),
        )

        if is_a_survey:
            for score_item in model_response.get("scores", []):
                ChatService.add_question_score(
                    chat_id=data["chat_id"],
                    section=data["mental_health_aspect"],
                    group_id=data["group_id"],
                    score=score_item.get("score"),
                    original_question=score_item.get("survey_question"),
                    chat_item_id=chat_item._id
                )


        return jsonify({
            "data": {
                "chat_item_id": str(chat_item._id),
                "mental_health_aspect": chat_item.mental_health_aspect,
                "original_question": chat_item.original_question,
                "ai_response": chat_item.ai_response,
                "user_answer": chat_item.user_answer,
                "generated_response": chat_item.generated_response,
                "score": chat_item.score,
                "created_at": chat_item.created_at
            }
        }), 201
    
    @staticmethod
    @chat_bp.get("/<chat_id>")
    def get_chat_detail(chat_id):
        chat = ChatService.get_chat_detail(chat_id=chat_id)
        if not chat:
            return jsonify({
                "error": "Chat not found"
            }), 404
        
        return jsonify({
            "data": chat
        }), 200
    
    @staticmethod
    @chat_bp.get("/user/<user_id>")
    def get_user_chats(user_id):
        chats = ChatService.get_user_chats(user_id=user_id)
        return jsonify({
            "data": chats
        }), 200
        
