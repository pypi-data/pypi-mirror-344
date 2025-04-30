# pyzt

Life is short, I use Python.

`pyzt` is a Python library that provides a simple and efficient way to work with various tasks.
It is designed to be easy to use and flexible, allowing you to quickly implement and customize your tasks as needed.

## pyzt.auth

A reusable and secure Python authentication toolkit for JWT-based APIs and Applications.

### Features

- Create and verify JWT tokens (access and refresh tokens).
- Customizable `issuer` and `audience` and expiry and scopes.
- Defends against signature stripping, invalid types, and expired tokens.
- Secure password hashing with `argon2` or `bcrypt`.
- Zero-framework dependency — plug into any FastAPI, Flask, Django, or any other Python web frameworks, APIs, or even CLIs.


## Installation

```bash
uv add pyzt
```

## Usage

### 🔐 JWTAuth

```python
from pyzt.auth.jwt import JWTAuth

jwt_auth = JWTAuth(
    secret="your-secret",
    issuer="your-api",
    audience="your-app"
)

# Create a token with optional custom claims
access_token = jwt_auth.create_access_token("user@example.com", {
    "role": "admin",
    "scope": "read write"
})

# Validate token
payload = jwt_auth.decode_token(access_token, token_type="access")
```

### 🔁 Token Pair

```python
pair = jwt_auth.create_token_pair("user@example.com")
print(pair.access_token, pair.refresh_token)
```


### 🔒 Password Hashing

```python
from pyzt.auth.crypto import PasswordHasher

hasher = PasswordHasher("argon2")
hash = hasher.hash("mypassword")
assert hasher.verify("mypassword", hash)
```


## Models

```python
from pyzt.types.tokens import TokenPair, TokenPayload
```

## Security Coverage

- ✅ HS256 token signing
- ✅ Expiry checks
- ✅ Signature stripping attack defense
- ✅ Token type validation
- ✅ Role/scope claim support

## Testing

```bash
pytest tests/
```

## License
MIT
