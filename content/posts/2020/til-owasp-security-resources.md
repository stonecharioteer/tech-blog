---
date: 2020-11-11T10:00:00+05:30
draft: false
title: "TIL: OWASP Security Resources - Cheat Sheets, Top 10, and Testing Guide"
description: "Today I learned about OWASP's comprehensive security resources including cheat sheets for secure development, the Top 10 web application risks, and the detailed web security testing guide."
tags:
  - til
  - security
  - owasp
  - web-security
  - penetration-testing
  - secure-development
---

Today I discovered a treasure trove of security resources from OWASP (Open Web Application Security Project) that provide practical guidance for secure development and testing.

## OWASP Cheat Sheet Series

[OWASP Cheat Sheets](https://github.com/OWASP/CheatSheetSeries) offer concise, actionable security guidance for developers and security professionals.

### Key Cheat Sheets:

#### **Authentication and Session Management:**
```javascript
// Secure session configuration example
app.use(session({
  name: 'sessionId',
  secret: process.env.SESSION_SECRET, // Strong, unique secret
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: true,        // HTTPS only
    httpOnly: true,      // Prevent XSS access
    maxAge: 1800000,     // 30 minutes
    sameSite: 'strict'   // CSRF protection
  },
  store: new RedisStore({
    host: 'localhost',
    port: 6379
  })
}));
```

#### **Input Validation:**
```python
# Secure input validation patterns
import re
from html import escape

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email)) and len(email) <= 254

def sanitize_html_input(user_input):
    # Escape HTML entities
    escaped = escape(user_input)
    # Remove potential script tags
    cleaned = re.sub(r'<script.*?</script>', '', escaped, flags=re.IGNORECASE)
    return cleaned

# Parameterized queries for SQL injection prevention
cursor.execute(
    "SELECT * FROM users WHERE email = %s AND status = %s",
    (validated_email, 'active')
)
```

#### **Cryptography Guidelines:**
```python
# Secure password hashing
import bcrypt
import secrets

def hash_password(password):
    # Generate salt with sufficient rounds
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

# Secure random token generation
def generate_csrf_token():
    return secrets.token_urlsafe(32)
```

## OWASP Top 10 Web Application Security Risks

[OWASP Top 10](https://owasp.org/www-project-top-ten/) identifies the most critical web application security risks based on industry data and expert consensus.

### 2021 Top 10 Breakdown:

#### **A01: Broken Access Control**
```javascript
// Vulnerable: Direct object reference
app.get('/user/:id/profile', (req, res) => {
  const userId = req.params.id;
  // No authorization check!
  const profile = database.getProfile(userId);
  res.json(profile);
});

// Secure: Proper authorization
app.get('/user/:id/profile', authenticate, (req, res) => {
  const userId = req.params.id;
  const currentUser = req.user;
  
  // Verify user can access this profile
  if (currentUser.id !== userId && !currentUser.isAdmin) {
    return res.status(403).json({ error: 'Access denied' });
  }
  
  const profile = database.getProfile(userId);
  res.json(profile);
});
```

#### **A02: Cryptographic Failures**
```python
# Secure data encryption at rest
from cryptography.fernet import Fernet
import os

def encrypt_sensitive_data(data):
    # Use environment variable for key
    key = os.environ.get('ENCRYPTION_KEY').encode()
    cipher_suite = Fernet(key)
    
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

def decrypt_sensitive_data(encrypted_data):
    key = os.environ.get('ENCRYPTION_KEY').encode()
    cipher_suite = Fernet(key)
    
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    return decrypted_data.decode()
```

#### **A03: Injection Attacks**
```sql
-- Vulnerable: SQL injection
SELECT * FROM users WHERE username = '" + user_input + "'

-- Secure: Parameterized query
SELECT * FROM users WHERE username = ?
```

### Risk Assessment Matrix:
- **Broken Access Control**: Prevalence: High, Impact: High
- **Cryptographic Failures**: Prevalence: Medium, Impact: High
- **Injection**: Prevalence: Medium, Impact: High
- **Insecure Design**: Prevalence: Medium, Impact: High
- **Security Misconfiguration**: Prevalence: High, Impact: Medium

## OWASP Web Security Testing Guide

[OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/v41/) provides systematic methodology for testing web application security.

### Testing Framework:

#### **Information Gathering:**
```bash
# Subdomain enumeration
subfinder -d example.com -o subdomains.txt

# Technology stack identification
whatweb https://example.com

# Directory and file discovery
dirb https://example.com /usr/share/dirb/wordlists/common.txt

# SSL/TLS configuration testing
sslscan example.com
```

#### **Authentication Testing:**
```python
# Automated authentication bypass testing
import requests

def test_authentication_bypass(base_url):
    test_cases = [
        # SQL injection attempts
        {"username": "admin' OR '1'='1", "password": "anything"},
        {"username": "admin'--", "password": ""},
        
        # Default credentials
        {"username": "admin", "password": "admin"},
        {"username": "administrator", "password": "password"},
        
        # Empty authentication
        {"username": "", "password": ""},
    ]
    
    for case in test_cases:
        response = requests.post(
            f"{base_url}/login",
            data=case,
            allow_redirects=False
        )
        
        if response.status_code == 302:  # Redirect might indicate success
            print(f"Potential bypass: {case}")
```

#### **Session Management Testing:**
```javascript
// Session testing checklist
const sessionTests = {
  // Test session token entropy
  checkTokenRandomness: (tokens) => {
    const uniqueTokens = new Set(tokens);
    return uniqueTokens.size === tokens.length;
  },
  
  // Test session fixation
  checkSessionFixation: async (sessionId) => {
    const loginResponse = await fetch('/login', {
      method: 'POST',
      headers: { 'Cookie': `SESSIONID=${sessionId}` },
      body: JSON.stringify({ username: 'test', password: 'test' })
    });
    
    const newSessionId = extractSessionFromResponse(loginResponse);
    return newSessionId !== sessionId; // Should be different
  },
  
  // Test session timeout
  checkSessionTimeout: async (sessionId) => {
    await new Promise(resolve => setTimeout(resolve, 1800000)); // 30 minutes
    
    const response = await fetch('/protected', {
      headers: { 'Cookie': `SESSIONID=${sessionId}` }
    });
    
    return response.status === 401; // Should be unauthorized
  }
};
```

### Testing Categories:

#### **Technical Testing:**
- **Input validation**: Boundary value analysis, fuzz testing
- **Error handling**: Information disclosure through error messages
- **Cryptography**: Weak algorithms, key management issues
- **Business logic**: Workflow bypasses, race conditions

#### **Infrastructure Testing:**
- **Network security**: Port scanning, SSL/TLS configuration
- **Web server configuration**: Default accounts, unnecessary services
- **Database security**: Privilege escalation, data exposure

These OWASP resources provide a comprehensive foundation for implementing security throughout the software development lifecycle, from secure coding practices to thorough security testing methodologies.