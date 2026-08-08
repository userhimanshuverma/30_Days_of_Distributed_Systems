"""
primary_secondary_replication.py
--------------------------------
An educational Python simulation demonstrating Primary/Secondary (Leader/Follower)
replication behavior in distributed databases.

Key Concepts:
    - Primary Node: The single node that accepts write operations.
    - Secondary Nodes: Read-only replicas that receive updates from the primary.
    - Replication Lag: The temporal window where secondary nodes have not yet
      received or applied updates processed by the primary.
"""

import sys
from typing import Dict, Any, List


class Node:
    """Represents a database node (Primary or Secondary) holding key-value records."""
    
    def __init__(self, node_id: str, role: str):
        self.node_id = node_id
        self.role = role  # "Primary" or "Secondary"
        self.storage: Dict[str, Any] = {}

    def write_local(self, key: str, value: Any):
        """Writes data to the local node's storage engine."""
        self.storage[key] = value

    def read_local(self, key: str) -> Any:
        """Reads data from the local node's storage engine."""
        return self.storage.get(key, "<Not Present>")

    def __repr__(self):
        return f"[{self.role} {self.node_id}] Data: {self.storage}"


class PrimarySecondaryCluster:
    """
    Simulates a primary/secondary cluster where all writes go to the primary node
    and are subsequently replicated to secondary replicas.
    """

    def __init__(self, secondary_ids: List[str]):
        self.primary = Node("Node-0 (Primary)", role="Primary")
        self.secondaries = [Node(f"Node-{i} (Secondary)", role="Secondary") for i in secondary_ids]

    def print_cluster_state(self, step_description: str):
        """Utility method to print the current state of all replicas."""
        print(f"\n--- {step_description} ---")
        print(f"  Primary   : {self.primary}")
        for sec in self.secondaries:
            print(f"  Secondary : {sec}")

    def execute_write(self, key: str, value: Any, sync_replica_indices: List[int], async_replica_indices: List[int]):
        """
        Executes a write operation on the primary node and replicates to secondaries.
        """
        print(f"\n[CLIENT WRITE REQUEST] -> Set '{key}' = '{value}' on Primary")
        
        # Step 1: Write to the Primary node first
        self.primary.write_local(key, value)
        print(f"  [Primary] Write accepted and written to storage.")

        # Step 2: Synchronous replication to designated sync secondaries
        for idx in sync_replica_indices:
            sec = self.secondaries[idx]
            sec.write_local(key, value)
            print(f"  [Replication] Synchronous replication completed for {sec.node_id}.")

        self.print_cluster_state("State Immediately After Client Write Acknowledgment")

        # Step 3: Simulate read queries to show replication lag on asynchronous secondaries
        for idx in async_replica_indices:
            sec = self.secondaries[idx]
            val = sec.read_local(key)
            print(f"  [!] [CLIENT READ] Querying {sec.node_id} for key '{key}' -> Result: '{val}' (REPLICATION LAG!)")

        # Step 4: Asynchronous replication completes after network delay
        print("\n[NETWORK] Catching up asynchronous replicas...")
        for idx in async_replica_indices:
            sec = self.secondaries[idx]
            sec.write_local(key, value)
            print(f"  [Replication] Asynchronous replication caught up for {sec.node_id}.")

        self.print_cluster_state("State After Asynchronous Replication Completes")


def main():
    print("=" * 70)
    print("      DEMONSTRATION: PRIMARY / SECONDARY REPLICATION & LAG")
    print("=" * 70)

    # Create cluster with 2 secondary nodes
    cluster = PrimarySecondaryCluster(secondary_ids=["1", "2"])
    cluster.print_cluster_state("Initial Cluster State")

    # Perform Write 1: Update customer email
    cluster.execute_write(
        key="user:101:email",
        value="alice@example.com",
        sync_replica_indices=[0],   # Secondary 1 sync
        async_replica_indices=[1]   # Secondary 2 async (lagging)
    )

    # Perform Write 2: Update customer tier
    cluster.execute_write(
        key="user:101:tier",
        value="PLATINUM",
        sync_replica_indices=[0],
        async_replica_indices=[1]
    )

    print("\n" + "=" * 70)
    print("Key Intuition:")
    print("1. All writes MUST route to the Primary.")
    print("2. Secondaries can serve reads, but asynchronous replicas introduce")
    print("   a window of time where reads return stale data (Replication Lag).")
    print("=" * 70)


if __name__ == "__main__":
    main()
