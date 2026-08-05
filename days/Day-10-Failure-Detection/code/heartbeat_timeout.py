"""
heartbeat_timeout.py - Simplified Failure Detector and Timeout Evaluation Model

This module defines the core data models and failure detection logic for a 
distributed cluster. It models failure detection as an estimation process under
uncertainty:
- Nodes periodically send heartbeats.
- The FailureDetector tracks the timestamp of the last received heartbeat for each node.
- If elapsed time exceeds a configurable timeout, the node state transitions:
  HEALTHY -> SUSPECTED -> FAILED.
- Triggers recovery callbacks upon failure declaration.

NOTE: This is a simplified educational model designed to illustrate the mental 
model of failure detection under network uncertainty.
"""

import time
from enum import Enum
from typing import Dict, Optional, Callable


class NodeStatus(Enum):
    """
    Represents the health state of a node from the cluster monitor's perspective.
    
    In distributed systems, state is always an estimate based on observation,
    never an absolute guarantee of physical hardware reality.
    """
    HEALTHY = "HEALTHY"        # Heartbeats arriving on time
    SUSPECTED = "SUSPECTED"    # Missed one or more heartbeats, timeout counter ticking
    FAILED = "FAILED"          # Timeout threshold exceeded, node declared dead


class Heartbeat:
    """
    Represents a heartbeat message emitted by a worker node.
    """
    def __init__(self, node_id: str, timestamp: float, sequence_number: int):
        self.node_id = node_id
        self.timestamp = timestamp
        self.sequence_number = sequence_number

    def __repr__(self) -> str:
        return f"Heartbeat(node={self.node_id}, seq={self.sequence_number}, ts={self.timestamp:.2f}s)"


class FailureDetector:
    """
    A heartbeat-timeout based failure detector.
    
    The detector observes incoming heartbeats and evaluates node status relative
    to a heartbeat interval and a timeout threshold.
    """
    def __init__(
        self,
        heartbeat_interval: float = 1.0,
        timeout_threshold: float = 3.0,
        on_failure_callback: Optional[Callable[[str], None]] = None
    ):
        """
        :param heartbeat_interval: Expected time interval (in seconds) between heartbeats.
        :param timeout_threshold: Time elapsed (in seconds) before declaring a node FAILED.
        :param on_failure_callback: Optional function invoked when a node transitions to FAILED.
        """
        self.heartbeat_interval = heartbeat_interval
        self.timeout_threshold = timeout_threshold
        self.on_failure_callback = on_failure_callback

        # Tracks last heartbeat timestamp received from each node: {node_id: timestamp}
        self.last_heartbeat: Dict[str, float] = {}

        # Tracks current evaluated status of each node: {node_id: NodeStatus}
        self.node_states: Dict[str, NodeStatus] = {}

        # Tracks how long each node has been silent: {node_id: silence_duration_seconds}
        self.silence_duration: Dict[str, float] = {}

    def register_node(self, node_id: str, current_time: float) -> None:
        """Registers a new node with the failure detector at simulation start."""
        self.last_heartbeat[node_id] = current_time
        self.node_states[node_id] = NodeStatus.HEALTHY
        self.silence_duration[node_id] = 0.0

    def receive_heartbeat(self, heartbeat: Heartbeat) -> None:
        """
        Processes an incoming heartbeat message from a node.
        Resets the silence timer and restores state to HEALTHY.
        """
        node_id = heartbeat.node_id
        self.last_heartbeat[node_id] = heartbeat.timestamp
        self.silence_duration[node_id] = 0.0
        
        previous_state = self.node_states.get(node_id, NodeStatus.HEALTHY)
        self.node_states[node_id] = NodeStatus.HEALTHY

        if previous_state != NodeStatus.HEALTHY:
            print(f"  [RECOVERY] Node '{node_id}' sent a heartbeat! State restored: {previous_state.value} -> HEALTHY")

    def evaluate_nodes(self, current_time: float) -> Dict[str, NodeStatus]:
        """
        Evaluates the health status of all registered nodes based on current time.
        
        Transitions:
        - Silence > heartbeat_interval: HEALTHY -> SUSPECTED
        - Silence >= timeout_threshold: SUSPECTED -> FAILED
        """
        for node_id, last_ts in list(self.last_heartbeat.items()):
            current_status = self.node_states[node_id]
            
            # If already marked FAILED, no further timeout evaluation needed
            if current_status == NodeStatus.FAILED:
                continue

            elapsed = current_time - last_ts
            self.silence_duration[node_id] = elapsed

            if elapsed >= self.timeout_threshold:
                # Silence exceeded safety limit — declare failure with high confidence
                self.node_states[node_id] = NodeStatus.FAILED
                print(f"  [TIMEOUT EXCEEDED] Node '{node_id}' silent for {elapsed:.1f}s (>= {self.timeout_threshold:.1f}s threshold).")
                print(f"  [STATE CHANGE] Node '{node_id}': {current_status.value} -> FAILED")
                
                # Trigger cluster recovery actions
                if self.on_failure_callback:
                    self.on_failure_callback(node_id)

            elif elapsed > self.heartbeat_interval:
                # Missed at least one heartbeat — suspect failure under uncertainty
                if current_status == NodeStatus.HEALTHY:
                    self.node_states[node_id] = NodeStatus.SUSPECTED
                    print(f"  [WARNING] Node '{node_id}' missed expected heartbeat. Silent for {elapsed:.1f}s.")
                    print(f"  [STATE CHANGE] Node '{node_id}': HEALTHY -> SUSPECTED")

        return self.node_states
