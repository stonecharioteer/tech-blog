---
date: "2026-01-08T12:21:16+05:30"
draft: true
title: "Distributed Systems Learning Resources"
description: "Curated collection of books, papers, and articles for learning distributed systems and performance engineering"
tags:
  - "Distributed Systems"
  - "Performance Engineering"
  - "Learning"
---

A comprehensive collection of resources for learning distributed systems, performance engineering, and scalable system design.

## Books

### Distributed Systems & Databases

- Database Internals - Alex Petrov
- Designing Data-Intensive Applications - Martin Kleppmann
- High Performance Browser Networking - Ilya Grigorik
- Just Use Postgres! - Denis Magda
- Latency - Pekka Enberg

### Language-Centric

- Fluent Python - Lucian Ramalho
- Rust Atomics and Locks - Mara Bos
- Rust for Rustaceans - Jon Gjengset

### AI

I'm not focussing on learning AI skills specifically. For my learning I plan on
_avoiding_ AI altogether, at least coding agents.

- Build a Large Language Model (From Scratch) - Sebastian Raschka ( Low Priority
  )
- AI Engineering - Chip Huyen ( Low Priority )
- Designing Machine Learning Systems - Chip Huyen ( Low Priority )

## Python PEPs

I wanted to read some Python Enhancement Proposals that led to improved
concurrency in Python. These are what I have so far.

- [PEP 563 – Postponed Evaluation of Annotations](https://peps.python.org/pep-0563/)
- [PEP 649 – Deferred Evaluation Of Annotations Using Descriptors](https://peps.python.org/pep-0649/)
- [PEP 703 – Making the Global Interpreter Lock Optional in CPython](https://peps.python.org/pep-0703/)
- [PEP 734 – Multiple Interpreters in the Stdlib](https://peps.python.org/pep-0734/)
- [PEP 744 – JIT Compilation](https://peps.python.org/pep-0744/)
- [PEP 749 - Implementing PEP 649](https://peps.python.org/pep-0749/)
- [PEP 810 – Explicit lazy imports](https://peps.python.org/pep-0810/)
- [PEP 3156 - Asynchronous IO Support Rebooted: the "asyncio" Module](https://peps.python.org/pep-3156/)

## Blog Articles

- [Napkin Math](https://sirupsen.com/napkin/) - Back-of-the-envelope calculations for systems design

### Brendan Gregg - Performance Engineering

- [Linux Load Averages: Solving the Mystery](https://www.brendangregg.com/blog/2017-08-08/linux-load-averages.html)
- [CPU Utilization is Wrong](https://www.brendangregg.com/blog/2017-05-09/cpu-utilization-is-wrong.html)
- [Flame Graphs](https://www.brendangregg.com/flamegraphs.html)
- [Differential Flame Graphs](https://www.brendangregg.com/blog/2014-11-09/differential-flame-graphs.html)
- [BPF: A New Type of Software](https://www.brendangregg.com/blog/2019-12-02/bpf-a-new-type-of-software.html)
- [Give me 15 minutes and I'll change your view of Linux tracing](https://www.brendangregg.com/blog/2016-12-27/linux-tracing-in-15-minutes.html)
- [Learn eBPF Tracing: Tutorial and Examples](https://www.brendangregg.com/blog/2019-01-01/learn-ebpf-tracing.html)
- [Systems Performance: Enterprise and the Cloud, 2nd Edition](https://www.brendangregg.com/blog/2020-07-15/systems-performance-2nd-edition.html)
- [BPF Performance Tools: Linux System and Application Observability](https://www.brendangregg.com/blog/2019-07-15/bpf-performance-tools-book.html)

### Engineering Blogs

- [Building and Scaling Notion's Data Lake](https://www.notion.com/blog/building-and-scaling-notions-data-lake)
- [The Great Re-shard](https://www.notion.com/blog/the-great-re-shard)
- [Sharding Postgres at Notion](https://www.notion.com/blog/sharding-postgres-at-notion)

### Cloudflare Postmortems

- [Cloudflare outage on November 18, 2025](https://www.cloudflare.com/18-november-2025-outage/)
- [Cloudflare outage on December 5, 2025](https://www.cloudflare.com/5-december-2025-outage/)
- [Code Orange: Fail Small — our resilience plan following recent incidents](https://www.cloudflare.com/fail-small-resilience-plan/)

## Papers

{{< warning title="Uncurated List" >}}
This list hasn't been curated yet. I'll prune or strikethrough papers that I haven't found useful or won't read for my preparation.
{{< /warning >}}

### Essential Papers (Start Here)

1. [Time, clocks, and the ordering of events in a distributed system](https://doi.org/10.1145/359545.359563) - Leslie Lamport, 1978
2. [The Byzantine Generals Problem](https://doi.org/10.1145/357172.357176) - Leslie Lamport, Robert Shostak, and Marshall Pease, 1982
3. [Distributed snapshots: determining global states of distributed systems](https://doi.org/10.1145/214451.214456) - K. Mani Chandy and Leslie Lamport, 1985
4. [Impossibility of distributed consensus with one faulty process](https://doi.org/10.1145/3149.214121) - Michael J. Fischer, Nancy A. Lynch, and Michael S. Paterson, 1985
5. [Viewstamped Replication: A New Primary Copy Method to Support Highly-Available Distributed Systems](https://doi.org/10.1145/62546.62549) - Brian M. Oki and Barbara H. Liskov, 1988
6. [The part-time parliament (Paxos)](https://doi.org/10.1145/279227.279229) - Leslie Lamport, 1998
7. [Paxos Made Simple](https://www.microsoft.com/en-us/research/publication/paxos-made-simple/) - Leslie Lamport, 2001
8. [Bitcoin: A Peer-to-Peer Electronic Cash System](https://bitcoin.org/en/bitcoin-paper) - Satoshi Nakamoto, 2008
9. [Conflict-free replicated data types](https://dl.acm.org/doi/10.5555/2050613.2050642) - Marc Shapiro, Nuno Preguiça, Carlos Baquero, and Marek Zawirski, 2011
10. [In search of an understandable consensus algorithm (Raft)](https://dl.acm.org/doi/10.5555/2643634.2643666) - Diego Ongaro and John Ousterhout, 2014

### Comprehensive Reading List

#### System Design Principles

- [Harvest, Yield and Scalable Tolerant Systems](https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.33.411)
- [On Designing and Deploying Internet Scale Services](https://mvdirona.com/jrh/talksAndPapers/JamesRH_Lisa.pdf)
- [The Perils of Good Abstractions](https://web.archive.org/web/20181006111158/http://www.addsimplicity.com/adding_simplicity_an_engi/2006/12/the_perils_of_g.html)
- [Chaotic Perspectives](https://web.archive.org/web/20180821164750/http://www.addsimplicity.com/adding_simplicity_an_engi/2007/05/chaotic_perspec.html)
- [Data on the Outside versus Data on the Inside](http://cidrdb.org/cidr2005/papers/P12.pdf)
- [Memories, Guesses and Apologies](https://channel9.msdn.com/Shows/ARCast.TV/ARCastTV-Pat-Helland-on-Memories-Guesses-and-Apologies)
- [SOA and Newton's Universe](https://web.archive.org/web/20190719121913/https://blogs.msdn.microsoft.com/pathelland/2007/05/20/soa-and-newtons-universe/)
- [Building on Quicksand](https://arxiv.org/abs/0909.1788)
- [Why Distributed Computing?](https://www.artima.com/weblogs/viewpost.jsp?thread=4247)
- [A Note on Distributed Computing](https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.41.7628)
- [Stevey's Google Platforms Rant](https://web.archive.org/web/20190319154842/https://plus.google.com/112678702228711889851/posts/eVeouesvaVX)

#### Latency

- [Latency Exists, Cope!](https://web.archive.org/web/20181004043647/http://www.addsimplicity.com/adding_simplicity_an_engi/2007/02/latency_exists_.html)
- [Latency - the new web performance bottleneck](https://www.igvita.com/2012/07/19/latency-the-new-web-performance-bottleneck/)
- [Patterson](http://dl.acm.org/citation.cfm?id=1022596)
- [The Tail At Scale](https://research.google/pubs/pub40801/)

#### Amazon Systems

- [A Conversation with Werner Vogels](https://queue.acm.org/detail.cfm?id=1142065)
- [Discipline and Focus](https://queue.acm.org/detail.cfm?id=1388773)
- [Vogels on Scalability](https://web.archive.org/web/20130729204944id_/http://itc.conversationsnetwork.org/shows/detail1634.html)
- [SOA creates order out of chaos @ Amazon](http://searchwebservices.techtarget.com/originalContent/0,289142,sid26_gci1195702,00.html)

#### Google Systems

- [MapReduce](https://research.google/pubs/pub62/)
- [Chubby Lock Manager](https://research.google/pubs/pub27897/)
- [Google File System](https://research.google/pubs/pub51/)
- [BigTable](https://research.google/pubs/pub27898/)
- [Data Management for Internet-Scale Single-Sign-On](https://www.usenix.org/legacy/event/worlds06/tech/prelim_papers/perl/perl.pdf)
- [Dremel: Interactive Analysis of Web-Scale Datasets](https://research.google/pubs/pub36632/)
- [Large-scale Incremental Processing Using Distributed Transactions and Notifications](https://research.google/pubs/pub36726/)
- [Megastore: Providing Scalable, Highly Available Storage for Interactive Services](http://cidrdb.org/cidr2011/Papers/CIDR11_Paper32.pdf)
- [Spanner](https://research.google/pubs/pub39966/)
- [Photon](https://research.google/pubs/pub41318/)
- [Mesa: Geo-Replicated, Near Real-Time, Scalable Data Warehousing](https://research.google/pubs/pub42851/)

#### Consistency Models

- [CAP Conjecture](https://web.archive.org/web/20190629112250/https://www.glassbeam.com/sites/all/themes/glassbeam/images/blog/10.1.1.67.6951.pdf)
- [Consistency, Availability, and Convergence](https://www.cs.utexas.edu/users/dahlin/papers/cac-tr.pdf)
- [CAP Twelve Years Later: How the "Rules" Have Changed](https://www.infoq.com/articles/cap-twelve-years-later-how-the-rules-have-changed)
- [Consistency and Availability](https://www.infoq.com/news/2008/01/consistency-vs-availability)
- [Eventual Consistency](https://www.allthingsdistributed.com/2007/12/eventually_consistent.html)
- [Avoiding Two-Phase Commit](https://web.archive.org/web/20180821165044/http://www.addsimplicity.com/adding_simplicity_an_engi/2006/12/avoiding_two_ph.html)
- [2PC or not 2PC, Wherefore Art Thou XA?](https://web.archive.org/web/20180821164931/http://www.addsimplicity.com/adding_simplicity_an_engi/2006/12/2pc_or_not_2pc_.html)
- [Life Beyond Distributed Transactions](https://docs.microsoft.com/en-us/archive/blogs/pathelland/link-to-quotlife-beyond-distributed-transactions-an-apostates-opinion)
- [If you have too much data, then 'good enough' is good enough](https://queue.acm.org/detail.cfm?id=1988603)
- [Starbucks doesn't do two phase commit](https://www.enterpriseintegrationpatterns.com/docs/IEEE_Software_Design_2PC.pdf)
- [You Can't Sacrifice Partition Tolerance](https://codahale.com/you-cant-sacrifice-partition-tolerance/)
- [Optimistic Replication](https://www.hpl.hp.com/techreports/2002/HPL-2002-33.pdf)

#### Theory

- [Distributed Computing Economics](https://arxiv.org/pdf/cs/0403019.pdf)
- [Rules of Thumb in Data Engineering](https://www.microsoft.com/en-us/research/publication/rules-of-thumb-in-data-engineering/)
- [Fallacies of Distributed Computing](https://en.wikipedia.org/wiki/Fallacies_of_distributed_computing)
- [Coordinated Attack or Two Generals Problem](https://en.wikipedia.org/wiki/Two_Generals%27_Problem)
- [Unreliable Failure Detectors for Reliable Distributed Systems](https://www.cs.utexas.edu/~lorenzo/corsi/cs380d/papers/p225-chandra.pdf)
- [Virtual Time and Global States of Distributed Systems](https://pages.cs.wisc.edu/~remzi/Classes/739/Fall2016/Papers/mattern89.pdf)
- [Practical uses of synchronized clocks in distributed systems](https://muratbuffalo.blogspot.com/2022/11/practical-uses-of-synchronized-clocks.html)
- [Lazy Replication: Exploiting the Semantics of Distributed Services](https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.17.469)
- [Scalable Agreement - Towards Ordering as a Service](https://www.usenix.org/legacy/event/hotdep10/tech/full_papers/Kapritsos.pdf)
- [Scalable Eventually Consistent Counters over Unreliable Networks](https://arxiv.org/pdf/1307.3207v1.pdf)

**Expository and Tutorial Resources:**
- [There is No Now](https://queue.acm.org/detail.cfm?id=2745385) - Justin Sheehy, ACM Queue 2015
- [Why Logical Clocks are Easy](https://queue.acm.org/detail.cfm?id=2917756) - Carlos Baquero and Nuno Preguiça, ACM Queue 2016
- [Hybrid logical clocks](http://muratbuffalo.blogspot.com/2014/07/hybrid-logical-clocks.html) - Murat Buffalo blog
- [Logical clocks and Vector clocks modeling in TLA+/PlusCal](http://muratbuffalo.blogspot.com/2018/01/logical-clocks-and-vector-clocks.html) - Murat Buffalo blog
- [A Brief Tour of FLP Impossibility](http://the-paper-trail.org/blog/a-brief-tour-of-flp-impossibility/) - Paper Trail blog
- [Paper summary: Perspectives on the CAP theorem](http://muratbuffalo.blogspot.com/2015/02/paper-summary-perspectives-on-cap.html) - Murat Buffalo blog

#### Languages and Tools

- [Programming Distributed Erlang Applications: Pitfalls and Recipes](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.137.9417&rep=rep1&type=pdf)

#### Infrastructure

- [Principles of Robust Timing over the Internet](https://queue.acm.org/detail.cfm?id=1773943)

#### Distributed Storage

- [Consistent Hashing and Random Trees](https://www.akamai.com/us/en/multimedia/documents/technical-publication/consistent-hashing-and-random-trees-distributed-caching-protocols-for-relieving-hot-spots-on-the-world-wide-web-technical-publication.pdf)
- [Amazon's Dynamo Storage Service](https://www.allthingsdistributed.com/2007/10/amazons_dynamo.html)

#### Consensus and Replication

- [Implementing Fault-Tolerant Services Using the State Machine Approach](https://www.cs.cornell.edu/fbs/publications/smsurvey.pdf)
- [How to build a highly available system with consensus](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.61.8330&rep=rep1&type=pdf)
- [Paxos Made Live - An Engineering Perspective](https://static.googleusercontent.com/media/research.google.com/en/us/archive/paxos_made_live.pdf)
- [Paxos Made Moderately Complex](https://www.cs.cornell.edu/courses/cs7412/2011sp/paxos.pdf)
- [Revisiting the Paxos Algorithm](https://groups.csail.mit.edu/tds/paxos.html)
- [Consensus in the Cloud: Paxos Systems Demystified](https://cse.buffalo.edu/tech-reports/2016-02.orig.pdf)
- [Flexible Paxos: Quorum intersection revisited](https://arxiv.org/abs/1608.06696)
- [Practical Byzantine Fault Tolerance](http://pmg.csail.mit.edu/papers/osdi99.pdf)
- [Chain Replication for Supporting High Throughput and Availability](https://www.cs.cornell.edu/home/rvr/papers/OSDI04.pdf)
- [ZooKeeper: Wait-free coordination for Internet-scale systems](https://www.usenix.org/legacy/event/atc10/tech/full_papers/Hunt.pdf)
- [Tango: Distributed Data Structures over a Shared Log](https://dl.acm.org/doi/10.1145/2517349.2522732)
- [There is more consensus in Egalitarian parliaments](https://dl.acm.org/doi/10.1145/2517349.2517350)
- [Mencius: Building Efficient Replicated State Machines for WANs](https://www.usenix.org/legacy/event/osdi08/tech/full_papers/mao/mao_html/)
- [Reconfiguring a State Machine](https://www.microsoft.com/en-us/research/publication/reconfiguring-a-state-machine/)
- [WormSpace: A modular foundation for simple, verifiable distributed systems](https://flint.cs.yale.edu/flint/publications/socc19.pdf)

**Expository and Tutorial Resources:**
- [Modeling Paxos and Flexible Paxos in Pluscal and TLA+](http://muratbuffalo.blogspot.com/2016/11/modeling-paxos-and-flexible-paxos-in.html) - Murat Buffalo blog
- [Dissecting performance bottlenecks of Paxos protocols](http://muratbuffalo.blogspot.com/2019/07/dissecting-performance-bottlenecks-of.html) - Murat Buffalo blog

#### Gossip Protocols and Epidemic Algorithms

- [How robust are gossip-based communication protocols?](https://infoscience.epfl.ch/record/109302?ln=en)
- [Astrolabe: A Robust and Scalable Technology For Distributed Systems Monitoring, Management, and Data Mining](https://www.cs.cornell.edu/home/rvr/papers/astrolabe.pdf)
- [Epidemic Computing at Cornell](https://www.allthingsdistributed.com/historical/archives/000456.html)
- [Fighting Fire With Fire: Using Randomized Gossip To Combat Stochastic Scalability Limits](https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.5.4000)
- [Bi-Modal Multicast](https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.17.7959)
- [ACM SIGOPS Operating Systems Review - Gossip-based computer networking](https://dl.acm.org/toc/sigops/2007/41/5)
- [SWIM: Scalable Weakly-consistent Infection-style Process Group Membership Protocol](https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.18.9737)

#### Peer-to-Peer Systems

- [Chord: A Scalable Peer-to-peer Lookup Protocol for Internet Applications](https://pdos.csail.mit.edu/papers/ton:chord/paper-ton.pdf)
- [Kademlia: A Peer-to-peer Information System Based on the XOR Metric](https://pdos.csail.mit.edu/~petar/papers/maymounkov-kademlia-lncs.pdf)
- [Pastry: Scalable, decentralized object location and routing for large-scale peer-to-peer systems](https://rowstron.azurewebsites.net/PAST/pastry.pdf)
- [PAST: A large-scale, persistent peer-to-peer storage utility](http://research.microsoft.com/en-us/um/people/antr/PAST/hotos.pdf)
- [SCRIBE: A large-scale and decentralised application-level multicast infrastructure](https://rowstron.azurewebsites.net/PAST/jsac.pdf)

#### Distributed Algorithms

- [Self-stabilizing systems in spite of distributed control](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.93.314&rep=rep1&type=pdf)
- [The Drinking Philosophers Problem](https://www.cs.utexas.edu/users/misra/scannedPdf.dir/DrinkingPhil.pdf)
- [Sparse partitions](http://courses.csail.mit.edu/6.895/fall02/papers/Awerbuch/focs90.pdf)
- [Distributed reset](http://web.cse.ohio-state.edu/siefast/group/publications/distributed-reset.pdf)
- [The Arrow Distributed Directory Protocol](http://cs.brown.edu/people/mph/DemmerH98/disc.pdf)

**Expository and Tutorial Resources:**
- [Dijkstra's stabilizing token ring algorithm](http://muratbuffalo.blogspot.com/2015/01/dijkstras-stabilizing-token-ring.html) - Murat Buffalo blog
- [Modeling the hygienic dining philosophers algorithm in TLA+](http://muratbuffalo.blogspot.com/2016/11/hygienic-dining-philosophers.html) - Murat Buffalo blog

#### System Design and Architecture

- [Hints for computer system design](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/acrobat-17.pdf)
- [The role of distributed state](https://courses.cs.washington.edu/courses/cse552/07sp/papers/distributed_state.pdf)
- [SEDA: An Architecture for Well-Conditioned, Scalable Internet Services](http://www.sosp.org/2001/papers/welsh.pdf)
- [Crash only software](http://usenix.org/events/hotos03/tech/full_papers/candea/candea.pdf)

**Expository and Tutorial Resources:**
- [Learning about distributed systems: where to start?](http://muratbuffalo.blogspot.com/2020/06/learning-about-distributed-systems.html) - Murat Buffalo blog

#### Cloud Computing and Big Data

- [Lessons from Giant-Scale Services](https://courses.cs.washington.edu/courses/cse454/05sp/papers/GiantScale-IEEE.pdf)
- [Consistency Analysis in Bloom: a CALM and Collected Approach](https://people.ucsc.edu/~palvaro/cidr11.pdf)
- [Resilient Distributed Datasets (Spark)](https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final138.pdf)
- [TensorFlow: A System for Large-Scale Machine Learning](https://www.usenix.org/conference/osdi16/technical-sessions/presentation/abadi)
- [Above the Clouds: A Berkeley View of Cloud Computing](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2009/EECS-2009-28.pdf)
- [Cloud Programming Simplified: A Berkeley View on Serverless Computing](https://arxiv.org/abs/1902.03383)
