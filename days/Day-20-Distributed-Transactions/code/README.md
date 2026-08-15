# Day 20 — Code: Hands-on Distributed Transactions & Failure Simulations

This directory contains executable Python scripts demonstrating why distributed transactions across independent services/databases fail, how **Two-Phase Commit (2PC)** attempts atomic coordination, and how the **Saga Pattern** uses compensating transactions for business-level recovery.

---

## Files

* [`distributed_transfer.py`](file:///d:/30_Days_of_Distributed_Systems/days/Day-20-Distributed-Transactions/code/distributed_transfer.py)
  * Simulates naive distributed transfers across two isolated database services (`Database_1` and `Database_2`).
  * Demonstrates how network failures between calls leave system state inconsistent (e.g., money debited from Account A but never credited to Account B).
  * Proves why naive local `try-except` blocks fail when compensating error-handling calls themselves drop over the wire.

* [`two_phase_commit.py`](file:///d:/30_Days_of_Distributed_Systems/days/Day-20-Distributed-Transactions/code/two_phase_commit.py)
  * Implements a full **Two-Phase Commit (2PC)** protocol simulation with a Coordinator, Participants, and Write-Ahead Logging (WAL).
  * Demonstrates Phase 1 (`PREPARE`), Phase 2 (`COMMIT` / `ABORT`), and resource locking.
  * Features a failure mode simulation showing **Coordinator Crash After Prepare**, illustrating why participants become uncertain and blocked indefinitely holding locks.

* [`saga_transfer.py`](file:///d:/30_Days_of_Distributed_Systems/days/Day-20-Distributed-Transactions/code/saga_transfer.py)
  * Implements a **Saga Workflow Orchestrator** executing distributed transactions as a sequence of independent local commits.
  * Demonstrates automatic **Compensating Transactions** (business refunds) triggered when a downstream step fails.
  * Simulates transient compensation failures and resolves them via **Idempotent Retries**, illustrating forward recovery without global database locks.

---

## How to Run

Execute each simulation directly using Python 3 (standard library only, no external dependencies required):

```bash
python distributed_transfer.py
python two_phase_commit.py
python saga_transfer.py
```

### Expected Output Summary
1. **`distributed_transfer.py`**: Shows total system balance dropping from ₹15,000 to ₹13,000 upon network failure, highlighting the lack of distributed atomicity.
2. **`two_phase_commit.py`**: Shows atomic commit, atomic abort, and the blocking state where participants hold locks indefinitely when the coordinator crashes mid-flight.
3. **`saga_transfer.py`**: Shows how local commits mutate state immediately and how compensating actions refund debits idempotently upon downstream failure.
