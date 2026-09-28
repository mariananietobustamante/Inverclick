from sqlalchemy import select
from sqlalchemy.orm import Session

from Models.currencies import Currency


class CurrenciesRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, currency_id: int) -> Currency | None:
        statement = select(Currency).where(Currency.id == currency_id)
        return self.db.execute(statement).scalar_one_or_none()
