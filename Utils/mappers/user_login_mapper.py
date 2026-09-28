from Models.users_login import UserLoginDTO, UserLoginResponseSchema


def to_login_response(login: UserLoginDTO, email: str | None = None) -> UserLoginResponseSchema:
    return UserLoginResponseSchema(
        id=login.id,
        user_id=login.user_id,
        email=email,
        created_at=login.created_at,
        updated_at=login.updated_at,
        active=login.is_active,
        auth_provider=getattr(login, "auth_provider", None) or "local",
        external_id=getattr(login, "external_id", None),
        has_local_password=bool(login.password_hash),
    )
