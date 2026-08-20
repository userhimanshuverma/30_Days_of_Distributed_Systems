# Day 25 — References & Further Reading: Service Discovery

This document contains curated, authoritative primary sources, foundational research papers, production engineering articles, official documentation, and technical talks on **Service Discovery, Service Registries, DNS-based Discovery, Kubernetes Networking, Dynamic Routing, Health Checking, and Ephemeral Infrastructure**.

---

## 📚 Books

* **Designing Distributed Systems: Patterns and Paradigms for Scalable, Reliable Services**
  * **Source**: Brendan Burns (O'Reilly Media, Chapter 9: Ambassador Pattern & Chapter 10: Service Discovery)
  * **Link**: [https://www.oreilly.com/library/view/designing-distributed-systems/9781491983638/](https://www.oreilly.com/library/view/designing-distributed-systems/9781491983638/)
  * **Description**: Foundational breakdown by Kubernetes co-founder on why ephemeral container lifecycles require dynamic service discovery registries and sidecar ambassador proxies.

* **Kubernetes: Up and Running (3rd Edition)**
  * **Source**: Brendan Burns, Joe Beda, Kelsey Hightower, and Lachlan Evenson (O'Reilly Media, Chapter 5: Services & Chapter 15: Service Discovery)
  * **Link**: [https://www.oreilly.com/library/view/kubernetes-up-and/9781098110192/](https://www.oreilly.com/library/view/kubernetes-up-and/9781098110192/)
  * **Description**: Definitive guide on Kubernetes Services, kube-proxy, CoreDNS service resolution, Virtual IPs (ClusterIP), and endpoints tracking.

* **Microservices Patterns: With examples in Java**
  * **Source**: Chris Richardson (Manning Publications, Chapter 3: Interprocess Communication in a Microservice Architecture — Service Discovery Pattern)
  * **Link**: [https://www.manning.com/books/microservices-patterns](https://www.manning.com/books/microservices-patterns)
  * **Description**: Comprehensive analysis contrasting client-side discovery patterns with server-side discovery routers and self-registration lifecycles.

---

## 📄 Research Papers & Standards

* **Domain Names - Concepts and Facilities (RFC 1034) & Implementation and Specification (RFC 1035)**
  * **Source**: P. Mockapetris (Internet Engineering Task Force - IETF RFC 1034 / RFC 1035)
  * **Link**: [https://www.rfc-editor.org/rfc/rfc1034](https://www.rfc-editor.org/rfc/rfc1034)
  * **Description**: The foundational Internet standard establishing hierarchical name resolution, domain tree structure, and resource record caching principles.

* **A DNS RR for specifying the location of services (DNS SRV - RFC 2782)**
  * **Source**: A. Gulbrandsen, P. Vixie, L. Esibov (IETF RFC 2782)
  * **Link**: [https://www.rfc-editor.org/rfc/rfc2782](https://www.rfc-editor.org/rfc/rfc2782)
  * **Description**: The official standard for locating network services via DNS SRV records specifying symbolic service names, protocols, ports, and priorities.

* **Large-scale cluster management at Google with Borg (2015)**
  * **Source**: Abhishek Verma, Luis Pedrosa, Madhukar Korupolu, David Oppenheimer, Eric Tune, John Wilkes (ACM EuroSys '15)
  * **Link**: [https://research.google/pubs/pub43438/](https://research.google/pubs/pub43438/)
  * **Description**: Seminal paper detailing Google's Borg Name Service (BNS), which laid the architectural groundwork for modern container service discovery in Kubernetes.

---

## 🛠️ Engineering Blogs & Primary Case Studies

* **Eureka! Why You Shouldn't Hardcode IP Addresses in Microservices**
  * **Source**: Netflix TechBlog (Karthik Rangarajan)
  * **Link**: [https://netflixtechblog.com/eureka-service-discovery-in-the-netflix-cloud-1b4e5bb02e7a](https://netflixtechblog.com/eureka-service-discovery-in-the-netflix-cloud-1b4e5bb02e7a)
  * **Description**: Landmark article explaining why Netflix built an AP (available/partition-tolerant) client-side service registry to handle dynamic AWS EC2 autoscaling.

* **How Airbnb Uses SmartStack for Automated Service Discovery**
  * **Source**: Airbnb Engineering & Data Science (Igor Serebryany)
  * **Link**: [https://medium.com/airbnb-engineering/smartstack-service-discovery-in-the-cloud-4b8bac0e0d08](https://medium.com/airbnb-engineering/smartstack-service-discovery-in-the-cloud-4b8bac0e0d08)
  * **Description**: Deep dive into Airbnb's Nerve and Synapse architecture, combining ZooKeeper with local HAProxy sidecars for zero-downtime service registration.

* **An Illustrated Guide to Kubernetes Networking**
  * **Source**: Tim Hockin (Kubernetes Networking SIG & Google Cloud Blog)
  * **Link**: [https://cloud.google.com/blog/products/containers-kubernetes/an-illustrated-guide-to-kubernetes-networking-part-1](https://cloud.google.com/blog/products/containers-kubernetes/an-illustrated-guide-to-kubernetes-networking-part-1)
  * **Description**: Visual, rigorous breakdown of how Kubernetes assigns IP addresses to Pods, routes through Services via iptables/IPVS, and resolves DNS queries.

* **Under the Hood of Consul: Gossip Protocol & Raft Consensus**
  * **Source**: HashiCorp Engineering Blog (Armon Dadgar)
  * **Link**: [https://www.hashicorp.com/blog/consul-announcement](https://www.hashicorp.com/blog/consul-announcement)
  * **Description**: Original design document detailing how Consul pairs Serf gossip protocols for failure detection with Raft consensus for strongly consistent service registration.

---

## 🌐 Official Documentation

* **Kubernetes Documentation: Service Concept & Virtual IPs**
  * **Source**: Kubernetes Official Documentation
  * **Link**: [https://kubernetes.io/docs/concepts/services-networking/service/](https://kubernetes.io/docs/concepts/services-networking/service/)
  * **Description**: Authoritative documentation detailing Kubernetes ClusterIP, NodePort, LoadBalancer service abstractions, and selector-based EndpointSlices.

* **Kubernetes Documentation: DNS for Services and Pods**
  * **Source**: Kubernetes Official Documentation
  * **Link**: [https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
  * **Description**: Official reference on CoreDNS naming syntax (`<service-name>.<namespace>.svc.cluster.local`), SRV records, and search domains.

* **HashiCorp Consul Documentation: Service Discovery Overview**
  * **Source**: HashiCorp Consul Documentation
  * **Link**: [https://developer.hashicorp.com/consul/docs/discovery](https://developer.hashicorp.com/consul/docs/discovery)
  * **Description**: Core guide on registering service instances, health checking protocols (HTTP, TCP, gRPC, TTL), and querying the Consul catalog via DNS or HTTP API.

---

## 🎥 Conference Talks

* **GOTO 2018 • Service Discovery and Dynamic Routing in Modern Microservices**
  * **Source**: GOTO Conferences (Christian Posta)
  * **Link**: [https://www.youtube.com/watch?v=16fgzklcF7Y](https://www.youtube.com/watch?v=16fgzklcF7Y)
  * **Description**: High-impact talk explaining the transition from static DNS and hardware load balancers to dynamic registries and dynamic sidecar service proxies.

* **KubeCon + CloudNativeCon • CoreDNS: Under the Hood of Kubernetes DNS**
  * **Source**: CNCF / Linux Foundation (John Belamaric & Yong Tang)
  * **Link**: [https://www.youtube.com/watch?v=iR5n_q19cM4](https://www.youtube.com/watch?v=iR5n_q19cM4)
  * **Description**: Technical deep dive into CoreDNS plugin architecture, cluster DNS caching, latency trade-offs, and scaling internal DNS queries.

---

## 📹 Videos

* **Service Discovery in Microservices Explained**
  * **Source**: ByteByteGo (Alex Xu)
  * **Link**: [https://www.youtube.com/watch?v=6b8n7eWdJzQ](https://www.youtube.com/watch?v=6b8n7eWdJzQ)
  * **Description**: Visual primer breaking down Client-Side Discovery vs. Server-Side Discovery, heartbeats, and service registry synchronization.

* **How Kubernetes Service Networking Actually Works**
  * **Source**: That DevOps Guy (Nana Janashia)
  * **Link**: [https://www.youtube.com/watch?v=0Omvgd7Hg1k](https://www.youtube.com/watch?v=0Omvgd7Hg1k)
  * **Description**: Clear step-by-step visual demonstration of how ClusterIP stable addresses route traffic to ephemeral Pod IPs behind the scenes.
