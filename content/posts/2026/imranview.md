---
date: "2026-04-05T15:48:04+05:30"
title: "How I Made Arrow-Key Navigation Feel Instant in a Rust Image Viewer"
description:
  "A practical write-up of the queueing, visible-first thumbnail decoding, and
  cache budget work that made ImranView feel much faster."
tags:
  - "rust"
  - "desktop"
  - "performance"
  - "egui"
  - "systems-programming"
---

I've been building ImranView, a cross-platform desktop image viewer.

The feature checklist was moving fast, but one thing felt bad every day:
arrow-key navigation. I'd hold right-arrow to move through a folder and it
would stutter, sometimes hard. Thumbnails also felt late, and startup had one
run that was hilariously slow.

```text
[perf][WARN] open_image=679ms (target=150ms threshold=300ms)
[perf][OK] open_image=8ms (target=150ms threshold=300ms)
[perf][OK] open_image=7ms (target=150ms threshold=300ms)
[perf][WARN] open_image=352ms (target=150ms threshold=300ms)
[perf][WARN] startup=25766ms (target=450ms threshold=700ms)
```

The first instinct is "optimize image decode." That's part of it, but that
wasn't the main bug. The real issue was control flow: too much work competing,
out-of-order results, and no strict runtime budgets.

This post is about the bit that actually moved the needle.

## 1) Coalesce navigation instead of firing open requests blindly

If you press next 12 times quickly, most apps don't need to execute 12 full
open cycles. They need to land on the right final file, and stay responsive
while doing it.

I moved navigation to a queued step counter. Input only mutates backlog. Actual
open dispatch happens one-at-a-time.

```rust
fn queue_navigation_step(&mut self, step: i32) {
    if step == 0 {
        return;
    }
    if !self.state.has_image() {
        self.state.set_error("no image loaded");
        return;
    }

    self.pending.queued_navigation_steps =
        (self.pending.queued_navigation_steps + step).clamp(-256, 256);

    if !self.pending.open_inflight {
        self.dispatch_queued_navigation_step();
    }
}

fn dispatch_queued_navigation_step(&mut self) {
    let queued = self.pending.queued_navigation_steps;
    if queued == 0 {
        return;
    }

    let forward = queued > 0;
    let path_result = if forward {
        self.state.resolve_next_path_with_wrap(true)
    } else {
        self.state.resolve_previous_path_with_wrap(true)
    };

    match path_result {
        Ok(path) => {
            if forward {
                self.pending.queued_navigation_steps -= 1;
            } else {
                self.pending.queued_navigation_steps += 1;
            }
            self.dispatch_open(path, true);
        }
        Err(err) => {
            self.pending.queued_navigation_steps = 0;
            self.state.set_error(err.to_string());
        }
    }
}
```

Source: [navigation queue code][nav-queue]

This made repeated key presses stop feeling like dropped input. It also reduced
wasted decode work under bursty input.

## 2) Drop stale worker results on arrival

Background work can finish out of order. If request `41` returns after `44`,
`41` is stale and must be ignored.

So every async path carries a request id, and UI apply-paths guard on "latest"
ids.

```rust
WorkerResult::Opened {
    request_id,
    path,
    directory,
    files,
    loaded,
    metadata,
} => {
    if request_id != self.pending.latest_open {
        log::debug!(
            target: "imranview::worker",
            "drop stale open result request_id={} latest_open={}",
            request_id,
            self.pending.latest_open
        );
        return;
    }

    self.pending.open_inflight = false;
    self.state.apply_open_payload(path, directory, files, loaded);
    self.current_metadata = Some(metadata);
    self.update_main_texture_from_state(ctx);
    self.dispatch_queued_navigation_step();
}
```

Source: [stale result guard][stale-guard]

Without this, fast input feels haunted. You jump ahead, then an old result pops
in and rewinds the UI.

## 3) Decode thumbnails only when likely useful

The thumbnail strip/window should not trigger eager decode for an entire folder.
I made it visible-first with a small hint radius around the current index.

```rust
if self.thumb_cache.get(&entry.path).is_none()
    && (entry.decode_hint
        || response.response.rect.is_positive()
            && ui.is_rect_visible(response.response.rect))
{
    self.request_thumbnail_decode(entry.path.clone());
}
```

Source: [visible-first thumbnail decode][thumb-visible]

That one condition does a lot:

1. Avoid duplicate decode when already cached.
2. Prioritize current-neighborhood items (`decode_hint`).
3. Load on visibility for scrolled content.

The perceptual difference is immediate: thumbnails "arrive" progressively
instead of all-or-nothing.

## 4) Put hard byte budgets on caches

A "cache" without eviction policy is just delayed memory growth.

ImranView now uses bounded caches for both thumbnail textures and preloaded
full-image payloads, each with entry caps and byte caps.

```rust
fn evict_if_needed(&mut self) {
    while self.map.len() > self.capacity || self.total_bytes > self.max_bytes {
        if let Some(oldest) = self.order.pop_front() {
            self.map.remove(&oldest);
            if let Some(bytes) = self.byte_sizes.remove(&oldest) {
                self.total_bytes = self.total_bytes.saturating_sub(bytes);
            }
        } else {
            break;
        }
    }
}
```

Source: [thumbnail texture cache][thumb-cache]

Preload cache in the worker uses the same discipline:

```rust
fn evict(&mut self) {
    while self.map.len() > self.capacity || self.total_bytes > self.max_bytes {
        if let Some(oldest) = self.order.pop_front() {
            self.map.remove(&oldest);
            if let Some(bytes) = self.byte_sizes.remove(&oldest) {
                self.total_bytes = self.total_bytes.saturating_sub(bytes);
            }
        } else {
            break;
        }
    }
}
```

Source: [worker preload cache][preload-cache]

This gave me predictable behavior over big folders and longer sessions.

## 5) Keep perf budgets in code, and fail when they drift

I don't trust "feels fast" after a long day of coding.

I keep explicit target/threshold budgets and log every critical path with a
consistent format.

```rust
pub fn log_timing(label: &str, elapsed: Duration, budget: PerfBudget) {
    let elapsed_ms = elapsed.as_millis();
    if elapsed_ms > budget.threshold_ms {
        log::warn!(
            target: "imranview::perf",
            "[WARN] {label}={}ms (target={}ms threshold={}ms)",
            elapsed_ms,
            budget.target_ms,
            budget.threshold_ms
        );
    } else if elapsed_ms > budget.target_ms {
        log::info!(
            target: "imranview::perf",
            "[SLOW] {label}={}ms (target={}ms threshold={}ms)",
            elapsed_ms,
            budget.target_ms,
            budget.threshold_ms
        );
    } else {
        log::debug!(
            target: "imranview::perf",
            "[OK] {label}={}ms (target={}ms threshold={}ms)",
            elapsed_ms,
            budget.target_ms,
            budget.threshold_ms
        );
    }
}
```

Source: [perf logger + budgets][perf-rs]

Then CI runs a gate script that fails if warning-class budget breaches show up
in logs.

```bash
warnings="$(rg -n "\\[WARN\\].*\\(target=.*threshold=.*\\)" "$log_file" || true)"
if [[ -n "$warnings" ]]; then
  echo "[perf-gate][FAIL] budget warnings found in $log_file"
  echo "$warnings"
  failed=1
fi
```

Source: [perf gate script][perf-gate]

That combination keeps performance from becoming a one-time cleanup project.

## What changed in practice

- Rapid next/previous input no longer fights itself.
- Old async results don't clobber newer intent.
- Thumbnails appear progressively, with visible items first.
- Memory behavior is bounded and tunable.
- Regressions get flagged early instead of becoming folklore.

I still have work to do, especially on the rare slow cold-open outliers. But
this was the turning point where the app started feeling crisp under normal
usage.

## If you're building desktop software

If you're in the same spot I was, I'd start here before micro-optimizing decode
internals:

1. Coalesce bursty input.
2. Reject stale async results.
3. Load visual data by visibility priority.
4. Bound caches by bytes, not item count alone.
5. Encode performance budgets in code and CI.

Most of the win came from these boring systems choices, not exotic algorithms.

[nav-queue]: https://github.com/stonecharioteer/imranview/blob/main/src/main.rs#L2401-L2451
[stale-guard]: https://github.com/stonecharioteer/imranview/blob/main/src/main.rs#L2502-L2541
[thumb-visible]: https://github.com/stonecharioteer/imranview/blob/main/src/main.rs#L6324-L6330
[thumb-cache]: https://github.com/stonecharioteer/imranview/blob/main/src/main.rs#L1281-L1361
[preload-cache]: https://github.com/stonecharioteer/imranview/blob/main/src/worker.rs#L599-L670
[perf-rs]: https://github.com/stonecharioteer/imranview/blob/main/src/perf.rs#L3-L57
[perf-gate]: https://github.com/stonecharioteer/imranview/blob/main/scripts/perf_gate.sh#L17-L30
