from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Numeric, DateTime, Identity
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, ConfigDict
from Repositories.database import Base

class ConstructionCompanyDTO(Base):
    __tablename__ = "construction_companies"
    __table_args__ = {"schema": "public"}

    id: Mapped[int] = mapped_column(Integer, Identity(always=False, start=1), primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    rating: Mapped[Optional[float]] = mapped_column(Numeric, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow)

class ConstructionCompanyCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")
    name: str
    rating: Optional[float] = None

class ConstructionCompanyResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    rating: Optional[float] = None
    created_at: Optional[datetime] = None