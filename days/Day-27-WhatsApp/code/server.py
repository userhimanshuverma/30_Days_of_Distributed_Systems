"""
Day 27: How WhatsApp Delivers Billions of Messages
Component: Messaging Server Gateway & Routing Infrastructure

Simulates the core connection gateway, user routing table, and store-and-forward delivery system.
Decouples message submission (accepting from sender) from final delivery (pushing to recipient).
"""

import sys
from typing import Dict, Optional
import uuid

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
from message_store import Message, MessageStatus, OfflineMessageStore
from client import UserClient


class MessagingServer:
    """
    Simulates a distributed messaging gateway infrastructure.
    
    Responsibilities:
    1. Maintain connection state (User Routing Table).
    2. Accept incoming messages & issue immediate server acknowledgements.
    3. Route messages to recipient if connected, or queue in OfflineMessageStore.
    4. Deliver queued offline messages when recipient reconnects.
    5. Propagate delivery/read acknowledgements back to the original sender.
    """
    def __init__(self) -> None:
        # User Routing Table: active_connections maps user_id -> UserClient instance
        self.active_connections: Dict[str, UserClient] = {}
        # Store for offline message persistence
        self.offline_store = OfflineMessageStore()
        # Message registry for tracking acknowledgements across the system
        self.message_registry: Dict[str, Message] = {}

    def register_connection(self, user_id: str, client: UserClient) -> None:
        """
        Registers an active connection for a user.
        If offline messages exist for this user, flushes and delivers them sequentially.
        """
        self.active_connections[user_id] = client
        
        # Check if user has queued messages waiting from while they were offline
        if self.offline_store.has_pending(user_id):
            pending_messages = self.offline_store.fetch_pending_messages(user_id)
            print(f"\n📦 [Server] Reconnection detected for '{user_id}'. Flushing {len(pending_messages)} offline message(s)...")
            
            for msg in list(pending_messages):
                print(f"   -> [Server] Delivering queued offline message {msg.message_id[:8]}... to '{user_id}'")
                client.receive_message(msg)
                
            # Clear flushed messages from offline storage
            self.offline_store.clear_pending(user_id)

    def unregister_connection(self, user_id: str) -> None:
        """Removes user from active connection routing table."""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            print(f"⚙️  [Server] Routing table updated: '{user_id}' marked OFFLINE.")

    def is_user_online(self, user_id: str) -> bool:
        """Checks if the user has an active connection registered."""
        return user_id in self.active_connections

    def route_message(self, sender_id: str, recipient_id: str, content: str) -> Message:
        """
        Core delivery routing pipeline:
        1. Generates unique message ID.
        2. Sets initial status to SENT_TO_SERVER (Server ACK).
        3. If recipient is online: Pushes immediately to recipient device.
        4. If recipient is offline: Persists in OfflineMessageStore for future delivery.
        """
        msg_id = str(uuid.uuid4())
        msg = Message(
            message_id=msg_id,
            sender_id=sender_id,
            recipient_id=recipient_id,
            content=content,
            status=MessageStatus.SENT_TO_SERVER
        )
        self.message_registry[msg_id] = msg

        if self.is_user_online(recipient_id):
            print(f"⚡ [Server] Recipient '{recipient_id}' is ONLINE. Pushing directly...")
            recipient_client = self.active_connections[recipient_id]
            recipient_client.receive_message(msg)
        else:
            print(f"💾 [Server] Recipient '{recipient_id}' is OFFLINE. Storing in OfflineMessageStore...")
            self.offline_store.store_message(recipient_id, msg)

        return msg

    def process_ack(self, message_id: str, status: MessageStatus) -> None:
        """
        Processes an incoming delivery or read acknowledgement from a recipient.
        Updates internal registry and notifies sender if online.
        """
        if message_id not in self.message_registry:
            return

        msg = self.message_registry[message_id]
        msg.status = status

        sender_id = msg.sender_id
        if self.is_user_online(sender_id):
            sender_client = self.active_connections[sender_id]
            sender_client.on_ack_received(message_id, status)
