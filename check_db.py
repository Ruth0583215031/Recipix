from app import app
from  models import ( db, Recipe)


def show_data():
    with app.app_context():
        # שליפת כל המתכונים
        recipes = Recipe.query.all()

        print(f"\n📊 נמצאו {len(recipes)} מתכונים בדאטה-בייס:\n" + "-" * 40)

        for r in recipes:
            print(f"🆔 מזהה מתכון: {r.id}")
            print(f"🍽️ סוג: {r.type}")
            print(f"📝 הוראות: {r.instructions}")
            print("🥗 רכיבים:")
            # לולאה על הרכיבים של המתכון
            for ing in r.ingredients:
                print(f"   - {ing.amount} {ing.unit} של {ing.product}")
            print("-" * 40)


if __name__ == "__main__":
    show_data()