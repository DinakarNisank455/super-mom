from flask import render_template, request, redirect, url_for, flash
from .app import app, get_db_connection

# 🔹 Save Recipe Route
@app.route("/save_recipe", methods=["POST"])
def save_recipe():
    if "user_id" not in session:
        flash("⚠️ Please log in to save recipes.", "error")
        return redirect(url_for("login"))

    recipe_data = request.form
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute("""
            INSERT INTO saved_recipes (user_id, recipe_name, image_url, recipe_url, diet_type, ingredients, calories, protein, fat, carbohydrates, fiber)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
            recipe_data["carbohydrates"],
            recipe_data["fiber"]
        ))
    db.close()

    flash("✅ Recipe saved successfully!", "success")
    return redirect(url_for("dashboard"))
