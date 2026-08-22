"""
Day 27: How WhatsApp Delivers Billions of Messages
Demonstration Script: Distributed Messaging Simulation

Runs two primary scenarios demonstrating real-time distributed messaging mechanics:
1. Online Delivery Scenario: Immediate routing, delivery, and acknowledgement (SENT -> DELIVERED -> READ).
2. Offline Store-and-Forward Scenario: Recipient offline during send, message persistence, reconnection flushing.
"""

import sys
import time

# Ensure UTF-8 output encoding on Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from server import MessagingServer
from client import UserClient
from message_store import MessageStatus


def print_section(title: str) -> None:
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def run_demo() -> None:
    print("🚀 Initializing Distributed Messaging System Simulation...")
    server = MessagingServer()

    # Create clients
    alice = UserClient("alice", server)
    bob = UserClient("bob", server)
    charlie = UserClient("charlie", server)

    # -------------------------------------------------------------------------
    # SCENARIO 1: Immediate Delivery to Online Recipient
    # -------------------------------------------------------------------------
    print_section("SCENARIO 1: Immediate Delivery (Both Users Online)")
    
    print("1. Connecting Alice and Bob...")
    alice.connect()
    bob.connect()

    print("\n2. Alice sends a real-time message to Bob...")
    msg1 = alice.send_message("bob", "Hey Bob! Are you free for a call?")

    print("\n3. Bob opens and reads the message...")
    if msg1:
        bob.read_message(msg1.message_id)

    print("\n4. Checking Alice's sent message tracker:")
    if msg1:
        status = alice.sent_status_tracker.get(msg1.message_id)
        print(f"   -> Alice sees status for message {msg1.message_id[:8]}...: {status.value if status else 'UNKNOWN'}")

    # -------------------------------------------------------------------------
    # SCENARIO 2: Store-and-Forward for Offline Recipient
    # -------------------------------------------------------------------------
    print_section("SCENARIO 2: Offline Store-and-Forward Delivery")

    print("1. Verification: Charlie is currently offline (not connected).")
    print(f"   -> Is Charlie online? {server.is_user_online('charlie')}")

    print("\n2. Alice sends a message to Charlie while Charlie is OFFLINE...")
    msg2 = alice.send_message("charlie", "Hey Charlie, let me know when you get back online!")

    print("\n3. Inspecting Server Offline Storage:")
    pending_count = server.offline_store.get_pending_count("charlie")
    print(f"   -> Pending messages in store for 'charlie': {pending_count}")

    print("\n4. Alice checks her sent message status tracker:")
    if msg2:
        status = alice.sent_status_tracker.get(msg2.message_id)
        print(f"   -> Alice sees status for message {msg2.message_id[:8]}...: {status.value if status else 'UNKNOWN'}")

    print("\n5. Charlie reconnects to the network (e.g. toggles Airplane Mode off)...")
    charlie.connect()

    print("\n6. Alice checks her sent message tracker after Charlie's reconnection:")
    if msg2:
        status = alice.sent_status_tracker.get(msg2.message_id)
        print(f"   -> Alice sees status for message {msg2.message_id[:8]}...: {status.value if status else 'UNKNOWN'}")

    print("\n7. Charlie reads the delivered offline message...")
    if msg2:
        charlie.read_message(msg2.message_id)

    print("\n8. Final status check on Alice's device:")
    if msg2:
        status = alice.sent_status_tracker.get(msg2.message_id)
        print(f"   -> Alice sees status for message {msg2.message_id[:8]}...: {status.value if status else 'UNKNOWN'}")

    print_section("SIMULATION COMPLETE")
    print("All distributed messaging flows executed successfully!\n")


if __name__ == "__main__":
    run_demo()
