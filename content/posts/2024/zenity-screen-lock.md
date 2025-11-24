---
date: "2024-01-29T10:48:25+05:30"
draft: false
title: "Screen Lock for Cinnamon Desktop using Zenity and Terminal Commands"
description:
  "A simple solution using Zenity to create a confirmation dialog for screen
  locking in Cinnamon Desktop on Fedora 39."
tags:
  - "linux"
  - "cinnamon"
  - "fedora"
  - "zenity"
  - "bash"
---

{{< note title="This is how I did it in case I forget" >}} This post is more of
a "this is how I did it incase I forget". {{< /note >}}

I've switched to Cinnamon Desktop (on Fedora 39) last year, after giving up on
trying to maintain my Qtile configuration. I was wasting too much time on it.

One personal painpoint I had is that I wanted to lock my screen without
resorting to using the main Cinnamon menu all the time. I could use the keyboard
shortcuts dialog to trigger the built-in screen lock but I also wanted a
_confirmation_, which I haven't yet figured out how to do with the built-in
features. Plus, I'm a creature of habit, so I wanted something that I could
preserve and use in another window manager if need be.

To that end, I remembered a friend once showed me
[Zenity](https://www.linux.org/threads/introduction-to-zenity-part-1.44381/) to
create simple GUIs for Linux. I strung up this one liner that prompts me if I
want to lock my screen and then locks it if I click yes.

```bash
bash -c "zenity --question --text='Lock screen?' --title='Screen lock?' && \
  cinnamon-screensaver-command -l && xset dpms force off;"
```

![Screenlock prompt with Zenity](/images/posts/zenity-screenlock.png "Screenlock prompt with Zenity")

I needed the `bash -c ""` bit since this would be within the cinnamon launch
options and I'd want to ensure that this is reproducible all the time.

If I move to another window manager, I just need to replace
`cinnamon-screensave-command`. I also use `xset dpms force off` because it takes
a while to turn off my laptop screen and sometimes I do this just before
sleeping or turning the lights off and I don't want to wait.

I don't close the lid because I use my current laptop, an Asus RoG X13 Flow in
the tent mode, and would have to disconnect my docking station to flip it around
and close the lid.
