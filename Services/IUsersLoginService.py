from Models.auth import LoginTokenResponseSchema
from Models.users_login import (
    LoginRequestSchema,
    UserLoginCreateSchema,
    UserLoginResponseSchema,
    UserLoginUpdateSchema,
)


class IUsersLoginService:
    def get_by_id(self, login_id: int) -> UserLoginResponseSchema:
        pass

    def get_by_user_id(self, user_id: int) -> UserLoginResponseSchema:
        pass

    def get_by_email(self, email: str) -> UserLoginResponseSchema:
        pass

    def get_all(self, skip: int = 0, limit: int = 100) -> list[UserLoginResponseSchema]:
        pass

    def create(self, schema: UserLoginCreateSchema) -> UserLoginResponseSchema:
        pass

    def update(self, login_id: int, schema: UserLoginUpdateSchema) -> UserLoginResponseSchema:
        pass

    def delete(self, login_id: int) -> bool:
        pass

    def authenticate(self, credentials: LoginRequestSchema) -> LoginTokenResponseSchema:
        pass
