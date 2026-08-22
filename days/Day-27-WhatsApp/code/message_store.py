"""
Day 27: How WhatsApp Delivers Billions of Messages
Component: Offline Message Store & Message State Management

This module provides the data structures for representing messages, tracking their
acknowledgement lifecycle, and persisting messages when recipient devices are offline.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional
import time
import uuid


class MessageStatus(Enum):
    """
    Tracks the life cycle of a message in the system.
    
    - SENT_TO_SERVER: Accepted by the messaging server/gateway.
    - DELIVERED: Successfully pushed to and received by the recipient's device.
    - READ: Recipient opened/viewed the message.
    """
    SENT_TO_SERVER = "SENT_TO_SERVER"
    DELIVERED = "DELIVERED"
    READ = "READ"


@dataclass
class Message:
    """
    Represents an immutable message unit flowing through the system.
    
    Attributes:
        message_id: Unique identifier for idempotency and tracking.
        sender_id: ID of the user sending the message.
        recipient_id: ID of the target user.
        content: Text payload of the message.
        timestamp: Unix timestamp when the message was accepted.
        status: Current acknowledgement state.
    """
    message_id: str
    sender_id: str
    recipient_id: str
    content: str
    timestamp: float = field(default_factory=time.time)
    status: MessageStatus = MessageStatus.SENT_TO_SERVER

    def __repr__(self) -> str:
        return (f"Message(id={self.message_id[:8]}..., "
                f"from={self.sender_id}, to={self.recipient_id}, "
                f"status={self.status.value}, content='{self.content}')")


class OfflineMessageStore:
    """
    In-memory temporary storage for messages addressed to offline users.
    
    In a production system (like WhatsApp's architecture), offline messages are stored
    temporarily in a persistent database (e.g., RocksDB, Cassandra, or custom store)
    until the recipient reconnects and acknowledges receipt. Once acknowledged,
    the server can safely purge the message from server storage.
    """
    def __init__(self) -> None:
        # Maps recipient_id -> List of pending Message objects (FIFO queue per user)
        self._store: Dict[str, List[Message]] = {}

    def store_message(self, recipient_id: str, message: Message) -> None:
        """Stores a message for an offline user."""
        if recipient_id not in self._store:
            self._store[recipient_id] = []
        self._store[recipient_id].append(message)

    def fetch_pending_messages(self, recipient_id: str) -> List[Message]:
        """Retrieves all pending messages for a user without deleting them yet."""
        return self._store.get(recipient_id, [])

    def clear_pending(self, recipient_id: str) -> None:
        """Purges pending messages after receipt is confirmed."""
        if recipient_id in self._store:
            del self._store[recipient_id]

    def has_pending(self, recipient_id: str) -> bool:
        """Returns True if there are stored messages for the recipient."""
        return bool(self._store.get(recipient_id))

    def get_pending_count(self, recipient_id: str) -> int:
        """Returns the count of queued offline messages for a user."""
        return len(self._store.get(recipient_id, []))
