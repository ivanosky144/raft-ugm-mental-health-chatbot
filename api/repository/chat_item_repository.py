from api.model.chat_item_model import ChatItem


class ChatItemRepository:
    @staticmethod
    def create_chat_item(
        user_answer=None,
        ai_response=None,
        type=None,
        chat_id=None,
    ):
        chat_item = ChatItem(
            user_answer=user_answer,
            ai_response=ai_response,
            type=type,
            chat_id=chat_id,
        )
        chat_item.save()
        return chat_item
    
    @staticmethod
    def get_latest_item(chat_id):
        return ChatItem.get_latest_item(chat_id)