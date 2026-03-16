"""Authentication module with intentional security vulnerabilities."""
import hashlib
import os
import sqlite3
import subprocess


# VULNERABILITY: Hardcoded credentials
API_KEY = "sk-proj-1234567890abcdef"
DB_PASSWORD = "SuperSecret123!"
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"


def authenticate_user(username, password):
    """VULNERABILITY: SQL Injection - user input concatenated into query."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    return user


def get_user_profile(user_id):
    """VULNERABILITY: SQL Injection via string formatting."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profiles WHERE user_id = %s" % user_id)
    return cursor.fetchone()


def hash_password(password):
    """VULNERABILITY: Using MD5 for password hashing (weak/broken)."""
    return hashlib.md5(password.encode()).hexdigest()


def run_health_check(host):
    """VULNERABILITY: Command injection via shell=True."""
    result = subprocess.run(
        f"ping -c 1 {host}",
        shell=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def render_welcome(username):
    """VULNERABILITY: Cross-site scripting (XSS) - no output encoding."""
    return f"<html><body><h1>Welcome back, {username}!</h1></body></html>"


def read_user_avatar(filename):
    """VULNERABILITY: Path traversal - no sanitization of filename."""
    avatar_path = f"/uploads/avatars/{filename}"
    with open(avatar_path, "rb") as f:
        return f.read()


def reset_password(email):
    """VULNERABILITY: Insecure token generation using predictable seed."""
    import random
    random.seed(email)
    token = random.randint(100000, 999999)
    return token
