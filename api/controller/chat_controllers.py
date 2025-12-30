import json
import os
from flask import Blueprint, request, jsonify
from datetime import datetime

from api.model.user_model import User
from api.model.chat_model import Chat
from api.model.chat_item_model import ChatItem

chat_bp = Blueprint("chat", __name__)

class ChatController:

    @staticmethod
    @chat_bp.get("/mental-health-aspect")
    def get_mental_health_aspect():
        return

    @staticmethod
    @chat_bp.post("/process-user-answer")
    def process_user_answer():
        return
    
    @staticmethod
    @chat_bp.post("/start-new-chat")
    def start_new_chat():
        return