# Day 23 Visual Assets Specification

This directory holds visual specifications and asset placeholders for **Day 23 — Circuit Breakers: Failure Containment & Cascading Isolation**.

> [!NOTE]
> Do not generate raw binary image files directly. This specification defines the exact visual layout, topology, labels, and aesthetic requirements for diagrams to be created.

---

## 🎨 Visual Design System & Aesthetics

All diagrams for Day 23 follow the course visual language:
- **Palette**: Dark canvas (`#0F172A` / `#1E293B`) with royal purple (`#8B5CF6`), bright violet (`#A78BFA`), crisp cyan (`#06B6D4`), dark amber (`#F59E0B`), and alert red (`#EF4444`) accents.
- **Typography**: Clean sans-serif (Inter or Outfit), high contrast, large bold header titles, minimum 14pt body labels.
- **Icons**: Minimal vector icons for Client, Microservice API, Circuit Breaker Switch, Database, and Thread Pool.
- **Style**: Modern dark mode, subtle glassmorphism card containers, rounded corners, soft drop shadows, glowing vector flow arrows.

---

## 📐 Required Asset Specifications

### 1. `cascading-failure.png`

* **Title Header**: "The Anatomy of a Cascading Failure (Unprotected Architecture)"
* **Goal**: Visualize step-by-step how a single degraded downstream database exhausts thread pools upstream and brings down healthy services.
* **Layout**: Horizontal multi-tier call chain from left to right:
  `[ Client Requests ] ──► [ Service A (API Gateway) ] ──► [ Service B (Auth/Fraud) ] ──► [ Unhealthy Database ]`
* **Visual Components**:
  - **Client Requests (Left)**: Surge of incoming red arrow vectors representing incoming user HTTP requests (`1,000 req/sec`).
  - **Service A Card (Middle Left)**: Dark slate container labeled "Service A (Healthy Code)". Inside, show worker thread pool completely filled with blocked red threads (`Worker Threads: 500/500 Occupied (100%)`). Show socket read queue spilling over (`Listen Queue Full -> Dropping SYN Packets`).
  - **Service B Card (Middle Right)**: Orange warning card labeled "Service B (Slow Response)". Show high latency badge (`Latency: 45,000ms`).
  - **Database (Right)**: Red flashing node labeled "Database (Row Locked / GC Freeze)".
  - **Failure Callout Banner (Bottom)**: "🔥 Unbounded waiting transforms a localized downstream delay into a global catastrophic failure."
* **Color Palette**: Dark background, crimson red failure paths, amber latency callouts, dark purple service containers.

---

### 2. `circuit-breaker-states.png`

* **Title Header**: "The 3-State Finite State Machine Model"
* **Goal**: Present a clean state machine diagram detailing state transitions, triggering conditions, and request routing behavior.
* **Layout**: Circular / Triangular state diagram connecting three prominent state nodes:
  - **Top-Left Node: `CLOSED` State** (Emerald Green Card)
    - Subtitle: "Normal Operation"
    - Details: "Requests allowed normally. Failure rate & latency monitored continuously."
  - **Right Node: `OPEN` State** (Vibrant Red Card)
    - Subtitle: "Trip State (Short-Circuit)"
    - Details: "Threshold crossed. Outbound calls blocked fast. Instant fallback execution."
  - **Bottom-Center Node: `HALF-OPEN` State** (Amber Yellow Card)
    - Subtitle: "Controlled Probe Trial"
    - Details: "Recovery window elapsed. Single trial request allowed to test dependency health."
* **Transition Arrows & Labels**:
  - `CLOSED ─── (Failure Threshold Reached) ───► OPEN`: Bold red arrow.
  - `OPEN ─── (Recovery Timeout Window Elapses) ───► HALF-OPEN`: Curved amber arrow labeled "Wait Window (e.g. 5s)".
  - `HALF-OPEN ─── (Trial Request Succeeds) ───► CLOSED`: Green return arrow labeled "Probe Success".
  - `HALF-OPEN ─── (Trial Request Fails) ───► OPEN`: Red re-tripping arrow labeled "Probe Failure".
* **Visual Style**: Sleek dark mode card layout, high-contrast state badges, glowing transition paths.

---

### 3. `protected-service-flow.png`

* **Title Header**: "Protected Service Request Lifecycle"
* **Goal**: Show how incoming traffic is handled depending on the current circuit breaker state, highlighting the fast failure path.
* **Layout**: Flowchart diagram splitting incoming traffic:
  ```text
                                 ┌── [CLOSED] ──► Call Dependency ─┬─ Success ─► Return 200 OK
  [ Client Request ] ──► [ Circuit Breaker ]                       └─ Failure ─► Record & Fallback
                                 ├── [OPEN] ────► Fast Short-Circuit ───► Instant Fallback (503 / Cached)
                                 └── [HALF-OPEN]─► Limited Trial Request ─┬─ Success ─► Close Circuit
                                                                         └─ Failure ─► Re-Open Circuit
  ```
* **Visual Components**:
  - **Input Node**: "Incoming Client Request".
  - **Decision Switch**: Central circuit breaker box with an animated-style switch mechanism.
  - **Branch 1 (Green)**: Closed circuit path leading directly to `Service B`.
  - **Branch 2 (Red - Short-Circuit)**: Open circuit path short-circuiting immediately to `Fallback Handler` (skipping network hop completely).
  - **Branch 3 (Amber - Probe)**: Half-Open trial path passing 1 test request while holding other incoming traffic.
* **Visual Style**: Purple/cyan glowing lines, bold decision diamonds, clear response status badges (`200 OK` vs `503 Short-Circuited` vs `200 Degraded Fallback`).

---

### 4. `recovery-flow.png`

* **Title Header**: "Controlled Recovery & Half-Open Probe Flow"
* **Goal**: Illustrate why the system does not immediately flood a recovering dependency with 100% traffic, showing step-by-step probe execution.
* **Layout**: Timeline sequence diagram contrasting two recovery strategies:
  - **Top Timeline (Naive Recovery - Traffic Storm)**:
    - `OPEN -> Sudden Full Traffic (10,000 req/sec) -> Downstream Crashes Again`. Shown with red explosive shockwave icon.
  - **Bottom Timeline (Controlled Circuit Breaker Recovery)**:
    - `OPEN (Timer: 5.0s)` -> `Transition HALF-OPEN` -> `1 Probe Request Sent` -> `Probe ACK (20ms)` -> `Transition CLOSED` -> `Normal Traffic Resumes`.
* **Key Callout Box**: "⚡ Half-Open prevents 'Recovery Storms' by testing downstream health before releasing full load."
* **Visual Style**: Clean dark background, purple and cyan timeline markers, crisp step labels, side-by-side comparative layout.
