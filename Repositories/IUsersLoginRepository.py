from typing import Any

from Models.users_login import UserLoginDTO


class IUsersLoginRepository:
    def get_by_id(self, login_id: int) -> UserLoginDTO | None:
        pass

    def get_by_user_id(self, user_id: int) -> UserLoginDTO | None:
        pass

    def get_by_external_id(self, external_id: str) -> UserLoginDTO | None:
        pass

    def get_all(self, skip: int = 0, limit: int = 100) -> list[UserLoginDTO]:
        pass

    def create(self, login_dto: UserLoginDTO) -> UserLoginDTO:
        pass

    def update(self, login_id: int, login_dto: UserLoginDTO | dict[str, Any]) -> UserLoginDTO | None:
        pass

    def delete(self, login_id: int) -> bool:
        pass
