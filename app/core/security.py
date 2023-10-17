from datetime import datetime, timedelta
from jose import JWTError, jwt  # type: ignore
from passlib.context import CryptContext  # type: ignore
from app.core.config import settings
from app.core.exceptions import Unauthenticated
from typing import Any

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Jwt:
    @staticmethod
    def _encode_token(claims: dict[str, Any]) -> str:
        return jwt.encode(
            claims, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )

    @staticmethod
    def _decode_token(token: str, is_access: bool) -> dict[str, Any]:
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            if is_access != payload["access"]:
                raise Unauthenticated("Could not validate credentials")

            return payload
        except JWTError:
            raise Unauthenticated("Could not validate credentials")

    @classmethod
    def get_access_token(cls, sub: Any) -> str:
        expire_time = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_IN_MINUTES,
        )
        expire = datetime.utcnow() + expire_time
        to_encode = {"sub": sub, "exp": expire, "access": True}
        return cls._encode_token(to_encode)

    @classmethod
    def get_refresh_token(cls, sub: Any) -> str:
        expire_time = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_IN_DAYS)
        expire = datetime.utcnow() + expire_time
        to_encode = {"sub": sub, "exp": expire, "access": False}
        return cls._encode_token(to_encode)

    @classmethod
    def decode_access_token(cls, token: str) -> dict[str, Any]:
        return cls._decode_token(token, is_access=True)

    @classmethod
    def decode_refresh_token(cls, token: str) -> dict[str, Any]:
        return cls._decode_token(token, is_access=False)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
