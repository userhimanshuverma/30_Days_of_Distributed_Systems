"""
Day 21: Retries - Circuit Breaker Pattern Demonstration
======================================================

Educational code demonstrating a Circuit Breaker state machine.
NOTE: This code is for learning purposes and is not production-ready.

Concept:
A Circuit Breaker sits between a client and a downstream dependency to prevent cascading
failures. When a downstream dependency is failing continuously, retrying requests only
worsens the outage.

State Machine:
1. CLOSED: Normal operation. Requests flow to downstream. Consecutive failures are counted.
   - If failures >= threshold -> Transition to OPEN.
2. OPEN: Fast failure! All requests fail immediately without touching downstream.
   - Saves downstream resources & CPU.
   - After `recovery_timeout` seconds -> Transition to HALF-OPEN.
3. HALF-OPEN: Trial mode. Allows limited test traffic to inspect if downstream recovered.
   - If trial request SUCCEEDS -> Transition to CLOSED.
   - If trial request FAILS -> Transition to OPEN (reset recovery timer).
"""

import time
from enum import Enum
from typing import Callable, Any, TypeVar

T = TypeVar('T')


class CircuitState(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF-OPEN"


class CircuitBreakerOpenException(Exception):
    """Raised when request is rejected fast because the Circuit Breaker is OPEN."""
    pass


class CircuitBreaker:
    """
    Simplified Circuit Breaker implementation.
    """
    def __init__(self, failure_threshold: int = 3, recovery_timeout: float = 2.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        
        self.state = CircuitState.CLOSED
        self.consecutive_failures = 0
        self.last_state_change = time.time()

    def _update_state(self):
        """Checks if OPEN state timer has elapsed to transition into HALF-OPEN."""
        now = time.time()
        if self.state == CircuitState.OPEN:
            if (now - self.last_state_change) >= self.recovery_timeout:
                print(f"  [Circuit Breaker] Recovery timeout ({self.recovery_timeout}s) elapsed. State: OPEN -> HALF-OPEN")
                self.state = CircuitState.HALF_OPEN
                self.last_state_change = now

    def execute(self, func: Callable[[], T]) -> T:
        self._update_state()

        if self.state == CircuitState.OPEN:
            print("  [Circuit Breaker] Blocked call! State is OPEN (Failing Fast)")
            raise CircuitBreakerOpenException("Circuit Breaker is OPEN: downstream target is unhealthy.")

        try:
            result = func()
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _on_success(self):
        if self.state == CircuitState.HALF_OPEN:
            print("  [Circuit Breaker] Trial request succeeded! State: HALF-OPEN -> CLOSED")
            self.state = CircuitState.CLOSED
            self.last_state_change = time.time()
        
        self.consecutive_failures = 0

    def _on_failure(self):
        self.consecutive_failures += 1
        print(f"  [Circuit Breaker] Recorded failure ({self.consecutive_failures}/{self.failure_threshold})")
        
        if self.state == CircuitState.HALF_OPEN or self.consecutive_failures >= self.failure_threshold:
            print(f"  [Circuit Breaker] Threshold reached. State: {self.state.value} -> OPEN")
            self.state = CircuitState.OPEN
            self.last_state_change = time.time()


class UnhealthyService:
    """Simulates a service that drops requests."""
    def __init__(self):
        self.is_healthy = False

    def process(self):
        if not self.is_healthy:
            raise Exception("500 Internal Server Error: Database Deadlock")
        return "200 OK - Payment Processed"


if __name__ == "__main__":
    print("=" * 65)
    print("   DISTRIBUTED SYSTEMS HANDBOOK: CIRCUIT BREAKER DEMO")
    print("=" * 65)

    cb = CircuitBreaker(failure_threshold=3, recovery_timeout=1.5)
    downstream = UnhealthyService()

    print("\n--- PHASE 1: Downstream is unhealthy (Failures accumulate) ---")
    for i in range(1, 5):
        print(f"\nClient Call #{i}:")
        try:
            cb.execute(downstream.process)
        except CircuitBreakerOpenException as ex:
            print(f"  Result: Intercepted by Circuit Breaker ({ex})")
        except Exception as ex:
            print(f"  Result: Downstream Failed ({ex})")

    print("\n--- PHASE 2: Client retries while Circuit Breaker is OPEN ---")
    print("Client retrying immediately...")
    try:
        cb.execute(downstream.process)
    except CircuitBreakerOpenException as ex:
        print(f"  Result: Intercepted fast by Circuit Breaker! (Zero downstream traffic generated)")

    print("\n--- PHASE 3: Waiting for recovery timeout (1.5s)... ---")
    time.sleep(1.6)
    print("Downstream recovers in background...")
    downstream.is_healthy = True

    print("\n--- PHASE 4: Trial Request in HALF-OPEN state ---")
    try:
        res = cb.execute(downstream.process)
        print(f"  Result: Success! Downstream returned: '{res}'")
    except Exception as ex:
        print(f"  Result: Failed ({ex})")

    print(f"\nFinal Circuit State: {cb.state.value}")
