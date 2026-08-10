# Day 15 Visual Assets Specification

This directory holds visual specifications and asset placeholders for **Day 15 — Eventual Consistency: Why Your Instagram Like Appears Later**.

---

## 🎨 Required Asset Specifications

### 1. `replication-delay.png`
* **Description**: Visualizing asynchronous propagation delay as a write payload travels from entry Replica A across network channels to secondary Replicas B and C.
* **Layout**:
  * **Top Canvas Header**: "Asynchronous Replication Latency ($t_0 \rightarrow t_n$)"
  * **Timeline View**: Horizontal propagation vectors originating from Replica A.
  * **Node A**: Highlighted in dark violet with an incoming write packet (`POST /like`).
  * **Network Channels**: Dotted animated vectors pointing from Replica A to Replica B ($+120\text{ms}$) and Replica C ($+340\text{ms}$).
  * **Node B & Node C**: Rounded server cards displaying buffer queues with pending replication packets.
* **Visual Style**: Premium white background, deep purple accent vectors, soft card shadows, clean network latency badges ($+120\text{ms}$, $+340\text{ms}$).

---

### 2. `temporary-divergence.png`
* **Description**: Visualizing the state matrix during the active replication window, demonstrating temporary replica disagreement.
* **Layout**:
  * **Top Canvas Header**: "Temporary State Divergence Window"
  * **State Cards**:
    * **Replica A (Entry)**: Solid purple card with filled red heart (`❤️ status: True`).
    * **Replica B (In-Flight)**: Soft lavender card with outlined heart (`♡ status: False`, processing queue).
    * **Replica C (Lagging)**: Soft grey card with outlined heart (`♡ status: False`, replication delayed).
  * **Divergence Callout Banner**: "⚠️ Replicas disagree temporarily due to asynchronous propagation. System is NOT broken."
* **Visual Style**: High-contrast state cards, royal purple primary accents, pastel warning banners, crisp status badges.

---

### 3. `eventual-convergence.png`
* **Description**: Visualizing full cluster state convergence after all replication queues drain and background updates cease.
* **Layout**:
  * **Top Canvas Header**: "Eventual Convergence ($t_{\text{final}}$: All Updates Applied)"
  * **State Cards**:
    * **Replica A**: Solid purple card with filled red heart (`❤️ status: True`).
    * **Replica B**: Solid purple card with filled red heart (`❤️ status: True`).
    * **Replica C**: Solid purple card with filled red heart (`❤️ status: True`).
  * **Convergence Highlight**: Glowing emerald checkmark banner connecting all three nodes: "$A = B = C \implies \text{Cluster Converged}$".
* **Visual Style**: Premium white canvas, emerald green success accents, deep purple node highlights, clean 16:9 layout.

---

### 4. `user-observation.png`
* **Description**: Dual-user view showing why Alice sees her own like immediately while Bob connected to a lagging replica sees stale state.
* **Layout**:
  * **Left Side (User Alice)**: Client phone screen displaying "Post Liked ❤️", connected via solid blue ray to **Replica A** (`status: True`).
  * **Right Side (User Bob)**: Client phone screen displaying "Post Unliked ♡", connected via solid orange ray to **Replica C** (`status: False`).
  * **Center Cluster**: Replicas A, B, and C with asynchronous propagation arrows between them.
  * **Callout Box**: "Different client routing to different replicas yields different temporary observations."
* **Visual Style**: Sleek mobile device frames, vibrant directional rays, soft node drop shadows, large readable typography.

---

### 5. `consistency-spectrum.png`
* **Description**: Spectrum diagram illustrating engineering trade-offs between stale-tolerant high-scale workloads and strict correctness workloads.
* **Layout**:
  * **Horizontal Spectrum Axis**: Gradient arrow going from **Eventual Consistency** (Left) to **Strong Consistency** (Right).
  * **Left Anchor (High Scale / Low Latency)**: Social Media Likes, Activity Feeds, Product Recommendations, Search Indexing.
  * **Middle Anchor (Balanced)**: Session Stores, User Profiles, Shopping Carts.
  * **Right Anchor (Strict Correctness)**: Bank Balances, Payment Processing, Hotel/Flight Reservations, Inventory Checkout.
  * **Key Metrics Bar**: Annotations showing Latency (increases left to right) vs. Availability (decreases left to right).
* **Visual Style**: Smooth gradient spectrum line (Violet to Deep Royal Blue), rounded white workload cards, minimal text hierarchy.
