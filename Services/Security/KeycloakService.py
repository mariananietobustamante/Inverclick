"""Comunicación con Keycloak (OAuth 2.0 Authorization Code). Aislado de la lógica de negocio."""

from __future__ import annotations

import base64
import hashlib
import hmac
import os
import time
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode

import httpx


class KeycloakConfigError(RuntimeError):
    """Configuración de Keycloak incompleta o inválida."""


class KeycloakCommunicationError(RuntimeError):
    """Error al comunicarse con el servidor Keycloak."""


class KeycloakInvalidGrantError(KeycloakCommunicationError):
    """El authorization code es inválido, expiró o ya fue usado."""


@dataclass(frozen=True)
class KeycloakUserInfo:
    external_id: str
    email: str
    name: str | None
    given_name: str | None
    family_name: str | None


class KeycloakService:
    """Encapsula autorización, intercambio de código y userinfo de Keycloak."""

    STATE_TTL_SECONDS = 600

    def __init__(
        self,
        server_url: str | None = None,
        realm: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        redirect_uri: str | None = None,
        state_secret: str | None = None,
    ):
        self.server_url = (server_url or os.getenv("KEYCLOAK_SERVER_URL", "")).rstrip("/")
        self.realm = realm or os.getenv("KEYCLOAK_REALM", "")
        self.client_id = client_id or os.getenv("KEYCLOAK_CLIENT_ID", "")
        self.client_secret = client_secret or os.getenv("KEYCLOAK_CLIENT_SECRET", "")
        self.redirect_uri = redirect_uri or os.getenv(
            "KEYCLOAK_REDIRECT_URI",
            "http://127.0.0.1:8000/auth/keycloak/callback",
        )
        self.state_secret = state_secret or os.getenv(
            "KEYCLOAK_STATE_SECRET",
            os.getenv("JWT_SECRET_KEY", "inverclick-dev-secret-change-in-production"),
        )

    def ensure_configured(self) -> None:
        missing = [
            name
            for name, value in (
                ("KEYCLOAK_SERVER_URL", self.server_url),
                ("KEYCLOAK_REALM", self.realm),
                ("KEYCLOAK_CLIENT_ID", self.client_id),
                ("KEYCLOAK_CLIENT_SECRET", self.client_secret),
                ("KEYCLOAK_REDIRECT_URI", self.redirect_uri),
            )
            if not value
        ]
        if missing:
            raise KeycloakConfigError(
                f"Configuración Keycloak incompleta. Faltan: {', '.join(missing)}"
            )

    @property
    def _realm_base(self) -> str:
        return f"{self.server_url}/realms/{self.realm}"

    @property
    def authorization_endpoint(self) -> str:
        return f"{self._realm_base}/protocol/openid-connect/auth"

    @property
    def token_endpoint(self) -> str:
        return f"{self._realm_base}/protocol/openid-connect/token"

    @property
    def userinfo_endpoint(self) -> str:
        return f"{self._realm_base}/protocol/openid-connect/userinfo"

    def create_state(self) -> str:
        """Estado firmado (CSRF) con marca de tiempo."""
        timestamp = str(int(time.time()))
        signature = hmac.new(
            self.state_secret.encode("utf-8"),
            timestamp.encode("utf-8"),
            hashlib.sha256,
        ).digest()
        token = f"{timestamp}.{base64.urlsafe_b64encode(signature).decode('ascii')}"
        return token

    def validate_state(self, state: str | None) -> bool:
        if not state or "." not in state:
            return False
        timestamp_str, signature_b64 = state.split(".", 1)
        try:
            timestamp = int(timestamp_str)
        except ValueError:
            return False
        if abs(int(time.time()) - timestamp) > self.STATE_TTL_SECONDS:
            return False
        expected = hmac.new(
            self.state_secret.encode("utf-8"),
            timestamp_str.encode("utf-8"),
            hashlib.sha256,
        ).digest()
        try:
            provided = base64.urlsafe_b64decode(signature_b64.encode("ascii"))
        except (ValueError, TypeError):
            return False
        return hmac.compare_digest(expected, provided)

    def build_authorization_url(self, state: str | None = None) -> str:
        self.ensure_configured()
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "scope": "openid email profile",
            "redirect_uri": self.redirect_uri,
            "state": state or self.create_state(),
        }
        return f"{self.authorization_endpoint}?{urlencode(params)}"

    def exchange_code_for_tokens(self, code: str) -> dict[str, Any]:
        """Intercambia el authorization code por tokens de Keycloak."""
        self.ensure_configured()
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        try:
            with httpx.Client(timeout=20.0) as client:
                response = client.post(
                    self.token_endpoint,
                    data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )
        except httpx.HTTPError as exc:
            raise KeycloakCommunicationError(f"No se pudo contactar Keycloak: {exc}") from exc

        if response.status_code >= 400:
            body = response.text
            if response.status_code == 400 and "invalid_grant" in body:
                raise KeycloakInvalidGrantError(
                    "El código OAuth de Keycloak no es válido, expiró o ya se usó. "
                    "No refresques la URL del callback: vuelve a iniciar en GET /auth/keycloak."
                )
            raise KeycloakCommunicationError(
                f"Keycloak rechazó el intercambio de código (HTTP {response.status_code}): {body}"
            )
        payload = response.json()
        if "access_token" not in payload:
            raise KeycloakCommunicationError("Respuesta de Keycloak sin access_token")
        return payload

    def fetch_userinfo(self, access_token: str) -> KeycloakUserInfo:
        """Obtiene el perfil del usuario autenticado en Keycloak."""
        self.ensure_configured()
        try:
            with httpx.Client(timeout=20.0) as client:
                response = client.get(
                    self.userinfo_endpoint,
                    headers={"Authorization": f"Bearer {access_token}"},
                )
        except httpx.HTTPError as exc:
            raise KeycloakCommunicationError(f"No se pudo obtener userinfo: {exc}") from exc

        if response.status_code >= 400:
            raise KeycloakCommunicationError(
                f"Keycloak rechazó userinfo (HTTP {response.status_code}): {response.text}"
            )

        data = response.json()
        external_id = data.get("sub")
        email = data.get("email")
        if not external_id or not email:
            raise KeycloakCommunicationError(
                "userinfo de Keycloak incompleto: se requieren 'sub' y 'email'"
            )

        return KeycloakUserInfo(
            external_id=str(external_id),
            email=str(email).strip().lower(),
            name=data.get("name"),
            given_name=data.get("given_name"),
            family_name=data.get("family_name"),
        )

    def authenticate_with_code(self, code: str) -> KeycloakUserInfo:
        tokens = self.exchange_code_for_tokens(code)
        return self.fetch_userinfo(tokens["access_token"])
