from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from sqlalchemy import BigInteger, DateTime, ForeignKey, Identity, Text
from sqlalchemy.orm import Mapped, mapped_column
from Repositories.database import Base

class LeadDTO(Base):
    __tablename__ = "leads"
    __table_args__ = {"schema": "public"}

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    state: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

class LeadCreateSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")
    user_id: int
    state: Optional[str] = "Nuevo"
    description: Optional[str] = None

class LeadResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    state: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime