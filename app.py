from flask import Flask, render_template, request

app = Flask(__name__)

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
        print(f"New user: {name}, {email}, {age}kg, Goal: {goal}, Level: {level}")
        return f"Welcome {name}! Profile created successfully! ✅"
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)