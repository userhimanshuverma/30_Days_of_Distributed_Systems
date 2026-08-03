"""
network_partition_demo.py - Simulating Network Partitions in a 5-Node Cluster

This educational script demonstrates how a physical network failure can break a 
single 5-node cluster into two isolated network partitions (subnets).

Key Concepts Demonstrated:
1. Complete Topology: Nodes usually communicate freely over a shared network mesh.
2. Partition Injection: A network fault breaks communication between specific node subsets.
3. Asymmetric Visibility: Nodes in Partition A can talk to each other, and nodes in 
   Partition B can talk to each other, but messages between Partition A and Partition B fail.
4. Silence vs. Crash: No machine crashed! Disks, CPU, and memory are 100% healthy on all 5 nodes.
   The ONLY failure is the communication link between them.
"""

from typing import Dict, List, Set, Tuple
import time


class NetworkMesh:
    """
    Simulates a virtual network switch connecting distributed nodes.
    Supports isolating subsets of nodes to simulate network partitions.
    """
    def __init__(self, node_ids: List[str]):
        self.node_ids = node_ids
        # Track active partitions. If empty, all nodes can talk to all nodes.
        # Otherwise, maps node_id -> partition_group_id
        self.partition_map: Dict[str, int] = {nid: 1 for nid in node_ids}
        self.is_partitioned = False

    def heal_network(self) -> None:
        """Restores full connectivity across all nodes."""
        for nid in self.node_ids:
            self.partition_map[nid] = 1
        self.is_partitioned = False
        print("\n[NETWORK EVENT] [OK] Network healed. All nodes can communicate again.")

    def create_partition(self, group1: List[str], group2: List[str]) -> None:
        """
        Splits the network into two isolated partitions.
        Group 1 nodes can only talk to Group 1.
        Group 2 nodes can only talk to Group 2.
        """
        for nid in group1:
            self.partition_map[nid] = 1
        for nid in group2:
            self.partition_map[nid] = 2
        self.is_partitioned = True
        print("\n[NETWORK EVENT] [!] NETWORK PARTITION CREATED!")
        print(f"  |-- Isolated Group A: {group1}")
        print(f"  +-- Isolated Group B: {group2}")

    def can_send(self, sender_id: str, receiver_id: str) -> bool:
        """
        Returns True if the network allows a message to pass from sender to receiver.
        """
        if not self.is_partitioned:
            return True
        return self.partition_map.get(sender_id) == self.partition_map.get(receiver_id)


class ClusterNode:
    """
    Represents an individual node in the cluster with healthy hardware.
    """
    def __init__(self, node_id: str, network: NetworkMesh):
        self.node_id = node_id
        self.network = network
        self.health_status = "HEALTHY (CPU: 2%, RAM: 15%, Disk: OK)"

    def send_message(self, target_id: str, message: str) -> bool:
        """
        Attempts to send a network packet to target_id.
        """
        print(f"  [{self.node_id}] Sending '{message}' to [{target_id}]...")
        if self.network.can_send(self.node_id, target_id):
            print(f"    +-- [SUCCESS]: [{target_id}] received message.")
            return True
        else:
            print(f"    +-- [NETWORK DROP]: Packet to [{target_id}] timed out! (Unreachable link)")
            return False


def run_partition_demo():
    print("=" * 70)
    print(" DAY 8 SIMULATION 1: DEMONSTRATING A NETWORK PARTITION ")
    print("=" * 70)
    
    node_ids = ["Node-1", "Node-2", "Node-3", "Node-4", "Node-5"]
    network = NetworkMesh(node_ids)
    
    # Instantiate 5 healthy nodes
    nodes = {nid: ClusterNode(nid, network) for nid in node_ids}
    
    print("\n--- PHASE 1: HEALTHY CLUSTER NETWORK ---")
    print("All 5 machines are running fine. Testing cross-cluster communications...")
    nodes["Node-1"].send_message("Node-2", "Heartbeat Ping")
    nodes["Node-1"].send_message("Node-5", "Heartbeat Ping")
    
    print("\n--- PHASE 2: SIMULATING CROSS-DATACENTER FIBER CUT ---")
    # Partition cluster into Group A: Node-1, Node-2 and Group B: Node-3, Node-4, Node-5
    network.create_partition(group1=["Node-1", "Node-2"], group2=["Node-3", "Node-4", "Node-5"])
    
    print("\n--- PHASE 3: TESTING COMMUNICATION INSIDE & ACROSS PARTITIONS ---")
    
    print("\n1. Internal Group A communication (Node-1 to Node-2):")
    nodes["Node-1"].send_message("Node-2", "Internal Ping")
    
    print("\n2. Internal Group B communication (Node-3 to Node-4):")
    nodes["Node-3"].send_message("Node-4", "Internal Ping")
    
    print("\n3. Cross-partition communication (Node-1 to Node-3):")
    nodes["Node-1"].send_message("Node-3", "Cross-partition Heartbeat")
    
    print("\n4. Cross-partition communication (Node-5 to Node-1):")
    nodes["Node-5"].send_message("Node-1", "Cross-partition Heartbeat")
    
    print("\n--- CRITICAL OBSERVATION ---")
    print("Notice the health status of all nodes:")
    for nid, node in nodes.items():
        print(f"  - {nid}: {node.health_status}")
    print("\nEvery single server is completely healthy and functioning correctly.")
    print("However, because communication across the boundary is severed, nodes on each side")
    print("cannot distinguish between a failed remote server and a failed network link!")
    print("=" * 70)


if __name__ == "__main__":
    run_partition_demo()
