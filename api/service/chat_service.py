from datetime import datetime
from bson import ObjectId
from api.repository.chat_repository import ChatRepository
from api.repository.chat_item_repository import ChatItemRepository
from api.repository.question_score_repository import QuestionScoreRepository


class ChatService:
    @staticmethod
    def start_new_chat(user_id):
        chat = ChatRepository.create(
            summary="",
            start_time=datetime.utcnow(),
            end_time=None,
            valid=False,
            user_id=user_id
        )

        return chat
    
    @staticmethod
    def add_chat_item(
        chat_id,
        type,
        user_answer=None,
        ai_response=None,
    ):
        chat_item = ChatItemRepository.create(
            user_answer=user_answer,
            ai_response=ai_response,
            type=type,
            chat_id=chat_id
        )
        return chat_item
    
    @staticmethod
    def add_question_score(
        section,
        original_question,
        score,
        chat_item_id,
        group_id=None
    ):
        question_score = QuestionScoreRepository.create(
            section=section,
            original_question=original_question,
            score=score,
            chat_item_id=chat_item_id,
            group_id=group_id
        )
        return question_score
    
    
    @staticmethod
    def get_chat(chat_id):
        return ChatRepository.get_by_id(chat_id)
    
    @staticmethod
    def get_latest_chat_item(chat_id):
        return ChatItemRepository.get_latest_item(chat_id)
    
    @staticmethod
    def get_user_chats(user_id):
        return ChatRepository.get_all_by_user(user_id)
    
    