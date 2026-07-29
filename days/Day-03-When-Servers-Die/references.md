# 📚 Day 3 References & Further Reading

These resources explore single points of failure, redundancy intuition, high availability fundamentals, and building fault-tolerant architectures.

---

## 📖 Books

* **[Designing Data-Intensive Applications](https://dataintensive.net/)** by Martin Kleppmann  
  *Chapter 5 introduces the fundamental need for replication to maintain availability when hardware components fail.*
* **[Site Reliability Engineering: How Google Runs Production Systems](https://sre.google/sre-book/table-of-contents/)** by Betsy Beyer, Chris Jones, Jennifer Petoff, and Niall Richard Murphy  
  *Covers Google's philosophy on accepting server failures as normal events and building software-managed redundancy.*
* **[Release It!: Design and Deploy Production-Ready Software](https://pragprog.com/titles/mnee2/release-it-second-edition/)** by Michael T. Nygard  
  *Examines real-world production outages caused by single points of failure and physical hardware crashes.*

---

## 📰 Engineering Blogs

* **[Google Cloud Architecture Center: High Availability and Redundancy Design](https://cloud.google.com/architecture)**  
  *Explains basic architectural patterns for designing redundant systems that survive physical machine loss.*
* **[AWS Well-Architected Framework: Reliability Pillar](https://aws.amazon.com/architecture/well-architected/)**  
  *AWS operational guidelines for eliminating single points of failure and automating recovery across backup resources.*
* **[Cloudflare Blog: Lessons From Production Outages](https://blog.cloudflare.com/)**  
  *Real-world engineering post-mortems analyzing single-node failures and the transition toward replicated backup paths.*
* **[Netflix TechBlog: Redundancy and Chaos Engineering](https://netflixtechblog.com/)**  
  *Details how Netflix designs cloud services to survive sudden server crashes without customer disruption.*

---

## 📄 Official Documentation

* **[The System Design Primer: Redundancy & Replication Concepts](https://github.com/donnemartin/system-design-primer)**  
  *Visual breakdown of single points of failure (SPOF) and how adding replicas restores service availability.*
* **[Kubernetes Documentation: High Availability Overview](https://kubernetes.io/docs/concepts/architecture/)**  
  *Conceptual documentation on replacing failed container instances with replicated pods across physical nodes.*

---

## 🎙️ Conference Talks

* **[Martin Kleppmann: Redundancy and Replication Intuition](https://www.youtube.com/results?search_query=martin+kleppmann+replication)**  
  *An intuitive talk breaking down why single-node storage fails and why storing multiple copies is required for reliability.*
* **[Netflix Chaos Engineering: Lessons in Server Resilience](https://www.youtube.com/results?search_query=netflix+chaos+engineering+server+failures)**  
  *Engineering talk demonstrating what happens when servers die in production and how failover prevents downtime.*

---

## 🎥 Videos

* **[MIT 6.824: Fault Tolerance & Primary-Backup Replication Intuition](https://www.youtube.com/watch?v=cQP851234pq)**  
  *Lecture introducing why hardware failures necessitate maintaining backup copies of application state.*
* **[ByteByteGo: What is High Availability and Failover?](https://www.youtube.com/results?search_query=bytebytego+high+availability)**  
  *Short visual animation contrasting single-server vulnerability against multi-server replicated availability.*
