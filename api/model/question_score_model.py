from bson import ObjectId
from datetime import datetime, timezone

class QuestionScore:
    def __init__(self, section, original_question, score, chat_item_id, group_id=None, _id=None, created_at=None):
        self._id = _id or ObjectId()
        self.section = section
        self.group_id = group_id
        self.original_question = original_question
        self.score = score
        self.chat_item_id = chat_item_id
        self.created_at = created_at or datetime.now(timezone.utc)

    def to_dict(self):
        return vars(self)

    @staticmethod
    def from_dict(data):
        if not data:
            return None
        return QuestionScore(**data)