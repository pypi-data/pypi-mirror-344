
# JWTManager - A Lightweight JWT Utility Package

JWTManager is a lightweight and simple Python utility package for handling JSON Web Tokens (JWT). 
It allows you to easily create, validate, and refresh JWT tokens, with built-in customizable expiration, multiple algorithms, and custom exception handling.

## Features
- Create JWT access tokens with customizable expiration
- Validate JWT tokens securely
- Refresh expired or about-to-expire tokens
- Supports HS256, HS384, HS512 algorithms
- Built-in logging for important events
- Custom exception handling for token errors

## Installation
```bash
pip install jwt_manager
```

## Usage
```python
from jwt_manager import JWTManager, InvalidTokenError

# Secret key
secret = "my_secret_key"

# Create a token
token = JWTManager.create_token({"user_id": 123}, secret, expiry_minutes=30)

# Validate the token
try:
    payload = JWTManager.validate_token(token, secret)
except InvalidTokenError:
    print("Token is invalid!")

# Refresh the token
new_token = JWTManager.refresh_token(token, secret, additional_minutes=60)
```

## License
This project is licensed under the MIT License.
