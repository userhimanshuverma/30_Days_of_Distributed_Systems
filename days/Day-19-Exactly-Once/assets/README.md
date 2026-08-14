# Day 19 — Visual Assets Specification

This directory contains specifications and visual architectural diagrams for **Day 19 — Exactly Once**. 

> [!NOTE]
> The image asset files listed below represent production visual assets to be generated according to these structural design guidelines.

---

## Required Visual Diagrams

### 1. `failure-window.png`
* **Title**: The Distributed Uncertainty Window (Lost Response Scenario)
* **Concept**: Illustrates the asymmetry of knowledge between client and server when a network partition or response loss occurs.
* **Layout**:
  * **Top Timeline**: Client sends HTTP POST `/payment`, transitions into a `WAITING_FOR_ACK` state, times out, and sees `TimeoutError`.
  * **Middle Network Pipe**: Request arrow pointing right (green check: delivered), Response arrow pointing left (red X: dropped at network layer).
  * **Bottom Timeline**: Server receives request, executes database balance deduction (`UPDATE accounts SET balance = balance - 1000`), commits ACID transaction, generates HTTP 200 OK, and attempts transmission.
* **Key Visual Takeaway**: Shows that from the Client's perspective, a `TimeoutError` is completely indistinguishable between "Server crashed before processing" and "Server succeeded but response was dropped".

---

### 2. `delivery-semantics.png`
* **Title**: Spectrum of Distributed Delivery Semantics
* **Concept**: High-level visual comparison of At-Most-Once, At-Least-Once, and Exactly-Once (Effectively-Once) Processing.
* **Layout**:
  * **Panel A — At-Most-Once**: Producer → Consumer (No retries on network error). Result: 0 or 1 delivery. Message loss possible.
  * **Panel B — At-Least-Once**: Producer → Consumer → Network Failure → Producer Retries → Consumer. Result: 1+ deliveries. Duplicates guaranteed over time.
  * **Panel C — Exactly-Once Effect**: Producer (with Request ID) → Consumer → Network Failure → Producer Retries (Same ID) → Consumer Deduplication Store → Skip duplicate, replay cached response. Result: 1 logical state transition.

---

### 3. `idempotency-flow.png`
* **Title**: Idempotency Key Evaluation Flowchart
* **Concept**: Step-by-step internal execution flow of an idempotent service receiving a request.
* **Layout**:
  * Decision Diamond: `Idempotency Key present in headers?`
    * `No` → Return `400 Bad Request` (or execute standard non-idempotent flow).
    * `Yes` → Look up key in `idempotency_store`.
  * Decision Diamond: `Key state?`
    * `IN_FLIGHT` → Return `409 Conflict` (Concurrent request in progress).
    * `COMPLETED` → Return cached HTTP payload (No state modification).
    * `NOT_FOUND` → Atomically mark `IN_FLIGHT` → Execute Business Logic → Commit DB State + Mark `COMPLETED` → Return Response.

---

### 4. `end-to-end-processing.png`
* **Title**: Multi-Layer End-to-End Exactly-Once Pipeline
* **Concept**: Maps where duplicate records can be injected across every layer of a microservices architecture.
* **Layout**: Horizontal flow spanning 5 system components:
  1. **Client App**: Injects retry on network timeout.
  2. **API Gateway / Service A**: Ingress endpoint; assigns/validates `idempotency_key`.
  3. **Transactional Outbox / Database**: Ensures state change and message dispatch are atomic.
  4. **Distributed Message Broker (Kafka / RabbitMQ)**: Handles producer retries (`acks=all`) and consumer group rebalances.
  5. **Downstream Service B (Consumer) & External API (Payment Gateway)**: Checks deduplication table before executing third-party side effects.
