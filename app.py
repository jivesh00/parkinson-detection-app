from flask import Flask, render_template, request, redirect, session, send_file
import pickle
import sqlite3
import random
import os

from werkzeug.security import generate_password_hash, check_password_hash
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)
app.secret_key = "secret123"

model = pickle.load(open("model.pkl", "rb"))

def init_db():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS patients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age TEXT,
        sex TEXT,
        weight TEXT,
        address TEXT,
        result TEXT,
        confidence TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session["user"] = username
            return redirect("/home")
        else:
            return "Invalid Login"

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO users(username, password) VALUES(?,?)", (username, password))
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("signup.html")

@app.route("/home")
def home():
    if "user" in session:
        return render_template("index.html")
    return redirect("/")

@app.route("/predict", methods=["POST"])
def predict():
    values = [
        float(request.form["bmi"]),
        float(request.form["sleep"]),
        float(request.form["chol"]),
        float(request.form["dep"]),
        float(request.form["post"])
    ]

    prediction = model.predict([values])
    prob = model.predict_proba([values])
    confidence = round(max(prob[0]) * 100, 2)

    result = "Parkinson Detected" if prediction[0] == 1 else "Healthy"

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO patients(name, age, sex, weight, address, result, confidence)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        request.form["name"],
        request.form["age"],
        request.form["sex"],
        request.form["weight"],
        request.form["address"],
        result,
        str(confidence) + "%"
    ))
    conn.commit()
    conn.close()

    session["report"] = {
        "Name": request.form["name"],
        "Result": result,
        "Confidence": str(confidence) + "%"
    }

    return render_template("index.html", prediction_text=result)

@app.route("/download")
def download():
    data = session.get("report")

    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()
    content = []

    for key, value in data.items():
        content.append(Paragraph(f"{key}: {value}", styles["Normal"]))
        content.append(Spacer(1, 10))

    doc.build(content)

    return send_file("report.pdf", as_attachment=True)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)