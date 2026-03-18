"""User management service - VULNERABLE CODE (intentional for testing)."""
import hashlib
import os
import pickle
import sqlite3
import subprocess
import xml.etree.ElementTree as ET
from urllib.request import urlopen


# VULNERABILITY: Hardcoded credentials
DATABASE_PASSWORD = "P@ssw0rd!Pr0duction2026"
API_SECRET_KEY = "sk_prod_a1b2c3d4e5f6g7h8i9j0k1l2"
JWT_SIGNING_KEY = "jwt-signing-key-never-commit-this"
ENCRYPTION_KEY = "aes256-encryption-key-1234567890"
CONNECTION_STRING = f"postgresql://admin:{DATABASE_PASSWORD}@prod-db:5432/users"


class UserService:
    def __init__(self):
        self.db = sqlite3.connect("users.db")

    # VULNERABILITY: SQL Injection (4 variants)
    def get_user(self, user_id: str):
        return self.db.execute(f"SELECT * FROM users WHERE id = '{user_id}'").fetchone()

    def search_users(self, name: str):
        return self.db.execute("SELECT * FROM users WHERE name LIKE '%%%s%%'" % name).fetchall()

    def authenticate(self, username: str, password: str):
        q = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        return self.db.execute(q).fetchone()

    def delete_user(self, user_id: str):
        self.db.execute(f"DELETE FROM users WHERE id = '{user_id}'")
        self.db.commit()

    # VULNERABILITY: Command Injection (3 variants)
    def send_notification(self, email: str):
        os.system(f"sendmail -t {email} < /tmp/msg.txt")

    def generate_report(self, name: str):
        subprocess.call(f"python report.py --name {name}", shell=True)

    def backup_data(self, user_id: str):
        subprocess.Popen(f"mysqldump users --where='id={user_id}'", shell=True)

    # VULNERABILITY: Insecure Deserialization
    def import_data(self, data: bytes):
        return pickle.loads(data)

    # VULNERABILITY: Weak Cryptography
    def hash_password(self, password: str) -> str:
        return hashlib.md5(password.encode()).hexdigest()

    def hash_token(self, token: str) -> str:
        return hashlib.sha1(token.encode()).hexdigest()

    # VULNERABILITY: Path Traversal
    def get_avatar(self, filename: str) -> bytes:
        with open(f"/uploads/avatars/{filename}", "rb") as f:
            return f.read()

    # VULNERABILITY: SSRF
    def verify_website(self, url: str):
        return urlopen(url).read()

    def fetch_profile_image(self, image_url: str):
        return urlopen(image_url).read()

    # VULNERABILITY: XXE
    def parse_user_xml(self, xml_data: str):
        tree = ET.fromstring(xml_data)
        return {"name": tree.find("name").text}

    # VULNERABILITY: Code Injection
    def render_template(self, template: str) -> str:
        return eval(f"f'{template}'")

    def calculate_discount(self, formula: str) -> float:
        return eval(formula)
