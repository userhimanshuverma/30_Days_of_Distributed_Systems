"""
heartbeat_simulation.py - Educational Simulation of Cluster Node Heartbeats

This script simulates a 5-node cluster monitored by a central NodeMonitor:
1. Five nodes (node-1 through node-5) send periodic heartbeats every 1.0 second.
2. At time t = 3.0s, node-3 suddenly fails (e.g., power loss or network disconnection)
   and stops sending heartbeats.
3. The cluster monitor evaluates node health at each tick.
4. The monitor observes missing heartbeats, transitions node-3 to SUSPECTED,
   and finally marks node-3 UNHEALTHY once the 3.0s timeout threshold is exceeded.

Run this script directly:
    python heartbeat_simulation.py
"""

import time
from node_monitor import NodeMonitor, HeartbeatPayload, NodeState


class SimulatedNode:
    """
    Represents an individual node in the cluster capable of sending heartbeats.
    """
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.sequence_number = 0
        self.is_alive = True

    def produce_heartbeat(self, current_time: float) -> HeartbeatPayload:
        """Generates a new HeartbeatPayload and increments the sequence counter."""
        self.sequence_number += 1
        return HeartbeatPayload(
            node_id=self.node_id,
            timestamp=current_time,
            sequence_number=self.sequence_number
        )


def run_heartbeat_simulation():
    print("=" * 75)
    print("DAY 9 SIMULATION: DISTRIBUTED CLUSTER HEARTBEAT MONITORING")
    print("=" * 75)
    print("Configuration:")
    print("  - Total Cluster Nodes: 5 (node-1, node-2, node-3, node-4, node-5)")
    print("  - Heartbeat Interval:  1.0 second")
    print("  - Failure Timeout:     3.0 seconds")
    print("  - Scheduled Event:     node-3 crashes at t = 3.0s")
    print("=" * 75)
    print()

    # Initialize 5 nodes
    node_ids = [f"node-{i}" for i in range(1, 6)]
    nodes = {nid: SimulatedNode(nid) for nid in node_ids}

    # Initialize central cluster monitor (1.0s interval, 3.0s timeout, 1 missed beat for SUSPECTED)
    monitor = NodeMonitor(heartbeat_interval=1.0, timeout_threshold=3.0, max_missed_heartbeats=1)

    # Register all nodes at simulation start (t = 0.0)
    simulated_clock = 0.0
    for nid in node_ids:
        monitor.register_node(nid, current_time=simulated_clock)

    print(f"--- [t = {simulated_clock:.1f}s] Cluster Initialized: All 5 nodes registered as HEALTHY ---")
    print()

    # Execute discrete time step ticks (0.0s to 7.0s)
    total_ticks = 8
    for tick in range(1, total_ticks):
        simulated_clock = float(tick)
        print(f"---------------------------------------------------------------------------")
        print(f"[CLOCK] t = {simulated_clock:.1f}s")
        print(f"---------------------------------------------------------------------------")

        # Inject Failure Scenario: node-3 stops sending heartbeats at t >= 3.0s
        if simulated_clock >= 3.0:
            if nodes["node-3"].is_alive:
                print(" [EVENT] node-3 experienced a total failure! (Power cut / network drop)")
                nodes["node-3"].is_alive = False

        # Phase 1: Alive nodes dispatch heartbeats to the monitor
        print(" [SEND] Dispatching Heartbeats:")
        for nid, node in nodes.items():
            if node.is_alive:
                hb = node.produce_heartbeat(simulated_clock)
                monitor.receive_heartbeat(hb)
                print(f"    OK  {nid} -> Sent Heartbeat (seq={hb.sequence_number})")
            else:
                print(f"   FAIL {nid} -> [SILENT] No heartbeat emitted!")

        # Phase 2: Central monitor checks and evaluates node health
        print("\n [CHECK] Monitor Health Check & State Evaluation:")
        states = monitor.check_all_nodes(current_time=simulated_clock)

        # Print current summary table of cluster states
        print("\n [STATUS TABLE]")
        for nid in sorted(states.keys()):
            state = states[nid]
            missed = monitor.missed_counts[nid]
            last_seen = monitor.last_heartbeat_time[nid]
            elapsed = simulated_clock - last_seen
            status_tag = "[HEALTHY]" if state == NodeState.HEALTHY else (" [SUSPECT]" if state == NodeState.SUSPECTED else "  [DEAD] ")
            print(f"  {status_tag} {nid:7s} | State: {state.name:9s} | Last Seen: {elapsed:3.1f}s ago | Missed Beats: {missed}")

        print()
        time.sleep(0.05)

    print("=" * 75)
    print("SIMULATION CONCLUSION:")
    print("  - Nodes 1, 2, 4, and 5 continuously delivered heartbeats and remained HEALTHY.")
    print("  - Node-3 missed heartbeats at t=3.0s, was SUSPECTED at t=4.0s (missed beats = 1),")
    print("    and declared UNHEALTHY (DEAD) at t=6.0s once the 3.0s timeout was exceeded.")
    print("  - Notice that the cluster did not instantly panic on the first missing message;")
    print("    it gave time for potential network jitter before declaring failure.")
    print("=" * 75)


if __name__ == "__main__":
    run_heartbeat_simulation()
