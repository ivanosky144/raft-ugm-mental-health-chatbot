from bson import ObjectId
from datetime import datetime
from config.config import db

question_score_collection = db['question_scores']

class QuestionScore:
    def __init__(self, section, original_question, score, chat_item_id, group_id=None, _id=None):
        self._id = _id or ObjectId()
        self.section = section
        self.group_id = group_id
        self.original_question = original_question
        self.score = score
        self.chat_item_id = chat_item_id
        self.created_at = datetime.utcnow()
    
    def to_dict(self):
        return {
            "_id": self._id,
            "section": self.section,
            "group_id": self.group_id,
            "original_question": self.original_question,
            "score": self.score,
            "chat_item_id": self.chat_item_id,
            "created_at": self.created_at
        }

    def save(self):
        return question_score_collection.insert_one(self.to_dict())
    
    @classmethod
    def find_one(cls, query):
        data = question_score_collection.find_one(query)
        if data:
            return cls(
                _id=data.get('_id'),
                section=data['section'],
                group_id=data.get('group_id'),
                original_question=data['original_question'],
                score=data['score'],
                chat_item_id=data['chat_item_id']
            )
        return None