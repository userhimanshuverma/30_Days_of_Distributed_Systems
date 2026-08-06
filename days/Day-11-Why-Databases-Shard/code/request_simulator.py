"""
request_simulator.py
--------------------
Simulates workload generation from multiple stateless Application Servers 
attempting to read and write state from a single, centralized Database.

This module provides data structures and helper utilities for simulating:
1. Application Server instances emitting concurrent HTTP/RPC transactional requests.
2. Synthetic workload request objects (e.g., READ user profile, WRITE order).
3. Realistic network latencies and client thread management.
"""

import time
import random
import dataclasses
from typing import List, Dict, Any, Optional
from enum import Enum


class RequestType(Enum):
    """Types of database operations initiated by Application Servers."""
    READ_PROFILE = "READ_PROFILE"      # Lightweight read
    CHECK_INVENTORY = "CHECK_INVENTORY"# Moderate read
    CREATE_ORDER = "CREATE_ORDER"      # Heavy write (requires transaction locks)
    PROCESS_PAYMENT = "PROCESS_PAYMENT"# Heavy write (requires strict serialization)


@dataclasses.dataclass
class DatabaseRequest:
    """Represents an incoming query or command sent to the single database."""
    request_id: str
    server_id: str
    request_type: RequestType
    created_at: float
    estimated_db_cost_ms: float
    payload_size_kb: float


class ApplicationServer:
    """
    Simulates a stateless Application Server.
    
    In modern web architectures, application servers scale out horizontally with ease.
    Each app server handles incoming user traffic by opening connection pools to the central database.
    """

    def __init__(self, server_id: str):
        self.server_id = server_id
        self.requests_sent: int = 0
        self.requests_completed: int = 0
        self.total_wait_time_ms: float = 0.0

    def generate_request(self) -> DatabaseRequest:
        """Generates a realistic database operation request based on traffic distribution."""
        self.requests_sent += 1
        req_id = f"req-{self.server_id}-{self.requests_sent}"

        # Workload mix: 60% Reads, 40% Writes
        rand_val = random.random()
        if rand_val < 0.40:
            req_type = RequestType.READ_PROFILE
            cost_ms = random.uniform(1.0, 3.0)  # Simple index lookup
            payload_kb = random.uniform(0.5, 2.0)
        elif rand_val < 0.70:
            req_type = RequestType.CHECK_INVENTORY
            cost_ms = random.uniform(2.0, 5.0)  # Range read
            payload_kb = random.uniform(1.0, 4.0)
        elif rand_val < 0.90:
            req_type = RequestType.CREATE_ORDER
            cost_ms = random.uniform(10.0, 20.0) # Write + index update + write lock
            payload_kb = random.uniform(2.0, 8.0)
        else:
            req_type = RequestType.PROCESS_PAYMENT
            cost_ms = random.uniform(15.0, 30.0) # Disk commit lock
            payload_kb = random.uniform(1.0, 3.0)

        return DatabaseRequest(
            request_id=req_id,
            server_id=self.server_id,
            request_type=req_type,
            created_at=time.time(),
            estimated_db_cost_ms=cost_ms,
            payload_size_kb=payload_kb
        )

    def record_completion(self, wait_time_ms: float) -> None:
        """Tracks latency experienced by this application server."""
        self.requests_completed += 1
        self.total_wait_time_ms += wait_time_ms

    @property
    def average_latency_ms(self) -> float:
        """Calculates mean response time experienced by this server."""
        if self.requests_completed == 0:
            return 0.0
        return self.total_wait_time_ms / self.requests_completed
