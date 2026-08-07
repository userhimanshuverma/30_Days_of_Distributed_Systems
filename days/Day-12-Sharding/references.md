# 📚 Day 12 References: Sharding — How Instagram Stores Billions of Photos

Curated learning resources, original engineering blogs, and foundational documentation on database sharding and horizontal data partitioning.

---

## 📖 Books

* **[Designing Data-Intensive Applications (DDIA)](https://dataintensive.net/) — Martin Kleppmann**  
  *Chapter 6 provides the definitive foundation on partitioning, sharding architectures, and skew management.*
* **[Site Reliability Engineering: How Google Runs Production Systems](https://sre.google/sre-book/table-of-contents/) — Betsy Beyer et al. (Google SRE Book)**  
  *Explores horizontal scaling, storage partitioning, and managing massive-scale datastores reliably.*
* **[Database Internals: A Deep Dive into How Distributed Data Systems Work](https://www.databass.dev/) — Alex Petrov**  
  *Detailed technical breakdown of storage engines, distributed data organization, and partitioning primitives.*

---

## 🔬 Research Papers

* **[F1: A Distributed SQL Database That Scales](https://research.google/pubs/pub41344/) — Google Inc. (VLDB 2013)**  
  *Google's paper explaining how massive relational data is partitioned and processed horizontally across distributed clusters.*
* **[Dynamo: Amazon’s Highly Available Key-value Store](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf) — Giuseppe DeCandia et al. (SOSP 2007)**  
  *The landmark paper detailing data partitioning across autonomous storage nodes to scale key-value workloads.*

---

## 🛠️ Engineering Blogs

* **[Sharding IDs at Instagram](https://instagram-engineering.com/sharding-ids-at-instagram-59b71e10beb8) — Instagram Engineering Blog**  
  *Original post explaining how Instagram sharded PostgreSQL across multiple database servers to support billions of photos.*
* **[Meta Engineering: Scaling Infrastructure and Storage](https://engineering.fb.com/) — Meta Engineering**  
  *In-depth technical writeups detailing how Meta scales database fleets to handle globally distributed social graph data.*
* **[Amazon Builders' Library: Workload Partitioning and Sharding](https://aws.amazon.com/builders-library/) — AWS Engineering**  
  *Architectural patterns for splitting database workloads across multiple nodes to eliminate single-point scaling bottlenecks.*

---

## 📑 Official Documentation

* **[PostgreSQL Documentation: Table Partitioning and Scale-out Concepts](https://www.postgresql.org/docs/current/ddl-partitioning.html)**  
  *Official Postgres documentation on dividing physical tables into logical sub-tables and multi-node architectures.*
* **[MySQL Documentation: InnoDB Partitioning and Sharding Guidance](https://dev.mysql.com/doc/refman/8.0/en/partitioning.html)**  
  *Detailed guide covering table partitioning methods and multi-database horizontal scaling practices in MySQL.*

---

## 🎥 Conference Talks & Videos

* **[InfoQ Architecture Talks: Lessons from Sharding Massive Databases](https://www.infoq.com/architecture-design/presentations/) — InfoQ Architecture**  
  *Real-world engineering presentations sharing practical experiences and pitfalls when transitioning from single DB to sharded fleets.*
* **[System Design Primer: Database Sharding & Partitioning Strategies](https://www.youtube.com/) — Distributed Systems Educational Series**  
  *Visual video breakdown explaining horizontal data partitioning, request routing, and capacity planning for backend engineers.*
