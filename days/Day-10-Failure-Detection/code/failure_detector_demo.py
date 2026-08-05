"""
failure_detector_demo.py - Interactive Simulation of Failure Detection Under Uncertainty

This educational simulation demonstrates how a cluster detects node failure:
1. Multiple nodes (node-1, node-2, node-3, node-4) send periodic heartbeats every 1.0 second.
2. At time t = 2.0s, node-2 stops sending heartbeats (simulating a crash, network partition, or OS freeze).
3. The cluster failure detector monitors nodes at each tick:
   - At t = 2.0s: node-2 misses its first heartbeat -> State becomes SUSPECTED.
   - At t = 3.0s & t = 4.0s: Silence duration counter increases.
   - At t = 5.0s: Silence reaches the 3.0s timeout threshold -> Node-2 declared FAILED.
4. Recovery pipeline is triggered to reschedule workloads from node-2 onto healthy nodes.

Key Insight:
The cluster NEVER receives a message saying "node-2 has died". It acts purely
because its confidence in node-2 being alive has dropped below an acceptable threshold.

Run this script directly:
    python failure_detector_demo.py
"""

import time
from heartbeat_timeout import FailureDetector, Heartbeat, NodeStatus


class SimulatedNode:
    """
    Models a cluster worker node capable of generating heartbeats or being silenced.
    """
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.sequence_number = 0
        self.is_silent = False  # Set to True to simulate crash/freeze/disconnection

    def produce_heartbeat(self, current_time: float) -> Heartbeat:
        """Generates a heartbeat packet if the node is actively transmitting."""
        self.sequence_number += 1
        return Heartbeat(
            node_id=self.node_id,
            timestamp=current_time,
            sequence_number=self.sequence_number
        )


def trigger_cluster_recovery(failed_node_id: str) -> None:
    """
    Simulated recovery procedure executed when a node is declared FAILED.
    """
    print(f"\n  [ACTION REQUIRED] RECOVERY PIPELINE TRIGGERED")
    print(f"     1. Removing '{failed_node_id}' from active load balancer pool.")
    print(f"     2. Rescheduling pods/tasks from '{failed_node_id}' to active healthy nodes.")
    print(f"     3. Cluster state updated: Operating safely with remaining healthy nodes.\n")


def run_failure_detection_simulation():
    print("=" * 80)
    print("DAY 10 SIMULATION: FAILURE DETECTION & UNCERTAINTY IN DISTRIBUTED SYSTEMS")
    print("=" * 80)
    print("Configuration:")
    print("  - Cluster Nodes:        node-1, node-2, node-3, node-4")
    print("  - Heartbeat Interval:   1.0 second")
    print("  - Timeout Threshold:    3.0 seconds")
    print("  - Scheduled Event:      node-2 suddenly stops sending heartbeats at t = 2.0s")
    print("=" * 80)
    print()

    node_ids = ["node-1", "node-2", "node-3", "node-4"]
    nodes = {nid: SimulatedNode(nid) for nid in node_ids}

    # Initialize Failure Detector with 1.0s heartbeat interval, 3.0s timeout threshold
    detector = FailureDetector(
        heartbeat_interval=1.0,
        timeout_threshold=3.0,
        on_failure_callback=trigger_cluster_recovery
    )

    # Register all nodes at simulation time t = 0.0s
    simulated_time = 0.0
    for nid in node_ids:
        detector.register_node(nid, current_time=simulated_time)

    # Run discrete time step simulation (tick = 1.0s)
    simulation_steps = 7
    for step in range(simulation_steps):
        print(f"--- TICK {step}: Time = {simulated_time:.1f}s ---")

        # Inject failure event: node-2 goes silent at t = 2.0s (step 2)
        if step == 2:
            print("  [EVENT] node-2 has stopped responding! (Simulating OS Hang / Network Partition / Crash)")
            nodes["node-2"].is_silent = True

        # Healthy nodes transmit heartbeats
        for nid, node in nodes.items():
            if not node.is_silent:
                hb = node.produce_heartbeat(simulated_time)
                detector.receive_heartbeat(hb)
                print(f"  [RECEIVED] {hb}")
            else:
                print(f"  [SILENCE] No heartbeat received from {nid}")

        # Failure detector evaluates cluster status
        print("\n  [EVALUATING] Checking Node Health:")
        states = detector.evaluate_nodes(simulated_time)

        # Print current summary table
        print("\n  Current Cluster Overview:")
        for nid in node_ids:
            st = states[nid].value
            silence = detector.silence_duration.get(nid, 0.0)
            print(f"    - {nid:<8}: Status = {st:<10} | Silence Duration = {silence:.1f}s")
        print()

        # Advance clock by 1 second
        simulated_time += 1.0
        time.sleep(0.1)  # Brief delay for terminal readability

    print("=" * 80)
    print("SIMULATION SUMMARY & LESSON:")
    print("Notice how the cluster NEVER received a message confirming node-2 died.")
    print("It observed 3.0 seconds of silence, crossed its timeout threshold, and made")
    print("the best possible decision with incomplete information under uncertainty.")
    print("=" * 80)


if __name__ == "__main__":
    run_failure_detection_simulation()
