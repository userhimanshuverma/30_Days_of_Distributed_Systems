"""
Service Instance representation for Service Discovery.

Represents a single running instance of a microservice with network location,
health status, and metadata.
"""

from dataclasses import dataclass, field
import time
from typing import Dict, Any


@dataclass
class ServiceInstance:
    """
    Represents a discrete running instance of a service.
    
    Attributes:
        service_name: Logical identity of the service (e.g., 'payment-service')
        instance_id: Unique identifier for this specific instance (e.g., 'payment-inst-1')
        host: IP address or hostname where this instance is listening
        port: Port number for network traffic
        is_healthy: Real-time health status of this instance
        last_heartbeat: Timestamp of the most recent heartbeat ping
        metadata: Optional key-value pairs (e.g., version, availability zone, tags)
    """
    service_name: str
    instance_id: str
    host: str
    port: int
    is_healthy: bool = True
    last_heartbeat: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def address(self) -> str:
        """Returns the full socket address of the instance."""
        return f"{self.host}:{self.port}"

    def update_heartbeat(self) -> None:
        """Refreshes the heartbeat timestamp to signify active liveness."""
        self.last_heartbeat = time.time()

    def __repr__(self) -> str:
        status = "HEALTHY" if self.is_healthy else "UNHEALTHY"
        return f"[{self.service_name} | {self.instance_id} @ {self.address} ({status})]"
