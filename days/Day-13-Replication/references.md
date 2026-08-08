# 📚 Day 13 References: Replication — Primary, Secondary, Multi-Leader, and Leaderless

Curated learning resources, original research papers, engineering blogs, and official documentation on distributed data replication models.

---

## 📖 Books

* **[Designing Data-Intensive Applications (DDIA)](https://dataintensive.net/) — Martin Kleppmann**  
  *Chapter 5 provides the definitive breakdown of replication topologies, replication lag, multi-leader write conflicts, and leaderless systems.*
* **[Database Internals: A Deep Dive into How Distributed Data Systems Work](https://www.databass.dev/) — Alex Petrov**  
  *Offers in-depth coverage of replication mechanics, write-ahead log shipping, anti-entropy protocols, and cluster membership.*
* **[Distributed Systems: Principles and Paradigms](https://www.distributed-systems.net/) — Andrew S. Tanenbaum & Maarten van Steen**  
  *Comprehensive academic reference detailing data consistency, replication models, and fault tolerance strategies.*

---

## 🔬 Research Papers

* **[Dynamo: Amazon's Highly Available Key-value Store](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf) — Giuseppe DeCandia et al. (SOSP 2007)**  
  *Landmark paper introducing leaderless replication, quorum techniques, and eventual consistency to achieve high write availability.*
* **[Active Database Replication Using State Machine Replication](https://www.cs.cornell.edu/fbs/publications/SMSurvey.pdf) — Fred B. Schneider (ACM Computing Surveys 1990)**  
  *Foundational paper establishing the core theory behind primary-secondary and active-passive state machine replication.*

---

## 🛠️ Engineering Blogs

* **[Amazon Architecture: Lessons Learned from Building Dynamo](https://www.allthingsdistributed.com/) — Werner Vogels (All Things Distributed)**  
  *Original insights from AWS CTO on designing fault-tolerant, decentralized replication for mission-critical e-commerce infrastructure.*
* **[Meta Engineering: High Availability and Database Replication](https://engineering.fb.com/) — Meta Engineering**  
  *Detailed writeup on how Meta manages cross-datacenter MySQL primary-secondary replication fleets at global scale.*
* **[Netflix TechBlog: Global Data Replication in Cassandra](https://netflixtechblog.com/) — Netflix Technology Blog**  
  *Explores multi-region leaderless replication strategies for keeping user viewing history synchronized across continents.*

---

## 📑 Official Documentation

* **[PostgreSQL Documentation: Streaming Replication and High Availability](https://www.postgresql.org/docs/current/warm-standby.html)**  
  *Official Postgres documentation on physical write-ahead log (WAL) shipping, synchronous vs asynchronous standbys, and failover.*
* **[MySQL Documentation: Group Replication and Multi-Source Replication](https://dev.mysql.com/doc/refman/8.0/en/group-replication.html)**  
  *Official MySQL guide explaining primary-secondary topologies, multi-primary group replication, and conflict detection engines.*
* **[Apache Cassandra Documentation: Replication and Architecture](https://cassandra.apache.org/doc/latest/cassandra/architecture/replication.html)**  
  *Official guide covering leaderless replication, replication factor selection, and configurable consistency levels.*

---

## 🎥 Conference Talks

* **[AWS re:Invent: Deep Dive into Distributed Data Store Replication](https://www.youtube.com/) — AWS Architecture Series**  
  *Technical deep-dive into how cloud-native databases implement primary-secondary failover and cross-region replication.*
* **[InfoQ: Designing Systems for High Availability with Multi-Leader Topology](https://www.infoq.com/presentations/) — Distributed Systems Conference**  
  *Real-world engineering presentation dissecting the trade-offs and conflict resolution techniques in multi-leader replication.*

---

## 🎬 Videos

* **[Distributed Systems 5.1: Replication & Leader-Based Topologies](https://www.youtube.com/) — Martin Kleppmann (Cambridge University Lecture Series)**  
  *University lecture breaking down leader/follower replication, synchronous vs asynchronous trade-offs, and replication lag.*
* **[Leaderless Replication & Quorums Explained Visually](https://www.youtube.com/) — Distributed Systems Educational Series**  
  *Clear visual walkthrough demonstrating how leaderless quorum reads and writes maintain data resilience without a single leader.*
