from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from Models.auth import AuthContext
from Services.Security.JwtService import JwtService
from Utils.enums import AppModule


# scheme_name debe coincidir con BearerAuth en main.custom_openapi (botón Authorize de Swagger)
bearer_scheme = HTTPBearer(auto_error=False, scheme_name="BearerAuth")


def _normalize_modules(modules: list[str]) -> list[str]:
    from Utils.enums import ALL_MODULES

    if "all" in modules:
        return ALL_MODULES
    return modules


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> AuthContext:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación no provistas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        auth = JwtService.decode_token(credentials.credentials)
        return AuthContext(
            user_id=auth.user_id,
            email=auth.email,
            role_id=auth.role_id,
            role_name=auth.role_name,
            modules=_normalize_modules(auth.modules),
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_module(module: AppModule):
    def _checker(current_user: AuthContext = Depends(get_current_user)) -> AuthContext:
        if module.value not in _normalize_modules(current_user.modules):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No tiene permiso para acceder al módulo '{module.value}'",
            )
        return current_user

    return _checker
