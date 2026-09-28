from datetime import datetime, timezone
from typing import Any

from Models.users import UserCreateSchema, UserDTO, UserResponseSchema, UserUpdateSchema
from Repositories.CountriesRepository import CountriesRepository
from Repositories.ConstructionCompanyRepository import ConstructionCompanyRepository
from Repositories.IdTypesRepository import IdTypesRepository
from Repositories.IUsuariosRepository import IUsuariosRepository
from Repositories.PrefixRepository import PrefixRepository
from Repositories.UsersRoleRepository import UsersRoleRepository
from Utils.HttpResponses.userHttpResponses import UserHttpResponses
from Utils.mappers.user_mapper import apply_create_schema, apply_update_schema, to_response
from Utils.user_validator import UserValidator


class UsuariosService:
    def __init__(
        self,
        repository: IUsuariosRepository,
        countries_repository: CountriesRepository,
        prefix_repository: PrefixRepository,
        roles_repository: UsersRoleRepository,
        id_types_repository: IdTypesRepository,
        construction_company_repository: ConstructionCompanyRepository,
        http_responses: UserHttpResponses,
        validator: UserValidator,
    ):
        self.repository = repository
        self.countries_repository = countries_repository
        self.prefix_repository = prefix_repository
        self.roles_repository = roles_repository
        self.id_types_repository = id_types_repository
        self.construction_company_repository = construction_company_repository
        self.http_responses = http_responses
        self.validator = validator

    def _resolve_id_type_id(self, identification_type: str | None) -> int | None:
        if not identification_type:
            return None
        id_type = self.id_types_repository.get_by_type(identification_type)
        if id_type is None:
            raise self.http_responses.error_id_type_not_found()
        return id_type.id

    def _get_identification_type_code(self, id_type_id: int | None) -> str | None:
        if id_type_id is None:
            return None
        id_type = self.id_types_repository.get_by_id(id_type_id)
        return id_type.type if id_type else None

    def _to_response(self, user: UserDTO) -> UserResponseSchema:
        return to_response(user, self._get_identification_type_code(user.id_type_id))

    def _validate_references(self, data: dict[str, Any], *, is_create: bool = False) -> None:
        country_id = data.get("country_id")
        prefix_id = data.get("prefix_id")
        user_id_role = data.get("user_id_role")
        email = data.get("email")
        identification = data.get("identification")
        identification_type = data.get("identification_type")

        if country_id is not None and self.countries_repository.get_by_id(country_id) is None:
            raise self.http_responses.error_country_not_found()

        if prefix_id is not None and self.prefix_repository.get_by_id(prefix_id) is None:
            raise self.http_responses.error_prefix_not_found()

        if user_id_role is not None and self.roles_repository.get_by_id(user_id_role) is None:
            raise self.http_responses.error_role_not_found()

        company_id = data.get("construction_company_id")
        if company_id is not None and self.construction_company_repository.get_by_id(company_id) is None:
            raise self.http_responses.error_construction_company_not_found()

        if email and self.repository.get_by_email(email) is not None:
            if is_create:
                raise self.http_responses.error_email_already_exists()

        if identification and identification_type:
            existing = self.repository.get_by_identification(identification, identification_type)
            if existing is not None and is_create:
                raise self.http_responses.error_identification_already_exists()

    def get_by_id(self, user_id: int) -> UserResponseSchema:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise self.http_responses.error_user_not_found()
        return self._to_response(user)

    def get_by_email(self, email: str) -> UserResponseSchema:
        user = self.repository.get_by_email(email)
        if user is None:
            raise self.http_responses.error_user_not_found()
        return self._to_response(user)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[UserResponseSchema]:
        users = self.repository.get_all(skip, limit)
        return [self._to_response(user) for user in users]

    def create(self, schema: UserCreateSchema) -> UserResponseSchema:
        business_error = self.validator.validate_user_business_rules(schema, is_create=True)
        if business_error:
            raise self.http_responses.error_validation(business_error)

        invalid = self.validator.validate_user_dto_lengths(schema.model_dump(exclude_none=True))
        if invalid:
            field, min_len, max_len = invalid
            raise self.http_responses.error_invalid_length(field, min_len, max_len)

        payload = schema.model_dump(exclude_none=True)
        self._validate_references(payload, is_create=True)
        id_type_id = self._resolve_id_type_id(schema.identification_type)

        user = UserDTO(
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        apply_create_schema(user, schema, id_type_id)
        created = self.repository.create(user)
        return self._to_response(created)

    def update(self, user_id: int, schema: UserUpdateSchema) -> UserResponseSchema:
        payload = schema.model_dump(exclude_unset=True)

        business_error = self.validator.validate_user_business_rules(schema, is_create=False)
        if business_error:
            raise self.http_responses.error_validation(business_error)

        invalid = self.validator.validate_user_dto_lengths(payload)
        if invalid:
            field, min_len, max_len = invalid
            raise self.http_responses.error_invalid_length(field, min_len, max_len)

        db_user = self.repository.get_by_id(user_id)
        if db_user is None:
            raise self.http_responses.error_user_not_updated()

        if schema.email and schema.email != db_user.email and self.repository.get_by_email(str(schema.email)):
            raise self.http_responses.error_email_already_exists()

        id_type_id = None
        if schema.identification_type is not None:
            id_type_id = self._resolve_id_type_id(schema.identification_type)

        if schema.identification and (schema.identification_type or db_user.id_type_id):
            type_code = schema.identification_type or self._get_identification_type_code(db_user.id_type_id)
            if type_code:
                existing = self.repository.get_by_identification(schema.identification, type_code)
                if existing is not None and existing.id != user_id:
                    raise self.http_responses.error_identification_already_exists()

        self._validate_references(payload)
        apply_update_schema(db_user, schema, id_type_id=id_type_id)
        db_user.updated_at = datetime.now(timezone.utc)
        updated = self.repository.update(user_id, db_user)
        if updated is None:
            raise self.http_responses.error_user_not_updated()
        return self._to_response(updated)

    def delete(self, user_id: int) -> bool:
        success = self.repository.delete(user_id)
        if not success:
            raise self.http_responses.error_user_not_deleted()
        return success

    def get_user_entity_by_email(self, email: str) -> UserDTO | None:
        return self.repository.get_by_email(email)
