from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


@dataclass(frozen=True)
class AuthContext:
    user_id: int
    email: str
    role_id: Optional[int]
    role_name: Optional[str]
    modules: list[str]


class LoginTokenResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user_id: int
    email: str
    role: Optional[str] = None
    modules: list[str] = []
