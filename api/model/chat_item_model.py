from bson import ObjectId
from datetime import datetime, timezone

class ChatItem:
    def __init__(self, type, ai_response=None, chat_id=None, _id=None, user_answer=None, created_at=None):
        self._id = _id or ObjectId()
        self.type = type
        self.user_answer = user_answer
        self.ai_response = ai_response
        self.chat_id = chat_id
        self.created_at = created_at or datetime.now(timezone.utc)

    def to_dict(self):
        return vars(self)

    @staticmethod
    def from_dict(data):
        if not data:
            return None
        return ChatItem(**data)