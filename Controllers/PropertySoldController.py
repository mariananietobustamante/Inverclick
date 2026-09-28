from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from Models.auth import AuthContext
from Models.property_sold import PropertySoldCreateSchema, PropertySoldResponseSchema
from Repositories.LeadsRepository import LeadsRepository
from Repositories.PropertySoldRepository import PropertySoldRepository
from Repositories.RealEstateRepository import RealEstateRepository
from Repositories.UsersRoleRepository import UsersRoleRepository
from Repositories.UsuariosRepository import UsersRepository
from Repositories.database import get_db
from Services.IPropertySoldService import IPropertySoldService
from Services.Impl.PropertySoldService import PropertySoldService
from Services.Security.auth_dependencies import require_module
from Utils.enums import AppModule

router = APIRouter(prefix="/sales", tags=["Sales"])


def get_sales_service(db: Session = Depends(get_db)) -> IPropertySoldService:
    return PropertySoldService(
        repository=PropertySoldRepository(db),
        real_estate_repository=RealEstateRepository(db),
        leads_repository=LeadsRepository(db),
        users_repository=UsersRepository(db),
        roles_repository=UsersRoleRepository(db),
    )


@router.post("", status_code=201, response_model=PropertySoldResponseSchema)
def create_sale(
    sale_in: PropertySoldCreateSchema,
    service: IPropertySoldService = Depends(get_sales_service),
    auth_context: AuthContext = Depends(require_module(AppModule.SALES)),
):
    return service.register_sale(schema=sale_in, current_agent_id=auth_context.user_id)


@router.get("", response_model=list[PropertySoldResponseSchema])
def get_all_sales(
    skip: int = 0,
    limit: int = 100,
    service: IPropertySoldService = Depends(get_sales_service),
    auth_context: AuthContext = Depends(require_module(AppModule.SALES)),
):
    return service.get_all_for_user(user_id=auth_context.user_id, skip=skip, limit=limit)
