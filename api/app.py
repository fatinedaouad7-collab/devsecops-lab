from flask import Flask, request
import sqlite3
import subprocess
import hashlib
import os
import bcrypt

app = Flask(__name__)

SECRET_KEY = os.getenv("SECRET_KEY", "secure-key")


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # SECURE QUERY (no SQL injection)
    query = "SELECT * FROM users WHERE username=? AND password=?"
    cursor.execute(query, (username, password))

    result = cursor.fetchone()

    if result:
        return {"status": "success", "user": username}

    return {"status": "error", "message": "Invalid credentials"}


@app.route("/ping", methods=["POST"])
def ping():
    host = request.json.get("host", "")

    # SECURE (no shell=True)
    try:
        output = subprocess.check_output(["ping", "-c", "1", host])
        return {"output": output.decode()}
    except:
        return {"error": "Invalid host"}


@app.route("/compute", methods=["POST"])
def compute():
    return {"message": "Function disabled for security reasons"}


@app.route("/hash", methods=["POST"])
def hash_password():
    pwd = request.json.get("password", "admin")

    hashed = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())

    return {"bcrypt": hashed.decode()}


@app.route("/readfile", methods=["POST"])
def readfile():
    return {"message": "Access denied for security reasons"}


@app.route("/debug", methods=["GET"])
def debug():
    return {"message": "Debug disabled"}


@app.route("/hello", methods=["GET"])
def hello():
    return {"message": "Secure API running"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)