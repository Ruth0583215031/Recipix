# בס"ד - services/recipe_service.py המלא
import json
from models import db, Recipe, IngredientEntry, Rating

class RecipeService:
    @staticmethod
    def save_new_recipe(form_data, image_path, variations, user_id):
        new_recipe = Recipe(
            user_id=user_id,
            name=form_data.get('name'),
            type=form_data.get('type'),
            instructions=form_data.get('instructions'),
            image_path=image_path,
            variation_paths=json.dumps(variations),
            is_active=True
        )
        new_recipe.save()
        ingredients_raw = form_data.get('ingredients')
        if ingredients_raw:
            ingredients_list = json.loads(ingredients_raw)
            for item in ingredients_list:
                new_ing = IngredientEntry(
                    amount=item['amount'], unit=item['unit'],
                    product=item['product'], recipe_id=new_recipe.id
                )
                new_ing.save()
        return new_recipe

    @staticmethod
    def delete_recipe(recipe_id):
        recipe = Recipe.query.get(recipe_id)
        if recipe:
            recipe.is_active = False # מחיקה רכה
            db.session.commit()
            return True
        return False

    @staticmethod
    def restore_recipe(recipe_id):
        recipe = Recipe.query.get(recipe_id)
        if recipe:
            recipe.is_active = True # שחזור
            db.session.commit()
            return True
        return False

    @staticmethod
    def search_by_ingredients(user_ingredients_list):
        user_set = {ing.strip().lower() for ing in user_ingredients_list if ing.strip()}
        all_recipes = Recipe.query.filter_by(is_active=True).all()
        results = []
        for recipe in all_recipes:
            recipe_set = {ing.product.strip().lower() for ing in recipe.ingredients}
            if not recipe_set: continue
            common = user_set & recipe_set
            score = len(common) / len(recipe_set)
            if score >= 0.2:
                results.append({"recipe": recipe, "score": round(score * 100, 1)})
        results.sort(key=lambda x: x['score'], reverse=True)
        return results

    @staticmethod
    def add_rating(user_id, recipe_id, score):
        # בדיקה אם המשתמש כבר דירג את המתכון הזה - אפשר לעדכן במקום ליצור חדש
        existing = Rating.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
        if existing:
            existing.score = score
        else:
            new_rating = Rating(user_id=user_id, recipe_id=recipe_id, score=score)
            db.session.add(new_rating)

        db.session.commit()
        return True