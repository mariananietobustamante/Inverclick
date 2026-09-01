from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from Repositories.database import Base


class NumPrefix(Base):
    __tablename__ = "num_prefix"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    prefix: Mapped[str] = mapped_column(Text, nullable=False)
    country_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("countries.id", ondelete="RESTRICT"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
