#!/usr/bin/env python3
"""
Day 22 — Timeouts: Educational Demo
-----------------------------------
This script demonstrates the core concepts of distributed timeouts:
1. Connect vs. Read Timeouts.
2. Deadline Budget Decay across dependency calls (Client -> Service A -> Service B).
3. Early cancellation when budget is exhausted.
4. Timeout-aware retries with exponential backoff.

Run directly with:
    python timeout_demo.py
"""

import time
import socket
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from dataclasses import dataclass
from typing import Optional

# ============================================================================
# 1. SIMULATED BACKEND SERVERS
# ============================================================================

class SlowServiceBHandler(BaseHTTPRequestHandler):
    """
    Simulates Service B, a downstream dependency that can be fast or slow.
    If the requested path is '/slow', it delays response by 2.5 seconds.
    If the requested path is '/fast', it responds immediately in 50ms.
    """
    def do_GET(self):
        if self.path == "/slow":
            # Simulate heavy database query or downstream lock
            time.sleep(2.5)
        else:
            time.sleep(0.05)

        try:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "success", "data": "Service B payload"}')
        except (ConnectionError, socket.error):
            # Client closed the connection (timed out) while server was processing!
            # Real production servers must handle orphaned writes gracefully.
            pass

    def log_message(self, format, *args):
        # Suppress default HTTP logging to keep console output clean
        return

def start_server_b(port: int) -> HTTPServer:
    server = HTTPServer(("127.0.0.1", port), SlowServiceBHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server

# ============================================================================
# 2. DEADLINE CONTEXT & BUDGET PROPAGATION
# ============================================================================

@dataclass
class TimeBudget:
    """
    Represents an end-to-end request deadline budget.
    Instead of passing static timeouts, services pass remaining time.
    """
    deadline_timestamp: float  # Absolute unix timestamp when work MUST finish

    @classmethod
    def start_new(cls, budget_seconds: float) -> "TimeBudget":
        return cls(deadline_timestamp=time.time() + budget_seconds)

    def remaining_seconds(self) -> float:
        """Returns seconds left in the budget, or 0.0 if expired."""
        remaining = self.deadline_timestamp - time.time()
        return max(0.0, remaining)

    def is_expired(self) -> bool:
        return time.time() >= self.deadline_timestamp

# ============================================================================
# 3. SERVICE A (MIDDLEWARE SERVICE USING TIME BUDGETS)
# ============================================================================

class ServiceAClient:
    """
    Service A processes client requests and calls Service B.
    It enforces strict deadline decay so it never waits longer than
    its caller's remaining budget.
    """
    def __init__(self, service_b_port: int):
        self.service_b_url = f"http://127.0.0.1:{service_b_port}"

    def call_service_b(self, endpoint: str, budget: TimeBudget) -> dict:
        """
        Executes a call to Service B using ONLY the remaining budget as the timeout.
        """
        # Step 1: Check if budget is ALREADY exhausted before making network call
        remaining_time = budget.remaining_seconds()
        if remaining_time <= 0.001:
            print("  [Service A] [ERROR] Budget exhausted BEFORE calling Service B! Aborting call.")
            return {"error": "DeadlineExceeded", "source": "Service A local budget check"}

        print(f"  [Service A] Calling Service B path '{endpoint}' (Remaining Budget: {remaining_time:.3f}s)...")

        # Step 2: Pass remaining_time as the socket read/request timeout
        start_t = time.time()
        try:
            url = f"{self.service_b_url}{endpoint}"
            req = Request(url)
            
            # urlopen's timeout parameter controls the socket timeout
            with urlopen(req, timeout=remaining_time) as response:
                elapsed = time.time() - start_t
                body = response.read().decode('utf-8')
                print(f"  [Service A] [SUCCESS] Service B responded in {elapsed:.3f}s")
                return {"status": "ok", "body": body}

        except URLError as e:
            elapsed = time.time() - start_t
            # Check if failure was caused by socket timeout
            if isinstance(e.reason, socket.timeout):
                print(f"  [Service A] [TIMEOUT] Service B did not respond within budget ({remaining_time:.3f}s). Elapsed: {elapsed:.3f}s")
                return {"error": "Timeout", "detail": f"Socket timed out after {elapsed:.3f}s"}
            else:
                print(f"  [Service A] [NETWORK ERROR] Calling Service B: {e.reason}")
                return {"error": "NetworkError", "detail": str(e.reason)}
        except TimeoutError:
            elapsed = time.time() - start_t
            print(f"  [Service A] [TIMEOUT] Service B read timed out ({remaining_time:.3f}s). Elapsed: {elapsed:.3f}s")
            return {"error": "Timeout", "detail": f"Timed out after {elapsed:.3f}s"}

# ============================================================================
# 4. TIMEOUT-AWARE RETRY DEMONSTRATION
# ============================================================================

def call_with_bounded_retries(client: ServiceAClient, endpoint: str, budget: TimeBudget, max_attempts: int = 3):
    """
    Demonstrates how retries MUST be bounded by the overall request deadline budget.
    """
    for attempt in range(1, max_attempts + 1):
        remaining = budget.remaining_seconds()
        if remaining <= 0:
            print(f"  [Retry Manager] Attempt {attempt}: Budget EXPIRED ({remaining:.3f}s remaining). Giving up retries.")
            return {"error": "DeadlineExceeded", "attempts": attempt}

        print(f"\n  [Retry Manager] --- Attempt {attempt}/{max_attempts} (Time Left: {remaining:.3f}s) ---")
        res = client.call_service_b(endpoint, budget)
        
        if res.get("status") == "ok":
            return res

        # Small backoff delay before retrying, BUT bounded by remaining budget
        backoff = 0.2 * (2 ** (attempt - 1))  # 200ms, 400ms...
        if budget.remaining_seconds() <= backoff:
            print(f"  [Retry Manager] Backoff ({backoff:.2f}s) would exceed remaining budget ({budget.remaining_seconds():.3f}s). Halting retries.")
            break
            
        print(f"  [Retry Manager] Sleeping backoff of {backoff:.2f}s before next attempt...")
        time.sleep(backoff)

    return {"error": "AllAttemptsFailedOrBudgetExhausted"}

# ============================================================================
# MAIN EXECUTION WORKFLOW
# ============================================================================

def main():
    print("=" * 75)
    print("DAY 22 DEMO: TIMEOUTS, DEADLINES, AND TIME BUDGETS")
    print("=" * 75)

    PORT = 18822
    server = start_server_b(PORT)
    print(f"Started simulated Service B on http://127.0.0.1:{PORT}\n")

    client_a = ServiceAClient(service_b_port=PORT)

    # ------------------------------------------------------------------------
    # SCENARIO 1: Successful request within Time Budget
    # ------------------------------------------------------------------------
    print("[SCENARIO 1] Fast Dependency Call within Generous Time Budget (1.5s)")
    budget_1 = TimeBudget.start_new(budget_seconds=1.5)
    result_1 = client_a.call_service_b(endpoint="/fast", budget=budget_1)
    print(f"  Outcome: {result_1}\n")

    # ------------------------------------------------------------------------
    # SCENARIO 2: Slow Dependency Call Triggering Socket Timeout
    # ------------------------------------------------------------------------
    print("[SCENARIO 2] Slow Dependency Call (Takes 2.5s) with Tight Budget (1.0s)")
    budget_2 = TimeBudget.start_new(budget_seconds=1.0)
    result_2 = client_a.call_service_b(endpoint="/slow", budget=budget_2)
    print(f"  Outcome: {result_2}\n")

    # ------------------------------------------------------------------------
    # SCENARIO 3: Multi-tier Call Chain with Deadline Decay & Budget Guard
    # ------------------------------------------------------------------------
    print("[SCENARIO 3] Service Chain Deadline Propagation & Budget Guard")
    # Total user request budget is 1.2s. Service A spends 0.5s doing local work first.
    budget_3 = TimeBudget.start_new(budget_seconds=1.2)
    
    print("  [Service A] Performing local CPU pre-processing (takes 0.5s)...")
    time.sleep(0.5)
    
    # Now Service A calls Service B. Remaining budget is 1.2s - 0.5s = 0.7s.
    print(f"  [Service A] Local work finished. Time budget remaining: {budget_3.remaining_seconds():.3f}s")
    result_3 = client_a.call_service_b(endpoint="/slow", budget=budget_3)
    print(f"  Outcome: {result_3}\n")

    # ------------------------------------------------------------------------
    # SCENARIO 4: Deadline-Bounded Retries Preventing Infinite Waiting
    # ------------------------------------------------------------------------
    print("[SCENARIO 4] Bounded Retries under Deadline Pressure (1.5s Total Budget)")
    budget_4 = TimeBudget.start_new(budget_seconds=1.5)
    result_4 = call_with_bounded_retries(client_a, endpoint="/slow", budget=budget_4, max_attempts=3)
    print(f"  Final Multi-Attempt Outcome: {result_4}\n")

    print("=" * 75)
    print("DEMO COMPLETE: Notice how remaining time budgets prevent services from")
    print("waiting forever, drop wasted downstream work, and bound retry storms!")
    print("=" * 75)

if __name__ == "__main__":
    main()
