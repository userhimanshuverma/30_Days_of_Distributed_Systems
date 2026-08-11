#!/usr/bin/env python3
"""
Day 16 — Remote Procedure Call (RPC) Educational Implementation: Server

This script demonstrates the server side of a minimal Remote Procedure Call framework
built from scratch using Python's standard library (`socket` and `json`).

Key Educational Goals:
1. Show how a server receives raw byte streams across a network boundary.
2. Demonstrate JSON request deserialization.
3. Route method calls to local Python handler functions.
4. Serialize and send structured JSON responses back across the wire.
5. Handle remote execution errors gracefully without crashing the server daemon.
"""

import json
import socket
import sys
import time

# --- MOCK IN-MEMORY DATABASE ---
USERS_DB = {
    42: {"id": 42, "name": "Alice Smith", "email": "alice@example.com", "role": "Distributed Systems Engineer"},
    101: {"id": 101, "name": "Bob Jones", "email": "bob@example.com", "role": "Site Reliability Engineer"},
}

ORDERS_DB = {
    9001: {"order_id": 9001, "user_id": 42, "item": "Distributed Systems Handbook", "amount_usd": 49.99},
}


# --- LOCAL HANDLER FUNCTIONS (REMOTE PROCEDURES) ---
def get_user(user_id: int) -> dict:
    """Remote Procedure: Fetch user data by ID."""
    print(f"  [Server Handler] Executing get_user(user_id={user_id})")
    if user_id in USERS_DB:
        return USERS_DB[user_id]
    raise ValueError(f"User with ID {user_id} not found.")


def get_order(order_id: int) -> dict:
    """Remote Procedure: Fetch order details by ID."""
    print(f"  [Server Handler] Executing get_order(order_id={order_id})")
    if order_id in ORDERS_DB:
        return ORDERS_DB[order_id]
    raise ValueError(f"Order with ID {order_id} not found.")


def slow_operation(delay_seconds: float) -> dict:
    """Remote Procedure: Simulates a slow backend service to trigger client timeouts."""
    print(f"  [Server Handler] Executing slow_operation(delay={delay_seconds}s)")
    time.sleep(delay_seconds)
    return {"status": "completed", "waited_seconds": delay_seconds}


# RPC Procedure Dispatch Registry
PROCEDURES = {
    "getUser": get_user,
    "getOrder": get_order,
    "slowOperation": slow_operation,
}


def handle_client_connection(conn: socket.socket, addr: tuple):
    """
    Handles an incoming RPC client connection over TCP.
    Protocol: Line-delimited JSON strings (each message ends with '\\n').
    """
    print(f"[Server] Connected by client at {addr[0]}:{addr[1]}")
    buffer = ""

    try:
        while True:
            # Receive raw bytes from network socket
            data = conn.recv(4096)
            if not data:
                print(f"[Server] Client {addr[0]}:{addr[1]} disconnected.")
                break

            buffer += data.decode("utf-8")

            # Process complete newline-terminated JSON messages
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                if not line.strip():
                    continue

                # 1. Network Boundary: Receive JSON Request Frame
                print(f"\n[Server] Received raw byte payload: {line.encode('utf-8')}")

                # 2. Deserialization: Parse raw JSON string into dict
                try:
                    request = json.loads(line)
                except json.JSONDecodeError as err:
                    response = {"jsonrpc": "2.0", "error": f"Invalid JSON payload: {str(err)}", "id": None}
                    conn.sendall((json.dumps(response) + "\n").encode("utf-8"))
                    continue

                req_id = request.get("id")
                method = request.get("method")
                params = request.get("params", {})

                # 3. Method Routing & Execution
                if method not in PROCEDURES:
                    response = {
                        "jsonrpc": "2.0",
                        "error": f"Method '{method}' not found on server dispatch table.",
                        "id": req_id,
                    }
                else:
                    try:
                        # Invoke target function with unpacked parameters
                        result = PROCEDURES[method](**params)
                        # 4. Success Response Packaging
                        response = {"jsonrpc": "2.0", "result": result, "error": None, "id": req_id}
                    except Exception as ex:
                        # 5. Partial Failure Handling: Capture runtime exception as RPC error response
                        print(f"  [Server Error] Exception during handling: {ex}")
                        response = {"jsonrpc": "2.0", "result": None, "error": str(ex), "id": req_id}

                # 6. Serialization & Network Transmission
                response_bytes = (json.dumps(response) + "\n").encode("utf-8")
                print(f"[Server] Sending serialized RPC response ({len(response_bytes)} bytes)")
                conn.sendall(response_bytes)

    except Exception as e:
        print(f"[Server] Connection error with {addr}: {e}")
    finally:
        conn.close()


def run_rpc_server(host: str = "127.0.0.1", port: int = 9999):
    """Starts the single-threaded RPC server socket listener."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        # Allow address reuse for quick restarts
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((host, port))
        server_sock.listen(5)
        print("=" * 65)
        print(f"[RPC Server] Day 16 Educational RPC Server listening on {host}:{port}")
        print("Press Ctrl+C to stop the server.")
        print("=" * 65)

        try:
            while True:
                conn, addr = server_sock.accept()
                handle_client_connection(conn, addr)
        except KeyboardInterrupt:
            print("\n[Server] Shutting down gracefully.")
            sys.exit(0)


if __name__ == "__main__":
    run_rpc_server()
