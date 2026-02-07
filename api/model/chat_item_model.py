from bson import ObjectId
from datetime import datetime
from config.config import db

chat_item_collection = db['chat_items']
chat_collection = db['chats']

class ChatItem:
    def __init__(self, type, ai_response=None, chat_id=None, _id=None, user_answer=None):
        self._id = _id or ObjectId()
        self.type = type
        self.user_answer = user_answer
        self.ai_response = ai_response
        self.chat_id = chat_id
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            "_id": self._id,
            "type": self.type,
            "ai_response": self.ai_response,
            "user_answer": self.user_answer,
            "chat_id": self.chat_id,
            "created_at": self.created_at
        }

    def save(self):
        return chat_item_collection.insert_one(self.to_dict())

    @classmethod
    def find_one(cls, query):
        data = chat_item_collection.find_one(query)
        if data:
            return cls(
                _id=data.get('_id'),
                type=data['type'],
                ai_response=data.get('ai_response'),
                chat_id=data.get('chat_id'),
                user_answer=data.get('user_answer')
            )
        return None
    
    def get_latest_item(chat_id):
        data = chat_item_collection.find_one(
            {"chat_id": chat_id},
            sort=[("created_at", -1)]
        )

        if not data:
            return None

        return ChatItem(
            _id=data.get('_id'),
            type=data['type'],
            ai_response=data.get('ai_response'),
            chat_id=data.get('chat_id'),
            user_answer=data.get('user_answer')
        )
