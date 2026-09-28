from sqlalchemy.orm import Session

from Models.property_sold import PropertySoldDTO
from Models.real_estate import RealEstateDTO


class RealEstateRepository:
    def __init__(self, db: Session):
        self.db = db

    def _exclude_sold(self, query):
        sold_ids = self.db.query(PropertySoldDTO.real_estate_id).filter(
            PropertySoldDTO.status.is_(True)
        )
        return query.filter(~RealEstateDTO.id.in_(sold_ids))

    def get_all(self, skip: int = 0, limit: int = 100):
        query = self._exclude_sold(self.db.query(RealEstateDTO))
        return query.offset(skip).limit(limit).all()

    def get_by_company(self, company_id: int, skip: int = 0, limit: int = 100):
        query = self.db.query(RealEstateDTO).filter(
            RealEstateDTO.construction_company_id == company_id
        )
        return self._exclude_sold(query).offset(skip).limit(limit).all()

    def create(self, property_data: dict):
        new_property = RealEstateDTO(**property_data)
        self.db.add(new_property)
        self.db.commit()
        self.db.refresh(new_property)
        return new_property

    def get_by_name(self, name: str):
        return self.db.query(RealEstateDTO).filter(RealEstateDTO.name == name).first()

    def get_by_address(self, address: str):
        return self.db.query(RealEstateDTO).filter(RealEstateDTO.address == address).first()

    def get_by_id(self, property_id: int):
        return self.db.query(RealEstateDTO).filter(RealEstateDTO.id == property_id).first()
