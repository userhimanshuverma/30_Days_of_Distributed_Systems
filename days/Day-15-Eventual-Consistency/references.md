# 📚 Day 15 References: Eventual Consistency — Why Your Instagram Like Appears Later

Curated learning resources, foundational research papers, engineering blogs, and official documentation on eventual consistency, replication lag, and consistency trade-offs in modern distributed systems.

---

## 📖 Books

* **[Designing Data-Intensive Applications (DDIA)](https://dataintensive.net/) — Martin Kleppmann**  
  *Chapter 5 ("Replication: Problems with Replication Lag") breaks down read-after-write consistency, monotonic reads, and eventual convergence in replicated databases.*
* **[Database Internals: A Deep Dive into How Distributed Data Systems Work](https://www.databass.dev/) — Alex Petrov**  
  *Chapter 10 details eventual consistency models, read repair, anti-entropy protocols, and background convergence mechanisms.*
* **[Distributed Systems: Principles and Paradigms](https://www.distributed-systems.net/) — Andrew S. Tanenbaum & Maarten van Steen**  
  *Provides formal definitions of data-centric and client-centric consistency models including eventual consistency and monotonic read guarantees.*

---

## 🔬 Research Papers

* **[Eventually Consistent](https://dl.acm.org/doi/10.1145/1466443.1466448) — Werner Vogels (CACM 2009 / ACM Queue 2008)**  
  *The landmark paper by Amazon's CTO explaining why high-scale distributed systems opt for eventual consistency and defining client-side consistency trade-offs.*
* **[Dynamo: Amazon's Highly Available Key-value Store](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf) — Giuseppe DeCandia et al. (SOSP 2007)**  
  *The foundational paper introducing tunable consistency, vector clocks, and background anti-entropy for high-availability cloud storage.*
* **[Quantifying Eventual Consistency in Replicated Databases](https://www.usenix.org/system/files/conference/socc2012/socc2012-paper17.pdf) — Peter Bailis et al. (SoCC 2012 / PBS)**  
  *Introduces Probabilistically Bounded Staleness (PBS) to measure how likely a read is to observe a recent write under eventual consistency.*

---

## 🛠️ Engineering Blogs

* **[TAO: Meta's Distributed Data Store for the Social Graph](https://engineering.fb.com/2013/06/25/core-infra/tao-the-power-behind-facebook-s-social-graph/) — Meta Engineering**  
  *Explains how Meta handles billions of social interactions per second using asynchronous replication caches optimized for read heavy eventually consistent graphs.*
* **[Amazon S3 Strong Consistency Announcement](https://aws.amazon.com/blogs/aws/amazon-s3-update-strong-read-after-write-consistency/) — AWS News Blog**  
  *Recounts S3's historical evolution from eventual consistency to strong read-after-write consistency for object operations.*
* **[Global Data Replication with Cassandra at Netflix](https://netflixtechblog.com/) — Netflix TechBlog**  
  *Explores how Netflix manages cross-region asynchronous database replication, handling propagation lag while serving video streaming metadata.*

---

## 📑 Official Documentation

* **[AWS DynamoDB Developer Guide: Eventual Consistency vs Strong Consistency](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html)**  
  *Official AWS guide explaining the latency, throughput cost, and behavior differences between eventual and strongly consistent read operations.*
* **[Apache Cassandra Documentation: Architecture & Data Replication](https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html)**  
  *Official technical reference detailing asynchronous multi-datacenter replication, hint handoff, and background read repair.*
* **[Google Cloud Spanner: Replication & Consistency Model](https://cloud.google.com/spanner/docs/replication)**  
  *Official documentation contrasting Google Cloud Spanner's synchronous TrueTime strong consistency with traditional eventually consistent datastores.*

---

## 🎥 Conference Talks

* **[QCon: Eventual Consistency — How Soon Is Eventually?](https://www.infoq.com/presentations/) — Peter Bailis**  
  *Engineering presentation dissecting real-world replication lag measurements and evaluating bounded staleness guarantees in production.*
* **[AWS re:Invent: Building Highly Available Distributed Applications](https://www.youtube.com/) — Werner Vogels**  
  *Keynote address exploring operational trade-offs between availability, latency, and consistency models across global microservices.*

---

## 🎬 Videos

* **[Distributed Systems 5.3: Eventual Consistency & Anti-Entropy](https://www.youtube.com/) — Martin Kleppmann (Cambridge University)**  
  *Visual university lecture covering replication lag, background anti-entropy techniques, and formal properties of eventual convergence.*
* **[MIT 6.824: Lecture 7 — Eventual Consistency & Dynamo](https://www.youtube.com/) — Robert Morris (MIT)**  
  *MIT Computer Science lecture walking through the architectural trade-offs of eventually consistent key-value stores.*
