from sqlalchemy import select
from sqlalchemy.orm import Session
from Models.leads import LeadDTO

class LeadsRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, lead_id: int) -> LeadDTO | None:
        statement = select(LeadDTO).where(LeadDTO.id == lead_id)
        return self.db.execute(statement).scalar_one_or_none()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[LeadDTO]:
        statement = select(LeadDTO).offset(skip).limit(limit)
        return list(self.db.execute(statement).scalars().all())

    def create(self, lead_dto: LeadDTO) -> LeadDTO:
        self.db.add(lead_dto)
        self.db.commit()
        self.db.refresh(lead_dto)
        return lead_dto