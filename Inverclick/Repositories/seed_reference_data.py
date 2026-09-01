from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from Models.id_types import IdType
from Models.users_role import UserRoleDTO
from Utils.enums import ALL_MODULES, AppModule, IdentificationTypeEnum

DEFAULT_ID_TYPES: list[tuple[str, str]] = [
    (IdentificationTypeEnum.CC.value, "Cédula de ciudadanía"),
    (IdentificationTypeEnum.CE.value, "Cédula de extranjería"),
    (IdentificationTypeEnum.PAS.value, "Pasaporte"),
    (IdentificationTypeEnum.NIT.value, "NIT"),
    (IdentificationTypeEnum.PEP.value, "PEP"),
]

DEFAULT_ROLES: list[tuple[str, list[str]]] = [
    ("admin", ALL_MODULES),
    (
        "cliente",
        [AppModule.USERS.value, AppModule.PREFIX.value],
    ),
    (
        "operador",
        [AppModule.USERS.value, AppModule.USERS_LOGIN.value],
    ),
]


def ensure_id_types(db: Session) -> None:
    """Inserta los tipos de identificación base si la tabla está vacía."""
    count = db.execute(select(func.count()).select_from(IdType)).scalar_one()
    if count > 0:
        return

    now = datetime.now(timezone.utc)
    for type_code, description in DEFAULT_ID_TYPES:
        db.add(IdType(type=type_code, description=description, created_at=now))
    db.commit()


def ensure_default_roles(db: Session) -> None:
    """Inserta roles base con sus módulos si la tabla está vacía."""
    count = db.execute(select(func.count()).select_from(UserRoleDTO)).scalar_one()
    if count > 0:
        return

    now = datetime.now(timezone.utc)
    for role_name, modules in DEFAULT_ROLES:
        db.add(UserRoleDTO(role=role_name, modules=modules, created_at=now))
    db.commit()
