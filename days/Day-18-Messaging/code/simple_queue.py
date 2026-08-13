"""
simple_queue.py
---------------
A minimal, educational implementation of an in-memory message queue.

This script demonstrates the foundational mechanics of a message broker:
1. Producer enqueuing structured message payloads into a FIFO buffer.
2. Consumer dequeuing messages for asynchronous processing.
3. Decoupled execution where producer and consumer operate independently.
"""

import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from queue import Queue, Empty
from typing import Optional


@dataclass
class Message:
    """Represents an immutable message payload passed through the broker."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    topic: str = "order.created"
    payload: dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SimpleBroker:
    """A basic single-queue message broker using a thread-safe FIFO queue."""
    def __init__(self, name: str = "OrderProcessingQueue"):
        self.name = name
        self._queue: Queue[Message] = Queue()

    def publish(self, payload: dict, topic: str = "order.created") -> Message:
        """Producer interface: Enqueue a new message onto the broker."""
        msg = Message(topic=topic, payload=payload)
        self._queue.put(msg)
        print(f"[PRODUCER] Published msg={msg.id} | Topic='{msg.topic}' | Data={payload}")
        return msg

    def consume(self, timeout: float = 1.0) -> Optional[Message]:
        """Consumer interface: Dequeue a message from the broker."""
        try:
            msg = self._queue.get(timeout=timeout)
            print(f"[CONSUMER] Fetched msg={msg.id} | Data={msg.payload}")
            return msg
        except Empty:
            print("[CONSUMER] Queue is empty. Waiting for messages...")
            return None

    def size(self) -> int:
        """Returns the current number of pending messages in the queue."""
        return self._queue.qsize()


def main():
    print("=" * 60)
    print("DEMO: Basic In-Memory Message Queue Mechanics")
    print("=" * 60)

    broker = SimpleBroker(name="CheckoutBroker")

    # 1. Producer publishes messages to the queue
    print("\n--- Producer Enqueuing Orders ---")
    broker.publish({"order_id": 101, "item": "Laptop", "amount": 1200.00})
    broker.publish({"order_id": 102, "item": "Headphones", "amount": 150.00})
    broker.publish({"order_id": 103, "item": "Keyboard", "amount": 85.00})

    print(f"\n[BROKER STATS] Pending messages in queue: {broker.size()}")

    # 2. Consumer processes messages asynchronously from the queue
    print("\n--- Consumer Processing Orders (FIFO) ---")
    while broker.size() > 0:
        msg = broker.consume()
        if msg:
            # Simulate work execution
            time.sleep(0.1)
            print(f"  |-- SUCCESS: Processed order #{msg.payload['order_id']}")

    print(f"\n[BROKER STATS] Remaining messages in queue: {broker.size()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
