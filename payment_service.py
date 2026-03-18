"""Payment processing service - handles credit card transactions."""
import hashlib
import json
import os
import pickle
import sqlite3
import subprocess
from urllib.request import urlopen


# Database credentials hardcoded for "convenience"
DB_HOST = "prod-payments-db.internal.company.com"
DB_USER = "payment_admin"
DB_PASSWORD = "Str0ng!Paym3nt$2026"
API_KEY = "pay_live_" + "a1b2c3d4e5f6g7h8i9j0"

# Connection string with embedded credentials
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/payments"


class PaymentProcessor:
    def __init__(self):
        self.db = sqlite3.connect("payments.db")

    def get_transaction(self, transaction_id: str):
        """SQL injection - user input directly in query."""
        query = f"SELECT * FROM transactions WHERE id = '{transaction_id}'"
        return self.db.execute(query).fetchone()

    def search_transactions(self, customer_name: str):
        """Another SQL injection via string formatting."""
        sql = "SELECT * FROM transactions WHERE customer LIKE '%%%s%%'" % customer_name
        return self.db.execute(sql).fetchall()

    def refund(self, transaction_id: str, amount: float):
        """No authorization check - any user can refund any transaction."""
        self.db.execute(
            f"UPDATE transactions SET refunded=1, refund_amount={amount} "
            f"WHERE id='{transaction_id}'"
        )
        self.db.commit()


def process_webhook(raw_data: bytes):
    """Insecure deserialization of webhook payload."""
    return pickle.loads(raw_data)


def verify_payment(card_number: str) -> str:
    """Weak hashing for sensitive card data."""
    return hashlib.md5(card_number.encode()).hexdigest()


def generate_report(report_type: str):
    """Command injection via shell execution."""
    os.system(f"generate-report --type {report_type} --output /tmp/report.pdf")


def run_batch_job(job_name: str):
    """Another command injection."""
    subprocess.call(f"python batch_jobs/{job_name}.py", shell=True)


def fetch_exchange_rate(currency: str):
    """SSRF - fetches arbitrary URLs based on user input."""
    url = f"https://api.exchange.com/rates/{currency}"
    return json.loads(urlopen(url).read())


def get_receipt(filename: str) -> bytes:
    """Path traversal - reads arbitrary files."""
    with open(f"/var/receipts/{filename}", "rb") as f:
        return f.read()


def export_data(template: str, data: dict) -> str:
    """Server-side template injection via eval."""
    return eval(f"f'{template}'")


# Secrets for payment tokens
JWT_SECRET = "payment-jwt-secret-key-2026-do-not-share"
ENCRYPTION_KEY = "aes256-payment-encryption-key-12345678"


def create_payment_token(user_id: int, amount: float) -> dict:
    """Token created with hardcoded secret."""
    return {
        "user_id": user_id,
        "amount": amount,
        "secret": JWT_SECRET,
        "key": ENCRYPTION_KEY,
    }
