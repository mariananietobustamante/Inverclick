from datetime import datetime, timezone

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from Repositories.AuditLogRepository import AuditLogRepository
from Repositories.database import SessionLocal
from Services.Security.JwtService import JwtService

AUDIT_ACTION_BY_METHOD = {
    "POST": "Creación",
    "PUT": "Edición",
    "DELETE": "Eliminación",
}

TARGET_MODULES = ("/construction-companies", "/real-estate", "/leads", "/sales")


class AuditLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        if request.method in AUDIT_ACTION_BY_METHOD:
            path = request.url.path
            if any(module in path for module in TARGET_MODULES):
                self._save_log(request, path)

        return response

    def _save_log(self, request: Request, path: str) -> None:
        user_id = None
        auth_header = request.headers.get("Authorization")
        db = SessionLocal()
        try:
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ", 1)[1]
                try:
                    auth = JwtService.decode_token(token)
                    user_id = auth.user_id
                except ValueError:
                    user_id = None

            repository = AuditLogRepository(db)
            repository.create(
                user_id=user_id,
                action=AUDIT_ACTION_BY_METHOD.get(request.method, request.method),
                route=path,
            )
        except Exception:
            db.rollback()
        finally:
            db.close()
