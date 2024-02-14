import uuid
from datetime import datetime

from entities import User
from jose import jwt
from settings import settings


def _create_token(
    jwt_secret: str,
    algorithm: str,
    type: str,
    exp: datetime,
    iat: datetime,
    jti: str,
    **kwargs,
) -> str:
    token_payload = {
        "token_type": type,
        "exp": exp,
        "iat": iat,
        "jti": jti,
    }
    token_payload.update(kwargs)
    return jwt.encode(token_payload, jwt_secret, algorithm=algorithm)


def _create_user_token(token_type: str, user: User, exp: datetime) -> str:
    return _create_token(
        jwt_secret=settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
        type=token_type,
        exp=exp,
        iat=datetime.utcnow(),
        jti=str(uuid.uuid4()),
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        groups=user.groups,
    )


def get_custom_jwt(user: User) -> dict:
    access_token = _create_user_token(
        token_type="access",
        exp=datetime.utcnow() + settings.access_token_lifetime,
        user=user,
    )
    refresh_token = _create_user_token(
        token_type="refresh",
        exp=datetime.utcnow() + settings.refresh_token_lifetime,
        user=user,
    )
    return {
        "token": access_token,
        "access": access_token,
        "refresh": refresh_token,
    }
