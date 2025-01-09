from datetime import UTC
from datetime import datetime
from datetime import timedelta
from uuid import uuid4

import jwt

from src.entities import User
from src.settings import settings


def _create_user_token(token_type: str, user: User, lifetime: timedelta) -> str:
    now = datetime.now(UTC)
    token_payload = {
        "token_type": token_type,
        "exp": now + lifetime,
        "iat": now,
        "jti": str(uuid4()),
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "groups": user.groups,
    }
    return jwt.encode(
        token_payload, settings.jwt_secret, algorithm=settings.jwt_algorithm
    )


def get_custom_jwt(user: User) -> dict:
    access_token = _create_user_token(
        token_type="access",
        lifetime=settings.access_token_lifetime,
        user=user,
    )
    refresh_token = _create_user_token(
        token_type="refresh",
        lifetime=settings.refresh_token_lifetime,
        user=user,
    )
    return {
        "token": access_token,
        "access": access_token,
        "refresh": refresh_token,
    }
