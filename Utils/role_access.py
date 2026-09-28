from Models.users import UserDTO
from Models.users_role import UserRoleDTO
from Utils.enums import CONSTRUCTORA_ROLE_NAME


def is_constructora_role(role_name: str | None) -> bool:
    if not role_name:
        return False
    return role_name.casefold() == CONSTRUCTORA_ROLE_NAME.casefold()


def is_constructora_user(user: UserDTO | None, role: UserRoleDTO | None) -> bool:
    if user is None or role is None:
        return False
    return is_constructora_role(role.role)
