from enum import Enum


class ResponseStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class IdentificationTypeEnum(str, Enum):
    CC = "CC"
    CE = "CE"
    PAS = "PAS"
    NIT = "NIT"
    PEP = "PEP"


class AppModule(str, Enum):
    """Módulos de la API vinculados a los roles en user_roles.modules."""

    USERS = "users"
    PREFIX = "prefix"
    USERS_ROLE = "users-role"
    USERS_LOGIN = "users-login"
    REAL_ESTATE = "propiedades"
    CONSTRUCTION_COMPANIES = "construction-companies"
    SALES = "sales"
    LEADS = "leads"
    DOCUMENTS = "documents"


ALL_MODULES: list[str] = [module.value for module in AppModule]

CONSTRUCTORA_ROLE_NAME = "constructora"
VENTAS_ROLE_NAME = "ventas"
ADMIN_ROLE_NAME = "admin"
CLIENTE_ROLE_NAME = "cliente"

INTERNAL_DOCUMENT_ROLE_NAMES = frozenset(
    {
        ADMIN_ROLE_NAME,
        "administrador",
        CONSTRUCTORA_ROLE_NAME,
        VENTAS_ROLE_NAME,
    }
)
CLIENT_ROLE_NAMES = frozenset({CLIENTE_ROLE_NAME, "usuario"})


class AuthProvider(str, Enum):
    """Origen de autenticación registrado en user_login.auth_provider."""

    LOCAL = "local"
    KEYCLOAK = "keycloak"
    HYBRID = "hybrid"
