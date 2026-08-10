"""
Day 15 — Eventual Consistency Simulator

An educational Python simulation demonstrating eventual consistency in a 3-replica
distributed system.

Key concepts demonstrated:
- Single write applied to a primary/entry replica first (t=1).
- Asynchronous replication propagation delay to secondary replicas (t=2, t=3).
- Temporary read divergence (different users reading different replicas see different state).
- Eventual convergence (all replicas reach identical state when updates pause).

No external dependencies required (uses standard library).
"""

import sys
from typing import Dict, List


class Replica:
    """Represents a single database replica in a distributed cluster."""

    def __init__(self, name: str):
        self.name = name
        # Data store mapping post_id -> like_status (Boolean)
        self.store: Dict[str, bool] = {}
        # Simulated incoming queue of replication messages: (post_id, value, deliver_at_tick)
        self.replication_queue: List[dict] = []

    def read(self, post_id: str) -> bool:
        """Read current state from this replica."""
        return self.store.get(post_id, False)

    def write_direct(self, post_id: str, value: bool):
        """Directly write state to this replica (client update)."""
        self.store[post_id] = value

    def enqueue_replication(self, post_id: str, value: bool, deliver_at_tick: int):
        """Enqueue a replication packet to be processed at a future tick."""
        self.replication_queue.append({
            "post_id": post_id,
            "value": value,
            "deliver_at_tick": deliver_at_tick
        })

    def process_tick(self, current_tick: int) -> List[str]:
        """Process any queued replication messages scheduled for current_tick."""
        applied_updates = []
        remaining_queue = []
        for item in self.replication_queue:
            if item["deliver_at_tick"] <= current_tick:
                self.store[item["post_id"]] = item["value"]
                applied_updates.append(f"Replica {self.name} applied update: {item['post_id']} = {item['value']}")
            else:
                remaining_queue.append(item)
        self.replication_queue = remaining_queue
        return applied_updates


class DistributedLikeService:
    """Simulates a multi-replica social network like system demonstrating eventual consistency."""

    def __init__(self):
        self.replicas = {
            "A": Replica("A"),
            "B": Replica("B"),
            "C": Replica("C"),
        }
        self.current_tick = 0

    def write_like(self, post_id: str, target_replica: str = "A", delay_b_ticks: int = 1, delay_c_ticks: int = 2):
        """
        Simulate a user clicking 'Like' served by `target_replica`.
        Replication packets are dispatched asynchronously with scheduled propagation delays.
        """
        print(f"\n[EVENT] User clicks LIKE on post '{post_id}' -> Served by Replica {target_replica}")
        # Immediate update on entry replica
        self.replicas[target_replica].write_direct(post_id, True)

        # Asynchronous propagation to Replica B and C
        if target_replica != "B":
            self.replicas["B"].enqueue_replication(post_id, True, self.current_tick + delay_b_ticks)
        if target_replica != "C":
            self.replicas["C"].enqueue_replication(post_id, True, self.current_tick + delay_c_ticks)

    def advance_tick(self):
        """Advance simulation clock by 1 tick and process pending replication queues."""
        self.current_tick += 1
        print(f"\n--- TICK t={self.current_tick} ---")
        updates_applied = []
        for replica in self.replicas.values():
            logs = replica.process_tick(self.current_tick)
            updates_applied.extend(logs)

        if updates_applied:
            for log in updates_applied:
                print(f"  [UPDATE] {log}")
        else:
            print("  [INFO] No network packets arrived in this tick.")

    def read_all_replicas(self, post_id: str) -> Dict[str, bool]:
        """Read post status across all replicas."""
        return {name: r.read(post_id) for name, r in self.replicas.items()}

    def display_cluster_state(self, post_id: str, client_views: List[tuple] = None):
        """Display visual status matrix of the cluster at current tick."""
        states = self.read_all_replicas(post_id)
        
        # Check convergence
        values = list(states.values())
        all_equal = len(set(values)) == 1

        print(f"\n[CLUSTER STATE at t={self.current_tick}]")
        for replica_name, liked in states.items():
            icon = "[LIKE HEART] (True)" if liked else "[EMPTY HEART] (False)"
            print(f"   * Replica {replica_name}: {icon}")

        if client_views:
            print("\n[CLIENT READ OBSERVATIONS]")
            for user_name, replica_choice in client_views:
                val = states[replica_choice]
                icon = "Liked (True)" if val else "Not Liked (False)"
                print(f"   * User '{user_name}' reading from Replica {replica_choice} -> sees {icon}")

        if all_equal:
            print("  ==> STATUS: EVENTUAL CONVERGENCE ACHIEVED (All replicas agree)")
        else:
            print("  ==> STATUS: TEMPORARY DIVERGENCE (Replicas disagree due to propagation delay)")


def run_simulation():
    """Runs a step-by-step deterministic demonstration of eventual consistency."""
    # Ensure stdout handles UTF-8 gracefully if available
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    print("==================================================================")
    print(" Day 15 Simulation: Eventual Consistency & Replica Divergence")
    print("==================================================================")

    post_id = "post_101"
    cluster = DistributedLikeService()

    # t = 0 : Initial State
    print("\n--- TICK t=0 ---")
    print("  [INFO] Initial cluster state before any action.")
    cluster.display_cluster_state(
        post_id,
        client_views=[("Alice", "A"), ("Bob", "B"), ("Charlie", "C")]
    )

    # User Alice likes post_101 at t=0, writing to Replica A.
    # Replica B receives update at t=1 (delay 1 tick).
    # Replica C receives update at t=2 (delay 2 ticks).
    cluster.write_like(post_id, target_replica="A", delay_b_ticks=1, delay_c_ticks=2)

    # t = 1 : Alice updated Replica A, but B & C are catching up
    cluster.advance_tick()
    cluster.display_cluster_state(
        post_id,
        client_views=[("Alice", "A"), ("Bob", "B"), ("Charlie", "C")]
    )

    # t = 2 : Replica B caught up, Replica C still lagging
    cluster.advance_tick()
    cluster.display_cluster_state(
        post_id,
        client_views=[("Alice", "A"), ("Bob", "B"), ("Charlie", "C")]
    )

    # t = 3 : Replica C catches up -> Full convergence
    cluster.advance_tick()
    cluster.display_cluster_state(
        post_id,
        client_views=[("Alice", "A"), ("Bob", "B"), ("Charlie", "C")]
    )

    print("\n==================================================================")
    print(" Key Takeaways:")
    print(" 1. At t=1, Alice saw 'Liked' on Replica A, while Bob saw 'Not Liked' on Replica B.")
    print(" 2. The system was NOT broken - it was in a temporary divergence window.")
    print(" 3. By t=3, after updates stopped, all replicas converged to 'Liked'.")
    print("==================================================================")


if __name__ == "__main__":
    run_simulation()
