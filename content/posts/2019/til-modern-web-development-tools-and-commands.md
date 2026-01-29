---
date: 2019-01-01T12:00:00+05:30
draft: false
title: "TIL: Modern Web Development Tools and Command-Line Utilities"
description:
  "Today I learned about essential modern development tools, from better
  command-line utilities to web frameworks, that significantly improve developer
  productivity and workflow."
tags:
  - til
  - cli
  - "web-development"
  - productivity
  - "development-tools"
  - "rust-tools"
  - "python-tools"
---

Today I discovered an impressive collection of modern development tools and
command-line utilities that represent significant improvements over traditional
Unix tools, showcasing how modern languages like Rust are revolutionizing
developer tooling.

## Superior Command-Line Tools

### HTTPie - Human-Friendly HTTP Client

[HTTPie](https://github.com/jakubroztocil/httpie) positions itself as "HTTP for
Humans" and dramatically simplifies API testing and HTTP requests:

```bash
# Simple GET request
http GET https://api.github.com/users/stonecharioteer

# POST with JSON data
http POST https://httpbin.org/post name=John age:=30 active:=true

# Authentication
http GET https://api.github.com/user Authorization:"token YOUR_TOKEN"

# File uploads
http --form POST https://httpbin.org/post file@upload.txt

# Custom headers and cookies
http GET https://example.com X-Custom-Header:value Cookie:session=abc123

# Pretty-print JSON responses (default)
http GET https://api.github.com/repos/python/cpython | jq '.stargazers_count'
```

{{< example title="HTTPie vs Curl Comparison" >}} **Curl**:
`curl -X POST -H "Content-Type: application/json" -d '{"name":"John","age":30}' https://api.example.com/users`

**HTTPie**: `http POST https://api.example.com/users name=John age:=30`

HTTPie's syntax is more intuitive and requires less boilerplate for common
operations. {{< /example >}}

### FZF - Fuzzy Finder Revolution

[FZF](https://github.com/junegunn/fzf) transforms command-line history and file
searching with fuzzy matching:

```bash
# Install fzf
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install

# Basic file search
fzf

# Search command history
history | fzf

# Search and edit files
vim $(find . -type f | fzf)

# Git integration
git log --oneline | fzf

# Process search and kill
ps aux | fzf | awk '{print $2}' | xargs kill
```

#### Advanced FZF Integration

```bash
# Add to .bashrc or .zshrc for enhanced functionality

# Better cd with fuzzy search
cdf() {
    local dir
    dir=$(find ${1:-.} -path '*/\.*' -prune \
          -o -type d -print 2> /dev/null | fzf +m) &&
    cd "$dir"
}

# Fuzzy git branch checkout
fgb() {
    local branches branch
    branches=$(git branch -vv) &&
    branch=$(echo "$branches" | fzf +m) &&
    git checkout $(echo "$branch" | awk '{print $1}' | sed "s/.* //")
}

# Fuzzy kill process
fkill() {
    local pid
    pid=$(ps -ef | sed 1d | fzf -m | awk '{print $2}')
    if [ "x$pid" != "x" ]; then
        echo $pid | xargs kill -${1:-9}
    fi
}
```

{{< tip title="FZF Productivity Boost" >}} FZF integrates with:

- **Shell history**: `Ctrl+R` for fuzzy history search
- **File navigation**: `Ctrl+T` for file picker
- **Directory jumping**: `Alt+C` for directory picker
- **Vim integration**: Fuzzy file finding in editors
- **Git workflows**: Branch switching, log browsing {{< /tip >}}

### Bat - Enhanced Cat with Syntax Highlighting

[Bat](https://github.com/sharkdp/bat) provides beautiful syntax highlighting and
Git integration:

```bash
# Install bat
cargo install bat
# or
brew install bat

# Basic usage with syntax highlighting
bat main.py

# Show line numbers and git changes
bat --number --show-all src/app.rs

# Use as pager replacement
export PAGER="bat --plain --paging=always"

# Combine with other tools
curl -s https://raw.githubusercontent.com/rust-lang/rust/master/README.md | bat -l md

# Configuration file
bat --config-file
```

### Ripgrep - Grep on Steroids

[Ripgrep](https://github.com/BurntSushi/ripgrep) offers blazing-fast text search
with intelligent defaults:

```bash
# Basic search
rg "TODO"

# Case insensitive search
rg -i "error"

# Search in specific file types
rg "function" --type py
rg "impl" --type rust

# Search with context lines
rg "error" -C 3

# Regular expressions
rg "fn\s+\w+\(" --type rust

# Exclude directories
rg "pattern" --glob '!target/' --glob '!node_modules/'

# Replace mode (preview)
rg "old_function" --replace "new_function" --type py

# JSON output for scripting
rg "pattern" --json | jq '.data.lines.text'
```

{{< note title="Ripgrep Performance" >}} Ripgrep is significantly faster than
grep, ack, or ag because:

- **Parallelization**: Uses multiple threads by default
- **Optimized algorithms**: Boyer-Moore string searching
- **Smart filtering**: Respects .gitignore and binary file detection
- **Memory efficiency**: Streaming search without loading entire files
  {{< /note >}}

## Development Utilities and Automation

### Python HTTP Server

The built-in Python HTTP server is perfect for quick local development:

```bash
# Python 3 (current)
python -m http.server 8000

# Python 2 (legacy)
python -m SimpleHTTPServer 8000

# Serve specific directory
python -m http.server 8000 --directory /path/to/files

# Bind to specific interface
python -m http.server 8000 --bind 127.0.0.1
```

This needs no additional dependencies and is available everywhere Python is
installed.

### Live-Server for Frontend Development

[Live-Server](https://github.com/tapio/live-server) provides automatic browser
refresh for static HTML development:

```bash
# Install globally
npm install -g live-server

# Serve current directory with live reload
live-server

# Custom port and browser
live-server --port=3000 --browser=firefox

# Serve specific directory
live-server --root=./dist

# Proxy API requests
live-server --proxy=/api:http://localhost:3000
```

### Pre-commit Hooks Management

[Pre-commit](https://pre-commit.com/) standardizes and automates code quality
checks:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 22.10.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/flake8
    rev: 5.0.4
    hooks:
      - id: flake8

  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort
        args: ["--profile", "black"]
```

```bash
# Install and setup
pip install pre-commit
pre-commit install

# Run on all files
pre-commit run --all-files

# Update hook versions
pre-commit autoupdate
```

## Advanced Development Tools

### Cookiecutter - Project Templating

[Cookiecutter](https://cookiecutter.readthedocs.io) uses Jinja2 templates to
generate project scaffolding:

```bash
# Install cookiecutter
pip install cookiecutter

# Create project from template
cookiecutter https://github.com/cookiecutter/cookiecutter-django

# Use local template
cookiecutter /path/to/my-template

# Create custom template structure
my-template/
├── cookiecutter.json
├── {{cookiecutter.project_name}}/
│   ├── README.md
│   ├── setup.py
│   └── {{cookiecutter.module_name}}/
│       └── __init__.py
```

Template configuration:

```json
{
  "project_name": "My Project",
  "module_name": "{{ cookiecutter.project_name.lower().replace(' ', '_') }}",
  "author_name": "Your Name",
  "version": "0.1.0",
  "license": ["MIT", "BSD", "GPL"]
}
```

### YouTube-DL - Media Download Utility

[YouTube-DL](https://github.com/ytdl-org/youtube-dl) enables downloading and
converting media from numerous platforms:

```bash
# Install
pip install youtube-dl

# Basic download
youtube-dl "https://www.youtube.com/watch?v=VIDEO_ID"

# Download audio only
youtube-dl -x --audio-format mp3 "URL"

# Download best quality
youtube-dl -f "best[height<=720]" "URL"

# Download playlist
youtube-dl -i "PLAYLIST_URL"

# Extract metadata
youtube-dl --get-title --get-duration "URL"

# Custom filename format
youtube-dl -o "%(uploader)s - %(title)s.%(ext)s" "URL"
```

## Code Analysis and Metrics

### CLOC - Count Lines of Code

[CLOC](https://github.com/AlDanial/cloc) provides detailed code statistics:

```bash
# Install
brew install cloc
# or
sudo apt install cloc

# Count lines in current directory
cloc .

# Specific languages
cloc --include-lang=Python,JavaScript .

# Exclude directories
cloc --exclude-dir=node_modules,target .

# Compare two codebases
cloc --diff version1/ version2/

# Output formats
cloc --json .
cloc --csv .
```

### Tokei - Modern Code Counter

[Tokei](https://github.com/XAMPPRocky/tokei) offers faster, more accurate line
counting:

```bash
# Install
cargo install tokei

# Basic usage
tokei

# Specific languages
tokei --languages rust,python

# Sort by lines
tokei --sort lines

# Output formats
tokei --output json
tokei --output yaml
```

## Modern Web Frameworks

### FastAPI - Async Flask Alternative

[FastAPI](https://fastapi.tiangolo.com/) provides high-performance async Python
web APIs:

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import asyncio

app = FastAPI(title="Modern API", version="1.0.0")

class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool = True

class UserCreate(BaseModel):
    name: str
    email: str

# Async endpoint with automatic OpenAPI documentation
@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    if user_id < 1:
        raise HTTPException(status_code=404, detail="User not found")

    # Simulate async database call
    await asyncio.sleep(0.1)
    return User(id=user_id, name="John Doe", email="john@example.com")

@app.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    # Auto-validation from Pydantic model
    new_user = User(id=123, **user.dict())
    return new_user

# Dependency injection
async def get_current_user() -> User:
    return User(id=1, name="Current User", email="user@example.com")

@app.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# Run with: uvicorn main:app --reload
```

{{< example title="FastAPI Benefits" >}}

- **Automatic OpenAPI/Swagger docs** at `/docs`
- **Type hints** for automatic validation
- **Async support** for high concurrency
- **Dependency injection** system
- **OAuth2 integration** built-in
- **WebSocket support** for real-time features
- **Background tasks** for async processing {{< /example >}}

### Go Web Frameworks

#### Revel Framework

[Revel](https://revel.github.io/) provides a full-stack web framework for Go:

```go
package controllers

import (
    "github.com/revel/revel"
)

type App struct {
    *revel.Controller
}

func (c App) Index() revel.Result {
    return c.Render()
}

func (c App) Hello(myName string) revel.Result {
    c.Viewargs["name"] = myName
    return c.Render()
}

// Routes (conf/routes)
// GET     /                                       App.Index
// GET     /hello/:myName                          App.Hello
```

## Security and Quality Tools

### Bandit - Python Security Scanner

[Bandit](https://github.com/PyCQA/bandit) identifies common security issues in
Python code:

```bash
# Install
pip install bandit

# Scan current directory
bandit -r .

# Skip test files
bandit -r . --skip B101

# Output formats
bandit -r . -f json
bandit -r . -f html -o security-report.html

# Configuration file
bandit -r . -c bandit.conf
```

### Responses - Mock HTTP Requests

[Responses](https://github.com/getsentry/responses) enables safe mocking of HTTP
requests in tests:

```python
import responses
import requests

@responses.activate
def test_api_call():
    # Mock the API response
    responses.add(
        responses.GET,
        "https://api.example.com/users/1",
        json={"id": 1, "name": "John Doe"},
        status=200
    )

    # Make the request
    resp = requests.get("https://api.example.com/users/1")

    # Test the response
    assert resp.status_code == 200
    assert resp.json()["name"] == "John Doe"

# Dynamic responses
@responses.activate
def test_dynamic_response():
    def request_callback(request):
        return (200, {}, '{"dynamic": "response"}')

    responses.add_callback(
        responses.GET,
        "https://api.example.com/dynamic",
        callback=request_callback
    )
```

## Development Productivity Insights

### Tool Selection Criteria

When choosing modern development tools, key factors include:

{{< tip title="Tool Evaluation Framework" >}}

1. **Performance**: Measurably faster than alternatives
2. **Ergonomics**: Better default behavior and user experience
3. **Integration**: Works well with existing workflows
4. **Maintenance**: Actively maintained with good documentation
5. **Cross-platform**: Consistent behavior across operating systems
6. **Community**: Strong ecosystem and community support {{< /tip >}}

### Command-Line Productivity Multipliers

The modern command-line tools demonstrate several important patterns:

1. **Intelligent Defaults**: Tools like `rg` and `bat` make smart assumptions
2. **Better Output**: Syntax highlighting and structured display improve
   usability
3. **Performance Focus**: Rust-based tools leverage systems programming for
   speed
4. **Integration-First**: Designed to work with pipes, scripts, and other tools
5. **Configuration**: Reasonable defaults with extensive customization options

## Migration Strategy

### Gradually Adopting Modern Tools

```bash
# Create aliases for gradual adoption
alias cat='bat'
alias grep='rg'
alias find='fd'  # fd is another excellent Rust-based find replacement

# Add to .bashrc/.zshrc
export PAGER="bat --plain --paging=always"

# Customize fzf key bindings
export FZF_DEFAULT_COMMAND='rg --files'
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
```

{{< warning title="Migration Considerations" >}} When adopting new tools:

- **Script Compatibility**: Some scripts may depend on specific output formats
- **Team Alignment**: Ensure team members can use the same tools
- **Learning Curve**: Budget time for learning new command syntax
- **Fallback Plans**: Keep traditional tools available for compatibility
  {{< /warning >}}

This exploration of modern development tools showcases how thoughtful tool
selection can dramatically improve developer productivity and code quality.

---

_These modern development tools from my archive demonstrate the ongoing
evolution of developer tooling, with languages like Rust enabling a new
generation of fast, reliable, and user-friendly command-line utilities._
