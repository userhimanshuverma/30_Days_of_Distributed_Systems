"""
backpressure_demo.py
--------------------
Demonstrates producer rate vs consumer rate imbalance, backlog growth, and backpressure mitigations.

Distributed Systems Concepts:
1. Backlog Accumulation: When Producer Rate > Consumer Rate, messages pile up in the queue.
2. Consumer Lag: The time delay between message publication and message processing.
3. Backpressure Mechanics: Bounded queues throttle producers, preventing memory exhaustion.
4. Consumer Scaling: Adding consumer instances to match incoming production throughput.
"""

import time
import queue
import threading
from typing import List


class BackpressureSimulation:
    def __init__(self, queue_capacity: int = 10):
        # Bounded queue enforces hard limit on pending messages (backpressure control)
        self.bounded_queue = queue.Queue(maxsize=queue_capacity)
        self.produced_count = 0
        self.consumed_count = 0
        self.producers_throttled_time = 0.0
        self.stop_signal = threading.Event()
        self.lock = threading.Lock()

    def producer(self, produce_interval: float, total_messages: int):
        """Simulates high-velocity producer pushing events rapidly."""
        print(f"[PRODUCER] Starting high-rate production (Interval: {produce_interval:.3f}s/msg)...")
        for i in range(1, total_messages + 1):
            if self.stop_signal.is_set():
                break

            msg = f"Event-{i}"
            start_wait = time.time()
            
            # Put will BLOCK if queue capacity is reached (Enforces Producer Backpressure!)
            self.bounded_queue.put(msg)
            
            waited = time.time() - start_wait
            if waited > 0.01:
                with self.lock:
                    self.producers_throttled_time += waited

            with self.lock:
                self.produced_count += 1
            
            time.sleep(produce_interval)

        print("[PRODUCER] Production finished.")

    def consumer(self, worker_id: int, process_delay: float):
        """Simulates slow consumer processing tasks sequentially."""
        print(f"  [CONSUMER-{worker_id}] Worker started (Processing time: {process_delay:.3f}s/msg).")
        while not self.stop_signal.is_set() or not self.bounded_queue.empty():
            try:
                msg = self.bounded_queue.get(timeout=0.2)
                time.sleep(process_delay)
                with self.lock:
                    self.consumed_count += 1
                self.bounded_queue.task_done()
            except queue.Empty:
                continue


def main():
    print("=" * 70)
    print("DEMO: Backpressure & Consumer Lag Mechanics")
    print("=" * 70)

    # Scenario: Queue capacity = 8, Producer generates 20 msgs @ 20ms apart (50 msg/sec)
    # 1 Consumer processes @ 100ms per msg (10 msg/sec)
    sim = BackpressureSimulation(queue_capacity=8)

    total_msgs = 20
    producer_delay = 0.02  # 50 msgs/sec
    consumer_delay = 0.10  # 10 msgs/sec per worker

    print(f"Configuration:")
    print(f"  - Queue Max Capacity (Buffer): 8 items")
    print(f"  - Producer Rate:  50 msgs/sec")
    print(f"  - Consumer Rate:  10 msgs/sec (1 worker)")
    print(f"  - Total Messages: {total_msgs}\n")

    # Start Phase 1: 1 Producer, 1 Consumer
    prod_thread = threading.Thread(target=sim.producer, args=(producer_delay, total_msgs))
    c1_thread = threading.Thread(target=sim.consumer, args=(1, consumer_delay))

    prod_thread.start()
    c1_thread.start()

    # Monitor queue growth / lag during production
    print("--- Monitoring Queue Backlog & Producer Throttling ---")
    for _ in range(6):
        time.sleep(0.1)
        qsize = sim.bounded_queue.qsize()
        with sim.lock:
            p_cnt = sim.produced_count
            c_cnt = sim.consumed_count
        print(f"  [STATUS] Queue Size: {qsize}/8 | Produced: {p_cnt} | Consumed: {c_cnt} | Consumer Lag: {p_cnt - c_cnt}")

    # Start Phase 2: Scale up consumers (Add 3 more consumers to relieve backpressure)
    print("\n--- Scaling Consumer Pool (Adding 3 additional workers) ---")
    scaled_consumers: List[threading.Thread] = []
    for w_id in range(2, 5):
        t = threading.Thread(target=sim.consumer, args=(w_id, consumer_delay))
        t.start()
        scaled_consumers.append(t)

    # Wait for completion
    prod_thread.join()
    sim.stop_signal.set()
    c1_thread.join()
    for t in scaled_consumers:
        t.join()

    print("\n" + "=" * 70)
    print("BACKPRESSURE SIMULATION RESULTS:")
    print(f"  - Total Produced Messages:    {sim.produced_count}")
    print(f"  - Total Consumed Messages:    {sim.consumed_count}")
    print(f"  - Producer Throttled Time:    {sim.producers_throttled_time:.3f} seconds (Producer backpressure applied)")
    print(f"  - Remaining Queue Backlog:    {sim.bounded_queue.qsize()}")
    print("=" * 70)


if __name__ == "__main__":
    main()
