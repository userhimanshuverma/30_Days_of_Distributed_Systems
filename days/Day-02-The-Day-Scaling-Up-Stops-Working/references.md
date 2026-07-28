# 📚 Day 2 References & Further Reading

These resources delve deeper into physical hardware bottlenecks, Amdahl's Law, the limits of vertical scaling, and the transition toward horizontal distributed systems.

---

## 📖 Books

* **[Designing Data-Intensive Applications](https://dataintensive.net/)** by Martin Kleppmann  
  *The foundational guide on data system architecture, scalability bottlenecks, and trade-offs in distributed computing.*
* **[Site Reliability Engineering: How Google Runs Production Systems](https://sre.google/sre-book/table-of-contents/)** by Betsy Beyer, Chris Jones, Jennifer Petoff, and Niall Richard Murphy  
  *Insights into how Google manages massive scale across hundreds of thousands of commodity machines rather than giant single mainframes.*
* **[Computer Architecture: A Quantitative Approach](https://www.elsevier.com/books/computer-architecture/hennessy/978-0-12-811905-1)** by John L. Hennessy and David A. Patterson  
  *The classic textbook explaining the physical hardware limits of processors, memory buses, and multi-core scaling constraints.*

---

## 📰 Engineering Blogs

* **[Google Research: Web Search for a Planet: The Google Cluster Architecture](https://research.google/pubs/pub27777/)**  
  *Google's landmark original research paper detailing why they abandoned large servers in favor of clusters of low-cost commodity PCs.*
* **[AWS Architecture Center: Scaling Up vs. Scaling Out](https://aws.amazon.com/architecture/)**  
  *An operational breakdown from AWS on vertical hardware limits and how cloud infrastructure enables seamless scale-out architectures.*
* **[Netflix TechBlog: Building Cloud-Native Systems](https://netflixtechblog.com/)**  
  *Case studies on how Netflix migrated away from massive relational databases on single servers to horizontally distributed microservices.*
* **[Cloudflare Blog: Understanding Hardware Bottlenecks at Scale](https://blog.cloudflare.com/)**  
  *Real-world engineering posts covering network interface limits, memory bandwidth ceilings, and Linux kernel context-switching overhead.*

---

## 📄 Official Documentation

* **[The System Design Primer: Scalability Concepts](https://github.com/donnemartin/system-design-primer)**  
  *Comprehensive visual summaries comparing vertical scaling trade-offs against horizontal scaling topologies.*
* **[Linux Kernel Documentation: NUMA and CPU Affinity](https://www.kernel.org/doc/html/latest/)**  
  *Technical details on non-uniform memory access (NUMA) bottlenecks when adding dozens of CPU cores to a single motherboard.*

---

## 🎙️ Conference Talks

* **[Martin Kleppmann: Distributed Systems Keynote](https://www.youtube.com/results?search_query=martin+kleppmann+distributed+systems)**  
  *An engaging breakdown of why single-node computing hits physical barriers and how distributed state changes software design.*
* **[Jeff Dean: Building Software Systems at Google Scale](https://www.youtube.com/results?search_query=jeff+dean+building+software+systems+at+google+scale)**  
  *Google Senior Fellow Jeff Dean explains the practical design principles behind computing across thousands of nodes.*

---

## 🎥 Videos

* **[GOTO Conferences: Scaling Up vs Scaling Out](https://www.youtube.com/results?search_query=goto+conference+scaling+up+vs+scaling+out)**  
  *Clear visual presentations comparing multi-core motherboard bottlenecks with horizontal cluster architectures.*
* **[MIT 6.824: Lecture 1 - Introduction to Distributed Systems](https://www.youtube.com/watch?v=cQP851234pq)**  
  *MIT's flagship course lecture explaining why software engineering evolved from single-machine compute to distributed networks.*
