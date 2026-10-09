import uuid
from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from app.constants import USER_ROLES


class SignupRequest(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=8, max_length=128)
    confirm_password: str = Field(min_length=8, max_length=128)

    @model_validator(mode="after")
    def passwords_match(self) -> "SignupRequest":
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match.")
        return self


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    role: str
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class RoleUpdateRequest(BaseModel):
    role: str

    @field_validator("role")
    @classmethod
    def valid_role(cls, value: str) -> str:
        role = (value or "").strip().upper()
        if role not in USER_ROLES:
            raise ValueError(f"Role must be one of: {', '.join(USER_ROLES)}")
        return role


class AuditLogResponse(BaseModel):
    id: uuid.UUID
    actor_user_id: uuid.UUID | None = None
    actor_username: str | None = None
    actor_role: str | None = None
    action: str
    resource_type: str | None = None
    resource_id: str | None = None
    detail: str | None = None
    meta: dict | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}
