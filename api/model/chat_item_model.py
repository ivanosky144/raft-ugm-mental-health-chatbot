from bson import ObjectId
from datetime import datetime
from config.config import db

chat_item_collection = db['chat_items']
chat_collection = db['chats']

class ChatItem:
    def __init__(self, section, question=None, score=None, dialog_id=None, _id=None, question_key=None, generated_response=None, user_answer=None):
        self._id = _id or ObjectId()
        self.section = section
        self.generated_response = generated_response
        self.user_answer = user_answer
        self.question = question
        self.question_key = question_key
        self.score = score
        self.dialog_id = dialog_id
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            "_id": self._id,
            "section": self.section,
            "question": self.question,
            "generated_response": self.generated_response,
            "score": self.score,
            "user_answer": self.user_answer,
            "dialog_id": self.dialog_id,
            "question_key": self.question_key,
            "created_at": self.created_at
        }

    def save(self):
        return chat_item_collection.insert_one(self.to_dict())

    @classmethod
    def find_one(cls, query):
        data = chat_item_collection.find_one(query)
        if data:
            return cls(
                section=data['section'],
                question=data.get('question'),
                question_key=data.get('question_key'),
                score=data.get('score'),
                dialog_id=data.get('dialog_id'),
                _id=data.get('_id'),
                generated_response=data.get('generated_response'),
                user_answer=data.get('user_answer')
            )
        return None
