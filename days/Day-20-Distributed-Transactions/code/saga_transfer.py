"""
saga_transfer.py — Educational simulation of the Saga Pattern (Compensating Transactions).

Demonstrates:
1. Saga execution as a sequence of independent local transactions.
2. Automatic compensating transaction triggers when a downstream step fails.
3. Handling transient failures during compensating actions using idempotent retries.
4. Business correctness without global database locks or 2PC prepare phase.
"""

import sys
import time
import uuid
import random
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

@dataclass
class Account:
    account_id: str
    balance: float
    # Stores executed idempotency keys to ensure compensation and actions are idempotent
    processed_idempotency_keys: Dict[str, Any] = field(default_factory=dict)


class AccountService:
    """Independent microservice owning account data for a specific bank domain."""
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.accounts: Dict[str, Account] = {}
        self.failure_rate: float = 0.0

    def add_account(self, account_id: str, initial_balance: float):
        self.accounts[account_id] = Account(account_id, initial_balance)

    def debit_local_tx(self, saga_id: str, account_id: str, amount: float) -> bool:
        """Local transaction: Deduct balance immediately in local database."""
        if random.random() < self.failure_rate:
            raise ConnectionError(f"[{self.service_name}] Service unavailable or database error during DEBIT")
        
        acc = self.accounts.get(account_id)
        if not acc:
            raise ValueError(f"[{self.service_name}] Account {account_id} not found")
        
        key = f"DEBIT_{saga_id}"
        if key in acc.processed_idempotency_keys:
            print(f"  └─ [{self.service_name}] Idempotent replay: Debit {saga_id} already executed.")
            return True

        if acc.balance < amount:
            raise ValueError(f"[{self.service_name}] Insufficient funds in {account_id} (Balance ₹{acc.balance})")

        acc.balance -= amount
        acc.processed_idempotency_keys[key] = {"amount": amount, "timestamp": time.time()}
        print(f"  └─ [{self.service_name}] Local Tx Committed: Debited ₹{amount:.2f} from {account_id}. Balance: ₹{acc.balance:.2f}")
        return True

    def credit_local_tx(self, saga_id: str, account_id: str, amount: float) -> bool:
        """Local transaction: Credit balance immediately in local database."""
        if random.random() < self.failure_rate:
            raise ConnectionError(f"[{self.service_name}] Service unavailable or database error during CREDIT")

        acc = self.accounts.get(account_id)
        if not acc:
            raise ValueError(f"[{self.service_name}] Account {account_id} not found")

        key = f"CREDIT_{saga_id}"
        if key in acc.processed_idempotency_keys:
            print(f"  └─ [{self.service_name}] Idempotent replay: Credit {saga_id} already executed.")
            return True

        acc.balance += amount
        acc.processed_idempotency_keys[key] = {"amount": amount, "timestamp": time.time()}
        print(f"  └─ [{self.service_name}] Local Tx Committed: Credited ₹{amount:.2f} to {account_id}. Balance: ₹{acc.balance:.2f}")
        return True

    def compensate_debit(self, saga_id: str, account_id: str, amount: float) -> bool:
        """Compensating action: Re-credit (refund) the debited account."""
        if random.random() < self.failure_rate:
            raise ConnectionError(f"[{self.service_name}] Network timeout during COMPENSATING REFUND!")

        acc = self.accounts.get(account_id)
        if not acc:
            raise ValueError(f"[{self.service_name}] Account {account_id} not found during compensation")

        key = f"REFUND_{saga_id}"
        if key in acc.processed_idempotency_keys:
            print(f"  └─ [{self.service_name}] Idempotent replay: Refund {saga_id} already completed.")
            return True

        acc.balance += amount
        acc.processed_idempotency_keys[key] = {"amount": amount, "timestamp": time.time()}
        print(f"  └─ [{self.service_name}] COMPENSATING ACTION EXECUTED: Refunded ₹{amount:.2f} to {account_id}. Balance: ₹{acc.balance:.2f}")
        return True


class SagaOrchestrator:
    """Manages the Saga workflow state and triggers forward or compensating actions."""
    def __init__(self, bank_a_svc: AccountService, bank_b_svc: AccountService):
        self.bank_a_svc = bank_a_svc
        self.bank_b_svc = bank_b_svc
        self.saga_log: List[str] = []

    def execute_transfer_saga(self, saga_id: str, from_account: str, to_account: str, amount: float):
        print(f"\n--- Starting Saga Workflow: {saga_id} ---")
        self.saga_log.append(f"SAGA_STARTED {saga_id}")

        # STEP 1: Debit From Account (Bank A)
        print("▶ Step 1: Executing Local Tx 1 — Debit Account A...")
        try:
            self.bank_a_svc.debit_local_tx(saga_id, from_account, amount)
            self.saga_log.append(f"STEP_1_SUCCESS {saga_id}")
        except Exception as e:
            print(f"  ❌ Step 1 Failed: {e}. Aborting Saga before any state was changed on other services.")
            self.saga_log.append(f"SAGA_ABORTED_AT_STEP_1 {saga_id}")
            return

        # STEP 2: Credit To Account (Bank B)
        print("▶ Step 2: Executing Local Tx 2 — Credit Account B...")
        try:
            self.bank_b_svc.credit_local_tx(saga_id, to_account, amount)
            self.saga_log.append(f"STEP_2_SUCCESS {saga_id}")
            self.saga_log.append(f"SAGA_COMPLETED_SUCCESSFULLY {saga_id}")
            print(f"✅ Saga {saga_id} Completed Successfully!")
            return
        except Exception as e:
            print(f"  ❌ Step 2 Failed: {e}")
            self.saga_log.append(f"STEP_2_FAILED {saga_id}")

        # COMPENSATING FLOW: Step 2 failed, so roll back Step 1 using a compensating transaction!
        print("\n🔄 TRIGGERING COMPENSATION FLOW (Rolling back Step 1)...")
        max_retries = 3
        retry_count = 0
        compensation_success = False

        while retry_count < max_retries and not compensation_success:
            retry_count += 1
            print(f"  └─ Attempting Compensating Action (Attempt {retry_count}/{max_retries})...")
            try:
                # Temporarily clear artificial failure rate on retry so compensation succeeds
                if retry_count > 1:
                    self.bank_a_svc.failure_rate = 0.0

                self.bank_a_svc.compensate_debit(saga_id, from_account, amount)
                compensation_success = True
                self.saga_log.append(f"COMPENSATION_SUCCESS {saga_id}")
                print(f"✅ Saga {saga_id} Rolled Back Successfully via Business Compensation!")
            except Exception as comp_err:
                print(f"  ⚠️ Compensation Attempt {retry_count} Failed: {comp_err}")
                time.sleep(0.1)

        if not compensation_success:
            print(f"💥 CRITICAL SAGA ALERT: Compensation failed after {max_retries} attempts!")
            print("  └─ Action: Human intervention / Dead-Letter Queue (DLQ) required!")
            self.saga_log.append(f"COMPENSATION_FAILED_DLQ {saga_id}")


def run_happy_saga():
    print("="*70)
    print("DEMO 1: Successful Saga Workflow")
    print("="*70)
    svc_a = AccountService("Bank_A_Service")
    svc_b = AccountService("Bank_B_Service")
    svc_a.add_account("Acc_101", 10000.0)
    svc_b.add_account("Acc_202", 5000.0)

    orchestrator = SagaOrchestrator(svc_a, svc_b)
    orchestrator.execute_transfer_saga("SAGA_001", "Acc_101", "Acc_202", 2000.0)
    print(f"Final Balances: Bank A (Acc_101) = ₹{svc_a.accounts['Acc_101'].balance:.2f} | Bank B (Acc_202) = ₹{svc_b.accounts['Acc_202'].balance:.2f}")


def run_saga_with_compensation():
    print("\n" + "="*70)
    print("DEMO 2: Saga Step 2 Failure & Compensating Refund")
    print("="*70)
    svc_a = AccountService("Bank_A_Service")
    svc_b = AccountService("Bank_B_Service")
    svc_a.add_account("Acc_101", 10000.0)
    svc_b.add_account("Acc_202", 5000.0)
    svc_b.failure_rate = 1.0  # Force Step 2 credit to fail

    orchestrator = SagaOrchestrator(svc_a, svc_b)
    orchestrator.execute_transfer_saga("SAGA_002", "Acc_101", "Acc_202", 2000.0)
    print(f"Final Balances: Bank A (Acc_101) = ₹{svc_a.accounts['Acc_101'].balance:.2f} | Bank B (Acc_202) = ₹{svc_b.accounts['Acc_202'].balance:.2f}")
    print("Notice: Account A balance was debited then restored to ₹10,000 via compensating refund!")


def run_saga_compensation_retry():
    print("\n" + "="*70)
    print("DEMO 3: Saga Compensation Failure with Idempotent Retries")
    print("="*70)
    svc_a = AccountService("Bank_A_Service")
    svc_b = AccountService("Bank_B_Service")
    svc_a.add_account("Acc_101", 10000.0)
    svc_b.add_account("Acc_202", 5000.0)
    svc_b.failure_rate = 1.0  # Force Step 2 credit to fail
    svc_a.failure_rate = 0.5  # Transient failure during compensation!

    orchestrator = SagaOrchestrator(svc_a, svc_b)
    orchestrator.execute_transfer_saga("SAGA_003", "Acc_101", "Acc_202", 2000.0)
    print(f"Final Balances: Bank A (Acc_101) = ₹{svc_a.accounts['Acc_101'].balance:.2f} | Bank B (Acc_202) = ₹{svc_b.accounts['Acc_202'].balance:.2f}")


if __name__ == "__main__":
    run_happy_saga()
    run_saga_with_compensation()
    run_saga_compensation_retry()
