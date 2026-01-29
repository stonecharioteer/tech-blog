---
date: 2021-06-02T10:00:00+05:30
draft: false
title: "TIL: DNS Performance Testing and Pi-hole with Unbound"
description:
  "Today I learned about DNS performance testing tools and troubleshooting
  Pi-hole performance issues with Unbound recursive DNS server."
tags:
  - "til"
  - "dns"
  - "performance"
  - "pihole"
  - "networking"
---

## DNS Performance Testing

[GitHub - cleanbrowsing/dnsperftest](https://github.com/cleanbrowsing/dnsperftest) -
DNS Performance test.

A simple script to test the performance of different DNS resolvers from your
location. It helps you find the fastest DNS servers for your network, testing
popular providers like:

- Cloudflare (1.1.1.1)
- Google (8.8.8.8)
- OpenDNS
- Quad9
- And many others

## Pi-hole with Unbound Performance Issues

[reddit: Pi-hole with Unbound as recursive DNS server slow performance](https://www.reddit.com/r/pihole/comments/d9j1z6/unbound_as_recursive_dns_server_slow_performance/)

Discussion about performance issues when using Unbound as a recursive DNS server
with Pi-hole. Common solutions include:

- Tuning Unbound configuration
- Adjusting cache settings
- Optimizing network timeouts
- Understanding the trade-offs between privacy and speed

## Cloudflare DNS Learning

[What is DNS? | Cloudflare](https://www.cloudflare.com/learning/dns/what-is-dns/)

Comprehensive guide to understanding DNS fundamentals, covering:

- How DNS resolution works
- DNS record types
- DNS security considerations
- Performance optimization techniques
