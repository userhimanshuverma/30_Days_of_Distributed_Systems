"""
Day 3: Single Server Failure Simulation

This simulation demonstrates what happens when a system relies on a single server.
When the server crashes, 100% of user requests fail, leading to immediate downtime.
"""

import time


class SingleServer:
    def __init__(self, name="Server-A"):
        self.name = name
        self.is_alive = True
        self.database = {"user_1": "Alice", "user_2": "Bob", "user_3": "Charlie"}

    def handle_request(self, request_id, action):
        """Processes an incoming user request."""
        if not self.is_alive:
            print(f"[FAIL] [Request #{request_id}] FAILED: {self.name} is DEAD (Connection Refused / 503 Service Unavailable)")
            return False

        print(f"[OK]   [Request #{request_id}] SUCCESS: {self.name} processed '{action}' successfully.")
        return True

    def simulate_hardware_crash(self):
        """Simulates a catastrophic hardware or OS crash."""
        print(f"\n[ALERT] BREAKING: {self.name} suffered a total power failure / kernel panic! [ALERT]\n")
        self.is_alive = False


def main():
    print("=" * 60)
    print("      SCENARIO 1: SINGLE SERVER ARCHITECTURE (NO BACKUP)")
    print("=" * 60)
    
    server = SingleServer("Primary-Server-01")

    # Phase 1: Normal Operation
    print("\n--- Phase 1: Normal Operation ---")
    for req_id in range(1, 4):
        server.handle_request(req_id, "Read Profile")
        time.sleep(0.1)

    # Phase 2: Server Dies
    print("\n--- Phase 2: Unexpected Hardware Failure ---")
    server.simulate_hardware_crash()

    # Phase 3: Outage (All requests fail)
    print("--- Phase 3: User Impact After Failure ---")
    success_count = 0
    failure_count = 0

    for req_id in range(4, 8):
        success = server.handle_request(req_id, "Read Profile")
        if success:
            success_count += 1
        else:
            failure_count += 1
        time.sleep(0.1)

    print("\n" + "=" * 60)
    print("OUTAGE REPORT:")
    print(f"Successful Requests : {success_count}")
    print(f"Failed Requests     : {failure_count}")
    print("System Availability : 0% after server crash")
    print("Business Outcome    : Complete Service Outage! Customers cannot log in or pay.")
    print("=" * 60)


if __name__ == "__main__":
    main()
