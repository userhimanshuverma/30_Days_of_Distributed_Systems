# Day 20 — References & Further Reading: Distributed Transactions

This document contains curated, authoritative primary sources, foundational research papers, production engineering articles, official documentation, and technical talks on **Distributed Transactions, Two-Phase Commit (2PC), and the Saga Pattern**.

---

## 📚 Books

* **Designing Data-Intensive Applications**
  * **Source**: Martin Kleppmann (O'Reilly Media, Chapter 9: Consistency and Consensus — "Distributed Transactions and Consensus")
  * **Link**: [https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/)
  * **Description**: Essential breakdown of atomic commit protocols, two-phase commit mechanics, coordinator failure modes, and distributed transaction trade-offs.

* **Transaction Processing: Concepts and Techniques**
  * **Source**: Jim Gray & Andreas Reuter (Morgan Kaufmann)
  * **Link**: [https://www.sciencedirect.com/book/9781558601901/transaction-processing](https://www.sciencedirect.com/book/9781558601901/transaction-processing)
  * **Description**: The definitive textbook on transaction processing, detailing write-ahead logging, two-phase locking, and atomic commitment.

* **Distributed Systems: Principles and Paradigms**
  * **Source**: Andrew S. Tanenbaum & Maarten van Steen (Pearson, Chapter 8: Coordination & Distributed Transactions)
  * **Link**: [https://www.distributed-systems.net/](https://www.distributed-systems.net/)
  * **Description**: Foundational textbook explaining nested transactions, flat transactions, 2PC, and 3PC protocols across autonomous systems.

---

## 📄 Research Papers

* **Notes on Data Base Operating Systems (1978)**
  * **Source**: Jim Gray (IBM Research Report / Operating Systems, Springer)
  * **Link**: [https://research.redhat.com/wp-content/uploads/2012/03/gray-notes-on-data-base-operating-systems.pdf](https://research.redhat.com/wp-content/uploads/2012/03/gray-notes-on-data-base-operating-systems.pdf)
  * **Description**: The landmark paper that formally introduced Two-Phase Commit (2PC) and write-ahead transaction recovery logging.

* **SAGAS (1987)**
  * **Source**: Hector Garcia-Molina & Kenneth Salem (Princeton University, ACM SIGMOD)
  * **Link**: [https://www.cs.cornell.edu/courses/cs632/2014sp/papers/sagas-87.pdf](https://www.cs.cornell.edu/courses/cs632/2014sp/papers/sagas-87.pdf)
  * **Description**: The original research paper introducing Sagas to break long-lived transactions into sequences of local transactions with compensating steps.

* **Consensus in the Presence of Partial Synchrony (1988)**
  * **Source**: Cynthia Dwork, Nancy Lynch, & Larry Stockmeyer (Journal of the ACM)
  * **Link**: [https://dl.acm.org/doi/pdf/10.1145/42282.42283](https://dl.acm.org/doi/pdf/10.1145/42282.42283)
  * **Description**: Mathematical analysis of atomic agreement under varying network models and crash-recovery failure regimes.

---

## 🛠️ Engineering Blogs

* **Building Financial Systems on Event-Driven Architecture**
  * **Source**: Uber Engineering Blog
  * **Link**: [https://www.uber.com/blog/building-financial-systems-on-event-driven-architecture/](https://www.uber.com/blog/building-financial-systems-on-event-driven-architecture/)
  * **Description**: Insights into how Uber coordinates fare payment, driver payout, and rider billing asynchronously across microservice boundaries.

* **Sagas: Distributed Transactions in Microservices**
  * **Source**: Microservices.io (Chris Richardson)
  * **Link**: [https://microservices.io/patterns/data/saga.html](https://microservices.io/patterns/data/saga.html)
  * **Description**: Comprehensive architectural reference comparing Orchestration vs. Choreography in Saga pattern implementations.

* **Amazon DynamoDB Transactions: How It Works**
  * **Source**: AWS Architecture Blog / DynamoDB Documentation
  * **Link**: [https://aws.amazon.com/blogs/aws/new-amazon-dynamodb-transactions/](https://aws.amazon.com/blogs/aws/new-amazon-dynamodb-transactions/)
  * **Description**: Technical explanation of how DynamoDB executes coordinated two-phase transactions across distributed partition keys.

---

## 🌐 Official Documentation

* **Temporal Documentation: Workflows & Compensation**
  * **Source**: Temporal Technologies
  * **Link**: [https://docs.temporal.io/workflows](https://docs.temporal.io/workflows)
  * **Description**: Production reference for durable workflow orchestration engines that handle saga state persistence, retries, and compensation.

* **PostgreSQL Documentation: PREPARE TRANSACTION & 2PC**
  * **Source**: PostgreSQL Global Development Group
  * **Link**: [https://www.postgresql.org/docs/current/sql-prepare-transaction.html](https://www.postgresql.org/docs/current/sql-prepare-transaction.html)
  * **Description**: Official SQL command specification for Postgres prepared transactions used in two-phase commit coordinators.

* **Apache Kafka Documentation: Transactional Messaging**
  * **Source**: Apache Software Foundation
  * **Link**: [https://kafka.apache.org/documentation/#design_transactions](https://kafka.apache.org/documentation/#design_transactions)
  * **Description**: Details Kafka's internal Transaction Coordinator, `initTransactions()`, and atomic writes across topics.

---

## 🎥 Conference Talks

* **GOTO 2015 • Applying the Saga Pattern**
  * **Source**: Caitie McCaffrey (Twitter / GOTO Conferences)
  * **Link**: [https://www.youtube.com/watch?v=0UTOLRTwDB0](https://www.youtube.com/watch?v=0UTOLRTwDB0)
  * **Description**: High-impact talk explaining how to manage distributed state recovery across microservices using compensating operations.

* **Distributed Transactions at Scale**
  * **Source**: Randy Shoup (eBay / Google / QCon)
  * **Link**: [https://www.youtube.com/watch?v=YPbGW3Fnmbc](https://www.youtube.com/watch?v=YPbGW3Fnmbc)
  * **Description**: Pragmatic engineering perspective on moving away from 2PC towards eventual consistency, idempotency, and asynchronous sagas.

---

## 📹 Videos

* **System Design: Distributed Transactions (2PC vs Saga)**
  * **Source**: ByteByteGo (Alex Xu)
  * **Link**: [https://www.youtube.com/watch?v=vVj4xXqPHzY](https://www.youtube.com/watch?v=vVj4xXqPHzY)
  * **Description**: High-level visual comparison demonstrating the Prepare/Commit phases of 2PC alongside Saga compensating workflows.

* **Two-Phase Commit Protocol Explained**
  * **Source**: Martin Kleppmann (University of Cambridge Lectures)
  * **Link**: [https://www.youtube.com/watch?v=gT8-yK6hZJk](https://www.youtube.com/watch?v=gT8-yK6hZJk)
  * **Description**: Computer science lecture detailing coordinator state machines, failure recovery logs, and blocking conditions in 2PC.
