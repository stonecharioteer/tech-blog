---
date: "2025-11-18T20:06:54+05:30"
draft: true
title: "Rust Download Manager"
description: ""
tags:
  - "Rust"
  - "learning"
---

It's been a hot minute since I've coded in Rust. I absolutely love the language
and after trying Ruby, Python, Javascript and Typescript, I can confidently say
I love Rust more than any other language. That being said, I wanted to jolt my
muscle memory for Rust using a project that I could sink my teeth into. My
friend recommended that I build a download manager, and I wanted to see what I
could do with that train of thought.

My goals with this project were:

1. Relearn everything I once knew about Rust, improving my understanding of
   things I might have missed out on.
2. Build a download-manager I can use in lieu of `wget`-fu.

So I set about planning the features out.

{{< note title="Source Code & Prelude" >}}
[`stonecharioteer/download-manager`](https://github.com/stonecharioteer/download-manager)
has all the code for this project, and I've tagged everything in stages so I can
talk about the features as they evolved. My objectives with this blog post are
to outline my train of thought, and discuss the _whys_ of changes I had to make.
Some of these changes were fuelled by trying to write idiomatic-rust, and some
by the need to DRY. For the sake of this learning exercise, I _might_ (most
certainly) have over-engineered this tool. There certainly are features that I
do not need, but I implemented them anyway just to learn how to do these things.
{{< /note >}}

## Stage 1: Fetching a file and writing to disk

**Source**:
[`tag:v0.1-task1-blocking-mvp`](https://github.com/stonecharioteer/download-manager/releases/tag/v0.1-task1-blocking-mvp)

My first goal was to get to writing the file to disk as soon as possible. I
wanted a CLI, so I reached for `clap`, and used the `derive` API, and had a
simple download command that had the following design:

```bash
dlm $URL
```

I wasn't aiming for concurrency or speed at the beginning, I just wanted a
simple download CLI that would take a URL and write the file it provided to
disk. For the UX, I wanted to have some sort of progress indicator, so I reached
for `indicatif` and used the `ProgressBar::new_spinner()`, which gave me a clean
little indicator that something was going on. I also used
`indicatif::HumanBytes` to humanize the bytes being printed to screen next to
the spinner.

Next, I wanted to implement support for `SIGKILL`, since it was getting hard to
test this out without being able to hit `CTRL-c`. I hadn't used the `ctrlc`
crate before, but that proved to be easy (for now).

I also quickly realized I needed to add support for `--resume`,
`--target-directory`, `--overwrite`, since I wanted to test quickly. `--resume`
needed the ``
