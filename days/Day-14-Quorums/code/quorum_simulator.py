"""
Day 14 — Quorums: Why 2 of 3 Votes Matter
Miniature Replicated Key-Value Store Quorum Simulator

This script simulates a leaderless distributed key-value cluster to demonstrate:
- Configurable Read (R) and Write (W) quorums across N replicas.
- Quorum intersection (W + R > N) ensuring read freshness.
- Fault tolerance when replicas become unavailable or lag.
- Quorum failure handling when insufficient ACKs are received.
- Basic Read Repair mechanism when stale data is detected during a read quorum.
"""

import time
from typing import Dict, Any, List, Optional, Tuple


class StoredRecord:
    """Represents a versioned data record stored on a replica node."""
    def __init__(self, value: Any, timestamp: float, version: int):
        self.value = value
        self.timestamp = timestamp
        self.version = version

    def __repr__(self) -> str:
        return f"Record(val={self.value!r}, v={self.version}, t={self.timestamp:.2f})"


class ReplicaNode:
    """
    Simulates an individual database replica node.
    Can be marked offline to simulate network partitions or crashes.
    """
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.storage: Dict[str, StoredRecord] = {}
        self.is_online = True
        self.latency_ms = 10  # Simulated network latency

    def write(self, key: str, value: Any, timestamp: float, version: int) -> bool:
        """Processes a write request if the node is online."""
        if not self.is_online:
            return False
        
        # Check if existing record is newer
        current = self.storage.get(key)
        if current and current.version >= version:
            # Reject older or duplicate write versions
            return True

        self.storage[key] = StoredRecord(value, timestamp, version)
        return True

    def read(self, key: str) -> Optional[StoredRecord]:
        """Processes a read request if the node is online."""
        if not self.is_online:
            return None
        return self.storage.get(key)


class QuorumCluster:
    """
    Simulates a leaderless distributed storage cluster using Quorum consensus.
    """
    def __init__(self, node_ids: List[str]):
        self.nodes = {nid: ReplicaNode(nid) for nid in node_ids}
        self.N = len(node_ids)
        self.key_versions: Dict[str, int] = {}

    def set_node_status(self, node_id: str, is_online: bool):
        """Toggles node availability to simulate failure or network partition."""
        if node_id in self.nodes:
            self.nodes[node_id].is_online = is_online
            status_str = "ONLINE" if is_online else "OFFLINE (Simulated Failure)"
            print(f"  [CLUSTER EVENT] Node '{node_id}' is now {status_str}")

    def write(self, key: str, value: Any, W: int) -> Tuple[bool, int, List[str]]:
        """
        Executes a Write operation with Write Quorum W.
        Returns (success: bool, acks_received: int, acknowledging_nodes: List[str]).
        """
        if W > self.N:
            raise ValueError(f"Write quorum W ({W}) cannot exceed total replicas N ({self.N})")

        # Increment logical version counter for this key
        next_version = self.key_versions.get(key, 0) + 1
        now = time.time()

        acks = []
        for node_id, node in self.nodes.items():
            if node.write(key, value, now, next_version):
                acks.append(node_id)

        acks_count = len(acks)
        is_quorum_met = acks_count >= W

        if is_quorum_met:
            self.key_versions[key] = next_version

        return is_quorum_met, acks_count, acks

    def read(self, key: str, R: int) -> Tuple[bool, Optional[Any], int, Dict[str, Optional[StoredRecord]]]:
        """
        Executes a Read operation with Read Quorum R.
        Reads from all available replicas, gathers responses, and resolves to the latest version.
        Triggers Read Repair if stale nodes are detected within the quorum response set.
        """
        if R > self.N:
            raise ValueError(f"Read quorum R ({R}) cannot exceed total replicas N ({self.N})")

        responses: Dict[str, Optional[StoredRecord]] = {}
        for node_id, node in self.nodes.items():
            record = node.read(key)
            if record is not None or node.is_online:
                responses[node_id] = record

        # Filter active responses (ignoring offline nodes that returned None due to failure)
        valid_responses = {nid: rec for nid, rec in responses.items() if rec is not None or self.nodes[nid].is_online}

        # Count nodes that answered the read request (even if key was empty on that node)
        responding_nodes = [nid for nid, rec in responses.items() if self.nodes[nid].is_online]
        acks_count = len(responding_nodes)
        is_quorum_met = acks_count >= R

        if not is_quorum_met:
            return False, None, acks_count, responses

        # Determine the latest record version from the responding quorum
        latest_record: Optional[StoredRecord] = None
        for record in responses.values():
            if record is not None:
                if latest_record is None or record.version > latest_record.version:
                    latest_record = record

        # Read Repair: update any online node in the quorum that had a stale or missing record
        if latest_record:
            for nid in responding_nodes:
                rec = responses.get(nid)
                if rec is None or rec.version < latest_record.version:
                    print(f"  [READ REPAIR] Repairing stale/missing key '{key}' on Node '{nid}' to v{latest_record.version}")
                    self.nodes[nid].write(key, latest_record.value, latest_record.timestamp, latest_record.version)

        val = latest_record.value if latest_record else None
        return True, val, acks_count, responses


def print_section(title: str):
    print(f"\n{'=' * 75}")
    print(f" {title}")
    print(f"{'=' * 75}")


def main():
    print_section("DEMO: 3-Replica Quorum Cluster (N=3, W=2, R=2)")
    
    # Initialize 3-node cluster
    cluster = QuorumCluster(["Node_A", "Node_B", "Node_C"])
    N = 3
    W = 2
    R = 2
    
    print(f"Cluster Configuration: Total Replicas N = {N}")
    print(f"Write Quorum (W) = {W}, Read Quorum (R) = {R}")
    print(f"Quorum Check (W + R > N): {W} + {R} > {N} => {W + R > N} (Guarantees Overlap!)\n")

    # -------------------------------------------------------------------------
    # SCENARIO 1: Successful Write with All Nodes Healthy
    # -------------------------------------------------------------------------
    print_section("SCENARIO 1: Successful Write (All Nodes Healthy)")
    key = "user_101:profile"
    val1 = {"name": "Alice", "city": "Tokyo"}
    
    print(f"Client executing WRITE: key='{key}', value='{val1}', W={W}")
    success, acks, ack_list = cluster.write(key, val1, W)
    print(f"Result: Success={success} | ACKs Received={acks}/{N} from {ack_list}")
    assert success, "Write should succeed when all nodes are healthy!"

    # -------------------------------------------------------------------------
    # SCENARIO 2: Read Overlap (All Nodes Healthy)
    # -------------------------------------------------------------------------
    print_section("SCENARIO 2: Successful Read Overlap")
    print(f"Client executing READ: key='{key}', R={R}")
    success, read_val, acks, responses = cluster.read(key, R)
    print(f"Result: Success={success} | Read Value={read_val} | ACKs Received={acks}")

    # -------------------------------------------------------------------------
    # SCENARIO 3: Node Failure & Tolerating 1 Offline Replica
    # -------------------------------------------------------------------------
    print_section("SCENARIO 3: One Replica Goes Down (Node_C Offline)")
    cluster.set_node_status("Node_C", is_online=False)

    val2 = {"name": "Alice", "city": "Kyoto"}
    print(f"\nClient executing WRITE: key='{key}', value='{val2}', W={W}")
    success, acks, ack_list = cluster.write(key, val2, W)
    print(f"Result: Success={success} | ACKs Received={acks}/{N} from {ack_list}")
    print(f"Notice: Write succeeded despite Node_C being OFFLINE because W=2 (Node_A & Node_B acknowledged).")

    # Read while Node_C is still down
    print(f"\nClient executing READ: key='{key}', R={R}")
    success, read_val, acks, responses = cluster.read(key, R)
    print(f"Result: Success={success} | Read Value={read_val} | ACKs Received={acks}")

    # -------------------------------------------------------------------------
    # SCENARIO 4: Replica Recovery & Read Repair
    # -------------------------------------------------------------------------
    print_section("SCENARIO 4: Node_C Recovers (Stale Data) & Read Repair")
    cluster.set_node_status("Node_C", is_online=True)
    print("Node_C missed the latest write ('Kyoto') and still holds 'Tokyo' (or missing data).")
    
    node_c_rec_before = cluster.nodes["Node_C"].read(key)
    print(f"Node_C state before Read Repair: {node_c_rec_before}")

    print(f"\nClient executing READ quorum (R={R}) across cluster:")
    success, read_val, acks, responses = cluster.read(key, R)
    print(f"Read Result: Success={success} | Value Read={read_val}")

    node_c_rec_after = cluster.nodes["Node_C"].read(key)
    print(f"Node_C state AFTER Read Repair: {node_c_rec_after}")
    assert node_c_rec_after.value == val2, "Read Repair should update Node_C!"

    # -------------------------------------------------------------------------
    # SCENARIO 5: Quorum Failure (Major Failure - 2 Nodes Offline)
    # -------------------------------------------------------------------------
    print_section("SCENARIO 5: Quorum Failure (2 of 3 Nodes Offline)")
    cluster.set_node_status("Node_B", is_online=False)
    cluster.set_node_status("Node_C", is_online=False)
    print("Only Node_A is available. 2 of 3 nodes are offline.")

    val3 = {"name": "Alice", "city": "Osaka"}
    print(f"\nClient executing WRITE: key='{key}', value='{val3}', W={W}")
    success, acks, ack_list = cluster.write(key, val3, W)
    print(f"Result: Success={success} | ACKs Received={acks}/{N} from {ack_list}")
    print("Outcome: WRITE FAILED! Quorum cannot be satisfied (1 ACK < W=2 required).")
    print("System chooses CONSISTENCY/DURABILITY over false availability.")

    print_section("DEMO COMPLETE — Quorum Mechanics Successfully Verified!")


if __name__ == "__main__":
    main()
