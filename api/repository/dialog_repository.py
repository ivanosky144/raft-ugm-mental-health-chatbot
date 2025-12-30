from api.model.chat_model import Dialog

class DialogRepository:
    @staticmethod
    def create_dialog(summary="", start_time=None, end_time=None, valid=True, user_id=None):
        dialog = Dialog(
            summary=summary,
            start_time=start_time,
            end_time=end_time,
            valid=valid,
            user_id=user_id
        )
        dialog.save()
        return dialog

