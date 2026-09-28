from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from Models.users_login import UserLoginDTO


class UsersLoginRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, login_id: int) -> UserLoginDTO | None:
        statement = select(UserLoginDTO).where(UserLoginDTO.id == login_id)
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_user_id(self, user_id: int) -> UserLoginDTO | None:
        statement = select(UserLoginDTO).where(UserLoginDTO.user_id == user_id)
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_external_id(self, external_id: str) -> UserLoginDTO | None:
        statement = select(UserLoginDTO).where(UserLoginDTO.external_id == external_id)
        return self.db.execute(statement).scalar_one_or_none()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[UserLoginDTO]:
        statement = select(UserLoginDTO).offset(skip).limit(limit)
        return list(self.db.execute(statement).scalars().all())

    def create(self, login_dto: UserLoginDTO) -> UserLoginDTO:
        self.db.add(login_dto)
        self.db.commit()
        self.db.refresh(login_dto)
        return login_dto

    def update(self, login_id: int, login_dto: UserLoginDTO | dict[str, Any]) -> UserLoginDTO | None:
        db_login = self.get_by_id(login_id)
        if db_login:
            if isinstance(login_dto, dict):
                data = login_dto
            else:
                data = {k: v for k, v in login_dto.__dict__.items() if not k.startswith("_")}
            for key, value in data.items():
                if value is not None and hasattr(db_login, key):
                    setattr(db_login, key, value)
            self.db.commit()
            self.db.refresh(db_login)
        return db_login

    def delete(self, login_id: int) -> bool:
        db_login = self.get_by_id(login_id)
        if db_login:
            self.db.delete(db_login)
            self.db.commit()
            return True
        return False
