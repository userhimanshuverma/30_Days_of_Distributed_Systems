# Day 1 References: Why One Server Is Never Enough

Curated references and foundational reading materials exploring hardware resource limits, vertical scaling trade-offs, and the physical constraints of single-machine web server architectures.

---

## 📚 Books

- **[Designing Data-Intensive Applications](https://dataintensive.net/) by Martin Kleppmann**  
  *Essential reading (Chapter 1) on reliability, scalability, and how hardware limits define system architecture.*
- **[Site Reliability Engineering: How Google Runs Production Systems](https://sre.google/sre-book/table-of-contents/) by Betsy Beyer, Chris Jones, Jennifer Petoff, and Niall Richard Murphy**  
  *Provides empirical insights into operational limits, service degradation, and capacity planning under extreme load.*
- **[Systems Performance: Enterprise and the Cloud (2nd Edition)](https://www.brendangregg.com/systems-performance-2nd-edition-book.html) by Brendan Gregg**  
  *Definitive guide to CPU, memory, storage, and networking hardware bottlenecks inside host operating systems.*

---

## 📰 Engineering Blogs

- **[Netflix TechBlog — Modernizing the Netflix Streaming Bus](https://netflixtechblog.com/)**  
  *Explains why global media platforms cannot rely on single giant compute nodes and how traffic spikes force architectural evolution.*
- **[Cloudflare Blog — How We Handle Millions of Requests per Second](https://blog.cloudflare.com/)**  
  *Demonstrates real-world network buffer limits, socket backlogs, and hardware saturation at internet scale.*
- **[AWS Architecture Center — Scalability & Reliability Whitepapers](https://aws.amazon.com/architecture/)**  
  *Offers foundational design frameworks explaining the ceiling of vertical compute instances vs. distributed architectures.*
- **[Google Cloud Architecture Framework — System Capacity & Scaling](https://cloud.google.com/architecture/framework)**  
  *Details hardware capacity planning, resource quota management, and hardware failure modes.*

---

## 📖 Official Documentation

- **[Linux Kernel Networking & Socket Backlog Documentation](https://www.kernel.org/doc/html/latest/networking/)**  
  *Deep dive into TCP SYN queues, accept backlogs (`somaxconn`), and socket buffer allocation during traffic surges.*
- **[NGINX Tuning & Worker Process Configuration Guide](https://nginx.org/en/docs/)**  
  *Official documentation explaining how CPU cores, worker processes, and connection limits dictate server capacity.*
- **[Python Queue & Concurrent Execution Documentation](https://docs.python.org/3/library/queue.html)**  
  *Explains memory queue constraints, thread pool scheduling, and non-blocking task handling.*

---

## 🎤 Conference Talks

- **[GOTO 2015: Designing Data-Intensive Applications](https://www.youtube.com/watch?v=fU9hR3kiOK0) by Martin Kleppmann**  
  *A foundational talk breaking down why single-node paradigms fail when data volume and request throughput outgrow physical hardware.*
- **[USENIX LISA: Systems Performance and Monitoring](https://www.usenix.org/conference/lisa19) by Brendan Gregg**  
  *Visualizes CPU utilization, memory bus contention, and disk queue depth in production environments.*

---

## 🎥 Videos

- **[MIT 6.824: Distributed Systems (Lecture 1 — Introduction)](https://www.youtube.com/watch?v=cQP8WApzIQQ)**  
  *First principles introduction to why computer systems shift from single machines to distributed nodes.*
- **[How Large-Scale Web Applications Work (System Design Basics)](https://www.youtube.com/watch?v=SqcXvc3Lev8)**  
  *High-level conceptual breakdown of request lifecycles, load bottlenecks, and hardware limits.*
