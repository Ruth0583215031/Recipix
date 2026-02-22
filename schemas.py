# בס"ד - schemas.py
from marshmallow import Schema, fields, validate

class IngredientSchema(Schema):
    amount = fields.Float(required=True, validate=validate.Range(min=0.1, error="כמות חייבת להיות גדולה מ-0"))
    unit = fields.Str(required=True)
    product = fields.Str(required=True, validate=validate.Length(min=2, error="שם מוצר חייב להכיל לפחות 2 תווים"))

class RecipeSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=3, error="שם המתכון חייב להכיל לפחות 3 תווים"))
    type = fields.Str(required=True, validate=validate.OneOf(["Dairy", "Meat", "Parve"], error="סוג מתכון לא תקין"))
    instructions = fields.Str(required=True, validate=validate.Length(min=10, error="הוראות הכנה חייבות להכיל לפחות 10 תווים"))

class RatingSchema(Schema):
    score = fields.Int(required=True, validate=validate.Range(min=1, max=5))
    recipe_id = fields.Int(required=True)