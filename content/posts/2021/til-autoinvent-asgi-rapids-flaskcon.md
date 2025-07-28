---
date: 2021-05-21T10:00:00+05:30
draft: false
title: "TIL: AutoInvent, ASGI, Python Packaging, RAPIDS GPU Computing, and FlaskCon"
description: "Today I learned about AutoInvent's development tools, ASGI specification for async Python web apps, dh-virtualenv for Python packaging, RAPIDS for GPU data science, and FlaskCon 2020 talks."
tags:
  - TIL
  - Python
  - ASGI
  - GPU Computing
  - Packaging
  - Conferences
---

## AutoInvent - Development Tools

[AutoInvent · GitHub](https://github.com/autoinvent/)

AutoInvent provides development tools and frameworks, particularly focused on:
- Rapid application development
- Code generation and scaffolding
- Developer productivity tools
- Modern web application frameworks

## ASGI - Async Python Web Standard

[GitHub - django/asgiref](https://github.com/django/asgiref) - ASGI specification and utilities.

ASGI (Asynchronous Server Gateway Interface) is the spiritual successor to WSGI, providing:
- Asynchronous request handling
- WebSocket support
- HTTP/2 compatibility
- Background task processing
- Integration with modern async Python frameworks like FastAPI and Django Channels

## dh-virtualenv - Python Debian Packaging

[GitHub - spotify/dh-virtualenv](https://github.com/spotify/dh-virtualenv) - Python virtualenvs in Debian packages.

Spotify's tool for packaging Python applications as Debian packages while maintaining virtualenv isolation:
- Combines Python virtualenvs with Debian packaging
- Solves dependency conflicts in production
- Maintains isolation between Python applications
- Simplifies deployment on Debian-based systems

## RAPIDS - GPU Data Science

[Open GPU Data Science | RAPIDS](https://rapids.ai/)

RAPIDS provides GPU-accelerated libraries for data science and analytics:
- GPU-accelerated DataFrames (cuDF)
- Machine learning (cuML)
- Graph analytics (cuGraph)
- Spatial analytics (cuSpatial)
- Massive performance improvements over CPU-only solutions

## FlaskCon 2020 Talks

[PyVideo.org · FlaskCon 2020](https://pyvideo.org/events/flaskcon-2020.html)

Collection of talks from FlaskCon 2020 covering:
- Flask best practices and patterns
- Modern web development with Flask
- Performance optimization
- Testing strategies
- Real-world Flask applications