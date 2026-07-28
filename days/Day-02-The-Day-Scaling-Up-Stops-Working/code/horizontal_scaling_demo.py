"""
Day 2: The Day Scaling Up Stops Working
File: horizontal_scaling_demo.py

Description:
This script demonstrates the fundamental intuition behind Horizontal Scaling (Scaling Out).
Instead of buying an increasingly expensive supercomputer, horizontal scaling spreads the
incoming workload across multiple smaller, low-cost commodity servers working together.

Intuition:
- A single commodity server has modest CPU and memory capacity.
- By adding identical commodity servers in parallel, total system capacity grows LINEARLY.
- Work is shared among servers, keeping CPU utilization low and latency stable.
- Hardware costs scale linearly instead of exponentially.
"""

import time
import random
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class CommodityServerNode:
    node_id: int
    name: str
    max_ops_per_sec: float = 800.0  # Modest capacity per server
    monthly_cost_usd: float = 50.0  # Low cost per server

    def process_traffic_share(self, assigned_rps: float) -> Dict[str, float]:
        """
        Calculates how a single commodity node handles its assigned share of traffic.
        """
        utilization = assigned_rps / self.max_ops_per_sec
        base_latency_ms = 12.0

        if utilization < 0.85:
            # Healthy operation
            queuing_delay = base_latency_ms * (1.0 / (1.0 - utilization))
            avg_latency_ms = queuing_delay
            dropped_requests = 0
            status = "HEALTHY"
        elif utilization <= 1.0:
            # High load
            avg_latency_ms = base_latency_ms * 4.0
            dropped_requests = 0
            status = "HEAVY LOAD"
        else:
            # Overloaded node
            avg_latency_ms = base_latency_ms * 20.0
            total_reqs = int(assigned_rps)
            successful = int(self.max_ops_per_sec)
            dropped_requests = total_reqs - successful
            status = "OVERLOADED"

        return {
            "assigned_rps": round(assigned_rps, 1),
            "utilization_pct": min(100.0, utilization * 100.0),
            "avg_latency_ms": round(avg_latency_ms, 2),
            "dropped_requests": dropped_requests,
            "status": status,
        }


class HorizontalClusterSimulator:
    """
    Simulates a cluster of commodity servers sharing a total workload.
    """

    def __init__(self, node_count: int):
        self.nodes = [
            CommodityServerNode(node_id=i + 1, name=f"Node-{i + 1:02d}")
            for i in range(node_count)
        ]

    @property
    def total_monthly_cost(self) -> float:
        return sum(node.monthly_cost_usd for node in self.nodes)

    def distribute_and_process(self, total_traffic_rps: float) -> Dict[str, float]:
        """
        Conceptually divides total incoming traffic across all available nodes in the cluster.
        (Conceptual distribution - no complex load balancing math yet!)
        """
        node_count = len(self.nodes)
        rps_per_node = total_traffic_rps / node_count

        node_results = []
        total_dropped = 0
        latencies = []

        for node in self.nodes:
            res = node.process_traffic_share(rps_per_node)
            node_results.append(res)
            total_dropped += res["dropped_requests"]
            latencies.append(res["avg_latency_ms"])

        avg_cluster_latency = sum(latencies) / len(latencies)
        avg_utilization = sum(r["utilization_pct"] for r in node_results) / len(node_results)

        return {
            "node_count": node_count,
            "rps_per_node": round(rps_per_node, 1),
            "avg_utilization_pct": round(avg_utilization, 1),
            "avg_cluster_latency_ms": round(avg_cluster_latency, 2),
            "total_dropped_requests": total_dropped,
            "total_monthly_cost": self.total_monthly_cost,
            "per_node_breakdown": node_results,
        }


def print_divider(title: str = ""):
    print("\n" + "=" * 80)
    if title:
        print(f"  {title.upper()}")
        print("=" * 80)


def run_horizontal_scaling_demo():
    print_divider("Day 2: Horizontal Scaling Simulation (Scaling Out)")

    # Test heavy production workload (7,500 RPS) that crushed the giant single server on Day 2
    workload_rps = 7500.0

    print(f"Incoming Target Workload: {workload_rps:,.0f} Requests/Second\n")
    print("Testing cluster configurations with increasing node counts:")
    print("-" * 80)
    print(f"{'Cluster Size':<15} | {'Cost/mo':<10} | {'RPS/Node':<10} | {'Avg Load':<10} | {'Avg Latency':<12} | {'Cluster Status'}")
    print("-" * 80)

    cluster_sizes = [1, 2, 5, 10, 15]

    for size in cluster_sizes:
        cluster = HorizontalClusterSimulator(node_count=size)
        result = cluster.distribute_and_process(total_traffic_rps=workload_rps)

        cost_str = f"${result['total_monthly_cost']:,.0f}"
        rps_node_str = f"{result['rps_per_node']:,.0f}"
        load_str = f"{result['avg_utilization_pct']:.1f}%"
        lat_str = f"{result['avg_cluster_latency_ms']:.1f}ms"

        if result["total_dropped_requests"] > 0:
            status = "CRITICAL (Overloaded Nodes)"
        elif result["avg_utilization_pct"] > 85.0:
            status = "DEGRADED (High Load)"
        else:
            status = "HEALTHY & FAST"

        print(f"{size:<2} Nodes{'':<8} | {cost_str:<10} | {rps_node_str:<10} | {load_str:<10} | {lat_str:<12} | {status}")

    # Detailed breakdown of a 10-node cluster vs single monster server
    print_divider("Detailed Inspection: 10-Node Horizontal Cluster at 7,500 RPS")
    cluster_10 = HorizontalClusterSimulator(node_count=10)
    res_10 = cluster_10.distribute_and_process(total_traffic_rps=workload_rps)

    print(f"Total Cluster Nodes:     {res_10['node_count']}")
    print(f"Workload per Node:       {res_10['rps_per_node']} RPS")
    print(f"Average Node CPU Load:   {res_10['avg_utilization_pct']}%")
    print(f"Average Request Latency: {res_10['avg_cluster_latency_ms']} ms")
    print(f"Total Monthly Cost:      ${res_10['total_monthly_cost']:,.0f}")
    print("\nNode Request Distribution:")
    for idx, n_res in enumerate(res_10["per_node_breakdown"][:5]):
        print(f"  - Node-{idx+1:02d}: Processing {n_res['assigned_rps']} RPS | Load: {n_res['utilization_pct']}% | Latency: {n_res['avg_latency_ms']}ms")
    print("  - ... (Nodes 06 to 10 processing identical equal shares)")

    # Direct Comparison Summary
    print_divider("Side-by-Side Architectural Comparison (7,500 RPS)")
    print("""
+--------------------------+----------------------------+----------------------------+
| Metric                   | Vertical Scaling (1 Giant) | Horizontal Scaling (10 Small)|
+--------------------------+----------------------------+----------------------------+
| Hardware Type            | 96-Core Monster Server     | 10x 4-Core Commodity Nodes |
| Monthly Infrastructure   | $4,800 / month             | $500 / month               |
| CPU Load at 7,500 RPS    | 136.4% (SEVERELY CRASHED)  | 93.8% (Handled Smoothly)   |
| Average Request Latency  | > 800 ms (Timeout errors)  | ~ 75.0 ms                  |
| Single Point of Failure? | YES (1 node failure = down)| NO (Loss of 1 node = 90% ok)|
| Max Scaling Ceiling      | HARD CEILING REACHED       | INFINITE (Add Node 11, 12) |
+--------------------------+----------------------------+----------------------------+

Key Intuition:
By shifting our thinking from "How can ONE machine do more work?" to 
"How can MANY machines share the work?", we reduced monthly costs by 90% 
while turning an unhandleable crash into a fast, reliable system!
""")


if __name__ == "__main__":
    run_horizontal_scaling_demo()
