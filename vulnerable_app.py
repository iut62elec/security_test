import os
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Hardcoded database credentials
DB_HOST = "prod-db.internal.company.com"
DB_USER = "admin"
DB_PASSWORD = "SuperSecret123!"
API_KEY = "sk-live-4f3c2b1a0d9e8f7g6h5i4j3k2l1m0n"

# Hardcoded JWT secret
JWT_SECRET = "my-super-secret-jwt-key-do-not-share"


def get_db():
    return sqlite3.connect("app.db")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # SQL Injection vulnerability - user input directly in query
    db = get_db()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    result = db.execute(query).fetchone()

    if result:
        return jsonify({"status": "authenticated", "user": username})
    return jsonify({"status": "failed"}), 401


@app.route("/search")
def search():
    term = request.args.get("q", "")

    # XSS vulnerability - unsanitized user input in response
    return f"<html><body><h1>Search results for: {term}</h1></body></html>"


@app.route("/exec", methods=["POST"])
def run_command():
    # Command injection vulnerability
    cmd = request.json.get("command")
    result = os.popen(cmd).read()
    return jsonify({"output": result})


@app.route("/file")
def read_file():
    # Path traversal vulnerability
    filename = request.args.get("name")
    with open(f"/app/uploads/{filename}", "r") as f:
        return f.read()


@app.route("/redirect")
def redirect_user():
    # Open redirect vulnerability
    url = request.args.get("url")
    return f'<meta http-equiv="refresh" content="0;url={url}">'


if __name__ == "__main__":
    # Debug mode enabled in production
    app.run(host="0.0.0.0", port=80, debug=True)
# trigger rescan
# rescan trigger 2
# rescan trigger 3
# rescan trigger 4
