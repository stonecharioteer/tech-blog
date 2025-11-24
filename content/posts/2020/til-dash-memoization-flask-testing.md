---
date: "2020-07-23T23:59:59+05:30"
draft: false
title: "TIL: Dash Memoization, Flask-Dash Integration, and Testing"
tags: ["til", "dash", "flask", "testing", "python", "caching"]
---

## TIL 2020-07-23

1. **[Memoizing Dash Callback Responses with Flask-Caching](http://dash.plotly.com/testing)** -
   It's possible to cache dash callback responses for better performance using
   flask-caching.

2. **Configurable Dash Registration** - Always ensure that dash registration in
   a Flask-Dash app is configurable. You might want to skip loading dash when
   testing backend-only functionality.

3. **pytest-dash Status** - pytest-dash has been abandoned since the official
   dash repository now supports Selenium testing via pytest directly.
