# בס"ד - controllers/recipe_controller.py
from flask import jsonify, request
import json
from schemas import RecipeSchema, IngredientSchema, RatingSchema
from flask_jwt_extended import get_jwt_identity
from services.recipe_service import RecipeService
from utils.image_utils import ImageUtils
from models import User, Recipe, Rating, db
from sqlalchemy import func, or_


class RecipeController:
    @staticmethod
    def add_recipe(form_data, files):
        """הוספת מתכון חדש עם אימות נתונים והעלאת תמונה"""
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        # בדיקת הרשאות: רק מנהל או מעלה תוכן מאושר
        if not user or (user.role != "Admin" and not user.is_approved_uploader):
            return {"error": "Unauthorized"}, 403

        data_to_validate = form_data.to_dict()
        ingredients_raw = data_to_validate.pop('ingredients', '[]')

        # אימות נתוני המתכון
        recipe_schema = RecipeSchema()
        errors = recipe_schema.validate(data_to_validate)
        if errors:
            return {"error": errors}, 400

        # אימות נתוני הרכיבים
        try:
            ings = json.loads(ingredients_raw)
            ing_schema = IngredientSchema(many=True)
            ing_errors = ing_schema.validate(ings)
            if ing_errors:
                return {"error": {"ingredients": ing_errors}}, 400
        except json.JSONDecodeError:
            return {"error": "מבנה רכיבים לא תקין"}, 400

        try:
            if 'image' not in files:
                return {"error": "חובה לצרף תמונה"}, 400

            # שמירת תמונות ויצירת ווריאציות
            image_path, variations = ImageUtils.save_recipe_images(files['image'])

            # שמירה סופית במסד הנתונים
            recipe = RecipeService.save_new_recipe(form_data, image_path, variations, user.id)
            return {"message": "Recipe added", "id": recipe.id}, 201
        except Exception as e:
            return {"error": str(e)}, 400

    @staticmethod
    def get_all_recipes(search_term=None):
        # קבלת פרמטרים נוספים מהבקשה
        recipe_type = request.args.get('type')  # חלבי, בשרי, פרווה
        min_rating = request.args.get('min_rating', type=float)  # דירוג מינימלי

        query = Recipe.query.filter_by(is_active=True)

        # סינון לפי מילת חיפוש
        if search_term:
            query = query.filter(Recipe.name.contains(search_term))

        # סינון לפי סוג
        if recipe_type and recipe_type != 'All':
            query = query.filter_by(type=recipe_type)

        recipes = query.all()

        # עיצוב התוצאות
        results = [RecipeController._format_recipe(r) for r in recipes]

        # סינון לפי דירוג (מתבצע אחרי החישוב ב-_format_recipe)
        if min_rating:
            results = [r for r in results if r['rating'] >= min_rating]

        return results

    @staticmethod
    def get_single_recipe(recipe_id):
        """שליפת מתכון בודד לפי מזהה"""
        recipe = Recipe.query.get(recipe_id)
        if not recipe: return None
        return RecipeController._format_recipe(recipe)

    @staticmethod
    def get_recipes_by_ingredients():
        """חיפוש משוכלל לפי רכיבים (Matching Score)"""
        data = request.get_json()
        user_ingredients = data.get('ingredients', [])

        if not user_ingredients:
            return jsonify([]), 200

        scored_results = RecipeService.search_by_ingredients(user_ingredients)

        # עיצוב התוצאות והוספת ציון ההתאמה
        formatted_results = []
        for item in scored_results:
            recipe_data = RecipeController._format_recipe(item['recipe'])
            recipe_data['match_score'] = item['score']
            formatted_results.append(recipe_data)

        return formatted_results

    @staticmethod
    def get_archived_recipes():
        """שליפת מתכונים מהארכיון (לשימוש מנהל בלבד)"""
        archived = Recipe.query.filter_by(is_active=False).all()
        return [RecipeController._format_recipe(r) for r in archived]

    @staticmethod
    def delete_recipe(recipe_id):
        """מחיקה רכה - העברה לארכיון"""
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        recipe = Recipe.query.get(recipe_id)

        if not recipe: return {"error": "מתכון לא נמצא"}, 404

        # בדיקת הרשאות (כפי שראינו בסרטון)
        if user.role != "Admin" and recipe.user_id != user.id:
            return {"error": "אין לך הרשאה למחוק מתכון זה"}, 403

        recipe.is_active = False  # שינוי הסטטוס בלבד
        db.session.commit()
        return {"message": "המתכון הועבר לארכיון"}, 200

    @staticmethod
    def restore_recipe(recipe_id):
        """שחזור מהארכיון - למנהל בלבד"""
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if user.role != "Admin":
            return {"error": "רק מנהל יכול לשחזר מתכונים"}, 403

        recipe = Recipe.query.get(recipe_id)
        if not recipe: return {"error": "מתכון לא נמצא"}, 404

        recipe.is_active = True
        db.session.commit()
        return {"message": "המתכון שוחזר בהצלחה"}, 200

    @staticmethod
    def _format_recipe(r):
        """פונקציית עזר לעיצוב אובייקט המתכון ל-JSON"""
        base_url = request.host_url.rstrip('/')
        # נרמול נתיב התמונה לתצוגה בדפדפן
        path_part = r.image_path.split('uploads')[-1].replace('\\', '/').strip('/')

        # חישוב ממוצע דירוגים
        avg_rating = db.session.query(func.avg(Rating.score)).filter(Rating.recipe_id == r.id).scalar() or 0

        return {
            'id': r.id,
            'name': r.name,
            'user_id': r.user_id,
            'type': r.type,
            'instructions': r.instructions,
            'image_url': f"{base_url}/uploads/{path_part}",
            'variations': json.loads(r.variation_paths),
            'ingredients': [{'amount': i.amount, 'unit': i.unit, 'product': i.product} for i in r.ingredients],
            'rating': round(avg_rating, 1),
            'is_active': r.is_active
        }

    @staticmethod
    def add_rating():
        current_user_id = get_jwt_identity()
        data = request.get_json()

        # ולידציה
        schema = RatingSchema()
        errors = schema.validate(data)
        if errors: return {"error": errors}, 400

        RecipeService.add_rating(current_user_id, data['recipe_id'], data['score'])
        return {"message": "Rating saved"}, 200