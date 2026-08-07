"""
simple_sharding_demo.py
-----------------------
Educational simulation showing how data is distributed across multiple
independent database shards rather than stored on a single monolithic database server.

Mental Model:
    - 4 Python dictionaries represent 4 separate database servers (Shard 0 to Shard 3).
    - A UserRouter uses a deterministic modulo rule (user_id % total_shards) to decide
      which shard receives reads and writes.
    - No single shard holds the full dataset; workload and storage are divided.
"""

from user_router import UserRouter


def main():
    print("=" * 70)
    print("DAY 12 SIMULATION: SHARDING BILLIONS OF USER RECORDS")
    print("=" * 70)
    print("Mental Model: 1 database stores everything -> Sharded DB shares the work.")
    print("-" * 70)

    # Step 1: Create 4 independent database shards.
    # In a real system, these would be 4 separate PostgreSQL/MySQL server instances.
    NUM_SHARDS = 4
    db_shards = [{} for _ in range(NUM_SHARDS)]

    print(f"\n[SYSTEM SETUP] Initialized {NUM_SHARDS} independent database shards:")
    for idx in range(NUM_SHARDS):
        print(f"  * Database Shard {idx}: Ready (0 records)")

    # Step 2: Initialize the application user router
    router = UserRouter(db_shards)

    # Step 3: Simulate creating users (Instagram photo uploads and profiles)
    sample_users = [
        (1001, "Alice", "alice@example.com", 142),
        (1002, "Bob", "bob@example.com", 89),
        (1003, "Charlie", "charlie@example.com", 310),
        (1004, "Diana", "diana@example.com", 56),
        (1005, "Eve", "eve@example.com", 215),
        (1006, "Frank", "frank@example.com", 18),
        (1007, "Grace", "grace@example.com", 430),
        (1008, "Heidi", "heidi@example.com", 94),
    ]

    print("\n" + "=" * 70)
    print("WRITE OPERATIONS: ROUTING NEW USER REGISTRATIONS")
    print("=" * 70)

    for user_id, name, email, photos in sample_users:
        # Route write request
        assigned_shard = router.write_user(user_id, name, email, photos)
        print(f"User ID {user_id:4d} ({name:7s}) -> Routed to [Shard {assigned_shard}] via rule ({user_id} % {NUM_SHARDS} = {assigned_shard})")

    # Step 4: Display the storage state across all independent database shards
    print("\n" + "=" * 70)
    print("DATABASE SHARD STORAGE INSPECTION")
    print("=" * 70)

    for idx, shard in enumerate(db_shards):
        print(f"\nDatabase Shard {idx} (Contains {len(shard)} user records):")
        for u_id, record in shard.items():
            print(f"    - Record [User ID {u_id}]: {record['name']} | Email: {record['email']} | Photos: {record['photo_count']}")

    # Step 5: Simulate read operations
    print("\n" + "=" * 70)
    print("READ OPERATIONS: DIRECT QUERY ROUTING")
    print("=" * 70)

    query_user_ids = [1003, 1007, 1002]

    for q_id in query_user_ids:
        # Calculate target shard directly without scanning all databases
        target_shard_idx = router.get_shard_index(q_id)
        user_data = router.read_user(q_id)
        
        print(f"Querying Profile for User ID {q_id}:")
        print(f"  1. Router maps User ID {q_id} directly to Shard {target_shard_idx}")
        print(f"  2. Fetching from Shard {target_shard_idx}... Result: {user_data['name']} ({user_data['photo_count']} photos uploaded)")
        print(f"  3. Note: Shards 0, 1, 2 were NEVER queried for this request!\n")

    print("=" * 70)
    print("KEY LESSON:")
    print("Each database shard only handles a fraction of total storage and queries.")
    print("By adding more shards, system storage and throughput capacity scale horizontally.")
    print("=" * 70)


if __name__ == "__main__":
    main()
