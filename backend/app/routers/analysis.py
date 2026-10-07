import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.deps import get_current_user
from app.models.analysis import Analysis, RiskFinding
from app.models.document import Document
from app.models.property_case import PropertyCase
from app.models.user import User
from app.schemas.analysis import AnalysisResponse, EvidenceResponse, RecommendationResponse
from app.services.analysis_service import analyze_document, serialize_analysis

router = APIRouter(prefix="/property-cases", tags=["analysis"])


def _owned_case(db: Session, case_id: uuid.UUID, user: User) -> PropertyCase:
    case = db.scalar(
        select(PropertyCase)
        .options(selectinload(PropertyCase.documents))
        .where(PropertyCase.id == case_id)
    )
    if case is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "We could not find this property file.")
    if case.user_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "You cannot open this property file.")
    return case


def _owned_document(db: Session, case_id: uuid.UUID, document_id: uuid.UUID, user: User) -> tuple[PropertyCase, Document]:
    case = _owned_case(db, case_id, user)
    document = next((item for item in case.documents if item.id == document_id), None)
    if document is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "We could not find this document.")
    return case, document


def _load_analysis(db: Session, analysis_id: uuid.UUID) -> Analysis | None:
    return db.scalar(
        select(Analysis)
        .options(
            selectinload(Analysis.findings).selectinload(RiskFinding.evidence),
            selectinload(Analysis.recommendations),
            selectinload(Analysis.document),
        )
        .where(Analysis.id == analysis_id)
    )


def _latest_for_document(db: Session, document_id: uuid.UUID) -> Analysis | None:
    return db.scalar(
        select(Analysis)
        .options(
            selectinload(Analysis.findings).selectinload(RiskFinding.evidence),
            selectinload(Analysis.recommendations),
            selectinload(Analysis.document),
        )
        .where(Analysis.document_id == document_id)
        .order_by(Analysis.created_at.desc())
        .limit(1)
    )


@router.post(
    "/{case_id}/documents/{document_id}/analyze",
    response_model=AnalysisResponse,
)
def analyze_uploaded_document(
    case_id: uuid.UUID,
    document_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    case, document = _owned_document(db, case_id, document_id, current_user)
    analysis = analyze_document(db, document, case.documents)
    loaded = _load_analysis(db, analysis.id)
    return serialize_analysis(loaded, loaded.document)


@router.get(
    "/{case_id}/documents/{document_id}/analysis",
    response_model=AnalysisResponse,
)
def get_document_analysis(
    case_id: uuid.UUID,
    document_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    _owned_document(db, case_id, document_id, current_user)
    analysis = _latest_for_document(db, document_id)
    if analysis is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No analysis is available for this document yet.")
    return serialize_analysis(analysis, analysis.document)


@router.get("/{case_id}/analysis", response_model=AnalysisResponse)
def get_case_analysis(
    case_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    case = _owned_case(db, case_id, current_user)
    analysis = db.scalar(
        select(Analysis)
        .options(
            selectinload(Analysis.findings).selectinload(RiskFinding.evidence),
            selectinload(Analysis.recommendations),
            selectinload(Analysis.document),
        )
        .where(Analysis.property_case_id == case.id)
        .order_by(Analysis.created_at.desc())
        .limit(1)
    )
    if analysis is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No analysis is available for this property file yet.")
    return serialize_analysis(analysis, analysis.document)


@router.get("/{case_id}/recommendations", response_model=list[RecommendationResponse])
def get_case_recommendations(
    case_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[dict]:
    payload = get_case_analysis(case_id, db, current_user)
    return payload["recommendations"]


@router.get("/{case_id}/evidence/{finding_id}", response_model=list[EvidenceResponse])
def get_finding_evidence(
    case_id: uuid.UUID,
    finding_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[dict]:
    case = _owned_case(db, case_id, current_user)
    finding = db.scalar(
        select(RiskFinding)
        .options(selectinload(RiskFinding.evidence), selectinload(RiskFinding.analysis))
        .where(RiskFinding.id == finding_id)
    )
    if finding is None or finding.analysis.property_case_id != case.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "We could not find this evidence.")
    return [
        {
            "id": item.id,
            "document_id": item.document_id,
            "document_type": item.document_type,
            "page_number": item.page_number,
            "source_text": item.source_text,
            "extracted_field": item.extracted_field,
            "confidence": item.confidence,
        }
        for item in finding.evidence
    ]
