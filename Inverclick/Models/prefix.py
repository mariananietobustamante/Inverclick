from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from Repositories.database import Base

class Prefix(Base):
    __tablename__ = "NumPrefix"

    id: Mapped[int] = mapped_column(primary_key=True)
    cod_country: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    prefix: Mapped[str] = mapped_column(String(100))
