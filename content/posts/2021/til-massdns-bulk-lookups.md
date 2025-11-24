---
date: 2021-06-10T10:00:00+05:30
draft: false
title: "TIL: MassDNS - High-Performance Bulk DNS Lookups"
description:
  "Today I learned about MassDNS, a high-performance DNS stub resolver designed
  for bulk lookups and reconnaissance, useful for subdomain enumeration and DNS
  analysis."
tags:
  - TIL
  - DNS
  - Security
  - Networking
  - Tools
---

## MassDNS - Bulk DNS Resolution

[GitHub - blechschmidt/massdns](https://github.com/blechschmidt/massdns) - A
high-performance DNS stub resolver for bulk lookups and reconnaissance
(subdomain enumeration).

MassDNS is a simple high-performance DNS stub resolver targeting those who seek
to resolve a massive amount of domain names in the order of millions or even
billions. It's particularly useful for:

- Subdomain enumeration
- DNS reconnaissance
- Large-scale DNS analysis
- Security research

The tool is designed to be fast and efficient when dealing with massive DNS
query volumes, making it valuable for cybersecurity professionals and
researchers.
