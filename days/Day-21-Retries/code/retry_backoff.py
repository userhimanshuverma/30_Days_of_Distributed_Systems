"""
Day 21: Retries - Exponential Backoff Demonstration
===================================================

Educational code demonstrating Exponential Backoff.
NOTE: This code is for learning purposes and is not production-ready.

Concept:
When a downstream service fails or becomes overloaded, immediately retrying at a constant
interval (e.g., every 100ms) will flood the struggling service with requests. 
Exponential backoff increases the delay exponentially between successive retry attempts:
    delay = min(max_delay, initial_delay * (backoff_factor ** attempt))

This allows the downstream service time to recover while still giving the client a chance
to complete the request if the failure was transient.
"""

import time
import random
from typing import Callable, Any, TypeVar

T = TypeVar('T')


class ServiceUnavailableException(Exception):
    """Simulated transient server/network error."""
    pass


class SimulatedDownstreamService:
    """
    Simulates a service that fails transiently for the first N calls
    before succeeding.
    """
    def __init__(self, failures_before_success: int = 3):
        self.failures_before_success = failures_before_success
        self.attempts_made = 0

    def call_api(self) -> str:
        self.attempts_made += 1
        if self.attempts_made <= self.failures_before_success:
            print(f"  [Downstream Server] Internal processing failed (Attempt #{self.attempts_made})")
            raise ServiceUnavailableException("HTTP 503: Service Unavailable")
        
        print(f"  [Downstream Server] Request processed successfully! (Attempt #{self.attempts_made})")
        return "200 OK - Data Payload"


def execute_with_exponential_backoff(
    func: Callable[[], T],
    max_retries: int = 5,
    initial_delay: float = 0.5,
    backoff_factor: float = 2.0,
    max_delay: float = 8.0
) -> T:
    """
    Executes a function with exponential backoff retry logic.
    """
    attempt = 0
    while True:
        try:
            return func()
        except ServiceUnavailableException as e:
            attempt += 1
            if attempt > max_retries:
                print(f"[Retry Engine] Exceeded maximum retries ({max_retries}). Giving up.")
                raise e

            # Calculate backoff delay: initial_delay * (backoff_factor ^ (attempt - 1))
            delay = min(max_delay, initial_delay * (backoff_factor ** (attempt - 1)))
            print(f"[Retry Engine] Attempt {attempt} failed ({e}). Backing off for {delay:.2f}s...")
            time.sleep(delay)


if __name__ == "__main__":
    print("=" * 60)
    print("   DISTRIBUTED SYSTEMS HANDBOOK: EXPONENTIAL BACKOFF DEMO")
    print("=" * 60)
    
    service = SimulatedDownstreamService(failures_before_success=3)

    start_time = time.time()
    try:
        result = execute_with_exponential_backoff(
            func=service.call_api,
            max_retries=4,
            initial_delay=0.2, # 200ms
            backoff_factor=2.0,
            max_delay=5.0
        )
        total_elapsed = time.time() - start_time
        print(f"\n[Result] Final Response: '{result}' in {total_elapsed:.2f}s total elapsed time.")
    except Exception as ex:
        print(f"\n[Result] Operation permanently failed: {ex}")
