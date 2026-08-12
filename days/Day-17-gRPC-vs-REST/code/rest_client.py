#!/usr/bin/env python3
"""
Day 17 — Minimal REST HTTP Client (Standard Library)

Demonstrates client-side REST interaction:
1. Constructing an HTTP GET request to a URI.
2. Opening a TCP socket and receiving an HTTP response stream over the network.
3. Inspecting response status codes and HTTP headers.
4. Manually parsing and deserializing the JSON payload into dynamic client memory structures.
5. Handling network layer errors (timeouts, 404s, connection refused).
"""

import json
import sys
import urllib.request
import urllib.error

def fetch_user(user_id: int, base_url: str = "http://127.0.0.1:8080"):
    """Fetches user resource via REST HTTP GET request."""
    url = f"{base_url}/users/{user_id}"
    print(f"\n[REST Client] Initiating HTTP GET -> {url}")

    # Build HTTP Request object with custom headers
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": "DistributedSystemsClient/1.0"}
    )

    try:
        # Open network connection and transmit HTTP GET over TCP
        with urllib.request.urlopen(request, timeout=3.0) as response:
            # 1. Inspect HTTP Status Code
            status_code = response.getcode()
            content_type = response.headers.get("Content-Type")
            content_length = response.headers.get("Content-Length")
            
            print(f"[REST Client] Response Received | Status: {status_code} OK")
            print(f"[REST Client] Headers | Content-Type: {content_type}, Content-Length: {content_length} bytes")

            # 2. Read raw response bytes off TCP buffer
            raw_bytes = response.read()
            print(f"[REST Client] Raw Payload Wire Bytes ({len(raw_bytes)} bytes): {raw_bytes.decode('utf-8')}")

            # 3. Parse JSON string into Python dynamic dict structure
            user_data = json.loads(raw_bytes.decode('utf-8'))
            
            print(f"[REST Client] Successfully Deserialized Data:")
            print(f"              ID:    {user_data.get('user_id')}")
            print(f"              Name:  {user_data.get('name')}")
            print(f"              Role:  {user_data.get('role')}")
            return user_data

    except urllib.error.HTTPError as e:
        print(f"[REST Client] HTTP Failure Error Code: {e.code}")
        err_body = e.read().decode('utf-8')
        print(f"[REST Client] Server Returned Error Payload: {err_body}")
    except urllib.error.URLError as e:
        print(f"[REST Client] Network/Connection Error: {e.reason}")
        print(f"              (Ensure rest_server.py is running on http://127.0.0.1:8080)")
    except Exception as e:
        print(f"[REST Client] Unexpected Exception: {e}")

if __name__ == "__main__":
    print("==================================================")
    print("           REST Client Execution Demo             ")
    print("==================================================")
    
    # 1. Successful fetch
    fetch_user(42)

    # 2. Query non-existent user (Demonstrating HTTP 404)
    fetch_user(999)
