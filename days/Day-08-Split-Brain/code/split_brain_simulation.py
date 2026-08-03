"""
split_brain_simulation.py - Educational Simulation of Split Brain Failure

This script simulates a Split Brain scenario in a 5-node distributed database cluster.

Key Concepts Demonstrated:
1. Healthy Consensus State: Initial 5-node cluster with Node-1 as leader and balance = $1,000.
2. Network Partition Event: The network splits into Partition A (Node-1, Node-2) and 
   Partition B (Node-3, Node-4, Node-5).
3. Dual Leader Emergence: 
   - Partition A keeps Node-1 as active leader.
   - Partition B misses heartbeats from Node-1, presumes Node-1 has crashed, and elects Node-3 as new leader.
4. Divergent Writes: Clients send transactions to both leaders simultaneously.
   - Client A deposits $500 via Node-1 (Balance: $1,000 -> $1,500).
   - Client B withdraws $800 via Node-3 (Balance: $1,000 -> $200).
5. Data Corruption: When the network connection heals, the cluster contains two completely 
   valid, conflicting histories with no deterministic automated way to reconcile them!
"""

from typing import Dict, List, Optional


class NetworkBoundary:
    """
    Controls connectivity between cluster partitions.
    """
    def __init__(self, node_ids: List[str]):
        self.node_ids = node_ids
        self.partition_groups: Dict[str, int] = {nid: 1 for nid in node_ids}
        self.is_partitioned = False

    def split_cluster(self, group_a: List[str], group_b: List[str]):
        """Splits cluster into two isolated partitions."""
        for nid in group_a:
            self.partition_groups[nid] = 1
        for nid in group_b:
            self.partition_groups[nid] = 2
        self.is_partitioned = True
        print("\n[NETWORK FAULT] [!] Network partitioned! Group A and Group B are now isolated.")

    def heal_cluster(self):
        """Heals network partition."""
        for nid in self.node_ids:
            self.partition_groups[nid] = 1
        self.is_partitioned = False
        print("\n[NETWORK HEAL] [OK] Network link restored! Partition boundary removed.")

    def can_communicate(self, sender: str, receiver: str) -> bool:
        if not self.is_partitioned:
            return True
        return self.partition_groups[sender] == self.partition_groups[receiver]


class BankNode:
    """
    Represents a database node tracking customer balance state and local log history.
    """
    def __init__(self, node_id: str, network: NetworkBoundary):
        self.node_id = node_id
        self.network = network
        self.is_leader = False
        self.balance = 1000.0  # Shared starting balance
        self.transaction_log: List[str] = ["INITIAL DEPOSIT: $1000.00"]

    def receive_heartbeat(self, leader_id: str) -> bool:
        """Checks if heartbeat from leader reaches this node."""
        return self.network.can_communicate(leader_id, self.node_id)

    def process_transaction(self, client_id: str, tx_type: str, amount: float) -> bool:
        """
        Executes a transaction locally if this node is acting as leader.
        """
        if not self.is_leader:
            print(f"  [{self.node_id}] REJECTED transaction from {client_id}: Node is not a leader!")
            return False

        if tx_type == "DEPOSIT":
            self.balance += amount
            entry = f"DEPOSIT: +${amount:.2f} (Client: {client_id})"
        elif tx_type == "WITHDRAWAL":
            if self.balance < amount:
                print(f"  [{self.node_id}] REJECTED transaction: Insufficient funds!")
                return False
            self.balance -= amount
            entry = f"WITHDRAWAL: -${amount:.2f} (Client: {client_id})"
        else:
            return False

        self.transaction_log.append(entry)
        print(f"  [{self.node_id} - LEADER] Executed {entry}. New Balance: ${self.balance:.2f}")
        return True


class SplitBrainSimulation:
    def __init__(self):
        self.node_ids = ["Node-1", "Node-2", "Node-3", "Node-4", "Node-5"]
        self.network = NetworkBoundary(self.node_ids)
        self.nodes: Dict[str, BankNode] = {nid: BankNode(nid, self.network) for nid in self.node_ids}

    def run(self):
        print("=" * 75)
        print(" DAY 8 SIMULATION 2: SPLIT BRAIN & DATA CORRUPTION SIMULATION ")
        print("=" * 75)

        # -------------------------------------------------------------
        # STEP 1: Healthy Single-Leader Cluster
        # -------------------------------------------------------------
        print("\n--- STEP 1: INITIAL HEALTHY CLUSTER STATE ---")
        self.nodes["Node-1"].is_leader = True
        print("Node-1 is designated as the sole cluster leader.")
        print(f"All 5 nodes agree: Account Balance = ${self.nodes['Node-1'].balance:.2f}")

        # -------------------------------------------------------------
        # STEP 2: Network Partition Occurs
        # -------------------------------------------------------------
        print("\n--- STEP 2: NETWORK PARTITION OCCURS ---")
        # Subnet A = [Node-1, Node-2], Subnet B = [Node-3, Node-4, Node-5]
        self.network.split_cluster(["Node-1", "Node-2"], ["Node-3", "Node-4", "Node-5"])

        # -------------------------------------------------------------
        # STEP 3: Emergence of Dual Leaders (Split Brain)
        # -------------------------------------------------------------
        print("\n--- STEP 3: EMERGENCE OF DUAL LEADERS (SPLIT BRAIN) ---")
        print("  - Partition A (Node-1, Node-2): Node-1 continues serving as Leader.")
        print("  - Partition B (Node-3, Node-4, Node-5): Heartbeats from Node-1 fail!")
        print("  Partition B nodes assume Node-1 is DEAD. They elect Node-3 as their new Leader!")
        
        self.nodes["Node-3"].is_leader = True
        
        print("\n[!] WARNING: SPLIT BRAIN STATE ACTIVE!")
        print("  - Partition A Leader: Node-1")
        print("  - Partition B Leader: Node-3")
        print("  Both leaders are healthy, alive, and actively processing writes!")

        # -------------------------------------------------------------
        # STEP 4: Independent Conflicting Write Operations
        # -------------------------------------------------------------
        print("\n--- STEP 4: CONCURRENT WRITES TO ISOLATED LEADERS ---")
        print("\nClient 1 connects to Partition A (Node-1) and DEPOSITS $500.00:")
        self.nodes["Node-1"].process_transaction("Client-1", "DEPOSIT", 500.0)

        print("\nClient 2 connects to Partition B (Node-3) and WITHDRAWS $800.00:")
        self.nodes["Node-3"].process_transaction("Client-2", "WITHDRAWAL", 800.0)

        # Propagate within partition subnets
        self.nodes["Node-2"].balance = self.nodes["Node-1"].balance
        self.nodes["Node-2"].transaction_log = list(self.nodes["Node-1"].transaction_log)

        for nid in ["Node-4", "Node-5"]:
            self.nodes[nid].balance = self.nodes["Node-3"].balance
            self.nodes[nid].transaction_log = list(self.nodes["Node-3"].transaction_log)

        # -------------------------------------------------------------
        # STEP 5: Inspecting Irreconcilable Divergent State
        # -------------------------------------------------------------
        print("\n--- STEP 5: CLUSTER STATE DIVERGENCE SUMMARY ---")
        print("Partition A State (Nodes 1 & 2):")
        print(f"  - Calculated Balance: ${self.nodes['Node-1'].balance:.2f}")
        print(f"  - Transaction Log: {self.nodes['Node-1'].transaction_log}")
        
        print("\nPartition B State (Nodes 3, 4 & 5):")
        print(f"  - Calculated Balance: ${self.nodes['Node-3'].balance:.2f}")
        print(f"  - Transaction Log: {self.nodes['Node-3'].transaction_log}")

        # -------------------------------------------------------------
        # STEP 6: Network Heals & Crisis Manifests
        # -------------------------------------------------------------
        print("\n--- STEP 6: NETWORK RESTORATION & RECONCILIATION CRISIS ---")
        self.network.heal_cluster()

        print("\nThe network cable is repaired. Nodes 1 and 3 attempt to sync state:")
        print(f"  - Node-1 log: {self.nodes['Node-1'].transaction_log}")
        print(f"  - Node-3 log: {self.nodes['Node-3'].transaction_log}")
        
        print("\n[CRITICAL FAILURE] IRRECONCILABLE DATA CONFLICT DETECTED!")
        print("  - If we pick Node-1's state ($1,500), Client 2's withdrawal of $800 is ERASED (Lost Write).")
        print("  - If we pick Node-3's state ($200), Client 1's deposit of $500 is ERASED (Lost Money).")
        print("  - If we try to replay both ($1000 + $500 - $800 = $700), order of execution was NEVER agreed upon!")
        print("  - Both systems were completely healthy, but operating simultaneously created silent corruption.")
        
        print("\n" + "=" * 75)
        print(" LESSON: Two healthy systems are far more dangerous than one failed system. ")
        print("=" * 75)


if __name__ == "__main__":
    simulation = SplitBrainSimulation()
    simulation.run()
