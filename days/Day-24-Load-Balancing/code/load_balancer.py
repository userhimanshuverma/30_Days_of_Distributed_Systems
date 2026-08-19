#!/usr/bin/env python3
"""
Day 24 — Load Balancer Implementation (Educational Simulation)
--------------------------------------------------------------
This module provides a zero-dependency, self-contained Python implementation of an
in-memory Load Balancer featuring health checks and Round Robin request distribution.

Goal:
    Decide where incoming requests go across available backend server capacity,
    automatically skipping unhealthy servers and resuming traffic routing when backends recover.

NOTE:
    This is an educational simulation designed for teaching distributed systems concepts.
    Production load balancers (such as NGINX, HAProxy, Envoy, or AWS ALB) operate at the
    OS socket / IP stack level (Layer 4 / Layer 7) with multi-threaded event loops,
    epoll/kqueue I/O, and hardware-accelerated TLS termination.
"""

from typing import List, Dict, Optional, Callable
import logging

# Configure logging for decision tracing
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("LoadBalancer")


class BackendServer:
    """
    Represents an individual backend application server managed by the load balancer.

    Attributes:
        server_id (str): Unique name or IP identifier of the backend server.
        weight (int): Capacity weighting factor for weighted algorithms (default: 1).
        is_healthy (bool): Whether the server is currently passing health checks.
        active_connections (int): Number of requests currently being processed.
        total_requests_handled (int): Cumulative count of requests routed to this server.
    """

    def __init__(self, server_id: str, weight: int = 1):
        self.server_id = server_id
        self.weight = weight
        self.is_healthy = True
        self.active_connections = 0
        self.total_requests_handled = 0

    def mark_unhealthy(self) -> None:
        """Mark backend as failed/unhealthy."""
        if self.is_healthy:
            self.is_healthy = False
            logger.warning(f"Server '{self.server_id}' marked UNHEALTHY.")

    def mark_healthy(self) -> None:
        """Mark backend as healthy/recovered."""
        if not self.is_healthy:
            self.is_healthy = True
            logger.info(f"Server '{self.server_id}' marked HEALTHY.")

    def __repr__(self) -> str:
        status = "HEALTHY" if self.is_healthy else "UNHEALTHY"
        return f"<BackendServer id={self.server_id} status={status} active={self.active_connections} total={self.total_requests_handled}>"


class LoadBalancer:
    """
    A Traffic-Control Layer distributing incoming requests across backend servers.

    Parameters:
        server_ids (List[str]): Initial list of server identifiers (e.g. ['server-a', 'server-b', 'server-c']).
        algorithm (str): Routing algorithm to use ('round_robin', 'least_connections', or 'weighted_round_robin').
    """

    def __init__(self, server_ids: List[str], algorithm: str = "round_robin"):
        self.servers: Dict[str, BackendServer] = {
            s_id: BackendServer(s_id) for s_id in server_ids
        }
        self.algorithm = algorithm
        self._rr_index = 0

    def add_server(self, server_id: str, weight: int = 1) -> None:
        """Add a new server to the backend pool dynamically."""
        if server_id not in self.servers:
            self.servers[server_id] = BackendServer(server_id, weight=weight)
            logger.info(f"Added new server '{server_id}' to load balancer pool.")

    def remove_server(self, server_id: str) -> None:
        """Remove a server from the load balancer pool (e.g., server decommissioned)."""
        if server_id in self.servers:
            del self.servers[server_id]
            logger.info(f"Removed server '{server_id}' from load balancer pool.")

    def set_server_health(self, server_id: str, is_healthy: bool) -> None:
        """Explicitly set the health status of a backend server."""
        if server_id in self.servers:
            if is_healthy:
                self.servers[server_id].mark_healthy()
            else:
                self.servers[server_id].mark_unhealthy()

    def get_healthy_servers(self) -> List[BackendServer]:
        """Return all servers that are currently marked healthy."""
        return [s for s in self.servers.values() if s.is_healthy]

    def next_server(self) -> Optional[str]:
        """
        Select and return the identifier of the next healthy backend server.

        Decision Process:
            1. Filter all available servers to find only those marked HEALTHY.
            2. If no healthy servers exist, reject request (returns None).
            3. Apply the routing algorithm (e.g. Round Robin) to select a healthy backend.
            4. Increment active connections and total request metrics.
            5. Return the selected server ID.

        Returns:
            Optional[str]: Server identifier (e.g. 'server-a') or None if all backends are down.
        """
        healthy_servers = self.get_healthy_servers()

        if not healthy_servers:
            logger.error("ALL BACKEND SERVERS ARE UNHEALTHY! Request dropped (503 Service Unavailable).")
            return None

        selected: BackendServer

        if self.algorithm == "least_connections":
            # Select healthy server with lowest active connection count
            selected = min(healthy_servers, key=lambda s: s.active_connections)
        elif self.algorithm == "weighted_round_robin":
            # Simplified weighted round robin: expand servers by weight
            weighted_pool = []
            for s in healthy_servers:
                weighted_pool.extend([s] * s.weight)
            selected = weighted_pool[self._rr_index % len(weighted_pool)]
            self._rr_index = (self._rr_index + 1) % len(weighted_pool)
        else:
            # Standard Round Robin across healthy backends
            selected = healthy_servers[self._rr_index % len(healthy_servers)]
            self._rr_index = (self._rr_index + 1) % len(healthy_servers)

        # Update server metrics
        selected.active_connections += 1
        selected.total_requests_handled += 1

        logger.info(f"Routed request to '{selected.server_id}' [Active: {selected.active_connections}, Total: {selected.total_requests_handled}]")
        return selected.server_id

    def release_connection(self, server_id: str) -> None:
        """Decrement active connection count when a request finishes processing."""
        if server_id in self.servers and self.servers[server_id].active_connections > 0:
            self.servers[server_id].active_connections -= 1

    def run_health_checks(self, check_fn: Callable[[str], bool]) -> Dict[str, bool]:
        """
        Execute active health checks against all registered backend servers.

        Args:
            check_fn: A callable taking server_id and returning True if healthy, False otherwise.

        Returns:
            Dict[str, bool]: Health status mapping for all backends.
        """
        results = {}
        for server_id, server in self.servers.items():
            is_healthy = check_fn(server_id)
            self.set_server_health(server_id, is_healthy)
            results[server_id] = is_healthy
        return results
