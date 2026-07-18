---
date: '2025-10-09T14:12:34+05:30'
draft: false
title: 'Fixing Toggleterm.nvim Toggle Behavior in Neovim'
description: 'How to properly configure toggleterm.nvim so terminals actually hide and show on Linux'
tags:
  - "neovim"
  - "linux"
  - "til"
  - "configuration"
---

## The Problem

I was using toggleterm.nvim in Neovim but ran into a frustrating issue: when I
opened a terminal, it wouldn't actually hide when I pressed the toggle key
again. The terminal would open fine, but there was no way to quickly hide it
and get back to my code without closing the buffer entirely.

This made the whole point of a "toggle" terminal kind of useless. I needed to
be able to pop open a terminal, run a quick command, then hide it with the same
keybinding.

## What Was Missing

It turns out toggleterm.nvim needs specific configuration to enable the toggle
behavior. Without proper setup, the plugin is installed but not actually
configured to handle showing and hiding terminals properly.

The key settings that make the toggle functionality work are:

1. **`open_mapping`** - This defines the keybinding that opens AND closes the terminal
2. **`terminal_mappings = true`** - This is crucial. It means the open mapping works even when you're inside the terminal buffer, so you can press the same key to hide it
3. **`insert_mappings = true`** - Allows the toggle to work from insert mode as well

## The Solution

I created a proper toggleterm configuration file at `~/.config/nvim/lua/plugins/toggleterm.lua`:

```lua
---@type LazySpec
return {
  "akinsho/toggleterm.nvim",
  version = "*",
  opts = {
    size = function(term)
      if term.direction == "horizontal" then
        return 15
      elseif term.direction == "vertical" then
        return vim.o.columns * 0.4
      end
    end,
    open_mapping = [[<c-\>]],
    hide_numbers = true,
    shade_terminals = true,
    shading_factor = 2,
    start_in_insert = true,
    insert_mappings = true,
    terminal_mappings = true,
    persist_size = true,
    persist_mode = true,
    direction = "float",
    close_on_exit = true,
    shell = vim.o.shell,
    auto_scroll = true,
    float_opts = {
      border = "curved",
      width = math.floor(vim.o.columns * 0.8),
      height = math.floor(vim.o.lines * 0.8),
      winblend = 3,
      zindex = 50,
    },
  },
  keys = {
    { "<C-\\>", "<cmd>ToggleTerm<cr>", desc = "Toggle terminal", mode = { "n", "t" } },
    { "<leader>tf", "<cmd>ToggleTerm direction=float<cr>", desc = "ToggleTerm float" },
    { "<leader>th", "<cmd>ToggleTerm size=10 direction=horizontal<cr>", desc = "ToggleTerm horizontal split" },
    { "<leader>tv", "<cmd>ToggleTerm size=80 direction=vertical<cr>", desc = "ToggleTerm vertical split" },
  },
}
```

## Key Keybindings

- `<C-\>` (Control + backslash) - Toggle the terminal (works in normal mode and inside the terminal)
- `<leader>tf` - Open floating terminal
- `<leader>th` - Open horizontal split terminal
- `<leader>tv` - Open vertical split terminal

## Why It Works

The combination of `open_mapping` with `terminal_mappings = true` is what
enables the "press once to show, press again to hide" behavior. Without
`terminal_mappings = true`, the keybinding only works in normal mode, so you'd
have to manually switch back to normal mode before hiding the terminal.

This is all happening inside Neovim itself - toggleterm creates a Neovim buffer
with a terminal, and the plugin manages showing and hiding that buffer. It
works the same way in any terminal emulator (Alacritty, Ghostty, Kitty, etc.)
because the terminal emulator is just displaying Neovim.

## Bonus: Custom Terminal Instances

You can also create custom terminal instances for specific tools. Here's an
example for lazygit:

```lua
local Terminal = require("toggleterm.terminal").Terminal

local lazygit = Terminal:new {
  cmd = "lazygit",
  dir = "git_dir",
  direction = "float",
  float_opts = {
    border = "curved",
    width = math.floor(vim.o.columns * 0.9),
    height = math.floor(vim.o.lines * 0.9),
  },
  on_open = function(term)
    vim.cmd "startinsert!"
    vim.api.nvim_buf_set_keymap(term.bufnr, "n", "q", "<cmd>close<CR>", { noremap = true, silent = true })
  end,
}

function _LAZYGIT_TOGGLE() lazygit:toggle() end
```

Then map it with: `{ "<leader>gg", "<cmd>lua _LAZYGIT_TOGGLE()<CR>", desc = "LazyGit" }`

Now toggleterm actually toggles.
