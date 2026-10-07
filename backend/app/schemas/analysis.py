import uuid
from datetime import datetime
from typing import Any

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
    classification_confidence: float | None = None
    processing_error: str | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class EvidenceResponse(BaseModel):
    id: uuid.UUID | None = None
    document_id: uuid.UUID | None = None
    document_type: str | None = None
    page_number: int | None = None
    source_text: str
    extracted_field: str | None = None
    confidence: float | None = None


class FindingResponse(BaseModel):
    id: uuid.UUID
    category: str
    category_label: str
    status: str
    risk_level: str
    summary: str
    finding_data: dict[str, Any] | None = None
    evidence: list[EvidenceResponse] = []


class RecommendationResponse(BaseModel):
    id: uuid.UUID
    category: str
    category_label: str
    document_type: str
    label: str
    reason: str


class PipelineStepResponse(BaseModel):
    id: str
    label: str
    done: bool


class AnalysisResponse(BaseModel):
    id: uuid.UUID
    property_case_id: uuid.UUID
    document_id: uuid.UUID
    analysis_status: str
    document_name: str | None = None
    document_status: str | None = None
    document_type: str | None = None
    document_type_label: str | None = None
    classification_confidence: float | None = None
    classification_note: str | None = None
    detected_language: str | None = None
    original_text: str | None = None
    translated_text: str | None = None
    extracted_data: dict[str, Any] | None = None
    pipeline_steps: list[PipelineStepResponse] = []
    findings: list[FindingResponse] = []
    recommendations: list[RecommendationResponse] = []
    processing_error: str | None = None
    created_at: datetime | None = None
