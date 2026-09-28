from fastapi import HTTPException


class AuthHttpResponses:
    @staticmethod
    def error_keycloak_not_configured(detail: str | None = None) -> HTTPException:
        return HTTPException(
            status_code=503,
            detail=detail or "Integración Keycloak no configurada en el servidor",
        )

    @staticmethod
    def error_keycloak_communication(detail: str | None = None) -> HTTPException:
        return HTTPException(
            status_code=502,
            detail=detail or "Error al comunicarse con el proveedor de identidad Keycloak",
        )

    @staticmethod
    def error_invalid_grant(detail: str | None = None) -> HTTPException:
        return HTTPException(
            status_code=400,
            detail=detail
            or (
                "El código OAuth ya se usó o expiró. "
                "Abre de nuevo http://127.0.0.1:8000/auth/keycloak (no refresques el callback)."
            ),
        )

    @staticmethod
    def error_missing_authorization_code() -> HTTPException:
        return HTTPException(
            status_code=400,
            detail="Falta el código de autorización de Keycloak (query param 'code')",
        )

    @staticmethod
    def error_invalid_oauth_state() -> HTTPException:
        return HTTPException(
            status_code=400,
            detail="Parámetro 'state' inválido o expirado (posible ataque CSRF)",
        )

    @staticmethod
    def error_account_inactive() -> HTTPException:
        return HTTPException(status_code=403, detail="La cuenta de usuario se encuentra inactiva")

    @staticmethod
    def error_role_not_assigned() -> HTTPException:
        return HTTPException(status_code=403, detail="El usuario no tiene un rol asignado")

    @staticmethod
    def error_role_without_modules() -> HTTPException:
        return HTTPException(status_code=403, detail="El rol del usuario no tiene módulos asignados")

    @staticmethod
    def error_user_not_found() -> HTTPException:
        return HTTPException(status_code=404, detail="Usuario no encontrado")
