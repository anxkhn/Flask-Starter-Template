from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from functools import wraps
from cs50 import SQL
import os


# Configure application
app = Flask(__name__)
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# Database setup
if not os.path.exists("sqlite.db"):
    open("sqlite.db", "w").close()

db = SQL("sqlite:///sqlite.db")
db.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        hash TEXT NOT NULL
    )
"""
)
db.execute(
    """
    INSERT OR IGNORE INTO users (hash, username)
    VALUES (
        'pbkdf2:sha256:260000$FP5Hh1wII3nVzFfg$061583004b53c954faeb90c0dc85c9a66b4315a86bb0826f31b0dac6436e8f22',
        'admin'
    )
"""
)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username").lower().strip()
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username or not password or not confirmation:
            flash("Please enter all required fields!", "red")
            return redirect("/register")
        if password != confirmation:
            flash("Passwords do not match.", "red")
            return redirect("/register")
        if not is_valid_password(password):
            flash("Password does not meet all criteria.", "red")
            return redirect("/register")
        hashed_password = generate_password_hash(password)
        try:
            db.execute(
                "INSERT INTO users(username, hash) VALUES (?, ?)",
                username,
                hashed_password,
            )
        except:
            flash("Username is already taken.", "yellow")
            return redirect("/register")
        else:
            # Remember which user has logged in
            rows = db.execute("SELECT * FROM users WHERE username = ?", username)
            session["user_id"] = rows[0]["id"]
            flash("Registration successful.", "green")
            return redirect("/")
    else:
        return render_template("register.html")


def is_valid_password(password):
    # Password must be at least 8 characters long
    if len(password) < 8:
        return False
    # Check for at least one lowercase letter
    if not any(char.islower() for char in password):
        return False
    # Check for at least one uppercase letter
    if not any(char.isupper() for char in password):
        return False
    # Check for at least one digit
    if not any(char.isdigit() for char in password):
        return False
    # Check for at least one special character
    special_characters = "~`!@#$%^&*()_-+={[}]|\:;<,>.?/"
    if not any(char in special_characters for char in password):
        return False
    return True


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            flash("Please enter both username and password.", "red")
            return redirect("/login")
        username = username.lower().strip()
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash("Invalid username and/or password.", "red")
            return redirect("/login")
        session["user_id"] = rows[0]["id"]
        flash("Login successful. Welcome!", "green")
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
