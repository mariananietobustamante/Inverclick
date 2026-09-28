"""Configura realm/client/usuario de prueba en Keycloak local (HU04).

Prerrequisito:
  docker compose -f docker-compose.keycloak.yml up -d

Uso:
  python scripts/setup_keycloak.py
"""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request

BASE = "http://127.0.0.1:8080"
REALM = "inverclick"
CLIENT_ID = "inverclick-api"
CLIENT_SECRET = "inverclick-dev-client-secret"
REDIRECT = "http://127.0.0.1:8000/auth/keycloak/callback"
TEST_USER = "sso.prueba"
TEST_EMAIL = "sso.prueba@inverclick.local"
TEST_PASS = "Prueba123!"


def req(method: str, url: str, data=None, token: str | None = None, form: bool = False):
    headers: dict[str, str] = {}
    body = None
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if data is not None:
        if form:
            body = urllib.parse.urlencode(data).encode()
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        else:
            body = json.dumps(data).encode()
            headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=30) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()


def main() -> None:
    status, raw = req(
        "POST",
        f"{BASE}/realms/master/protocol/openid-connect/token",
        {
            "grant_type": "password",
            "client_id": "admin-cli",
            "username": "admin",
            "password": "admin",
        },
        form=True,
    )
    if status != 200:
        raise SystemExit(f"No se pudo obtener token admin ({status}): {raw!r}")
    token = json.loads(raw)["access_token"]

    status, _ = req("GET", f"{BASE}/admin/realms/{REALM}", token=token)
    if status == 404:
        status, raw = req(
            "POST",
            f"{BASE}/admin/realms",
            {
                "realm": REALM,
                "enabled": True,
                "loginWithEmailAllowed": True,
                "duplicateEmailsAllowed": False,
            },
            token=token,
        )
        if status not in (201, 204):
            raise SystemExit(f"No se pudo crear realm: {status} {raw!r}")
        print(f"Realm '{REALM}' creado")
    else:
        print(f"Realm '{REALM}' ya existe")

    status, raw = req(
        "GET",
        f"{BASE}/admin/realms/{REALM}/clients?clientId={CLIENT_ID}",
        token=token,
    )
    clients = json.loads(raw) if status == 200 else []
    if not clients:
        status, raw = req(
            "POST",
            f"{BASE}/admin/realms/{REALM}/clients",
            {
                "clientId": CLIENT_ID,
                "name": "Inverclick API",
                "enabled": True,
                "protocol": "openid-connect",
                "publicClient": False,
                "secret": CLIENT_SECRET,
                "standardFlowEnabled": True,
                "directAccessGrantsEnabled": True,
                "redirectUris": [REDIRECT],
                "webOrigins": ["http://127.0.0.1:8000", "+"],
            },
            token=token,
        )
        if status not in (201, 204):
            raise SystemExit(f"No se pudo crear client: {status} {raw!r}")
        status, raw = req(
            "GET",
            f"{BASE}/admin/realms/{REALM}/clients?clientId={CLIENT_ID}",
            token=token,
        )
        clients = json.loads(raw)
        print(f"Client '{CLIENT_ID}' creado")
    else:
        print(f"Client '{CLIENT_ID}' ya existe")

    client_uuid = clients[0]["id"]
    status, raw = req("GET", f"{BASE}/admin/realms/{REALM}/clients/{client_uuid}", token=token)
    client = json.loads(raw)
    client["secret"] = CLIENT_SECRET
    client["publicClient"] = False
    client["standardFlowEnabled"] = True
    client["redirectUris"] = [REDIRECT]
    client["webOrigins"] = ["http://127.0.0.1:8000", "+"]
    status, raw = req(
        "PUT",
        f"{BASE}/admin/realms/{REALM}/clients/{client_uuid}",
        client,
        token=token,
    )
    if status not in (200, 204):
        raise SystemExit(f"No se pudo actualizar client: {status} {raw!r}")

    status, raw = req(
        "GET",
        f"{BASE}/admin/realms/{REALM}/users?username={TEST_USER}&exact=true",
        token=token,
    )
    users = json.loads(raw) if status == 200 else []
    if not users:
        status, raw = req(
            "POST",
            f"{BASE}/admin/realms/{REALM}/users",
            {
                "username": TEST_USER,
                "email": TEST_EMAIL,
                "enabled": True,
                "emailVerified": True,
                "firstName": "SSO",
                "lastName": "Prueba",
            },
            token=token,
        )
        if status not in (201, 204):
            raise SystemExit(f"No se pudo crear usuario: {status} {raw!r}")
        status, raw = req(
            "GET",
            f"{BASE}/admin/realms/{REALM}/users?username={TEST_USER}&exact=true",
            token=token,
        )
        users = json.loads(raw)
        print(f"Usuario '{TEST_USER}' creado")
    else:
        print(f"Usuario '{TEST_USER}' ya existe")

    user_id = users[0]["id"]
    status, raw = req(
        "PUT",
        f"{BASE}/admin/realms/{REALM}/users/{user_id}/reset-password",
        {"type": "password", "value": TEST_PASS, "temporary": False},
        token=token,
    )
    if status not in (200, 204):
        raise SystemExit(f"No se pudo setear password: {status} {raw!r}")

    print("\nListo. Credenciales para .env:")
    print(f"  KEYCLOAK_SERVER_URL={BASE}")
    print(f"  KEYCLOAK_REALM={REALM}")
    print(f"  KEYCLOAK_CLIENT_ID={CLIENT_ID}")
    print(f"  KEYCLOAK_CLIENT_SECRET={CLIENT_SECRET}")
    print(f"  KEYCLOAK_REDIRECT_URI={REDIRECT}")
    print("\nUsuario de prueba SSO:")
    print(f"  usuario/email: {TEST_USER} / {TEST_EMAIL}")
    print(f"  password: {TEST_PASS}")
    print("\nAdmin Keycloak: http://127.0.0.1:8080  (admin / admin)")
    print("Probar: http://127.0.0.1:8000/auth/keycloak")


if __name__ == "__main__":
    main()
