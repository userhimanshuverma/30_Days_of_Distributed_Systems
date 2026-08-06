# 📚 Day 11 References: Why Databases Can't Live on One Machine

Curated learning resources and foundational reading for understanding single-database limits and the necessity of scaling data storage.

---

## 📖 Books

* **[Designing Data-Intensive Applications (DDIA)](https://dataintensive.net/) — Martin Kleppmann**  
  *The definitive guide to understanding data storage architectures, scaling trade-offs, and why single-node storage engines reach physical limits.*
* **[Site Reliability Engineering: How Google Runs Production Systems](https://sre.google/sre-book/table-of-contents/) — Betsy Beyer et al. (Google SRE Book)**  
  *Explores operational bottlenecks, resource limits, and capacity planning when scaling datastores in large distributed environments.*
* **[Database Internals: A Deep Dive into How Distributed Data Systems Work](https://www.databass.dev/) — Alex Petrov**  
  *Covers disk structures, thread concurrency models, and storage engine bottlenecks that bound single-node database performance.*

---

## 🔬 Research Papers

* **[Dynamo: Amazon’s Highly Available Key-value Store](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf) — Giuseppe DeCandia et al. (SOSP 2007)**  
  *Amazon's landmark paper documenting why standard centralized databases could not sustain Black Friday traffic scale, motivating distributed data stores.*
* **[The End of an Architectural Era (It's Time for a Complete Rewrite)](https://db.cs.cmu.edu/papers/2007/hstore-vldb2007.pdf) — Michael Stonebraker et al. (VLDB 2007)**  
  *Analyzes CPU overhead, locking, and memory bus limits in legacy single-node relational database engines under heavy concurrent workloads.*

---

## 🛠️ Engineering Blogs

* **[Amazon Builders' Library: Challenges with Distributed Systems](https://aws.amazon.com/builders-library/) — AWS Engineering**  
  *Explains real-world architectural challenges when scaling stateless application fleets while state remains bottlenecked on centralized datastores.*
* **[Figma’s Journey to Scaling PostgreSQL](https://www.figma.com/blog/how-figma-scaled-its-databases/) — Figma Engineering Blog**  
  *A production case study detailing how rapid user growth saturated single PostgreSQL database CPU and connection pools before distributing data.*
* **[How Stripe Scaled Its Infrastructure](https://stripe.com/blog/infrastructure-engineering)**  
  *Insights into managing database contention, connection pool exhaustion, and IOPS limits during massive payment processing surges.*

---

## 📑 Official Documentation

* **[PostgreSQL Documentation: Managing Connections & Tuning Memory](https://www.postgresql.org/docs/current/runtime-config-connection.html)**  
  *Official postgres guide detailing process-per-connection memory consumption and connection pool saturation limits.*
* **[MySQL Documentation: InnoDB Disk I/O & Thread Concurrency](https://dev.mysql.com/doc/refman/8.0/en/innodb-diskio.html)**  
  *Explains IOPS limits, write-ahead logging (WAL) synchronization locks, and hardware queue congestion in single-node MySQL setups.*

---

## 🎥 Conference Talks & Videos

* **[Rethinking Data Storage for Modern Applications](https://www.youtube.com/) — Martin Kleppmann**  
  *A conceptual keynote unpacking why application compute and data storage must scale under fundamentally different architectural rules.*
* **[Scaling Databases: Lessons Learned from Production Failures](https://www.infoq.com/presentations/) — InfoQ Architecture Presentations**  
  *Real-world post-mortems highlighting single-database connection saturation, locking bottlenecks, and operational single points of failure.*
