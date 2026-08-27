---
date: "2026-06-20T20:51:25+05:30"
draft: true
title: "From HTTP/1.1 to gRPC: A Python Developer's Guide to Talking on the Web"
description: "A hands-on walkthrough of HTTP/1.1, HTTP/2, SSE, WebSockets, and gRPC — with runnable FastAPI and Python examples for each."
tags:
  - "python"
  - "microservices"
  - "grpc"
  - "web-development"
---

## TLDR

- **HTTP/1.1**: Simple, text-based, request-response. Still the workhorse of the
  web.
- **HTTP/2**: Multiplexed, binary, efficient. Not everywhere because of TLS
  complexity, debugging pain, and "good enough" HTTP/1.1.
- **SSE**: Server-to-client streaming over HTTP. Dead simple for dashboards and
  notifications.
- **WebSockets**: Full-duplex persistent connections. Chat, gaming, real-time
  collaboration.
- **gRPC**: Structured RPC with Protobufs over HTTP/2. Microservices love it.

## Introduction

I was debugging a flaky microservice connection the other day and realized I'd
taken the "how do computers talk" stack for granted. HTTP/1.1 was just "the
internet" for years. Then HTTP/2 showed up with multiplexing and I went "cool,
now what?" Then WebSockets, SSE, gRPC — each solving a specific problem but
adding cognitive overhead.

This post is my attempt to map the territory. We'll build a minimal server and
client for each protocol in Python, using FastAPI where it makes sense, and
understand _when_ to reach for each.

All the code lives alongside this article. For the rest of the examples, assume
you're working from the `code/` directory inside this bundle. Install the
dependencies first:

```bash
cd code
uv pip install -r requirements.txt
```

Or, if you're still using `pip`:

```bash
cd code
pip install -r requirements.txt
```

---

## HTTP/1.1: The Foundation

HTTP/1.1 is text-based, request-response, and synchronous. One request in, one
response out. Keep-alive helps reuse TCP connections, but each connection can
carry only one request at a time unless you use pipelining, which is poorly
supported and rarely used. Browsers work around this by opening multiple parallel
connections per domain, but that adds overhead and doesn't scale cleanly.

FastAPI with Uvicorn is perfect here. The server is trivial:

{{< bundle-code language="python" source="code/http1_server.py" >}}

And a client with `requests`:

{{< bundle-code language="python" source="code/http1_client.py" >}}

Run the server with `python http1_server.py` and the client in another terminal.
You'll see the familiar JSON exchange.

### Why you'd use it

Literally everything. REST APIs, web pages, simple integrations. It's the
default because it's the default. You reach for something else when you hit its
limits.

---

## HTTP/2: The Almost-Standard

HTTP/2 solves HTTP/1.1's biggest problems without changing the semantics:

- **Binary framing**: No more parsing text. Efficient and less error-prone.
- **Multiplexing**: Multiple requests and responses interleaved on one TCP
  connection. No more head-of-line blocking at the HTTP layer.
- **Header compression (HPACK)**: Headers are repetitive; HTTP/2 compresses
  them.
- **Server push**: Was part of the spec, but has been deprecated in practice.

To see HTTP/2 in action, we need a server that speaks it. FastAPI + Hypercorn
does the job. Browsers only speak HTTP/2 over TLS, though `h2c` (HTTP/2 over
cleartext) exists for internal services. For this demo we'll use a self-signed
certificate:

{{< bundle-code language="python" source="code/http2_server.py" >}}

Generate a self-signed certificate first:

```bash
openssl req -x509 -newkey rsa:2048 -keyout server.key -out server.crt \
  -days 365 -nodes -subj "/CN=localhost"
```

And the client with `httpx`:

{{< bundle-code language="python" source="code/http2_client.py" >}}

### Why HTTP/2 isn't everywhere

This is the interesting part. HTTP/2 was standardized in 2015. A decade later,
it still hasn't fully displaced HTTP/1.1. Here's why:

1. **TLS is effectively mandatory**: Browsers require TLS for HTTP/2. Setting up
   and maintaining certificates is work. Let's Encrypt helps, but it's still
   friction — especially in internal or development environments.

2. **Debugging is harder**: Binary frames don't `curl` well. You need
   specialized tools (`nghttp`, browser dev tools) to inspect traffic. When
   something breaks at 2 AM, engineers reach for what's easy to debug.

3. **Corporate middleboxes**: Many enterprise proxies and firewalls understand
   HTTP/1.1 but choke on HTTP/2 or silently downgrade it. The internet is held
   together by infrastructure that upgrades slowly.

4. **"Good enough"**: For many applications, HTTP/1.1 with keep-alive and
   connection pooling is sufficient. The complexity isn't worth the gain unless
   you're pushing serious traffic or have many concurrent requests.

5. **Server push died**: It was supposed to be a killer feature, but it was hard
   to use correctly and has been deprecated in favor of Early Hints and preload.

6. **gRPC ate its lunch**: For APIs where HTTP/2's multiplexing shines, gRPC
   provides a full framework with schemas, streaming, and code generation. Many
   teams skipped "raw HTTP/2 REST" and went straight to gRPC.

### Why you'd use it

Browser-facing sites, APIs where latency matters, when you need true
multiplexing without multiple TCP connections. It's also what powers gRPC under
the hood, so you're using it whether you know it or not.

---

## SSE: Streaming Without the Drama

Server-Sent Events (SSE) is the "what if we streamed but kept it simple?"
protocol. It's just HTTP/1.1 with:

- `Content-Type: text/event-stream`
- A specific text format (`data: ...\n\n`)
- Built-in browser auto-reconnect and event IDs

The server:

{{< bundle-code language="python" source="code/sse_server.py" >}}

And a client with `requests`:

{{< bundle-code language="python" source="code/sse_client.py" >}}

### Why you'd use it

One-way server-to-client streaming. Stock tickers, notification feeds, progress
bars. If you don't need client-to-server streaming, SSE is simpler than
WebSockets and works over standard HTTP infrastructure.

---

## WebSockets: Full Duplex

WebSockets upgrade an HTTP/1.1 connection to a persistent, full-duplex TCP
channel. Binary or text frames in both directions. It's the only protocol here
that breaks the request-response model entirely.

FastAPI has native WebSocket support:

{{< bundle-code language="python" source="code/websocket_server.py" >}}

And a client with the `websockets` library:

{{< bundle-code language="python" source="code/websocket_client.py" >}}

### Why you'd use it

Chat applications, collaborative editing, gaming, anything requiring real-time
bidirectional communication. When SSE isn't enough because the client also needs
to push data frequently.

---

## gRPC: The Structured Approach

gRPC is HTTP/2 under the hood but you don't think about it. You write `.proto`
files, generate code, and get strongly-typed RPC with streaming support.

First, the schema:

{{< bundle-code language="protobuf" source="code/chat.proto" >}}

Generate the Python code:

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. chat.proto
```

This produces `chat_pb2.py` and `chat_pb2_grpc.py`. Don't edit them by hand.

The server:

{{< bundle-code language="python" source="code/grpc_server.py" >}}

And the client:

{{< bundle-code language="python" source="code/grpc_client.py" >}}

### Why you'd use it

Microservices, polyglot systems, anything where strict contracts and high
performance matter. The schema _is_ the documentation. If you're building a
system where Python, Go, and Java services need to agree on message shapes, gRPC
is hard to beat.

---

## The Decision Matrix

|     Protocol     |    Direction    |     Transport     |  Complexity  |            Best For             |
| :--------------: | :-------------: | :---------------: | :----------: | :-----------------------------: |
|    HTTP/1.1      | Request-response |       TCP         |     Low      |        Everything default       |
|     HTTP/2       | Request-response (multiplexed) | TCP + TLS |  Medium  |     High-throughput APIs        |
|       SSE        | Server → Client |     HTTP/1.1      |     Low      |   Notifications, live feeds     |
|   WebSockets     |  Bidirectional  | TCP (upgraded)    |   Medium     | Chat, real-time collaboration   |
|      gRPC        | Request-response + streaming | HTTP/2 |   Higher     | Microservices, typed APIs       |

---

## Conclusion

None of these replace each other. HTTP/1.1 is the reliable workhorse. HTTP/2 is
the faster horse that never quite won the race because cars (gRPC) showed up.
SSE and WebSockets solve streaming from opposite ends of the complexity
spectrum. gRPC gives you structure at the cost of flexibility.

Pick the tool that matches your constraints, not the one that's newest.
