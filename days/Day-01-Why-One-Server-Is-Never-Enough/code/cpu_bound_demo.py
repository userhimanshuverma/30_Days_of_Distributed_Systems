"""
Day 1: Why One Server Is Never Enough
Simulation 2: CPU Bound & Core Saturation Demo

CONCEPT OVERVIEW:
A CPU does not become "faster" just because more software threads request work.
Each physical CPU core can only execute ONE thread instruction stream at any given microsecond.

When an application receives concurrent CPU-heavy requests (e.g., password hashing,
JSON serialization, image rendering, or data computation):
  1. Operating System context switching overhead rises rapidly.
  2. Memory bus & L1/L2/L3 cache thrashing degrades instruction throughput.
  3. Total throughput (operations/sec) hits a physical ceiling equal to [num_cores].
  4. Per-request duration increases linearly or quadratically as concurrency rises!

This simulation measures actual CPU computation performance under increasing concurrent load.
"""

import concurrent.futures
import hashlib
import os
import time


def cpu_intensive_workstep(request_id: int, iterations: int = 40_000) -> float:
    """
    Simulates a heavy request payload (e.g., hashing passwords or processing image data).
    Returns total processing time for this specific request.
    """
    start_time = time.time()

    # Perform repeated CPU instructions (SHA-256 computation)
    data = f"payload_data_request_{request_id}".encode("utf-8")
    for _ in range(iterations):
        data = hashlib.sha256(data).digest()

    return time.time() - start_time


def run_concurrency_experiment(num_concurrent_requests: int):
    """
    Runs a batch of concurrent CPU-bound requests using a process/thread pool.
    """
    start_batch = time.time()

    # Execute requests concurrently using Python's ThreadPool (simulating multi-threaded web server)
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_concurrent_requests) as executor:
        futures = [
            executor.submit(cpu_intensive_workstep, req_id)
            for req_id in range(num_concurrent_requests)
        ]
        durations = [f.result() for f in futures]

    total_batch_time = time.time() - start_batch
    avg_req_latency = sum(durations) / len(durations)
    req_per_sec = num_concurrent_requests / total_batch_time

    return total_batch_time, avg_req_latency, req_per_sec


def main():
    logical_cores = os.cpu_count() or 4

    print("=" * 75)
    print("   DAY 1 SIMULATION: CPU SATURATION & CONTEXT SWITCHING BENCHMARK   ")
    print("=" * 75)
    print(f"[*] Host Machine Hardware Specs: {logical_cores} Logical CPU Cores detected.")
    print("[*] Benchmark Workload: Concurrent SHA-256 hashing requests.\n")

    concurrency_levels = [1, 2, logical_cores, logical_cores * 2, logical_cores * 8]

    print(f"{'Concurrent Requests':<22} | {'Batch Time (s)':<15} | {'Avg Latency (ms)':<18} | {'Throughput (req/s)':<18}")
    print("-" * 80)

    for concurrency in concurrency_levels:
        batch_time, avg_lat, throughput = run_concurrency_experiment(concurrency)
        avg_lat_ms = avg_lat * 1000

        print(
            f"{concurrency:<22} | {batch_time:<15.3f} | {avg_lat_ms:<18.1f} | {throughput:<18.1f}"
        )

    print("-" * 80)
    print("\n[*] KEY INSIGHT:")
    print("Notice how throughput (req/s) levels off once concurrency exceeds physical CPU core count.")
    print("Adding more requests beyond core capacity ONLY increases average request latency (wait time)!")
    print("Good code cannot bypass physical silicon clock speeds or core counts.")
    print("=" * 75)


if __name__ == "__main__":
    main()
