"""
Day 4: Why Copying Data Creates Bigger Problems
Demo 1: Replication Delay & Temporary Disagreement Simulation

This script demonstrates what happens when a user updates data on a system
with 3 replicated servers (Server A, Server B, Server C). Because network updates
take time to propagate, readers visiting different servers right after an update
will see DIFFERENT, conflicting answers.
"""

import time


class DatabaseNode:
    def __init__(self, name: str):
        self.name = name
        self.data = {"user_id": 42, "password": "old_password_123"}

    def get_password(self) -> str:
        """Read data from this server."""
        return self.data["password"]

    def update_password(self, new_password: str) -> None:
        """Directly write data to this server."""
        self.data["password"] = new_password


class ReplicatedCluster:
    def __init__(self):
        self.server_a = DatabaseNode("Server A (Primary)")
        self.server_b = DatabaseNode("Server B (Replica 1)")
        self.server_c = DatabaseNode("Server C (Replica 2)")
        self.servers = [self.server_a, self.server_b, self.server_c]

    def user_changes_password(self, new_password: str):
        print(f"\n[USER ACTION] Updating password to '{new_password}'...")
        print("-------------------------------------------------------")

        # Step 1: Update reaches Server A immediately
        print(" -> [0.0s] Update arrives at Server A.")
        self.server_a.update_password(new_password)
        print(f"   -> Server A state: password = '{self.server_a.get_password()}'")
        print(f"   -> Server B state: password = '{self.server_b.get_password()}' (Not updated yet!)")
        print(f"   -> Server C state: password = '{self.server_c.get_password()}' (Not updated yet!)")

    def simulate_user_logins_during_update(self, new_password: str):
        print("\n[USER LOGINS] LOGINS OCCURRING IMMEDIATELY AFTER UPDATE:")
        print("-------------------------------------------------------")

        # Request 1 goes to Server A
        ans_a = self.server_a.get_password()
        print(f" [User] Login Attempt #1 -> Routed to Server A: Found password '{ans_a}'")
        print(f"   --> User tries login with '{new_password}': SUCCESS! [OK]")

        # Request 2 goes to Server B
        ans_b = self.server_b.get_password()
        print(f" [User] Login Attempt #2 -> Routed to Server B: Found password '{ans_b}'")
        print(f"   --> User tries login with '{new_password}': FAILED! [FAIL] (Server B still has old password!)")

        print("\n[WARNING] OBSERVATION: Nothing crashed! No hardware failed!")
        print("    Yet the application behaves unpredictably because copies disagree.")

    def sync_remaining_servers(self, new_password: str):
        print("\n[NETWORK SYNC] SYNCHRONIZATION OVER TIME:")
        print("-------------------------------------------------------")
        time.sleep(1)
        print(" -> [1.0s] Background replication sync reaches Server B...")
        self.server_b.update_password(new_password)
        print(f"   -> Server B state: password = '{self.server_b.get_password()}'")

        time.sleep(1)
        print(" -> [2.0s] Background replication sync reaches Server C...")
        self.server_c.update_password(new_password)
        print(f"   -> Server C state: password = '{self.server_c.get_password()}'")

        print("\n[SUCCESS] FINAL STATE: All 3 servers are finally synchronized!")
        print(f"   Server A: '{self.server_a.get_password()}'")
        print(f"   Server B: '{self.server_b.get_password()}'")
        print(f"   Server C: '{self.server_c.get_password()}'")


def main():
    print("=======================================================")
    print("   DAY 4 DEMO: REPLICATION DELAY & DISAGREEMENT")
    print("=======================================================")

    cluster = ReplicatedCluster()

    # 1. Initial State
    print("\n[INITIAL STATE] All servers hold 'old_password_123'")
    for s in cluster.servers:
        print(f"   [{s.name}]: {s.get_password()}")

    # 2. User updates password
    new_pwd = "new_secret_password_2026"
    cluster.user_changes_password(new_pwd)

    # 3. Show inconsistent login attempts
    cluster.simulate_user_logins_during_update(new_pwd)

    # 4. Background sync brings convergence
    cluster.sync_remaining_servers(new_pwd)

    print("\n[KEY LESSON]")
    print("   Making copies is easy. Keeping them synchronized is the real challenge.")
    print("=======================================================")


if __name__ == "__main__":
    main()
