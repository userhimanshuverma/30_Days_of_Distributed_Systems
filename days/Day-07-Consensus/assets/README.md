# Day 7 Asset Specifications — Consensus: Why Voting Is Harder Than Elections

This directory specifies the required visual diagrams for **Day 7: Consensus**. These descriptions outline what each visual artifact communicates visually to reinforce the mental model without jumping ahead into deep protocol internals.

---

## 🖼️ 1. `board-meeting-analogy.png`
* **Title**: The Board Meeting Analogy — Chairperson vs. Voting Quorum
* **Visual Structure**:
  * **Left Side (Election)**: A room of board members raising hands to elect a Chairperson. Clear title: *"Electing a Chair is Easy (Leader Election)"*.
  * **Right Side (Proposal & Voting)**: The elected Chairperson holds up a document ("Acquire TechCorp for $50M"). Only 2 of 5 members are present/listening due to closed doors; 3 members are out of the room. A big red **STOP / REJECT** sign shows that the Chair cannot unilaterally bind the company without a quorum.
* **Key takeaway communicated**: Having a leader isn't enough; critical business decisions require a confirmed voting majority before taking effect.

---

## 🖼️ 2. `consensus-overview.png`
* **Title**: Distributed Consensus Lifecycle (Leader Proposal to Commit)
* **Visual Structure**:
  * **Leader Node**: Shows a designated Leader Node receiving an instruction from a client (`CREATE DEPLOYMENT web-app`).
  * **Broadcast Phase**: Arrows pointing from the Leader to 4 Follower Nodes carrying a "Proposal" packet.
  * **Response Phase**: 3 Followers return "ACK / YES", while 1 Follower returns a delayed/broken red arrow (Network Latency).
  * **Quorum Calculation**: A badge showing `4 / 5 ACKs >= Majority Threshold (3)`.
  * **Commit & Apply Phase**: Leader sends a "COMMIT" command, and all active nodes write the change into their state store simultaneously.
* **Key takeaway communicated**: Consensus is a multi-phase agreement loop ensuring every active machine moves to the exact same state together.

---

## 🖼️ 3. `majority-voting.png`
* **Title**: Quorum Safety & Partition Resiliency (3-Node vs. 5-Node Clusters)
* **Visual Structure**:
  * **Top Panel (5-Node Cluster)**: `Node A (Leader)`, `Node B`, `Node C`, `Node D`, `Node E`. A network lightning bolt severs `Node D` and `Node E`. `Nodes A, B, C` form a quorum of 3/5. Green checkmark: *"Progress Continues Safely"*.
  * **Bottom Panel (Minority Side)**: A isolated minority partition (`Node D`, `Node E`). Even if `Node D` tries to act as leader, it can only get 2/5 votes. Big red X: *"Proposals Blocked — Split-Brain Prevented"*.
* **Key takeaway communicated**: Majority quorums guarantee that only one partition can make progress, automatically preventing split-brain corruption.

---

## 🖼️ 4. `raft-visual.png`
* **Title**: Raft as a Practical Consensus Engine
* **Visual Structure**:
  * **High-Level Architectural View**: Shows a cluster box labeled *"Raft-Managed Cluster (e.g., etcd in Kubernetes)"*.
  * **Client Layer**: `kubectl` or Control Plane issuing commands to the Raft Leader.
  * **Raft Consensus Layer**: Highlights 3 conceptual steps inside Raft:
    1. Leader receives proposal.
    2. Leader replicates proposal to followers.
    3. Majority confirmation triggers commit across all nodes.
  * **State Machine Layer**: Below Raft, each node has a local state machine that strictly executes committed commands in sequence.
* **Key takeaway communicated**: Raft provides the practical algorithm that guarantees all nodes apply identical changes in identical order.
