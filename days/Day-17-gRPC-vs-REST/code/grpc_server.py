#!/usr/bin/env python3
"""
Day 17 — Minimal gRPC Server

Demonstrates gRPC Server Mechanics:
1. Implementing service interface methods defined in Protobuf contract (`user.proto`).
2. Receiving binary-serialized Protobuf request objects from client stubs.
3. Returning strongly-typed Protobuf response messages over HTTP/2 transport framing.
4. Supporting unary RPCs and Server Streaming RPCs.
"""

import time
import sys
from concurrent import futures

# Check if grpc dependencies are installed
try:
    import grpc
    GRPC_AVAILABLE = True
except ImportError:
    GRPC_AVAILABLE = False

# Database mock
USERS_DB = {
    42: {"user_id": 42, "name": "Alice Smith", "email": "alice@example.com", "role": "Site Reliability Engineer"},
    101: {"user_id": 101, "name": "Bob Jones", "email": "bob@example.com", "role": "Backend Developer"},
}

USER_ACTIVITIES = [
    {"timestamp": "2026-08-12T10:00:00Z", "action": "LOGIN_SUCCESS", "ip_address": "192.168.1.50"},
    {"timestamp": "2026-08-12T10:05:22Z", "action": "DEPLOY_SERVICE", "ip_address": "192.168.1.50"},
    {"timestamp": "2026-08-12T10:14:01Z", "action": "UPDATE_CONFIG", "ip_address": "192.168.1.50"},
]

if GRPC_AVAILABLE:
    # Try importing generated stubs (generated via protoc tool)
    try:
        import user_pb2
        import user_pb2_grpc
        STUBS_AVAILABLE = True
    except ImportError:
        STUBS_AVAILABLE = False

    if STUBS_AVAILABLE:
        class UserServiceServicer(user_pb2_grpc.UserServiceServicer):
            """Implementation of the gRPC UserService interface contract."""

            def GetUser(self, request: user_pb2.UserRequest, context: grpc.ServicerContext) -> user_pb2.UserResponse:
                """Unary RPC: Fetches a single user profile."""
                user_id = request.user_id
                print(f"[gRPC Server] Received Unary GetUser RPC request for user_id={user_id}")

                user = USERS_DB.get(user_id)
                if not user:
                    # Set gRPC error status code and details on the context
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details(f"User with ID {user_id} was not found.")
                    return user_pb2.UserResponse()

                # Return strongly-typed Protobuf response
                return user_pb2.UserResponse(
                    user_id=user["user_id"],
                    name=user["name"],
                    email=user["email"],
                    role=user["role"]
                )

            def StreamUserActivity(self, request: user_pb2.UserRequest, context: grpc.ServicerContext):
                """Server Streaming RPC: Yields activity log records sequentially."""
                user_id = request.user_id
                print(f"[gRPC Server] Received Streaming StreamUserActivity RPC request for user_id={user_id}")

                if user_id not in USERS_DB:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details(f"User {user_id} not found.")
                    return

                for act in USER_ACTIVITIES:
                    time.sleep(0.3) # Simulate streaming interval over HTTP/2 data frames
                    yield user_pb2.ActivityLog(
                        timestamp=act["timestamp"],
                        action=act["action"],
                        ip_address=act["ip_address"]
                    )

def run_grpc_server(host="127.0.0.1", port=50051):
    if not GRPC_AVAILABLE or not STUBS_AVAILABLE:
        print("="*60)
        print(" [gRPC Server Notice]")
        print(" grpcio or generated stubs (user_pb2.py) were not found.")
        print(" To generate stubs and run this server natively:")
        print("   1. pip install grpcio grpcio-tools")
        print("   2. python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. user.proto")
        print("   3. python grpc_server.py")
        print("="*60)
        return

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserServiceServicer(), server)
    server.add_insecure_port(f"{host}:{port}")
    server.start()
    print(f"==================================================")
    print(f"  gRPC Server running on {host}:{port} (HTTP/2)    ")
    print(f"==================================================")
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\nStopping gRPC server...")
        server.stop(0)

if __name__ == "__main__":
    run_grpc_server()
