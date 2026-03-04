---
date: "2026-03-03T23:00:10+05:30"
title: "Goforgo v0.9.0"
description:
  "I've made some updates to https://github.com/stonecharioteer/goforgo"
tags:
  - "go"
  - "cli"
  - "learning"
  - "programming"
  - "tools"
---

It's been a while since I've worked on GoForGo. I hadn't gotten around to
maintaining it and didn't realize there was a little interest about it on the
repo.

I've made some updates and fixes and I thought I'd list them down here.

1. You do not need the repo to install `goforgo`.
   `go install github.com/stonecharioteer/goforgo` will install the tool for
   you. The exercises and solutions are embedded into the binary.
2. The TUI has an auto-advance command so it will always advance to the next
   exercise once you're done with the one you're working on.
3. Logical ordering is a little better, control statements now show up before
   functions, which makes more sense if you're trying to learn the language from
   the ground up.
4. Some of the comments are cleaned up so they don't reveal the solution right
   away.
5. Added about 50 new exercises, mostly go-gotchas and nuances. I've tacked them
   onto the end, but I'm okay with them being there.

I'm going to be testing it out a lot more in the upcoming weeks, but I am glad
this little tool I made for myself is turning out useful for others.
