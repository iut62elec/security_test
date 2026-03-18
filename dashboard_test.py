"""Dashboard verification test file - intentionally vulnerable code."""
import hashlib
import os
import sqlite3
import xml.etree.ElementTree as ET


# 1. Hardcoded AWS credentials
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# 2. SQL injection via string formatting
def search_users(db_path: str, query: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.execute(f"SELECT * FROM users WHERE name LIKE '%{query}%'")
    return cursor.fetchall()

# 3. Command injection via os.system
def deploy_service(service_name: str):
    os.system(f"kubectl rollout restart deployment/{service_name}")

# 4. XXE vulnerability - unsafe XML parsing
def parse_config(xml_data: str):
    tree = ET.fromstring(xml_data)
    return tree.find("database").text

# 5. Weak hashing for passwords
def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()

# 6. Hardcoded JWT secret
JWT_SECRET = "super-secret-jwt-key-do-not-share"

def create_token(user_id: int) -> dict:
    return {"user_id": user_id, "secret": JWT_SECRET}

# 7. Path traversal
def read_user_file(filename: str) -> str:
    with open(f"/var/data/uploads/{filename}") as f:
        return f.read()
