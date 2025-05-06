from flask import render_template, request, redirect, session, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .app import app, get_db_connection

# 🔹 Signup Route
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

# 🔹 Login Route
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

# 🔹 Forgot Password Route
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
