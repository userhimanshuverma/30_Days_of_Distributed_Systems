"""
simple_consensus.py - Educational Simulation of Majority Consensus

This module provides an intuitive, high-level simulation of consensus in a distributed system.
It demonstrates how a designated leader node proposes a decision to follower nodes
and requires a strict majority approval before committing the change to the cluster state.

Key Concepts Demonstrated:
1. Leader Proposal: The leader does NOT unilaterally execute changes. It broadcasts a proposal.
2. Follower Voting: Followers receive the proposal, inspect network availability, and cast a vote.
3. Majority Quorum: The decision is COMMITTED only if a majority (N/2 + 1) of nodes agree.
4. Safe Rejection: If network delays or server failures prevent a majority, the proposal is REJECTED.
"""

from typing import List, Dict, Optional
import time


class Proposal:
    """
    Represents a proposed cluster state change (e.g., "Deploy Nginx Pod v2").
    """
    def __init__(self, proposal_id: str, action: str):
        self.proposal_id = proposal_id
        self.action = action
        self.votes_received: List[str] = []
        self.is_committed: bool = False
        self.is_rejected: bool = False

    def __repr__(self) -> str:
        status = "COMMITTED" if self.is_committed else ("REJECTED" if self.is_rejected else "PENDING")
        return f"Proposal(id='{self.proposal_id}', action='{self.action}', votes={len(self.votes_received)}, status={status})"


class Node:
    """
    Represents a single machine in the distributed cluster.
    """
    def __init__(self, node_id: str, is_leader: bool = False):
        self.node_id = node_id
        self.is_leader = is_leader
        self.is_reachable: bool = True
        self.committed_log: List[str] = []

    def receive_proposal(self, proposal: Proposal) -> bool:
        """
        Simulates receiving a proposal from the leader.
        Returns True if the node votes YES, False if unreachable or voting NO.
        """
        if not self.is_reachable:
            print(f"  [X] [{self.node_id}] Network timeout / Node unreachable. No vote cast.")
            return False
        
        # In a healthy state, follower evaluates and approves proposal
        print(f"  [YES] [{self.node_id}] Received proposal '{proposal.action}' -> Voted YES.")
        return True

    def apply_decision(self, action: str) -> None:
        """
        Applies the committed action to the local state after majority agreement.
        """
        if self.is_reachable:
            self.committed_log.append(action)
            print(f"  [APPLIED] [{self.node_id}] Applied committed action to local state: '{action}'")


class ConsensusCluster:
    """
    Manages a cluster of nodes and coordinates the consensus process.
    """
    def __init__(self, node_ids: List[str], leader_id: str):
        self.nodes: Dict[str, Node] = {
            nid: Node(nid, is_leader=(nid == leader_id))
            for nid in node_ids
        }
        self.leader_id = leader_id
        self.total_nodes = len(node_ids)
        # Majority Quorum calculation: Strictly greater than half (e.g., 3 out of 5)
        self.majority_threshold = (self.total_nodes // 2) + 1

        print(f"=== Initialized Cluster ({self.total_nodes} nodes) ===")
        print(f"Leader: {self.leader_id} | Majority Quorum Needed: {self.majority_threshold}/{self.total_nodes}\n")

    def get_leader(self) -> Node:
        return self.nodes[self.leader_id]

    def set_node_network_status(self, node_id: str, is_reachable: bool) -> None:
        """Helper to simulate network delays or node crashes."""
        if node_id in self.nodes:
            self.nodes[node_id].is_reachable = is_reachable
            status = "ONLINE" if is_reachable else "OFFLINE / UNREACHABLE"
            print(f"[NETWORK UPDATE] Node '{node_id}' is now {status}.")

    def propose_action(self, proposal_id: str, action: str) -> bool:
        """
        Executes the 2-phase agreement process:
        Phase 1: Leader broadcasts proposal and collects follower votes.
        Phase 2: Leader counts votes. If majority reached -> COMMIT; else -> REJECT.
        """
        leader = self.get_leader()
        if not leader.is_reachable:
            print(f"[ERROR] Leader '{self.leader_id}' is offline! Cannot initiate proposal.")
            return False

        proposal = Proposal(proposal_id, action)
        print(f"\n[Leader {self.leader_id}] Proposing Action: '{action}' (ID: {proposal_id})")
        print(f"--- Phase 1: Broadcasting Proposal to All Nodes ---")

        # Leader automatically votes YES for its own proposal
        proposal.votes_received.append(leader.node_id)
        print(f"  [YES] [{leader.node_id}] (Leader) Initiated and voted YES.")

        # Request votes from all follower nodes
        for node_id, node in self.nodes.items():
            if node_id == self.leader_id:
                continue
            
            if node.receive_proposal(proposal):
                proposal.votes_received.append(node_id)

        votes_count = len(proposal.votes_received)
        print(f"\n--- Phase 2: Counting Votes ---")
        print(f"Votes Collected: {votes_count} / {self.total_nodes} (Required for Majority: {self.majority_threshold})")

        # Check if majority quorum was achieved
        if votes_count >= self.majority_threshold:
            proposal.is_committed = True
            print(f"\n[SUCCESS] MAJORITY ACHIEVED! Proposal '{action}' is COMMITTED.")
            
            # Broadcast commit decision to all reachable nodes
            print("\n--- Phase 3: Applying Decision Across Cluster ---")
            for node in self.nodes.values():
                node.apply_decision(action)
            return True
        else:
            proposal.is_rejected = True
            print(f"\n[REJECTED] MAJORITY NOT REACHED! Proposal '{action}' is REJECTED to preserve cluster safety.")
            print("[SAFEGUARD] No state changes were applied to any node.")
            return False
