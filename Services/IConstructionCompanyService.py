from Models.construction_companies import ConstructionCompanyCreateSchema

class IConstructionCompanyService:
    """
    Interfaz para el servicio de Compañías Constructoras.
    """
    def get_all(self, skip: int = 0, limit: int = 100):
        pass

    def create(self, company: ConstructionCompanyCreateSchema):
        pass