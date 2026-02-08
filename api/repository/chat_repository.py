from api.model.chat_model import Chat
from config.config import db
from bson import ObjectId

chat_collection = db['chats']

class ChatRepository:
    
    @staticmethod
    def create(summary="", user_id=None, excel_file_path=""):
        chat = Chat(summary=summary, user_id=user_id, excel_file_path=excel_file_path)
        chat_collection.insert_one(chat.to_dict())
        return chat

    @staticmethod
    def get_by_id(chat_id: str):
        data = chat_collection.find_one({"_id": ObjectId(chat_id)})
        return Chat.from_dict(data)

    @staticmethod
    def get_all_by_user(user_id: str, only_valid=True):
        query = {"user_id": user_id}
        if only_valid:
            query["valid"] = True
            
        cursor = chat_collection.find(query).sort("start_time", 1)
        return [Chat.from_dict(item) for item in cursor]

    @staticmethod
    def update(chat_id: str, **payload):
        result = chat_collection.update_one(
            {"_id": ObjectId(chat_id)}, 
            {"$set": payload}
        )
        if result.modified_count > 0:
            return ChatRepository.get_by_id(chat_id)
        return None

    @staticmethod
    def delete(chat_id: str):
        result = chat_collection.delete_one({"_id": ObjectId(chat_id)})
        return result.deleted_count > 0