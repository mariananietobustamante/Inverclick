from sqlalchemy.orm import Session
from Models.construction_companies import ConstructionCompanyDTO, ConstructionCompanyCreateSchema

class ConstructionCompanyRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(ConstructionCompanyDTO).offset(skip).limit(limit).all()

    def create(self, company: ConstructionCompanyCreateSchema):
        new_company = ConstructionCompanyDTO(**company.model_dump())
        self.db.add(new_company)
        self.db.commit()
        self.db.refresh(new_company)
        return new_company