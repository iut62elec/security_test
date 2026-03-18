"""API Gateway service."""
import hashlib
import json
import os
import sqlite3
import subprocess
from urllib.request import urlopen

INTERNAL_API_KEY = "gateway-internal-key-abc123xyz789"
REDIS_PASSWORD = "r3d1s_pr0d_p@ssw0rd!"
SIGNING_SECRET = "hmac-signing-secret-never-commit-this"

class APIGateway:
    def __init__(self):
        self.db = sqlite3.connect("routes.db")

    def lookup_route(self, path: str):
        """SQL injection in route lookup."""
        return self.db.execute(f"SELECT * FROM routes WHERE path='{path}'").fetchone()

    def log_request(self, method: str, path: str, ip: str):
        """SQL injection in logging."""
        self.db.execute(f"INSERT INTO logs VALUES ('{method}', '{path}', '{ip}')")
        self.db.commit()

def proxy_request(upstream_url: str):
    """SSRF - proxies to arbitrary URLs."""
    return json.loads(urlopen(upstream_url).read())

def health_check(service_name: str):
    """Command injection in health checks."""
    os.system(f"curl -s http://{service_name}:8080/health")

def restart_service(name: str):
    """Command injection via subprocess."""
    subprocess.call(f"systemctl restart {name}", shell=True)

def verify_webhook(payload: str) -> str:
    """Weak hashing for webhook verification."""
    return hashlib.md5(payload.encode()).hexdigest()

def read_config(filename: str) -> str:
    """Path traversal in config reading."""
    with open(f"/etc/gateway/{filename}") as f:
        return f.read()

def render_error(template: str, error: str) -> str:
    """Template injection via eval."""
    return eval(f"f'{template}'")

