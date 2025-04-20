---
date: '2025-04-20T09:44:21+05:30'
draft: false
title: 'Py-x-Protobuf - Or How I Learned to Stop Worry and Love Protocol Buffers'
tags:
  - "python"
  - "microservices"
  - "grpc"
---

## TLDR

- Protobufs are a mainstay of microservice development.
- You can use them in lieu of JSONs when interacting with a webservice.
- They're _much_ faster than JSON when you're deserializing or serializing them.
- They're designed mostly for applications that talk to each other.
- They'd make excellent choices for MCP-centric applications as well.

## Introduction

I first heard about protobufs from a friend working at Gojek in 2017. I didn't
know what they were used for and even when I looked them up, I didn't understand
what I needed them for. JSONs were good enough, weren't they?

Honestly, I've noticed that it's a pattern (sample size > 10) with developers
who'd mostly coded in Python. Protobufs were something that came out of Java
(preconception: mine), and they were continued to be used by people who were
from that world, going on to become Go developers, perhaps.

I was wrong, and I'm glad that I discovered them when I did.

For those of you who are reading about protobufs for the first time, here's the
short story.

> Protocol Buffers (protobuf) are a language-neutral, platform-neutral
> extensible mechanism for serializing structured data
> [i](https://protobuf.dev/overview/).

Programmers define the data in a `.proto` file, which is then used to interface
with data, language-specific runtime libraries. For example:

{{< code language="proto" source="code/py-x-protobuf/book.proto" >}}

## Using a Protobuf in Python

Let's take the above `proto` example and save it to `Book.proto`.

<!--  TODO: Solve the admonition problem elegantly. -->

> ℹ️ _**Note**_
>
> The numbers you see above are _not_ default values. They're the field tags and
> they have meaning. Tags in the range 1-15 take 1 byte. You can use these for
> frequently-used fields. Avoid reusing/overriding old tags by using the
> `reserved` keyword.

Ensure that you've installed `grpcio_tools` using `uv add` or `pip install`.

Now, _generate_ the python code for the protobuf by running
`python -m grpc_tools.protoc -I. --python_out=. book.proto`.

This should have created the file `book_pb2` in the current directory. This file
should look like this:

{{< code language="python" source="code/py-x-protobuf/book_pb2.py" >}}

`protoc`, the protobuf compiler, will generate this for any language (the python
variant using `grpcio-tools` will generate the python syntax, naturally.)

As the docstring at the top tells you, you _should not edit this file_.

How do you use it?

{{< code language="python" source="code/py-x-protobuf/example.py" >}}

I used to wonder why this was really that useful, until I looked at the
performance metrics. For this, we are going to use the timeit module.

{{< code language="python" source="code/py-x-protobuf/performance.py" >}}

On my laptop, I get the following results:

```
Runtime results for serialization across 10^6 runs:
JSON=1.4081
protobuf=0.6609
% difference=53.0643
Runtime results for deserialization across 10^6 runs:
JSON=1.1308
protobuf=0.3009
% difference=73.389
```

For 10^6 (one million) runs of simple serialization/deserialization functions,
these are the results.

| **Activity**    | **JSON** | **Protobuf** | **% Difference** |
|:---------------:|:--------:|:------------:|:----------------:|
| Serialization   | 1.4081   | 0.6609       | 53.0643          |
| Deserialization | 1.1308   | 0.3009       | 73.389           |

For serialization, protobufs are 53% faster, while for deserialization, they're 73.4% faster. The output above is in seconds, so for a million runs, we saved almost 1.5 seconds by using protobufs vs using jsons if we were just serializing and deserializing them.

In a large application where the payload also becomes complex, this will aid in speeding things up greatly. Additionally, note the field tags. These are used in lieu of the field names within the definition, so you have the added memory reduction.

Additionally, the `json` library is unaware of whether a field is an int or a string. Protobufs make this explicit and leave no ambiguity to chance when creating the payload or when serializing or deserializing it.

I'll follow up with a part-2 where I discuss using protobufs with the usual suspect: gRPC.