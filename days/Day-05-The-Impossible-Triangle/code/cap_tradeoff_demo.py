"""
cap_tradeoff_demo.py - CAP Theorem Trade-off Demonstration

Demonstrates the two fundamental choices engineers must make when a network
partition strikes a distributed system:
  1. CP Mode (Consistency over Availability): Reject requests if consensus cannot be reached.
  2. AP Mode (Availability over Consistency): Accept requests locally, risking stale data.
"""

from typing import Dict, Any, Tuple


class SystemNode:
    def __init__(self, name: str):
        self.name = name
        self.storage: Dict[str, Any] = {"user_status": "Active"}

    def get_data(self, key: str) -> Any:
        return self.storage.get(key)

    def set_data(self, key: str, value: Any):
        self.storage[key] = value


class CAPCluster:
    def __init__(self, mode: str):
        """
        mode: 'CP' (Consistency + Partition Tolerance) or 'AP' (Availability + Partition Tolerance)
        """
        self.mode = mode.upper()
        self.node_1 = SystemNode("Node-1")
        self.node_2 = SystemNode("Node-2")
        self.is_partitioned = False

    def trigger_partition(self):
        self.is_partitioned = True

    def resolve_partition(self):
        self.is_partitioned = False
        # Sync node 1 data to node 2 upon healing
        self.node_2.storage = dict(self.node_1.storage)

    def process_write_request(self, target_node_name: str, key: str, value: Any) -> Tuple[bool, str]:
        """
        Processes a write request sent to a specific node.
        """
        target_node = self.node_1 if target_node_name == "Node-1" else self.node_2
        peer_node = self.node_2 if target_node_name == "Node-1" else self.node_1

        if not self.is_partitioned:
            # Normal state: write locally and sync with peer
            target_node.set_data(key, value)
            peer_node.set_data(key, value)
            return True, f"HTTP 200 OK: Data '{key}={value}' written and synchronized to all nodes."

        # Network is partitioned!
        if self.mode == "CP":
            # Consistency Choice: Refuse write because peer cannot acknowledge
            return False, f"HTTP 503 Service Unavailable: Network partition active. Cannot verify consistency with {peer_node.name}. Request rejected!"

        elif self.mode == "AP":
            # Availability Choice: Write locally to stay online, accept temporary divergence
            target_node.set_data(key, value)
            return True, f"HTTP 200 OK: Written to {target_node.name} locally. Warning: {peer_node.name} is isolated and out-of-sync."

        return False, "Unknown mode"

    def process_read_request(self, target_node_name: str, key: str) -> Tuple[bool, Any, str]:
        """
        Processes a read request sent to a specific node.
        """
        target_node = self.node_1 if target_node_name == "Node-1" else self.node_2
        peer_node = self.node_2 if target_node_name == "Node-1" else self.node_1

        if not self.is_partitioned:
            return True, target_node.get_data(key), f"HTTP 200 OK: Returned '{key}' from {target_node.name}."

        if self.mode == "CP":
            # CP requires confirmation that data is fresh across partition
            return False, None, f"HTTP 500 Read Error: Partition active. {target_node.name} cannot verify if data is latest."

        elif self.mode == "AP":
            # AP returns whatever local data is available immediately
            val = target_node.get_data(key)
            return True, val, f"HTTP 200 OK: Returned local data '{val}' from {target_node.name} (Data may be stale)."

        return False, None, "Unknown mode"


def demonstrate_tradeoffs():
    print("=" * 75)
    print("   CAP THEOREM TRADE-OFF DEMONSTRATION: CONSISTENCY VS AVAILABILITY")
    print("=" * 75)

    # ---------------------------------------------------------
    # SCENARIO A: CONSISTENCY OVER AVAILABILITY (CP MODE)
    # ---------------------------------------------------------
    print("\n[SCENARIO A] CP MODE (Prioritizing Consistency)")
    print("-" * 50)
    cp_cluster = CAPCluster(mode="CP")

    print("Step 1: Network Partition Occurs!")
    cp_cluster.trigger_partition()

    print("Step 2: Client sends update ('user_status' = 'Suspended') to Node-1:")
    success, msg = cp_cluster.process_write_request("Node-1", "user_status", "Suspended")
    print(f"  Response: {msg}")

    print("Step 3: Client queries Node-2 for user_status:")
    success, val, msg = cp_cluster.process_read_request("Node-2", "user_status")
    print(f"  Response: {msg}")

    print("\n  --> RESULT IN CP MODE: System sacrifices Availability (returns errors)")
    print("      to guarantee that stale or inconsistent data is NEVER returned.")

    # ---------------------------------------------------------
    # SCENARIO B: AVAILABILITY OVER CONSISTENCY (AP MODE)
    # ---------------------------------------------------------
    print("\n[SCENARIO B] AP MODE (Prioritizing Availability)")
    print("-" * 50)
    ap_cluster = CAPCluster(mode="AP")

    print("Step 1: Network Partition Occurs!")
    ap_cluster.trigger_partition()

    print("Step 2: Client sends update ('user_status' = 'Suspended') to Node-1:")
    success, msg = ap_cluster.process_write_request("Node-1", "user_status", "Suspended")
    print(f"  Response: {msg}")

    print("Step 3: Client queries Node-2 for user_status:")
    success, val, msg = ap_cluster.process_read_request("Node-2", "user_status")
    print(f"  Response: {msg} | Data read: '{val}'")

    print("Step 4: Client queries Node-1 for user_status:")
    success, val, msg = ap_cluster.process_read_request("Node-1", "user_status")
    print(f"  Response: {msg} | Data read: '{val}'")

    print("\n  --> RESULT IN AP MODE: System sacrifices Consistency (Node-2 returns 'Active'")
    print("      while Node-1 returns 'Suspended') to guarantee 100% Availability.")

    # ---------------------------------------------------------
    # RECONCILIATION AFTER HEALING
    # ---------------------------------------------------------
    print("\n[PARTITION HEALS] Re-establishing Network Connectivity")
    print("-" * 50)
    ap_cluster.resolve_partition()
    print("AP Cluster sync complete.")
    _, val_1, _ = ap_cluster.process_read_request("Node-1", "user_status")
    _, val_2, _ = ap_cluster.process_read_request("Node-2", "user_status")
    print(f"Post-heal values -> Node-1: '{val_1}', Node-2: '{val_2}' (Eventual Consistency Achieved)")

    print("=" * 75)


if __name__ == "__main__":
    demonstrate_tradeoffs()
