from fastapi import HTTPException

from Repositories.ConstructionCompanyRepository import ConstructionCompanyRepository
from Repositories.UsersRoleRepository import UsersRoleRepository
from Repositories.UsuariosRepository import UsersRepository
from Models.construction_companies import ConstructionCompanyCreateSchema
from Utils.role_access import is_constructora_user


class ConstructionCompanyService:
    def __init__(
        self,
        repository: ConstructionCompanyRepository,
        users_repository: UsersRepository,
        roles_repository: UsersRoleRepository,
    ):
        self.repository = repository
        self.users_repository = users_repository
        self.roles_repository = roles_repository

    def get_all_for_user(self, user_id: int, skip: int = 0, limit: int = 100):
        current_user = self.users_repository.get_by_id(user_id)
        if not current_user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado en la base de datos")

        role = self.roles_repository.get_by_id(current_user.role_id) if current_user.role_id else None
        if is_constructora_user(current_user, role):
            if not current_user.construction_company_id:
                return []
            company = self.repository.get_by_id(current_user.construction_company_id)
            return [company] if company else []

        return self.repository.get_all(skip, limit)

    def create(self, company: ConstructionCompanyCreateSchema):
        if self.repository.get_by_name(company.name):
            raise HTTPException(
                status_code=400,
                detail="Ya existe una constructora registrada con este nombre.",
            )
        return self.repository.create(company)
