from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from Models.id_types import IdType
from Models.users_role import UserRoleDTO
from Utils.enums import (
    ALL_MODULES,
    ADMIN_ROLE_NAME,
    AppModule,
    CLIENTE_ROLE_NAME,
    CONSTRUCTORA_ROLE_NAME,
    IdentificationTypeEnum,
    VENTAS_ROLE_NAME,
)

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
        CLIENTE_ROLE_NAME,
        [AppModule.USERS.value, AppModule.PREFIX.value, AppModule.DOCUMENTS.value],
    ),
    (
        "operador",
        [AppModule.USERS.value, AppModule.USERS_LOGIN.value],
    ),
    (
        "Usuario",
        [AppModule.USERS.value, AppModule.PREFIX.value, AppModule.DOCUMENTS.value],
    ),
    (
        VENTAS_ROLE_NAME,
        [
            AppModule.USERS.value,
            AppModule.REAL_ESTATE.value,
            AppModule.SALES.value,
            AppModule.DOCUMENTS.value,
        ],
    ),
]

SSO_DEFAULT_ROLE_NAME = "Usuario"
SSO_DEFAULT_MODULES = [AppModule.USERS.value, AppModule.PREFIX.value, AppModule.DOCUMENTS.value]

CONSTRUCTORA_MODULES = [
    AppModule.CONSTRUCTION_COMPANIES.value,
    AppModule.REAL_ESTATE.value,
    AppModule.SALES.value,
    AppModule.DOCUMENTS.value,
]

VENTAS_MODULES = [
    AppModule.USERS.value,
    AppModule.REAL_ESTATE.value,
    AppModule.SALES.value,
    AppModule.DOCUMENTS.value,
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


def ensure_sso_default_role(db: Session) -> None:
    """Garantiza el rol 'Usuario' para auto-registro SSO aunque ya existan otros roles."""
    existing = db.execute(
        select(UserRoleDTO).where(UserRoleDTO.role == SSO_DEFAULT_ROLE_NAME)
    ).scalar_one_or_none()
    if existing is not None:
        return

    db.add(
        UserRoleDTO(
            role=SSO_DEFAULT_ROLE_NAME,
            modules=SSO_DEFAULT_MODULES,
            created_at=datetime.now(timezone.utc),
        )
    )
    db.commit()


def ensure_constructora_role_modules(db: Session) -> None:
    """Asegura que el rol constructora tenga los módulos de negocio actuales."""
    role = db.execute(
        select(UserRoleDTO).where(UserRoleDTO.role == CONSTRUCTORA_ROLE_NAME)
    ).scalar_one_or_none()
    if role is None:
        db.add(
            UserRoleDTO(
                role=CONSTRUCTORA_ROLE_NAME,
                modules=CONSTRUCTORA_MODULES,
                created_at=datetime.now(timezone.utc),
            )
        )
        db.commit()
        return

    current = list(role.modules or [])
    missing = [m for m in CONSTRUCTORA_MODULES if m not in current]
    if not missing:
        return
    role.modules = current + missing
    db.commit()


def _append_missing_modules(role: UserRoleDTO, modules: list[str]) -> bool:
    current = list(role.modules or [])
    missing = [module for module in modules if module not in current]
    if not missing:
        return False
    role.modules = current + missing
    return True


def ensure_documents_access_roles(db: Session) -> None:
    """Crea el rol ventas si falta y otorga el módulo documents a cliente, Usuario y ventas."""
    specs: list[tuple[str, list[str], bool]] = [
        (CLIENTE_ROLE_NAME, [AppModule.DOCUMENTS.value], False),
        (SSO_DEFAULT_ROLE_NAME, [AppModule.DOCUMENTS.value], False),
        (VENTAS_ROLE_NAME, VENTAS_MODULES, True),
    ]
    now = datetime.now(timezone.utc)
    changed = False
    for role_name, modules, create_if_missing in specs:
        role = db.execute(select(UserRoleDTO).where(UserRoleDTO.role == role_name)).scalar_one_or_none()
        if role is None:
            if create_if_missing:
                db.add(UserRoleDTO(role=role_name, modules=modules, created_at=now))
                changed = True
            continue
        if _append_missing_modules(role, modules):
            changed = True
    if changed:
        db.commit()


def ensure_admin_all_modules(db: Session) -> None:
    """Añade módulos nuevos (p. ej. leads) al rol admin si se sembró con una lista fija."""
    role = db.execute(
        select(UserRoleDTO).where(UserRoleDTO.role == ADMIN_ROLE_NAME)
    ).scalar_one_or_none()
    if role is None:
        return
    current = list(role.modules or [])
    if "all" in current:
        return
    missing = [module for module in ALL_MODULES if module not in current]
    if not missing:
        return
    role.modules = current + missing
    db.commit()
