from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from Models.auth import AuthContext
from Models.real_estate import RealEstateCreateSchema, RealEstateResponseSchema
from Repositories.RealEstateRepository import RealEstateRepository
from Repositories.UsersRoleRepository import UsersRoleRepository
from Repositories.UsuariosRepository import UsersRepository
from Repositories.database import get_db
from Services.IRealEstateService import IRealEstateService
from Services.Impl.RealEstateService import RealEstateService
from Services.Security.auth_dependencies import require_module
from Utils.enums import AppModule

router = APIRouter(prefix="/real-estate", tags=["Real Estate"])


def get_real_estate_service(db: Session = Depends(get_db)) -> IRealEstateService:
    return RealEstateService(
        repository=RealEstateRepository(db),
        users_repository=UsersRepository(db),
        roles_repository=UsersRoleRepository(db),
    )


@router.get("", response_model=list[RealEstateResponseSchema])
def get_properties(
    skip: int = 0,
    limit: int = 100,
    service: IRealEstateService = Depends(get_real_estate_service),
    auth_context: AuthContext = Depends(require_module(AppModule.REAL_ESTATE)),
):
    return service.get_properties_for_user(user_id=auth_context.user_id, skip=skip, limit=limit)


@router.post("", status_code=201, response_model=RealEstateResponseSchema)
def create_property(
    property_in: RealEstateCreateSchema,
    service: IRealEstateService = Depends(get_real_estate_service),
    auth_context: AuthContext = Depends(require_module(AppModule.REAL_ESTATE)),
):
    return service.create_property(user_id=auth_context.user_id, property_in=property_in)
