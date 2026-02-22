# בס"ד - services/auth_service.py
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

class AuthService:
    @staticmethod
    def register_user(data):
        if User.query.filter_by(email=data.get('email')).first():
            return None, "User already exists"
        hashed_password = generate_password_hash(data.get('password'))
        new_user = User(
            email=data.get('email'),
            user_name=data.get('user_name'),
            password=hashed_password,
            role="Reader"
        )
        new_user.save()
        return new_user, None

    @staticmethod
    def login_user(data):
        user = User.query.filter_by(email=data.get('email')).first()
        if user and check_password_hash(user.password, data.get('password')):
            access_token = create_access_token(
                identity=str(user.id),
                additional_claims={"role": user.role}
            )
            return user, access_token
        return None, None

    @staticmethod
    def get_status(user_id):
        return User.query.get(user_id)

    # --- פונקציות ניהול ---

    @staticmethod
    def get_all_users():
        """שליפת כל המשתמשים עבור המנהל"""
        return User.query.all()

    @staticmethod
    def request_upgrade(user_id):
        user = User.query.get(user_id)
        if user:
            user.has_requested_upgrade = True
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_pending_upgrades():
        return User.query.filter_by(has_requested_upgrade=True, is_approved_uploader=False).all()

    @staticmethod
    def approve_user_upgrade(user_id):
        user = User.query.get(user_id)
        if user:
            user.role = "Content"
            user.is_approved_uploader = True
            user.has_requested_upgrade = False
            db.session.commit()
            return True
        return False