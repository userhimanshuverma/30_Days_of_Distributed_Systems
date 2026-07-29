"""
Day 3: Simple Replication Simulation

This simulation demonstrates the core intuition of replication.
When the primary server dies, a replica (backup copy) takes over incoming requests,
ensuring uninterrupted service for users.
"""

import time


class ServerNode:
    def __init__(self, name):
        self.name = name
        self.is_alive = True
        self.data = {"status": "Active", "inventory": 100}

    def process_request(self, request_id, action):
        if not self.is_alive:
            return False
        print(f"[OK]   [Request #{request_id}] Handled by {self.name} ('{action}')")
        return True


class ReplicatedSystem:
    def __init__(self):
        self.primary = ServerNode("Primary-Server-01")
        self.replica = ServerNode("Replica-Server-02")

    def route_request(self, request_id, action):
        """
        Routes traffic to the primary server.
        If the primary is dead, seamlessly falls back to the replica copy.
        """
        if self.primary.is_alive:
            return self.primary.process_request(request_id, action)

        print(f"[WARN] [Router] {self.primary.name} is down! Rerouting request #{request_id} to {self.replica.name}...")
        if self.replica.is_alive:
            return self.replica.process_request(request_id, action)

        print(f"[FAIL] [Request #{request_id}] FAILED: All replicated servers are offline.")
        return False


def main():
    print("=" * 60)
    print("      SCENARIO 2: REPLICATED SYSTEM ARCHITECTURE (WITH BACKUP)")
    print("=" * 60)

    system = ReplicatedSystem()

    # Phase 1: Normal operations (Primary handling requests)
    print("\n--- Phase 1: Normal Operations (Primary Server Active) ---")
    for req_id in range(1, 4):
        system.route_request(req_id, "Checkout Cart")
        time.sleep(0.1)

    # Phase 2: Primary server dies unexpected physical crash
    print("\n--- Phase 2: Primary Server Suffers Hardware Failure ---")
    system.primary.is_alive = False
    print(f"[ALERT] {system.primary.name} crashed! Power supply failure! [ALERT]\n")

    # Phase 3: Traffic served by Replica (Uninterrupted Service)
    print("--- Phase 3: Seamless Failover to Replica ---")
    success_count = 0
    failure_count = 0

    for req_id in range(4, 8):
        success = system.route_request(req_id, "Checkout Cart")
        if success:
            success_count += 1
        else:
            failure_count += 1
        time.sleep(0.1)

    print("\n" + "=" * 60)
    print("RESILIENCE REPORT:")
    print(f"Successful Requests : {success_count + 3} / 7")
    print(f"Failed Requests     : {failure_count}")
    print("System Availability : 100%")
    print("Business Outcome    : Zero Downtime! Customers experienced uninterrupted service.")
    print("=" * 60)


if __name__ == "__main__":
    main()
