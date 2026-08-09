# 📚 Day 14 References: Quorums — Why 2 of 3 Votes Matter

Curated learning resources, foundational research papers, engineering blogs, and official documentation on quorum replication, data overlap models, and consistency trade-offs.

---

## 📖 Books

* **[Designing Data-Intensive Applications (DDIA)](https://dataintensive.net/) — Martin Kleppmann**  
  *Chapter 5 ("Replication: Leaderless Replication") provides the definitive explanation of quorum reads/writes, $W + R > N$ intersection rules, and sloppy quorums.*
* **[Database Internals: A Deep Dive into How Distributed Data Systems Work](https://www.databass.dev/) — Alex Petrov**  
  *Chapter 10 details quorum replication algorithms, read repair mechanisms, anti-entropy protocols, and coordinator node operations.*
* **[Distributed Systems: Principles and Paradigms](https://www.distributed-systems.net/) — Andrew S. Tanenbaum & Maarten van Steen**  
  *Provides fundamental theoretical background on weighted quorum voting schemes, consistency models, and fault recovery limits.*

---

## 🔬 Research Papers

* **[Dynamo: Amazon's Highly Available Key-value Store](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf) — Giuseppe DeCandia et al. (SOSP 2007)**  
  *The landmark paper that popularized leaderless quorum replication ($N, W, R$), hinted handoff, and read repair in commercial cloud storage.*
* **[Weighted Voting for Replicated Data](https://dl.acm.org/doi/10.1145/800215.806583) — David K. Gifford (SOSP 1979)**  
  *The seminal paper establishing the mathematical foundation of read and write quorums ($W + R > N$) for maintaining serializability across replicas.*
* **[Paxos Made Simple](https://lamport.azurewebsites.net/pubs/paxos-simple.pdf) — Leslie Lamport (2001)**  
  *Explains how majority quorums are used to achieve consensus and resolve competing proposals without a single point of failure.*

---

## 🛠️ Engineering Blogs

* **[Amazon DynamoDB Architecture: How DynamoDB Achieves High Availability](https://aws.amazon.com/blogs/aws/) — AWS Architecture Blog**  
  *Explores how AWS uses Paxos and quorum replication across availability zones to guarantee single-digit millisecond latency and durability.*
* **[Cassandra Architecture: How Quorums Ensure Consistency](https://www.datastax.com/blog)**  
  *Explains how Apache Cassandra implements configurable read and write consistency levels (`LOCAL_QUORUM`, `QUORUM`, `ALL`) across multi-datacenter clusters.*
* **[Riak KV: Understanding Quorum and Consistency Levels](https://basho.com/) — Basho Engineering (Riak)**  
  *Detailed technical writeup on leaderless quorum tuning, sloppy quorums, and handling network partitions in production.*

---

## 📑 Official Documentation

* **[Apache Cassandra Documentation: Configurable Data Consistency](https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html)**  
  *Official documentation explaining Cassandra's leaderless architecture, quorum math, read repair, and active anti-entropy.*
* **[AWS DynamoDB Developer Guide: Read Consistency Models](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html)**  
  *Official guide contrasting eventual consistency reads versus strongly consistent quorum reads.*
* **[CockroachDB Documentation: Quorum Commit and Multi-Raft Groups](https://www.cockroachlabs.com/docs/stable/architecture/replication-layer.html)**  
  *Official reference on how CockroachDB combines Raft consensus groups with majority quorum writes for distributed transactions.*

---

## 🎥 Conference Talks

* **[AWS re:Invent: Deep Dive into Amazon DynamoDB Architecture](https://www.youtube.com/) — AWS Architecture Series**  
  *Technical breakdown of how storage nodes handle leaderless quorum writes, heartbeats, and storage node failovers in real time.*
* **[QCon: Quorums, Consistency, and Eventual Convergence in Distributed Storage](https://www.infoq.com/presentations/) — Distributed Systems Conference**  
  *Engineering presentation comparing strict quorums vs. relaxed/sloppy quorums in high-throughput database systems.*

---

## 🎬 Videos

* **[Distributed Systems 5.2: Leaderless Replication & Quorums](https://www.youtube.com/) — Martin Kleppmann (Cambridge University)**  
  *Visual university lecture detailing the mechanics of read and write quorums, stale read vulnerabilities, and quorum intersection math.*
* **[Why 2 of 3 Votes Matter: Quorum Voting Explained](https://www.youtube.com/) — Distributed Systems Educational Series**  
  *Step-by-step visual animation demonstrating why majority voting prevents split-brain and maintains availability during node crashes.*
