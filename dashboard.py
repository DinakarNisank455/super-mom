from flask import render_template, redirect, url_for, flash
from .app import app, get_db_connection

# 🔹 Dashboard Route
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
