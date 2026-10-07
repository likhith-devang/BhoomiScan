import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.constants import ALLOWED_DOMAINS, RESIDENTIAL_PROPERTY_TYPES


class PropertyCaseCreate(BaseModel):
    domain: str = Field(min_length=1, max_length=32)
    property_type: str = Field(min_length=1, max_length=64)


class PropertyCaseResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    domain: str
    property_type: str
    status: str
    document_count: int = 0
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


def validate_domain_and_type(domain: str, property_type: str) -> tuple[str, str]:
    domain_key = domain.strip().upper()
    type_key = property_type.strip().upper()
    if domain_key not in ALLOWED_DOMAINS:
        raise ValueError("Please pick a valid property kind.")
    if domain_key != "RESIDENTIAL":
        raise ValueError("Get Subscription to use this.")
    if type_key not in RESIDENTIAL_PROPERTY_TYPES:
        raise ValueError("Please pick a valid home type.")
    return domain_key, type_key
