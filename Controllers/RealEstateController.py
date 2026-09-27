from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Repositories.database import get_db
from Repositories.RealEstateRepository import RealEstateRepository
from Repositories.UsuariosRepository import UsersRepository
from Services.IRealEstateService import IRealEstateService
from Services.Impl.RealEstateService import RealEstateService 
from Models.real_estate import RealEstateCreateSchema, RealEstateResponseSchema
from Services.Security.auth_dependencies import require_module
from Utils.enums import AppModule

router = APIRouter(prefix="/real-estate", tags=["Real Estate"])

# Inyectamos ambos repositorios para construir el servicio completo
def get_real_estate_service(db: Session = Depends(get_db)) -> IRealEstateService:
    return RealEstateService(
        repository=RealEstateRepository(db),
        users_repository=UsersRepository(db)
    )

@router.get("", response_model=list[RealEstateResponseSchema])
def get_properties(
    skip: int = 0,
    limit: int = 100,
    service: IRealEstateService = Depends(get_real_estate_service),
    auth_context = Depends(require_module(AppModule.REAL_ESTATE))
):
    # El controlador solo extrae el ID y delega todo el trabajo
    user_id = getattr(auth_context, "user_id", getattr(auth_context, "id", getattr(auth_context, "usuario_id", None)))
    return service.get_properties_for_user(user_id=user_id, skip=skip, limit=limit)

@router.post("", status_code=201, response_model=RealEstateResponseSchema)
def create_property(
    property_in: RealEstateCreateSchema,
    service: IRealEstateService = Depends(get_real_estate_service),
    auth_context = Depends(require_module(AppModule.REAL_ESTATE))
):
    # Tráfico HTTP directo al servicio
    user_id = getattr(auth_context, "user_id", getattr(auth_context, "id", getattr(auth_context, "usuario_id", None)))
    return service.create_property(user_id=user_id, property_in=property_in)