# Day 16 Visual Assets Specification

This directory holds visual specifications and design guidelines for **Day 16 — RPC: Why Calling Another Server Feels Like Calling a Function**.

---

## 🎨 Required Asset Specifications

### 1. `local-vs-remote.png`
* **Filename**: `local-vs-remote.png`
* **Purpose**: Contrast the deterministic simplicity of a local function call in memory with the complex, multi-layered path of a remote procedure call across the network.
* **What the Diagram Should Show**:
  * **Left Side (Local Call)**: Application component pointing directly down to a Function execution stack, which reads/writes directly to local CPU Registers and RAM. Highlight single-process boundary in soft blue with a label "0.0001 ms, 100% In-Memory Determinism".
  * **Right Side (Remote Call)**: Application component calling a Client Stub, which serializes data, sends packets across a red-dashed Network Boundary (TCP/IP stack, routers, switches), into an RPC Server Stub, which unpacks the frame and invokes the Target Handler.
* **Important Labels**: `Local Function Stack`, `Memory Bus`, `Client Stub`, `Serialization`, `Network Boundary (Latency & Drops)`, `Server Stub`, `Deserialization`, `Target Handler`.
* **Visual Relationship**: Parallel side-by-side comparison showing clean memory arrows on the left vs a multi-hop, cross-process network pipeline on the right.

---

### 2. `rpc-request-lifecycle.png`
* **Filename**: `rpc-request-lifecycle.png`
* **Purpose**: Provide a step-by-step sequential blueprint of an RPC request traveling from client application code to the server handler and back.
* **What the Diagram Should Show**:
  * Horizontal timeline or sequence flow starting at **Client App** $\rightarrow$ **Client Stub (Packing/Serialization)** $\rightarrow$ **Transport Layer (Sockets/TCP)** $\rightarrow$ **Network Cable** $\rightarrow$ **Server Transport** $\rightarrow$ **Server Stub (Unpacking/Deserialization)** $\rightarrow$ **Server Handler Routine**.
  * Show the return path mirroring back from right to left with serialized response payload bytes.
* **Important Labels**: `Step 1: Local Method Invocation`, `Step 2: Schema Serialization (JSON/Protobuf)`, `Step 3: Network Transport (Socket Write)`, `Step 4: Network Propagation`, `Step 5: Server Receive & Unpack`, `Step 6: Handler Execution`, `Step 7-12: Response Serialization & Return`.
* **Visual Relationship**: End-to-end U-shaped flow (top-left to bottom-right and back to top-left) with distinct layers (Application, Stub, Network, Handler) color-coded.

---

### 3. `rpc-failure.png`
* **Filename**: `rpc-failure.png`
* **Purpose**: Illustrate the concept of Partial Failure and network ambiguity where the response is dropped, leaving the client uncertain whether the remote operation executed.
* **What the Diagram Should Show**:
  * **Client Node**: Sends `charge_credit_card(user_id=42, amount=$100)` across the network.
  * **Server Node**: Receives request, successfully processes payment in database (`Database: Balance Deducted $100`).
  * **Return Path**: Server sends `200 OK Response`, but a red lightning bolt symbol icon indicates a Network Partition / Dropped Packet.
  * **Client State Callout**: Question mark speech bubble over Client: *"Request timed out! Did the server process my payment or fail before receiving it?"*
* **Important Labels**: `Client Stub (Waiting)`, `Successful Remote Execution`, `Network Partition (Dropped ACKs)`, `Client Uncertainty Window`, `Partial Failure Dilemma`.
* **Visual Relationship**: Top-to-bottom transmission showing green successful execution on server side, severed red return arrow, and highlighted client state of ambiguity.

---

### 4. `timeout-and-retry.png`
* **Filename**: `timeout-and-retry.png`
* **Purpose**: Visualizing how uncoordinated client retries on non-idempotent endpoints cause duplicate side effects in backend infrastructure.
* **What the Diagram Should Show**:
  * Timeline of Attempt 1: Client sends `CreateOrder()`, Server processes it, but response delays past $500\text{ms}$ client deadline threshold.
  * Timeout Trigger: Client Stub raises `TimeoutError` at $t=500\text{ms}$.
  * Timeline of Attempt 2: Naive client automatically retries `CreateOrder()`. Server receives Attempt 2 and creates a *second* duplicate order in database.
  * Side-by-side callout banner explaining non-idempotent duplication vs idempotent safe retries.
* **Important Labels**: `Deadline = 500ms`, `Delayed Server ACK`, `Client Timeout Exception`, `Automatic Retry Attempt 2`, `Duplicate Database Insertion (Order #101 & #102)`, `Idempotency Key Solution`.
* **Visual Relationship**: Cascading dual-attempt timeline showing time progression along the vertical axis and duplicate side-effects in the storage layer.

---

### 5. `service-dependency-graph.png`
* **Filename**: `service-dependency-graph.png`
* **Purpose**: Show how RPC calls multiply exponentially across microservice architecture, leading to fan-out latency and cascading failures.
* **What the Diagram Should Show**:
  * Root node: **API Gateway** making concurrent RPC calls to **User Service** and **Order Service**.
  * **Order Service** branching out to make child RPC calls to **Inventory Service**, **Payment Service**, and **Notification Service**.
  * **Payment Service** calling external **Stripe API**.
  * Annotations showing how $50\text{ms}$ latency at each tier compounds to $350\text{ms}$ total response time at the gateway, and how one slow leaf node stalls the entire request chain.
* **Important Labels**: `API Gateway (Ingress)`, `Fan-Out Factor = 3`, `Multi-Tier RPC Chain`, `Latency Compounding ($L_{\text{total}} = \sum L_i$)`, `Cascading Timeout Risk`.
* **Visual Relationship**: Tree hierarchy graph expanding from top to bottom with highlighted call latency badges on each edge.
