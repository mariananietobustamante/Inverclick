from sqlalchemy.orm import Session

from Models.construction_companies import ConstructionCompanyCreateSchema, ConstructionCompanyDTO


class ConstructionCompanyRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(ConstructionCompanyDTO).offset(skip).limit(limit).all()

    def get_by_id(self, company_id: int) -> ConstructionCompanyDTO | None:
        return (
            self.db.query(ConstructionCompanyDTO)
            .filter(ConstructionCompanyDTO.id == company_id)
            .first()
        )

    def get_by_name(self, name: str) -> ConstructionCompanyDTO | None:
        return (
            self.db.query(ConstructionCompanyDTO)
            .filter(ConstructionCompanyDTO.name == name)
            .first()
        )

    def create(self, company: ConstructionCompanyCreateSchema):
        new_company = ConstructionCompanyDTO(**company.model_dump())
        self.db.add(new_company)
        self.db.commit()
        self.db.refresh(new_company)
        return new_company
