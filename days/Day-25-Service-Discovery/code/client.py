"""
Service Discovery Client.

Demonstrates client-side discovery: querying the Service Registry by logical
service name, selecting an available healthy instance (e.g., Round Robin),
and dispatching calls.
"""

from typing import Optional, List
from service_registry import ServiceRegistry
from service_instance import ServiceInstance


class ServiceDiscoveryClient:
    """
    Client that uses a ServiceRegistry to find and communicate with backend services.
    """

    def __init__(self, registry: ServiceRegistry, client_id: str = "caller-service"):
        self.registry = registry
        self.client_id = client_id
        self._rr_indices = {}  # service_name -> current round-robin index

    def get_healthy_instances(self, service_name: str) -> List[ServiceInstance]:
        """Queries registry for active healthy instances of a target service."""
        return self.registry.discover(service_name, healthy_only=True)

    def select_instance(self, service_name: str) -> Optional[ServiceInstance]:
        """
        Picks a healthy instance using client-side Round-Robin selection.
        """
        instances = self.get_healthy_instances(service_name)
        if not instances:
            return None
        
        idx = self._rr_indices.get(service_name, 0) % len(instances)
        selected = instances[idx]
        self._rr_indices[service_name] = (idx + 1) % len(instances)
        return selected

    def invoke(self, service_name: str, endpoint: str, payload: dict) -> str:
        """
        Discovers the destination instance by service name and executes the request.
        """
        target = self.select_instance(service_name)
        if not target:
            raise RuntimeError(
                f"[{self.client_id}] Service Discovery Error: No healthy instances available for '{service_name}'"
            )

        # Simulate network communication
        return f"[{self.client_id}] -> Called {target.instance_id} ({target.address}){endpoint} -> 200 OK | Payload: {payload}"
