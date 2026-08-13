# Day 18 — Messaging Code Examples & Hands-on Demonstrations

This directory contains standalone Python implementations demonstrating the fundamental mechanics of message brokers, consumer concurrency, acknowledgements, retries, dead-letter queues, and backpressure.

---

## 🛠️ Code Included

### 1. [`simple_queue.py`](file:///d:/30_Days_of_Distributed_Systems/days/Day-18-Messaging/code/simple_queue.py)
* **Goal**: Build intuition for basic in-memory FIFO message queuing.
* **Key Concepts**: Producer publish, Consumer consume, FIFO ordering, thread-safe message buffers.
* **How to run**:
  ```bash
  python simple_queue.py
  ```

### 2. [`producer_consumer.py`](file:///d:/30_Days_of_Distributed_Systems/days/Day-18-Messaging/code/producer_consumer.py)
* **Goal**: Understand consumer scaling and explicit acknowledgement (`ACK` / `NACK`) mechanics.
* **Key Concepts**: Concurrent consumer worker pools, visibility state/in-flight message tracking, message retries on NACK.
* **How to run**:
  ```bash
  python producer_consumer.py
  ```

### 3. [`retry_and_dead_letter.py`](file:///d:/30_Days_of_Distributed_Systems/days/Day-18-Messaging/code/retry_and_dead_letter.py)
* **Goal**: Explore fault tolerance, transient failure retries, and poison message handling.
* **Key Concepts**: Maximum retry threshold, Dead-Letter Queue (DLQ) routing, preventing head-of-line blocking.
* **How to run**:
  ```bash
  python retry_and_dead_letter.py
  ```

### 4. [`backpressure_demo.py`](file:///d:/30_Days_of_Distributed_Systems/days/Day-18-Messaging/code/backpressure_demo.py)
* **Goal**: Demonstrate producer/consumer velocity mismatch, backlog growth, lag, and backpressure mitigations.
* **Key Concepts**: Consumer lag monitoring, bounded queues (producer rate throttling), dynamic consumer worker scaling.
* **How to run**:
  ```bash
  python backpressure_demo.py
  ```

---

## 📋 System Requirements
* Python 3.8+ (Uses standard library packages: `queue`, `threading`, `dataclasses`, `datetime`, `uuid`). No third-party dependencies required.
