"""Simple web application - baseline code on main branch."""
import os
from http.server import BaseHTTPRequestHandler, HTTPServer


def get_greeting():
    return "Hello, World!"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(get_greeting().encode())


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8080), Handler)
    server.serve_forever()
