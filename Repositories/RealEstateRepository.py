from sqlalchemy.orm import Session
from Models.real_estate import RealEstateDTO

class RealEstateRepository:
    def __init__(self, db: Session):
        self.db = db

    # Función para el Administrador (Trae todo)
    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(RealEstateDTO).offset(skip).limit(limit).all()

    # Función para la Constructora (Aísla los datos)
    def get_by_company(self, company_id: int, skip: int = 0, limit: int = 100):
        return self.db.query(RealEstateDTO)\
            .filter(RealEstateDTO.construction_company_id == company_id)\
            .offset(skip).limit(limit).all()

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