from fastapi import HTTPException

from Repositories.RealEstateRepository import RealEstateRepository
from Repositories.UsersRoleRepository import UsersRoleRepository
from Repositories.UsuariosRepository import UsersRepository
from Utils.role_access import is_constructora_user


class RealEstateService:
    def __init__(
        self,
        repository: RealEstateRepository,
        users_repository: UsersRepository,
        roles_repository: UsersRoleRepository,
    ):
        self.repository = repository
        self.users_repository = users_repository
        self.roles_repository = roles_repository

    def _load_user(self, user_id: int):
        current_user = self.users_repository.get_by_id(user_id)
        if not current_user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado en la base de datos")
        role = self.roles_repository.get_by_id(current_user.role_id) if current_user.role_id else None
        return current_user, role

    def get_properties_for_user(self, user_id: int, skip: int = 0, limit: int = 100):
        current_user, role = self._load_user(user_id)
        if is_constructora_user(current_user, role):
            if not current_user.construction_company_id:
                return []
            return self.repository.get_by_company(current_user.construction_company_id, skip, limit)
        return self.repository.get_all(skip, limit)

    def create_property(self, user_id: int, property_in):
        current_user, role = self._load_user(user_id)
        data_dict = property_in.model_dump()

        if is_constructora_user(current_user, role):
            if not current_user.construction_company_id:
                raise HTTPException(
                    status_code=403,
                    detail="El usuario no tiene una empresa constructora asignada.",
                )
            data_dict["construction_company_id"] = current_user.construction_company_id
        elif not data_dict.get("construction_company_id"):
            raise HTTPException(
                status_code=400,
                detail="El ID de la constructora es obligatorio para registrar la propiedad.",
            )

        if self.repository.get_by_name(data_dict["name"]):
            raise HTTPException(status_code=400, detail="Ya existe una propiedad registrada con este nombre.")

        if self.repository.get_by_address(data_dict["address"]):
            raise HTTPException(
                status_code=400,
                detail="Ya existe una propiedad registrada con esta dirección exacta.",
            )

        return self.repository.create(data_dict)
