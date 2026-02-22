# check_users.py
from app import app
from models import User

with app.app_context():
    users = User.query.all()
    print(f"\n--- רשימת משתמשים (נמצאו {len(users)}) ---")
    for u in users:
        print(f"Name: {u.user_name} | Role: {u.role} | Requested: {u.has_requested_upgrade} | Approved: {u.is_approved_uploader}")