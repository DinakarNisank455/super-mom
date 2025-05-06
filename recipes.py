from flask import render_template, request, session, redirect, url_for, flash
from .app import app, get_db_connection
import requests

# 🔹 Recipe Search Route
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

# 🔹 Recipe Search by Ingredients
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
            response.raise_for_status()
            data = response.json()

            if "hits" in data:
                recipes = []
                for idx, hit in enumerate(data["hits"]):
                    recipe = hit["recipe"]
                    try:
                        recipes.append({
                            "idx": idx,
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
                    except (ValueError, TypeError, KeyError) as e:
                        print(f"Error processing recipe {idx}: {e}")
                        continue

                if not recipes:
                    flash("⚠️ No valid recipes found with those ingredients.", "error")
                    return render_template("ingredient_search.html", recipes=[])

                session["ingredient_search_results"] = recipes
                return render_template("ingredient_search.html", recipes=recipes, search_performed=search_performed)
            else:
                flash("⚠️ No recipes found with those ingredients.", "error")
                return render_template("ingredient_search.html", recipes=[])

        except requests.exceptions.RequestException as e:
            flash(f"⚠️ Error connecting to recipe service: {str(e)}", "error")
            return render_template("ingredient_search.html", recipes=[])
        except Exception as e:
            flash(f"⚠️ An unexpected error occurred: {str(e)}", "error")
            return render_template("ingredient_search.html", recipes=[])

    return render_template("ingredient_search.html", recipes=[])
