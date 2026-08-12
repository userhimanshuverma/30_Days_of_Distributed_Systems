# Day 17 Visual Assets Specification

This directory holds visual specifications and design guidelines for **Day 17 — REST vs gRPC**.

---

## 🎨 Required Asset Specifications

### 1. `rest-vs-grpc.png`
* **Filename**: `rest-vs-grpc.png`
* **Purpose**: Contrast REST and gRPC architecture side by side.
* **What the Diagram Should Show**:
  * **Left Side (REST)**: Client Application $\rightarrow$ HTTP Request (JSON Payload) $\rightarrow$ Network Boundary $\rightarrow$ HTTP Server $\rightarrow$ Controller Route Handler. Highlight text-based JSON over HTTP/1.1 or HTTP/2.
  * **Right Side (gRPC)**: Client Application $\rightarrow$ Auto-Generated Stub $\rightarrow$ Binary Protobuf Serialization $\rightarrow$ HTTP/2 Multiplexed Frames $\rightarrow$ Network Boundary $\rightarrow$ gRPC Server $\rightarrow$ Servicer Method.
* **Important Labels**: `REST (Architectural Style)`, `gRPC (RPC Framework)`, `JSON Serializer`, `Protobuf Compiler (protoc)`, `HTTP/1.1 vs HTTP/2`, `Human-Inspectable vs Binary Wire Format`.
* **Visual Relationship**: Parallel side-by-side architectural flow highlighting contract enforcement and serialization differences.

---

### 2. `rest-request-flow.png`
* **Filename**: `rest-request-flow.png`
* **Purpose**: Provide a step-by-step lifecycle flow of a REST HTTP call.
* **What the Diagram Should Show**:
  * Horizontal/Vertical sequence:
    1. **Application Code**: Initiates `GET /users/42`.
    2. **HTTP Client Library**: Builds HTTP request envelope (headers, method, URI).
    3. **JSON Serialization**: Converts internal memory struct/dict into UTF-8 JSON string bytes.
    4. **Network Socket**: Transmits raw HTTP frame across TCP socket.
    5. **Network Propagation**: Routers & switches deliver TCP packets.
    6. **REST Server**: Parses HTTP verb and route URL path.
    7. **Server Handler**: Processes request, queries DB, constructs JSON response.
    8. **Deserialization**: Client reads JSON bytes off socket and parses into language dict/object.
* **Important Labels**: `HTTP GET /users/42`, `Content-Type: application/json`, `TCP Socket Write`, `Route Matching`, `JSON.parse()`.

---

### 3. `grpc-request-flow.png`
* **Filename**: `grpc-request-flow.png`
* **Purpose**: Provide a step-by-step lifecycle flow of a gRPC method call.
* **What the Diagram Should Show**:
  * Horizontal/Vertical sequence:
    1. **Application Code**: Invokes generated method `stub.GetUser(UserRequest(user_id=42))`.
    2. **Generated Stub**: Validates parameters against static Protobuf types.
    3. **Protobuf Binary Serialization**: Encodes fields into compact binary varints and wire tags.
    4. **HTTP/2 Transport Framing**: Encapsulates binary payload into HTTP/2 HEADERS and DATA frames with stream IDs.
    5. **Network Propagation**: Low-latency multiplexed transmission over persistent TCP connection.
    6. **gRPC Server Engine**: Receives HTTP/2 frame, identifies target RPC method via header.
    7. **Servicer Execution**: Invokes implementation handler routine.
    8. **Return Path**: Binary response sent back across HTTP/2 stream, deserialized by stub into typed object.
* **Important Labels**: `Typed Method Call`, `Protobuf Encoder`, `HTTP/2 Multiplexing (STREAM ID)`, `Zero-Parsing Overhead`, `Typed Response Object`.

---

### 4. `remote-call-failure.png`
* **Filename**: `remote-call-failure.png`
* **Purpose**: Illustrate network failure paths, timeouts, retries, and non-idempotent side effects in remote call mechanics.
* **What the Diagram Should Show**:
  * **Top Timeline (Normal Request)**: Client $\rightarrow$ Request $\rightarrow$ Server $\rightarrow$ Success ACK.
  * **Middle Timeline (Network Drop / Timeout)**: Client sends request $\rightarrow$ Network drops packet (or response lost) $\rightarrow$ Client timer hits Deadline ($500\text{ms}$) $\rightarrow$ `TimeoutError` raised.
  * **Bottom Timeline (Unsafe Retry Side-Effect)**: Client receives Timeout $\rightarrow$ Sends Retry Attempt 2 $\rightarrow$ Server executes side effect *twice* (e.g. charging credit card twice) because endpoint lacks an Idempotency Key.
* **Important Labels**: `Network Cable Cut / Loss`, `Deadline Exceeded (500ms)`, `Ambiguous State Window`, `Uncoordinated Retry`, `Duplicate Execution Risk`, `Idempotency Guard`.
