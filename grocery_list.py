from flask import render_template, request, session, redirect, url_for, flash
from .app import app

@app.route("/add_to_grocery_list", methods=["POST"])
def add_to_grocery_list():
    recipe_data = request.form
    grocery_list = session.get('grocery_list', [])
    grocery_list.append(recipe_data)
    session['grocery_list'] = grocery_list
    flash("✅ Recipe added to grocery list!", "success")
    return redirect(url_for("grocery_list"))

@app.route("/grocery_list")
def grocery_list():
    grocery_list = session.get('grocery_list', [])
    return render_template("grocery_list.html", grocery_list=grocery_list)

@app.route("/remove_from_grocery_list", methods=["POST"])
def remove_from_grocery_list():
    recipe_data = request.form
    grocery_list = session.get('grocery_list', [])
    grocery_list = [item for item in grocery_list if item['name'] != recipe_data['name']]
    session['grocery_list'] = grocery_list
    flash("✅ Recipe removed from grocery list.", "success")
    return redirect(url_for("grocery_list"))

@app.route("/download_grocery_list")
def download_grocery_list():
    grocery_list = session.get('grocery_list', [])
    # Generate CSV or JSON file to download
    # Provide functionality to download this file
    return "Grocery list download functionality"
