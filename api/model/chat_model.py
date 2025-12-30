from bson import ObjectId
from datetime import datetime
from config.config import db

chat_collection = db['chats']
chat_item_collection = db['chat_items']

class Chat:
    def __init__(self, summary="", start_time=None, end_time=None, valid=True, user_id=None, _id=None):
        self._id = _id or ObjectId()
        self.summary = summary
        self.start_time = start_time or datetime.utcnow()
        self.end_time = end_time
        self.valid = valid
        self.user_id = user_id

    def to_dict(self):
        return {
            "_id": self._id,
            "summary": self.summary,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "valid": self.valid,
            "user_id": self.user_id
        }

    def save(self):
        return chat_collection.insert_one(self.to_dict())

    def get_responses(self):
        return list(chat_item_collection.find({"chat_id": self._id}))

    @classmethod
    def find_one(cls, query):
        data = chat_collection.find_one(query)
        if data:
            return cls(
                summary=data.get('summary', ''),
                start_time=data.get('start_time'),
                end_time=data.get('end_time'),
                valid=data.get('valid', True),
                user_id=data.get('user_id'),
                _id=data.get('_id')
            )
        return None

    @classmethod
    def find_all(cls, query):
        cursor = chat_collection.find(query).sort("start_time", 1)
        return [
            {
                "_id": str(item.get('_id')),
                "summary": item.get('summary', ''),
                "start_time": item.get('start_time'),
                "end_time": item.get('end_time'),
                "valid": item.get('valid', True),
                "user_id": str(item.get('user_id'))
            }
            for item in cursor
        ]
