---
date: "2026-08-14T13:17:39+05:30"
draft: true
title: "Dottler - Manage .env Files Across Git Worktrees"
description:
  "Dottler is a local CLI for managing project environment variables and
  sharing them across Git worktrees without a server."
tags:
  - "rust"
  - "cli"
  - "dotfiles"
  - "git"
  - "development-tools"
  - "open-source"
---

I've been having trouble managing `.env` files across multiple Git worktrees.
I kept copying the same files around manually, and I wanted a simple CLI to do
that for me.

I've used [Doppler](https://www.doppler.com/) a lot previously, but I wanted an
offline version of the same experience. I also wanted to test out Grok 4.6, so I
thought this was a nice chance to work on a new project to solve this problem.

Presenting
[`stonecharioteer/dottler`](https://github.com/stonecharioteer/dottler).

## What is Dottler?

Dottler is a local command-line tool for managing `.env` files by project. It
needs no account or server. It identifies a project from its Git remote and
keeps the variables in a global store under your home directory, so every
worktree for that repo uses the same store.

It can import an existing `.env`, write one into a new worktree, export variables
to your shell, or run a command with them.

Dottler stores values as plain text on your machine. It is not an encrypted
secrets vault. Its purpose is to keep local environment files out of version
control and make them easier to use across worktrees. You should still keep
`.env` in your `.gitignore`.

## Getting started

Dottler is written in Rust and can be installed from its Git repo:

```fish
cargo install --git https://github.com/stonecharioteer/dottler
```

Change to a directory inside a repo and run `dottler which`. Dottler uses the
Git remote to identify the project. It should output something like this:

```
project github.com-stonecharioteer-tech-blog
kind    remote
package (repo)
env     dev
config  (root)
target  dev
store   /Users/stonecharioteer/.config/dottler/projects/github.com-stonecharioteer-tech-blog
file    /Users/stonecharioteer/.config/dottler/projects/github.com-stonecharioteer-tech-blog/dev.env
```

You don't need repo-level files to configure Dottler. If you already have a
`.env` file, import it:

```fish
dottler import .env
```

Then, in another worktree, write those variables back to `.env`:

```fish
dottler dump
```

Dottler also supports repos with multiple packages. You can select a package
explicitly when dumping its variables:

```fish
dottler --package apps/api dump
```

You can also avoid writing a file and pass the variables directly to a command:

```fish
dottler run -- cargo test
```

Or load them into Bash or Zsh:

```bash
# Bash
eval "$(dottler export --shell bash)"

# Zsh
eval "$(dottler export --shell zsh)"
```

Dottler also supports separate `dev`, `stg`, and `prd` environments and named
config overlays.

It's proving useful to me personally, and it has stopped me from copying my
`.env` files around all the time. If you use multiple worktrees, you might find
it useful too.

The source and complete usage guide are on
[GitHub](https://github.com/stonecharioteer/dottler).
