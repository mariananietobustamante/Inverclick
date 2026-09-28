from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict
from sqlalchemy import ARRAY, BigInteger, DateTime, Identity, Text
from sqlalchemy.orm import Mapped, mapped_column

from Repositories.database import Base


class UserRoleDTO(Base):
    __tablename__ = "user_roles"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    role: Mapped[str] = mapped_column(Text, nullable=False)
    modules: Mapped[list[str]] = mapped_column(ARRAY(Text), nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class UserRoleCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    role: str
    modules: Optional[list[str]] = []


class UserRoleUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    role: Optional[str] = None
    modules: Optional[list[str]] = None


class UserRoleResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: str
    modules: Optional[list[str]] = []
