# Day 14 Visual Assets Specification

This directory holds visual specifications and asset placeholders for **Day 14 — Quorums: Why 2 of 3 Votes Matter**.

---

## 🎨 Required Asset Specifications

### 1. `three-replica-quorum.png`
* **Description**: Visual introduction to a 3-replica cluster and the concept of majority quorum voting ($2$ out of $3$ votes).
* **Layout**:
  * **Top Header**: "Total Replicas ($N = 3$) — Quorum Threshold ($W = 2$)"
  * **Center Nodes**: Three clean server node cards labeled **Replica A**, **Replica B**, and **Replica C**.
  * **Vote Highlights**: Replica A and Replica B show glowing green checkmarks ("ACK Vote 1", "ACK Vote 2"). Replica C is inactive or pending ("Unneeded / Slow").
  * **Summary Badge**: "Quorum Reached: 2 / 3 Votes Received -> Operation Committed".
* **Color Palette**: Premium white background, deep indigo node outlines, vibrant emerald checkmarks, soft shadows.

---

### 2. `quorum-overlap.png`
* **Description**: Visual proof of the Quorum Intersection Formula ($W + R > N$).
* **Layout**:
  * **Top Row (WRITE Set, $W = 2$)**: Shows Replica A (✓) and Replica B (✓) highlighted in dark purple. Replica C is grayed out.
  * **Bottom Row (READ Set, $R = 2$)**: Shows Replica A (✓) and Replica C (✓) highlighted in bright violet. Replica B is grayed out.
  * **Intersection Highlight**: Vertical glowing column highlighting **Replica A** as the overlapping node present in both sets.
  * **Callout Box**: "$W + R > N \implies 2 + 2 = 4 > 3$. Replica A guarantees the reader sees the latest write!"
* **Color Palette**: Royal purple write shading, magenta read shading, bright golden/amber overlap glow on white background.

---

### 3. `failed-replica.png`
* **Description**: Quorum fault tolerance demonstrating continuous availability despite replica node failure.
* **Layout**:
  * **Nodes Display**: 3 Replicas (A, B, C).
  * **Node C**: Red skull icon / cross mark ("OFFLINE / NETWORK PARTITION").
  * **Nodes A & B**: Active and responding ("ACK 1", "ACK 2").
  * **Client Box**: Receives $2$ ACKs out of $3$. Quorum ($W=2$) satisfied -> Operation succeeds seamlessly without waiting for Node C.
* **Color Palette**: Crimson red for failed node, emerald green for successful ACKs, soft purple client container.

---

### 4. `quorum-sizes.png`
* **Description**: Comparative diagram showcasing quorum threshold rules for $N=3$ vs. $N=5$ replica sets.
* **Layout**: Side-by-side comparison boxes:
  * **Left Box ($N = 3$)**:
    * 3 Server icons (A, B, C).
    * Majority Quorum ($Q = \lfloor 3/2 \rfloor + 1 = 2$).
    * Fault Tolerance: Tolerates $1$ node failure ($F = 1$).
  * **Right Box ($N = 5$)**:
    * 5 Server icons (A, B, C, D, E).
    * Majority Quorum ($Q = \lfloor 5/2 \rfloor + 1 = 3$).
    * Fault Tolerance: Tolerates $2$ node failures ($F = 2$).
* **Color Palette**: Clean white card background, deep purple typography, soft grey server frames, vivid green status pills.
