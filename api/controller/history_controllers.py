from flask import Blueprint, jsonify

from api.model.user_model import User
from api.model.chat_model import Chat
from api.model.chat_item_model import ChatItem


history_bp = Blueprint("history", __name__)


class HistoryController:

    def __init__(self):
        pass

    @staticmethod
    @history_bp.route("/api/get-all-chat/<string:email>", methods=["GET"])
    def get_all_chat(email):
        user = User.find_one({"email": email})
        if not user:
            return jsonify({"status": 404, "message": "User not found"})

        dialogs = Chat.find_all({"user_id": user._id})
        return jsonify({"status": 200, "data": dialogs})

    @staticmethod
    @history_bp.route("/api/get-chat-histories/<string:chat_id>", methods=["GET"])
    def get_chat_histories(chat_id):
        responses = ChatItem.find_all({"chat_id": chat_id})

        if not responses:
            return jsonify({"status": 404, "message": "Chat histories not found"})

        return jsonify({
            "status": 200,
            "message": "Chat histories retrieved",
            "data": [resp.to_dict() for resp in responses]
        })
