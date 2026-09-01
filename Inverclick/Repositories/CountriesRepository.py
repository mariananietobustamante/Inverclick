from sqlalchemy import select
from sqlalchemy.orm import Session

from Models.countries import Country


class CountriesRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, country_id: int) -> Country | None:
        statement = select(Country).where(Country.id == country_id)
        return self.db.execute(statement).scalar_one_or_none()
