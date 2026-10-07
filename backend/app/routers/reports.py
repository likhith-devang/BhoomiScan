import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.deps import get_current_user
from app.models.property_case import PropertyCase
from app.models.report import DocumentComparison, FinalReport
from app.models.user import User
from app.schemas.report import DueDiligenceResponse, FinalReportListItem, FinalReportResponse, IntegrityResponse
from app.services.case_analysis_service import recalculate_case
from app.services.report_pdf import build_report_pdf
from app.services.report_service import finalize_case, serialize_report, verify_report

router = APIRouter(prefix="/property-cases", tags=["due-diligence"])


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


def _owned_report(db: Session, case_id: uuid.UUID, report_id: uuid.UUID, user: User) -> FinalReport:
    case = _owned_case(db, case_id, user)
    report = db.scalar(
        select(FinalReport)
        .options(selectinload(FinalReport.ledger_record))
        .where(FinalReport.id == report_id, FinalReport.property_case_id == case.id)
    )
    if report is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "We could not find this report.")
    return report


@router.post("/{case_id}/recalculate", response_model=DueDiligenceResponse)
def recalculate_property_case(
    case_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    case = _owned_case(db, case_id, current_user)
    try:
        return recalculate_case(db, case)
    except ValueError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc


@router.get("/{case_id}/due-diligence", response_model=DueDiligenceResponse)
def get_due_diligence(
    case_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    return recalculate_property_case(case_id, db, current_user)


@router.get("/{case_id}/comparisons")
def get_comparisons(
    case_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[dict]:
    case = _owned_case(db, case_id, current_user)
    rows = db.scalars(
        select(DocumentComparison)
        .where(DocumentComparison.property_case_id == case.id)
        .order_by(DocumentComparison.created_at.asc())
    ).all()
    if not rows:
        payload = recalculate_property_case(case_id, db, current_user)
        return payload["comparisons"]
    return [
        {
            "id": row.id,
            "field": row.field,
            "document_a_id": row.document_a_id,
            "document_b_id": row.document_b_id,
            "value_a": row.value_a,
            "value_b": row.value_b,
            "result": row.result,
            "severity": row.severity,
            "explanation": row.explanation,
        }
        for row in rows
    ]


@router.post("/{case_id}/finalize", response_model=FinalReportResponse)
def finalize_due_diligence(
    case_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    case = _owned_case(db, case_id, current_user)
    try:
        report = finalize_case(db, case)
    except ValueError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc
    return serialize_report(report)


@router.get("/{case_id}/reports", response_model=list[FinalReportListItem])
def list_reports(
    case_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[FinalReport]:
    case = _owned_case(db, case_id, current_user)
    return db.scalars(
        select(FinalReport).where(FinalReport.property_case_id == case.id).order_by(FinalReport.version.desc())
    ).all()


@router.get("/{case_id}/reports/{report_id}", response_model=FinalReportResponse)
def get_report(
    case_id: uuid.UUID,
    report_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    return serialize_report(_owned_report(db, case_id, report_id, current_user))


@router.get("/{case_id}/reports/{report_id}/verify", response_model=IntegrityResponse)
def verify_report_integrity(
    case_id: uuid.UUID,
    report_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    report = _owned_report(db, case_id, report_id, current_user)
    return verify_report(db, report)


@router.get("/{case_id}/reports/{report_id}/pdf")
def download_report_pdf(
    case_id: uuid.UUID,
    report_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Response:
    report = _owned_report(db, case_id, report_id, current_user)
    payload = build_report_pdf(report)
    filename = f"BhoomiScan_DueDiligence_v{report.version}.pdf"
    return Response(
        content=payload,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
