"""
leader_demo.py - Leader Election Role & Coordination Simulation

Demonstrates:
1. Five server nodes joining a cluster.
2. Designation of Node-1 as the initial Leader.
3. Followers forwarding task requests to the Leader for central coordination.
4. The Leader crashing/stopping, leaving the cluster without coordination.
5. Placeholder warning for tomorrow's topic: How the cluster elects a new leader!

Usage:
    python leader_demo.py
"""

from simple_cluster import Cluster, Node, Task


def main():
    print("=" * 75)
    print(" DAY 6: LEADER ELECTION - DEMONSTRATING CLUSTER ROLES & COORDINATION")
    print("=" * 75)

    # 1. Five nodes joining a cluster
    print("\n--- Phase 1: Cluster Initialization ---")
    cluster = Cluster()
    node_ids = ["Node-1", "Node-2", "Node-3", "Node-4", "Node-5"]
    
    for nid in node_ids:
        cluster.add_node(Node(nid))

    # 2. One node becoming the leader
    print("\n--- Phase 2: Designating the Initial Leader ---")
    # Initial setup: Node-1 is appointed as leader
    cluster.set_leader("Node-1")

    # 3. Followers forwarding coordination tasks to the leader
    print("\n--- Phase 3: Client Submissions & Leader Coordination ---")
    
    task1 = Task("JOB-101", "Reschedule failed batch ETL worker #4")
    # Client sends request to Node-3 (a Follower)
    cluster.send_task_to_node("Node-3", task1)

    task2 = Task("JOB-102", "Allocate IP address block to new Pod")
    # Client sends request to Node-5 (a Follower)
    cluster.send_task_to_node("Node-5", task2)

    task3 = Task("JOB-103", "Commit schema migration lock")
    # Client sends request directly to Node-1 (the Leader)
    cluster.send_task_to_node("Node-1", task3)

    # 4. Simulate the leader stopping
    print("\n--- Phase 4: Simulating Leader Failure ---")
    print("[LEADER CRASH] Node-1 (the Leader) dies unexpectedly!")
    leader_node = cluster.nodes["Node-1"]
    leader_node.stop()

    # Attempting to send a new task to Node-2 (Follower) while the Leader is dead
    task4 = Task("JOB-104", "Provision replacement worker instance")
    success = cluster.send_task_to_node("Node-2", task4)

    if not success:
        print("\n[CRITICAL FAILURE] Task 'JOB-104' could not be coordinated!")
        print("   The cluster is in an UNCOORDINATED state because the Leader is down.")

    # 5. End with a placeholder indicating tomorrow's topic
    print("\n" + "=" * 75)
    print(" WHAT HAPPENS NEXT?")
    print("=" * 75)
    print(" Without a Leader, no node can make authoritative decisions.")
    print(" If every follower tries to make decisions independently, split-brain occurs.")
    print(" If followers do nothing, the system comes to a complete standstill.")
    print("\n NEXT LESSON PLACEHOLDER:")
    print("    Tomorrow, we will explore how the remaining followers detect the failure")
    print("    and automatically choose a NEW LEADER to restore cluster coordination!")
    print("=" * 75)


if __name__ == "__main__":
    main()
