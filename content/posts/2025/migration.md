---
date: "2025-07-30T21:18:11+05:30"
draft: false
title: "Migrating My Old Blog to Hugo with Claude"
tags:
  - "housekeeping"
  - "claude"
  - "ai"
---

I finally managed to migrate _all_ the tech content from my older blog(s). My blog went through 2 iterations
before this, first using Jekyll and markdown, and then using Sphinx and RestructuredText. Today, I'm back
on markdown, using Hugo. Thanks to GenAI, I've added admonitions to the PaperMod theme, and I'm able to modify
the theme to do whatever I want with Hugo. I don't think I need to go finding something else, and I can
finally focus on the content and not the code required to maintain my blog.

I used Claude Code to migrate all my old posts. I checked out my previous blog and this blog to my desktop,
told Claude to look for posts in the older folder and to cross-verify that the posts exist here. And it
managed to go ahead, get the post date using the commit history, read the content and write the Hugo
frontmatter itself, and it even figured out where I was storing my posts from the OG blog and figured out
how to migrate them as well.

I also managed to update my Qtile post from 2022 using today's config details! This is really cool!

Finally, I gave it a mammoth task, importing all my TIL posts from the discord-bot-generated markdown
file that had gotten super unruly in my original Jekyll blog. And [it did!](/tags/til)

Lately I've been feeling that AI is addressing my burnout really well. Claude Code, in specific, is managing to
help me make some of the ideas in my head a reality. I've managed to write
[helper scripts for just about anything](https://github.com/stonecharioteer/scripts),
[improve my Qtile config](https://github.com/stonecharioteer/dotfiles-qtile), to such an extent that I can
comfortably say this is the best my desktop has ever looked! And, it has helped configure `touchegg` and `sleep`
on my devices that my laptop can sleep on closing the lid, in _linux!_ That's both something that's existed for
a while, but I didn't have the mental bandwidth to go looking.

I can _pinch to zoom_ on my trackpad on my laptop, when running Linux!

`$YEAR` is finally the year of Linux on the Desktop!
