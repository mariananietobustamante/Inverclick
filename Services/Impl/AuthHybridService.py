"""Orquesta autenticación híbrida: Keycloak + perfil local + JWT unificado."""

from __future__ import annotations

from datetime import datetime, timezone

from Models.auth import AuthContext, LoginTokenResponseSchema
from Models.users import UserDTO
from Models.users_login import UserLoginDTO
from Repositories.IUsersLoginRepository import IUsersLoginRepository
from Repositories.IUsersRoleRepository import IUsersRoleRepository
from Repositories.IUsuariosRepository import IUsuariosRepository
from Services.Security.JwtService import JwtService
from Services.Security.KeycloakService import (
    KeycloakCommunicationError,
    KeycloakConfigError,
    KeycloakInvalidGrantError,
    KeycloakService,
    KeycloakUserInfo,
)
from Utils.enums import ALL_MODULES, AppModule, AuthProvider
from Utils.HttpResponses.authHttpResponses import AuthHttpResponses

SSO_DEFAULT_ROLE_NAME = "Usuario"
SSO_DEFAULT_MODULES = [AppModule.USERS.value, AppModule.PREFIX.value]


class AuthHybridService:
    def __init__(
        self,
        users_repository: IUsuariosRepository,
        login_repository: IUsersLoginRepository,
        roles_repository: IUsersRoleRepository,
        keycloak_service: KeycloakService | None = None,
        http_responses: AuthHttpResponses | None = None,
    ):
        self.users_repository = users_repository
        self.login_repository = login_repository
        self.roles_repository = roles_repository
        self.keycloak = keycloak_service or KeycloakService()
        self.http = http_responses or AuthHttpResponses()

    @staticmethod
    def _normalize_modules(modules: list[str]) -> list[str]:
        if "all" in modules:
            return ALL_MODULES
        return modules

    def get_keycloak_login_url(self) -> str:
        try:
            self.keycloak.ensure_configured()
        except KeycloakConfigError as exc:
            raise self.http.error_keycloak_not_configured(str(exc)) from exc
        return self.keycloak.build_authorization_url()

    def handle_keycloak_callback(self, code: str | None, state: str | None) -> LoginTokenResponseSchema:
        if not code:
            raise self.http.error_missing_authorization_code()
        if not self.keycloak.validate_state(state):
            raise self.http.error_invalid_oauth_state()

        try:
            kc_user = self.keycloak.authenticate_with_code(code)
        except KeycloakConfigError as exc:
            raise self.http.error_keycloak_not_configured(str(exc)) from exc
        except KeycloakInvalidGrantError as exc:
            raise self.http.error_invalid_grant(str(exc)) from exc
        except KeycloakCommunicationError as exc:
            raise self.http.error_keycloak_communication(str(exc)) from exc

        user, login = self._resolve_or_provision_user(kc_user)

        if not login.is_active:
            raise self.http.error_account_inactive()
        if not user.role_id:
            raise self.http.error_role_not_assigned()

        auth_context = self._build_auth_context(user)
        if not auth_context.modules:
            raise self.http.error_role_without_modules()

        access_token, expires_in = JwtService.create_access_token(auth_context)

        self.login_repository.update(
            login.id,
            {
                "last_login_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc),
                "external_id": kc_user.external_id,
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

    def _build_auth_context(self, user: UserDTO) -> AuthContext:
        role_name = None
        modules: list[str] = []
        if user.role_id:
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

    def _ensure_default_sso_role_id(self) -> int:
        role = self.roles_repository.get_by_role(SSO_DEFAULT_ROLE_NAME)
        if role is None:
            from Models.users_role import UserRoleDTO

            role = self.roles_repository.create(
                UserRoleDTO(
                    role=SSO_DEFAULT_ROLE_NAME,
                    modules=SSO_DEFAULT_MODULES,
                    created_at=datetime.now(timezone.utc),
                )
            )
        return role.id

    def _resolve_or_provision_user(
        self, kc_user: KeycloakUserInfo
    ) -> tuple[UserDTO, UserLoginDTO]:
        login = self.login_repository.get_by_external_id(kc_user.external_id)
        if login is not None:
            user = self.users_repository.get_by_id(login.user_id)
            if user is None:
                raise self.http.error_user_not_found()
            return user, login

        user = self.users_repository.get_by_email(kc_user.email)
        now = datetime.now(timezone.utc)

        if user is None:
            first_name = (kc_user.given_name or kc_user.name or kc_user.email.split("@")[0]).strip()
            last_name = (kc_user.family_name or "").strip() or None
            user = self.users_repository.create(
                UserDTO(
                    name=first_name[:100] or "Usuario",
                    surname=last_name,
                    email=kc_user.email,
                    role_id=self._ensure_default_sso_role_id(),
                    description="Cuenta creada automáticamente vía Keycloak SSO",
                    created_at=now,
                    updated_at=now,
                )
            )
            login = self.login_repository.create(
                UserLoginDTO(
                    user_id=user.id,
                    password_hash=None,
                    is_active=True,
                    auth_provider=AuthProvider.KEYCLOAK.value,
                    external_id=kc_user.external_id,
                    created_at=now,
                    updated_at=now,
                )
            )
            return user, login

        login = self.login_repository.get_by_user_id(user.id)
        if login is None:
            login = self.login_repository.create(
                UserLoginDTO(
                    user_id=user.id,
                    password_hash=None,
                    is_active=True,
                    auth_provider=AuthProvider.KEYCLOAK.value,
                    external_id=kc_user.external_id,
                    created_at=now,
                    updated_at=now,
                )
            )
        else:
            updates: dict = {
                "external_id": kc_user.external_id,
                "updated_at": now,
            }
            if login.auth_provider == AuthProvider.LOCAL.value and login.password_hash:
                updates["auth_provider"] = AuthProvider.HYBRID.value
            elif not login.password_hash:
                updates["auth_provider"] = AuthProvider.KEYCLOAK.value
            login = self.login_repository.update(login.id, updates) or login

            if not user.role_id:
                self.users_repository.update(
                    user.id,
                    {"role_id": self._ensure_default_sso_role_id(), "updated_at": now},
                )
                user = self.users_repository.get_by_id(user.id) or user

        return user, login
