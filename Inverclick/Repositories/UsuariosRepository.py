from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from Models.id_types import IdType
from Models.users import UserDTO


class UsersRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> UserDTO | None:
        statement = select(UserDTO).where(UserDTO.id == user_id)
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_email(self, email: str) -> UserDTO | None:
        statement = select(UserDTO).where(UserDTO.email == email)
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_identification(self, identification: str, identification_type: str) -> UserDTO | None:
        statement = (
            select(UserDTO)
            .join(IdType, UserDTO.id_type_id == IdType.id)
            .where(UserDTO.id_number == identification, IdType.type == identification_type)
        )
        return self.db.execute(statement).scalar_one_or_none()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[UserDTO]:
        statement = select(UserDTO).offset(skip).limit(limit)
        return list(self.db.execute(statement).scalars().all())

    def create(self, user_dto: UserDTO) -> UserDTO:
        self.db.add(user_dto)
        self.db.commit()
        self.db.refresh(user_dto)
        return user_dto

    def update(self, user_id: int, user_dto: UserDTO | dict[str, Any]) -> UserDTO | None:
        db_user = self.get_by_id(user_id)
        if db_user:
            if isinstance(user_dto, dict):
                for key, value in user_dto.items():
                    if value is not None and hasattr(db_user, key):
                        setattr(db_user, key, value)
            else:
                for key, value in user_dto.__dict__.items():
                    if not key.startswith("_") and value is not None and hasattr(db_user, key):
                        setattr(db_user, key, value)
            self.db.commit()
            self.db.refresh(db_user)
        return db_user

    def delete(self, user_id: int) -> bool:
        db_user = self.get_by_id(user_id)
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
            return True
        return False
