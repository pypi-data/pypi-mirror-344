
import jwt
import datetime
import logging
from .exceptions import InvalidTokenError, ExpiredTokenError, SignatureVerificationError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("JWTManager")

class JWTManager:
    @staticmethod
    def create_token(payload: dict, secret: str, expiry_minutes: int = 30, algorithm: str = "HS256") -> str:
        payload = payload.copy()
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=expiry_minutes)
        payload.update({"exp": expire})
        token = jwt.encode(payload, secret, algorithm=algorithm)
        logger.info("Access token created successfully.")
        return token

    @staticmethod
    def validate_token(token: str, secret: str, algorithms: list = ["HS256"]) -> dict:
        try:
            payload = jwt.decode(token, secret, algorithms=algorithms)
            logger.info("Token validated successfully.")
            return payload
        except jwt.ExpiredSignatureError:
            logger.error("Token has expired.")
            raise ExpiredTokenError("Token has expired.")
        except jwt.InvalidSignatureError:
            logger.error("Token signature verification failed.")
            raise SignatureVerificationError("Invalid signature.")
        except jwt.InvalidTokenError:
            logger.error("Invalid token provided.")
            raise InvalidTokenError("Invalid token.")

    @staticmethod
    def refresh_token(old_token: str, secret: str, additional_minutes: int = 30, algorithm: str = "HS256") -> str:
        try:
            payload = jwt.decode(old_token, secret, algorithms=[algorithm], options={"verify_exp": False})
            new_expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=additional_minutes)
            payload.update({"exp": new_expire})
            refreshed_token = jwt.encode(payload, secret, algorithm=algorithm)
            logger.info("Token refreshed successfully.")
            return refreshed_token
        except jwt.InvalidTokenError:
            logger.error("Invalid token provided for refresh.")
            raise InvalidTokenError("Cannot refresh an invalid token.")
