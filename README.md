# 👨‍🍳 Recipix - Full Stack Recipe Community Platform

מערכת מקיפה לניהול, שיתוף ודירוג מתכונים, המשלבת טכנולוגיות מתקדמות בצד השרת ובצד הלקוח. הפרויקט נבנה בדגש על חוויית משתמש חלקה, ניהול הרשאות קפדני ועיבוד תמונה אוטומטי.

## 🌟 תכונות מרכזיות (Key Features)

### 🔐 מערכת הרשאות מבוססת תפקידים (RBAC)
* **Reader:** צפייה במתכונים ודירוג הקהילה.
* **Content Creator:** הוספה וניהול של מתכונים אישיים (לאחר אישור מנהל).
* **Admin:** ניהול מלא של משתמשים, אישור בקשות שדרוג וניהול ארכיון מתכונים.

### 🥗 אלגוריתם חיפוש "מה יש לי במקרר?"
* מנוע חיפוש חכם המחשב **ציון התאמה (Match Score)** באחוזים בין הרכיבים שבידי המשתמש לבין המצרכים במתכון.

### 🖼️ עיבוד תמונה אוטומטי (Image Processing)
כל תמונה שמועלית עוברת עיבוד בצד השרת באמצעות ספריית **Pillow** ליצירת שלוש וריאציות:
1. **Sepia:** מראה וינטג' נוסטלגי.
2. **Sharp:** חידוד פרטי המנה למראה מקצועי.
3. **Bright:** שיפור תאורה וצבעים.

### 📊 ניהול נתונים ודירוג
* מערכת דירוג כוכבים (1-5) עם חישוב ממוצע דירוגים אוטומטי.
* ניהול ארכיון בשיטת **Soft Delete** (מחיקה רכה ושחזור).

---

## 🛠️ טכנולוגיות (Tech Stack)

### **Backend (Python & Flask)**
* **Framework:** Flask
* **Database:** SQLite עם SQLAlchemy
* **Security:** JWT (JSON Web Tokens) לאימות מאובטח
* **Validation:** Marshmallow (סיריאליזציה וולידציה)
* **Processing:** Pillow (עיבוד תמונה מתקדם)

### **Frontend (Angular)**
* **Version:** Angular 17+ (Standalone Components)
* **Forms:** Reactive Forms עם Custom Validators
* **Interceptors:** ניהול טוקנים אוטומטי בבקשות HTTP
* **UI:** Bootstrap 5 בשילוב CSS מותאם אישית

---

## 📁 מבנה הפרויקט (Architecture)

```text
Recipix/
├── app.py                # הגדרות שרת, JWT ו-Blueprints
├── models.py             # הגדרת סכמות מסד הנתונים
├── schemas.py            # ולידציה של נתוני קלט
├── controllers/          # לוגיקה עסקית (RecipeController)
├── services/             # שכבת שירותי הנתונים (Auth/Recipe Services)
├── routes/               # הגדרת ה-Endpoints
├── utils/                # כלי עזר (ImageUtils)
├── client/               # פרויקט האנגולר המלא
└── recipes.db            # מסד הנתונים
