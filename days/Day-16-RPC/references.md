# Day 16 — References & Further Reading: Remote Procedure Call (RPC)

This document contains curated, authoritative primary sources, foundational research papers, production engineering articles, and academic lectures on **Remote Procedure Call (RPC)** and network boundaries.

---

## 📚 Books

* **Designing Data-Intensive Applications**
  * **Source**: O'Reilly Media (Chapter 4: Modes of Data Flow)
  * **Link**: [https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/)
  * **Why it matters**: Martin Kleppmann delivers an unmatched analysis of RPC design trade-offs, network transparency illusions, schema evolution, and binary serialization overhead.

* **Distributed Systems: Principles and Paradigms**
  * **Source**: Andrew S. Tanenbaum & Maarten Van Steen
  * **Link**: [https://www.distributed-systems.net/](https://www.distributed-systems.net/)
  * **Why it matters**: Provides foundational academic explanations of client/server stub generation, parameter marshaling, and RPC transport binding.

---

## 📄 Research Papers

* **Implementing Remote Procedure Calls (1984)**
  * **Source**: ACM Transactions on Computer Systems (TOCS) — Andrew D. Birrell & Bruce Jay Nelson
  * **Link**: [https://dl.acm.org/doi/10.1145/2080.2081](https://dl.acm.org/doi/10.1145/2080.2081)
  * **Why it matters**: The landmark paper that introduced practical RPC architecture, defining stubs, binding routines, and network transmission lifecycles.

* **A Note on Distributed Computing (1994)**
  * **Source**: Sun Microsystems Laboratories — Jim Waldo, Geoff Wyant, Ann Wollrath, & Samuel Kendall
  * **Link**: [https://scholar.harvard.edu/waldo/publications/note-distributed-computing](https://scholar.harvard.edu/waldo/publications/note-distributed-computing)
  * **Why it matters**: The seminal paper proving why unified local/remote object abstractions fail and why network latency, memory separation, and partial failure cannot be hidden.

---

## 🛠️ Engineering Blogs

* **gRPC at Google: Official Overview & Architecture**
  * **Source**: Google Cloud Engineering Blog
  * **Link**: [https://cloud.google.com/blog/products/g-suite/grpc-a-high-performance-open-source-universal-rpc-framework](https://cloud.google.com/blog/products/g-suite/grpc-a-high-performance-open-source-universal-rpc-framework)
  * **Why it matters**: Explains how Google evolved internal Stubby infrastructure into the modern, open-source gRPC framework for high-throughput microservices.

* **Idempotency Keys in Financial APIs**
  * **Source**: Stripe Engineering Blog
  * **Link**: [https://stripe.com/blog/idempotency](https://stripe.com/blog/idempotency)
  * **Why it matters**: Demonstrates real-world patterns for handling lost network responses, retries, and preventing duplicate operations in production RPC APIs.

---

## 📖 Official Documentation

* **gRPC Documentation & Core Guides**
  * **Source**: Cloud Native Computing Foundation (CNCF) / gRPC Project
  * **Link**: [https://grpc.io/docs/guides/](https://grpc.io/docs/guides/)
  * **Why it matters**: The primary technical reference for production RPC interfaces, context deadlines, protocol buffers, and HTTP/2 transport framing.

* **Protocol Buffers Language Guide (proto3)**
  * **Source**: Google Open Source Documentation
  * **Link**: [https://protobuf.dev/programming-guides/proto3/](https://protobuf.dev/programming-guides/proto3/)
  * **Why it matters**: Authoritative specification for defining strongly typed RPC contracts, compact binary encoding, and forward/backward schema compatibility.

---

## 🎥 Conference Talks

* **gRPC Core Concepts and Best Practices**
  * **Source**: Google Tech Talks / CNCF — Varun Talwar & Louis Ryan
  * **Link**: [https://www.youtube.com/watch?v=sGtrna30zF4](https://www.youtube.com/watch?v=sGtrna30zF4)
  * **Why it matters**: Deep dive into production RPC mechanics, multiplexing, deadlining propagation, and load balancing across service meshes.

---

## 📹 Videos

* **MIT 6.824: Distributed Systems — Lecture 2: Infrastructure: RPC and Threads**
  * **Source**: MIT OpenCourseWare — Prof. Robert Morris
  * **Link**: [https://www.youtube.com/watch?v=gA4yxUYX7tA](https://www.youtube.com/watch?v=gA4yxUYX7tA)
  * **Why it matters**: Comprehensive university lecture analyzing RPC semantics, failure handling, duplicate filtering, and concurrency safety.
