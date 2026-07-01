---
date: "2026-07-01T08:59:10+05:30"
draft: false
title: "Checking Mermaid Diagrams in CI"
description:
  "I wrote a small GitHub Action to catch broken Mermaid diagrams in Markdown
  and standalone diagram files before they land in a repository."
tags:
  - "automation"
  - "diagrams"
  - "github"
  - "markdown"
  - "testing"
---

I have been using Mermaid diagrams more often in repositories. They're great in
Markdown because the diagram stays close to the explanation, and they're also
nice as standalone `.mmd` files when the diagram starts to deserve its own file.

The annoying bit is that Mermaid syntax errors are easy to miss. A README can
look fine until someone opens the exact section with the broken diagram, or a
blog post can build successfully while the rendered diagram is wrong. I wanted a
small CI check for that, so I wrote
[`check-mmdjs-action`][check-mmdjs-action].

The action checks three common cases:

- fenced Mermaid blocks in Markdown files,
- standalone `.mmd` files,
- standalone `.mermaid` files.

It uses Mermaid's parser API for syntax validation. It does not render diagrams,
and it does not launch Chrome or Puppeteer. That matters because I only want CI
to answer one question: "is this diagram valid Mermaid?" Rendering failures and
browser setup failures should not be confused with syntax failures.

A minimal workflow looks like this:

```yaml
name: Check Mermaid diagrams

on:
  pull_request:
  push:

jobs:
  mermaid:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: stonecharioteer/check-mmdjs-action@v3.1
```

For this blog, I configured it more narrowly. I only need to scan the Markdown
content and the `diagrams/` directory:

```yaml
- name: Check Mermaid diagrams
  uses: stonecharioteer/check-mmdjs-action@v3.1
  with:
    files: |
      content/**/*.md
      diagrams/**/*.mmd
      diagrams/**/*.mermaid
      README.md
    ignore: |
      themes/**
      public/**
      node_modules/**
    mermaid-version: 11.4.1
```

That is now part of the Hugo workflow for this site. If I add a broken Mermaid
fence to a post or commit an invalid standalone diagram, the pull request should
fail before the bad diagram reaches the blog.

This is a tiny piece of automation, but it is exactly the kind I like: boring,
focused, and close to where the mistake happens.

[check-mmdjs-action]: https://github.com/stonecharioteer/check-mmdjs-action
