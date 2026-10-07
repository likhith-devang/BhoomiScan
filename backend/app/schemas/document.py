import uuid
from datetime import datetime

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: uuid.UUID
    property_case_id: uuid.UUID
    original_filename: str
    stored_filename: str
    file_type: str
    file_size: int
    status: str
    document_type: str | None = None
    processing_error: str | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}
