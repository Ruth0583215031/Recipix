# בסד
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, Float, ForeignKey


class Base(DeclarativeBase):
    pass


# אתחול של מסד הנתונים
db = SQLAlchemy(model_class=Base)


# --- מודלים (Models) ---
# מחלקה אבסטרקטית בסיסית שכל המחלקות יירשו ממנה
class BaseModel(db.Model):
    __abstract__ = True
    # משתנה ייחודי שגדל אוטומטית
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # פונקצית שמירה
    def save(self):
        db.session.add(self)
        db.session.commit()


class User(BaseModel):
    __tablename__ = 'users'
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    user_name: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, default="Reader")  # Reader, Content, Admin דרגה:
    is_approved_uploader: Mapped[bool] = mapped_column(Boolean, default=False)  # האם יש הרשאה להוספת מתכונים
    has_requested_upgrade: Mapped[bool] = mapped_column(Boolean, default=False)  # האם הייתה בקשה להעלאה

    recipes = relationship("Recipe", back_populates="user")  # למשתמש אחד יכולים להיות הרבה מתכונים
    ratings = relationship("Rating", back_populates="user")  # למשתמש אחד יכולים להיות הרבה דירוגים


# בס"ד - models.py (מעודכן)
class Recipe(BaseModel):
    __tablename__ = 'recipes'
    name: Mapped[str] = mapped_column(String, nullable=False)
    image_path: Mapped[str] = mapped_column(String, nullable=False)
    variation_paths: Mapped[str] = mapped_column(String, nullable=False)
    instructions: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    # שדה חדש לניהול ארכיון
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user = relationship("User", back_populates="recipes")
    ingredients = relationship("IngredientEntry", back_populates="recipe", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="recipe", cascade="all, delete-orphan")

class IngredientEntry(BaseModel):
    __tablename__ = 'ingredients'
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String, nullable=False)
    product: Mapped[str] = mapped_column(String, nullable=False)
    recipe_id: Mapped[int] = mapped_column(ForeignKey('recipes.id'), nullable=False)
    recipe = relationship("Recipe", back_populates="ingredients")


class Rating(BaseModel):
    __tablename__ = 'ratings'
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    recipe_id: Mapped[int] = mapped_column(ForeignKey('recipes.id'), nullable=False)

    user = relationship("User", back_populates="ratings")
    recipe = relationship("Recipe", back_populates="ratings")