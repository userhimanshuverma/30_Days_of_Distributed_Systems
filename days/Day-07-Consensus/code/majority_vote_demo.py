"""
majority_vote_demo.py - Interactive Demonstration of Consensus in Action

This script runs two realistic production scenarios using the ConsensusCluster simulation:

Scenario 1: Successful Consensus
- Cluster of 5 nodes with Node-1 as Leader.
- Leader proposes creating a Kubernetes deployment 'web-app-v2'.
- 4 out of 5 nodes respond (Majority achieved: 4 >= 3).
- Decision is committed and applied across the cluster.

Scenario 2: Failed Consensus (Network Partition / Node Failures)
- Network issues disable 3 nodes (Node-3, Node-4, Node-5).
- Leader proposes updating database config 'max_connections=500'.
- Only 2 nodes respond (Node-1, Node-2).
- Majority is NOT achieved (2 < 3).
- Proposal is safely rejected, preventing inconsistent cluster state.
"""

from simple_consensus import ConsensusCluster


def run_successful_consensus_demo():
    print("=" * 70)
    print("SCENARIO 1: SUCCESSFUL CONSENSUS (4 / 5 Nodes Active)")
    print("=" * 70)
    
    # 5 nodes in total (Node-1 is the leader)
    nodes = ["node-1", "node-2", "node-3", "node-4", "node-5"]
    cluster = ConsensusCluster(node_ids=nodes, leader_id="node-1")

    # Simulate 1 node experiencing mild transient delay, but 4 nodes online
    cluster.set_node_network_status("node-5", is_reachable=False)

    # Propose an operation
    success = cluster.propose_action(
        proposal_id="prop-001",
        action="kubectl create deployment web-app --image=nginx:1.25"
    )

    print(f"\nResult: {'SUCCESS' if success else 'FAILURE'}")
    print("State verification across cluster:")
    for node_id, node in cluster.nodes.items():
        print(f"  [{node_id}] Log: {node.committed_log}")


def run_failed_consensus_demo():
    print("\n" + "=" * 70)
    print("SCENARIO 2: FAILED CONSENSUS DUE TO NETWORK PARTITION (2 / 5 Nodes Active)")
    print("=" * 70)
    
    nodes = ["node-1", "node-2", "node-3", "node-4", "node-5"]
    cluster = ConsensusCluster(node_ids=nodes, leader_id="node-1")

    # Simulate network partition disconnecting Node-3, Node-4, Node-5
    print("\n[WARNING] Network Partition Occurs! Cutting off 3 nodes from the Leader...")
    cluster.set_node_network_status("node-3", is_reachable=False)
    cluster.set_node_network_status("node-4", is_reachable=False)
    cluster.set_node_network_status("node-5", is_reachable=False)

    # Leader attempts to propose a critical cluster state change
    success = cluster.propose_action(
        proposal_id="prop-002",
        action="kubectl scale deployment web-app --replicas=10"
    )

    print(f"\nResult: {'SUCCESS' if success else 'FAILURE (Safely Rejected)'}")
    print("State verification across cluster:")
    for node_id, node in cluster.nodes.items():
        print(f"  [{node_id}] Log: {node.committed_log}")


if __name__ == "__main__":
    run_successful_consensus_demo()
    run_failed_consensus_demo()
