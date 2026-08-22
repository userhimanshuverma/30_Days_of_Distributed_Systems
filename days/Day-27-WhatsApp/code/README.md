# Day 27 — Messaging System Simulation Code

This directory contains lightweight, dependency-free Python code simulating the core architecture of a large-scale real-time messaging system (such as WhatsApp).

---

## 📁 Included Modules

1. **[`message_store.py`](file:///d:/30_Days_of_Distributed_Systems/days/Day-27-WhatsApp/code/message_store.py)**
   - Defines the `Message` data structure and the `MessageStatus` lifecycle states (`SENT_TO_SERVER`, `DELIVERED`, `READ`).
   - Implements `OfflineMessageStore`, simulating temporary message persistence for offline recipients.

2. **[`client.py`](file:///d:/30_Days_of_Distributed_Systems/days/Day-27-WhatsApp/code/client.py)**
   - Simulates a mobile client device (`UserClient`).
   - Handles connecting/disconnecting long-lived socket connections, submitting messages, receiving pushed messages, and dispatching `DELIVERED` and `READ` acknowledgements.

3. **[`server.py`](file:///d:/30_Days_of_Distributed_Systems/days/Day-27-WhatsApp/code/server.py)**
   - Simulates a messaging gateway server maintaining the user routing table (`active_connections`).
   - Routes incoming messages directly to online recipient clients or hands them off to `OfflineMessageStore` when recipients are offline.
   - Flushes offline queues automatically upon recipient reconnection and propagates status ACKs back to senders.

4. **[`demo.py`](file:///d:/30_Days_of_Distributed_Systems/days/Day-27-WhatsApp/code/demo.py)**
   - End-to-end executable simulation driving both online delivery and offline store-and-forward scenarios.

---

## 🚀 How to Run

Execute the simulation directly using standard Python 3:

```bash
python demo.py
```

### Expected Output Highlights

- **Scenario 1 (Online Delivery)**: Demonstrates instant push delivery when recipient is online, accompanied by synchronous server ACK (`SENT_TO_SERVER`), recipient delivery ACK (`DELIVERED`), and recipient read ACK (`READ`).
- **Scenario 2 (Offline Delivery)**: Demonstrates that when Charlie is offline, Alice's message is accepted immediately by infrastructure (`SENT_TO_SERVER`), stored safely in `OfflineMessageStore`, and pushed automatically the instant Charlie reconnects to the network.
