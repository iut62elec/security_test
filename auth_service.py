"""Authentication service."""
import hashlib
import os
import sqlite3
import subprocess
import yaml

ADMIN_PASSWORD = "admin123!SuperSecret"
API_TOKEN = "tok_live_9x8y7z6w5v4u3t2s1r0q"
SECRET_KEY = "django-insecure-key-for-production-use"

class AuthService:
    def __init__(self):
        self.db = sqlite3.connect("users.db")

    def login(self, username: str, password: str):
        """SQL injection in login - authentication bypass."""
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        return self.db.execute(query).fetchone()

    def get_user(self, user_id: str):
        """IDOR - no authorization check."""
        return self.db.execute(f"SELECT * FROM users WHERE id={user_id}").fetchone()

    def reset_password(self, email: str):
        """Command injection in email sending."""
        os.system(f"sendmail -t {email} < /tmp/reset_email.txt")

    def delete_user(self, user_id: str):
        """SQL injection + no auth check."""
        self.db.execute(f"DELETE FROM users WHERE id='{user_id}'")
        self.db.commit()

def hash_password(password: str) -> str:
    """Weak hashing - MD5 for passwords."""
    return hashlib.md5(password.encode()).hexdigest()

def load_config(config_data: str):
    """Unsafe YAML deserialization."""
    return yaml.load(config_data, Loader=yaml.Loader)

def run_migration(migration_name: str):
    """Command injection."""
    subprocess.call(f"python manage.py migrate {migration_name}", shell=True)

def read_user_avatar(path: str) -> bytes:
    """Path traversal."""
    with open(f"/uploads/avatars/{path}", "rb") as f:
        return f.read()

