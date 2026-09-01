"""Registra todos los modelos ORM para que SQLAlchemy resuelva las FK correctamente."""

from Models.countries import Country
from Models.currencies import Currency
from Models.id_types import IdType
from Models.num_prefix import NumPrefix
from Models.users import UserDTO
from Models.users_login import UserLoginDTO
from Models.users_role import UserRoleDTO

__all__ = [
    "Country",
    "Currency",
    "IdType",
    "NumPrefix",
    "UserDTO",
    "UserLoginDTO",
    "UserRoleDTO",
]
