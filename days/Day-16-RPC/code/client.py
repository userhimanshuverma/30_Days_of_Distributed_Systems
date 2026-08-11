#!/usr/bin/env python3
"""
Day 16 — Remote Procedure Call (RPC) Educational Implementation: Client

This script demonstrates the client stub layer of a Remote Procedure Call system.

Key Educational Goals:
1. Demonstrate how a Client Stub makes a remote network call look like a local Python method call.
2. Show request object construction and JSON serialization.
3. Show socket transmission across the network boundary.
4. Demonstrate timeout and error handling when the server is slow or fails.
5. Highlight the fundamental difference between local functions and network RPCs.
"""

import json
import socket
import time


class RPCClientStub:
    """
    Client Stub Abstraction: Encapsulates network operations, socket lifecycles,
    serialization, deserialization, and timeout management behind clean local methods.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 9999, timeout_seconds: float = 2.0):
        self.host = host
        self.port = port
        self.timeout_seconds = timeout_seconds
        self._request_counter = 0

    def _call_remote_procedure(self, method_name: str, params: dict) -> dict:
        """
        Internal Stub Helper: Converts local method arguments into an RPC network frame.
        Handles serialization, socket transmission, timeout bounds, and deserialization.
        """
        self._request_counter += 1
        req_id = self._request_counter

        # 1. Request Object Construction
        rpc_request = {
            "jsonrpc": "2.0",
            "method": method_name,
            "params": params,
            "id": req_id,
        }

        # 2. Serialization: Convert Python dict to JSON byte stream
        serialized_payload = (json.dumps(rpc_request) + "\n").encode("utf-8")

        print(f"\n[Client Stub] Calling remote procedure: '{method_name}' with params {params}")
        print(f"[Client Stub] Serialized payload ({len(serialized_payload)} bytes): {serialized_payload.strip()}")

        start_time = time.time()

        # 3. Network Transmission over TCP Socket
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                # Enforce bounded deadline / timeout on network I/O
                sock.settimeout(self.timeout_seconds)

                print(f"[Client Stub] Connecting to remote endpoint {self.host}:{self.port} (Timeout={self.timeout_seconds}s)...")
                sock.connect((self.host, self.port))

                # Transmit frame across network boundary
                sock.sendall(serialized_payload)

                # 4. Receive and Buffer Response
                buffer = ""
                while True:
                    chunk = sock.recv(4096).decode("utf-8")
                    if not chunk:
                        raise ConnectionResetError("Server closed connection prematurely.")
                    buffer += chunk
                    if "\n" in buffer:
                        break

                elapsed = (time.time() - start_time) * 1000
                response_line = buffer.split("\n", 1)[0]
                print(f"[Client Stub] Received response in {elapsed:.2f}ms: {response_line.strip()}")

                # 5. Deserialization: Parse response JSON string back into Python dict
                response_data = json.loads(response_line)

                # 6. Error Evaluation
                if response_data.get("error"):
                    raise RuntimeError(f"Remote RPC Exception: {response_data['error']}")

                return response_data.get("result")

        except socket.timeout:
            elapsed = (time.time() - start_time) * 1000
            print(f"[Client Stub TIMEOUT] Request '{method_name}' exceeded deadline of {self.timeout_seconds}s after {elapsed:.2f}ms!")
            raise TimeoutError(f"RPC call to '{method_name}' timed out after {self.timeout_seconds}s.")
        except ConnectionRefusedError:
            print(f"[Client Stub ERROR] Could not connect to remote host {self.host}:{self.port}. Is server running?")
            raise ConnectionError("RPC Server is unavailable.")

    # --- PUBLIC STUB INTERFACE (LOOKS LIKE LOCAL FUNCTIONS) ---

    def getUser(self, user_id: int) -> dict:
        """Stub method wrapping remote call `getUser`."""
        return self._call_remote_procedure("getUser", {"user_id": user_id})

    def getOrder(self, order_id: int) -> dict:
        """Stub method wrapping remote call `getOrder`."""
        return self._call_remote_procedure("getOrder", {"order_id": order_id})

    def slowOperation(self, delay_seconds: float) -> dict:
        """Stub method wrapping remote call `slowOperation`."""
        return self._call_remote_procedure("slowOperation", {"delay_seconds": delay_seconds})


# --- DEMONSTRATION SCRIPT ---
def main():
    print("=" * 65)
    print("[RPC Client] Day 16 Educational RPC Client Demonstration")
    print("=" * 65)

    # Initialize Client Stub pointing to localhost server with a 2.0s deadline
    rpc_client = RPCClientStub(host="127.0.0.1", port=9999, timeout_seconds=2.0)

    # Demo 1: Successful Remote Call (Looks like local function!)
    try:
        user = rpc_client.getUser(42)
        print(f"\n[SUCCESS] Result returned to application code:")
        print(f"   User Name : {user['name']}")
        print(f"   User Role : {user['role']}")
    except Exception as e:
        print(f"Failed demo 1: {e}")

    # Demo 2: Querying another endpoint
    try:
        order = rpc_client.getOrder(9001)
        print(f"\n[SUCCESS] Result returned to application code:")
        print(f"   Order Item : {order['item']}")
        print(f"   Amount USD : ${order['amount_usd']}")
    except Exception as e:
        print(f"Failed demo 2: {e}")

    # Demo 3: Remote Error Handling (Requesting non-existent entity)
    print("\n--- Edge Case Demo: Handling Remote Function Exception ---")
    try:
        user = rpc_client.getUser(999)
    except RuntimeError as ex:
        print(f"[CAUGHT EXCEPTION] Application caught remote exception: {ex}")

    # Demo 4: Timeout / Partial Failure Demo (Server delays 4.0s, client timeout is 2.0s)
    print("\n--- Edge Case Demo: Enforcing Deadlines & Handling Network Timeout ---")
    try:
        rpc_client.slowOperation(delay_seconds=4.0)
    except TimeoutError as ex:
        print(f"[CAUGHT TIMEOUT] Application caught network deadline failure: {ex}")
        print("   Notice: The server may STILL be processing this work!")
        print("   This is PARTIAL FAILURE: The client timed out, but the server is unaware!")

    print("\n=" * 65)
    print("RPC Client execution finished.")
    print("=" * 65)


if __name__ == "__main__":
    main()
