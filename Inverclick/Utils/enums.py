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


ALL_MODULES: list[str] = [module.value for module in AppModule]
