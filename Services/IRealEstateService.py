from Models.real_estate import RealEstateCreateSchema
from Services.Impl.RealEstateService import RealEstateService

class IRealEstateService:
    """
    Interfaz para el servicio de Propiedades (Real Estate).
    """
    def get_properties_for_user(self, user_id: int, skip: int = 0, limit: int = 100):
        return RealEstateService.get_properties_for_user(self, user_id, skip, limit)

    def create_property(self, user_id: int, property_in: RealEstateCreateSchema):
        return RealEstateService.create_property(self, user_id, property_in)