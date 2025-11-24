---
date: 2020-11-06T10:00:00+05:30
draft: false
title:
  "TIL: HTTP Status Code Reference, Security Headers, and Python Security Tools"
description:
  "Today I learned about comprehensive HTTP status code references, OWASP secure
  headers project, security design principles, and Python tools for header
  security analysis."
tags:
  - til
  - http
  - security
  - headers
  - python
  - web-security
  - owasp
---

Today's learning focused on web security fundamentals, from HTTP status codes to
security headers and Python security tooling.

## HTTP Status Code Quick Reference

[HTTP Status Codes Cheatsheet](https://devhints.io/http-status) provides a
comprehensive quick reference for all HTTP response codes.

### Status Code Categories:

#### **1xx Informational:**

```http
100 Continue          - Server received headers, client should send body
101 Switching Protocols - Server switching to protocol in Upgrade header
102 Processing        - Server received request, still processing (WebDAV)
```

#### **2xx Success:**

```http
200 OK                - Request successful
201 Created           - Resource successfully created
202 Accepted          - Request accepted for processing (async)
204 No Content        - Success, but no content to return
206 Partial Content   - Range request successful
```

#### **3xx Redirection:**

```http
301 Moved Permanently - Resource permanently moved to new URL
302 Found             - Resource temporarily at different URL
304 Not Modified      - Resource not modified since last request
307 Temporary Redirect - Same as 302, but method must not change
308 Permanent Redirect - Same as 301, but method must not change
```

#### **4xx Client Errors:**

```http
400 Bad Request       - Malformed request syntax
401 Unauthorized      - Authentication required
403 Forbidden         - Server understood, but refuses to authorize
404 Not Found         - Resource not found
409 Conflict          - Request conflicts with current state
422 Unprocessable Entity - Syntax correct, but semantically incorrect
429 Too Many Requests - Rate limiting triggered
```

#### **5xx Server Errors:**

```http
500 Internal Server Error - Generic server error
502 Bad Gateway          - Invalid response from upstream server
503 Service Unavailable  - Server temporarily unavailable
504 Gateway Timeout      - Upstream server timeout
```

## OWASP Secure Headers Project

[OWASP Secure Headers](https://owasp.org/www-project-secure-headers/) provides
comprehensive guidance on implementing security-focused HTTP headers.

### Critical Security Headers:

#### **Content Security Policy (CSP):**

```http
Content-Security-Policy: default-src 'self';
                        script-src 'self' 'unsafe-inline' cdnjs.cloudflare.com;
                        style-src 'self' 'unsafe-inline' fonts.googleapis.com;
                        font-src 'self' fonts.gstatic.com;
                        img-src 'self' data: https:;
                        connect-src 'self' api.example.com;
                        frame-ancestors 'none';
```

#### **HTTP Strict Transport Security (HSTS):**

```http
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

#### **X-Frame-Options and Frame Ancestors:**

```http
X-Frame-Options: DENY
# or for CSP
Content-Security-Policy: frame-ancestors 'none';
```

#### **Content Type Options:**

```http
X-Content-Type-Options: nosniff
```

### Advanced Security Headers:

#### **Referrer Policy:**

```http
Referrer-Policy: strict-origin-when-cross-origin
```

#### **Permissions Policy (formerly Feature Policy):**

```http
Permissions-Policy: geolocation=(), microphone=(), camera=()
```

#### **Cross-Origin Headers:**

```http
Cross-Origin-Embedder-Policy: require-corp
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Resource-Policy: same-origin
```

### Implementation Examples:

#### **Express.js Security Headers:**

```javascript
const express = require("express");
const helmet = require("helmet");

const app = express();

app.use(
  helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'", "'unsafe-inline'", "cdnjs.cloudflare.com"],
        styleSrc: ["'self'", "'unsafe-inline'", "fonts.googleapis.com"],
        fontSrc: ["'self'", "fonts.gstatic.com"],
        imgSrc: ["'self'", "data:", "https:"],
        connectSrc: ["'self'", "api.example.com"],
        frameAncestors: ["'none'"],
      },
    },
    hsts: {
      maxAge: 31536000,
      includeSubDomains: true,
      preload: true,
    },
  }),
);
```

#### **Django Security Headers:**

```python
# settings.py
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
X_FRAME_OPTIONS = 'DENY'

CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "cdnjs.cloudflare.com")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "fonts.googleapis.com")
```

## Python Security Tools

### hsecscan - HTTP Security Header Scanner

[hsecscan](https://github.com/riramar/hsecscan) is a Python tool for analyzing
HTTP security headers:

```python
# Installation
pip install hsecscan

# Basic usage
hsecscan https://example.com

# Custom analysis
from hsecscan import scan_headers

def analyze_security_headers(url):
    results = scan_headers(url)

    security_score = 0
    recommendations = []

    # Check for essential headers
    essential_headers = [
        'strict-transport-security',
        'content-security-policy',
        'x-content-type-options',
        'x-frame-options'
    ]

    for header in essential_headers:
        if header in results['headers']:
            security_score += 25
        else:
            recommendations.append(f"Missing {header}")

    return {
        'score': security_score,
        'recommendations': recommendations,
        'headers': results['headers']
    }
```

### secure.py - Security Headers Library

[secure.py](https://secure.readthedocs.io/en/latest/index.html) provides easy
security header management:

```python
from secure import Secure

# Basic configuration
secure_headers = Secure()

# Custom configuration
secure_headers = Secure(
    csp=ContentSecurityPolicy(
        default_src="'self'",
        script_src=["'self'", "cdnjs.cloudflare.com"],
        style_src=["'self'", "'unsafe-inline'"]
    ),
    hsts=StrictTransportSecurity(
        max_age=31536000,
        include_subdomains=True,
        preload=True
    ),
    referrer=ReferrerPolicy.strict_origin_when_cross_origin,
    permissions=PermissionsPolicy(
        geolocation="none",
        microphone="none",
        camera="none"
    )
)

# Flask integration
from flask import Flask

app = Flask(__name__)

@app.after_request
def set_security_headers(response):
    secure_headers.framework.flask(response)
    return response

# Django middleware
class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        secure_headers.framework.django(response)
        return response
```

## Secure by Design Principles

[Secure by Design](https://www.manning.com/books/secure-by-design) book
emphasizes building security into software architecture from the beginning:

### Core Principles:

#### **Defense in Depth:**

- Multiple security layers
- Fail-safe defaults
- Principle of least privilege
- Input validation at every boundary

#### **Secure Architecture Patterns:**

```python
# Domain-driven security model
class SecureUser:
    def __init__(self, user_id, permissions):
        self._user_id = self._validate_user_id(user_id)
        self._permissions = self._validate_permissions(permissions)

    @staticmethod
    def _validate_user_id(user_id):
        if not isinstance(user_id, str) or len(user_id) < 3:
            raise ValueError("Invalid user ID")
        return user_id

    def can_access(self, resource):
        return resource.required_permission in self._permissions

    def sanitized_id(self):
        # Never expose internal IDs directly
        return hashlib.sha256(self._user_id.encode()).hexdigest()[:8]
```

### System Administration Tools:

#### **Process Investigation:**

```bash
# Find process ID by name pattern
pidof nginx
pidof -x python3

# Multiple processes
pidof -x "python.*myapp"

# Single process only
pidof -s httpd
```

These tools and principles provide a comprehensive foundation for implementing
and maintaining web application security, from basic HTTP understanding to
advanced security header configuration and automated security analysis.
