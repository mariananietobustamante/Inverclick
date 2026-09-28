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


ALL_MODULES: list[str] = [module.value for module in AppModule]

CONSTRUCTORA_ROLE_NAME = "constructora"


class AuthProvider(str, Enum):
    """Origen de autenticación registrado en user_login.auth_provider."""

    LOCAL = "local"
    KEYCLOAK = "keycloak"
    HYBRID = "hybrid"
