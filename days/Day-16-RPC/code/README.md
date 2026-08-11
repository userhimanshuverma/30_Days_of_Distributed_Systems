# Day 16 Code — Educational RPC Implementation

This directory contains a lightweight, zero-dependency Remote Procedure Call (RPC) demonstration built with Python standard library sockets (`socket`) and JSON (`json`).

---

## 📂 File Structure

* `server.py`: RPC Server daemon that listens on TCP port `9999`, receives serialized JSON requests, routes methods to Python functions, and sends serialized JSON responses.
* `client.py`: RPC Client Stub that exposes clean local Python methods (`getUser`, `getOrder`), encapsulates network socket I/O, manages request serialization, and enforces network timeouts.

---

## 🏃 How to Run

### Step 1: Start the RPC Server

In your first terminal window, navigate to this directory and start the server:

```bash
python server.py
```

You should see output indicating the server is listening:

```text
=================================================================
🚀 Day 16 Educational RPC Server listening on 127.0.0.1:9999
Press Ctrl+C to stop the server.
=================================================================
```

### Step 2: Run the RPC Client

In a second terminal window, run the client demonstration script:

```bash
python client.py
```

---

## 🔍 Key Concepts Demonstrated in Code

1. **Stub Abstraction**: Application code invokes `rpc_client.getUser(42)`. It looks and feels like a simple local function call.
2. **Serialization & Wire Protocol**: Behind the scenes, `client.py` packs the function name and parameters into a JSON message: `{"jsonrpc": "2.0", "method": "getUser", "params": {"user_id": 42}, "id": 1}` and transmits bytes over a TCP socket.
3. **Server Dispatching**: `server.py` reads raw byte chunks, parses JSON, looks up `getUser` in its procedure dictionary, executes it, and sends back a serialized result frame.
4. **Remote Exception Handling**: When querying a non-existent user (`user_id=999`), the server catches the Python exception and serializes an error frame back to the client stub, which re-raises it as a runtime error.
5. **Deadlines & Partial Failure**: When invoking `slowOperation(4.0)`, the client's $2.0\text{s}$ timeout triggers a `TimeoutError`. Notice that **the server continues running the slow operation in the background** — demonstrating why client-side timeouts can leave the application in an uncertain state regarding whether remote side effects executed.
