"""
simple_cluster.py - Educational Simulation of Cluster Roles (Leader & Followers)

This module defines the foundational primitives for a distributed cluster model:
- ClusterRole: Enum representing whether a node is a LEADER or FOLLOWER.
- Task: A unit of work requiring coordinated execution across the cluster.
- Node: A server node that can operate as a Leader or Follower, receiving and forwarding tasks.
- Cluster: A manager for interconnected nodes that handles node registration and cluster state.
"""

from enum import Enum, auto
from typing import List, Dict, Optional


class ClusterRole(Enum):
    """
    Represents the operational role of a node within the cluster.
    
    LEADER: Responsible for making authoritative decisions, coordinating cluster state,
            and preventing duplicate or conflicting task assignments.
    FOLLOWER: Accepts requests, forwards coordination tasks to the leader, and executes
              assigned work locally.
    """
    LEADER = auto()
    FOLLOWER = auto()


class Task:
    """
    Represents a job or coordination request sent to the cluster.
    """
    def __init__(self, task_id: str, description: str):
        self.task_id = task_id
        self.description = description
        self.assigned_node_id: Optional[str] = None
        self.completed: bool = False

    def __repr__(self) -> str:
        return f"Task(id='{self.task_id}', desc='{self.description}', assigned_to={self.assigned_node_id})"


class Node:
    """
    Represents a single server node in a distributed cluster.
    """
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.role: ClusterRole = ClusterRole.FOLLOWER
        self.is_alive: bool = True
        self.known_leader_id: Optional[str] = None
        self.processed_tasks: List[Task] = []

    def set_role(self, role: ClusterRole, leader_id: Optional[str] = None) -> None:
        """Assigns the role for this node and points to the current leader."""
        self.role = role
        if role == ClusterRole.LEADER:
            self.known_leader_id = self.node_id
        else:
            self.known_leader_id = leader_id

    def handle_request(self, task: Task, cluster_nodes: Dict[str, "Node"]) -> bool:
        """
        Processes an incoming task request.
        
        If this node is the LEADER:
            - Performs central coordination and assigns/executes the task.
        If this node is a FOLLOWER:
            - Forwards the request to the known LEADER to guarantee single-coordinator decision making.
        """
        if not self.is_alive:
            print(f"[DEAD] [{self.node_id}] Node is dead and cannot accept tasks.")
            return False

        if self.role == ClusterRole.LEADER:
            print(f"[LEADER] [{self.node_id}] Coordinating task '{task.task_id}': {task.description}")
            task.assigned_node_id = self.node_id
            task.completed = True
            self.processed_tasks.append(task)
            print(f"[SUCCESS] [{self.node_id}] Successfully coordinated task '{task.task_id}'.")
            return True
        else:
            print(f"[FOLLOWER] [{self.node_id}] Received task '{task.task_id}'. Forwarding to Leader ({self.known_leader_id})...")
            
            if not self.known_leader_id or self.known_leader_id not in cluster_nodes:
                print(f"[WARNING] [{self.node_id}] Cannot process task! No known leader available.")
                return False

            leader_node = cluster_nodes[self.known_leader_id]
            if not leader_node.is_alive:
                print(f"[FORWARD FAILED] [{self.node_id}] Forwarding failed! Leader '{leader_node.node_id}' is dead.")
                return False
                
            return leader_node.handle_request(task, cluster_nodes)

    def stop(self) -> None:
        """Simulates a node failure/stop."""
        self.is_alive = False
        print(f"[STOPPED] [{self.node_id}] Server stopped / crashed!")


class Cluster:
    """
    Manages a group of server nodes forming a distributed cluster.
    """
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.current_leader_id: Optional[str] = None

    def add_node(self, node: Node) -> None:
        """Registers a new node into the cluster."""
        self.nodes[node.node_id] = node
        print(f"[REGISTER] Registered {node.node_id} in cluster.")

    def set_leader(self, leader_id: str) -> None:
        """Designates a node as the leader and updates all followers."""
        if leader_id not in self.nodes:
            raise ValueError(f"Node {leader_id} does not exist in cluster.")

        self.current_leader_id = leader_id
        for nid, node in self.nodes.items():
            if nid == leader_id:
                node.set_role(ClusterRole.LEADER)
            else:
                node.set_role(ClusterRole.FOLLOWER, leader_id=leader_id)
        print(f"\n[LEADER ELECTED] Node '{leader_id}' designated as the Cluster Leader.")

    def send_task_to_node(self, target_node_id: str, task: Task) -> bool:
        """Sends a task request to an arbitrary node in the cluster."""
        if target_node_id not in self.nodes:
            print(f"[ERROR] Node '{target_node_id}' does not exist.")
            return False
        
        print(f"\n[CLIENT REQUEST] Submitting Task '{task.task_id}' to Node '{target_node_id}'...")
        return self.nodes[target_node_id].handle_request(task, self.nodes)
