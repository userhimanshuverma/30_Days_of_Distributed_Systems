"""
distributed_transfer.py — Failure simulation demonstrating non-atomic distributed transactions.

Demonstrates:
1. Scenario 1: A successful bank transfer across two independent databases.
2. Scenario 2: Network/System failure after debiting Account A but before crediting Account B (Inconsistent State).
3. Scenario 3: Naive local try-except rollback failure when the compensating/rollback operation itself drops over the network.
"""

import sys
import time
import random
from typing import Dict

# Ensure stdout handles UTF-8 formatting cleanly on Windows terminals
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class IndependentDatabase:
    """Simulates an isolated database instance representing a distinct service/shard."""
    def __init__(self, name: str):
        self.name = name
        self.balances: Dict[str, float] = {}
        self.network_failure_rate: float = 0.0

    def get_balance(self, account_id: str) -> float:
        return self.balances.get(account_id, 0.0)

    def set_balance(self, account_id: str, balance: float):
        self.balances[account_id] = balance

    def debit(self, account_id: str, amount: float) -> bool:
        if random.random() < self.network_failure_rate:
            raise ConnectionError(f"[{self.name}] Network connection lost during DEBIT operation!")
        current = self.balances.get(account_id, 0.0)
        if current < amount:
            raise ValueError(f"[{self.name}] Insufficient funds in {account_id}. Balance: ₹{current}, Requested: ₹{amount}")
        self.balances[account_id] = current - amount
        print(f"  └─ [{self.name}] Debited ₹{amount:.2f} from {account_id}. New Balance: ₹{self.balances[account_id]:.2f}")
        return True

    def credit(self, account_id: str, amount: float) -> bool:
        if random.random() < self.network_failure_rate:
            raise ConnectionError(f"[{self.name}] Network connection lost during CREDIT operation!")
        current = self.balances.get(account_id, 0.0)
        self.balances[account_id] = current + amount
        print(f"  └─ [{self.name}] Credited ₹{amount:.2f} to {account_id}. New Balance: ₹{self.balances[account_id]:.2f}")
        return True


def run_scenario_1_happy_path(db_a: IndependentDatabase, db_b: IndependentDatabase):
    print("\n" + "="*70)
    print("SCENARIO 1: Happy Path (No Network Failures)")
    print("="*70)
    db_a.set_balance("Account_A", 10000.0)
    db_b.set_balance("Account_B", 5000.0)
    db_a.network_failure_rate = 0.0
    db_b.network_failure_rate = 0.0

    print(f"Initial Balances: DB_A (Account_A) = ₹{db_a.get_balance('Account_A'):.2f} | DB_B (Account_B) = ₹{db_b.get_balance('Account_B'):.2f}")
    print("Executing naive distributed transfer: debit(A, 2000) then credit(B, 2000)...")
    
    db_a.debit("Account_A", 2000.0)
    db_b.credit("Account_B", 2000.0)

    print("Result: Transfer completed successfully.")
    print(f"Final Balances:   DB_A (Account_A) = ₹{db_a.get_balance('Account_A'):.2f} | DB_B (Account_B) = ₹{db_b.get_balance('Account_B'):.2f}")


def run_scenario_2_partial_failure(db_a: IndependentDatabase, db_b: IndependentDatabase):
    print("\n" + "="*70)
    print("SCENARIO 2: Failure Between Operations (Money Disappears into Thin Air)")
    print("="*70)
    db_a.set_balance("Account_A", 10000.0)
    db_b.set_balance("Account_B", 5000.0)
    db_a.network_failure_rate = 0.0
    db_b.network_failure_rate = 1.0  # Force credit operation to fail

    print(f"Initial Balances: DB_A (Account_A) = ₹{db_a.get_balance('Account_A'):.2f} | DB_B (Account_B) = ₹{db_b.get_balance('Account_B'):.2f}")
    print("Executing transfer: debit(A, 2000)...")

    try:
        db_a.debit("Account_A", 2000.0)
        print("Executing transfer: credit(B, 2000)...")
        db_b.credit("Account_B", 2000.0)
    except ConnectionError as e:
        print(f"  ❌ EXCEPTION CAUGHT: {e}")

    print("\n--- POST-MORTEM ANALYSIS ---")
    print(f"DB_A status: Debited ₹2000. Balance: ₹{db_a.get_balance('Account_A'):.2f} (Believes operation succeeded!)")
    print(f"DB_B status: Unchanged.       Balance: ₹{db_b.get_balance('Account_B'):.2f} (Never received request!)")
    print(f"System State: INCONSISTENT! Total money in system changed from ₹15,000 to ₹{db_a.get_balance('Account_A') + db_b.get_balance('Account_B'):.2f}")
    print("₹2,000 vanished because there was no transaction boundary spanning both databases.")


def run_scenario_3_failed_rollback(db_a: IndependentDatabase, db_b: IndependentDatabase):
    print("\n" + "="*70)
    print("SCENARIO 3: Naive Try-Except Rollback Fails (Compensation Drops)")
    print("="*70)
    db_a.set_balance("Account_A", 10000.0)
    db_b.set_balance("Account_B", 5000.0)
    db_a.network_failure_rate = 0.0
    db_b.network_failure_rate = 1.0  # Force credit to fail

    print(f"Initial Balances: DB_A (Account_A) = ₹{db_a.get_balance('Account_A'):.2f} | DB_B (Account_B) = ₹{db_b.get_balance('Account_B'):.2f}")
    print("Attempting transfer with naive try-except rollback code:")

    try:
        db_a.debit("Account_A", 2000.0)
        db_b.credit("Account_B", 2000.0)
    except Exception as e:
        print(f"  ❌ Primary operation failed: {e}")
        print("  └─ Attempting naive rollback: crediting back Account A...")
        # Simulating that during the rollback attempt, DB A network link also fails!
        db_a.network_failure_rate = 1.0
        try:
            db_a.credit("Account_A", 2000.0)
        except Exception as rollback_err:
            print(f"  💥 CRITICAL ROLLBACK FAILURE: {rollback_err}")

    print("\n--- POST-MORTEM ANALYSIS ---")
    print("Why naive try-except is inadequate:")
    print(f"1. Account A remains debited (Balance: ₹{db_a.get_balance('Account_A'):.2f}).")
    print("2. The rollback attempt itself encountered a failure.")
    print("3. In a distributed environment, error handling code can fail just like primary code.")


if __name__ == "__main__":
    db_1 = IndependentDatabase("Database_1 (Bank A)")
    db_2 = IndependentDatabase("Database_2 (Bank B)")

    run_scenario_1_happy_path(db_1, db_2)
    run_scenario_2_partial_failure(db_1, db_2)
    run_scenario_3_failed_rollback(db_1, db_2)
