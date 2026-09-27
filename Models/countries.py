from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, DateTime, Identity, Text
from sqlalchemy.orm import Mapped, mapped_column

from Repositories.database import Base


class Country(Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    iso_code: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
