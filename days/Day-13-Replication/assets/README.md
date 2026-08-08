# Day 13 Visual Assets Specification

This directory holds visual specifications and asset placeholders for **Day 13 — Replication: Primary, Secondary, Multi-Leader, and Leaderless**.

---

## 🎨 Required Asset Specifications

### 1. `replication-models.png`
* **Description**: A comprehensive side-by-side comparison diagram depicting the three primary replication architectures.
* **Layout**: Three vertical columns:
  * **Left Column (Primary / Secondary)**: Client write going to one central Primary node, with one-way arrows propagating data to two read-only Secondary replicas.
  * **Middle Column (Multi-Leader)**: Client writes going to two regional Leader nodes (Leader A and Leader B), with bidirectional replication arrows connecting the two leaders.
  * **Right Column (Leaderless)**: Client writes being broadcast directly to three peer Replica nodes without any single leader.
* **Color Palette**: 
  * Primary / Secondary: Blue primary node, sky blue secondary nodes.
  * Multi-Leader: Purple and Indigo leader nodes.
  * Leaderless: Teal peer nodes.

---

### 2. `primary-secondary.png`
* **Description**: Detailed architecture diagram of a Primary / Secondary (Leader / Follower) system.
* **Components**:
  * **Client App**: Sends write requests (`UPDATE user SET status = 'ACTIVE'`) to the Primary Node.
  * **Primary Node**: Single write coordinator holding Write-Ahead Log (WAL) and main data store.
  * **Secondary Node 1 (Synchronous)**: Immediate block/ack loop with Primary before returning write success to client.
  * **Secondary Node 2 (Asynchronous)**: Receives updates asynchronously via background replication stream.
  * **Read Clients**: Routing read traffic exclusively to secondaries to offload read pressure from the primary.

---

### 3. `multi-leader.png`
* **Description**: Multi-region Multi-Leader replication flow demonstrating write handling and cross-datacenter synchronization.
* **Components**:
  * **US East Datacenter**: Client writes to Leader Node A (`city = "Delhi"`).
  * **EU West Datacenter**: Client writes to Leader Node B (`city = "Bangalore"`).
  * **Cross-Region Network**: Asynchronous replication link connecting Leader A and Leader B.
  * **Conflict Resolution Box**: Highlights concurrent writes for the same record key and shows conflict detection and resolution (e.g., Last-Write-Wins rule).

---

### 4. `leaderless.png`
* **Description**: Leaderless (Dynamo-style) cluster processing a write request across peer replicas.
* **Components**:
  * **Client / Coordinator Node**: Sends write request broadcast directly to all 3 cluster replicas (Replica 1, Replica 2, Replica 3).
  * **Replica Nodes**: Equal peers. Replica 1 and Replica 2 respond immediately with `ACK`, fulfilling the Write Quorum requirement ($W=2$).
  * **Replica 3 (Slow / Degraded)**: Delayed ACK showing that the system accepts the write without waiting for 100% node availability.

---

### 5. `replication-vs-sharding.png`
* **Description**: A clear side-by-side visualization contrasting dataset partitioning (Sharding) versus dataset duplication (Replication).
* **Top Half (Sharding)**:
  * Dataset broken into Shard A (Users 1–1000) and Shard B (Users 1001–2000), located on separate machines.
  * Formula: **Sharding = Divide the Dataset**.
* **Bottom Half (Replication)**:
  * Full Dataset copied identically onto Node 1, Node 2, and Node 3.
  * Formula: **Replication = Copy the Dataset**.
* **Combined Model**:
  * Displays Shard A with 2 replicas, and Shard B with 2 replicas, demonstrating how real production systems use both together.

---

### 6. `replication-lag.png`
* **Description**: Timeline sequence diagram illustrating replication lag between a Primary and Asynchronous Secondary nodes.
* **Timeline Flow**:
  * **Time $t_0$**: Client issues write (`Set tier = 'PLATINUM'`) to Primary.
  * **Time $t_1$**: Primary acknowledges write to client. Primary data updated.
  * **Time $t_2$**: Client reads from Secondary 2. Secondary 2 has not received update yet -> Returns stale data (`tier = 'FREE'`).
  * **Time $t_3$**: Replication packet arrives at Secondary 2 -> Secondary 2 catches up.
