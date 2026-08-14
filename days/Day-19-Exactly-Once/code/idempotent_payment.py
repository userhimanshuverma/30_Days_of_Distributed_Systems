"""
idempotent_payment.py — Educational implementation of an idempotent payment service.

Demonstrates:
1. Atomic storage of idempotency records alongside business transactions.
2. Concurrent lock handling to prevent race conditions during duplicate processing.
3. Cached payload response replay for retried requests.
"""

import time
import uuid
import threading
from typing import Dict, Any, Optional, Tuple

class Database:
    """Simulates a database with atomic transaction support."""
    def __init__(self):
        self.balances: Dict[str, float] = {}
        self.idempotency_records: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def get_balance(self, account_id: str) -> float:
        with self._lock:
            return self.balances.get(account_id, 0.0)

    def set_balance(self, account_id: str, balance: float):
        with self._lock:
            self.balances[account_id] = balance

    def process_idempotent_payment(
        self, idempotency_key: str, account_id: str, amount: float
    ) -> Tuple[bool, Dict[str, Any], bool]:
        """
        Processes payment idempotently within a single database lock (simulating an ACID transaction).
        Returns: (success: bool, response_payload: dict, is_duplicate: bool)
        """
        with self._lock:
            # Step 1: Check if idempotency record exists
            record = self.idempotency_records.get(idempotency_key)
            if record is not None:
                if record["status"] == "IN_FLIGHT":
                    # Another concurrent request is actively processing this key
                    return False, {"error": "Concurrent request in progress. Retry later."}, True
                
                # Request already completed previously; return cached result
                return True, record["response"], True

            # Step 2: Mark request as IN_FLIGHT to claim ownership and prevent concurrent races
            self.idempotency_records[idempotency_key] = {
                "status": "IN_FLIGHT",
                "response": None,
                "created_at": time.time()
            }

            # Step 3: Perform business logic (Deduct balance)
            current_balance = self.balances.get(account_id, 0.0)
            if current_balance < amount:
                error_response = {
                    "status": "FAILED",
                    "reason": "Insufficient funds",
                    "account_id": account_id,
                    "amount": amount
                }
                # Record failure status idempotently
                self.idempotency_records[idempotency_key] = {
                    "status": "COMPLETED",
                    "response": error_response,
                    "created_at": time.time()
                }
                return False, error_response, False

            new_balance = current_balance - amount
            self.balances[account_id] = new_balance

            success_response = {
                "status": "SUCCESS",
                "transaction_id": f"tx_{uuid.uuid4().hex[:8]}",
                "account_id": account_id,
                "amount_charged": amount,
                "remaining_balance": new_balance
            }

            # Step 4: Persist final result atomically alongside state update
            self.idempotency_records[idempotency_key] = {
                "status": "COMPLETED",
                "response": success_response,
                "created_at": time.time()
            }

            return True, success_response, False


class NonIdempotentPaymentService:
    """Naive payment service without idempotency protections."""
    def __init__(self, db: Database):
        self.db = db

    def process_payment(self, account_id: str, amount: float) -> Dict[str, Any]:
        balance = self.db.get_balance(account_id)
        if balance < amount:
            return {"status": "FAILED", "reason": "Insufficient funds"}
        
        new_balance = balance - amount
        self.db.set_balance(account_id, new_balance)
        
        return {
            "status": "SUCCESS",
            "transaction_id": f"tx_{uuid.uuid4().hex[:8]}",
            "account_id": account_id,
            "amount_charged": amount,
            "remaining_balance": new_balance
        }


class IdempotentPaymentService:
    """Production-grade mental model payment service enforcing idempotency."""
    def __init__(self, db: Database):
        self.db = db

    def process_payment(self, idempotency_key: str, account_id: str, amount: float) -> Tuple[Dict[str, Any], bool]:
        if not idempotency_key:
            raise ValueError("Idempotency key is required")
        
        success, response, is_duplicate = self.db.process_idempotent_payment(
            idempotency_key, account_id, amount
        )
        return response, is_duplicate
