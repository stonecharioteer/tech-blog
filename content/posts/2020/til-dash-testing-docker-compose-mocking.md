---
date: "2020-07-23T23:59:59+05:30"
draft: false
title: "TIL: Dash Testing, Docker Compose, and Python Mocking"
tags:
  [
    "til",
    "dash",
    "plotly",
    "testing",
    "flask",
    "docker-compose",
    "python",
    "mocking",
    "pihole",
  ]
---

## Web Development and Testing

### Dash Framework Testing

- [It is possible to memoize dash callback responses with flask-caching](http://dash.plotly.com/testing)
- Dash supports response caching to improve performance
- Flask-caching integration allows for sophisticated caching strategies
- Important for optimizing callback-heavy Dash applications

### Flask-Dash Integration Best Practices

- Always ensure that dash registration in a Flask-Dash app is configurable
- Might want to not load dash when testing backend only
- Separation of concerns between backend API and frontend visualization
- Enables more targeted testing strategies

## Testing and Mocking

### Python Mock Module Best Practices

- When mocking python functions in a flask test, ensure you reference the module
  where the function is called, not where it originates from
- Common pitfall: mocking at the wrong import level
- Mock at the point of use, not the point of definition
- Critical for effective unit testing in complex applications

## Infrastructure and Networking

### Docker Compose Development Insights

- [docker-compose has _no_ docstrings](https://github.com/docker/compose/blob/master/compose/cli/main.py)
- Interesting observation about code documentation practices
- Even popular tools can have documentation gaps
- Reminder of the importance of good code documentation

### DNS and Network Tools

#### Pi-hole Architecture

- `pihole`'s Faster than light engine is a fork of dnsmasq
- Built on proven DNS server technology
- Optimized for ad-blocking and DNS filtering
- Demonstrates how open source projects build on each other

#### Command Line Tools

- `argparse` _does_ support sub-commands
- Python's built-in argument parsing library is more capable than often realized
- Enables building complex CLI interfaces with nested commands
- Alternative to third-party libraries like Click for simpler use cases
