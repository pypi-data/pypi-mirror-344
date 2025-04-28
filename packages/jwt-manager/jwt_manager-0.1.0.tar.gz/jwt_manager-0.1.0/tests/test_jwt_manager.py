
import pytest
from jwt_manager import JWTManager, InvalidTokenError, ExpiredTokenError
import time

SECRET = "test_secret_key"

def test_token_creation_and_validation():
    payload = {"user_id": 1}
    token = JWTManager.create_token(payload, SECRET, expiry_minutes=1)
    decoded = JWTManager.validate_token(token, SECRET)
    assert decoded["user_id"] == 1

def test_token_expiration():
    payload = {"user_id": 2}
    token = JWTManager.create_token(payload, SECRET, expiry_minutes=0)
    time.sleep(2)
    with pytest.raises(ExpiredTokenError):
        JWTManager.validate_token(token, SECRET)

def test_token_refresh():
    payload = {"user_id": 3}
    token = JWTManager.create_token(payload, SECRET, expiry_minutes=1)
    new_token = JWTManager.refresh_token(token, SECRET, additional_minutes=5)
    decoded = JWTManager.validate_token(new_token, SECRET)
    assert decoded["user_id"] == 3
