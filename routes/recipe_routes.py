# בס"ד - routes/recipe_routes.py המלא והמתוקן
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from controllers.recipe_controller import RecipeController
from services.recipe_service import RecipeService

recipe_bp = Blueprint('recipes', __name__)

@recipe_bp.route('/add_recipe', methods=['POST'])
@jwt_required()
def add_recipe():
    result, status_code = RecipeController.add_recipe(request.form, request.files)
    return jsonify(result), status_code

@recipe_bp.route('/', methods=['GET'])
def get_recipes():
    search_term = request.args.get('search')
    return jsonify(RecipeController.get_all_recipes(search_term))

@recipe_bp.route('/admin/archived', methods=['GET'])
@jwt_required()
def get_archived():
    # הנתיב שהיה חסר וגרם ל-404
    return jsonify(RecipeController.get_archived_recipes())

@recipe_bp.route('/restore_recipe/<int:id>', methods=['POST'])
@jwt_required()
def restore_recipe(id):
    if RecipeService.restore_recipe(id):
        return jsonify({"message": "Recipe restored"}), 200
    return jsonify({"error": "Not found"}), 404

@recipe_bp.route('/<int:id>', methods=['GET'])
def get_recipe_by_id(id):
    recipe = RecipeController.get_single_recipe(id)
    if not recipe: return jsonify({"error": "Recipe not found"}), 404
    return jsonify(recipe)

@recipe_bp.route('/delete_recipe/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_recipe(id):
    if RecipeService.delete_recipe(id):
        return jsonify({"message": "Archived"}), 200
    return jsonify({"error": "Not found"}), 404

@recipe_bp.route('/search_by_ingredients', methods=['POST'])
def search_by_ingredients():
    return jsonify(RecipeController.get_recipes_by_ingredients())

@recipe_bp.route('/rate', methods=['POST'])
@jwt_required()
def add_rating():
    result, status = RecipeController.add_rating()
    return jsonify(result), status