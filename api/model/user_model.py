from bson import ObjectId
from datetime import datetime
from config.config import db

users_collection = db['users']
dialogs_collection = db['dialogs']

class User:
    def __init__(self, username, email, password, role, _id=None):
        self._id = _id or ObjectId()
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            "_id": self._id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "created_at": self.created_at
        }

    def save(self):
        return users_collection.insert_one(self.to_dict())

    def get_dialogs(self):
        return list(dialogs_collection.find({"user_id": self._id}))

    @classmethod
    def find_one(cls, query):
        data = users_collection.find_one(query)
        if data:
            return cls(
                username=data.get('username'),
                email=data.get('email'),
                password=data.get('password'),
                role=data.get('role'),
                _id=data.get('_id')
            )
        return None

    @classmethod
    def find_all():
        return list(users_collection.find())