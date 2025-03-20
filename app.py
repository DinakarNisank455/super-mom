from flask import Flask, render_template, request, redirect, session, flash, url_for
import pymysql
from datetime import datetime
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
import requests

app = Flask(__name__)

# 🔹 Secret Key & Session Config
app.secret_key = "secret_key"
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
Session(app)

# 🔹 API Keys (Recipe Search)
app_id = "9339488b"
app_key = "4f804a4822c6c387579112bcda286297"

# ✅ Function to Establish Database Connection
def get_db_connection():
    return pymysql.connect(host="localhost", user="root", password="@Bunny455", database="prr")

# ✅ Generate Unique User ID
def generate_user_id():
    db = get_db_connection()
    cursor = db.cursor()
    today = datetime.today().strftime('%Y%m%d')
    cursor.execute("SELECT COUNT(*) FROM users WHERE user_id LIKE %s", (today + "%",))
    count = cursor.fetchone()[0] + 1
    db.close()
    return f"{today}{count:03d}"  # Format: YYYYMMDD001

# 🔹 Home Page
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if not all([name, email, password]):
            flash("⚠️ Please fill in all required fields!", "error")
            return redirect(url_for("signup"))

        hashed_password = generate_password_hash(password)  # ✅ Fixed

        user_id = generate_user_id()
        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            flash("⚠️ User already exists!", "error")
            return redirect(url_for("signup"))

        cursor.execute("INSERT INTO users (user_id, email, password) VALUES (%s, %s, %s)", (user_id, email, hashed_password))
        db.commit()
        cursor.close()
        db.close()

        flash("✅ Signup successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not email or not password:
            flash("⚠️ Please enter both email and password.", "error")
            return redirect(url_for("login"))

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT user_id, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        db.close()

        if user and check_password_hash(user[1], password):  # ✅ Fixed
            session["user_id"] = user[0]
            flash("✅ Login successful!", "success")
            return redirect(url_for("dashboard"))

        flash("⚠️ Invalid credentials.", "error")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['new_password']

        hashed_password = generate_password_hash(new_password)  # ✅ Fixed

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("UPDATE users SET password = %s WHERE email = %s", (hashed_password, email))
        db.commit()
        cursor.close()
        db.close()

        flash('✅ Password reset successful. You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('forgot_password.html')


# ✅ Dashboard Route
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("home"))

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (session["user_id"],))
    user = cursor.fetchone()
    cursor.close()
    db.close()

    return render_template("dashboard.html", user=user)

# ✅ Recipe Search Route
@app.route('/recipe_search', methods=['GET', 'POST'])
def recipe_search():
    query = request.args.get('query', '').strip()

    if not query:
        return render_template("recipe_search.html", recipes=[])

    api_url = f"https://api.edamam.com/api/recipes/v2?q={query}&app_id={app_id}&app_key={app_key}&type=public"
    response = requests.get(api_url)
    data = response.json()

    recipes = []
    if "hits" in data:
        for hit in data["hits"]:
            recipe = hit["recipe"]
            recipes.append({
                "name": recipe["label"],
                "image": recipe["image"],
                "recipe_link": recipe["url"],
                "diet_type": ", ".join(recipe.get("dietLabels", ["N/A"])),
                "ingredients": recipe.get("ingredientLines", []),
                "nutrition": {
                    "calories": int(recipe["calories"]) if "calories" in recipe else "N/A",
                    "protein": recipe["totalNutrients"].get("PROCNT", {}).get("quantity", "N/A"),
                    "fat": recipe["totalNutrients"].get("FAT", {}).get("quantity", "N/A")
                },
                "source_name": recipe["source"],
                "source_url": recipe["url"]
            })

    session["search_results"] = recipes  # Store results in session

    return render_template('recipe_search.html', recipes=recipes)

# ✅ Recipe Detail Route (Fixed)
@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    recipes = session.get("search_results", [])

    if 0 <= recipe_id < len(recipes):
        return render_template("recipe_detail.html", recipe=recipes[recipe_id])

    flash("⚠️ Recipe not found!", "error")
    return redirect(url_for("recipe_search"))

# ✅ Logout Route
@app.route("/logout")
def logout():
    session.clear()
    flash("✅ You have been logged out.", "info")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
