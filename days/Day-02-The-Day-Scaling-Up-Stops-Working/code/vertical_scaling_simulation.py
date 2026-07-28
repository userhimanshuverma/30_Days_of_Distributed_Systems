"""
Day 2: The Day Scaling Up Stops Working
File: vertical_scaling_simulation.py

Description:
This script simulates the phenomenon of Vertical Scaling (Scaling Up).
It demonstrates how repeatedly upgrading a single server (adding CPU cores & RAM)
initially solves performance problems, but eventually hits severe physical limits,
exponential cost scaling, and catastrophic queue saturation.

Intuition:
- A single machine processes work sequentially across its available CPU cores.
- As request traffic doubles, queuing delay increases non-linearly (M/M/1 queue dynamics).
- Upgrading to a larger server is easy, but cost increases exponentially while
  performance gains experience diminishing returns due to hardware bottlenecks.
"""

import time
import random
import math
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class ServerHardwareSpec:
    name: str
    cpu_cores: int
    ram_gb: int
    max_ops_per_sec: float
    monthly_cost_usd: float


class VerticalServerSimulator:
    """
    Simulates a single server undergoing hardware upgrades under increasing request load.
    """

    def __init__(self, spec: ServerHardwareSpec):
        self.spec = spec

    def process_workload(self, arrival_rate_rps: float, simulation_seconds: float = 1.0) -> Dict[str, float]:
        """
        Simulates processing incoming HTTP requests at a given Requests Per Second (RPS) rate.
        Calculates throughput, average latency (ms), queue buildup, and CPU utilization.
        """
        total_requests = int(arrival_rate_rps * simulation_seconds)
        max_capacity = self.spec.max_ops_per_sec * simulation_seconds

        # Base processing latency for a request on this hardware (in milliseconds)
        # Larger machines have slightly faster single-core speeds up to a limit
        base_latency_ms = max(5.0, 20.0 - (math.log2(self.spec.cpu_cores) * 2.0))

        # CPU Utilization calculation
        utilization = arrival_rate_rps / self.spec.max_ops_per_sec

        if utilization < 0.90:
            # Under healthy load: Latency = Base Latency + minor queuing delay
            # Formula models queuing theory: latency = base / (1 - utilization)
            queuing_multiplier = 1.0 / (1.0 - utilization)
            avg_latency_ms = base_latency_ms * queuing_multiplier
            successful_requests = total_requests
            dropped_requests = 0
            status = "HEALTHY"
        elif utilization <= 1.0:
            # Near saturation: Heavy queuing, high latency jitter
            avg_latency_ms = base_latency_ms * 15.0
            successful_requests = total_requests
            dropped_requests = 0
            status = "DEGRADED (High Latency)"
        else:
            # Saturated / Overloaded: Hardware cannot keep up. Queue overflows!
            # Severe delay and request drops occur.
            overflow_factor = utilization
            avg_latency_ms = base_latency_ms * 50.0 + (overflow_factor * 100.0)
            successful_requests = int(max_capacity)
            dropped_requests = total_requests - successful_requests
            status = "CRITICAL (Packet Drops & Timeouts)"

        return {
            "arrival_rate_rps": arrival_rate_rps,
            "utilization_pct": min(100.0, utilization * 100.0),
            "avg_latency_ms": round(avg_latency_ms, 2),
            "successful_requests": successful_requests,
            "dropped_requests": dropped_requests,
            "status": status,
        }


def print_divider(title: str = ""):
    print("\n" + "=" * 75)
    if title:
        print(f"  {title.upper()}")
        print("=" * 75)


def run_vertical_scaling_simulation():
    print_divider("Day 2: Vertical Scaling Simulation (Scaling Up)")

    # Define a progression of single-server hardware upgrades (Vertical Scaling)
    hardware_tiers = [
        ServerHardwareSpec(
            name="Small Instance (t3.medium)",
            cpu_cores=2,
            ram_gb=4,
            max_ops_per_sec=200.0,
            monthly_cost_usd=30.0,
        ),
        ServerHardwareSpec(
            name="Medium Instance (c5.2xlarge)",
            cpu_cores=8,
            ram_gb=16,
            max_ops_per_sec=700.0,
            monthly_cost_usd=150.0,
        ),
        ServerHardwareSpec(
            name="Large Instance (c5.12xlarge)",
            cpu_cores=48,
            ram_gb=96,
            max_ops_per_sec=3200.0,
            monthly_cost_usd=1200.0,
        ),
        ServerHardwareSpec(
            name="Monster Instance (c5.24xlarge)",
            cpu_cores=96,
            ram_gb=192,
            max_ops_per_sec=5500.0,
            # Cost increases non-linearly due to specialized high-end motherboards & NUMA architecture
            monthly_cost_usd=4800.0,
        ),
    ]

    # Traffic growth scenario over 4 quarters
    traffic_stages = [
        ("Q1 Launch", 150.0),      # 150 RPS
        ("Q2 Growth", 600.0),      # 600 RPS
        ("Q3 Viral Spike", 2800.0),# 2,800 RPS
        ("Q4 Scale Peak", 7500.0), # 7,500 RPS (Exceeds largest single server!)
    ]

    for stage_name, rps in traffic_stages:
        print_divider(f"Traffic Stage: {stage_name} ({rps:,.0f} Req/Sec)")
        print(f"{'Hardware Tier':<30} | {'Cost/mo':<9} | {'CPU Load':<9} | {'Latency':<10} | {'Status'}")
        print("-" * 75)

        for spec in hardware_tiers:
            sim = VerticalServerSimulator(spec)
            metrics = sim.process_workload(arrival_rate_rps=rps)

            cost_str = f"${spec.monthly_cost_usd:,.0f}"
            cpu_str = f"{metrics['utilization_pct']:.1f}%"
            lat_str = f"{metrics['avg_latency_ms']:.1f}ms"
            status = metrics["status"]

            print(f"{spec.name:<30} | {cost_str:<9} | {cpu_str:<9} | {lat_str:<10} | {status}")

    print_divider("Key Intuition & Summary")
    print("""
[!] OBSERVE THE VERTICAL SCALING LIMITS:
 1. Temporary Relief: Upgrading hardware solves capacity problems ONLY until traffic doubles again.
 2. Hardware Ceiling: At 7,500 RPS, even the giant 96-core Monster Server (costing $4,800/mo) 
    is overwhelmed (136% load) and drops requests!
 3. Diminishing Returns: Going from 48 cores to 96 cores doubled the cost (4x of Large instance), 
    but processing throughput only improved by ~71% due to inter-core synchronization bottlenecks.
 4. Single Point of Failure: If that single $4,800/mo server crashes or reboots for maintenance,
    100% of your users experience a total outage.

Conclusion: Buying bigger servers is only a temporary solution!
""")


if __name__ == "__main__":
    run_vertical_scaling_simulation()
