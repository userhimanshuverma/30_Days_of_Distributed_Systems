"""
retry_and_dead_letter.py
------------------------
Demonstrates retry mechanisms and Dead-Letter Queue (DLQ) pattern for handling poison messages.

Distributed Systems Concepts:
1. Transient Failures: Temporary network glitches or downstream unavailability solved by retries.
2. Poison Messages: Malformed payloads or unrecoverable logic bugs that fail consistently.
3. Dead-Letter Queue (DLQ): Prevents head-of-line blocking by isolating unprocessable messages for inspection.
"""

import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from queue import Queue, Empty
from typing import List


@dataclass
class Message:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    payload: dict = field(default_factory=dict)
    attempts: int = 0
    max_retries: int = 3
    error_log: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class BrokerWithDLQ:
    """Message Broker with automatic Dead-Letter Queue (DLQ) routing for failing messages."""
    def __init__(self, max_retries: int = 3):
        self.main_queue: Queue[Message] = Queue()
        self.dlq: Queue[Message] = Queue()
        self.max_retries = max_retries

    def publish(self, payload: dict, max_retries: int = 3) -> Message:
        msg = Message(payload=payload, max_retries=max_retries)
        self.main_queue.put(msg)
        return msg

    def process_message(self, msg: Message) -> bool:
        """Simulate message processing logic with deliberate failure injection."""
        msg.attempts += 1
        
        # Poison payload injection
        if msg.payload.get("corrupted", False):
            reason = f"Attempt {msg.attempts}: Invalid Schema / Malformed Payload"
            msg.error_log.append(reason)
            print(f"  [PROCESSOR] FAIL (Permanent): msg={msg.id} | Reason: {reason}")
            return False

        # Simulate transient error on attempt 1 for order 202
        if msg.payload.get("transient_bug", False) and msg.attempts == 1:
            reason = f"Attempt {msg.attempts}: Database Connection Timeout (Transient)"
            msg.error_log.append(reason)
            print(f"  [PROCESSOR] FAIL (Transient): msg={msg.id} | Reason: {reason}")
            return False

        # Success
        print(f"  [PROCESSOR] SUCCESS: msg={msg.id} | Payload={msg.payload['item']}")
        return True

    def run_consumer_loop(self):
        """Processes main queue messages, retrying failures or moving to DLQ if max retries exceeded."""
        while not self.main_queue.empty():
            msg = self.main_queue.get()
            print(f"\n[CONSUMER] Picked up msg={msg.id} (Attempt {msg.attempts + 1}/{msg.max_retries})")
            
            success = self.process_message(msg)
            
            if success:
                self.main_queue.task_done()
            else:
                if msg.attempts < msg.max_retries:
                    print(f"  [RETRY HANDLER] Re-enqueuing msg={msg.id} to Main Queue for retry.")
                    self.main_queue.put(msg)
                else:
                    print(f"  [DLQ ROUTER] Exceeded max retries ({msg.max_retries}). Routing msg={msg.id} to Dead-Letter Queue!")
                    self.dlq.put(msg)
                self.main_queue.task_done()


def main():
    print("=" * 70)
    print("DEMO: Message Retries & Dead-Letter Queue (DLQ) Mechanics")
    print("=" * 70)

    broker = BrokerWithDLQ(max_retries=3)

    # Publish normal, transient-failure, and poison messages
    print("\n--- Publishing Test Workload ---")
    m1 = broker.publish({"order_id": 201, "item": "Normal Order", "corrupted": False, "transient_bug": False})
    print(f"Published msg={m1.id} (Normal)")

    m2 = broker.publish({"order_id": 202, "item": "Transient Error Order", "corrupted": False, "transient_bug": True})
    print(f"Published msg={m2.id} (Transient Failure on Attempt 1)")

    m3 = broker.publish({"order_id": 203, "item": "Poison Pill Order", "corrupted": True, "transient_bug": False})
    print(f"Published msg={m3.id} (Poison Payload - Always Fails)")

    # Run processing loop
    print("\n--- Executing Consumer Processing & Retry Loop ---")
    broker.run_consumer_loop()

    # Inspect final queue states
    print("\n" + "=" * 70)
    print("SUMMARY OF QUEUE STATES:")
    print(f"  - Main Queue Pending Count: {broker.main_queue.qsize()}")
    print(f"  - Dead-Letter Queue (DLQ) Count: {broker.dlq.qsize()}")
    
    if not broker.dlq.empty():
        print("\n--- Inspecting Dead-Letter Queue (DLQ) Messages ---")
        while not broker.dlq.empty():
            dlq_msg = broker.dlq.get()
            print(f"  * DLQ Msg ID: {dlq_msg.id}")
            print(f"    Payload:    {dlq_msg.payload}")
            print(f"    Attempts:   {dlq_msg.attempts}")
            print(f"    Error Log:  {dlq_msg.error_log}")
    print("=" * 70)


if __name__ == "__main__":
    main()
