from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify
import pymysql
from datetime import datetime, timedelta
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
import requests

app = Flask(__name__)

# 🔹 Secret Key & Session Config
app.secret_key = "secret_key"
app.config["SESSION_TYPE"] = "filesystem"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)
Session(app)

# 🔹 API Keys
YOUTUBE_API_KEY = "AIzaSyDdVp_XXt2HP5cGsASHDBxeEmHeCiBsZhc"
app_id = "9339488b"
app_key = "4f804a4822c6c387579112bcda286297"

# ✅ Database Connection
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="@Bunny455",
        database="prr",
        autocommit=True
    )

# ✅ Unique User ID
def generate_user_id():
    db = get_db_connection()
    with db.cursor() as cursor:
        today = datetime.today().strftime('%Y%m%d')
        cursor.execute("SELECT COUNT(*) FROM users WHERE user_id LIKE %s", (today + "%",))
        count = cursor.fetchone()[0] + 1
    db.close()
    return f"{today}{count:03d}"

# 🔹 Home
@app.route("/")
def home():
    return render_template("index.html")

# 🔹 Signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("Confirm_password")

        if not all([name, email, password, confirm_password]):
            flash("⚠️ Please fill in all required fields!", "error")
            return redirect(url_for("signup"))

        if confirm_password != password:
            flash("⚠️ Passwords do not match!", "error")
            return redirect(url_for("signup"))

        hashed_password = generate_password_hash(password)
        user_id = generate_user_id()

        db = get_db_connection()
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                flash("⚠️ User already exists!", "error")
                return redirect(url_for("signup"))

            cursor.execute(
                "INSERT INTO users (user_id, email, password) VALUES (%s, %s, %s)",
                (user_id, email, hashed_password)
            )
        db.close()

        flash("✅ Signup successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")

# 🔹 Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not email or not password:
            flash("⚠️ Please enter both email and password.", "error")
            return redirect(url_for("login"))

        db = get_db_connection()
        with db.cursor() as cursor:
            cursor.execute("SELECT user_id, password FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
        db.close()

        if user and check_password_hash(user[1], password):
            session["user_id"] = user[0]
            flash("✅ Login successful!", "success")
            return redirect(url_for("dashboard"))

        flash("⚠️ Invalid credentials.", "error")
        return redirect(url_for("login"))

    return render_template("login.html")

# 🔹 Forgot Password
@app.route('/forgot_password', methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        new_password = request.form["new_password"]
        hashed_password = generate_password_hash(new_password)

        db = get_db_connection()
        with db.cursor() as cursor:
            cursor.execute("UPDATE users SET password = %s WHERE email = %s", (hashed_password, email))
        db.close()

        flash('✅ Password reset successful. Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('forgot_password.html')

# 🔹 Dashboard
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("home"))

    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (session["user_id"],))
        user = cursor.fetchone()
    db.close()

    return render_template("dashboard.html", user=user)

# 🔹 Recipe Search
@app.route("/select_search", methods=["POST"])
def select_search():
    selected_type = request.form.get("search_type")

    if selected_type == "nutrition":
        return redirect(url_for('nutrition_search'))
    elif selected_type == "ingredient":
        return redirect(url_for('ingredient_search'))
    else:
        flash("⚠️ Invalid selection. Please try again.", "error")
        return redirect(url_for('nutrition_search'))
    
# ✅ Recipe Search by Ingredients
@app.route("/ingredient_search", methods=["GET", "POST"])
def ingredient_search():
    search_performed = False

    if request.method == "POST":
        search_performed = True

        ingredients = request.form.get('ingredients', '').strip()
        
        if not ingredients:
            flash("⚠️ Please enter some ingredients!", "error")
            return render_template("ingredient_search.html", recipes=[])

        ingredients_query = ",".join(ingredient.strip() for ingredient in ingredients.split(","))
        api_url = f"https://api.edamam.com/api/recipes/v2?app_id={app_id}&app_key={app_key}&type=public&ingr={ingredients_query}"

        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Ensure we raise an exception for bad responses
            data = response.json()
            
            # Debugging output
            print("API Response:", data)  # Check the raw API response

            # Check if 'hits' is in the response
            if "hits" in data:
                recipes = []
                for hit in data["hits"]:
                    recipe = hit["recipe"]
                    recipes.append({
                        "name": recipe["label"],
                        "image": recipe["image"],
                        "recipe_link": recipe["url"],
                        "diet_type": ", ".join(recipe.get("dietLabels", ["N/A"])),
                        "ingredients": recipe.get("ingredientLines", []),
                        "nutrition": {
                            "calories": int(recipe.get("calories", 0)),
                            "protein": float(recipe["totalNutrients"].get("PROCNT", {}).get("quantity", 0) or 0),
                            "fat": float(recipe["totalNutrients"].get("FAT", {}).get("quantity", 0) or 0),
                            "carbohydrates": float(recipe["totalNutrients"].get("CHOCDF", {}).get("quantity", 0) or 0),
                            "fibers": float(recipe["totalNutrients"].get("FIBTG", {}).get("quantity", 0) or 0)
                        }
                    })
                session["ingredient_search_results"] = recipes
                return render_template("ingredient_search.html", recipes=recipes, search_performed=search_performed)
            else:
                flash("⚠️ No recipes found with those ingredients.", "error")
                return render_template("ingredient_search.html", recipes=[])

        except requests.exceptions.RequestException as e:
            flash(f"⚠️ Error fetching recipes: {e}", "error")
            return render_template("ingredient_search.html", recipes=[])

    return render_template("ingredient_search.html", recipes=[])


@app.route("/nutrition_search", methods=["GET", "POST"])
def nutrition_search():
    if request.method == "POST":
        def get_value(form_field, default):
            value = request.form.get(form_field)
            return float(value) if value else default

        # Get nutrition input safely
        min_calories = get_value("min_calories", 0)
        max_calories = get_value("max_calories", float('inf'))
        min_protein = get_value("min_protein", 0)
        max_protein = get_value("max_protein", float('inf'))
        min_fat = get_value("min_fat", 0)
        max_fat = get_value("max_fat", float('inf'))
        min_carbs = get_value("min_carbs", 0)
        max_carbs = get_value("max_carbs", float('inf'))
        min_fibers = get_value("min_fibers", 0)
        max_fibers = get_value("max_fibers", float('inf'))

        query = request.form.get("query", "").strip()

        # If user didn't give any keyword ➔ search everything
        if not query:
            query = "*"  # Wildcard search

        api_url = f"https://api.edamam.com/api/recipes/v2?q={query}&app_id={app_id}&app_key={app_key}&type=public"

        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            flash(f"⚠️ Error fetching recipes: {e}", "error")
            return render_template("nutrition_search.html", recipes=[])

        recipes = []
        if "hits" in data:
            for hit in data["hits"]:
                recipe = hit["recipe"]
                nutrition = {
                    "calories": recipe.get("calories", 0),
                    "protein": recipe["totalNutrients"].get("PROCNT", {}).get("quantity", 0),
                    "fat": recipe["totalNutrients"].get("FAT", {}).get("quantity", 0),
                    "carbohydrates": recipe["totalNutrients"].get("CHOCDF", {}).get("quantity", 0),
                    "fibers": recipe["totalNutrients"].get("FIBTG", {}).get("quantity", 0)
                }

                # Check nutrition filter
                if (
                    min_calories <= nutrition["calories"] <= max_calories and
                    min_protein <= nutrition["protein"] <= max_protein and
                    min_fat <= nutrition["fat"] <= max_fat and
                    min_carbs <= nutrition["carbohydrates"] <= max_carbs and
                    min_fibers <= nutrition["fibers"] <= max_fibers
                ):
                    recipes.append({
                        "name": recipe["label"],
                        "image": recipe["image"],
                        "recipe_link": recipe["url"],
                        "diet_type": ", ".join(recipe.get("dietLabels", ["N/A"])),
                        "ingredients": recipe.get("ingredientLines", []),
                        "nutrition": nutrition
                    })

            print("Number of recipes found:", len(recipes))

        return render_template("nutrition_search.html", recipes=recipes)

    return render_template("nutrition_search.html", recipes=[])


# 🔹 Save Recipe
@app.route("/save_recipe", methods=["POST"])
def save_recipe():
    if "user_id" not in session:
        flash("⚠️ Please log in to save recipes.", "error")
        return redirect(url_for("login"))

    recipe_data = request.form
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute("""
            INSERT INTO saved_recipes (user_id, recipe_name, image_url, recipe_url, diet_type, ingredients, calories, protein, fat,carbohydrates,fiber)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)
        """, (
            session["user_id"],
            recipe_data["name"],
            recipe_data["image"],
            recipe_data["url"],
            recipe_data["diet_type"],
            recipe_data["ingredients"],
            recipe_data["calories"],
            recipe_data["protein"],
            recipe_data["fat"],
            recipe_data["calories"],
            recipe_data["fiber"]
        ))
    db.close()

    flash("✅ Recipe saved successfully!", "success")
    return redirect(url_for("dashboard"))

# 🔹 YouTube Video Fetch
def get_youtube_video(recipe_name):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": f"{recipe_name} recipe",
        "key": YOUTUBE_API_KEY,
        "type": "video",
        "maxResults": 1
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data["items"]:
            video_id = data["items"][0]["id"]["videoId"]
            return f"https://www.youtube.com/embed/{video_id}"
    except requests.exceptions.RequestException:
        pass
    return None

@app.route("/recipe_search", methods=['GET'])
def recipe_search():
    return render_template('recipe_search.html')

# 🔹 Recipe Detail View
@app.route("/recipe/<int:recipe_id>")
def recipe_detail(recipe_id):
    recipes = session.get("search_results", [])
    if 0 <= recipe_id < len(recipes):
        selected_recipe = recipes[recipe_id]
        youtube_video = get_youtube_video(selected_recipe["name"])
        return render_template("recipe_detail.html", recipe=selected_recipe, youtube_video=youtube_video)

    flash("⚠️ Recipe not found.", "error")
    return redirect(url_for("recipe_search"))

# 🔹 Saved Recipes View
@app.route("/saved_recipes")
def saved_recipes():
    if "user_id" not in session:
        flash("⚠️ Please log in to view saved recipes.", "error")
        return redirect(url_for("login"))

    db = get_db_connection()
    with db.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM saved_recipes WHERE user_id = %s", (session["user_id"],))
        recipes = cursor.fetchall()
    db.close()

    return render_template("saved_recipes.html", recipes=recipes)

@app.route('/generate_grocery_list', methods=['POST'])
def generate_grocery_list():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    selected_recipe_ids = request.form.getlist('selected_recipes')
    if not selected_recipe_ids:
        flash("⚠️ No recipes selected.", "error")
        return redirect(url_for("saved_recipes"))

    db = get_db_connection()
    with db.cursor() as cursor:
        format_strings = ','.join(['%s'] * len(selected_recipe_ids))
        cursor.execute(f"SELECT ingredients FROM saved_recipes WHERE user_id=%s AND id IN ({format_strings})", (session['user_id'], *selected_recipe_ids))
        recipes = cursor.fetchall()
    db.close()

    grocery_list = set()
    for recipe in recipes:
        ingredients = recipe.get('ingredients', '').split(',')
        for ingredient in ingredients:
            grocery_list.add(ingredient.strip())

    return render_template('grocery_list.html', grocery_list=grocery_list)

@app.route('/download_grocery_list', methods=['POST'])
def download_grocery_list():
    grocery_list = request.form.get('grocery_list')
    if not grocery_list:
        flash("⚠️ No grocery list to download.", "error")
        return redirect(url_for("saved_recipes"))

    grocery_list = json.loads(grocery_list)
    grocery_list_str = "\n".join(grocery_list)

    response = Response(grocery_list_str, content_type='text/plain')
    response.headers['Content-Disposition'] = 'attachment; filename=grocery_list.txt'
    return response


# 🔹 Nutrition API
# 🔹 Nutrition API
@app.route('/api/nutrition')
def api_nutrition():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    period = request.args.get('period', 'daily')  # small correction here too!

    db = get_db_connection()
    with db.cursor(pymysql.cursors.DictCursor) as cursor:
        if period == 'monthly':
            cursor.execute(""" 
                SELECT 
                    SUM(CAST(calories AS DECIMAL)) AS calories, 
                    SUM(CAST(protein AS DECIMAL)) AS protein, 
                    SUM(CAST(fat AS DECIMAL)) AS fat, 
                    SUM(CAST(carbohydrates AS DECIMAL)) AS carbohydrates,
                    SUM(CAST(fiber AS DECIMAL)) AS fiber
                FROM saved_recipes 
                WHERE user_id = %s AND saved_at >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
            """, (session['user_id'],))
        else:
            cursor.execute(""" 
                SELECT 
                    SUM(CAST(calories AS DECIMAL)) AS calories, 
                    SUM(CAST(protein AS DECIMAL)) AS protein, 
                    SUM(CAST(fat AS DECIMAL)) AS fat, 
                    SUM(CAST(carbohydrates AS DECIMAL)) AS carbohydrates,
                    SUM(CAST(fiber AS DECIMAL)) AS fiber
                FROM saved_recipes 
                WHERE user_id = %s AND DATE(saved_at) = CURDATE()
            """, (session['user_id'],))

        result = cursor.fetchone()
    db.close()

    # Safely handle if any value is None
    calories = float(result.get("calories") or 0)
    protein = float(result.get("protein") or 0)
    fat = float(result.get("fat") or 0)
    carbohydrates = float(result.get("carbohydrates") or 0)
    fiber = float(result.get("fiber") or 0)

    return jsonify({
        "calories": calories,
        "protein": protein,
        "fat": fat,
        "carbohydrates": carbohydrates,
        "fiber": fiber
    })

# 🔹 Meal History API
@app.route("/api/meal-history")
def meal_history():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    period = request.args.get('period', 'daily')
    db = get_db_connection()

    with db.cursor(pymysql.cursors.DictCursor) as cursor:
        if period == 'monthly':
            cursor.execute("""
                SELECT recipe_name, calories, saved_at
                FROM saved_recipes
                WHERE user_id = %s AND saved_at >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
                ORDER BY saved_at DESC
            """, (session["user_id"],))
        else:
            cursor.execute("""
                SELECT recipe_name, calories, saved_at
                FROM saved_recipes
                WHERE user_id = %s AND DATE(saved_at) = CURDATE()
                ORDER BY saved_at DESC
            """, (session["user_id"],))

        recipes = cursor.fetchall()

    db.close()
    return jsonify({"recipes": recipes})

# 🔹 Logout
@app.route("/logout")
def logout():
    session.clear()
    flash("✅ You have been logged out.", "success")
    return redirect(url_for("login"))

# Start Server
if __name__ == "__main__":
    app.run(debug=True)
