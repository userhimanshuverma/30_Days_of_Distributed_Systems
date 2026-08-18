#!/usr/bin/env python3
"""
Day 23 — Circuit Breaker Interactive Demo
-----------------------------------------
This script demonstrates the complete lifecycle of a Circuit Breaker:
1. Normal operation in CLOSED state.
2. Accumulation of downstream failures until failure threshold is reached.
3. Tripping into OPEN state and short-circuiting subsequent requests (Fast Failure / Fallback).
4. Elapsing of the recovery window.
5. Trial execution in HALF-OPEN state.
6. Successful recovery back to CLOSED state.
7. Unsuccessful probe in HALF-OPEN state re-tripping back to OPEN state.

Run directly:
    python demo.py
"""

import time
import sys
from circuit_breaker import CircuitBreaker, CircuitBreakerOpenException, CircuitState


# ============================================================================
# SIMULATED DEPENDENCY & FALLBACK
# ============================================================================

class PaymentGatewayService:
    """
    Simulates a remote payment dependency (e.g., Stripe/Adyen API) that can
    be set to healthy or unhealthy states.
    """
    def __init__(self):
        self.is_healthy = True
        self.call_count = 0

    def process_payment(self, amount: float, account_id: str) -> dict:
        self.call_count += 1
        print(f"   --> Network I/O: Contacting Payment Gateway (Attempt #{self.call_count})...")
        
        if not self.is_healthy:
            # Simulate a 503 Service Unavailable or TCP socket timeout exception
            raise ConnectionError("503 Service Unavailable: Remote Payment Database Locked")

        return {
            "status": "SUCCESS",
            "transaction_id": f"tx_{self.call_count}_{int(time.time())}",
            "amount": amount,
            "account_id": account_id
        }


def fallback_cached_payment(amount: float, account_id: str) -> dict:
    """
    Fallback function executed when the main dependency is OPEN or failing.
    In a real system, this might return a queued offline response or degraded UI state.
    """
    print("   [FALLBACK ACTIVATED] Returning cached degraded payment response.")
    return {
        "status": "DEGRADED_PENDING",
        "message": "Payment accepted offline. Processing will resume shortly.",
        "amount": amount,
        "account_id": account_id
    }


# ============================================================================
# DEMO EXECUTION FLOWS
# ============================================================================

def print_banner(title: str):
    print("\n" + "=" * 75)
    print(f"  {title}")
    print("=" * 75)


def run_demo():
    print_banner("DAY 23: CIRCUIT BREAKER DEMONSTRATION")
    
    # Initialize dependency and circuit breaker
    # Threshold: 3 consecutive failures to trip
    # Recovery Timeout: 2.0 seconds window
    service = PaymentGatewayService()
    breaker = CircuitBreaker(
        failure_threshold=3,
        recovery_timeout=2.0,
        expected_exception=ConnectionError,
        fallback=fallback_cached_payment
    )

    # ------------------------------------------------------------------------
    # STEP 1: Healthy Operation (CLOSED State)
    # ------------------------------------------------------------------------
    print_banner("STEP 1: Healthy Dependency Calls (CLOSED State)")
    print("Sending 3 requests to healthy Payment Gateway...")
    
    for i in range(1, 4):
        res = breaker.call(service.process_payment, amount=99.99, account_id="acc_1001")
        print(f"Result #{i}: Status={res['status']}, TxID={res.get('transaction_id')}")
        time.sleep(0.2)

    print(f"\nCurrent Circuit State: {breaker.state.value} | Failures: {breaker.failure_count}")

    # ------------------------------------------------------------------------
    # STEP 2: Downstream Outage & Tripping Circuit (CLOSED -> OPEN)
    # ------------------------------------------------------------------------
    print_banner("STEP 2: Downstream Failure Surge (CLOSED -> OPEN)")
    print("[OUTAGE INJECTED] Injecting outage into Payment Gateway...")
    service.is_healthy = False

    for i in range(1, 4):
        print(f"\n--- Request Call #{i} during outage ---")
        res = breaker.call(service.process_payment, amount=150.00, account_id="acc_1002")
        print(f"Result #{i}: Status={res['status']}")

    print(f"\nCurrent Circuit State: {breaker.state.value} (Tripped after {breaker.failure_threshold} failures)")

    # ------------------------------------------------------------------------
    # STEP 3: Short-Circuiting & Fast Failure (OPEN State)
    # ------------------------------------------------------------------------
    print_banner("STEP 3: Fast Short-Circuiting (OPEN State)")
    print("Sending requests while circuit is OPEN...")
    print("Notice: Network calls to Payment Gateway are BLOCKED immediately!\n")

    calls_before = service.call_count
    for i in range(1, 4):
        print(f"--- Request Call #{i} while OPEN ---")
        res = breaker.call(service.process_payment, amount=200.00, account_id="acc_1003")
        print(f"Result #{i}: Status={res['status']}")

    calls_made = service.call_count - calls_before
    print(f"\nTotal remote network calls made to failing dependency during Step 3: {calls_made}")
    print("[PROTECTION CONFIRMED] ZERO network bandwidth or socket threads wasted on failing service!")

    # ------------------------------------------------------------------------
    # STEP 4: Recovery Window Elapses (OPEN -> HALF-OPEN) & Successful Recovery
    # ------------------------------------------------------------------------
    print_banner("STEP 4: Recovery Window & Successful Probe (OPEN -> HALF-OPEN -> CLOSED)")
    print(f"Waiting {breaker.recovery_timeout} seconds for recovery timeout window to elapse...")
    time.sleep(breaker.recovery_timeout + 0.2)

    print("\nPayment Gateway has recovered downstream.")
    service.is_healthy = True

    print("\nIssuing trial request (Circuit will probe in HALF-OPEN state)...")
    res = breaker.call(service.process_payment, amount=300.00, account_id="acc_1004")
    print(f"Probe Result: Status={res['status']}")
    print(f"Circuit State after successful probe: {breaker.state.value}")

    # ------------------------------------------------------------------------
    # STEP 5: Failed Probe Trial (HALF-OPEN -> OPEN)
    # ------------------------------------------------------------------------
    print_banner("STEP 5: Failed Probe Re-Tripping (CLOSED -> OPEN -> HALF-OPEN -> OPEN)")
    print("Simulating a secondary failure to show re-tripping behavior...")
    
    # Force back to OPEN state
    service.is_healthy = False
    for _ in range(3):
        breaker.call(service.process_payment, amount=50.00, account_id="acc_1005")

    print(f"Circuit tripped back to: {breaker.state.value}")
    print(f"Waiting {breaker.recovery_timeout} seconds for recovery window...")
    time.sleep(breaker.recovery_timeout + 0.2)

    print("\nDependency STILL FAILING during trial request...")
    res = breaker.call(service.process_payment, amount=50.00, account_id="acc_1005")
    print(f"Probe Result (Failed): Status={res['status']}")
    print(f"Circuit State immediately after failed probe: {breaker.state.value}")

    print_banner("DEMO COMPLETE")
    print("Key Insight: The Circuit Breaker protected the system from cascading failure!")


if __name__ == "__main__":
    run_demo()
