---
date: "2026-03-27T15:45:03+05:30"
title: "What Was I Reading Last? In Three Not-So-Easy Pieces"
description:
  "Syncing reading progress across devices sounds simple until you try it.
  Discovery, sync, and conflict resolution — with and without a cloud."
tags:
  - "merrilin"
  - "distributed-systems"
  - "android"
  - "local-first"
  - "peer-to-peer"
---

When I began building Merrilin, I wanted to solve a deeply personal problem. I
use multiple devices, and wanted to sync files, progress and annotations between
them.

I used KoReader until Feb 2025, and I relied on SyncThing to sync my files,
WebDav with Koofr for my reading progress, and koReader's cloud instance for
file progress. That felt like a lot of work for getting what should be a simple
feature working.

I didn't like it though. It was really messy, and the data felt very divided. Of
course, with my initial build of the android app, sync worked fine. Login to
Merrilin's cloud offering, and your files, progress and annotations are synced
perfectly.

But what if we don't want to sync to a cloud?

When we began designing the UX of the offline-mode app, I wanted sync to work
flawlessly. I'd seen it work fairly well with apps such as SyncThing, and I knew
that peer-to-peer sync should definitely possible over LAN. I didn't know the
specifics yet, but I had a laundry-list of items:

- I should be able to pair any number of devices over a local network.
- Once paired, devices should be able to survive changes in IP or the network
  itself.
- These sync features should not rely on a cloud or self-hosted instance.
- I should be able to sync files, progress, annotations (bookmarks and
  highlights) across devices.
- I should be able to sign into Merrilin's cloud instance after having read for
  a bit on any number of devices and have my local data sync to the cloud
  instance as well.
- I should be able to continue reading books locally without uploading the files
  themselves to the cloud, to preserve my credits.

These feel like small features, and I had some gumption of how severe they were
going to be, but I had no real idea.

![The PR diff stats](/images/posts/merrilin/tech/pr-diff-stats.png)

That's what my last 3 weeks ended up looking like.

Truth be told, if someone made this PR at work, I'd probably advocate for
getting them away from their AI accounts.

I had my work cut out for me, first, the original android app was a Capacitor
scaffolding over the website. It worked well, until it didn't and was not
testable. The web had code in `if-else` blocks that was mobile specific, and
vice-versa.

This feature ended up being a fun distributed systems problem that I had fun
building. There's a lot to write about the work that went on for building out
this entire PR, but in this post, I want to focus on the peer sync and how it
works both with and without the cloud.

## Two Lanes

Merrilin has two sync lanes, and everything in this post flows from that split.

The **guest-peer lane** is for devices that aren't signed in to anything. Two
Android phones on the same WiFi, no accounts, no internet. Local SQLite is the
source of truth. Sync happens directly between devices over the local network.

The **account-cloud lane** is for signed-in devices. The cloud PostgreSQL
instance is the source of truth. Devices write to a local outbox and flush to
the server. The server pushes updates back via polling or WebSocket.

![The two sync lanes](/images/posts/merrilin/tech/two-lanes.png)

Both lanes sync the same data: reading positions, annotations, reading events,
book metadata, and collections. Both use the same local SQLite database as their
working copy. The difference is where the data goes next, to a peer on your WiFi
or to a server over the internet, and who gets the final say when there's a
conflict.

A device starts in the guest lane. If you sign in, it switches to the cloud
lane. Your local data doesn't disappear, it gets replayed through the cloud's
ingest endpoints. More on that later.

Book _files_ are handled separately in both lanes. In the guest lane, you can
fetch a book from a paired device on demand. In the cloud lane, uploading a book
is optional. Your reading data syncs by file hash alone, even without the file
on the server. This means you can track progress across all your devices without
spending cloud storage on every book.

## Discovery and Pairing

The first problem to solve was how do 2 devices on the same network discover
each other. I use SyncThing and LocalSend a lot, and I liked how they do that.

When you launch Merrilin on one device and decide to use it locally without
signing into the cloud, it does two things in the background.

{{< info title="What is mDNS?" >}} mDNS (Multicast DNS) is a protocol that lets
devices find each other on a local network without a central DNS server. When
your printer shows up on your laptop without any configuration, that's mDNS.
Devices announce themselves by broadcasting a service name and port to everyone
on the same WiFi segment. Android exposes this through NSD (Network Service
Discovery). {{< /info >}}

**Advertising**: the app announces itself on the local network using mDNS with a
custom service type (`_merrilin-sync._tcp.`). This is the same protocol a
printer would use to show up on the laptop without any configuration.

**Browsing**: simultaneously, the app also listens for the same announcements
from other devices. When another device _advertises_ on the network, the app
gets a `peerDiscovered` event with the other device's chosen label, address and
identity fingerprints.

This works over your local WiFi. mDNS works by multicast on local WiFi segment.

![Discovery and pairing flow](/images/posts/merrilin/tech/discovery-pairing.png)

Next, while discovery is first step, you need to pair your devices to _trust_
them. Just discovering a device on the network that advertises on the same port
and with the same service type doesn't mean that we trust it.

You can easily pair two devices running Merrilin using a QR Code and a 6-digit
key. Internally, the two devices exchange and store each other's identity
fingerprint and a shared secret. From that point on, they trust and recognize
each other, even if the IP addresses change, even on a different WiFi network.
The fingerprint is a stable identity, not the network address. mDNS just helps
them find themselves all over again if the address changes. This way, even if
another device gets that IP address and tries to spoof this, one device won't
confuse it for another.

{{< tip title="The SSH Analogy" >}} If you've ever SSH'd into a server for the
first time, you've seen "The authenticity of host X can't be established."
Merrilin's pairing works the same way. First connection: verify out-of-band (QR
code or pairing code). Every subsequent connection: the stored fingerprint must
match. If it doesn't, the peer is deactivated, just like SSH's "WARNING: REMOTE
HOST IDENTIFICATION HAS CHANGED." This is called Trust-On-First-Use (TOFU).
{{< /tip >}}

The coolest thing was that this was mentally similar to SSH. At first
connection, we verify out-of-band. Every subsequent connection requires the
stored fingerprint to match. If it doesn't the peer is deactivated, just like
how SSH tells you: "WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED."

## The Sync Protocol

The two lanes sync differently, but they move the same data.

### Guest-Peer Sync

Once two devices are paired, syncing is almost trivial. It's one HTTP request
per peer, per round.

{{< info title="What is a watermark?" >}} In sync protocols, a watermark (or
cursor) is a bookmark that tracks "I've seen everything up to this point." It's
usually a timestamp or a sequence number. When Device A tells Device B its
watermark, B knows exactly which changes A is missing and only sends those. This
avoids re-sending the entire dataset every time. {{< /info >}}

Device A connects to Device B and says: "Here's everything that changed on my
side since last we talked, and here's my watermark so you know where I left
off." Device B looks at that watermark, gathers everything A is missing, and
sends it back, along with its own watermark. Both sides merge what they received
and advance their watermarks.

In one bidirectional round-trip, both devices are fully caught up.

![Peer sync round](/images/posts/merrilin/tech/peer-sync-round.png)

The key design choice is that Device A sends its own data _inside the request_,
not as a separate step. In a manner it's just "here are my updates, give me
yours." Both directions travel in a single `POST`. This matters on a phone where
you want to minimize how long the radio stays active.

### Account-Cloud Sync

The cloud lane works differently. It's not a bidirectional exchange, it's two
separate flows.

{{< info title="What is the Outbox Pattern?" >}} The outbox pattern is a
technique from microservices architecture. Instead of sending data directly to a
remote server (which might be down), you write it to a local queue first. A
background process drains the queue when the network is available. This gives
you instant local writes and reliable eventual delivery, even across app
restarts and network outages. {{< /info >}}

**Writing up**: the device saves every action to a local outbox first, then
flushes to the server in batches. The outbox is prioritized, reading position
updates go first, reading events can wait. A debounce timer collapses rapid page
turns into a single sync. If the network is down, the outbox just grows until it
can flush.

**Reading down**: the device polls the server for new events since its last
cursor, or gets a push via WebSocket. When a remote update arrives, it goes
through conflict resolution before being applied to the local SQLite.

![Cloud sync flow](/images/posts/merrilin/tech/cloud-sync.png)

The outbox pattern means the UI never waits for the network. You turn a page,
the local database updates instantly, the UI reflects it, and the cloud catches
up in the background. If you close the app before the flush happens, an Android
WorkManager job picks it up later.

### What Both Lanes Carry

The manifest, the payload that moves in both lanes, contains:

- Reading positions for every book (chapter, page, percentage, the position
  locator)
- Annotations (highlights and bookmarks, including soft-deletes)
- Reading events (how long we dwell on a page, reading speed)
- Book metadata (titles, authors - so a book that exists only on the other
  device still has a name)
- Availability (which book files the device actually has, so the other side can
  show a `Fetch` button)
- Collections (series groupings and their ordering)

Each is keyed by file hash, not by any internal ID. The same EPUB on two devices
produces the same `SHA-256` hash, so both sides know they're talking about the
same book without any central registry.

## Security Without a CA

This section is about the guest-peer lane specifically. The cloud lane uses
normal HTTPS with JWT authentication, nothing unusual there. The peer lane is
the interesting one.

This is peer-to-peer over WiFi. There's no certificate authority, no TLS cert
from Let's Encrypt, no server I control in between. So how do you run HTTPS
between two phones?

{{< info title="What is mTLS?" >}} Regular TLS (what HTTPS uses) is one-sided:
the server proves its identity to the client, but the client is anonymous.
Mutual TLS (mTLS) means both sides present certificates and verify each other.
It's commonly used in service-to-service communication in microservices, but
here we're using it between two phones. The "mutual" part is what makes it work
without a central server, both devices authenticate simultaneously.
{{< /info >}}

Each device generates a self-signed X.509 certificate and stores it in Android's
Keystore. When two devices connect, they use mutual TLS, both sides present
their certificates. The trust doesn't come from a CA chain, it comes from the
pairing step. When you scanned that QR code or entered the pairing code, both
devices stored each other's certificate fingerprint. Every subsequent connection
checks: does this certificate match what I stored during pairing?

On top of mTLS, every sync request is signed with the shared secret from
pairing. The signature covers the HTTP method, path, timestamp, a nonce, and a
hash of the request body. This means even if someone on your WiFi could somehow
intercept the TLS connection, they couldn't forge a valid request without the
shared secret.

{{< warning title="Fail Hard" >}} If anything fails, the fingerprint doesn't
match, the signature is wrong, the certificate changed, the peer gets
deactivated immediately. No silent fallback, no retry. You have to re-pair
manually. I'd rather be annoying than insecure. {{< /warning >}}

## Conflict Resolution

This is where the distributed systems part gets interesting. Two devices, both
offline, both reading, both making highlights. When they sync, whose data wins?

The answer depends on which lane you're in and what kind of data it is.

### In the Guest-Peer Lane

Peers are equals. Neither device is authoritative. Conflicts are resolved using
timestamps from a Hybrid Logical Clock.

{{< info title="What is a Hybrid Logical Clock (HLC)?" >}} A Hybrid Logical
Clock combines a physical wall-clock timestamp with a logical counter. Plain
wall clocks drift between devices, and pure logical clocks (like Lamport clocks)
lose track of real time. An HLC stays close to wall-clock time while still
guaranteeing a consistent ordering even when device clocks are slightly off.
CockroachDB and YugabyteDB use HLCs internally for the same reason.
{{< /info >}}

**Reading position**: most recent HLC timestamp wins. This works because you can
only actively read on one device at a time. If your phone says chapter 12 and
your tablet says chapter 8, and the phone's timestamp is newer, you're at
chapter 12.

**Annotations**: also HLC, but per-annotation. If you highlight a passage on
your phone and a different passage on your tablet, both survive. They merge as a
union. Deletes are soft-deletes with their own timestamp, so they propagate too.

**Reading events**: append-only. They're immutable facts: "I spent 45 seconds on
this page." No conflict is possible. Both sides accumulate events, and
duplicates get filtered by ID.

**Book metadata**: real titles always beat placeholders. When a peer tells you
about a book you don't have locally, a placeholder entry gets created. When the
actual title arrives later, it wins regardless of timestamps.

**Collections**: create-or-update. Newer edit wins for names. Books from both
sides end up in the collection.

One deliberate choice: deletions don't propagate between peers. If you remove a
book from one device, it stays on the other. In a system with no central
authority, I didn't want one device's cleanup to erase another device's library.

Book files also don't sync automatically. You see the other device has a book,
with its title and cover, but actually fetching the file is a deliberate action.
The fetch verifies the SHA-256 hash against what was advertised. If it doesn't
match, the transfer is rejected.

### In the Account-Cloud Lane

The cloud lane has a different trust model. The server is the coordination
point, and it gets the final say.

{{< info title="What is Compare-and-Swap?" >}} Compare-and-swap (CAS) is a
concurrency primitive from CPU architecture that's used throughout distributed
systems. The idea: "I expect the current value to be X. If it is, change it to
Y. If not, tell me what it actually is." Databases use this for optimistic
locking. Here, the device says "I was at version 8 when I made this change" and
the server either accepts (if version 8 is current) or rejects with the actual
current version. {{< /info >}}

**Reading position** is the most interesting difference. Instead of timestamps,
the cloud uses a version-based compare-and-swap. Your device sends: "I was at
version 8 when I made this change." The server checks: is version 8 still
current? If yes, it accepts and increments to version 9. If another device
already pushed version 9, you have a conflict.

But the server doesn't just reject conflicts. It looks at the _intent_ of the
update. If you're advancing forward in a book, the server will auto-rebase your
update on top of the newer version, up to three retries. If you're rewinding and
there's a conflict, it rejects immediately, because if another device advanced
past you, your rewind is stale.

**Annotations and events** use the same CRDT merge rules as the peer lane, the
server deduplicates by event ID and uses HLC for ordering. The server is more of
a relay here than an arbiter.

{{< note title="CRDTs" >}} CRDT stands for Conflict-free Replicated Data Type.
It's a data structure designed so that multiple replicas can be updated
independently and always converge to the same state when they sync, without any
coordination. The "conflict-free" part means the merge function is
mathematically guaranteed to produce the same result regardless of the order
operations are applied in. This is what makes the peer lane possible without a
central coordinator. {{< /note >}}

### Why Two Models

Most local-first systems I've read about pick one consistency model. We run
both, because the trust relationship is fundamentally different.

Peers are autonomous. They might never see a server. They need to converge with
just timestamps and deterministic merge rules, no coordinator involved. The
cloud is a coordination point that multiple devices converge on. It can afford
to be smarter, to look at intent, to rebase, to reject, because it has a global
view of all devices.

There's one more subtlety. When the app launches and you're signed in, there's a
brief window where the local database has yesterday's reading position but the
cloud might have today's from another device. Without protection, the app would
immediately sync the stale local position upstream and overwrite the newer one.
So there's a gate: cloud-bound syncs are held back until the initial pull from
the cloud completes and merges. Only then do local writes start flowing
upstream. It's a small thing, but without it you'd occasionally lose your place.

## Switching Lanes: Guest to Cloud

The last requirement on my list was the migration path. You've been reading as a
guest on two devices, syncing over WiFi, and now you sign in. What happens to
all that local data?

![Lane switch: guest to cloud](/images/posts/merrilin/tech/lane-switch.png)

The lane switches from guest-peer to account-cloud. The app replays your entire
local history through the cloud's batch ingest endpoints. Every reading
position, every highlight, every reading event gets uploaded, keyed by the
book's file hash. The cloud uses the same deduplication rules it uses for normal
sync, so replaying the same event twice is harmless.

The important thing is that this works _without uploading the book files_. Your
reading data, progress, highlights, bookmarks, reading events, all syncs to the
cloud by file hash alone. The cloud stores a metadata-only record. You can see
your progress across devices even if the actual EPUB never leaves your phone.

File upload is optional and separate. You'd only do it for cloud backup or to
unlock AI chat features. When you do upload, the metadata-only record gets
promoted to a full record. Nothing gets duplicated.

This was the part I was most nervous about, but it turned out to be the
simplest. The migration is just "replay all local history through the same
endpoints the normal cloud sync loop uses." Same CRDT merge rules, same event ID
deduplication, same conflict resolution. No special migration code path. The
lane switch is really just "start flushing your outbox to a different
destination."

## Closing Thoughts

This ended up being one of the most satisfying things I've built. At its core,
it's a distributed systems problem: two devices, no central coordinator, data
has to converge. The same problem that databases like CockroachDB and Cassandra
solve, running on phones over WiFi.

The realization that made it tractable was that by restricting to CRDTs and
Hybrid Logical Clocks, I didn't need consensus. No leader election, no two-phase
commit, no distributed locking. Each device is sovereign over its own writes.
The merge function is commutative and idempotent, so it doesn't matter what
order devices sync in or how many times they replay the same data. The system
converges regardless. That's the core promise of CRDTs, and it's well suited to
a mobile context where devices appear and disappear unpredictably.

If I were to point someone at the closest real-world analog, it would be
CouchDB's replication protocol. Same idea of local-first databases syncing via
bidirectional cursor exchange with conflict resolution at the document level.
The main difference is we do it peer-to-peer over mTLS rather than
client-to-server, and we use different conflict resolution strategies for
different data types rather than one-size-fits-all.
