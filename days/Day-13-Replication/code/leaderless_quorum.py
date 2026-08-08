"""
leaderless_quorum.py
--------------------
An educational Python simulation demonstrating Leaderless replication
and basic quorum acknowledgment concepts.

Key Concepts:
    - Leaderless Architecture: Any node in the cluster can accept a write or read request.
    - Quorum Decision: An operation is considered successful only if a designated number
      of replicas (Write Quorum 'W') acknowledge the write request.
"""

from typing import Dict, Any, List


class ReplicaNode:
    """Represents a node in a leaderless storage cluster."""

    def __init__(self, node_id: str, is_healthy: bool = True):
        self.node_id = node_id
        self.is_healthy = is_healthy
        self.storage: Dict[str, Any] = {}

    def receive_write(self, key: str, value: Any) -> bool:
        """
        Processes a write request sent directly to this replica.
        
        :return: True if write succeeded, False if node is offline/unhealthy.
        """
        if not self.is_healthy:
            return False
        self.storage[key] = value
        return True

    def receive_read(self, key: str) -> Any:
        """Reads data locally if node is healthy."""
        if not self.is_healthy:
            return None
        return self.storage.get(key)


class LeaderlessCluster:
    """
    Simulates a leaderless database cluster where clients broadcast writes
    to all N replicas and wait for W successful acknowledgments.
    """

    def __init__(self, replica_count: int, write_quorum: int):
        self.replicas = [ReplicaNode(f"Replica-{i+1}") for i in range(replica_count)]
        self.w_quorum = write_quorum

    def execute_write(self, key: str, value: Any) -> bool:
        """
        Broadcasts a write request to all replicas and evaluates quorum success.
        
        :param key: Data record key.
        :param value: Data record value.
        :return: True if write quorum W was met, False otherwise.
        """
        print(f"\n[CLIENT BROADCAST WRITE] -> Key: '{key}', Value: '{value}'")
        print(f"  Cluster Configuration: N={len(self.replicas)} Replicas, Required Write Quorum W={self.w_quorum}")

        successful_acks = 0
        failed_acks = 0

        for replica in self.replicas:
            success = replica.receive_write(key, value)
            if success:
                successful_acks += 1
                print(f"  [OK]   [{replica.node_id}] Write Acknowledged.")
            else:
                failed_acks += 1
                print(f"  [FAIL] [{replica.node_id}] Write Failed (Node Unavailable).")

        # Evaluate Write Quorum rule: successful_acks >= W
        if successful_acks >= self.w_quorum:
            print(f"  [SUCCESS] Received {successful_acks}/{len(self.replicas)} ACKs. Write Quorum (W={self.w_quorum}) MET!")
            return True
        else:
            print(f"  [FAILURE] Only received {successful_acks}/{len(self.replicas)} ACKs. Write Quorum (W={self.w_quorum}) NOT MET!")
            return False


def main():
    print("=" * 70)
    print("      DEMONSTRATION: LEADERLESS REPLICATION & QUORUM WRITES")
    print("=" * 70)

    # Scenario 1: Cluster of 3 nodes, Write Quorum W=2 (All 3 nodes healthy)
    print("\n--- Scenario 1: Healthy Cluster (N=3, W=2) ---")
    cluster1 = LeaderlessCluster(replica_count=3, write_quorum=2)
    cluster1.execute_write("user:202:status", "ACTIVE")

    # Scenario 2: Cluster of 3 nodes, Write Quorum W=2 (1 node fails)
    print("\n--- Scenario 2: Cluster with Partial Node Failure (N=3, W=2) ---")
    cluster2 = LeaderlessCluster(replica_count=3, write_quorum=2)
    # Simulate Replica-3 failing
    cluster2.replicas[2].is_healthy = False
    cluster2.execute_write("user:202:status", "SUSPENDED")

    # Scenario 3: Cluster of 3 nodes, Write Quorum W=2 (2 nodes fail)
    print("\n--- Scenario 3: Cluster with Major Node Outage (N=3, W=2) ---")
    cluster3 = LeaderlessCluster(replica_count=3, write_quorum=2)
    # Simulate Replica-2 and Replica-3 failing
    cluster3.replicas[1].is_healthy = False
    cluster3.replicas[2].is_healthy = False
    cluster3.execute_write("user:202:status", "DELETED")

    print("\n" + "=" * 70)
    print("Key Takeaways:")
    print("1. In leaderless replication, there is no single primary bottleneck.")
    print("2. Writes succeed as long as a quorum W of replicas acknowledge.")
    print("3. Note: Full production quorum systems also configure Read Quorums (R)")
    print("   and require R + W > N to guarantee reading the newest write.")
    print("=" * 70)


if __name__ == "__main__":
    main()
