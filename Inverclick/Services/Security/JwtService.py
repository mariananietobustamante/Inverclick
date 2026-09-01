import os
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from jwt import InvalidTokenError

from Models.auth import AuthContext

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "inverclick-dev-secret-change-in-production")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))


class JwtService:
    @staticmethod
    def create_access_token(auth: AuthContext) -> tuple[str, int]:
        expires_in = JWT_EXPIRE_MINUTES * 60
        expire_at = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)
        payload = {
            "sub": str(auth.user_id),
            "email": auth.email,
            "role_id": auth.role_id,
            "role": auth.role_name,
            "modules": auth.modules,
            "exp": expire_at,
        }
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return token, expires_in

    @staticmethod
    def decode_token(token: str) -> AuthContext:
        try:
            payload: dict[str, Any] = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            user_id = int(payload["sub"])
            return AuthContext(
                user_id=user_id,
                email=payload.get("email", ""),
                role_id=payload.get("role_id"),
                role_name=payload.get("role"),
                modules=list(payload.get("modules") or []),
            )
        except (InvalidTokenError, KeyError, TypeError, ValueError) as exc:
            raise ValueError("Token inválido o expirado") from exc
