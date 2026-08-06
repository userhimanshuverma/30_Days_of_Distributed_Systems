"""
database_bottleneck_demo.py
---------------------------
Educational simulation demonstrating why single database architectures become 
the primary bottleneck as application compute scales horizontally.

This script simulates a realistic scenario:
- Application servers scale horizontally (1 -> 5 -> 20 -> 50 instances).
- All application servers send read and write transactions to a SINGLE central Database server.
- The single database server has fixed physical limits (CPU cores, Disk IOPS, Connection pool capacity).
- As request volume increases, a massive request queue builds up at the database layer.
- Response times explode while database throughput plateaus (resource saturation).

Run:
    python database_bottleneck_demo.py
"""

import time
import random
import queue
import threading
from typing import List, Dict
from request_simulator import ApplicationServer, DatabaseRequest, RequestType


class SingleDatabaseServer:
    """
    Simulates a centralized Single Database Engine.
    
    Key Characteristics:
    - Fixed connection pool capacity (max concurrent connections).
    - Fixed worker threads (simulating physical CPU core count and disk lock concurrency).
    - A shared input request queue where incoming app server requests wait.
    """

    def __init__(self, max_connections: int = 10, worker_threads: int = 4):
        self.max_connections = max_connections
        self.worker_threads = worker_threads
        self.incoming_queue: queue.Queue = queue.Queue()
        self.active_connections = 0
        self.lock = threading.Lock()
        
        # Metrics
        self.processed_count = 0
        self.rejected_count = 0
        self.latencies_ms: List[float] = []
        self.max_queue_depth = 0
        self.running = False
        self.workers: List[threading.Thread] = []

    def start(self):
        """Starts the database worker threads."""
        self.running = True
        self.processed_count = 0
        self.rejected_count = 0
        self.latencies_ms.clear()
        self.max_queue_depth = 0
        
        for i in range(self.worker_threads):
            t = threading.Thread(target=self._worker_loop, daemon=True, name=f"db-worker-{i}")
            self.workers.append(t)
            t.start()

    def stop(self):
        """Stops the database engine."""
        self.running = False

    def submit_request(self, request: DatabaseRequest) -> bool:
        """
        Attempts to submit a request from an application server to the database.
        If the connection pool or queue is saturated beyond limits, the request is rejected.
        """
        with self.lock:
            # Track peak queue depth
            current_q_len = self.incoming_queue.qsize()
            if current_q_len > self.max_queue_depth:
                self.max_queue_depth = current_q_len

            # If connection queue exceeds safe limits (simulating socket connection overflow)
            if current_q_len >= 200:
                self.rejected_count += 1
                return False

        self.incoming_queue.put(request)
        return True

    def _worker_loop(self):
        """Simulates single database thread executing queries sequentially per core."""
        while self.running or not self.incoming_queue.empty():
            try:
                request: DatabaseRequest = self.incoming_queue.get(timeout=0.05)
            except queue.Empty:
                continue

            # Simulate CPU + Disk IO processing time (scaled down for simulation speed)
            # In real system: Disk IOPS bounds, WAL log locks, cache misses
            simulated_execution_sec = (request.estimated_db_cost_ms / 1000.0) * 0.05
            time.sleep(simulated_execution_sec)

            # Calculate total queuing + execution time spent by request
            total_duration_ms = (time.time() - request.created_at) * 1000.0

            with self.lock:
                self.processed_count += 1
                self.latencies_ms.append(total_duration_ms)

            self.incoming_queue.task_done()


def run_benchmark_scenario(num_app_servers: int, requests_per_server: int = 30) -> Dict[str, float]:
    """
    Runs a test scenario with a specific number of application servers 
    pounding a single centralized database.
    """
    db = SingleDatabaseServer(max_connections=15, worker_threads=4)
    db.start()

    # Create app servers
    servers = [ApplicationServer(server_id=f"app-server-{i+1}") for i in range(num_app_servers)]
    
    start_time = time.time()
    threads = []

    def server_workload(server: ApplicationServer):
        for _ in range(requests_per_server):
            req = server.generate_request()
            success = db.submit_request(req)
            if success:
                server.record_completion(req.estimated_db_cost_ms)
            # App server slight pause between user transactions
            time.sleep(0.002)

    # Launch concurrent App Servers sending requests
    for server in servers:
        t = threading.Thread(target=server_workload, args=(server,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Wait for DB to drain remaining queued items
    db.incoming_queue.join()
    elapsed_sec = time.time() - start_time
    db.stop()

    avg_lat = sum(db.latencies_ms) / len(db.latencies_ms) if db.latencies_ms else 0.0
    sorted_lat = sorted(db.latencies_ms) if db.latencies_ms else [0.0]
    p99_lat = sorted_lat[int(len(sorted_lat) * 0.99)] if sorted_lat else 0.0
    throughput = db.processed_count / elapsed_sec if elapsed_sec > 0 else 0.0

    return {
        "num_servers": num_app_servers,
        "total_requests": num_app_servers * requests_per_server,
        "processed": db.processed_count,
        "rejected": db.rejected_count,
        "elapsed_sec": round(elapsed_sec, 2),
        "throughput_tps": round(throughput, 1),
        "avg_latency_ms": round(avg_lat, 2),
        "p99_latency_ms": round(p99_lat, 2),
        "max_queue_depth": db.max_queue_depth
    }


def main():
    print("=" * 80)
    print("  DAY 11 SIMULATION: WHY DATABASES CAN'T LIVE ON ONE MACHINE")
    print("=" * 80)
    print("Simulating application traffic scaling against a SINGLE centralized database...")
    print("Watch how average latency explodes and queue depth overflows as app servers scale out.\n")

    scenarios = [1, 5, 20, 50]
    results = []

    for num_servers in scenarios:
        print(f"Running simulation with {num_servers:2d} Application Server(s)...", end="", flush=True)
        res = run_benchmark_scenario(num_app_servers=num_servers, requests_per_server=40)
        results.append(res)
        print(" DONE")

    # Print summary metrics table
    print("\n" + "=" * 80)
    print(f"{'App Servers':<12} | {'Req Count':<10} | {'Throughput':<12} | {'Avg Latency':<13} | {'P99 Latency':<13} | {'Max Queue':<10}")
    print("=" * 80)
    
    for r in results:
        servers_str = f"{r['num_servers']} node(s)"
        tps_str = f"{r['throughput_tps']} TPS"
        avg_str = f"{r['avg_latency_ms']} ms"
        p99_str = f"{r['p99_latency_ms']} ms"
        q_str = f"{r['max_queue_depth']} reqs"
        print(f"{servers_str:<12} | {r['total_requests']:<10} | {tps_str:<12} | {avg_str:<13} | {p99_str:<13} | {q_str:<10}")

    print("=" * 80)
    print("\n[KEY OBSERVATION]:")
    print("1. As application servers scale from 1 to 50, compute capacity expands 50x.")
    print("2. However, single database throughput reaches a fixed hardware ceiling (~TPS plateau).")
    print("3. Excess requests accumulate in the single database queue, causing latency to skyrocket!")
    print("4. Conclusion: Scaling compute without scaling data storage creates a severe bottleneck.\n")


if __name__ == "__main__":
    main()
