from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import pymysql
import requests
from datetime import datetime

app = Flask(__name__)

# 🔹 Secret Key & Session Config
app.secret_key = "secret_key"
app.config["SESSION_TYPE"] = "filesystem"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)
Session(app)

# 🔹 API Keys
YOUTUBE_API_KEY = "your_api_key"
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
