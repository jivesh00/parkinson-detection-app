from flask import Flask, render_template, request, redirect, session, send_file
import pickle
import sqlite3
import random

# Security
from werkzeug.security import generate_password_hash, check_password_hash

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)
app.secret_key = "secret123"

# Load ML model
model = pickle.load(open("model.pkl", "rb"))

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    # Users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    # Patients table
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

# ---------------- LOGIN ----------------
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

# ---------------- SIGNUP ----------------
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

# ---------------- HOME ----------------
@app.route("/home")
def home():
    if "user" in session:
        return render_template("index.html")
    return redirect("/")

# ---------------- PREDICT ----------------
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

    values_dict = {
        "BMI": values[0],
        "Sleep": values[1],
        "Cholesterol": values[2],
        "Depression": values[3],
        "Postural": values[4]
    }

    # Save patient in DB
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

    # Save report for PDF
    session["report"] = {
        "Name": request.form["name"],
        "Age": request.form["age"],
        "Sex": request.form["sex"],
        "Weight": request.form["weight"],
        "Address": request.form["address"],
        "Result": result,
        "Confidence": str(confidence) + "%"
    }

    return render_template(
        "index.html",
        prediction_text=result,
        confidence=confidence,
        name=request.form["name"],
        age=request.form["age"],
        sex=request.form["sex"],
        weight=request.form["weight"],
        address=request.form["address"],
        data=values_dict
    )

# ---------------- PDF DOWNLOAD ----------------
@app.route("/download")
def download():
    data = session.get("report")

    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph("Patient Report", styles["Title"]))
    content.append(Spacer(1, 10))

    for key, value in data.items():
        content.append(Paragraph(f"{key}: {value}", styles["Normal"]))
        content.append(Spacer(1, 10))

    doc.build(content)

    return send_file("report.pdf", as_attachment=True)

# ---------------- HISTORY ----------------
@app.route("/history")
def history():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients")
    data = cur.fetchall()
    conn.close()

    return render_template("history.html", data=data)

# ---------------- CHATBOT ----------------
@app.route("/chat", methods=["POST"])
def chat():
    msg = request.form["message"].lower()

    if "tremor" in msg:
        reply = "Tremors are common in Parkinson’s disease."
    elif "treatment" in msg:
        reply = "Consult a neurologist for treatment."
    elif "hello" in msg:
        reply = "Hello! How can I help you?"
    else:
        reply = random.choice([
            "Please consult a doctor.",
            "Provide more details.",
            "Symptoms vary between patients."
        ])

    return {"response": reply}

# ---------------- DOCTORS ----------------
@app.route("/doctor")
def doctor():
    doctors = [
        {"name": "Dr. Sharma", "type": "Neurologist", "city": "Delhi"},
        {"name": "Dr. Patel", "type": "Neurologist", "city": "Mumbai"},
        {"name": "Dr. Reddy", "type": "Neurologist", "city": "Hyderabad"}
    ]

    return render_template("doctor.html", doctors=doctors)

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)