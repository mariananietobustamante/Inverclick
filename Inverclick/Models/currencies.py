from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from Repositories.database import Base


class Currency(Base):
    __tablename__ = "currencies"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    code: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
