---
date: "2025-12-03T19:58:07+05:30"
title: "gbt: branches touched in the last 24 hours"
description:
  "A tiny Fish function I use at Chatwoot to remind myself which Git branches I
  touched in the last day."
tags:
  - "til"
  - "git"
  - "fish"
  - "tools"
  - "chatwoot"
---

I keep too many branches alive when I'm working on Chatwoot. A day later I
forget the exact names and end up grepping through `git branch` output. I wrote
a tiny helper in Fish to show me the branches I touched in the last 24 hours:

```fish
function gbt --description 'List git branches updated/created in the last 24 hours'
    git for-each-ref --sort=-committerdate --format='%(committerdate:iso8601) %(refname:short)' refs/heads/ | \
    while read -l date time zone branch
        set -l commit_time (date -j -f "%Y-%m-%d %H:%M:%S %z" "$date $time $zone" +%s 2>/dev/null)
        set -l now (date +%s)
        set -l diff (math $now - $commit_time)
        if test $diff -le 86400
            echo "$date $time $branch"
        end
    end
end
```

### What it does

- `git for-each-ref` prints every local branch with its committer timestamp, most
  recent first.
- `read -l date time zone branch` splits that line into pieces so I can get the
  timestamp and branch name cleanly.
- `date -d "$date $time $zone" +%s` (GNU date on Linux) turns the ISO timestamp
  into epoch seconds.
- I subtract that from `date +%s` for "now" and keep anything under 86,400
  seconds—24 hours.
- The output is a short list I can scan:

### macOS note

The BSD `date` on macOS doesn't support `-d`. Swap the `commit_time` line for:

```fish
set -l commit_time (date -j -f "%Y-%m-%d %H:%M:%S %z" "$date $time $zone" +%s 2>/dev/null)
```

Or `brew install coreutils` and use `gdate -d "$date $time $zone" +%s` to match
the Linux version. Everything else stays the same.

```
$ gbt
2025-08-26 19:14:55 cx-app-perf
2025-08-26 10:02:07 fix-shift-threads
2025-08-26 08:41:33 remove-old-flows
```

That's enough to remind me where I should jump back in, and it's a good nudge
that I probably need to graduate these into separate worktrees soon.
