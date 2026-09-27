from datetime import datetime

from pydantic import BaseModel, ConfigDict
from sqlalchemy import BigInteger, DateTime, ForeignKey, Identity, Text
from sqlalchemy.orm import Mapped, mapped_column

from Repositories.database import Base


class NumPrefix(Base):
    __tablename__ = "num_prefix"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    prefix: Mapped[str] = mapped_column(Text, nullable=False)
    country_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("countries.id", ondelete="RESTRICT"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class NumPrefixResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    prefix: str
    country_id: int
    created_at: datetime
