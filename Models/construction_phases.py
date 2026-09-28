from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, DateTime, Identity
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, ConfigDict
from Repositories.database import Base

# Modelo de base de datos
class ConstructionPhaseDTO(Base):
    __tablename__ = "construction_phases"
    __table_args__ = {"schema": "public"}

    id: Mapped[int] = mapped_column(Integer, Identity(always=False, start=1), primary_key=True)
    phase_number: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow)

# Esquema para crear (POST)
class ConstructionPhaseCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")
    
    phase_number: int
    name: str
    description: Optional[str] = None

# Esquema de respuesta (GET/POST)
class ConstructionPhaseResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    phase_number: int
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None