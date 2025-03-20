from flask import Flask, render_template, request, redirect, session, jsonify, flash, url_for
import pymysql
import bcrypt
import requests
from datetime import datetime


app = Flask(__name__)
app.secret_key = "secret"

app_id = "9339488b"
app_key = "4f804a4822c6c387579112bcda286297"

# Function to establish a fresh database connection
def get_db_connection():
    return pymysql.connect(host="localhost", user="root", password="@Bunny455", database="prr")


def generate_user_id():
    db = get_db_connection()
    cursor = db.cursor()
    today = datetime.today().strftime('%Y%m%d')  # Format: YYYYMMDD
    cursor.execute("SELECT COUNT(*) FROM users WHERE user_id LIKE %s", (today + "%",))
    count = cursor.fetchone()[0] + 1  # Increment serial number
    return f"{today}{count:03d}"  # Ensures ID format YYYYMMDD001

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=['POST', 'GET'])
def signup():

    
    if request.method == 'POST':
        name = request.form.get("name")  # Use `.get()` to avoid KeyError
        email = request.form.get("email")
        password = request.form.get("password")
        is_gym_member = "on" if "is_gym_member" in request.form else "no"
        diet_type = request.form.get("diet_type", "")
        allergies = request.form.get("allergies", "")

        print(f"DEBUG: Name={name}, Email={email}, Password={password}")  # Debugging

        if not all([name, email, password]):  # Check required fields
            flash("⚠️Please fill in all required fields!", "error")
            return redirect(url_for("signup"))
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user_id = generate_user_id()

        try:
            db = get_db_connection()
            cursor = db.cursor()

              # Generate custom user ID

            # Insert user into `users`
            cursor.execute("INSERT INTO users (user_id ,email, password) VALUES (%s,%s, %s)", (user_id,email, hashed_password))
            db.commit()

            # Get user_id of the newly inserted user
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))


            # Insert into `profiles`
            cursor.execute("INSERT INTO profiles (user_id, name, gym_membership, nutrition_plan, food_allergies) VALUES (%s, %s, %s, %s, %s)",
                           (user_id, name, is_gym_member, diet_type, allergies))
            db.commit()

            flash("Signup successful! Please log in.", "success")

        except pymysql.MySQLError as e:
            db.rollback()
            if (str(e)=="duplicate"):
                flash(f"User already exist.")
            else:
                flash(f"Database error: {str(e)}", "error")

        finally:
            cursor.close()
            db.close()

        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not email or not password:
            flash("Please enter both email and password.", "error")
            return redirect(url_for("login"))

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        db.close()
        

        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
            session["user_id"] = user[0]
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid credentials.", "error")
        return redirect(url_for("login"))

    return render_template("login.html")

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

@app.route('/recipe_search', methods=['GET', 'POST'])
def recipe_search():
    query = request.args.get('query', '')
    search_type = request.args.get('search_type', 'name')
    diet_filter = request.args.get('diet_filter', '')
    use_nutrition = request.args.get('use_nutrition', False)

    # Nutrition Filters
    calories = request.args.get('calories', '')
    protein = request.args.get('protein', '')
    fat = request.args.get('fat', '')

    if not query:
        return render_template("recipe_search.html", search_results=[])

    # Build API URL based on search type
    api_url = f"https://api.edamam.com/api/recipes/v2?q={query}&app_id={app_id}&app_key={app_key}&type=public"

    if diet_filter:
        api_url += f"&diet={diet_filter}"

    if use_nutrition:
        api_url += f"&calories=0-{calories}" if calories else ""
        api_url += f"&nutrients[PROCNT]={protein}-" if protein else ""
        api_url += f"&nutrients[FAT]=-{fat}" if fat else ""

    response = requests.get(api_url)
    data = response.json()

    # Extract recipe details
    recipes = []
    if "hits" in data:
        for hit in data["hits"]:
            recipe = hit["recipe"]
            recipes.append({
                "name": recipe["label"],
                "image": recipe["image"],
                "recipe_link": recipe["url"],
                "diet_type": ", ".join(recipe.get("dietLabels", ["N/A"])),
                "ingredients": ", ".join(recipe.get("ingredientLines", [])),
                "nutrition": {
                    "calories": int(recipe["calories"]) if "calories" in recipe else "N/A",
                    "protein": recipe["totalNutrients"].get("PROCNT", {}).get("quantity", "N/A"),
                    "fat": recipe["totalNutrients"].get("FAT", {}).get("quantity", "N/A")
                },
                "source_name": recipe["source"],
                "source_url": recipe["url"]
            })

            session["search_results"] = recipes

    return render_template('recipe_search.html', recipes=recipes)


@app.route('/recipe/<path:recipe_url>')
def recipe_detail(recipe_url):
    recipes = session.get("search_results", [])
    for recipe in recipes:
        if recipe["recipe_link"] == recipe_url:  # Match by URL instead of ID
            return render_template("recipe_detail.html", recipe=recipe)

    flash("Recipe not found!", "error")
    return redirect(url_for("recipe_search"))


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
