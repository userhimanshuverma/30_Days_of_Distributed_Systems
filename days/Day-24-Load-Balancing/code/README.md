# Day 24 Code — Load Balancer Implementation & Interactive Demo

This directory contains a zero-dependency, self-contained Python implementation of an in-memory **Load Balancer** (`load_balancer.py`) alongside an interactive demonstration script (`demo.py`).

---

## 🛠️ Code Architecture

- **`load_balancer.py`**: Implementation of the `LoadBalancer` and `BackendServer` classes.
  - Manages registered backend servers and their operational status (`HEALTHY` vs `UNHEALTHY`).
  - Implements Round Robin, Least Connections, and Weighted Round Robin request distribution algorithms.
  - Automatically filters out unhealthy backends during traffic distribution.
  - Supports dynamic server addition/removal and active health check probes.
- **`demo.py`**: Executable demonstration script illustrating backend routing, failure isolation, and recovery.

---

## 🚀 How to Run

No third-party packages or virtual environments are required. Requires Python 3.8+:

```bash
python demo.py
```

---

## 💡 What the Demo Demonstrates

When you run `python demo.py`, it executes 5 distinct phases in sequence:

1. **Phase 1: Normal Operation (All 3 Servers Healthy)**
   - Requests arrive and are evenly distributed across `server-a`, `server-b`, and `server-c` in sequential Round Robin order (`a -> b -> c -> a -> b -> c`).
2. **Phase 2: Backend Outage (Server B Fails)**
   - `server-b` experiences an unhandled failure and is marked `UNHEALTHY`.
3. **Phase 3: Traffic Rerouting During Outage**
   - The load balancer dynamically skips `server-b` and routes incoming requests exclusively between `server-a` and `server-c` (`a -> c -> a -> c -> a -> c`).
4. **Phase 4: Backend Recovery & Re-integration**
   - `server-b` recovers and passes health checks. It is marked `HEALTHY` again.
5. **Phase 5: Traffic Resumption Across Full Pool**
   - The load balancer seamlessly re-integrates `server-b` into the active rotation without dropping requests or interrupting clients.
