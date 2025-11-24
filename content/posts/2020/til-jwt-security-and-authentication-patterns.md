---
date: 2020-07-13T22:00:00+05:30
draft: false
title: "TIL: JWT Security Patterns and Token Management"
description:
  "Today I learned about advanced JWT security patterns, token blacklisting
  strategies, and secure authentication implementations using
  Flask-JWT-Extended."
tags:
  - til
  - jwt
  - security
  - authentication
  - flask
  - token-management
  - web-security
---

Today I explored advanced JWT (JSON Web Token) security patterns and discovered
comprehensive strategies for handling token expiration, blacklisting, and secure
authentication flows in web applications.

## Flask-JWT-Extended Security Patterns

### Advanced Token Blacklisting

[Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/stable/blacklist_and_token_revoking/)
provides sophisticated patterns for JWT blacklisting and token revocation:

```python
from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt, get_jwt_identity, create_refresh_token
)
import redis
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

jwt = JWTManager(app)

# Redis for blacklist storage
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

class TokenBlacklist:
    @staticmethod
    def add_token_to_blacklist(jti, expires_at):
        """Add token to blacklist with expiration"""
        # Calculate TTL for automatic cleanup
        ttl = int((expires_at - datetime.utcnow()).total_seconds())
        redis_client.setex(f"blacklist_{jti}", ttl, "true")

    @staticmethod
    def is_token_blacklisted(jti):
        """Check if token is blacklisted"""
        return redis_client.exists(f"blacklist_{jti}")

    @staticmethod
    def blacklist_user_tokens(user_id):
        """Blacklist all tokens for a specific user"""
        # This requires maintaining a user->tokens mapping
        user_tokens = redis_client.smembers(f"user_tokens_{user_id}")
        for jti in user_tokens:
            redis_client.set(f"blacklist_{jti}", "true")
        redis_client.delete(f"user_tokens_{user_id}")

# Token blacklist checker
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return TokenBlacklist.is_token_blacklisted(jti)

# Store tokens for user tracking
@jwt.additional_claims_loader
def add_claims_to_access_token(identity):
    return {
        'user_id': identity['user_id'],
        'roles': identity.get('roles', []),
        'issued_at': datetime.utcnow().isoformat()
    }
```

### Secure Token Generation and Validation

```python
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    # Validate credentials (implement your auth logic)
    user = authenticate_user(username, password)
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    # Create tokens with additional claims
    user_identity = {
        'user_id': user.id,
        'username': username,
        'roles': user.roles
    }

    access_token = create_access_token(
        identity=user_identity,
        additional_claims={'token_type': 'access'}
    )
    refresh_token = create_refresh_token(
        identity=user_identity,
        additional_claims={'token_type': 'refresh'}
    )

    # Track token for user (for mass revocation)
    access_jti = get_jwt()['jti']
    refresh_jti = get_jwt()['jti']  # Get from refresh token
    redis_client.sadd(f"user_tokens_{user.id}", access_jti, refresh_jti)

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'expires_in': app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds()
    })

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    current_user = get_jwt_identity()
    token = get_jwt()

    # Add current token to blacklist
    TokenBlacklist.add_token_to_blacklist(
        token['jti'],
        datetime.fromtimestamp(token['exp'])
    )

    return jsonify({'message': 'Successfully logged out'})

@app.route('/logout-all', methods=['POST'])
@jwt_required()
def logout_all_devices():
    current_user = get_jwt_identity()

    # Blacklist all tokens for this user
    TokenBlacklist.blacklist_user_tokens(current_user['user_id'])

    return jsonify({'message': 'Logged out from all devices'})
```

## Advanced JWT Security Patterns

### Token Refresh Strategy

```python
@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    old_token = get_jwt()

    # Blacklist the old refresh token
    TokenBlacklist.add_token_to_blacklist(
        old_token['jti'],
        datetime.fromtimestamp(old_token['exp'])
    )

    # Create new access token
    new_access_token = create_access_token(identity=current_user)

    # Optionally create new refresh token for rotation
    new_refresh_token = create_refresh_token(identity=current_user)

    return jsonify({
        'access_token': new_access_token,
        'refresh_token': new_refresh_token
    })

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    token_claims = get_jwt()

    # Additional security checks
    if token_claims.get('token_type') != 'access':
        return jsonify({'error': 'Invalid token type'}), 401

    # Check user still exists and is active
    user = get_user_by_id(current_user['user_id'])
    if not user or not user.is_active:
        return jsonify({'error': 'User account disabled'}), 401

    return jsonify({
        'user': current_user,
        'data': 'This is protected data'
    })
```

### Role-Based Access Control with JWTs

```python
from functools import wraps

def require_roles(*required_roles):
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            current_user = get_jwt_identity()
            user_roles = set(current_user.get('roles', []))
            required_roles_set = set(required_roles)

            if not required_roles_set.intersection(user_roles):
                return jsonify({
                    'error': 'Insufficient permissions',
                    'required_roles': list(required_roles),
                    'user_roles': list(user_roles)
                }), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/admin/users', methods=['GET'])
@require_roles('admin', 'super_admin')
def admin_users():
    return jsonify({'users': get_all_users()})

@app.route('/moderator/posts', methods=['GET'])
@require_roles('moderator', 'admin')
def moderate_posts():
    return jsonify({'posts': get_flagged_posts()})
```

## JWT Security Best Practices

### Secure Token Storage and Transport

{{< warning title="JWT Security Considerations" >}} **Critical Security
Practices:**

- **HTTPS Only**: Never transmit JWTs over unencrypted connections
- **Short Expiration**: Keep access tokens short-lived (15-60 minutes)
- **Secure Storage**: Store tokens in HttpOnly cookies or secure storage
- **Token Validation**: Always validate token signature and claims
- **Blacklist Support**: Implement token revocation for security incidents
  {{< /warning >}}

```python
# Secure cookie configuration
app.config.update(
    JWT_TOKEN_LOCATION=['cookies'],
    JWT_COOKIE_SECURE=True,  # HTTPS only
    JWT_COOKIE_HTTPONLY=True,  # No JavaScript access
    JWT_COOKIE_SAMESITE='Strict',  # CSRF protection
    JWT_COOKIE_CSRF_PROTECT=True,  # Enable CSRF protection
)

# CSRF token handling
from flask_jwt_extended import get_csrf_token

@app.route('/get-csrf-token', methods=['GET'])
@jwt_required()
def get_csrf():
    return jsonify({'csrf_token': get_csrf_token(get_jwt())})
```

### Token Structure and Claims Validation

```python
import jwt
from datetime import datetime, timezone

def validate_jwt_structure(token):
    """Comprehensive JWT validation"""
    try:
        # Decode without verification first to check structure
        unverified = jwt.decode(token, options={"verify_signature": False})

        # Required claims validation
        required_claims = ['exp', 'iat', 'jti', 'sub']
        for claim in required_claims:
            if claim not in unverified:
                raise ValueError(f"Missing required claim: {claim}")

        # Expiration check
        exp = datetime.fromtimestamp(unverified['exp'], tz=timezone.utc)
        if exp < datetime.now(timezone.utc):
            raise ValueError("Token has expired")

        # Not before check (if present)
        if 'nbf' in unverified:
            nbf = datetime.fromtimestamp(unverified['nbf'], tz=timezone.utc)
            if nbf > datetime.now(timezone.utc):
                raise ValueError("Token not yet valid")

        # Custom business logic validation
        if 'user_id' not in unverified:
            raise ValueError("Token missing user identification")

        return True

    except jwt.InvalidTokenError as e:
        raise ValueError(f"Invalid token structure: {str(e)}")

# Integration with Flask-JWT-Extended
@jwt.token_verification_loader
def verify_token_callback(jwt_header, jwt_payload):
    """Additional token verification"""
    try:
        # Business logic validation
        user_id = jwt_payload.get('user_id')
        if not user_exists(user_id):
            return False

        # Check for suspicious activity
        if detect_suspicious_activity(jwt_payload):
            TokenBlacklist.add_token_to_blacklist(
                jwt_payload['jti'],
                datetime.fromtimestamp(jwt_payload['exp'])
            )
            return False

        return True
    except Exception:
        return False
```

## Advanced JWT Implementation Patterns

### Sliding Session Extension

```python
from datetime import datetime, timedelta

@app.before_request
def extend_session():
    """Extend session for active users"""
    if request.endpoint in ['static', 'health']:
        return

    try:
        # Check if we have a valid JWT
        if request.headers.get('Authorization'):
            token = get_jwt()
            current_time = datetime.utcnow()
            exp_time = datetime.fromtimestamp(token['exp'])

            # If token expires within 15 minutes, issue a new one
            if (exp_time - current_time) < timedelta(minutes=15):
                current_user = get_jwt_identity()
                new_token = create_access_token(identity=current_user)

                # Add new token to response headers
                response = make_response()
                response.headers['X-New-Token'] = new_token
                return response

    except Exception:
        pass  # Continue with normal request processing
```

### Audit Logging for Token Operations

```python
import logging
from datetime import datetime

# Configure audit logger
audit_logger = logging.getLogger('jwt_audit')
audit_handler = logging.FileHandler('jwt_audit.log')
audit_formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
)
audit_handler.setFormatter(audit_formatter)
audit_logger.addHandler(audit_handler)
audit_logger.setLevel(logging.INFO)

def log_token_event(event_type, user_id, token_jti, additional_data=None):
    """Log JWT-related security events"""
    log_data = {
        'event': event_type,
        'user_id': user_id,
        'token_jti': token_jti,
        'timestamp': datetime.utcnow().isoformat(),
        'ip_address': request.remote_addr,
        'user_agent': request.headers.get('User-Agent'),
        'additional_data': additional_data or {}
    }

    audit_logger.info(f"JWT_EVENT: {log_data}")

# Integration with token operations
@app.route('/login', methods=['POST'])
def login_with_audit():
    # ... authentication logic ...

    access_token = create_access_token(identity=user_identity)
    token_data = get_jwt()

    # Log successful login
    log_token_event(
        'TOKEN_ISSUED',
        user.id,
        token_data['jti'],
        {'token_type': 'access', 'expires_at': token_data['exp']}
    )

    return jsonify({'access_token': access_token})

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout_with_audit():
    current_user = get_jwt_identity()
    token = get_jwt()

    # Log logout event
    log_token_event(
        'TOKEN_REVOKED',
        current_user['user_id'],
        token['jti'],
        {'reason': 'user_logout'}
    )

    TokenBlacklist.add_token_to_blacklist(
        token['jti'],
        datetime.fromtimestamp(token['exp'])
    )

    return jsonify({'message': 'Successfully logged out'})
```

## Key Security Takeaways

### JWT Best Practices Summary

{{< tip title="Essential JWT Security Checklist" >}}

1. **Short-lived Access Tokens**: 15-60 minutes maximum
2. **Secure Refresh Tokens**: Long-lived but revocable
3. **Token Blacklisting**: Support for immediate revocation
4. **HTTPS Transport**: Never send tokens over HTTP
5. **Secure Storage**: HttpOnly cookies or secure local storage
6. **Claims Validation**: Verify all token claims server-side
7. **Audit Logging**: Track all token operations
8. **Rate Limiting**: Prevent token-related abuse {{< /tip >}}

### Common JWT Security Mistakes

{{< warning title="Avoid These Pitfalls" >}}

- **Long-lived Access Tokens**: Increases security risk window
- **Client-side Secret Storage**: Never store secrets in frontend code
- **Missing Token Validation**: Always verify signature and claims
- **No Revocation Strategy**: Implement blacklisting for security incidents
- **Insufficient Logging**: Monitor token usage for suspicious activity
- **Weak Secret Keys**: Use cryptographically strong random keys
  {{< /warning >}}

## Production Deployment Considerations

```python
# Production-ready JWT configuration
class ProductionJWTConfig:
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)  # Short-lived
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)     # Reasonable refresh window

    # Security headers
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_HTTPONLY = True
    JWT_COOKIE_SAMESITE = 'Strict'
    JWT_COOKIE_CSRF_PROTECT = True

    # Algorithm specification (avoid 'none')
    JWT_ALGORITHM = 'HS256'

    # Token location preferences
    JWT_TOKEN_LOCATION = ['cookies', 'headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'

# Rate limiting for auth endpoints
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1000 per hour"]
)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # Prevent brute force
def login():
    # ... implementation ...
    pass
```

This comprehensive exploration of JWT security patterns demonstrates that while
JWTs are powerful, they require careful implementation to maintain security in
production applications.

---

_These JWT security insights from my archive highlight the evolution from simple
token-based auth to sophisticated security patterns that address real-world
attack vectors and compliance requirements._
