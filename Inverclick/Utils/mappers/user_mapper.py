from decimal import Decimal, InvalidOperation
from typing import Any, Optional

from Models.users import UserDTO, UserCreateSchema, UserResponseSchema, UserUpdateSchema


def _to_decimal(value: Optional[str]) -> Optional[Decimal]:
    if value is None or value == "":
        return None
    try:
        return Decimal(value)
    except (InvalidOperation, ValueError):
        return None


def _decimal_to_str(value: Optional[Decimal]) -> Optional[str]:
    if value is None:
        return None
    return format(value, "f")


def apply_create_schema(user: UserDTO, schema: UserCreateSchema, id_type_id: Optional[int]) -> None:
    user.name = schema.name
    user.surname = schema.last_name
    user.email = str(schema.email)
    user.id_number = schema.identification
    user.id_type_id = id_type_id
    user.description = schema.desired_description
    user.country_id = schema.country_id
    user.role_id = schema.user_id_role
    user.prefix_id = schema.prefix_id
    user.city = schema.residence_city
    user.address = schema.street_address
    user.zip_code = schema.zip_code
    user.phone = schema.phone_number
    user.job = schema.job
    user.income = _to_decimal(schema.monthly_income)
    user.outcome = _to_decimal(schema.monthly_outcome)
    user.currency_id = schema.currency_id
    user.taxes = _to_decimal(schema.taxes)
    user.birth_date = schema.date_of_birth


def apply_update_schema(user: UserDTO, schema: UserUpdateSchema, id_type_id: Optional[int] = None) -> None:
    if schema.name is not None:
        user.name = schema.name
    if schema.last_name is not None:
        user.surname = schema.last_name
    if schema.email is not None:
        user.email = str(schema.email)
    if schema.identification is not None:
        user.id_number = schema.identification
    if id_type_id is not None:
        user.id_type_id = id_type_id
    if schema.desired_description is not None:
        user.description = schema.desired_description
    if schema.country_id is not None:
        user.country_id = schema.country_id
    if schema.user_id_role is not None:
        user.role_id = schema.user_id_role
    if schema.prefix_id is not None:
        user.prefix_id = schema.prefix_id
    if schema.residence_city is not None:
        user.city = schema.residence_city
    if schema.street_address is not None:
        user.address = schema.street_address
    if schema.zip_code is not None:
        user.zip_code = schema.zip_code
    if schema.phone_number is not None:
        user.phone = schema.phone_number
    if schema.job is not None:
        user.job = schema.job
    if schema.monthly_income is not None:
        user.income = _to_decimal(schema.monthly_income)
    if schema.monthly_outcome is not None:
        user.outcome = _to_decimal(schema.monthly_outcome)
    if schema.currency_id is not None:
        user.currency_id = schema.currency_id
    if schema.taxes is not None:
        user.taxes = _to_decimal(schema.taxes)
    if schema.date_of_birth is not None:
        user.birth_date = schema.date_of_birth


def apply_update_dict(user: UserDTO, data: dict[str, Any], id_type_id: Optional[int] = None) -> None:
    apply_update_schema(user, UserUpdateSchema(**data), id_type_id=id_type_id)


def to_response(user: UserDTO, identification_type: Optional[str] = None) -> UserResponseSchema:
    return UserResponseSchema(
        id=user.id,
        name=user.name,
        last_name=user.surname,
        email=user.email,
        identification=user.id_number,
        identification_type=identification_type,
        country_id=user.country_id,
        user_id_role=user.role_id,
        prefix_id=user.prefix_id,
        residence_city=user.city,
        street_address=user.address,
        zip_code=user.zip_code,
        phone_number=user.phone,
        job=user.job,
        monthly_income=_decimal_to_str(user.income),
        monthly_outcome=_decimal_to_str(user.outcome),
        desired_description=user.description,
        currency_id=user.currency_id,
        taxes=_decimal_to_str(user.taxes),
        updated_at=user.updated_at,
        created_at=user.created_at,
        date_of_birth=user.birth_date,
    )
