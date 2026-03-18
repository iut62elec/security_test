import sqlite3
import os
import subprocess


def get_user(username: str) -> dict:
    """Fetch user from database - vulnerable to SQL injection."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return {"user": result}


def run_command(user_input: str) -> str:
    """Execute a system command - vulnerable to command injection."""
    output = subprocess.check_output(f"echo {user_input}", shell=True)
    return output.decode()


def read_file(filename: str) -> str:
    """Read a file - vulnerable to path traversal."""
    base_path = "/var/data/"
    with open(base_path + filename) as f:
        return f.read()


SECRET_API_KEY = "sk-live-abc123def456ghi789jkl012mno345"
DB_PASSWORD = "SuperSecret!Passw0rd"
