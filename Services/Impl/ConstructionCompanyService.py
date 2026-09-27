from Repositories.ConstructionCompanyRepository import ConstructionCompanyRepository
from Models.construction_companies import ConstructionCompanyCreateSchema

class ConstructionCompanyService:
    def __init__(self, repository: ConstructionCompanyRepository):
        self.repository = repository

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all(skip, limit)

    def create(self, company: ConstructionCompanyCreateSchema):
        # Aquí podrías agregar validaciones, por ejemplo, que el nombre no exista ya
        return self.repository.create(company)