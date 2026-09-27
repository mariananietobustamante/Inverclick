from datetime import date, datetime
from decimal import Decimal
from typing import Any, Optional, Union

from pydantic import BaseModel, ConfigDict
from sqlalchemy import BigInteger, Date, DateTime, ForeignKey, Identity, Integer, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from Repositories.database import Base


class UserDTO(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    surname: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    zip_code: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    city: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    country_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("countries.id", ondelete="SET NULL"), nullable=True
    )
    prefix_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("num_prefix.id", ondelete="SET NULL"), nullable=True
    )
    phone: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    email: Mapped[str] = mapped_column(Text, nullable=False)
    currency_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("currencies.id", ondelete="SET NULL"), nullable=True
    )
    taxes: Mapped[Optional[Decimal]] = mapped_column(Numeric(14, 2), nullable=True)
    income: Mapped[Optional[Decimal]] = mapped_column(Numeric(14, 2), nullable=True)
    job: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    outcome: Mapped[Optional[Decimal]] = mapped_column(Numeric(14, 2), nullable=True)
    id_type_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("id_types.id", ondelete="SET NULL"), nullable=True
    )
    id_number: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    role_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("user_roles.id", ondelete="SET NULL"), nullable=True
    )
    birth_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    construction_company_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("public.construction_companies.id"), nullable=True)


class UserCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    name: str
    last_name: str
    email: str
    identification: str
    identification_type: str
    desired_description: str
    phone_number: str
    country_id: Optional[int] = None
    user_id_role: Optional[int] = None
    prefix_id: Optional[int] = None
    residence_city: Optional[str] = None
    street_address: Optional[str] = None
    zip_code: Optional[str] = None
    job: Optional[str] = None
    monthly_income: Optional[str] = None
    monthly_outcome: Optional[str] = None
    currency_id: Optional[int] = None
    taxes: Optional[str] = None
    date_of_birth: Optional[date] = None
    construction_company_id: Optional[int] = None


class UserUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    identification: Optional[str] = None
    identification_type: Optional[str] = None
    country_id: Optional[int] = None
    user_id_role: Optional[int] = None
    prefix_id: Optional[int] = None
    residence_city: Optional[str] = None
    street_address: Optional[str] = None
    zip_code: Optional[str] = None
    phone_number: Optional[str] = None
    job: Optional[str] = None
    monthly_income: Optional[str] = None
    monthly_outcome: Optional[str] = None
    desired_description: Optional[str] = None
    currency_id: Optional[int] = None
    taxes: Optional[str] = None
    date_of_birth: Optional[date] = None
    construction_company_id: Optional[int] = None


class UserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    last_name: Optional[str] = None
    email: str
    identification: Optional[str] = None
    identification_type: Optional[str] = None
    country_id: Optional[int] = None
    user_id_role: Optional[int] = None
    prefix_id: Optional[int] = None
    residence_city: Optional[str] = None
    street_address: Optional[str] = None
    zip_code: Optional[str] = None
    phone_number: Optional[str] = None
    job: Optional[str] = None
    monthly_income: Optional[str] = None
    monthly_outcome: Optional[str] = None
    desired_description: Optional[str] = None
    currency_id: Optional[int] = None
    taxes: Optional[str] = None
    updated_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    date_of_birth: Optional[Union[date, datetime]] = None
    construction_company_id: Optional[int] = None
