# Day 8: Split Brain — References & Further Reading

This curated list of resources provides foundational context on network partitions, dual-leader anomalies, data corruption risks, and split-brain phenomena in distributed production systems.

---

## 📚 Books

* **[Designing Data-Intensive Applications (Chapter 8: The Trouble with Distributed Systems)](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/)** — Martin Kleppmann's comprehensive discussion on unreliable networks, network partitions, and the dangers of split-brain in distributed state management.
* **[Site Reliability Engineering: How Google Runs Production Systems (Chapter 23: Managing Critical State)](https://sre.google/sre-book/table-of-contents/)** — Google SRE insights on maintaining consistency across global datacenters and preventing brain split in Chubby lock service deployments.
* **[Database Internals: A Deep Dive into How Distributed Data Systems Work (Chapter 10: Fault Tolerance)](https://www.oreilly.com/library/view/database-internals/9781492040330/)** — Alex Petrov's exploration of network partitions, partial failure modes, and the catastrophic impact of dual leaders on database engines.

---

## 📑 Research Papers

* **[CAP Twelve Years Later: How the "Rules" Have Changed (Eric Brewer, 2012)](https://beebom.com/wp-content/uploads/2021/04/Brewer-CAP-12-years.pdf)** — Eric Brewer's reflection on how network partitions force distributed systems to explicitly trade availability for consistency to prevent split-brain corruption.
* **[In Search of an Understandable Consensus Algorithm (Diego Ongaro & John Ousterhout, 2014)](https://raft.github.io/raft.pdf)** — The consensus paper explaining why single-leader invariants are critical and how network partitions create candidate isolation.
* **[The Chubby Lock Service for Loosely-Coupled Distributed Systems (Mike Burrows, Google, 2006)](https://research.google/pubs/pub27897/)** — Case study detailing how Google's infrastructure avoids split-brain through strict distributed locking and master coordination.

---

## 📰 Engineering Blogs

* **[Cloudflare Blog: Network Partitions and the Dangers of Split Brain](https://blog.cloudflare.com/)** — Practical post-mortem analysis showing how real-world fiber cuts and packet drops induce dual-master scenarios if not strictly controlled.
* **[Etcd Engineering Blog: Preserving Kubernetes Control Plane Consistency](https://etcd.io/blog/)** — Technical breakdown explaining why etcd refuses writes when disconnected from the cluster to protect Kubernetes etcd state.
* **[AWS Architecture Blog: Designing Resilient Systems Against Network Partitions](https://aws.amazon.com/blogs/architecture/)** — High-level operational strategies for detecting lost connectivity across availability zones before data divergence occurs.

---

## 📑 Official Documentation

* **[Kubernetes Documentation: Operating etcd Clusters for High Availability](https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/)** — Official guidance on etcd node counts and preventing split-brain states in production Kubernetes clusters.
* **[Etcd Official Documentation: FAQ on Network Partitions](https://etcd.io/docs/v3.5/faq/)** — Detailed explanation of what happens to etcd nodes during a network partition and why partition isolation preserves data integrity.
* **[Elasticsearch Documentation: Split-Brain Prevention in Master Nodes](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-discovery.html)** — Architectural notes on master node elections and preventing dual-master Elasticsearch clusters.

---

## 🎤 Conference Talks

* **[Martin Kleppmann — Distributed Systems Want To Break Your Heart (QCon)](https://www.youtube.com/results?search_query=martin+kleppmann+distributed+systems+want+to+break+your+heart)** — Keynote analyzing real-world network partitions, split-brain failure modes, and why data loss happens in healthy systems.
* **[CNCF Presentation — Avoiding Split-Brain in Kubernetes Control Planes](https://www.youtube.com/results?search_query=cncf+kubernetes+etcd+split+brain)** — Technical presentation breaking down how Kubernetes handles isolated nodes without corrupting API server state.

---

## 🎥 Videos

* **[MIT 6.824: Distributed Systems — Lecture 3: Network Partitions and Fault Tolerance](https://www.youtube.com/results?search_query=mit+6.824+network+partitions)** — MIT lecture covering partition models, partial failure, and why dual leaders destroy serializability.
* **[Computerphile: Split Brain Problem in Distributed Systems](https://www.youtube.com/results?search_query=computerphile+split+brain)** — Intuitive visual overview of split brain scenarios and why network cuts lead to conflicting server states.
