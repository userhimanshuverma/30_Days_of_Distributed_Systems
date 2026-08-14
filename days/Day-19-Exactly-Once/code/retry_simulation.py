"""
retry_simulation.py — Failure simulation demonstrating network response loss & retries.

Scenario:
1. Client sends payment request of ₹1,000 (INR 1,000).
2. Server processes payment successfully.
3. Response is LOST on the network path back to the client.
4. Client times out and automatically retries the request.

Demonstrates:
- Naive Non-Idempotent Service -> Double Charge (INR 2,000 deducted).
- Idempotent Service -> Safe Retry (INR 1,000 deducted total, cached response returned).
"""

import sys
import time
from idempotent_payment import Database, NonIdempotentPaymentService, IdempotentPaymentService

# Force stdout to UTF-8 if available to avoid Windows charmap encoding errors
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def run_non_idempotent_experiment():
    print("\n" + "="*70)
    print(" EXPERIMENT 1: NAIVE NON-IDEMPOTENT PAYMENT SERVICE (RETRIES CAUSE DUPLICATES)")
    print("="*70)

    db = Database()
    account_id = "acc_user_101"
    initial_balance = 5000.0
    db.set_balance(account_id, initial_balance)
    service = NonIdempotentPaymentService(db)

    charge_amount = 1000.0
    print(f"Initial Account Balance: INR {db.get_balance(account_id):,.2f}")

    # --- Attempt 1 ---
    print("\n[Client] Sending payment request: Charge INR 1,000...")
    print("[Server] Processing payment...")
    response_1 = service.process_payment(account_id, charge_amount)
    print(f"[Server] Payment processed successfully. Transferred INR {charge_amount}.")

    # Network drops the response
    print("❌ [Network Failure] Response dropped before reaching client!")
    print("⏳ [Client] Request timed out after 1000ms waiting for ACK.")

    # --- Client Retries ---
    print("\n[Client] Retrying payment request: Charge INR 1,000 (Blind retry)...")
    print("[Server] Processing retry request...")
    response_2 = service.process_payment(account_id, charge_amount)
    print(f"[Server] Payment processed successfully. Transferred INR {charge_amount}.")
    print("✅ [Network Success] Response received by client.")

    final_balance = db.get_balance(account_id)
    total_deducted = initial_balance - final_balance

    print("\n--- NON-IDEMPOTENT RESULT ---")
    print(f"Expected Deduction: INR {charge_amount:,.2f}")
    print(f"Actual Total Deducted: INR {total_deducted:,.2f}")
    print(f"Final Account Balance: INR {final_balance:,.2f}")

    if total_deducted > charge_amount:
        print("🚨 CRITICAL BUG: Customer was DOUBLE-CHARGED due to blind network retries!")


def run_idempotent_experiment():
    print("\n" + "="*70)
    print(" EXPERIMENT 2: IDEMPOTENT PAYMENT SERVICE (SAFE RETRIES & DEDUPLICATION)")
    print("="*70)

    db = Database()
    account_id = "acc_user_202"
    initial_balance = 5000.0
    db.set_balance(account_id, initial_balance)
    service = IdempotentPaymentService(db)

    charge_amount = 1000.0
    idempotency_key = "req_pay_unique_99812"

    print(f"Initial Account Balance: INR {db.get_balance(account_id):,.2f}")
    print(f"Generated Idempotency Key: '{idempotency_key}'")

    # --- Attempt 1 ---
    print("\n[Client] Sending payment request (Key: req_pay_unique_99812): Charge INR 1,000...")
    print("[Server] Inspecting Idempotency Key...")
    response_1, is_dup_1 = service.process_payment(idempotency_key, account_id, charge_amount)
    print(f"[Server] First-time key detected. Processed payment. Duplicate: {is_dup_1}")
    print(f"[Server] Response: {response_1}")

    # Network drops the response
    print("❌ [Network Failure] Response dropped before reaching client!")
    print("⏳ [Client] Request timed out after 1000ms waiting for ACK.")

    # --- Client Retries with SAME Key ---
    print("\n[Client] Retrying payment request with SAME Idempotency Key 'req_pay_unique_99812'...")
    print("[Server] Inspecting Idempotency Key...")
    response_2, is_dup_2 = service.process_payment(idempotency_key, account_id, charge_amount)
    print(f"[Server] Duplicate key detected! Replaying cached response. Duplicate: {is_dup_2}")
    print("✅ [Network Success] Response received by client.")
    print(f"[Client] Received Response: {response_2}")

    final_balance = db.get_balance(account_id)
    total_deducted = initial_balance - final_balance

    print("\n--- IDEMPOTENT RESULT ---")
    print(f"Expected Deduction: INR {charge_amount:,.2f}")
    print(f"Actual Total Deducted: INR {total_deducted:,.2f}")
    print(f"Final Account Balance: INR {final_balance:,.2f}")

    if total_deducted == charge_amount:
        print("🎉 SUCCESS: Retry was executed safely. Exactly-once logical effect achieved!")


if __name__ == "__main__":
    run_non_idempotent_experiment()
    run_idempotent_experiment()
