"""User management service - CLEAN CODE (secure implementation).

A security scanner should NOT flag any issues in this file.
"""
import hashlib
import hmac
import os
import secrets
from pathlib import Path
from typing import Optional

import bcrypt

# Secrets from environment variables
DATABASE_URL = os.environ.get("DATABASE_URL", "")
SECRET_KEY = os.environ.get("SECRET_KEY", "")


class SecureUserService:
    def __init__(self, db_connection):
        self.db = db_connection

    def get_user(self, user_id: int) -> Optional[dict]:
        """Parameterized query prevents SQL injection."""
        cursor = self.db.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def search_users(self, name: str) -> list[dict]:
        cursor = self.db.execute("SELECT id, name, email FROM users WHERE name LIKE ?", (f"%{name}%",))
        return [dict(row) for row in cursor.fetchall()]

    def authenticate(self, username: str, password: str) -> Optional[dict]:
        cursor = self.db.execute("SELECT id, username, password_hash FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if not user:
            return None
        if bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
            return {"id": user["id"], "username": user["username"]}
        return None

    def create_user(self, username: str, password: str, email: str) -> int:
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        cursor = self.db.execute(
            "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
            (username, password_hash, email),
        )
        self.db.commit()
        return cursor.lastrowid

    def delete_user(self, requester_id: int, target_id: int) -> bool:
        requester = self.get_user(requester_id)
        if not requester or not requester.get("is_admin"):
            raise PermissionError("Only admins can delete users")
        self.db.execute("DELETE FROM users WHERE id = ?", (target_id,))
        self.db.commit()
        return True


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def generate_token() -> str:
    return secrets.token_urlsafe(32)


def get_avatar(user_id: int, uploads_dir: str = "/uploads/avatars") -> Optional[bytes]:
    base = Path(uploads_dir).resolve()
    avatar_path = (base / f"{user_id}.png").resolve()
    if not str(avatar_path).startswith(str(base)):
        raise ValueError("Invalid path")
    return avatar_path.read_bytes() if avatar_path.exists() else None


def verify_signature(payload: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def add(a: int, b: int) -> int:
    return a + b
