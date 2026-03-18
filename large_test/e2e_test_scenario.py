import os
import sqlite3
import pickle
import hashlib

# VULNERABILITY 1: Insecure deserialization
def load_user_data(serialized_data):
    """Load user data from untrusted source."""
    return pickle.loads(serialized_data)

# VULNERABILITY 2: Weak hashing for passwords
def hash_password(password):
    """Hash password using MD5 (insecure)."""
    return hashlib.md5(password.encode()).hexdigest()

# VULNERABILITY 3: Hardcoded credentials
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
DB_CONNECTION = "postgresql://admin:SuperSecret123@prod-db.internal:5432/users"

# VULNERABILITY 4: SSRF via user-controlled URL
def fetch_url(user_url):
    """Fetch content from user-provided URL."""
    import urllib.request
    return urllib.request.urlopen(user_url).read()

# Clean function (no issues)
def calculate_total(items):
    """Calculate total price of items."""
    return sum(item["price"] * item["quantity"] for item in items)
