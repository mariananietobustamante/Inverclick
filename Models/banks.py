from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from sqlalchemy import BigInteger, DateTime, Identity, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column
from Repositories.database import Base

class BankDTO(Base):
    __tablename__ = "banks"
    __table_args__ = {"schema": "public"}

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    agreement_state: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    swift: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    interest_rate: Mapped[Optional[float]] = mapped_column(Numeric, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

class BankCreateSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    agreement_state: Optional[str] = None
    swift: Optional[str] = None
    address: Optional[str] = None
    interest_rate: Optional[float] = None

class BankResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    agreement_state: Optional[str] = None
    swift: Optional[str] = None
    address: Optional[str] = None
    interest_rate: Optional[float] = None
    created_at: datetime