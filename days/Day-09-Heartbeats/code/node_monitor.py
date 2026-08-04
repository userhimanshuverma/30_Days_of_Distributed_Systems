"""
node_monitor.py - Centralized Node Health Monitor for Heartbeat Tracking

This module provides the core primitives for tracking heartbeats in a distributed cluster:
- NodeState: Enum representing the operational state of a node (HEALTHY, SUSPECTED, UNHEALTHY).
- HeartbeatPayload: Data container for heartbeats sent by cluster nodes.
- NodeMonitor: Central controller that registers heartbeats, checks heartbeat freshness,
  and transitions node status based on configurable timeout thresholds.
"""

import time
from enum import Enum, auto
from typing import Dict, List, Optional
from dataclasses import dataclass


class NodeState(Enum):
    """
    Represents the health state of a node as evaluated by the monitoring process.
    
    HEALTHY: Heartbeats are arriving on schedule within expected intervals.
    SUSPECTED: Missed one or more consecutive heartbeats; degraded but not yet declared dead.
    UNHEALTHY: Exceeded the failure timeout threshold; declared dead by the cluster.
    """
    HEALTHY = auto()
    SUSPECTED = auto()
    UNHEALTHY = auto()


@dataclass
class HeartbeatPayload:
    """
    Lightweight message sent periodically by a node to indicate life.
    """
    node_id: str
    timestamp: float
    sequence_number: int


class NodeMonitor:
    """
    Tracks node heartbeats and determines node vitality based on timeout limits.
    
    Attributes:
        heartbeat_interval (float): Expected time between heartbeats in seconds.
        timeout_threshold (float): Duration without heartbeats before declaring node UNHEALTHY.
        max_missed_heartbeats (int): Number of missed beats before marking SUSPECTED.
    """
    def __init__(self, heartbeat_interval: float = 1.0, timeout_threshold: float = 3.0, max_missed_heartbeats: int = 1):
        self.heartbeat_interval = heartbeat_interval
        self.timeout_threshold = timeout_threshold
        self.max_missed_heartbeats = max_missed_heartbeats
        
        # State tracking structures
        self.last_heartbeat_time: Dict[str, float] = {}
        self.last_sequence_num: Dict[str, int] = {}
        self.node_states: Dict[str, NodeState] = {}
        self.missed_counts: Dict[str, int] = {}

    def register_node(self, node_id: str, current_time: Optional[float] = None) -> None:
        """Registers a new node in the cluster monitor with an initial HEALTHY state."""
        now = current_time if current_time is not None else time.time()
        self.last_heartbeat_time[node_id] = now
        self.last_sequence_num[node_id] = 0
        self.node_states[node_id] = NodeState.HEALTHY
        self.missed_counts[node_id] = 0

    def receive_heartbeat(self, payload: HeartbeatPayload) -> None:
        """
        Processes an incoming heartbeat payload from a node.
        
        Updates last known timestamp and sequence number, resetting missed beat counter.
        """
        node_id = payload.node_id
        if node_id not in self.node_states:
            self.register_node(node_id, payload.timestamp)

        self.last_heartbeat_time[node_id] = payload.timestamp
        self.last_sequence_num[node_id] = payload.sequence_number
        self.missed_counts[node_id] = 0
        
        # If node was previously SUSPECTED or UNHEALTHY, receiving a valid heartbeat restores HEALTHY
        prev_state = self.node_states[node_id]
        self.node_states[node_id] = NodeState.HEALTHY
        
        if prev_state != NodeState.HEALTHY:
            print(f"  [RECOVERY] Node '{node_id}' restored state from {prev_state.name} to HEALTHY.")

    def evaluate_node_health(self, node_id: str, current_time: Optional[float] = None) -> NodeState:
        """
        Evaluates the current health of a single node against configured timeouts.
        
        Returns the updated NodeState.
        """
        now = current_time if current_time is not None else time.time()
        if node_id not in self.last_heartbeat_time:
            return NodeState.UNHEALTHY

        elapsed = now - self.last_heartbeat_time[node_id]
        missed = int(elapsed // self.heartbeat_interval)
        self.missed_counts[node_id] = missed

        previous_state = self.node_states[node_id]

        if elapsed >= self.timeout_threshold:
            new_state = NodeState.UNHEALTHY
        elif missed >= self.max_missed_heartbeats:
            new_state = NodeState.SUSPECTED
        else:
            new_state = NodeState.HEALTHY

        if new_state != previous_state:
            print(f"  [STATE CHANGE] Node '{node_id}': {previous_state.name} -> {new_state.name} "
                  f"(Elapsed: {elapsed:.2f}s, Missed Beats: {missed})")
            self.node_states[node_id] = new_state

        return new_state

    def check_all_nodes(self, current_time: Optional[float] = None) -> Dict[str, NodeState]:
        """Evaluates health across all registered nodes."""
        now = current_time if current_time is not None else time.time()
        results = {}
        for node_id in list(self.last_heartbeat_time.keys()):
            results[node_id] = self.evaluate_node_health(node_id, now)
        return results
