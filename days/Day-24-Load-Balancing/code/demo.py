#!/usr/bin/env python3
"""
Day 24 — Load Balancer Interactive Demonstration
------------------------------------------------
This script demonstrates how a load balancer manages incoming client traffic
across a pool of backend servers, handles backend failures, and recovers.

Scenario Workflow:
    Phase 1: Initial state with 3 healthy servers (server-a, server-b, server-c).
             Requests are evenly distributed using Round Robin.
    Phase 2: Server B experiences a failure (e.g. database pool exhaustion / crash).
             The load balancer detects/receives health status and removes server-b.
    Phase 3: Client requests continue to flow. Traffic is routed exclusively to healthy servers (a & c).
    Phase 4: Server B recovers. Health check confirms recovery.
             The load balancer re-integrates server-b into the active rotation.
"""

import sys
import time
from load_balancer import LoadBalancer

# Ensure UTF-8 output encoding for standard output on Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def print_header(title: str) -> None:
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_server_status(lb: LoadBalancer) -> None:
    print("\n--- Current Backend Server Pool Status ---")
    for server_id, server in lb.servers.items():
        status_icon = "[OK] HEALTHY  " if server.is_healthy else "[FAIL] UNHEALTHY"
        print(f"  * {server_id}: {status_icon} | Active: {server.active_connections} | Total Handled: {server.total_requests_handled}")
    print("-" * 70)


def simulate_requests(lb: LoadBalancer, count: int, phase_name: str) -> None:
    print(f"\n[->] Sending {count} client requests during [{phase_name}]...")
    for i in range(1, count + 1):
        assigned_server = lb.next_server()
        if assigned_server:
            # Simulate brief request processing then release
            lb.release_connection(assigned_server)
        time.sleep(0.05)


def main():
    print_header("Day 24 -- Load Balancer Educational Demonstration")

    # Step 1: Initialize Load Balancer with 3 servers
    server_list = ["server-a", "server-b", "server-c"]
    print(f"\n[*] Initializing LoadBalancer with pool: {server_list}")
    lb = LoadBalancer(server_ids=server_list, algorithm="round_robin")
    print_server_status(lb)

    # Phase 1: All 3 servers are healthy
    print_header("PHASE 1: Normal Operation (All 3 Servers Healthy)")
    simulate_requests(lb, count=6, phase_name="Phase 1: Normal Traffic")
    print_server_status(lb)

    # Phase 2: Server B becomes unhealthy
    print_header("PHASE 2: Backend Outage (Server B Fails)")
    print("[ALERT] Server B encountered an unexpected internal crash / memory freeze!")
    print("[ACTION] Marking 'server-b' as UNHEALTHY in load balancer registry...")
    lb.set_server_health("server-b", is_healthy=False)
    print_server_status(lb)

    # Phase 3: Traffic during outage
    print_header("PHASE 3: Traffic Rerouting During Outage")
    print("[INFO] Client traffic arrives. Observe how traffic completely avoids 'server-b'...")
    simulate_requests(lb, count=6, phase_name="Phase 3: Outage Rerouting")
    print_server_status(lb)

    # Phase 4: Server B recovers
    print_header("PHASE 4: Backend Recovery & Re-integration")
    print("[RECOVERY] Server B process restarted and passed application health check.")
    print("[ACTION] Marking 'server-b' as HEALTHY in load balancer registry...")
    lb.set_server_health("server-b", is_healthy=True)
    print_server_status(lb)

    # Phase 5: Normal distribution resumes
    print_header("PHASE 5: Traffic Resumption Across Full Pool")
    print("[INFO] Client traffic arrives. Observe how Round Robin resumes across all 3 backends...")
    simulate_requests(lb, count=6, phase_name="Phase 5: Recovered Traffic")
    print_server_status(lb)

    # Summary
    print_header("SUMMARY & KEY LESSON")
    print("  1. Adding machines alone does NOT balance traffic; a load balancer is required.")
    print("  2. Load balancers continuously monitor backend health.")
    print("  3. Unhealthy backends are removed from traffic routing instantly.")
    print("  4. Clients interact with a single entry point, completely unaware of infrastructure changes.")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
