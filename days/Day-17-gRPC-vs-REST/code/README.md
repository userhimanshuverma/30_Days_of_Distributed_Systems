# Day 17 Code — Hands-On REST vs gRPC Comparison

This directory contains minimal, runnable code examples comparing **REST (HTTP/JSON)** and **gRPC (HTTP/2 / Protobuf)** in Python.

---

## 📁 Files Included

* `rest_server.py`: Minimal REST HTTP server implementation using Python's standard library (`http.server`). Zero third-party dependencies required.
* `rest_client.py`: Minimal REST HTTP client making GET requests with `urllib.request` and parsing JSON payloads. Zero dependencies required.
* `user.proto`: Protocol Buffer contract defining `UserService`, data messages (`UserRequest`, `UserResponse`), and streaming methods (`StreamUserActivity`).
* `grpc_server.py`: gRPC server implementing `UserService` for unary and server streaming RPCs.
* `grpc_client.py`: gRPC client invoking unary RPC methods and consuming stream responses using auto-generated client stubs.

---

## 🚀 How to Run Example 1: REST (Zero Setup Required)

The REST examples run out-of-the-box using standard Python 3.

### Step 1: Start the REST Server
In your terminal, run:
```bash
python rest_server.py
```
Output:
```text
==================================================
  REST HTTP Server running on http://127.0.0.1:8080
  Try: curl -i http://127.0.0.1:8080/users/42
==================================================
```

### Step 2: Run the REST Client
In a second terminal window, run:
```bash
python rest_client.py
```

Or test directly with `curl`:
```bash
curl -i http://127.0.0.1:8080/users/42
```

---

## 🚀 How to Run Example 2: gRPC

To run the gRPC examples natively, install the official `grpcio` and `grpcio-tools` packages.

### Step 1: Install Dependencies
```bash
pip install grpcio grpcio-tools
```

### Step 2: Generate Python Stubs from `user.proto`
Compile the Protobuf contract to generate `user_pb2.py` and `user_pb2_grpc.py`:
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. user.proto
```

### Step 3: Start the gRPC Server
In Terminal 1:
```bash
python grpc_server.py
```
Output:
```text
==================================================
  gRPC Server running on 127.0.0.1:50051 (HTTP/2)
==================================================
```

### Step 4: Run the gRPC Client
In Terminal 2:
```bash
python grpc_client.py
```
Output:
```text
==================================================
           gRPC Client Execution Demo
==================================================

Opening HTTP/2 channel to 127.0.0.1:50051...

--- Demo 1: Unary GetUser RPC ---
Calling stub.GetUser(user_id=42) with 2.0s deadline...
RPC Response Received!
              ID:    42
              Name:  Alice Smith
              Email: alice@example.com
              Role:  Site Reliability Engineer

--- Demo 2: Handling gRPC Error Status (User 999) ---
Calling stub.GetUser(user_id=999)...
Caught expected RPC Error!
              Status Code: StatusCode.NOT_FOUND
              Error Detail: User with ID 999 was not found.

--- Demo 3: Server Streaming StreamUserActivity RPC ---
Subscribing to activity log stream for user_id=42...
Received Log: [2026-08-12T10:00:00Z] Action: LOGIN_SUCCESS (IP: 192.168.1.50)
Received Log: [2026-08-12T10:05:22Z] Action: DEPLOY_SERVICE (IP: 192.168.1.50)
Received Log: [2026-08-12T10:14:01Z] Action: UPDATE_CONFIG (IP: 192.168.1.50)
```
