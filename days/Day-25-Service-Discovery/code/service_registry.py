"""
In-Memory Service Registry for Service Discovery.

Manages instance registration, deregistration, heartbeats, active health state,
and dynamic lookup for services.
"""

import time
import threading
from typing import Dict, List, Optional
from service_instance import ServiceInstance


class ServiceRegistry:
    """
    Central directory maintaining the mapping between logical service names
    and active physical service instances.
    """

    def __init__(self, heartbeat_ttl_seconds: float = 10.0):
        # Mapping: service_name -> {instance_id: ServiceInstance}
        self._services: Dict[str, Dict[str, ServiceInstance]] = {}
        self._lock = threading.Lock()
        self.heartbeat_ttl_seconds = heartbeat_ttl_seconds

    def register(self, instance: ServiceInstance) -> bool:
        """
        Registers a new service instance or updates an existing one.
        """
        with self._lock:
            if instance.service_name not in self._services:
                self._services[instance.service_name] = {}
            
            instance.update_heartbeat()
            self._services[instance.service_name][instance.instance_id] = instance
            return True

    def deregister(self, service_name: str, instance_id: str) -> bool:
        """
        Removes a service instance from the registry upon graceful shutdown.
        """
        with self._lock:
            if service_name in self._services and instance_id in self._services[service_name]:
                del self._services[service_name][instance_id]
                if not self._services[service_name]:
                    del self._services[service_name]
                return True
            return False

    def heartbeat(self, service_name: str, instance_id: str) -> bool:
        """
        Refreshes the liveness heartbeat for a specific registered instance.
        """
        with self._lock:
            if service_name in self._services and instance_id in self._services[service_name]:
                self._services[service_name][instance_id].update_heartbeat()
                return True
            return False

    def set_health(self, service_name: str, instance_id: str, is_healthy: bool) -> bool:
        """
        Explicitly updates health status (e.g., from an active health checker).
        """
        with self._lock:
            if service_name in self._services and instance_id in self._services[service_name]:
                self._services[service_name][instance_id].is_healthy = is_healthy
                return True
            return False

    def discover(self, service_name: str, healthy_only: bool = True) -> List[ServiceInstance]:
        """
        Queries available instances for a logical service name.
        By default, returns only healthy instances that have not timed out.
        """
        with self._lock:
            now = time.time()
            instances = self._services.get(service_name, {})
            result = []
            
            for inst in instances.values():
                is_fresh = (now - inst.last_heartbeat) <= self.heartbeat_ttl_seconds
                if healthy_only:
                    if inst.is_healthy and is_fresh:
                        result.append(inst)
                else:
                    result.append(inst)
                    
            return result

    def evict_stale_instances(self) -> List[ServiceInstance]:
        """
        Removes instances that have failed to heartbeat within the TTL window.
        """
        evicted = []
        now = time.time()
        with self._lock:
            for service_name, instances in list(self._services.items()):
                for inst_id, inst in list(instances.items()):
                    if (now - inst.last_heartbeat) > self.heartbeat_ttl_seconds:
                        evicted.append(inst)
                        del instances[inst_id]
                if not instances:
                    del self._services[service_name]
        return evicted

    def get_all_services(self) -> Dict[str, List[ServiceInstance]]:
        """Returns a snapshot of all registered services and instances."""
        with self._lock:
            return {
                s_name: list(inst_map.values())
                for s_name, inst_map in self._services.items()
            }
