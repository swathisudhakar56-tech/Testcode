from flask import Flask, request, jsonify, render_template_string
import sqlite3
import jwt
import os

app = Flask(__name__)
SECRET_KEY = "hardcoded_secret"  # [A2: Cryptographic Failures]

# Insecure DB connection (no auth, no encryption)
def get_db():
    conn = sqlite3.connect("users.db")
    return conn

# [A1: Broken Access Control]
@app.route("/admin")
def admin_panel():
    # No authentication check!
    return "Welcome to the Admin Panel! Anyone can access this."

# [A3: Injection]
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    conn = get_db()
    cursor = conn.cursor()
    # SQL Injection possible
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    user = cursor.fetchone()

    if user:
        token = jwt.encode({"user": username}, SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token})
    else:
        return "Invalid credentials"

# [A5: Security Misconfiguration] – Debug mode ON
@app.route("/debug")
def debug():
    return eval(request.args.get("code"))  # Remote Code Execution (RCE)

# [A7: Identification and Authentication Failures]
@app.route("/reset_password", methods=["POST"])
def reset_password():
    # No rate limiting, no OTP validation
    email = request.form.get("email")
    new_pass = request.form.get("new_password")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE users SET password='{new_pass}' WHERE email='{email}'")
    conn.commit()
    return "Password reset successful!"

# [A6: Vulnerable and Outdated Components]
@app.route("/render")
def render():
    template = request.args.get("template")
    # SSTI - Server-Side Template Injection
    return render_template_string(template)

if __name__ == "__main__":
    # Debug ON (bad practice)
    app.run(host="0.0.0.0", port=5000, debug=True)
