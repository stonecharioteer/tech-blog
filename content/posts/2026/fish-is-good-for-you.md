---
date: "2026-08-26T11:36:41+05:30"
draft: true
title: "Fish Is Good for You"
description: "After years of daily-driving fish I can't go back. A case for sane defaults, abbreviations over aliases, and treating the shell as a UI, not a language."
tags:
  - "fish"
  - "shell"
  - "tools"
  - "reflection"
---

I have been using the `fish` shell for the last few years. I like it a lot.

This is an opinion piece, not a tutorial. Your mileage will vary. Mine hasn't.

## TLDR

- Write scripts in bash with a shebang. Fish is for your fingers, not your cron jobs.
- Its defaults replaced my entire plugin ecosystem. My config runs no plugin manager at all.
- Abbreviations beat aliases, and I will die on this hill.
- One config serves my Mac and my Linux boxes unchanged.
- It still annoys me in specific ways. I stay anyway.

## "I can't be bothered to learn fish's syntax"

Then don't. That is the whole answer. Write your shell scripts in bash, put `#!/usr/bin/env bash` on line one, and run them like any other program. I do this. Fish never reads them.

The interactive shell and the scripting language are two different jobs. Fish is the shell I talk to. Bash is the shell my computer runs. I hold the same split everywhere else without thinking about it. My editor is not my compiler, and my terminal is not my multiplexer. Yet people judge fish by whether they would enjoy scripting in it. Nobody demands vi stay compatible with ed.

The POSIX complaint is the same objection in a costume. My scripts are portable because they declare their interpreter. My fingers are happy because fish treats them well. Neither fact cancels the other.

## Defaults are the feature

What sold me first was tab completion. Type any substring of a directory and hit tab. Fish completes it, case-insensitive, and highlights the part you typed. `cd checkouts<TAB>` finds the path even when I only remember a fragment of the name. It knows my commands too, because fish generates completions from man pages. `git checkout <TAB>` offers my actual branches. In years of using fish I have written zero lines of completion code.

Autosuggestions and syntax highlighting work on first launch with zero config. Compare that with the zsh playbook: install a framework, pick a theme, curate plugins, debug how they interact. Bash can approximate some of it with fzf's `**<TAB>` triggers or ble.sh, but I don't want to approximate. Every bolt-on is a thing you own, version, and debug.

My git history proves I learned this the hard way. Fundle rode along in my config from 2022 and went out in the November 2025 cleanup. Fisher lasted eleven months, August 2025 to July 2026, before I deleted it too. Each time I thought I needed a plugin manager. Each time, stock fish plus a few plain files turned out to be enough.

What my config actually does is wire in tools that are not fish at all. starship, atuin, zoxide, direnv, mise, fzf. Each one enters through a single `| source` line. My entire key binding integration is three lines: `fzf --fish | source`. Old guides shipped two hundred lines of bind syntax for less.

## Abbreviations beat aliases

Aliases hide the command. Abbreviations expand in place, so you re-read the real command every time you type the short one. You teach yourself while you type. I run roughly ninety of them. A git family, a docker compose family, tmux, lsd, and my Django set built on `uv run manage.py`.

The trick most people miss is `--set-cursor`. An abbreviation can drop a template on the line and park your cursor inside it. `B` becomes `% | bat`, `C` becomes `% | pbcopy` on the Mac and `% | xclip` on Linux, `E` becomes `2>&1 `. Typing `cat foo.log B` yields `cat foo.log | bat`, cursor ready at the pipe.

Configs should also explain themselves. My `dj-help` function prints the Django abbreviations defined in the file next to it. Six months from now, when I forget `djcsu`, the config reminds me.

## One config, every machine

`conf.d/` gates by platform. `linux.fish` and `sway.fish` only load where they make sense, and sway auto-starts when login lands on `/dev/tty1`. The Mac branches on `uname` inside `config.fish`. Git tracks the portable parts. Universal variables hold machine-local junk like keystore paths, and `fish_variables` is gitignored so the repo ports cleanly.

Getting here took one deliberate pass. In early 2026 I purged auto-generated files from the repo so the same clone works on both operating systems. Boring work. It paid for itself immediately.

## What still annoys me

Python virtualenvs assume bash. I source `activate.fish` and it works, but the fish path is always the afterthought. My [qtile setup](/posts/2025/qtile-window-manager/) depends on this dance.

Plenty of tools print setup snippets for bash and zsh and treat fish as a second-class citizen. The modern ones I use cope. The long tail does not.

And my config carries a zoxide workaround that copies `cd` into `__zoxide_cd_internal` before init, because zoxide expects the function to exist as a file. It works. I resent that I know why.

## Where this ends

I spend my working day in a terminal. Fish makes that room quiet. Fewer plugins, fewer hacks, fewer surprises at 3am.

[gbt](/posts/2025/git-branches-24h/) started as a blog post and still lives in my autoloaded functions. atuin replaced mcfly somewhere along the way, which you can verify by digging through my TIL posts from 2021. My config lives at [dotfiles-qtile](https://github.com/stonecharioteer/dotfiles-qtile), installed by [distributed-dotfiles](https://github.com/stonecharioteer/distributed-dotfiles).
