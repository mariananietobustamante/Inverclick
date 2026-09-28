from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Numeric, DateTime, ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, ConfigDict
from Repositories.database import Base

class RealEstateDTO(Base):
    __tablename__ = "real_estate"
    __table_args__ = {"schema": "public"}

    id: Mapped[int] = mapped_column(Integer, Identity(always=False, start=1), primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False) # CA2: Unicidad de Nombre
    cost: Mapped[float] = mapped_column(Numeric, nullable=False) # CA2: Valor obligatorio
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    address: Mapped[str] = mapped_column(String, unique=True, nullable=False) # CA2: Unicidad de Dirección
    zip_code: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    # CA2: Llave foránea obligatoria
    construction_company_id: Mapped[int] = mapped_column(Integer, ForeignKey("public.construction_companies.id"), nullable=False)
    phase_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("public.construction_phases.id"), nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class RealEstateCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")
    
    name: str
    cost: float
    description: Optional[str] = None
    address: str
    zip_code: Optional[str] = None
    city: Optional[str] = None
    stock: int
    construction_company_id: Optional[int] = None # Opcional en el JSON porque el backend lo autocompleta para constructoras
    phase_id: Optional[int] = None

class RealEstateResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    cost: float
    description: Optional[str] = None
    address: str
    zip_code: Optional[str] = None
    city: Optional[str] = None
    stock: int
    construction_company_id: int
    phase_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None