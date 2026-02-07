from api.model.user_model import User

class UserRepository:

    @staticmethod
    def find_by_email(email: str):
        return User.find_one({"email": email})

    @staticmethod
    def create_user(username: str, email: str, hashed_password: str, role: str):
        user = User(username=username, email=email, password=hashed_password, role=role)
        user.save()
        return user
    
    @staticmethod
    def get_all_users():
        return User.find_all()
