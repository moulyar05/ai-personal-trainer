from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
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
        age = request.form["age"]
        weight = request.form["weight"]
        goal = request.form["goal"]
        level = request.form["level"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, age, weight, goal, level) VALUES (?, ?, ?, ?, ?, ?)",
                       (name, email, age, weight, goal, level))
        conn.commit()
        conn.close()

        return f"Welcome {name}! Profile saved successfully! ✅"
    return render_template("register.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)


