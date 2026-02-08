from api.model.chat_item_model import ChatItem
from config.config import db
from bson import ObjectId

chat_item_collection = db['chat_items']

class ChatItemRepository:
    @staticmethod
    def create(type, chat_id, ai_response=None, user_answer=None):
        chat_item = ChatItem(
            type=type,
            chat_id=chat_id,
            ai_response=ai_response,
            user_answer=user_answer
        )
        chat_item_collection.insert_one(chat_item.to_dict())
        return chat_item

    @staticmethod
    def get_by_id(item_id: str):
        data = chat_item_collection.find_one({"_id": ObjectId(item_id)})
        return ChatItem.from_dict(data)

    @staticmethod
    def get_latest_item(chat_id):
        data = chat_item_collection.find_one(
            {"chat_id": chat_id},
            sort=[("created_at", -1)]
        )
        return ChatItem.from_dict(data)

    @staticmethod
    def get_all_by_chat(chat_id):
        cursor = chat_item_collection.find({"chat_id": chat_id}).sort("created_at", 1)
        return [ChatItem.from_dict(item) for item in cursor]

    @staticmethod
    def update(item_id: str, **payload):
        result = chat_item_collection.update_one(
            {"_id": ObjectId(item_id)},
            {"$set": payload}
        )
        return result.modified_count > 0

    @staticmethod
    def delete_by_chat(chat_id):
        result = chat_item_collection.delete_many({"chat_id": chat_id})
        return result.deleted_count