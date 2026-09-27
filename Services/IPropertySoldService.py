from Models.property_sold import PropertySoldCreateSchema, PropertySoldResponseSchema

class IPropertySoldService:
    def register_sale(self, schema: PropertySoldCreateSchema, current_agent_id: int) -> PropertySoldResponseSchema:
        """
        Registra una venta cumpliendo con las reglas de negocio de Listado Activo, 
        Disponibilidad y Trazabilidad Comercial.
        """
        pass