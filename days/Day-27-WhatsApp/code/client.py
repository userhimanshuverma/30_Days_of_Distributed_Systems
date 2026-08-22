"""
Day 27: How WhatsApp Delivers Billions of Messages
Component: User Client Simulation

Simulates a mobile messaging client (e.g., WhatsApp mobile app).
Manages connection state, sending messages, receiving pushed messages, and sending back
acknowledgements (DELIVERED, READ) to the server.
"""

import sys
from typing import Dict, List, Optional, TYPE_CHECKING
from message_store import Message, MessageStatus

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

if TYPE_CHECKING:
    from server import MessagingServer


class UserClient:
    """
    Simulates an individual client device connected to the messaging system.
    
    Attributes:
        user_id: Unique handle identifying the user (e.g., 'alice', 'bob').
        server: Reference to the central MessagingServer gateway.
        is_connected: Boolean flag indicating if active socket/long-lived connection exists.
        inbox: Received messages currently stored on the client device.
        sent_status_tracker: Tracks status updates (SENT, DELIVERED, READ) for messages sent by this client.
    """
    def __init__(self, user_id: str, server: 'MessagingServer') -> None:
        self.user_id = user_id
        self.server = server
        self.is_connected = False
        self.inbox: List[Message] = []
        self.sent_status_tracker: Dict[str, MessageStatus] = {}

    def connect(self) -> None:
        """
        Establishes long-lived connection with the messaging infrastructure.
        Triggers automatic delivery of queued offline messages.
        """
        self.is_connected = True
        print(f"🟢 [Client:{self.user_id}] Connected to messaging server.")
        self.server.register_connection(self.user_id, self)

    def disconnect(self) -> None:
        """Simulates network loss, device powering off, or Wi-Fi disconnection."""
        self.is_connected = False
        self.server.unregister_connection(self.user_id)
        print(f"🔴 [Client:{self.user_id}] Disconnected from server.")

    def send_message(self, recipient_id: str, content: str) -> Optional[Message]:
        """
        Sends a message to the target recipient via the messaging server.
        
        Returns:
            The accepted Message object with SENT_TO_SERVER status, or None if client is disconnected.
        """
        if not self.is_connected:
            print(f"⚠️  [Client:{self.user_id}] Cannot send message while offline.")
            return None

        print(f"📤 [Client:{self.user_id}] Sending message to '{recipient_id}': \"{content}\"")
        msg = self.server.route_message(self.user_id, recipient_id, content)
        if msg:
            self.sent_status_tracker[msg.message_id] = msg.status
            print(f"   ✓ [Client:{self.user_id}] Server ACK received: Message {msg.message_id[:8]}... is {msg.status.value}")
        return msg

    def receive_message(self, message: Message) -> None:
        """
        Callback invoked by the server when a message is pushed to this client.
        Automatically responds with a DELIVERED acknowledgement.
        """
        self.inbox.append(message)
        print(f"📥 [Client:{self.user_id}] Received message from '{message.sender_id}': \"{message.content}\"")
        
        # Send DELIVERED ACK back to server
        self.server.process_ack(message.message_id, MessageStatus.DELIVERED)

    def read_message(self, message_id: str) -> None:
        """
        Simulates the user opening the app and viewing a specific message.
        Sends a READ acknowledgement back to the server.
        """
        for msg in self.inbox:
            if msg.message_id == message_id:
                msg.status = MessageStatus.READ
                print(f"👁️  [Client:{self.user_id}] Read message {message_id[:8]}...")
                self.server.process_ack(message_id, MessageStatus.READ)
                return
        print(f"⚠️  [Client:{self.user_id}] Message {message_id[:8]}... not found in inbox.")

    def on_ack_received(self, message_id: str, status: MessageStatus) -> None:
        """
        Callback invoked by the server when a recipient updates the status of a sent message.
        (e.g., single tick -> double tick -> blue ticks).
        """
        self.sent_status_tracker[message_id] = status
        print(f"🔔 [Client:{self.user_id}] Status update for message {message_id[:8]}... -> {status.value}")
