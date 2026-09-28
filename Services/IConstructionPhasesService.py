from Models.construction_phases import ConstructionPhaseCreateSchema

class IConstructionPhasesService:
    def get_all(self, skip: int = 0, limit: int = 100):
        pass

    def create(self, phase_in: ConstructionPhaseCreateSchema):
        pass