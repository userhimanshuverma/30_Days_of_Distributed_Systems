"""
Day 4: Why Copying Data Creates Bigger Problems
Demo 2: Consistency Simulation - Observing Data Drift & Synchronization

This script simulates a record update ("School Notice Board" scenario) across
3 distributed nodes (Notice Board 1, Notice Board 2, Notice Board 3).
It illustrates how read operations performed during the propagation window
return inconsistent states across nodes until background synchronization completes.
"""

import time


class NoticeBoardNode:
    """Represents a single server node holding a copy of the notice board announcement."""

    def __init__(self, node_id: str, board_location: str):
        self.node_id = node_id
        self.location = board_location
        # Initial state: Exam starts at 09:00 AM on all boards
        self.announcement = "Math Exam: Friday 09:00 AM"
        self.version = 1

    def read_announcement(self) -> dict:
        """Simulates a student reading from this notice board."""
        return {
            "node_id": self.node_id,
            "location": self.location,
            "announcement": self.announcement,
            "version": self.version,
        }

    def write_announcement(self, text: str, version: int):
        """Updates the announcement on this specific notice board."""
        self.announcement = text
        self.version = version


class NoticeBoardCluster:
    """Simulates a distributed system holding 3 notice board replicas."""

    def __init__(self):
        self.nodes = [
            NoticeBoardNode("Node-1", "Main Hallway"),
            NoticeBoardNode("Node-2", "Library Entrance"),
            NoticeBoardNode("Node-3", "Science Building"),
        ]

    def print_cluster_state(self, step_title: str):
        """Helper to print current state across all nodes."""
        print(f"\n--- {step_title} ---")
        print(f"{'Node ID':<10} | {'Location':<18} | {'Version':<8} | {'Announcement'}")
        print("-" * 70)
        for node in self.nodes:
            state = node.read_announcement()
            print(
                f"{state['node_id']:<10} | {state['location']:<18} | v{state['version']:<7} | '{state['announcement']}'"
            )

    def publish_update(self, new_text: str, new_version: int):
        """Simulates the principal updating the exam schedule."""
        print(f"\n[PRINCIPAL ACTION] Update exam schedule to '{new_text}' (v{new_version})")

        # Step 1: Update Node-1 immediately
        print(" -> Updating Node-1 (Main Hallway) first...")
        self.nodes[0].write_announcement(new_text, new_version)

        # Step 2: Show immediate inconsistency
        self.print_cluster_state("STATE IMMEDIATELY AFTER INITIAL UPDATE (TEMPORARY DISAGREEMENT)")

        print("\n[STUDENT READS] STUDENTS READING NOTICE BOARDS RIGHT NOW:")
        student_a = self.nodes[0].read_announcement()
        student_b = self.nodes[1].read_announcement()
        student_c = self.nodes[2].read_announcement()

        print(f"   Student A (reading at {student_a['location']}): '{student_a['announcement']}'")
        print(f"   Student B (reading at {student_b['location']}): '{student_b['announcement']}'")
        print(f"   Student C (reading at {student_c['location']}): '{student_c['announcement']}'")

        if student_a["announcement"] != student_b["announcement"]:
            print("\n[INCONSISTENCY DETECTED] Student A and Student B have DIFFERENT schedules!")
            print("   Both students are acting on correct information according to the board they checked.")

        # Step 3: Propagation delay (Node-2 gets updated)
        time.sleep(1)
        print("\n -> Syncing Node-2 (Library Entrance)...")
        self.nodes[1].write_announcement(new_text, new_version)
        self.print_cluster_state("STATE AFTER NODE-2 SYNC")

        # Step 4: Final propagation (Node-3 gets updated)
        time.sleep(1)
        print("\n -> Syncing Node-3 (Science Building)...")
        self.nodes[2].write_announcement(new_text, new_version)
        self.print_cluster_state("STATE AFTER ALL NODES SYNCED (CONSISTENT STATE)")


def main():
    print("==========================================================")
    print("   DAY 4 DEMO: CONSISTENCY & DATA DRIFT SIMULATION")
    print("==========================================================")

    cluster = NoticeBoardCluster()
    cluster.print_cluster_state("INITIAL STATE (ALL COPIES MATCH v1)")

    # Perform an update
    cluster.publish_update("Math Exam: Rescheduled to Friday 11:00 AM", 2)

    print("\n[CONCLUSION]")
    print("   Replication created 3 boards for availability.")
    print("   Consistency ensures all 3 boards agree on the exam time.")
    print("   Making copies is easy. Keeping them synchronized is the real challenge.")
    print("==========================================================")


if __name__ == "__main__":
    main()
