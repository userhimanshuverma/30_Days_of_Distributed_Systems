# Day 17 — References & Further Reading: REST vs gRPC

This document contains curated, authoritative primary sources, foundational research papers, production engineering articles, and official specifications for **REST and gRPC**.

---

## 📚 Books

* **Architectural Styles and the Design of Network-based Software Architectures**
  * **Source**: Roy Thomas Fielding (Ph.D. Dissertation, University of California, Irvine, 2000)
  * **Link**: [https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm)
  * **Why it is useful**: The foundational dissertation that defined REST (Representational State Transfer) as an architectural style for network-based applications.

* **Designing Data-Intensive Applications**
  * **Source**: Martin Kleppmann (O'Reilly Media, Chapter 4: Modes of Data Flow)
  * **Link**: [https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/)
  * **Why it is useful**: Provides an exceptional breakdown of REST vs RPC, schema evolution, Protobuf binary encoding, and network transparency trade-offs.

---

## 📄 Research Papers

* **A Note on Distributed Computing (1994)**
  * **Source**: Sun Microsystems Laboratories — Jim Waldo, Geoff Wyant, Ann Wollrath, & Samuel Kendall
  * **Link**: [https://scholar.harvard.edu/waldo/publications/note-distributed-computing](https://scholar.harvard.edu/waldo/publications/note-distributed-computing)
  * **Why it is useful**: The classic paper explaining why attempting to hide the network behind local call abstractions causes system failure.

* **Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content (RFC 7231)**
  * **Source**: Internet Engineering Task Force (IETF) — R. Fielding & J. Reschke
  * **Link**: [https://datatracker.ietf.org/doc/html/rfc7231](https://datatracker.ietf.org/doc/html/rfc7231)
  * **Why it is useful**: The authoritative RFC specification for HTTP methods, headers, status codes, and safe/idempotent semantics.

* **Hypertext Transfer Protocol Version 2 (HTTP/2) (RFC 7540)**
  * **Source**: Internet Engineering Task Force (IETF) — M. Belshe, R. Peon, & M. Thomson
  * **Link**: [https://datatracker.ietf.org/doc/html/rfc7540](https://datatracker.ietf.org/doc/html/rfc7540)
  * **Why it is useful**: The standard specifying binary framing, stream multiplexing, header compression (HPACK), and server push that power gRPC transport.

---

## 🛠️ Engineering Blogs

* **gRPC at Google: Official Overview & Architecture**
  * **Source**: Google Cloud Engineering Blog
  * **Link**: [https://cloud.google.com/blog/products/g-suite/grpc-a-high-performance-open-source-universal-rpc-framework](https://cloud.google.com/blog/products/g-suite/grpc-a-high-performance-open-source-universal-rpc-framework)
  * **Why it is useful**: Explains how Google evolved internal Stubby RPC infrastructure into open-source gRPC for massive internal microservice ecosystems.

* **REST vs gRPC: How to Choose the Right API Architecture**
  * **Source**: AWS Architecture Blog
  * **Link**: [https://aws.amazon.com/compare/the-difference-between-grpc-and-rest/](https://aws.amazon.com/compare/the-difference-between-grpc-and-rest/)
  * **Why it is useful**: Practical architectural comparison outlining operational scenarios, performance trade-offs, and browser compatibility limits.

---

## 📖 Official Documentation

* **gRPC Core Concepts and Documentation**
  * **Source**: Cloud Native Computing Foundation (CNCF) / gRPC Project
  * **Link**: [https://grpc.io/docs/guides/](https://grpc.io/docs/guides/)
  * **Why it is useful**: The primary reference for gRPC service definitions, stubs, channel lifecycle, streaming types, and deadline propagation.

* **Protocol Buffers Language Guide (proto3)**
  * **Source**: Google Developer Documentation
  * **Link**: [https://protobuf.dev/programming-guides/proto3/](https://protobuf.dev/programming-guides/proto3/)
  * **Why it is useful**: Official specification for defining strongly-typed Protobuf contracts, field numbers, binary wire formats, and backward compatibility rules.

---

## 🎥 Conference Talks

* **gRPC Core Concepts and Best Practices**
  * **Source**: Google Tech Talks / CNCF — Varun Talwar & Louis Ryan
  * **Link**: [https://www.youtube.com/watch?v=sGtrna30zF4](https://www.youtube.com/watch?v=sGtrna30zF4)
  * **Why it is useful**: Detailed explanation of HTTP/2 multiplexing, deadlining, load balancing, and internal RPC design patterns.

---

## 📹 Videos

* **REST vs gRPC: Which API Style Should You Choose?**
  * **Source**: ByteByteGo (Alex Xu)
  * **Link**: [https://www.youtube.com/watch?v=4Hex-S-9GgE](https://www.youtube.com/watch?v=4Hex-S-9GgE)
  * **Why it is useful**: Clear visual breakdown of payload sizes, serialization speeds, multiplexing, and public vs internal service decision trees.
