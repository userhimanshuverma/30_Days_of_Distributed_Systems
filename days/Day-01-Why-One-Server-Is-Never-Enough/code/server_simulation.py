"""
Day 1: Why One Server Is Never Enough
Simulation 1: Single Server Request Queue & Worker Saturation

CONCEPT OVERVIEW:
Every server operating on a single physical machine has finite execution capacity.
When HTTP requests arrive faster than worker threads can process them:
  1. Requests wait in an in-memory Queue.
  2. Average Response Latency grows linearly (Processing Time + Wait Time in Queue).
  3. When the Queue fills up to its maximum capacity, new requests are REJECTED (Dropped).
  4. Latency spikes exponentially from the client's perspective before failure occurs.

This script simulates this exact breakdown in a clean, educational console interface.
"""

import queue
import random
import threading
import time


class SingleServerSimulation:
    def __init__(self, num_workers=4, queue_capacity=15, process_time_sec=0.08):
        """
        Initialize a single server model.

        :param num_workers: Physical CPU cores / worker thread limit of this machine.
        :param queue_capacity: Operating system / Web server socket queue limit.
        :param process_time_sec: Average work time required per request.
        """
        self.num_workers = num_workers
        self.queue_capacity = queue_capacity
        self.process_time_sec = process_time_sec

        # In-memory queue representing socket backlogs (e.g., TCP SYN queue / web server backlog)
        self.request_queue = queue.Queue(maxsize=queue_capacity)

        # Operational metrics
        self.completed_requests = 0
        self.dropped_requests = 0
        self.total_latency = 0.0
        self.lock = threading.Lock()
        self.is_running = True

    def worker_thread(self, worker_id):
        """
        Simulates an operating system thread or web worker (e.g., Gunicorn/Uvicorn worker).
        """
        while self.is_running:
            try:
                # Wait up to 0.5s for a request from the queue
                req_id, arrival_time = self.request_queue.get(timeout=0.5)

                # Simulate work (CPU processing + I/O overhead)
                time.sleep(self.process_time_sec)

                finish_time = time.time()
                latency = finish_time - arrival_time

                with self.lock:
                    self.completed_requests += 1
                    self.total_latency += latency

                self.request_queue.task_done()
            except queue.Empty:
                continue

    def simulate_traffic_wave(self, request_rate_per_sec, duration_sec):
        """
        Generates incoming traffic at a specified arrival rate.
        """
        start_time = time.time()
        req_counter = 0

        while time.time() - start_time < duration_sec:
            req_counter += 1
            arrival_time = time.time()

            try:
                # Attempt to place request into server queue (non-blocking)
                self.request_queue.put_nowait((req_counter, arrival_time))
            except queue.Full:
                # HARDWARE/SERVER LIMIT: Queue full! Server drops connection.
                with self.lock:
                    self.dropped_requests += 1

            # Control request arrival pacing
            sleep_interval = 1.0 / request_rate_per_sec
            time.sleep(sleep_interval)

    def run_simulation(self):
        print("=" * 70)
        print("   DAY 1 SIMULATION: SINGLE SERVER HARDWARE SATURATION MODEL   ")
        print("=" * 70)
        print(f"[*] Server Spec: {self.num_workers} Worker Threads | Max Queue Depth: {self.queue_capacity}")
        print(f"[*] Processing Time per Request: {self.process_time_sec * 1000:.0f} ms")
        print(f"[*] Theoretical Max Throughput: {self.num_workers / self.process_time_sec:.1f} req/sec\n")

        # Spawn worker threads
        threads = []
        for i in range(self.num_workers):
            t = threading.Thread(target=self.worker_thread, args=(i + 1,), daemon=True)
            t.start()
            threads.append(t)

        # Traffic Phases (Simulating viral traffic growth)
        phases = [
            ("Phase 1: Normal Traffic (Low Load)", 15, 3.0),      # Below capacity (15 req/s)
            ("Phase 2: Peak Traffic (Near Capacity)", 40, 3.0),   # At capacity (40 req/s)
            ("Phase 3: Viral Spike (Severe Overload)", 100, 3.0), # Way over capacity (100 req/s)
        ]

        for phase_name, arrival_rate, duration in phases:
            print("-" * 70)
            print(f"[*] {phase_name} -> Incoming Traffic Rate: {arrival_rate} req/sec")
            print("-" * 70)

            # Reset window metrics
            with self.lock:
                self.completed_requests = 0
                self.dropped_requests = 0
                self.total_latency = 0.0

            # Run wave
            self.simulate_traffic_wave(request_rate_per_sec=arrival_rate, duration_sec=duration)

            # Snapshot state
            q_depth = self.request_queue.qsize()
            with self.lock:
                completed = self.completed_requests
                dropped = self.dropped_requests
                avg_latency_ms = (self.total_latency / completed * 1000) if completed > 0 else 0

            print(f"   - Queue Backlog Depth : {q_depth}/{self.queue_capacity} requests waiting")
            print(f"   - Requests Completed  : {completed}")
            print(f"   - Requests Dropped    : {dropped} (503 Service Unavailable)")
            print(f"   - Avg Client Latency  : {avg_latency_ms:.1f} ms")

            if dropped > 0:
                print("   [CRASH] STATUS: SERVER DROPPING CONNECTIONS!")
            elif q_depth > self.queue_capacity * 0.7:
                print("   [WARN]  STATUS: HIGH DEGRADATION - Latency spikes, queue filling up!")
            else:
                print("   [OK]    STATUS: HEALTHY - All requests served rapidly.")
            print()

        self.is_running = False
        print("=" * 70)
        print("LESSON: Single servers have a hard ceiling defined by physical cores & memory queue bounds.")
        print("When traffic exceeds max throughput, latency explodes long before requests drop!")
        print("=" * 70)


if __name__ == "__main__":
    sim = SingleServerSimulation(num_workers=4, queue_capacity=15, process_time_sec=0.08)
    sim.run_simulation()
