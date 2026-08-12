#!/usr/bin/env python3
"""
Day 17 — Minimal gRPC Client

Demonstrates gRPC Client Mechanics:
1. Connecting to gRPC server using HTTP/2 channel (`grpc.insecure_channel`).
2. Instantiating auto-generated client stub (`user_pb2_grpc.UserServiceStub`).
3. Calling RPC procedures like native Python methods with static request objects.
4. Setting deadlines/timeouts (`timeout=2.0`).
5. Handling gRPC status codes (`grpc.RpcError`).
6. Consuming Server Streaming RPC responses as a standard Python generator.
"""

import sys
import time

try:
    import grpc
    GRPC_AVAILABLE = True
except ImportError:
    GRPC_AVAILABLE = False

if GRPC_AVAILABLE:
    try:
        import user_pb2
        import user_pb2_grpc
        STUBS_AVAILABLE = True
    except ImportError:
        STUBS_AVAILABLE = False

def run_client():
    if not GRPC_AVAILABLE or not STUBS_AVAILABLE:
        print("="*60)
        print(" [gRPC Client Notice]")
        print(" grpcio or generated stubs (user_pb2.py) were not found.")
        print(" To run this client against grpc_server.py:")
        print("   1. pip install grpcio grpcio-tools")
        print("   2. python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. user.proto")
        print("   3. python grpc_server.py (in Terminal 1)")
        print("   4. python grpc_client.py (in Terminal 2)")
        print("="*60)
        return

    # 1. Open persistent HTTP/2 transport channel to gRPC server
    channel_target = "127.0.0.1:50051"
    print(f"\n[gRPC Client] Opening HTTP/2 channel to {channel_target}...")
    
    with grpc.insecure_channel(channel_target) as channel:
        # 2. Instantiate client stub
        stub = user_pb2_grpc.UserServiceStub(channel)

        # ---------------------------------------------------------------------
        # DEMO 1: Successful Unary RPC Invocation
        # ---------------------------------------------------------------------
        print("\n--- Demo 1: Unary GetUser RPC ---")
        try:
            # Construct strongly typed request object
            request = user_pb2.UserRequest(user_id=42)
            print(f"[gRPC Client] Calling stub.GetUser(user_id=42) with 2.0s deadline...")

            # Invoke RPC method over channel (Serialized to Protobuf wire format)
            response = stub.GetUser(request, timeout=2.0)
            
            print(f"[gRPC Client] RPC Response Received!")
            print(f"              ID:    {response.user_id}")
            print(f"              Name:  {response.name}")
            print(f"              Email: {response.email}")
            print(f"              Role:  {response.role}")
        except grpc.RpcError as e:
            print(f"[gRPC Client] RPC Error Failed: Code={e.code()}, Details={e.details()}")

        # ---------------------------------------------------------------------
        # DEMO 2: Error Handling (Querying Missing User)
        # ---------------------------------------------------------------------
        print("\n--- Demo 2: Handling gRPC Error Status (User 999) ---")
        try:
            request = user_pb2.UserRequest(user_id=999)
            print(f"[gRPC Client] Calling stub.GetUser(user_id=999)...")
            response = stub.GetUser(request, timeout=2.0)
        except grpc.RpcError as e:
            print(f"[gRPC Client] Caught expected RPC Error!")
            print(f"              Status Code: {e.code()}")
            print(f"              Error Detail: {e.details()}")

        # ---------------------------------------------------------------------
        # DEMO 3: Server Streaming RPC
        # ---------------------------------------------------------------------
        print("\n--- Demo 3: Server Streaming StreamUserActivity RPC ---")
        try:
            request = user_pb2.UserRequest(user_id=42)
            print(f"[gRPC Client] Subscribing to activity log stream for user_id=42...")
            
            # Returns an iterator over response messages streamed from server over HTTP/2
            stream = stub.StreamUserActivity(request, timeout=5.0)
            
            for activity in stream:
                print(f"[gRPC Stream] Received Log: [{activity.timestamp}] Action: {activity.action} (IP: {activity.ip_address})")
        except grpc.RpcError as e:
            print(f"[gRPC Client] Stream RPC Failed: Code={e.code()}, Details={e.details()}")

if __name__ == "__main__":
    print("==================================================")
    print("           gRPC Client Execution Demo             ")
    print("==================================================")
    run_client()
