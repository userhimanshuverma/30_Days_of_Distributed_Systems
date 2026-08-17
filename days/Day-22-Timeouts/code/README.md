# Day 22 Code — Timeouts & Deadline Budget Demo

This directory contains a self-contained, zero-dependency Python demonstration of **socket timeouts, request time budgets, deadline propagation, and deadline-bounded retries**.

---

## 🛠️ Files

- `timeout_demo.py`: Executable Python script demonstrating four production scenarios.

---

## 🚀 How to Run

No third-party packages or virtual environments are required. Use Python 3.8+:

```bash
python timeout_demo.py
```

---

## 💡 What the Demo Teaches

When you run `python timeout_demo.py`, it executes four distinct scenarios:

1. **Scenario 1: Fast Request within Budget**
   - Service A calls Service B with a 1.5s time budget. Service B responds in ~50ms.
   - Demonstrates successful execution within deadline limits.

2. **Scenario 2: Socket Read Timeout**
   - Service A calls Service B with a 1.0s budget. Service B takes 2.5s to respond.
   - Demonstrates how socket read timeouts abort client waiting at the exact budget boundary.

3. **Scenario 3: Service Chain Deadline Decay**
   - Service A performs 0.5s of local CPU work out of a 1.2s total request budget.
   - Service A dynamically updates the remaining budget to 0.7s before calling Service B.
   - Demonstrates that downstream timeouts must inherit the *remaining* budget rather than a static global config.

4. **Scenario 4: Deadline-Bounded Retries**
   - Demonstrates how client retry managers must check the remaining time budget before issuing retries or sleeping for exponential backoff.
   - Prevents retry loops from extending beyond the total client request deadline.
