from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from pwdlib import PasswordHash
from pwdlib.exceptions import UnknownHashError

from app.core.config import settings

password_hasher = PasswordHash.recommended()
DUMMY_HASH = password_hasher.hash("dummy-password-for-timing-only")


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


get_password_hash = hash_password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return password_hasher.verify(plain_password, hashed_password)
    except (ValueError, UnknownHashError):
        return False


def _signing_key() -> str:
    if settings.secret_key == "change-this-secret-key" or len(settings.secret_key.encode()) < 32:
        raise RuntimeError("Configure SECRET_KEY with at least 32 bytes before using authentication.")
    return settings.secret_key


def create_access_token(user_id: UUID) -> str:
    now = datetime.now(timezone.utc)
    return jwt.encode(
        {"sub": str(user_id), "iat": now,
         "exp": now + timedelta(minutes=settings.access_token_expire_minutes),
         "iss": "chicosense-api", "aud": "chicosense-api", "type": "access"},
        _signing_key(), algorithm="HS256",
    )


def decode_access_token(token: str) -> UUID:
    payload = jwt.decode(token, _signing_key(), algorithms=["HS256"],
                         audience="chicosense-api", issuer="chicosense-api",
                         options={"require": ["sub", "iat", "exp", "iss", "aud", "type"]})
    if payload["type"] != "access":
        raise jwt.InvalidTokenError("Invalid token type")
    try:
        return UUID(payload["sub"])
    except (ValueError, TypeError, AttributeError) as exc:
        raise jwt.InvalidTokenError("Invalid subject") from exc
