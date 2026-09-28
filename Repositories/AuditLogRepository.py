from datetime import datetime, timezone

from sqlalchemy.orm import Session

from Models.audit_logs import AuditLogDTO


class AuditLogRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int | None, action: str, route: str) -> AuditLogDTO:
        log_entry = AuditLogDTO(
            user_id=user_id,
            action=action,
            route=route,
            created_at=datetime.now(timezone.utc),
        )
        self.db.add(log_entry)
        self.db.commit()
        self.db.refresh(log_entry)
        return log_entry
