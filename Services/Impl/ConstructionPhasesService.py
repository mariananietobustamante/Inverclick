from Repositories.ConstructionPhasesRepository import ConstructionPhasesRepository
from Models.construction_phases import ConstructionPhaseCreateSchema

class ConstructionPhasesService:
    def __init__(self, repository: ConstructionPhasesRepository):
        self.repository = repository

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all(skip, limit)

    def create(self, phase_in: ConstructionPhaseCreateSchema):
        data_dict = phase_in.model_dump()
        return self.repository.create(data_dict)