"""
multi_leader_conflict.py
------------------------
An educational Python simulation demonstrating Multi-Leader replication
and concurrent write conflict resolution.

Key Concepts:
    - Multi-Leader: Multiple database nodes accept write operations concurrently.
    - Write Conflict: Occurs when two leaders process concurrent updates for the
      same record before cross-leader replication takes place.
    - Conflict Resolution: A deterministic policy (e.g., Last-Write-Wins or Lexical Ordering)
      required to ensure replicas converge on identical data.
"""

from typing import Dict, Any, Tuple


class LeaderNode:
    """Represents a leader node capable of accepting writes directly from clients."""

    def __init__(self, name: str):
        self.name = name
        # Storage maps key -> (value, timestamp_sec)
        self.storage: Dict[str, Tuple[Any, float]] = {}

    def client_write(self, key: str, value: Any, timestamp: float):
        """Accepts a direct write operation from a client."""
        self.storage[key] = (value, timestamp)
        print(f"  [{self.name}] Accepted Client Write: key='{key}', val='{value}', ts={timestamp}")

    def receive_replicated_write(self, key: str, incoming_value: Any, incoming_timestamp: float) -> str:
        """
        Processes a replicated write received from another leader node.
        Detects conflicts and applies a Last-Write-Wins (LWW) resolution policy.
        """
        if key not in self.storage:
            self.storage[key] = (incoming_value, incoming_timestamp)
            return "APPLIED_NEW"

        existing_val, existing_ts = self.storage[key]

        # Conflict detected! Check timestamps
        if incoming_timestamp > existing_ts:
            self.storage[key] = (incoming_value, incoming_timestamp)
            return f"CONFLICT_RESOLVED_INCOMING_WON ('{incoming_value}' > '{existing_val}')"
        elif incoming_timestamp < existing_ts:
            return f"CONFLICT_RESOLVED_LOCAL_WON ('{existing_val}' > '{incoming_value}')"
        else:
            if str(incoming_value) > str(existing_val):
                self.storage[key] = (incoming_value, incoming_timestamp)
                return f"TIE_BREAKER_INCOMING_WON ('{incoming_value}')"
            return f"TIE_BREAKER_LOCAL_WON ('{existing_val}')"

    def __repr__(self):
        readable_storage = {k: v[0] for k, v in self.storage.items()}
        return f"[{self.name}] Storage: {readable_storage}"


def main():
    print("=" * 70)
    print("     DEMONSTRATION: MULTI-LEADER REPLICATION & WRITE CONFLICTS")
    print("=" * 70)

    leader_a = LeaderNode("Leader A (US East)")
    leader_b = LeaderNode("Leader B (EU West)")

    print("\n--- Initial State ---")
    print(leader_a)
    print(leader_b)

    # Step 1: Concurrent writes occur at two different leaders for the same user record
    print("\n--- Concurrent Writes Arrive at Different Leaders ---")

    # Leader A receives a write from a US client at timestamp 100.0
    t_a = 100.0
    leader_a.client_write(key="user:101:city", value="Delhi", timestamp=t_a)

    # Leader B receives a write from an EU client at timestamp 100.5
    t_b = 100.5
    leader_b.client_write(key="user:101:city", value="Bangalore", timestamp=t_b)

    print("\n--- State Before Cross-Leader Replication ---")
    print(f"  {leader_a}")
    print(f"  {leader_b}")
    print("  [!] Notice: The two leaders currently disagree on user:101:city!")

    # Step 2: Cross-leader replication occurs
    print("\n--- Cross-Leader Replication & Conflict Resolution ---")

    # Leader A sends its write to Leader B
    val_a, ts_a = leader_a.storage["user:101:city"]
    res_b = leader_b.receive_replicated_write("user:101:city", val_a, ts_a)
    print(f"  [Replication A -> B] Leader B processed update: {res_b}")

    # Leader B sends its write to Leader A
    val_b, ts_b = leader_b.storage["user:101:city"]
    res_a = leader_a.receive_replicated_write("user:101:city", val_b, ts_b)
    print(f"  [Replication B -> A] Leader A processed update: {res_a}")

    print("\n--- Converged Cluster State After Replication ---")
    print(f"  {leader_a}")
    print(f"  {leader_b}")

    print("\n" + "=" * 70)
    print("Key Takeaways:")
    print("1. Multi-Leader allows local low-latency writes across regions.")
    print("2. When two leaders modify the same record concurrently, a write conflict occurs.")
    print("3. Both leaders must run a conflict resolution strategy (e.g., LWW) so")
    print("   their datasets eventually converge to identical values.")
    print("=" * 70)


if __name__ == "__main__":
    main()
