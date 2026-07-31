# Day 5: The Impossible Triangle — References & Further Reading

This collection of resources covers the theoretical foundation, practical implications, and real-world trade-offs of the CAP Theorem and network partitions in distributed systems.

---

## 📚 Books

* **[Designing Data-Intensive Applications (Chapter 8 & 9)](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/)** — Martin Kleppmann’s definitive guide on network partitions, linearizability, and the physical trade-offs of consistency versus availability.
* **[Site Reliability Engineering: How Google Runs Production Systems (Chapter 23)](https://sre.google/sre-book/table-of-contents/)** — Google SRE handbook detailing how large-scale distributed services manage reliability and network split-brain scenarios.

---

## 📑 Research Papers

* **[Towards Robust Distributed Systems (Eric Brewer, 2000)](https://eecs.berkeley.edu/~brewer/cs262b-2004/PODC-keynote.pdf)** — Eric Brewer's original keynote address presenting the CAP hypothesis at the Symposium on Principles of Distributed Computing (PODC).
* **[CAP Twelve Years Later: How the "Rules" Have Changed (Eric Brewer, 2012)](https://www.infoq.com/articles/cap-twelve-years-later-how-the-rules-have-changed/)** — Brewer's follow-up paper clarifying common misunderstandings about the 2-out-of-3 myth and partition handling.
* **[Consistency Tradeoffs in Modern Distributed Database System Design (Daniel Abadi, 2012)](https://www.computer.org/csdl/magazine/co/2012/02/mco2012020037/13rRUxAIFjW)** — Introduces the PACELC theorem, extending CAP to include latency trade-offs during normal (non-partitioned) operation.

---

## 📰 Engineering Blogs

* **[Netflix Technology Blog: Active-Active Multi-Region Deployment](https://netflixtechblog.com/)** — Insights into how Netflix prioritizes availability during regional cloud isolation and network degradation.
* **[AWS Architecture Center: Building Fault-Tolerant High-Availability Systems](https://aws.amazon.com/architecture/)** — Guidelines on choosing data consistency models and handling network partition events across Availability Zones.
* **[Cloudflare Engineering Blog: Understanding Network Partitions](https://blog.cloudflare.com/)** — Real-world operational post-mortems and analysis of fiber cuts, BGP leaks, and network edge isolations.

---

## 📑 Official Documentation

* **[Amazon DynamoDB Documentation: Data Consistency Model](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html)** — Explains eventual consistency vs. strongly consistent reads in distributed key-value stores.
* **[Apache Cassandra Documentation: Architecture & Consistency Levels](https://cassandra.apache.org/doc/latest/cassandra/architecture/overview.html)** — Details how tunable consistency allows engineers to balance CAP trade-offs per read/write query.

---

## 🎤 Conference Talks

* **[Martin Kleppmann — Distributed Systems Want To Break Your Heart (QCon)](https://www.youtube.com/results?search_query=martin+kleppmann+distributed+systems+want+to+break+your+heart)** — A classic talk demonstrating how network delays, clock drift, and partitions disrupt simple engineering assumptions.
* **[Eric Brewer — CAP Theorem and Beyond (Google Tech Talk)](https://www.youtube.com/results?search_query=eric+brewer+cap+theorem)** — Brewer unpacks the practical realities of high availability and partition recovery.

---

## 🎥 Videos

* **[MIT 6.824: Distributed Systems — CAP Theorem & Linearizability](https://www.youtube.com/results?search_query=mit+6.824+cap+theorem)** — Lecture series explaining formal definitions of consistency and partition tolerance in distributed consensus algorithms.
