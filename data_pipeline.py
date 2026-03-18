"""Data processing pipeline."""
import hashlib
import json
import os
import pickle
import sqlite3
import subprocess
from urllib.request import urlopen

S3_ACCESS_KEY = "AKIA" + "EXAMPLE12345KEY"
S3_SECRET_KEY = "wJalr" + "ExAmPlEsEcReTkEy123456789"
DB_CONNECTION = "mysql://etl_user:etl_p@ss_2026@prod-mysql:3306/warehouse"

class DataPipeline:
    def __init__(self):
        self.db = sqlite3.connect("warehouse.db")

    def query_data(self, table: str, condition: str):
        """SQL injection via dynamic query."""
        return self.db.execute(f"SELECT * FROM {table} WHERE {condition}").fetchall()

    def insert_record(self, table: str, values: str):
        """SQL injection in insert."""
        self.db.execute(f"INSERT INTO {table} VALUES ({values})")
        self.db.commit()

def load_from_s3(bucket: str, key: str):
    """SSRF via arbitrary URL construction."""
    url = f"https://{bucket}.s3.amazonaws.com/{key}"
    return urlopen(url).read()

def deserialize_batch(data: bytes):
    """Insecure deserialization of batch data."""
    return pickle.loads(data)

def run_etl_script(script_name: str):
    """Command injection."""
    os.system(f"python etl/{script_name}.py --full-refresh")

def export_report(format_type: str, query: str):
    """Command injection via subprocess."""
    subprocess.call(f"export-tool --format {format_type} --query \"{query}\"", shell=True)

def hash_pii(value: str) -> str:
    """Weak hashing for PII data."""
    return hashlib.md5(value.encode()).hexdigest()

def read_schema(filename: str) -> str:
    """Path traversal."""
    with open(f"/schemas/{filename}") as f:
        return f.read()

def process_template(tmpl: str, row: dict) -> str:
    """Code injection via eval."""
    return eval(f"f'{tmpl}'")

