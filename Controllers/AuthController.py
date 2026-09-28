from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from sqlalchemy.orm import Session

from Models.auth import LoginTokenResponseSchema
from Repositories.database import get_db
from Repositories.UsersLoginRepository import UsersLoginRepository
from Repositories.UsersRoleRepository import UsersRoleRepository
from Repositories.UsuariosRepository import UsersRepository
from Services.Impl.AuthHybridService import AuthHybridService
from Services.Security.KeycloakService import KeycloakService

router = APIRouter(prefix="/auth", tags=["Auth / SSO"])


def get_auth_hybrid_service(db: Session = Depends(get_db)) -> AuthHybridService:
    return AuthHybridService(
        users_repository=UsersRepository(db),
        login_repository=UsersLoginRepository(db),
        roles_repository=UsersRoleRepository(db),
        keycloak_service=KeycloakService(),
    )


@router.get("/keycloak")
def keycloak_login(service: AuthHybridService = Depends(get_auth_hybrid_service)):
    """
    Redirige al usuario al servidor Keycloak (Authorization Code Flow).
    Endpoint público — no altera el login local ni los módulos protegidos.
    """
    return RedirectResponse(url=service.get_keycloak_login_url(), status_code=302)


@router.get("/keycloak/callback")
def keycloak_callback(
    request: Request,
    code: str | None = Query(default=None),
    state: str | None = Query(default=None),
    service: AuthHybridService = Depends(get_auth_hybrid_service),
):
    """
    Callback OAuth: intercambia el code por identidad Keycloak,
    aprovisiona el perfil local si es necesario y emite el JWT local unificado.

    En navegador responde HTML y limpia el `code` de la URL (evita invalid_grant al refrescar).
    """
    token_response: LoginTokenResponseSchema = service.handle_keycloak_callback(
        code=code, state=state
    )
    accept = (request.headers.get("accept") or "").lower()
    wants_html = "text/html" in accept and "application/json" not in accept.split(",")[0]

    if wants_html:
        payload = token_response.model_dump_json(indent=2)
        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8"/>
  <title>Inverclick — SSO OK</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 720px; margin: 2rem auto; padding: 0 1rem; }}
    pre {{ background: #f4f4f4; padding: 1rem; overflow: auto; border-radius: 8px; }}
    a {{ color: #0b5fff; }}
  </style>
</head>
<body>
  <h1>Inicio de sesión SSO exitoso</h1>
  <p>Copia el <code>access_token</code> para usarlo en Swagger (Authorize).</p>
  <p><a href="/docs">Abrir Swagger</a> · <a href="/auth/keycloak">Volver a iniciar SSO</a></p>
  <pre id="token">{payload}</pre>
  <script>
    // Quita code/state de la barra de direcciones para que F5 no reutilice el code.
    if (window.history && window.history.replaceState) {{
      window.history.replaceState({{}}, document.title, "/auth/done");
    }}
  </script>
</body>
</html>"""
        return HTMLResponse(content=html, status_code=200)

    return JSONResponse(content=token_response.model_dump(), status_code=200)


@router.get("/done", response_class=HTMLResponse)
def auth_done():
    """Página limpia tras SSO (sin code en la URL). Evita invalid_grant al refrescar."""
    return """<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"/><title>Inverclick — SSO</title></head>
<body style="font-family:system-ui;max-width:640px;margin:2rem auto;padding:0 1rem">
  <h1>Sesión SSO ya procesada</h1>
  <p>Si necesitas un token nuevo, inicia de nuevo (no uses la URL vieja del callback):</p>
  <p><a href="/auth/keycloak">Iniciar SSO otra vez</a> · <a href="/docs">Swagger</a></p>
</body>
</html>"""
