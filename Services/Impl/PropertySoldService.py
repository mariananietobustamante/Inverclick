from datetime import datetime, timezone

from fastapi import HTTPException

from Models.property_sold import PropertySoldCreateSchema, PropertySoldDTO, PropertySoldResponseSchema
from Repositories.LeadsRepository import LeadsRepository
from Repositories.PropertySoldRepository import PropertySoldRepository
from Repositories.RealEstateRepository import RealEstateRepository
from Repositories.UsersRoleRepository import UsersRoleRepository
from Repositories.UsuariosRepository import UsersRepository
from Services.IPropertySoldService import IPropertySoldService
from Utils.role_access import is_constructora_user


class PropertySoldService(IPropertySoldService):
    def __init__(
        self,
        repository: PropertySoldRepository,
        real_estate_repository: RealEstateRepository,
        leads_repository: LeadsRepository,
        users_repository: UsersRepository,
        roles_repository: UsersRoleRepository,
    ):
        self.repository = repository
        self.real_estate_repository = real_estate_repository
        self.leads_repository = leads_repository
        self.users_repository = users_repository
        self.roles_repository = roles_repository

    def register_sale(self, schema: PropertySoldCreateSchema, current_agent_id: int) -> PropertySoldResponseSchema:
        property_record = self.real_estate_repository.get_by_id(schema.real_estate_id)
        if not property_record:
            raise HTTPException(
                status_code=404,
                detail="La propiedad no se encuentra formalmente listada en el catálogo disponible.",
            )

        if self.repository.check_if_sold(schema.real_estate_id):
            raise HTTPException(
                status_code=400,
                detail="Operación rechazada: La propiedad ya está marcada como vendida.",
            )

        lead = self.leads_repository.get_by_id(schema.lead_id)
        if not lead:
            raise HTTPException(status_code=404, detail="El lead asociado a la venta no existe.")

        if lead.user_id != schema.user_id:
            raise HTTPException(
                status_code=400,
                detail="El comprador de la venta debe coincidir con el usuario del lead.",
            )

        payload = schema.model_dump()
        payload["agent_id"] = current_agent_id

        sale_dto = PropertySoldDTO(
            **payload,
            created_at=datetime.now(timezone.utc),
        )
        created_sale = self.repository.create(sale_dto)
        return PropertySoldResponseSchema.model_validate(created_sale)

    def get_all_for_user(self, user_id: int, skip: int = 0, limit: int = 100) -> list[PropertySoldResponseSchema]:
        current_user = self.users_repository.get_by_id(user_id)
        if not current_user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado en la base de datos")

        role = self.roles_repository.get_by_id(current_user.role_id) if current_user.role_id else None
        if is_constructora_user(current_user, role):
            if not current_user.construction_company_id:
                return []
            sales = self.repository.get_by_company(current_user.construction_company_id, skip, limit)
            return [PropertySoldResponseSchema.model_validate(sale) for sale in sales]

        sales = self.repository.get_all(skip, limit)
        return [PropertySoldResponseSchema.model_validate(sale) for sale in sales]
