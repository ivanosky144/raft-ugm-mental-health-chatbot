from datetime import datetime
from api.repository.chat_repository import ChatRepository
from api.repository.user_repository import UserRepository

class AdminService:
    @staticmethod
    def get_all_valid_chats(user_id):
        return ChatRepository.get_all_valid_chats(user_id)
    
    @staticmethod
    def get_all_users():
        return UserRepository.get_all_users()
    
    @staticmethod
    def  get_user_assesments(chat_id):
        return ChatRepository.get_by_id(chat_id)