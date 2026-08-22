# Day 27 Visual Assets Specification

This directory holds visual specifications and asset metadata for **Day 27 — How WhatsApp Delivers Billions of Messages**.

> [!NOTE]
> This specification defines the exact visual layout, topology, labels, data flow, color coding, and aesthetic requirements for visual assets representing large-scale distributed real-time messaging systems.

---

## 🎨 Visual Design System & Aesthetics

All diagrams for Day 27 follow the course visual language:
- **Canvas & Theme**: Modern dark slate mode (`#0F172A` / `#1E293B`) with high-contrast typography, glowing neon routing vectors, and translucent glassmorphism containers.
- **Color Palette**:
  - **Connection Tier & Sockets**: Emerald Green (`#10B981`) and Cyber Teal (`#14B8A6`).
  - **Routing & Discovery Layer**: Royal Blue (`#3B82F6`) and Deep Indigo (`#6366F1`).
  - **Offline Storage & Persistence**: Warm Amber (`#F59E0B`) and Flame Orange (`#F97316`).
  - **Acknowledgement States (Single / Double / Blue Ticks)**: Slate Gray (`#64748B`), Emerald Green (`#10B981`), and Electric Cyan (`#06B6D4`).
  - **Disconnects / Failure Modes**: Crimson Red (`#EF4444`).
- **Containers**: Translucent glass cards with rounded corners (`12px`), 1px subtle glow borders, and clean title badges.
- **Typography**: Clean sans-serif (Inter / Roboto / Outfit), bold hierarchical titles, and minimum 14pt readable labels.

---

## 📐 Required Asset Specifications

### 1. `messaging-overview.png`

* **Title Header**: "High-Level End-to-End Real-Time Messaging Architecture"
* **Goal**: Illustrate the complete architectural flow connecting a sender client, connection gateways, user routing lookups, offline storage queues, and a recipient client.
* **Intended Teaching Point**: Decouple the sender's client connection from the recipient's client connection. Highlight that sending a message and delivering a message are distinct asynchronous events separated by infrastructure state.
* **Layout**:
  - **Left (Sender Side)**: `Sender App (Alice)` connected via persistent TCP/TLS WebSocket to `Gateway Server A`.
  - **Center (Routing & Core Infrastructure)**:
    - `Gateway Server A` ──▶ `User Routing Table (Directory / Cache)` (Query: "Where is Bob?").
    - Decision Split:
      - **Branch 1 (Online)**: Direct push to `Gateway Server Z` ──▶ `Recipient App (Bob)`.
      - **Branch 2 (Offline)**: Store message in `Offline Store Queue` until reconnect.
  - **Right (Recipient Side)**: `Gateway Server Z` connected to `Recipient App (Bob)`.

---

### 2. `online-offline-delivery.png`

* **Title Header**: "Immediate Direct Push vs. Store-and-Forward Delivery"
* **Goal**: Contrast the execution flow when the recipient is actively online versus when the recipient is temporarily disconnected or offline.
* **Intended Teaching Point**: Demonstrates how persistent connection state determines whether a message takes the low-latency fast path (direct socket push) or the durable slow path (temporary persistence queue followed by reconnection flushing).
* **Layout**: 2-Column Side-by-Side Comparison:
  - **Left Column ("Online Recipient — Direct Push Path")**:
    - `Sender` ──▶ `Server` ──(Active TCP Socket found)──▶ `Recipient Device`.
    - Latency: < 50 ms.
    - Status: Fast-path delivery.
  - **Right Column ("Offline Recipient — Store & Forward Path")**:
    - `Sender` ──▶ `Server` ──(No active connection)──▶ `Offline Storage (RocksDB / Queue)`.
    - Recipient powers on / reconnects ──▶ TCP Socket handshake ──▶ Server flushes pending queue ──▶ `Recipient Device`.
    - Latency: Asynchronous (minutes/hours/days).

---

### 3. `message-lifecycle.png`

* **Title Header**: "The 4 Distinct States of Message Delivery & Acknowledgements"
* **Goal**: Clearly map the progress of a message through every state in its lifecycle alongside the corresponding client/server state changes.
* **Intended Teaching Point**: Explain why seeing "sent" on a sender device does not guarantee delivery, and how acknowledgements flow back asynchronously to update sender state.
* **Layout**: Horizontal Pipeline showing 4 key stages:
  1. **Stage 1 (Client Sent)**: Message created locally on client device, buffered in client queue.
  2. **Stage 2 (Accepted by Infrastructure / Server ACK)**: Server validates payload, generates message ID, persists to write buffer, sends `ACK` to sender (Single Tick ✓).
  3. **Stage 3 (Delivered to Target Device / Recipient ACK)**: Socket pushes payload to recipient phone, recipient OS receives payload and dispatches `DELIVERED_ACK` back to server (Double Ticks ✓✓).
  4. **Stage 4 (Read by User / App ACK)**: Recipient opens app conversation view, dispatches `READ_ACK` back to server (Blue Double Ticks ✓✓).

---

### 4. `distributed-routing.png`

* **Title Header**: "Distributed User Routing Across Decoupled Gateway Servers"
* **Goal**: Show how a system routes messages between users connected to completely different physical servers across the globe.
* **Intended Teaching Point**: Individual connection servers only hold sockets for their connected users. Inter-server message delivery relies on a central or distributed routing lookup (e.g., distributed hash table, Redis session cache, or ephemeral routing service).
* **Layout**:
  - **Nodes & Sockets**:
    - `Alice (NYC)` connected to `Gateway Server A (US-East)`.
    - `Bob (London)` connected to `Gateway Server Z (EU-West)`.
  - **Routing Mechanism**:
    - `Gateway Server A` receives message from Alice targeted to `Bob`.
    - `Gateway Server A` queries `Distributed Session Registry / Cache`.
    - Registry returns: `"Bob is currently connected to Gateway Server Z (IP: 192.168.1.50)"`.
    - `Gateway Server A` forwards message internally to `Gateway Server Z`.
    - `Gateway Server Z` pushes message over existing socket to `Bob`.
