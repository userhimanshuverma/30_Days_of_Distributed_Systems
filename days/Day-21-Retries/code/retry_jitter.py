"""
Day 21: Retries - Jitter Demonstration
======================================

Educational code demonstrating why Jitter is required alongside Exponential Backoff.
NOTE: This code is for learning purposes and is not production-ready.

Concept:
If 1,000 clients fail at the exact same moment (e.g. during a 100ms network partition)
and all use deterministic Exponential Backoff (1s, 2s, 4s), all 1,000 clients will retry
at t=1.0s, t=3.0s, t=7.0s. This produces severe periodic traffic spikes (Retry Spikes),
keeping the downstream service crashed (Thundering Herd Problem).

Adding "Jitter" introduces randomness into the backoff delay:
  1. No Jitter:     delay = base * 2^attempt
  2. Full Jitter:   delay = random(0, base * 2^attempt)
  3. Equal Jitter:  delay = (base * 2^attempt) / 2 + random(0, (base * 2^attempt) / 2)

Jitter breaks client synchronization and spreads retry traffic smoothly across time.
"""

import time
import random
from typing import List, Dict


def calculate_no_jitter(base_delay: float, attempt: int, max_delay: float) -> float:
    """Deterministic exponential backoff without jitter."""
    return min(max_delay, base_delay * (2 ** attempt))


def calculate_full_jitter(base_delay: float, attempt: int, max_delay: float) -> float:
    """Full jitter: Pick a uniform random value between 0 and max exponential backoff."""
    calculated = min(max_delay, base_delay * (2 ** attempt))
    return random.uniform(0, calculated)


def calculate_equal_jitter(base_delay: float, attempt: int, max_delay: float) -> float:
    """Equal jitter: Half deterministic base, half uniform random jitter."""
    calculated = min(max_delay, base_delay * (2 ** attempt))
    half = calculated / 2.0
    return half + random.uniform(0, half)


def simulate_client_retries(strategy_name: str, strategy_func, num_clients: int = 50, attempt: int = 2) -> List[float]:
    """
    Simulates `num_clients` all experiencing a failure at t=0.0s and calculating their
    next retry timestamp for attempt N.
    """
    base_delay = 1.0
    max_delay = 16.0
    retry_timestamps = []
    
    for _ in range(num_clients):
        delay = strategy_func(base_delay, attempt, max_delay)
        retry_timestamps.append(delay)
        
    return sorted(retry_timestamps)


def print_histogram(timestamps: List[float], num_bins: int = 10, title: str = ""):
    """Prints a simple text ASCII histogram of retry timing distribution."""
    print(f"\n--- {title} ---")
    min_t = 0.0
    max_t = max(timestamps) if timestamps else 1.0
    bin_width = max(max_t / num_bins, 0.1)
    
    bins = [0] * num_bins
    for t in timestamps:
        idx = min(int(t / bin_width), num_bins - 1)
        bins[idx] += 1
        
    for i in range(num_bins):
        start_r = i * bin_width
        end_r = (i + 1) * bin_width
        bar = "#" * (bins[i] // 2) if bins[i] > 0 else ""
        print(f"[{start_r:4.1f}s - {end_r:4.1f}s]: {bins[i]:2d} clients | {bar}")


if __name__ == "__main__":
    print("=" * 65)
    print("   DISTRIBUTED SYSTEMS HANDBOOK: RETRY JITTER SIMULATION")
    print("=" * 65)
    print("Simulating 50 concurrent clients retrying at Attempt #2 (Base Backoff: 4.0s)\n")

    random.seed(42) # Fixed seed for reproducible output comparison

    no_jitter_ts = simulate_client_retries("No Jitter", calculate_no_jitter, num_clients=50, attempt=2)
    full_jitter_ts = simulate_client_retries("Full Jitter", calculate_full_jitter, num_clients=50, attempt=2)
    equal_jitter_ts = simulate_client_retries("Equal Jitter", calculate_equal_jitter, num_clients=50, attempt=2)

    print_histogram(no_jitter_ts, num_bins=8, title="1. NO JITTER (Deterministic Backoff - High Synchronization)")
    print("Notice: ALL 50 clients hit the server at the exact same instant (t=4.0s)! Spiking server load.")

    print_histogram(full_jitter_ts, num_bins=8, title="2. FULL JITTER (Randomized Spread)")
    print("Notice: Retries are distributed smoothly between t=0.0s and t=4.0s, eliminating the spike.")

    print_histogram(equal_jitter_ts, num_bins=8, title="3. EQUAL JITTER (Guaranteed Min Delay + Randomization)")
    print("Notice: Retries are distributed between t=2.0s and t=4.0s, guaranteeing delay while preventing spikes.")
