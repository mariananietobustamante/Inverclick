from datetime import datetime, timezone
from typing import Any

from Models.auth import AuthContext, LoginTokenResponseSchema
from Models.users import UserDTO
from Models.users_login import (
    LoginRequestSchema,
    UserLoginCreateSchema,
    UserLoginDTO,
    UserLoginResponseSchema,
    UserLoginUpdateSchema,
)
from Repositories.IUsersLoginRepository import IUsersLoginRepository
from Repositories.IUsuariosRepository import IUsuariosRepository
from Repositories.UsersRoleRepository import UsersRoleRepository
from Services.Security.CryptPass import get_password_hash, verify_password
from Services.Security.JwtService import JwtService
from Utils.HttpResponses.userLoginHttpResponses import UserLoginHttpResponses
from Utils.enums import ALL_MODULES, AuthProvider
from Utils.mappers.user_login_mapper import to_login_response
from Utils.user_login_validator import UserLoginValidator


class UsersLoginService:
    def __init__(
        self,
        repository: IUsersLoginRepository,
        http_responses: UserLoginHttpResponses,
        validator: UserLoginValidator,
        users_repository: IUsuariosRepository | None = None,
        roles_repository: UsersRoleRepository | None = None,
    ):
        self.repository = repository
        self.http_responses = http_responses
        self.validator = validator
        self.users_repository = users_repository
        self.roles_repository = roles_repository

    @staticmethod
    def _normalize_modules(modules: list[str]) -> list[str]:
        if "all" in modules:
            return ALL_MODULES
        return modules

    def _build_auth_context(self, user: UserDTO) -> AuthContext:
        role_name = None
        modules: list[str] = []
        if user.role_id and self.roles_repository:
            role = self.roles_repository.get_by_id(user.role_id)
            if role:
                role_name = role.role
                modules = self._normalize_modules(list(role.modules or []))
        return AuthContext(
            user_id=user.id,
            email=user.email,
            role_id=user.role_id,
            role_name=role_name,
            modules=modules,
        )

    def _to_response(self, login: UserLoginDTO, email: str | None = None) -> UserLoginResponseSchema:
        if email is None and self.users_repository:
            user = self.users_repository.get_by_id(login.user_id)
            email = user.email if user else None
        return to_login_response(login, email=email)

    def get_by_id(self, login_id: int) -> UserLoginResponseSchema:
        login = self.repository.get_by_id(login_id)
        if login is None:
            raise self.http_responses.error_login_not_found()
        return self._to_response(login)

    def get_by_user_id(self, user_id: int) -> UserLoginResponseSchema:
        login = self.repository.get_by_user_id(user_id)
        if login is None:
            raise self.http_responses.error_login_not_found()
        return self._to_response(login)

    def get_by_email(self, email: str) -> UserLoginResponseSchema:
        if self.users_repository is None:
            raise self.http_responses.error_user_not_found()
        user = self.users_repository.get_by_email(email)
        if user is None:
            raise self.http_responses.error_user_not_found()
        login = self.repository.get_by_user_id(user.id)
        if login is None:
            raise self.http_responses.error_login_not_found()
        return self._to_response(login, email=user.email)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[UserLoginResponseSchema]:
        logins = self.repository.get_all(skip, limit)
        return [self._to_response(login) for login in logins]

    def create(self, schema: UserLoginCreateSchema) -> UserLoginResponseSchema:
        invalid = self.validator.validate_user_login_dto_lengths(schema.model_dump(exclude_none=True))
        if invalid:
            field, min_len, max_len = invalid
            raise self.http_responses.error_invalid_length(field, min_len, max_len)

        if self.users_repository and self.users_repository.get_by_id(schema.user_id) is None:
            raise self.http_responses.error_user_not_found()

        if self.repository.get_by_user_id(schema.user_id) is not None:
            raise self.http_responses.error_login_already_exists()

        now = datetime.now(timezone.utc)
        login = UserLoginDTO(
            user_id=schema.user_id,
            password_hash=get_password_hash(schema.user_password),
            is_active=schema.active if schema.active is not None else True,
            auth_provider=AuthProvider.LOCAL.value,
            external_id=None,
            created_at=now,
            updated_at=now,
        )
        created = self.repository.create(login)
        return self._to_response(created)

    def update(self, login_id: int, schema: UserLoginUpdateSchema) -> UserLoginResponseSchema:
        payload: dict[str, Any] = {}
        if schema.user_password is not None:
            payload["password_hash"] = get_password_hash(schema.user_password)
        if schema.active is not None:
            payload["is_active"] = schema.active

        if schema.user_password is not None:
            invalid = self.validator.validate_user_login_dto_lengths({"user_password": schema.user_password})
            if invalid:
                field, min_len, max_len = invalid
                raise self.http_responses.error_invalid_length(field, min_len, max_len)

        payload["updated_at"] = datetime.now(timezone.utc)
        login = self.repository.update(login_id, payload)
        if login is None:
            raise self.http_responses.error_login_not_updated()
        return self._to_response(login)

    def delete(self, login_id: int) -> bool:
        success = self.repository.delete(login_id)
        if not success:
            raise self.http_responses.error_login_not_deleted()
        return success

    def authenticate(self, credentials: LoginRequestSchema) -> LoginTokenResponseSchema:
        if self.users_repository is None:
            raise self.http_responses.error_invalid_credentials()

        email = str(credentials.email)
        user = self.users_repository.get_by_email(email)
        if user is None:
            raise self.http_responses.error_invalid_credentials()

        login = self.repository.get_by_user_id(user.id)
        if login is None or not login.password_hash:
            raise self.http_responses.error_invalid_credentials()

        if not verify_password(credentials.user_password, login.password_hash):
            raise self.http_responses.error_invalid_credentials()

        if not login.is_active:
            raise self.http_responses.error_account_inactive()

        if not user.role_id:
            raise self.http_responses.error_role_not_assigned()

        auth_context = self._build_auth_context(user)
        if not auth_context.modules:
            raise self.http_responses.error_role_without_modules()

        access_token, expires_in = JwtService.create_access_token(auth_context)

        self.repository.update(
            login.id,
            {
                "last_login_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc),
            },
        )

        return LoginTokenResponseSchema(
            access_token=access_token,
            token_type="bearer",
            expires_in=expires_in,
            user_id=user.id,
            email=user.email,
            role=auth_context.role_name,
            modules=auth_context.modules,
        )
