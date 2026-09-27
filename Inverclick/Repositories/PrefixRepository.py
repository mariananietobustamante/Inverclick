from sqlalchemy import select
from sqlalchemy.orm import Session

from Models.prefix import Prefix


class PrefixRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, prefix_id: int) -> Prefix | None:
        statement = select(Prefix).where(Prefix.id == prefix_id)
        return self.db.execute(statement).scalar_one_or_none()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Prefix]:
        statement = select(Prefix).offset(skip).limit(limit)
        return list(self.db.execute(statement).scalars().all())

    def get_by_prefix(self, prefix: str) -> Prefix | None:
        statement = select(Prefix).where(Prefix.prefix == prefix)
        return self.db.execute(statement).scalar_one_or_none()
