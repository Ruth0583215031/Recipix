# בס"ד - app.py (גרסה סופית ומשופרת להגשה)
import os
from dotenv import load_dotenv
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
from models import db
from routes.auth_routes import auth_bp
from routes.recipe_routes import recipe_bp

load_dotenv()

app = Flask(__name__)
CORS(app)

# הגדרות מסד נתונים
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///recipes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# הגדרות אבטחה
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)

jwt = JWTManager(app)
db.init_app(app)
with app.app_context():
    db.create_all() # פקודה זו יוצרת את קובץ ה-db ואת כל הטבלאות לפי המודלים

app.url_map.strict_slashes = False

# --- תוספת מומלצת: טיפול גלובלי בשגיאות ---
@app.errorhandler(Exception)
def handle_exception(e):
    """תופס כל שגיאה בשרת ומחזיר אותה בפורמט JSON מסודר"""
    print(f"Server Error: {str(e)}") # הדפסה לטרמינל לדיבאג
    return jsonify({
        "error": "משהו השתבש בשרת",
        "details": str(e)
    }), 500

# רישום Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(recipe_bp, url_prefix='/recipes')

@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    return send_from_directory('uploads', filename)

# בלוק ההרצה (וודא שהוא קיים בסוף הקובץ)
if __name__ == "__main__":
    app.run(debug=True)