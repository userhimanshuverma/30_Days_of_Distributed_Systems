"""
producer_consumer.py
--------------------
Demonstrates multi-threaded producer-consumer workflow with explicit acknowledgements (ACK).

Key Distributed Systems Concepts:
1. Producer-Consumer Decoupling: Producers push work independently of consumer capacity.
2. Worker Pool Concurrency: Multiple consumer workers drain the same queue concurrently.
3. Explicit Acknowledgements (ACK/NACK): Messages remain tracked until consumer confirms completion.
"""

import time
import uuid
import random
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from queue import Queue, Empty
from typing import Dict, Optional


@dataclass
class Message:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    payload: dict = field(default_factory=dict)
    attempts: int = 0
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class AckableBroker:
    """
    Message Broker supporting explicit acknowledgements (ACK) and in-flight tracking.
    """
    def __init__(self):
        self._queue: Queue[Message] = Queue()
        self._in_flight: Dict[str, Message] = {}
        self._lock = threading.Lock()
        self.acknowledged_count = 0

    def publish(self, payload: dict) -> Message:
        msg = Message(payload=payload)
        self._queue.put(msg)
        return msg

    def consume(self, worker_id: str, timeout: float = 1.0) -> Optional[Message]:
        try:
            msg = self._queue.get(timeout=timeout)
            with self._lock:
                msg.attempts += 1
                self._in_flight[msg.id] = msg
            return msg
        except Empty:
            return None

    def ack(self, msg_id: str, worker_id: str):
        """Consumer signals message processed successfully. Removes from in-flight tracking."""
        with self._lock:
            if msg_id in self._in_flight:
                del self._in_flight[msg_id]
                self.acknowledged_count += 1
                self._queue.task_done()

    def nack(self, msg_id: str, worker_id: str):
        """Consumer signals processing failed. Re-enqueues message for redelivery."""
        with self._lock:
            if msg_id in self._in_flight:
                msg = self._in_flight.pop(msg_id)
                self._queue.task_done()
                self._queue.put(msg)  # Re-enqueue for retry

    def pending_count(self) -> int:
        return self._queue.qsize()

    def in_flight_count(self) -> int:
        with self._lock:
            return len(self._in_flight)


def producer_worker(broker: AckableBroker, total_items: int):
    """Simulates a service generating incoming transaction events."""
    items = ["Payment", "Order", "Refund", "KYC_Check", "Notification"]
    for i in range(1, total_items + 1):
        item_type = random.choice(items)
        payload = {"transaction_id": 1000 + i, "type": item_type, "amount": round(random.uniform(10, 500), 2)}
        msg = broker.publish(payload)
        print(f"[PRODUCER] Enqueued tx #{payload['transaction_id']} (msg_id={msg.id})")
        time.sleep(0.05)


def consumer_worker(worker_id: str, broker: AckableBroker, stop_event: threading.Event):
    """Simulates a worker instance pulling and processing messages with explicit ACKs."""
    print(f"  [WORKER-{worker_id}] Started.")
    while not stop_event.is_set() or broker.pending_count() > 0 or broker.in_flight_count() > 0:
        msg = broker.consume(worker_id=worker_id, timeout=0.2)
        if msg is None:
            continue

        print(f"  [WORKER-{worker_id}] Processing msg={msg.id} (tx #{msg.payload['transaction_id']})")
        
        # Simulate processing work
        time.sleep(random.uniform(0.1, 0.2))

        # Simulate 90% success rate
        if random.random() < 0.9:
            broker.ack(msg.id, worker_id)
            print(f"  [WORKER-{worker_id}] ACKed msg={msg.id}")
        else:
            broker.nack(msg.id, worker_id)
            print(f"  [WORKER-{worker_id}] NACKed msg={msg.id} (Re-queued for retry)")


def main():
    print("=" * 65)
    print("DEMO: Multi-Worker Consumer Pool with Explicit Acknowledgements (ACK)")
    print("=" * 65)

    broker = AckableBroker()
    stop_event = threading.Event()

    total_messages = 12
    consumer_threads = []
    
    # Start 3 Consumer Worker Threads
    for w_id in range(1, 4):
        t = threading.Thread(target=consumer_worker, args=(f"W{w_id}", broker, stop_event))
        t.start()
        consumer_threads.append(t)

    # Start 1 Producer Thread
    prod_thread = threading.Thread(target=producer_worker, args=(broker, total_messages))
    prod_thread.start()

    # Wait for producer to finish publishing
    prod_thread.join()
    print("\n[SYSTEM] Producer completed generating messages. Draining queue...\n")

    # Signal stop to consumers once queue drains
    stop_event.set()
    for t in consumer_threads:
        t.join()

    print("\n" + "=" * 65)
    print(f"FINAL METRICS:")
    print(f"  - Total Messages Acknowledged: {broker.acknowledged_count}")
    print(f"  - Pending Messages in Queue:  {broker.pending_count()}")
    print(f"  - In-Flight Messages Left:    {broker.in_flight_count()}")
    print("=" * 65)


if __name__ == "__main__":
    main()
