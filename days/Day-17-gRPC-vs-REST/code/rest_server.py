#!/usr/bin/env python3
"""
Day 17 — Minimal REST HTTP Server (Standard Library)

Demonstrates the core mechanics of a RESTful API:
1. Routing based on HTTP Methods (GET) and URIs (/users/<id>).
2. Resource representation using JSON serialization over HTTP/1.1.
3. Standard HTTP status codes (200 OK, 404 Not Found, 400 Bad Request).
"""

import json
import re
from http.server import HTTPServer, BaseHTTPRequestHandler

# In-memory user database representing resource state
USERS_DB = {
    42: {"user_id": 42, "name": "Alice Smith", "email": "alice@example.com", "role": "Site Reliability Engineer"},
    101: {"user_id": 101, "name": "Bob Jones", "email": "bob@example.com", "role": "Backend Developer"},
}

class RESTUserRequestHandler(BaseHTTPRequestHandler):
    """Handles HTTP requests adhering to REST conventions."""

    def do_GET(self):
        """Handle GET requests for retrieving user resources."""
        # Match URI pattern: /users/<user_id>
        match = re.match(r"^/users/(\d+)$", self.path)
        
        if match:
            user_id = int(match.group(1))
            user = USERS_DB.get(user_id)
            
            if user:
                # 1. Resource Found -> Serialize Python dict to JSON payload
                payload = json.dumps(user).encode('utf-8')
                
                # 2. Write HTTP Headers
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                
                # 3. Write Response Body to Network Socket
                self.wfile.write(payload)
                print(f"[REST Server] 200 OK -> Returned user {user_id}")
            else:
                # Resource Not Found -> Standard HTTP 404
                self._send_json_error(404, {"error": "User Not Found", "user_id": user_id})
        else:
            # Invalid URI / Endpoint -> Standard HTTP 400
            self._send_json_error(400, {"error": "Invalid URI path. Use /users/<id>"})

    def _send_json_error(self, status_code: int, message_dict: dict):
        """Helper to send standard HTTP error responses formatted as JSON."""
        payload = json.dumps(message_dict).encode('utf-8')
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)
        print(f"[REST Server] {status_code} Error -> {message_dict}")

    def log_message(self, format, *args):
        """Suppress default HTTP server logging to keep terminal output clean."""
        return

def run_server(host="127.0.0.1", port=8080):
    server_address = (host, port)
    httpd = HTTPServer(server_address, RESTUserRequestHandler)
    print(f"==================================================")
    print(f"  REST HTTP Server running on http://{host}:{port}")
    print(f"  Try: curl -i http://{host}:{port}/users/42")
    print(f"==================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down REST server.")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
