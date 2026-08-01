# Day 6: Leader Election — References & Further Reading

This curated list of resources provides deeper context on leader election, central coordination, and single-leader architectures in real-world distributed systems.

---

## 📚 Books

* **[Designing Data-Intensive Applications (Chapter 5: Replication & Chapter 9: Consistency & Consensus)](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/)** — Martin Kleppmann's authoritative analysis of single-leader replication, active-passive architectures, and the role of coordination.
* **[Site Reliability Engineering: How Google Runs Production Systems (Chapter 23: Managing Critical State)](https://sre.google/sre-book/table-of-contents/)** — Google SRE guide detailing how leader election and centralized state management are maintained under high availability constraints.
* **[Database Internals: A Deep Dive into How Distributed Data Systems Work (Chapter 10)](https://www.oreilly.com/library/view/database-internals/9781492040330/)** — Alex Petrov’s comprehensive overview of leader-follower roles, primary-backup coordination, and split-brain risks.

---

## 📑 Research Papers

* **[In Search of an Understandable Consensus Algorithm (Ongaro & Ousterhout, 2014)](https://raft.github.io/raft.pdf)** — The landmark USENIX ATC paper introducing Raft, emphasizing leader election as a distinct phase for cluster coordination.
* **[Paxos Made Simple (Leslie Lamport, 2001)](https://lamport.azurewebsites.net/pubs/paxos-simple.pdf)** — Lamport's classic foundational paper explaining how distributed agreement operates around a distinguished leader/proposer.
* **[ZooKeeper: Wait-free coordination for Cloud Services (Hunt et al., 2010)](https://www.usenix.org/legacy/event/atc10/tech/full_paper/Hunt.pdf)** — The USENIX paper explaining ZooKeeper's architecture for central coordination, leader election, and distributed locks.

---

## 📰 Engineering Blogs

* **[Kubernetes Blog: Kubernetes Leader Election in Go](https://kubernetes.io/blog/)** — Technical deep dive into how Kubernetes components use leader election abstractions for high-availability control planes.
* **[etcd Blog: High Availability and Leader Coordination](https://etcd.io/blog/)** — Insights into how etcd maintains primary coordination and cluster metadata state.
* **[Cloudflare Blog: How We Built a Distributed Scheduler](https://blog.cloudflare.com/)** — Real-world post-mortem and design breakdown of central scheduling without duplicate execution.

---

## 📑 Official Documentation

* **[Kubernetes Documentation: Control Plane Components & Leader Election](https://kubernetes.io/docs/concepts/overview/components/)** — Official documentation explaining how `kube-scheduler` and `kube-controller-manager` select leaders.
* **[etcd Documentation: Core Architecture & Governance](https://etcd.io/docs/)** — Overview of how etcd acts as the single source of truth for cluster state coordination.
* **[Apache ZooKeeper Documentation: Leader Election & Recipes](https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html)** — Guide to ZooKeeper primitives for electing leaders and maintaining lock synchronization.

---

## 🎤 Conference Talks

* **[Martin Kleppmann — Distributed Systems Want To Break Your Heart (QCon)](https://www.youtube.com/results?search_query=martin+kleppmann+distributed+systems+want+to+break+your+heart)** — Discussion on the necessity of leader coordination to prevent split-brain and state corruption.
* **[CNCF Presentation — Kubernetes Control Plane High Availability](https://www.youtube.com/results?search_query=kubernetes+control+plane+high+availability+cncf)** — Session explaining how Kubernetes control plane instances elect a primary leader to execute controller loops.

---

## 🎥 Videos

* **[MIT 6.824: Distributed Systems — Primary-Backup Replication & Leaders](https://www.youtube.com/results?search_query=mit+6.824+primary+backup+replication)** — MIT lecture series breaking down why primary-backup models rely on single-leader authority.
* **[USENIX ATC — Raft and Leader-Based Systems](https://www.youtube.com/results?search_query=usenix+raft+leader+election)** — Conference presentation detailing the intuition behind leader-driven cluster coordination.
