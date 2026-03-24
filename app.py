from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "your_secret_key_123"
bcrypt = Bcrypt(app)

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            password TEXT,
            age INTEGER,
            weight REAL,
            goal TEXT,
            level TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")
        age = request.form["age"]
        weight = request.form["weight"]
        goal = request.form["goal"]
        level = request.form["level"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, password, age, weight, goal, level) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (name, email, password, age, weight, goal, level))
        conn.commit()
        conn.close()

        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user[3], password):
            session["user_id"] = user[0]
            session["user_name"] = user[1]
            return redirect(url_for("dashboard"))
        else:
            return "Invalid email or password ❌"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return f"Welcome {session['user_name']}! 🎉 Your dashboard is coming soon!"

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)