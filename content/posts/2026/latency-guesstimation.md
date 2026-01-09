---
date: "2026-01-09T15:22:33+05:30"
draft: true
title: "Latency Guesstimation"
description: "A post on guesstimating latency, still a work in progress"
tags:
  - "latency"
  - "architecture"
---

{{< warning title="Work in Progress" >}}
This is a running document that's currently a work in progress. It will be updated as and when I make progress on this topic.
{{< /warning >}}

Following up from my posts on [career direction]({{< ref "posts/2026/direction.md" >}}), I wanted to write a
potential CFP submission on _Latency Guesstimation_. This post is going to be my
ongoing document charting this out. I'll keep the source-code for the slides in
[this github repo](https://github.com/stonecharioteer/latency-guesstimation),
and chart out the plan here instead.

## Elevator Pitch

It is impossible to have anything less than `1ns` latency between two servers
connected by a `30cm` wire. Why is that? What even _is_ latency? I wanted to
learn more about latency and why software is slow when it is. These notes are
the result of my investigation.
