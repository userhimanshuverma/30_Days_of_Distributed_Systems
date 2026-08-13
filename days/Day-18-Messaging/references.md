# Day 18 — References & Further Reading: Messaging, Kafka & RabbitMQ

This document contains curated, authoritative primary sources, foundational research papers, production engineering articles, official documentation, and technical talks on **Asynchronous Messaging, Queueing Systems, Apache Kafka, and RabbitMQ**.

---

## 📚 Books

* **Designing Data-Intensive Applications**
  * **Source**: Martin Kleppmann (O'Reilly Media, Chapter 11: Stream Processing)
  * **Link**: [https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/)
  * **Description**: The definitive architectural breakdown of message brokers vs event logs, delivery semantics, stream processing, and log-based storage engines.

* **Kafka: The Definitive Guide (2nd Edition)**
  * **Source**: Gwen Shapira, Todd Palino, Rajini Sivaram, & Krit Petty (O'Reilly Media)
  * **Link**: [https://www.oreilly.com/library/view/kafka-the-definitive/9781492043072/](https://www.oreilly.com/library/view/kafka-the-definitive/9781492043072/)
  * **Description**: Comprehensive technical reference covering Kafka topics, partitions, consumer groups, replication protocol, and production deployment tuning.

* **Enterprise Integration Patterns**
  * **Source**: Gregor Hohpe & Bobby Woolf (Addison-Wesley Professional)
  * **Link**: [https://www.enterpriseintegrationpatterns.com/](https://www.enterpriseintegrationpatterns.com/)
  * **Description**: The foundational blueprint catalog defining enterprise messaging patterns including Message Channels, Routers, Dead-Letter Channels, and Idempotent Receivers.

---

## 📄 Research Papers

* **Kafka: a Distributed Messaging System for Log Processing (2011)**
  * **Source**: Jay Kreps, Neha Narkhede, & Jun Rao (LinkedIn Corporation, ACM NetDB)
  * **Link**: [https://www.ingentaconnect.com/content/one/ez/2011/00000001/00000001/art00008](https://www.ingentaconnect.com/content/one/ez/2011/00000001/00000001/art00008)
  * **Description**: The original paper from LinkedIn introducing Apache Kafka as a high-throughput distributed commit log for real-time event streaming.

* **Queues Don't Fix Overload (2020)**
  * **Source**: Fred Hebert (Honeycomb Engineering / Stacks)
  * **Link**: [https://ferd.ca/queues-don-t-fix-overload.html](https://ferd.ca/queues-don-t-fix-overload.html)
  * **Description**: An insightful analysis explaining why queues only smooth out temporary traffic spikes and why unbounded queues inevitably lead to latency collapse.

* **AMQP 0-9-1 Model Architecture Specification**
  * **Source**: OASIS / AMQP Working Group
  * **Link**: [https://www.rabbitmq.com/amqp-0-9-1-reference.html](https://www.rabbitmq.com/amqp-0-9-1-reference.html)
  * **Description**: Formal technical specification detailing Advanced Message Queuing Protocol entities: exchanges, bindings, queues, channels, and framing.

---

## 🛠️ Engineering Blogs

* **The Log: What every software engineer should know about real-time data's unifying abstraction**
  * **Source**: Jay Kreps (LinkedIn Engineering Blog / Confluent)
  * **Link**: [https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying](https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying)
  * **Description**: Masterclass essay on why append-only distributed logs are the foundational core of distributed data systems, replication, and event-driven microservices.

* **Should You Use RabbitMQ or Apache Kafka?**
  * **Source**: Eran Stiller (Confluent Blog)
  * **Link**: [https://www.confluent.io/blog/kafka-vs-rabbitmq/](https://www.confluent.io/blog/kafka-vs-rabbitmq/)
  * **Description**: Objective comparison contrasting smart broker / dumb consumer routing (RabbitMQ) vs dumb broker / smart consumer log partitioning (Kafka).

* **What Every Developer Should Know About Exactly-Once Semantics in Apache Kafka**
  * **Source**: Neha Narkhede (Confluent Blog)
  * **Link**: [https://www.confluent.io/blog/exactly-once-semantics/](https://www.confluent.io/blog/exactly-once-semantics/)
  * **Description**: Technical explanation of transactional message delivery, idempotent producers, and sequence numbering in Apache Kafka.

---

## 🌐 Official Documentation

* **Apache Kafka Official Documentation**
  * **Source**: Apache Software Foundation
  * **Link**: [https://kafka.apache.org/documentation/](https://kafka.apache.org/documentation/)
  * **Description**: Complete specification of Kafka core concepts, configuration parameters, producer/consumer APIs, and operations guides.

* **RabbitMQ Core Concepts & Documentation**
  * **Source**: VMware Tanzu / Broadcom
  * **Link**: [https://www.rabbitmq.com/documentation.html](https://www.rabbitmq.com/documentation.html)
  * **Description**: Authoritative documentation covering exchanges, routing keys, publisher confirms, consumer acknowledgements, and clustering.

* **CloudEvents Specification (CNC)**
  * **Source**: Cloud Native Computing Foundation (CNCF)
  * **Link**: [https://cloudevents.io/](https://cloudevents.io/)
  * **Description**: Standard specification for describing event data in common formats to provide interoperability across messaging platforms.

---

## 🎥 Conference Talks

* **GOTO 2017 • The Many Meanings of Event-Driven Architecture**
  * **Source**: Martin Fowler (GOTO Conferences)
  * **Link**: [https://www.youtube.com/watch?v=STKCRSUsyP0](https://www.youtube.com/watch?v=STKCRSUsyP0)
  * **Description**: Clarifying key event-driven patterns: Event Notification, Event-Carried State Transfer, Event Sourcing, and CQRS.

* **Kafka and RabbitMQ: Comparing the Architectural Patterns**
  * **Source**: Tim Berglund (Confluent / Strange Loop)
  * **Link**: [https://www.youtube.com/watch?v=06iRM1Ghr1k](https://www.youtube.com/watch?v=06iRM1Ghr1k)
  * **Description**: Architectural deep dive contrasting queue-based work distribution with log-based event streaming.

---

## 📹 Videos

* **System Design: Message Queues & Event Streaming**
  * **Source**: ByteByteGo (Alex Xu)
  * **Link**: [https://www.youtube.com/watch?v=iJLL-256w44](https://www.youtube.com/watch?v=iJLL-256w44)
  * **Description**: Concise visual walkthrough comparing message queues, exchanges, and distributed log topics for system design interviews.

* **How Kafka Works: Topics, Partitions & Offsets**
  * **Source**: Confluent Developer Channel
  * **Link**: [https://www.youtube.com/watch?v=UEg40Te89E0](https://www.youtube.com/watch?v=UEg40Te89E0)
  * **Description**: Educational video series explaining topic partitioning, consumer group rebalancing, and offset management.
