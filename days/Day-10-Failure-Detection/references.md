# Day 10: Failure Detection — References & Further Reading

This curated selection of resources provides foundational and technical context on failure detection, dealing with network uncertainty, and managing machine liveness in distributed systems.

---

## 📚 Books

* **[Designing Data-Intensive Applications (Chapter 8: The Trouble with Distributed Systems)](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/)** — Martin Kleppmann's masterclass on unreliable networks, stop-the-world GC pauses, clock drift, and why node failures can only be inferred through timeouts.
* **[Site Reliability Engineering: How Google Runs Production Systems (Chapter 23: Managing Critical State)](https://sre.google/sre-book/table-of-contents/)** — Google SRE handbook detailing how large-scale infrastructure handles node liveness, heartbeat intervals, and automated failover safety.

---

## 📑 Research Papers

* **[Unreliable Failure Detectors for Reliable Distributed Systems (Chandra & Toueg, 1996)](https://dl.acm.org/doi/10.1145/226643.226647)** — The seminal paper introducing the mathematical abstraction of failure detectors, formalizing completeness vs. accuracy under partial synchrony.

---

## 📰 Engineering Blogs

* **[Kubernetes Blog: Node Heartbeats and Lease API](https://kubernetes.io/blog/)** — Technical post on how Kubernetes handles node health monitoring and evolved from heavy NodeStatus updates to lightweight Lease API heartbeats.
* **[AWS Architecture Blog: Handling Transient Failures and Timeouts](https://aws.amazon.com/blogs/architecture/)** — Operational best practices on configuring heartbeat intervals, retry strategies, and avoiding false positives during network degradation.

---

## 📑 Official Documentation

* **[Kubernetes Documentation: Node Health Monitoring](https://kubernetes.io/docs/concepts/architecture/nodes/#heartbeats)** — Official guide explaining how the kubelet reports node health and how the node lifecycle controller handles missing heartbeats.
* **[etcd Documentation: Tuning Heartbeat Interval and Election Timeout](https://etcd.io/docs/v3.5/tuning/)** — Practical operational documentation detailing how to configure heartbeat frequencies relative to network round-trip time and disk latency.
* **[Apache ZooKeeper Documentation: Session Management](https://zookeeper.apache.org/doc/r3.8.0/zookeeperProgrammers.html#ch_zkSessions)** — Explains how ZooKeeper clients maintain session liveness through continuous heartbeat pings to detect node failures.

---

## 🎤 Conference Talks

* **[Martin Kleppmann — Distributed Systems Want To Break Your Heart (QCon)](https://www.youtube.com/results?search_query=martin+kleppmann+distributed+systems+want+to+break+your+heart)** — Outstanding presentation exploring the physical realities of missing messages, network delays, and failure detection trade-offs.
* **[CNCF / KubeCon — Node Lifecycle Management & Health Monitoring in Kubernetes](https://www.youtube.com/results?search_query=kubecon+node+lifecycle+controller+heartbeat)** — Deep dive into how Kubernetes node monitoring balances fast recovery with protection against false alarms.

---

## 🎥 Videos

* **[MIT 6.824: Distributed Systems — Failure Detection & Timeouts](https://www.youtube.com/results?search_query=mit+6.824+failure+detection)** — Lecture series covering fundamental failure modes, asynchronous network assumptions, and handling partial failures in consensus protocols.
