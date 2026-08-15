"""
two_phase_commit.py — Educational simulation of the Two-Phase Commit (2PC) protocol.

Demonstrates:
1. Two-Phase Commit Lifecycle (Phase 1: Prepare, Phase 2: Commit / Abort).
2. Participant decision logic and resource locking during PREPARE.
3. Successful 2PC coordination.
4. Participant Abort handling.
5. Coordinator Failure Scenario: Participants locked in PREPARED state (Indecision / Blocking).
"""

import sys
from enum import Enum, auto
from typing import List, Dict, Optional

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class ParticipantState(Enum):
    INIT = auto()
    PREPARED = auto()
    COMMITTED = auto()
    ABORTED = auto()

class Vote(Enum):
    YES = auto()
    NO = auto()

class Participant:
    """Simulates a database participant in a 2PC protocol."""
    def __init__(self, name: str, balance: float):
        self.name = name
        self.balance = balance
        self.state = ParticipantState.INIT
        self.locked_amount: float = 0.0
        self.pending_operation: Optional[str] = None  # "DEBIT" or "CREDIT"
        self.wal_log: List[str] = []  # Write-Ahead Log

    def prepare(self, tx_id: str, operation: str, amount: float) -> Vote:
        """
        Phase 1: Prepare.
        Checks constraints, acquires locks, writes undo/redo log, and votes.
        """
        self.wal_log.append(f"PREPARE_REQUEST {tx_id} {operation} {amount}")
        
        if operation == "DEBIT":
            if self.balance < amount:
                print(f"  └─ [{self.name}] Voting NO: Insufficient funds (Balance ₹{self.balance}, Need ₹{amount})")
                self.wal_log.append(f"VOTE_NO {tx_id}")
                return Vote.NO
            
            # Lock resources for transaction duration
            self.locked_amount = amount
            self.pending_operation = "DEBIT"
            self.state = ParticipantState.PREPARED
            self.wal_log.append(f"VOTE_YES_PREPARED {tx_id}")
            print(f"  └─ [{self.name}] Prepared successfully. Locked ₹{amount:.2f}. Voted YES.")
            return Vote.YES

        elif operation == "CREDIT":
            self.locked_amount = amount
            self.pending_operation = "CREDIT"
            self.state = ParticipantState.PREPARED
            self.wal_log.append(f"VOTE_YES_PREPARED {tx_id}")
            print(f"  └─ [{self.name}] Prepared successfully. Reserved credit ₹{amount:.2f}. Voted YES.")
            return Vote.YES

        return Vote.NO

    def commit(self, tx_id: str):
        """Phase 2: Commit decision received from Coordinator."""
        if self.state != ParticipantState.PREPARED:
            print(f"  ⚠️ [{self.name}] Warning: Cannot commit from state {self.state}")
            return

        if self.pending_operation == "DEBIT":
            self.balance -= self.locked_amount
        elif self.pending_operation == "CREDIT":
            self.balance += self.locked_amount

        self.state = ParticipantState.COMMITTED
        self.wal_log.append(f"COMMIT {tx_id}")
        print(f"  └─ [{self.name}] COMMITTED tx {tx_id}. Final Balance: ₹{self.balance:.2f}, Locks Released.")
        self.locked_amount = 0.0
        self.pending_operation = None

    def abort(self, tx_id: str):
        """Phase 2: Abort decision received from Coordinator."""
        self.state = ParticipantState.ABORTED
        self.wal_log.append(f"ABORT {tx_id}")
        print(f"  └─ [{self.name}] ABORTED tx {tx_id}. Locks Released. Balance unchanged: ₹{self.balance:.2f}")
        self.locked_amount = 0.0
        self.pending_operation = None


class Coordinator:
    """Orchestrates Two-Phase Commit across multiple participants."""
    def __init__(self, name: str):
        self.name = name
        self.coordinator_wal: List[str] = []

    def execute_transaction(
        self, tx_id: str, participant_ops: Dict[Participant, tuple]
    ) -> bool:
        """
        Executes 2PC protocol.
        participant_ops format: {participant_obj: (operation_type, amount)}
        """
        print(f"\n--- Coordinator starting 2PC Transaction: {tx_id} ---")
        self.coordinator_wal.append(f"START_2PC {tx_id}")

        # PHASE 1: PREPARE
        print("▶ PHASE 1: PREPARE PHASE")
        votes: Dict[Participant, Vote] = {}
        for participant, (op, amount) in participant_ops.items():
            print(f"Sending PREPARE to {participant.name} for {op} ₹{amount}...")
            vote = participant.prepare(tx_id, op, amount)
            votes[participant] = vote

        # Check prepare responses
        all_yes = all(v == Vote.YES for v in votes.values())

        # PHASE 2: COMMIT OR ABORT
        print("\n▶ PHASE 2: DECISION PHASE")
        if all_yes:
            print("Coordinator Consensus: All participants voted YES. Writing COMMIT to Coordinator WAL.")
            self.coordinator_wal.append(f"COMMIT_DECISION {tx_id}")
            print("Broadcasting COMMIT command to all participants...")
            for participant in participant_ops.keys():
                participant.commit(tx_id)
            return True
        else:
            print("Coordinator Consensus: At least one participant voted NO/Failed. Writing ABORT to Coordinator WAL.")
            self.coordinator_wal.append(f"ABORT_DECISION {tx_id}")
            print("Broadcasting ABORT command to all participants...")
            for participant in participant_ops.keys():
                participant.abort(tx_id)
            return False

    def simulate_coordinator_crash_after_prepare(
        self, tx_id: str, participant_ops: Dict[Participant, tuple]
    ):
        """Simulates Coordinator crash immediately after all participants PREPARE."""
        print(f"\n--- Coordinator starting 2PC Transaction: {tx_id} (FAILS MID-WAY) ---")
        self.coordinator_wal.append(f"START_2PC {tx_id}")

        print("▶ PHASE 1: PREPARE PHASE")
        for participant, (op, amount) in participant_ops.items():
            print(f"Sending PREPARE to {participant.name} for {op} ₹{amount}...")
            participant.prepare(tx_id, op, amount)

        print("\n💥 CRASH! Coordinator node crashed before writing decision to WAL or sending Phase 2 commands!")
        print("\n--- PARTICIPANT INSECURITY & BLOCKING DEMONSTRATION ---")
        for participant in participant_ops.keys():
            print(f"[{participant.name}] Current State: {participant.state.name}")
            print(f"  └─ Problem: Is {participant.name} allowed to commit independently? NO! (Other nodes might have aborted)")
            print(f"  └─ Problem: Is {participant.name} allowed to abort independently? NO! (Other nodes might have committed)")
            print(f"  └─ Result: {participant.name} IS BLOCKED INDEFINITELY HOLDING LOCKS ON ₹{participant.locked_amount:.2f}!")


def run_successful_2pc():
    print("="*70)
    print("DEMO 1: Successful Two-Phase Commit")
    print("="*70)
    p_a = Participant("Participant_A (Bank A)", balance=10000.0)
    p_b = Participant("Participant_B (Bank B)", balance=5000.0)
    coord = Coordinator("Transaction_Coordinator")

    ops = {
        p_a: ("DEBIT", 2000.0),
        p_b: ("CREDIT", 2000.0)
    }

    success = coord.execute_transaction("TX_1001", ops)
    print(f"Transaction Result: {'SUCCESS (Atomic Commit)' if success else 'ABORTED'}")


def run_aborted_2pc():
    print("\n" + "="*70)
    print("DEMO 2: Aborted 2PC (Participant Constraint Failure)")
    print("="*70)
    p_a = Participant("Participant_A (Bank A)", balance=1000.0)  # Only ₹1000 balance!
    p_b = Participant("Participant_B (Bank B)", balance=5000.0)
    coord = Coordinator("Transaction_Coordinator")

    ops = {
        p_a: ("DEBIT", 3000.0),  # Attempting to debit ₹3000 -> Will fail!
        p_b: ("CREDIT", 3000.0)
    }

    success = coord.execute_transaction("TX_1002", ops)
    print(f"Transaction Result: {'SUCCESS' if success else 'ABORTED (Atomic Rollback across all nodes)'}")


def run_blocking_coordinator_crash():
    print("\n" + "="*70)
    print("DEMO 3: 2PC Coordinator Crash (Demonstrating Indecision & Blocking)")
    print("="*70)
    p_a = Participant("Participant_A (Bank A)", balance=10000.0)
    p_b = Participant("Participant_B (Bank B)", balance=5000.0)
    coord = Coordinator("Transaction_Coordinator")

    ops = {
        p_a: ("DEBIT", 2000.0),
        p_b: ("CREDIT", 2000.0)
    }

    coord.simulate_coordinator_crash_after_prepare("TX_1003", ops)


if __name__ == "__main__":
    run_successful_2pc()
    run_aborted_2pc()
    run_blocking_coordinator_crash()
