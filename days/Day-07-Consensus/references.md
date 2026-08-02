# Day 7: Consensus — References & Further Reading

This curated list of resources provides deeper context on distributed consensus, quorum decision-making, and state machine replication in production systems.

---

## 📚 Books

* **[Designing Data-Intensive Applications (Chapter 9: Consistency & Consensus)](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/)** — Martin Kleppmann's masterclass on consensus algorithms, linearizability, and why leader election alone is insufficient for total order.
* **[Site Reliability Engineering: How Google Runs Production Systems (Chapter 23: Managing Critical State)](https://sre.google/sre-book/table-of-contents/)** — Google SRE insights into how distributed consensus engines (like Chubby) maintain single source of truth under continuous hardware faults.
* **[Database Internals: A Deep Dive into How Distributed Data Systems Work (Chapter 11: Consensus)](https://www.oreilly.com/library/view/database-internals/9781492040330/)** — Alex Petrov's detailed exploration of multi-paxos, Raft replication loops, and consensus-backed state engines.

---

## 📑 Research Papers

* **[In Search of an Understandable Consensus Algorithm (Diego Ongaro & John Ousterhout, 2014)](https://raft.github.io/raft.pdf)** — The original USENIX ATC paper introducing Raft, designed specifically to decouple consensus intuition into readable, modular phases.
* **[Paxos Made Simple (Leslie Lamport, 2001)](https://lamport.azurewebsites.net/pubs/paxos-simple.pdf)** — Leslie Lamport's seminal paper laying out the foundational mathematical model of distributed agreement.
* **[The Chubby Lock Service for Loosely-Coupled Distributed Systems (Mike Burrows, Google, 2006)](https://research.google/pubs/pub27897/)** — Google's real-world paper explaining how consensus locks are leveraged across massive datacenter clusters.

---

## 📰 Engineering Blogs

* **[Etcd Blog: How Etcd Uses Raft to Manage Kubernetes State](https://etcd.io/blog/)** — Architectural breakdown showing how etcd acts as the persistent, consensus-backed engine behind Kubernetes control plane state.
* **[CockroachDB Blog: Consensus, Quorums, and Replicated State Machines](https://www.cockroachlabs.com/blog/)** — In-depth article explaining how distributed SQL databases use majority voting for serializable consistency.
* **[Cloudflare Blog: Building a Distributed Lock Manager with Raft](https://blog.cloudflare.com/)** — Practical engineering post-mortem on handling network partitions while maintaining cluster agreement.

---

## 📑 Official Documentation

* **[Etcd Official Documentation: Raft Consensus & Architecture](https://etcd.io/docs/v3.5/learning/algorithm/)** — Official documentation explaining how etcd replicates state changes across a cluster of 3 or 5 nodes.
* **[Kubernetes Documentation: Operating etcd Clusters for High Availability](https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/)** — Operational guide on maintaining odd-numbered etcd nodes to preserve quorum requirements.
* **[Raft Consensus Algorithm Web Portal & Visualizations](https://raft.github.io/)** — Interactive visualizations and complete specification for the Raft consensus algorithm.

---

## 🎤 Conference Talks

* **[Martin Kleppmann — Distributed Systems Want To Break Your Heart (QCon)](https://www.youtube.com/results?search_query=martin+kleppmann+distributed+systems+want+to+break+your+heart)** — Engaging keynote on split-brain, lost updates, and why consensus is necessary for distributed correctness.
* **[CNCF Presentation — How etcd Works Under the Hood in Kubernetes](https://www.youtube.com/results?search_query=cncf+etcd+raft+kubernetes)** — Deep dive presentation explaining how Kubernetes API requests are serialized via Raft consensus.

---

## 🎥 Videos

* **[MIT 6.824: Distributed Systems — Lecture 5: Raft Consensus](https://www.youtube.com/results?search_query=mit+6.824+raft+lecture)** — MIT's premier computer science lecture detailing the transition from leader election to majority agreement.
* **[Secret Algorithm Behind Kubernetes: Raft Explained Simply](https://www.youtube.com/results?search_query=raft+consensus+explained+kubernetes)** — Conceptual visual walkthrough showing how nodes vote and commit proposals in production.
