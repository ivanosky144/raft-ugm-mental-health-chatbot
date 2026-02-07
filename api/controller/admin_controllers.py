from api.service.admin_service import AdminService
from flask import Blueprint, request, jsonify

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

class AdminController:
    @staticmethod
    @admin_bp.get("/all-valid-chats")
    def get_all_valid_chats(user_id):
        chats = AdminService.get_all_valid_chats(user_id)
        chat_list = [chat.to_dict() for chat in chats]
        return jsonify({"data": chat_list}), 200
    
    @staticmethod
    @admin_bp.get("/all-users")
    def get_all_users():
        users = AdminService.get_all_users()
        user_list = [user.to_dict() for user in users]
        return jsonify({"data": user_list}), 200
    
    @staticmethod
    @admin_bp.get("/user-assessments")
    def get_user_assessments():
        user_id = request.args.get("user_id")
        assessments = AdminService.get_user_assesments(user_id)
        assessment_list = [assessment.to_dict() for assessment in assessments]
        return jsonify({"data": assessment_list}), 200