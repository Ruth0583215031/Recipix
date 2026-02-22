# בס"ד
from app import app, db
from models import User

with app.app_context():
    # שים כאן את המייל שאיתו נרשמת לאתר
    user_email = "a@a"

    user = User.query.filter_by(email=user_email).first()

    if user:
        user.role = "Admin"
        user.is_approved_uploader = True
        db.session.commit()
        # שינוי מ-user.name ל-user.user_name
        print(f"המשתמש {user.user_name} הוגדר כעת כמנהל (Admin)!")
    else:
        print("המשתמש לא נמצא. וודא שהמייל נכון.")