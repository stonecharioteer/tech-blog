---
date: "2020-08-28T23:59:59+05:30"
draft: false
title: "TIL: macOS Gatekeeper and Rust Struct Optimization"
tags:
  ["til", "macos", "gatekeeper", "security", "rust", "optimization", "compiler"]
---

## TIL 2020-08-28

1. **[Disabling Gatekeeper on macOS Sierra](https://www.techjunkie.com/gatekeeper-macos-sierra/)** -
   Run `sudo spctl --master-disable` to allow apps from anywhere (be prepared
   for corporate IT emails).

2. **[Optimizing Rust Struct Size](https://camlorn.net/posts/April%202017/rust-struct-field-reordering/)** -
   A 6-month compiler development program focusing on automatic struct field
   reordering for better memory layout.
