"""
user_router.py
--------------
An educational Python router demonstrating how user data requests (reads and writes)
are directed to independent database shards based on a deterministic routing rule.

Key Concept:
    Instead of sending all requests to a single central database, the router calculates 
    which database shard holds a given record (e.g., using `user_id % total_shards`)
    and dispatches the operation directly to that database instance.
"""

from typing import Dict, Any, Optional, List


class UserRouter:
    """
    Simulates an application-level router or database gateway that directs
    read and write requests across multiple independent database shards.
    """

    def __init__(self, shards: List[Dict[int, Dict[str, Any]]]):
        """
        Initialize the router with a reference to all available database shards.
        
        :param shards: A list of dictionary objects, where each dictionary 
                       represents an independent database shard storing user records.
        """
        self.shards = shards
        self.num_shards = len(shards)

    def get_shard_index(self, user_id: int) -> int:
        """
        Determines the target shard index for a given user ID.
        
        Using a simple modulo rule: user_id % num_shards.
        This ensures that a given user ID will always map to the exact same shard.
        
        :param user_id: The unique integer ID of the user.
        :return: The index of the shard assigned to hold this user's data.
        """
        return user_id % self.num_shards

    def write_user(self, user_id: int, name: str, email: str, photo_count: int = 0) -> int:
        """
        Routes a user creation or update request to the appropriate database shard.
        
        :param user_id: Unique user identifier.
        :param name: User's display name.
        :param email: User's email address.
        :param photo_count: Initial photo count.
        :return: The target shard index where the record was saved.
        """
        # Step 1: Calculate which shard should store this user's data
        shard_idx = self.get_shard_index(user_id)
        
        # Step 2: Access the targeted independent database shard
        target_shard = self.shards[shard_idx]
        
        # Step 3: Write the user payload directly into that shard
        target_shard[user_id] = {
            "user_id": user_id,
            "name": name,
            "email": email,
            "photo_count": photo_count
        }
        
        return shard_idx

    def read_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Routes a user read request directly to the shard containing the user's data.
        
        :param user_id: Unique user identifier.
        :return: The user record dictionary if found, or None if not present.
        """
        # Step 1: Calculate which shard holds this user's data
        shard_idx = self.get_shard_index(user_id)
        
        # Step 2: Look up the record inside that specific shard
        target_shard = self.shards[shard_idx]
        return target_shard.get(user_id)
