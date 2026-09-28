from sqlalchemy.orm import Session
from Models.construction_phases import ConstructionPhaseDTO

class ConstructionPhasesRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(ConstructionPhaseDTO).offset(skip).limit(limit).all()

    def create(self, phase_data: dict):
        new_phase = ConstructionPhaseDTO(**phase_data)
        self.db.add(new_phase)
        self.db.commit()
        self.db.refresh(new_phase)
        return new_phase