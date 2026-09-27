from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from Models.property_sold import PropertySoldCreateSchema, PropertySoldResponseSchema
from Repositories.PropertySoldRepository import PropertySoldRepository
from Repositories.RealEstateRepository import RealEstateRepository
from Repositories.database import get_db
from Services.IPropertySoldService import IPropertySoldService
from Services.Impl.PropertySoldService import PropertySoldService
from Services.Security.auth_dependencies import require_module
from Utils.enums import AppModule

router = APIRouter(prefix="/sales", tags=["Sales"])

def get_sales_service(db: Session = Depends(get_db)) -> IPropertySoldService:
    """Fábrica para inyectar dependencias y retornar la interfaz del servicio de ventas."""
    return PropertySoldService(
        repository=PropertySoldRepository(db),
        real_estate_repository=RealEstateRepository(db)
    )

@router.post("", status_code=201, response_model=PropertySoldResponseSchema)
def create_sale(
    sale_in: PropertySoldCreateSchema,
    service: IPropertySoldService = Depends(get_sales_service),
    auth_context = Depends(require_module(AppModule.SALES)), # Asume que tienes "SALES" o similar en tu enum
):
    """
    Registra la venta de una propiedad. 
    Aplica reglas de negocio (Listado Activo, Disponibilidad) y Trazabilidad Comercial.
    """
    # Extraemos el ID del agente que hace la petición desde el token (auth_context)
    # Utilizamos el mismo enfoque de extracción de tu controlador RealEstate
    agent_id = getattr(auth_context, "user_id", getattr(auth_context, "id", getattr(auth_context, "usuario_id", None)))
    
    return service.register_sale(schema=sale_in, current_agent_id=agent_id)

@router.get("", response_model=list[PropertySoldResponseSchema])
def get_all_sales(
    skip: int = 0,
    limit: int = 100,
    service: IPropertySoldService = Depends(get_sales_service),
    _auth = Depends(require_module(AppModule.SALES)),
):
    """Obtiene el historial de todas las ventas registradas."""
    return service.repository.get_all(skip=skip, limit=limit)