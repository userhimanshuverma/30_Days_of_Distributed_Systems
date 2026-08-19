# Day 24 Visual Assets Specification

This directory holds visual specifications and asset placeholders for **Day 24 — Load Balancers: Traffic Distribution & Health-Aware Routing**.

> [!NOTE]
> Do not generate raw binary image files directly. This specification defines the exact visual layout, topology, labels, and aesthetic requirements for diagrams to be created.

---

## 🎨 Visual Design System & Aesthetics

All diagrams for Day 24 follow the course visual language:
- **Canvas & Layout**: Modern dark slate mode (`#0F172A` / `#1E293B`) with high-contrast text and glowing vector paths.
- **Palette**: Primary royal purple (`#8B5CF6`), bright violet (`#A78BFA`), crisp cyan (`#06B6D4`), success emerald (`#10B981`), amber warning (`#F59E0B`), and crimson red (`#EF4444`).
- **Containers**: Glassmorphism cards with rounded corners (`12px`), 1px subtle border glow, dark translucent fills.
- **Typography**: Clean sans-serif (Inter / Outfit), bold title headers, clear minimum 14pt label text.
- **Icons**: Minimal vector icons for Client Devices, Load Balancer Traffic Router, Backend Servers (Server A, B, C), and Health Check Probes.

---

## 📐 Required Asset Specifications

### 1. `load-balancer-architecture.png`

* **Title Header**: "Load Balancer Architecture & Entry Point Abstraction"
* **Goal**: Illustrate how clients communicate exclusively with a single load balancer entry point (IP/DNS), decoupling client applications from physical backend topology.
* **Intended Teaching Point**: A load balancer hides infrastructure complexity; clients send requests to one service endpoint, while the load balancer decides backend routing behind the scenes.
* **Layout**:
  - **Left Section (Clients)**: Cluster of client devices (Mobile, Web Browser, API Client) pointing to a single public endpoint (`https://api.example.com` / `VIP: 192.0.2.1`).
  - **Center Section (Load Balancer)**: Elevated royal purple glass card labeled "Load Balancer Layer (Reverse Proxy / L7 Router)". Highlights the internal routing engine and health status registry.
  - **Right Section (Backend Server Fleet)**: Three parallel backend server containers:
    - `Server A (10.0.0.10:8080)` - Active State (Cyan border)
    - `Server B (10.0.0.11:8080)` - Active State (Cyan border)
    - `Server C (10.0.0.12:8080)` - Active State (Cyan border)
* **Arrows & Connections**:
  - Glowing violet arrow from Clients to Load Balancer labeled "Public HTTPS Request".
  - Three distinct cyan distribution arrows fanning out from Load Balancer to Servers A, B, and C labeled "Internal VPC Forwarding".

---

### 2. `traffic-distribution.png`

* **Title Header**: "Request Routing Algorithms & Traffic Distribution Patterns"
* **Goal**: Graphically compare Round Robin, Weighted Routing, and Least Connections traffic distribution mechanisms.
* **Intended Teaching Point**: Different load balancing algorithms utilize different system signals (sequential order, machine capacity weight, or active request depth) to distribute workload.
* **Layout**: 3-panel side-by-side comparative layout:
  - **Panel A: Round Robin**
    - Label: "Sequential Equal Distribution"
    - Flow: Client Requests `R1, R2, R3, R4` mapped sequentially: `R1 -> Server A`, `R2 -> Server B`, `R3 -> Server C`, `R4 -> Server A`.
    - Server States: Equal load badges (`33% / 33% / 33%`).
  - **Panel B: Weighted Round Robin**
    - Label: "Capacity-Aware Distribution"
    - Server Specs: `Server A (Weight: 50% - 16-Core CPU)`, `Server B (Weight: 30% - 8-Core CPU)`, `Server C (Weight: 20% - 4-Core CPU)`.
    - Server States: Proportional traffic badges (`50% / 30% / 20%`).
  - **Panel C: Least Connections**
    - Label: "Active Workload Distribution"
    - Server States: `Server A (Active: 12 req - Heavy)`, `Server B (Active: 2 req - Idle -> Targeted)`, `Server C (Active: 8 req - Medium)`.
    - Arrow: Prominent green targeted arrow pointing incoming request directly to `Server B` (lowest connection count).

---

### 3. `health-aware-routing.png`

* **Title Header**: "Health-Aware Routing & Automatic Outage Isolation"
* **Goal**: Visualizing active health check probing, bad backend removal, and zero-downtime recovery.
* **Intended Teaching Point**: Reachability does not equal application health; a load balancer must actively probe application endpoints and divert traffic away from degraded backends.
* **Layout**: 2-stage vertical flow (Before vs After Outage):
  - **Stage 1: Active Health Checking**
    - Load Balancer sends periodic HTTP probes (`GET /healthz`) down to backends.
    - `Server A`: `HTTP 200 OK` (Green checkmark `✓`)
    - `Server B`: `HTTP 500 Error / Socket Timeout` (Red warning `✗`)
    - `Server C`: `HTTP 200 OK` (Green checkmark `✓`)
  - **Stage 2: Dynamic Routing Table Update**
    - Routing Table Box showing `Server B` status updated to `UNHEALTHY (Removed from Rotation)`.
    - Incoming client arrows automatically split `50% / 50%` between `Server A` and `Server C`.
    - Red dashed arrow from Load Balancer to `Server B` labeled "Traffic Blocked / Probe Retries Only".

---

### 4. `horizontal-scaling.png`

* **Title Header**: "Horizontal Scaling Transformation: Single Bottleneck to Elastic Fleet"
* **Goal**: Demonstrate the transformation from a single overloaded server to a horizontally scaled architecture enabled by a load balancer.
* **Intended Teaching Point**: Horizontal scaling provides physical compute capacity, but the load balancer provides the single-service abstraction that makes multiple machines work as one.
* **Layout**: Before-and-After Split Screen:
  - **Left Side ("Before: Vertical Constraint")**:
    - `Clients (10,000 req/sec) ──► Single Server (100% CPU / Memory Exhausted / Dropping Requests)`.
    - Red flame icon callout: "Single Point of Failure & Hard Capacity Ceiling".
  - **Right Side ("After: Horizontal Fleet + Load Balancer")**:
    - `Clients (10,000 req/sec) ──► Load Balancer ──► [Server A | Server B | Server C | Server D]`.
    - Server Fleet Container showing autoscaling indicator (`+ Server D dynamically added`).
    - Green status callout: "Elastic Scale & Failure Resilience: Individual Server Crash Has Zero Client Impact".
