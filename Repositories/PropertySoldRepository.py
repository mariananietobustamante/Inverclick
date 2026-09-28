from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from Models.property_sold import PropertySoldDTO
from Models.real_estate import RealEstateDTO


class PropertySoldRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, sale_id: int) -> PropertySoldDTO | None:
        statement = select(PropertySoldDTO).where(PropertySoldDTO.id == sale_id)
        return self.db.execute(statement).scalar_one_or_none()

    def check_if_sold(self, real_estate_id: int) -> bool:
        statement = select(PropertySoldDTO).where(
            PropertySoldDTO.real_estate_id == real_estate_id,
            PropertySoldDTO.status.is_(True),
        )
        sale = self.db.execute(statement).scalar_one_or_none()
        return sale is not None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[PropertySoldDTO]:
        statement = select(PropertySoldDTO).offset(skip).limit(limit)
        return list(self.db.execute(statement).scalars().all())

    def get_by_company(self, company_id: int, skip: int = 0, limit: int = 100) -> list[PropertySoldDTO]:
        statement = (
            select(PropertySoldDTO)
            .join(RealEstateDTO, PropertySoldDTO.real_estate_id == RealEstateDTO.id)
            .where(RealEstateDTO.construction_company_id == company_id)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.execute(statement).scalars().all())

    def create(self, sale_dto: PropertySoldDTO) -> PropertySoldDTO:
        self.db.add(sale_dto)
        self.db.commit()
        self.db.refresh(sale_dto)
        return sale_dto

    def update(self, sale_id: int, sale_data: dict[str, Any]) -> PropertySoldDTO | None:
        db_sale = self.get_by_id(sale_id)
        if db_sale:
            for key, value in sale_data.items():
                if value is not None and hasattr(db_sale, key):
                    setattr(db_sale, key, value)
            self.db.commit()
            self.db.refresh(db_sale)
        return db_sale
