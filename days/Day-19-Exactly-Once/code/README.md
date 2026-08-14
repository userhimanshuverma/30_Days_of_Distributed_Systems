# Day 19 — Code: Hands-on Idempotency & Failure Simulation

This directory contains executable Python scripts demonstrating why "exactly once" is an end-to-end guarantee requiring client-side identity and server-side deduplication rather than a raw network delivery property.

---

## Files

* [`idempotent_payment.py`](file:///d:/30_Days_of_Distributed_Systems/days/Day-19-Exactly-Once/code/idempotent_payment.py)
  * Implements an **Idempotent Payment Processor** and an in-memory **Transactional State Store**.
  * Demonstrates atomic state transition (`process request` + `record idempotency key`) using thread locks.
  * Protects against race conditions from concurrent duplicate requests and replays cached HTTP payload responses for duplicate keys.

* [`retry_simulation.py`](file:///d:/30_Days_of_Distributed_Systems/days/Day-19-Exactly-Once/code/retry_simulation.py)
  * Runs an interactive failure simulation comparing **Naive Non-Idempotent Retries** vs. **Idempotent Retries**.
  * Simulates a lost HTTP response over a faulty network path, forcing the client to time out and retry.
  * Proves how blind retries cause double-charging (INR 2,000 deducted), whereas idempotent retries achieve an **effectively-once** logical outcome (INR 1,000 deducted).

---

## How to Run

Execute the simulation directly using standard Python 3 (no external dependencies required):

```bash
python retry_simulation.py
```

### Expected Output Summary
1. **Experiment 1 (Non-Idempotent)**: The client retries after a network drop. The server processes the payment twice, deducting ₹2,000 instead of ₹1,000.
2. **Experiment 2 (Idempotent)**: The client retries with the same `idempotency_key`. The server detects the key, skips balance deduction, and returns the original cached response.
