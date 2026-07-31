"""
partition_simulation.py - Simple Network Partition Simulation

Demonstrates how two distributed server nodes behave during normal network operation
and during a network partition (communication failure between servers).
"""

class ServerNode:
    def __init__(self, name: str):
        self.name = name
        self.data_store = {"account_balance": 100}

    def write(self, key: str, value: int):
        self.data_store[key] = value

    def read(self, key: str):
        return self.data_store.get(key, None)


class NetworkEnvironment:
    def __init__(self, node_a: ServerNode, node_b: ServerNode):
        self.node_a = node_a
        self.node_b = node_b
        self.is_partitioned = False

    def simulate_partition(self):
        """Simulate a network fiber cut between Node A and Node B."""
        self.is_partitioned = True
        print("\n[NETWORK FAILURE] Fiber cable severed! Node A and Node B can no longer communicate.")

    def heal_partition(self):
        """Restore network connectivity between Node A and Node B."""
        self.is_partitioned = False
        print("\n[NETWORK RESTORED] Connection re-established between Node A and Node B.")

    def sync_nodes(self, source: ServerNode, target: ServerNode, key: str) -> bool:
        """Attempt to synchronize data between nodes."""
        if self.is_partitioned:
            print(f"[SYNC FAILED] Cannot sync from {source.name} to {target.name} due to network partition!")
            return False
        
        target.write(key, source.read(key))
        print(f"[SYNC SUCCESS] {source.name} synced '{key}' = {source.read(key)} to {target.name}")
        return True


def run_simulation():
    print("=" * 70)
    print("      DAY 5: SIMULATING A NETWORK PARTITION BETWEEN TWO SERVERS")
    print("=" * 70)

    # Initialize nodes and network
    node_a = ServerNode("Server-A (East US)")
    node_b = ServerNode("Server-B (West US)")
    net = NetworkEnvironment(node_a, node_b)

    print(f"\n1. Normal State:")
    print(f"   {node_a.name} balance: ${node_a.read('account_balance')}")
    print(f"   {node_b.name} balance: ${node_b.read('account_balance')}")

    # Normal sync operation
    print("\n2. User updates balance on Server-A to $150:")
    node_a.write("account_balance", 150)
    net.sync_nodes(node_a, node_b, "account_balance")

    print(f"   {node_a.name} balance: ${node_a.read('account_balance')}")
    print(f"   {node_b.name} balance: ${node_b.read('account_balance')}")

    # Trigger Network Partition
    net.simulate_partition()

    # User attempts write during partition
    print("\n3. User updates balance on Server-A to $200 while network is partitioned:")
    node_a.write("account_balance", 200)
    sync_ok = net.sync_nodes(node_a, node_b, "account_balance")

    print("\n4. Current System State during Partition:")
    print(f"   {node_a.name} sees balance: ${node_a.read('account_balance')} (Updated)")
    print(f"   {node_b.name} sees balance: ${node_b.read('account_balance')} (Stale/Old!)")

    if not sync_ok:
        print("\n[OBSERVATION] Server-A and Server-B now hold conflicting data!")
        print("   If a customer queries Server-B, they see $150.")
        print("   If a customer queries Server-A, they see $200.")
        print("   This is the core problem of distributed communication failures.")

    # Heal network
    net.heal_partition()
    net.sync_nodes(node_a, node_b, "account_balance")
    print(f"\n5. Final State after Network Healing:")
    print(f"   {node_a.name} balance: ${node_a.read('account_balance')}")
    print(f"   {node_b.name} balance: ${node_b.read('account_balance')}")
    print("=" * 70)


if __name__ == "__main__":
    run_simulation()
