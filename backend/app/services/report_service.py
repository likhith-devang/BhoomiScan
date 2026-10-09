from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.constants import DISCLAIMER, REPORT_STATUS_FINAL
from app.models.property_case import PropertyCase
from app.models.report import FinalReport
from app.services.case_analysis_service import recalculate_case
from app.services.hashing import canonical_json, hash_payload
from app.services.ledger_service import append_ledger, verify_chain, verify_record

def _jsonable(payload: dict) -> dict:
    return __import__("json").loads(canonical_json(payload))


def build_report_content(case: PropertyCase, analysis: dict) -> dict:
    findings = analysis["findings"]
    detected = [item for item in findings if item["status"] == "DETECTED"]
    return {
        "title": "PROPERTY DUE-DILIGENCE REPORT",
        "product": "BhoomiScan",
        "tagline": "Your AIvocate.",
        "property_case_id": str(case.id),
        "property_information": analysis["property_information"],
        "documents_reviewed": [
            {
                "name": item["original_filename"],
                "document_type": item.get("document_type_label") or item.get("document_type"),
                "status": item.get("status"),
            }
            for item in analysis["documents"]
        ],
        "risk_summary": [
            {
                "category": item["category"],
                "category_label": item["category_label"],
                "status": item["status"],
                "risk_level": item["risk_level"],
                "summary": item["summary"],
            }
            for item in findings
        ],
        "overall_risk": {
            "risk_score": analysis["risk_score"],
            "risk_level": analysis["risk_level"],
        },
        "score_reasons": analysis.get("score_reasons") or [],
        "verification_coverage": analysis["verification_coverage"],
        "detected_issues": [
            {
                "category_label": item["category_label"],
                "risk_level": item["risk_level"],
                "summary": item["summary"],
                "findings": item.get("findings") or [],
            }
            for item in detected
        ],
        "evidence": [
            {
                "category_label": item["category_label"],
                "document_id": str(ev.get("document_id")) if ev.get("document_id") else None,
                "page_number": ev.get("page_number"),
                "source_text": ev.get("source_text"),
            }
            for item in findings
            for ev in (item.get("evidence") or [])
        ],
        "document_mismatches": analysis["mismatches"],
        "unverified_checks": analysis["unverified"],
        "recommended_actions": analysis["recommendations"],
        "disclaimer": DISCLAIMER,
    }


def serialize_report(report: FinalReport) -> dict:
    ledger = report.ledger_record
    return {
        "id": report.id,
        "property_case_id": report.property_case_id,
        "version": report.version,
        "status": REPORT_STATUS_FINAL,
        "report_content": report.report_content,
        "report_hash": report.report_hash,
        "risk_score": report.risk_score,
        "risk_level": report.risk_level,
        "verification_coverage": report.verification_coverage,
        "created_at": report.created_at,
        "ledger": None
        if ledger is None
        else {
            "id": ledger.id,
            "sequence": report.version,
            "previous_hash": ledger.previous_hash,
            "report_hash": ledger.report_hash,
            "record_hash": ledger.record_hash,
            "hashed_at": ledger.hashed_at,
        },
        "disclaimer": DISCLAIMER,
    }


def finalize_case(db: Session, case: PropertyCase, actor=None) -> FinalReport:
    analysis = recalculate_case(db, case)
    content = _jsonable(build_report_content(case, analysis))
    version = (db.scalar(select(func.max(FinalReport.version)).where(FinalReport.property_case_id == case.id)) or 0) + 1
    report = FinalReport(
        property_case_id=case.id,
        version=version,
        report_content=content,
        report_hash=hash_payload(content),
        risk_score=analysis["risk_score"],
        risk_level=analysis["risk_level"],
        verification_coverage=float(analysis["verification_coverage"]["percent"]),
    )
    db.add(report)
    db.flush()
    append_ledger(db, report)
    # After the report is sealed, discard uploaded bytes so personal papers are not kept on disk.
    from app.services.audit_service import record_audit
    from app.services.document_lifecycle import discard_case_documents

    record_audit(
        db,
        action="REPORT_FINALIZED",
        actor=actor,
        resource_type="final_report",
        resource_id=report.id,
        detail=f"Final report v{version} created for case {case.id}.",
        meta={"risk_score": report.risk_score, "risk_level": report.risk_level},
    )
    discard_case_documents(db, case, actor=actor)
    db.commit()
    db.refresh(report)
    return db.scalar(
        select(FinalReport).options(selectinload(FinalReport.ledger_record)).where(FinalReport.id == report.id)
    )


def verify_report(db: Session, report: FinalReport) -> dict:
    recalculated = hash_payload(report.report_content)
    report_hash_valid = recalculated == report.report_hash
    ledger = report.ledger_record
    ledger_valid = bool(ledger) and verify_record(ledger) and ledger.report_hash == report.report_hash
    chain_valid = bool(ledger) and verify_chain(db, ledger)
    status = "VALID" if report_hash_valid and ledger_valid and chain_valid else "TAMPERED"
    return {
        "status": status,
        "report_hash_valid": report_hash_valid,
        "ledger_valid": ledger_valid,
        "chain_valid": chain_valid,
        "report_hash": report.report_hash,
        "recalculated_hash": recalculated,
        "previous_hash": ledger.previous_hash if ledger else None,
        "record_hash": ledger.record_hash if ledger else None,
        "sequence": report.version,
        "hashed_at": ledger.hashed_at if ledger else None,
    }
