# בס"ד - utils/image_utils.py
import os
import uuid
from PIL import Image, ImageOps, ImageEnhance
from werkzeug.utils import secure_filename

class ImageUtils:
    @staticmethod
    def save_recipe_images(file):
        recipe_uid = str(uuid.uuid4())
        folder = os.path.join('uploads', recipe_uid)
        os.makedirs(folder, exist_ok=True)

        filename = secure_filename(file.filename)
        original_path = os.path.join(folder, filename)
        file.save(original_path)

        variations = []
        with Image.open(original_path) as img:
            img = img.convert("RGB")

            # 1. פילטר Sepia - "מראה וינטג' קלאסי"
            sepia_img = ImageOps.colorize(img.convert("L"), "#704214", "#C0A080")
            sepia_path = os.path.join(folder, f"sepia_{filename}")
            sepia_img.save(sepia_path)
            variations.append({"title": "מראה וינטג' (Sepia)", "path": sepia_path})

            # 2. חידוד - "הדגשת טקסטורת האוכל"
            sharp_img = ImageEnhance.Sharpness(img).enhance(2.0)
            sharp_path = os.path.join(folder, f"sharp_{filename}")
            sharp_img.save(sharp_path)
            variations.append({"title": "חידוד פרטים (Sharp)", "path": sharp_path})

            # 3. הבהרה - "תאורת סטודיו מוארת"
            bright_img = ImageEnhance.Brightness(img).enhance(1.2)
            bright_path = os.path.join(folder, f"bright_{filename}")
            bright_img.save(bright_path)
            variations.append({"title": "תאורה מוגברת (Bright)", "path": bright_path})

        return original_path, variations