from api.model.chat_model import Chat
from bson import ObjectId

class ChatRepository:
    @staticmethod
    def create_chat(summary="", start_time=None, end_time=None, valid=True, user_id=None):
        chat = Chat(
            summary=summary,
            start_time=start_time,
            end_time=end_time,
            valid=valid,
            user_id=user_id
        )
        chat.save()
        return chat

    @staticmethod
    def get_by_id(chat_id):
        return Chat.find_one({"_id": ObjectId(chat_id)})
    
    @staticmethod
    def get_all_by_user(user_id):
        return Chat.find_one({"user_id": user_id})
    
    @staticmethod
    def get_all_valid_chats(user_id):
        return Chat.find_all({"user_id": user_id, "valid": True})
    
    @staticmethod
    def get_user_assessments(user_id, chat_id):
        return Chat.find_all({"user_id": user_id, "_id": ObjectId(chat_id)})


