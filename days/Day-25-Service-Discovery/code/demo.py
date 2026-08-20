"""
Service Discovery Interactive Simulation Demo.

Demonstrates:
1. Dynamic registration of multiple service instances
2. Client-side discovery by logical service name
3. Health check status change excluding unhealthy instances
4. Autoscaling / rolling deployment (new instance added, old drained)
5. Heartbeat expiration / TTL eviction of crashed nodes
"""

import time
from service_instance import ServiceInstance
from service_registry import ServiceRegistry
from client import ServiceDiscoveryClient


def print_separator(title: str) -> None:
    print(f"\n{'='*70}\n  {title}\n{'='*70}")


def main():
    print_separator("Day 25: Service Discovery Demonstration")

    # 1. Initialize Central Registry (with a 2-second heartbeat TTL for demonstration)
    registry = ServiceRegistry(heartbeat_ttl_seconds=2.0)
    client = ServiceDiscoveryClient(registry, client_id="checkout-service")

    # -------------------------------------------------------------
    # Step 1: Initial Microservice Startup & Registration
    # -------------------------------------------------------------
    print("\n[Phase 1] Starting Payment Service instances across the cluster...")
    inst1 = ServiceInstance("payment-service", "payment-inst-1", "10.0.0.10", 8080)
    inst2 = ServiceInstance("payment-service", "payment-inst-2", "10.0.0.11", 8080)
    inst3 = ServiceInstance("payment-service", "payment-inst-3", "10.0.0.12", 8080)

    registry.register(inst1)
    registry.register(inst2)
    registry.register(inst3)

    print(f"Registry State: {len(registry.discover('payment-service'))} active payment instances found:")
    for inst in registry.discover("payment-service"):
        print(f"  -> {inst}")

    # -------------------------------------------------------------
    # Step 2: Client Discovers & Dispatches Requests
    # -------------------------------------------------------------
    print_separator("Phase 2: Checkout Service Calls 'payment-service' by Name")
    for req_id in range(1, 6):
        response = client.invoke("payment-service", "/api/v1/charge", {"order_id": 1000 + req_id, "amount": 49.99})
        print(f"Request #{req_id}: {response}")

    # -------------------------------------------------------------
    # Step 3: Instance Failure & Health Check Exclusion
    # -------------------------------------------------------------
    print_separator("Phase 3: Simulating Hardware Failure on payment-inst-2")
    print("Health check fails for payment-inst-2 (10.0.0.11:8080)...")
    registry.set_health("payment-service", "payment-inst-2", is_healthy=False)

    healthy_pool = registry.discover("payment-service")
    print(f"\nRegistry updated. Healthy instances remaining: {len(healthy_pool)}")
    for inst in healthy_pool:
        print(f"  -> {inst}")

    print("\nCheckout Service sends 4 more requests (notice payment-inst-2 is bypassed):")
    for req_id in range(6, 10):
        response = client.invoke("payment-service", "/api/v1/charge", {"order_id": 1000 + req_id, "amount": 99.00})
        print(f"Request #{req_id}: {response}")

    # -------------------------------------------------------------
    # Step 4: Dynamic Scaling / Deployment (Rolling Update)
    # -------------------------------------------------------------
    print_separator("Phase 4: Autoscaling / Rolling Deploy (Adding payment-inst-4)")
    inst4 = ServiceInstance("payment-service", "payment-inst-4", "10.0.0.13", 8080)
    registry.register(inst4)
    print(f"New container launched and registered: {inst4}")

    print("Gracefully decommissioning payment-inst-1 (10.0.0.10)...")
    registry.deregister("payment-service", "payment-inst-1")

    print(f"\nCurrent Active Pool: {[i.instance_id for i in registry.discover('payment-service')]}")
    print("\nCheckout Service dispatches requests across new pool:")
    for req_id in range(10, 14):
        response = client.invoke("payment-service", "/api/v1/charge", {"order_id": 1000 + req_id, "amount": 19.50})
        print(f"Request #{req_id}: {response}")

    # -------------------------------------------------------------
    # Step 5: Silent Crash & Heartbeat TTL Eviction
    # -------------------------------------------------------------
    print_separator("Phase 5: Silent Node Crash & Heartbeat Expiration (TTL)")
    print("Simulating payment-inst-3 crashing silently without sending deregistration...")
    print("payment-inst-4 continues sending background heartbeats to the registry...")
    
    # Wait 2.2 seconds; payment-inst-4 heartbeats during this time, payment-inst-3 does not
    time.sleep(1.0)
    registry.heartbeat("payment-service", "payment-inst-4")
    time.sleep(1.2)
    registry.heartbeat("payment-service", "payment-inst-4")

    print("\nRunning registry eviction sweep for expired heartbeats...")
    evicted = registry.evict_stale_instances()
    print(f"Evicted stale instances: {[inst.instance_id for inst in evicted]}")

    remaining = registry.discover("payment-service")
    print(f"Remaining discoverable instances: {remaining}")

    print("\nCheckout Service dispatches to the surviving active instance:")
    response = client.invoke("payment-service", "/api/v1/charge", {"order_id": 1015, "amount": 150.00})
    print(f"Final Request: {response}")

    print_separator("Demo Complete: Client never had a hardcoded IP address!")


if __name__ == "__main__":
    main()
