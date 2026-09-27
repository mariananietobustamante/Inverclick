from datetime import datetime
from typing import Optional


from pydantic import BaseModel, ConfigDict
from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column

from Repositories.database import Base

class PropertySoldDTO(Base):
    __tablename__ = "property_sold"
    __table_args__ = {"schema": "public"}

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    # Trazabilidad requerida por CA3
    # Le quitamos el "public." a users.id
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False) 
    agent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False) 
    
    # Estos se quedan igual porque leads y real_estate sí tienen el schema public definido en sus clases
    lead_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("public.leads.id", ondelete="RESTRICT"), nullable=False) 
    real_estate_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("public.real_estate.id", ondelete="RESTRICT"), nullable=False)
    
    bank_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("public.banks.id", ondelete="SET NULL"), nullable=True)
    status: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)


class PropertySoldCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    user_id: int
    lead_id: int
    real_estate_id: int
    bank_id: Optional[int] = None
    # No incluimos agent_id ni status porque el backend los asigna automáticamente


class PropertySoldResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    agent_id: int
    lead_id: int
    real_estate_id: int
    bank_id: Optional[int] = None
    status: bool
    created_at: datetime