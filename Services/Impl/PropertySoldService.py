from datetime import datetime, timezone
from fastapi import HTTPException

from Models.property_sold import PropertySoldCreateSchema, PropertySoldDTO, PropertySoldResponseSchema
from Repositories.PropertySoldRepository import PropertySoldRepository
from Repositories.RealEstateRepository import RealEstateRepository
from Services.IPropertySoldService import IPropertySoldService

class PropertySoldService(IPropertySoldService):
    def __init__(
        self,
        repository: PropertySoldRepository,
        real_estate_repository: RealEstateRepository
    ):
        self.repository = repository
        self.real_estate_repository = real_estate_repository

    def register_sale(self, schema: PropertySoldCreateSchema, current_agent_id: int) -> PropertySoldResponseSchema:
        # 1. Regla de Negocio (Listado Activo): Verificar que la propiedad exista
        property_record = self.real_estate_repository.get_by_id(schema.real_estate_id)
        if not property_record:
            raise HTTPException(
                status_code=404, 
                detail="La propiedad no se encuentra formalmente listada en el catálogo disponible."
            )

        # 2. Regla de Negocio (Disponibilidad): Prevenir ventas múltiples del mismo lote
        if self.repository.check_if_sold(schema.real_estate_id):
            raise HTTPException(
                status_code=400, 
                detail="Operación rechazada: La propiedad ya está marcada como vendida."
            )

        # 3. Trazabilidad de Venta (Auditoría Comercial)
        # Extraemos los datos del esquema y obligamos a registrar el agente autenticado
        payload = schema.model_dump()
        payload["agent_id"] = current_agent_id

        # Instanciamos el DTO de SQLAlchemy (Como haces en UsuariosService)
        sale_dto = PropertySoldDTO(
            **payload,
            created_at=datetime.now(timezone.utc)
        )

        # Guardamos en base de datos
        created_sale = self.repository.create(sale_dto)

        # Retornamos el esquema de respuesta validado por Pydantic
        return PropertySoldResponseSchema.model_validate(created_sale)