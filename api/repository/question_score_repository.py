from api.model.question_score_model import QuestionScore

class QuestionScoreRepository:
    @staticmethod
    def create_question_score(
        section,
        original_question,
        score,
        chat_item_id,
        group_id=None
    ):
        question_score = QuestionScore(
            section=section,
            original_question=original_question,
            score=score,
            chat_item_id=chat_item_id,
            group_id=group_id
        )
        question_score.save()
        return question_score