# Day 23 Code — Circuit Breaker Implementation & Demo

This directory contains a zero-dependency, self-contained Python implementation of the **Circuit Breaker** stability pattern (`circuit_breaker.py`) alongside an interactive demonstration script (`demo.py`).

---

## 🛠️ Code Architecture

- **`circuit_breaker.py`**: Implementation of the 3-state state machine (`CLOSED`, `OPEN`, `HALF-OPEN`).
  - Manages failure count thresholds and recovery timeouts.
  - Short-circuits outbound remote calls when in `OPEN` state.
  - Automatically routes execution to fallback handlers when available.
  - Manages probe request execution during `HALF-OPEN` recovery state.
- **`demo.py`**: Executable script demonstrating 5 real-world scenarios in sequence.

---

## 🚀 How to Run

No third-party packages or virtual environments are required. Use Python 3.8+:

```bash
python demo.py
```

---

## 💡 What the Demo Demonstrates

When you run `python demo.py`, it executes 5 distinct scenarios:

1. **Healthy Operation (`CLOSED` State)**:
   - Requests pass directly to the dependency. Successes keep failure counters at 0.
2. **Failure Threshold Tripping (`CLOSED` -> `OPEN`)**:
   - Simulated service outages cause consecutive connection failures.
   - Reaching the failure threshold (3 consecutive errors) immediately trips the circuit to `OPEN`.
3. **Fast Short-Circuiting & Fallbacks (`OPEN` State)**:
   - Subsequent calls are blocked **before** touching the network.
   - Fallback handlers execute instantly, saving worker threads and socket pools from waiting on timeouts.
4. **Successful Recovery Probe (`OPEN` -> `HALF-OPEN` -> `CLOSED`)**:
   - After the recovery timeout window (2.0s) elapses, the circuit transitions to `HALF-OPEN`.
   - A single trial request is permitted through. Upon downstream success, the circuit closes (`CLOSED`).
5. **Unsuccessful Recovery Probe (`HALF-OPEN` -> `OPEN`)**:
   - If the downstream dependency is still unhealthy when probed in `HALF-OPEN`, a single failure immediately re-trips the circuit back to `OPEN` for another full recovery window.
