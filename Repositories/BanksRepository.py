from sqlalchemy import select
from sqlalchemy.orm import Session
from Models.banks import BankDTO

class BanksRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_name(self, name: str) -> BankDTO | None:
        statement = select(BankDTO).where(BankDTO.name == name)
        return self.db.execute(statement).scalar_one_or_none()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[BankDTO]:
        statement = select(BankDTO).offset(skip).limit(limit)
        return list(self.db.execute(statement).scalars().all())

    def create(self, bank_dto: BankDTO) -> BankDTO:
        self.db.add(bank_dto)
        self.db.commit()
        self.db.refresh(bank_dto)
        return bank_dto