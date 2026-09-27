from sqlalchemy import func, select
from sqlalchemy.orm import Session

from Models.id_types import IdType


class IdTypesRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_type(self, type_code: str) -> IdType | None:
        normalized = type_code.strip().upper()
        statement = select(IdType).where(func.upper(IdType.type) == normalized)
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_id(self, id_type_id: int) -> IdType | None:
        statement = select(IdType).where(IdType.id == id_type_id)
        return self.db.execute(statement).scalar_one_or_none()
