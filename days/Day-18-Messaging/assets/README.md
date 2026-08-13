# Day 18 Visual Assets Specification

This directory holds visual specifications and design guidelines for **Day 18 — Messaging: Kafka, RabbitMQ & Queues**.

---

## 🎨 Required Asset Specifications

### 1. `messaging-model.png`
* **Filename**: `messaging-model.png`
* **Purpose**: Establish the foundational asynchronous producer-broker-consumer mental model.
* **What the Diagram Should Show**:
  * **Left Side**: Producer application generating events/messages.
  * **Center**: Message Broker containing a durable buffer/queue (temporal decoupling layer).
  * **Right Side**: Consumer application asynchronously pulling or receiving messages from the broker.
* **Important Labels**: `Producer (Publisher)`, `Temporal Decoupling (Broker Buffer)`, `Consumer (Subscriber)`, `Asynchronous Push/Pull`.
* **Visual Relationship**: Highlights how the message broker sits between services so producers do not block waiting for consumers.

---

### 2. `rabbitmq-model.png`
* **Filename**: `rabbitmq-model.png`
* **Purpose**: Visualize RabbitMQ's message routing topology and queue delivery mechanics.
* **What the Diagram Should Show**:
  * **Flow**: Producer $\rightarrow$ Exchange $\rightarrow$ Bindings / Routing Keys $\rightarrow$ Queues $\rightarrow$ Consumers.
  * Contrast exchange types: Direct (exact key match), Topic (wildcard pattern match), Fanout (broadcast to all bound queues).
  * Show message removal from queue upon explicit consumer Acknowledgement (`ACK`).
* **Important Labels**: `Exchange`, `Routing Key`, `Binding`, `Durable Queue`, `Consumer ACK`, `Destructive Read / Delivery`.

---

### 3. `kafka-model.png`
* **Filename**: `kafka-model.png`
* **Purpose**: Visualize Apache Kafka's distributed commit log architecture.
* **What the Diagram Should Show**:
  * **Topic**: Divided into multiple immutable append-only Partitions (Partition 0, Partition 1, Partition 2).
  * **Producers**: Appending record records to partition tails.
  * **Consumer Groups**: Independent consumer groups (e.g., Billing Group, Analytics Group) reading from partitions via distinct offset pointers.
* **Important Labels**: `Topic`, `Partition 0 / 1 / 2`, `Offset Counter`, `Append-Only Distributed Log`, `Consumer Group A & B`, `Non-Destructive Read`.

---

### 4. `delivery-semantics.png`
* **Filename**: `delivery-semantics.png`
* **Purpose**: Contrast At-Most-Once, At-Least-Once, and Exactly-Once delivery & processing semantics.
* **What the Diagram Should Show**:
  * **At-Most-Once**: Send & forget / ACK before processing $\rightarrow$ Message may be lost on crash, never redelivered.
  * **At-Least-Once**: ACK after processing $\rightarrow$ Network timeout on ACK triggers redelivery $\rightarrow$ Risk of duplicates (requires Idempotent consumer).
  * **Exactly-Once**: End-to-end atomic processing (Kafka transactional producer/consumer + idempotent storage writes).
* **Important Labels**: `At-Most-Once (Data Loss Risk)`, `At-Least-Once (Duplicate Risk)`, `Exactly-Once (Transactional & Idempotent)`, `Consumer Idempotency`.

---

### 5. `consumer-failure.png`
* **Filename**: `consumer-failure.png`
* **Purpose**: Illustrate consumer process crashes, unacknowledged messages, redelivery, and poison message routing to Dead-Letter Queue (DLQ).
* **What the Diagram Should Show**:
  * **Sequence 1**: Broker delivers message $\rightarrow$ Consumer crashes mid-execution before sending ACK.
  * **Sequence 2**: Visibility timeout expires $\rightarrow$ Broker re-enqueues message $\rightarrow$ Alternate Consumer worker picks up message.
  * **Sequence 3**: Message consistently fails across max retries $\rightarrow$ Broker routes poison message to Dead-Letter Queue (DLQ).
* **Important Labels**: `In-Flight State`, `Consumer Crash`, `Visibility Timeout Expiry`, `Redelivery Attempt`, `Max Retries Exceeded`, `Dead-Letter Queue (DLQ)`.

---

### 6. `backpressure.png`
* **Filename**: `backpressure.png`
* **Purpose**: Demonstrate producer velocity outpacing consumer throughput, consumer lag, and mitigation mechanisms.
* **What the Diagram Should Show**:
  * **Rate Mismatch**: Producer emitting $10,000\text{ msg/sec}$ vs Consumer processing $2,000\text{ msg/sec}$.
  * **Queue Backlog**: Accumulating buffer, rising queue size graph, and growing consumer lag.
  * **Mitigation Strategies**: Bounded queue throttling, Producer rate-limiting, and Scaling Consumer Worker instances.
* **Important Labels**: `Producer Velocity (10k/s)`, `Consumer Throughput (2k/s)`, `Growing Queue Backlog`, `Consumer Lag`, `Bounded Buffer Throttling`, `Horizontal Consumer Scaling`.
