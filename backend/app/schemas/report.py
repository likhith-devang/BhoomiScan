import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel


class ComparisonRow(BaseModel):
    id: uuid.UUID | None = None
    field: str
    field_label: str | None = None
    category: str | None = None
    document_a_id: uuid.UUID | None = None
    document_b_id: uuid.UUID | None = None
    document_a_name: str | None = None
    document_b_name: str | None = None
    value_a: str | None = None
    value_b: str | None = None
    result: str
    severity: str | None = None
    explanation: str


class CoverageCategory(BaseModel):
    category: str
    category_label: str
    coverage: str
    status: str | None = None


class CoverageResponse(BaseModel):
    percent: int
    explanation: str
    categories: list[CoverageCategory] = []


class LedgerResponse(BaseModel):
    id: uuid.UUID
    sequence: int
    previous_hash: str
    report_hash: str | None = None
    record_hash: str
    hashed_at: str


class DueDiligenceResponse(BaseModel):
    property_case_id: uuid.UUID
    domain: str | None = None
    property_type: str | None = None
    property_information: dict[str, Any] = {}
    documents: list[dict[str, Any]] = []
    analyzed_document_count: int = 0
    uploaded_document_count: int = 0
    findings: list[dict[str, Any]] = []
    comparisons: list[dict[str, Any]] = []
    matches: list[dict[str, Any]] = []
    mismatches: list[dict[str, Any]] = []
    not_available: list[dict[str, Any]] = []
    risk_score: int
    risk_level: str
    score_reasons: list[dict[str, Any]] = []
    verification_coverage: CoverageResponse
    recommendations: list[dict[str, Any]] = []
    unverified: list[dict[str, Any]] = []
    disclaimer: str


class FinalReportResponse(BaseModel):
    id: uuid.UUID
    property_case_id: uuid.UUID
    version: int
    status: str
    report_content: dict[str, Any]
    report_hash: str
    risk_score: int
    risk_level: str
    verification_coverage: float
    created_at: datetime | None = None
    ledger: LedgerResponse | None = None
    disclaimer: str


class FinalReportListItem(BaseModel):
    id: uuid.UUID
    version: int
    risk_score: int
    risk_level: str
    verification_coverage: float
    report_hash: str
    created_at: datetime | None = None


class IntegrityResponse(BaseModel):
    status: str
    report_hash_valid: bool
    ledger_valid: bool
    chain_valid: bool
    report_hash: str | None = None
    recalculated_hash: str | None = None
    previous_hash: str | None = None
    record_hash: str | None = None
    sequence: int | None = None
    hashed_at: str | None = None
