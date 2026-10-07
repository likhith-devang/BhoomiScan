from __future__ import annotations

from typing import Any

from sqlalchemy import delete, select
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.orm.attributes import flag_modified

from app.constants import (
    ANALYSIS_COMPLETE,
    COMPARISON_MISMATCH,
    COMPARISON_NOT_AVAILABLE,
    DISCLAIMER,
    DOCUMENT_STATUS_ANALYZED,
    DOCUMENT_TYPE_LABELS,
    RISK_CATEGORIES,
    RISK_CATEGORY_LABELS,
    RISK_HIGH,
    RISK_INFO,
    STATUS_DETECTED,
    STATUS_NO_ISSUE_FOUND,
    STATUS_NOT_VERIFIED,
)
from app.models.analysis import Analysis
from app.models.document import Document
from app.models.property_case import PropertyCase
from app.models.report import DocumentComparison
from app.services.comparison_service import compare_documents
from app.services.extraction_service import merge_extraction
from app.services.recommendation_engine import NEEDED, build_recommendations
from app.services.risk_engine import evaluate_risks
from app.services.evidence_service import ensure_finding_evidence
from app.services.scoring_service import overall_risk_level, risk_score, score_reasons, verification_coverage

_STATUS_RANK = {
    STATUS_DETECTED: 3,
    STATUS_NO_ISSUE_FOUND: 2,
    STATUS_NOT_VERIFIED: 1,
}
_RISK_RANK = {"HIGH": 4, "MEDIUM": 3, "LOW": 2, "INFO": 1}


def working_text(document: Document) -> str:
    return document.translated_text or document.original_text or ""


def analyzed_documents(case: PropertyCase) -> list[Document]:
    return [
        item
        for item in case.documents
        if item.status == DOCUMENT_STATUS_ANALYZED and item.extracted_data
    ]


def latest_complete_analysis(db: Session, document_id) -> Analysis | None:
    return db.scalar(
        select(Analysis)
        .options(selectinload(Analysis.findings), selectinload(Analysis.recommendations))
        .where(Analysis.document_id == document_id, Analysis.analysis_status == ANALYSIS_COMPLETE)
        .order_by(Analysis.created_at.desc())
        .limit(1)
    )


def _merge_findings(per_document: list[list[dict[str, Any]]]) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for findings in per_document:
        for finding in findings:
            category = finding["category"]
            current = merged.get(category)
            if current is None or _STATUS_RANK[finding["status"]] > _STATUS_RANK[current["status"]]:
                merged[category] = {
                    **finding,
                    "evidence": list(finding.get("evidence") or []),
                    "documents_reviewed": list(finding.get("documents_reviewed") or []),
                }
                continue
            if finding["status"] == current["status"] and _RISK_RANK.get(finding["risk_level"], 0) > _RISK_RANK.get(
                current["risk_level"], 0
            ):
                current["risk_level"] = finding["risk_level"]
                current["summary"] = finding["summary"]
            current["evidence"].extend(finding.get("evidence") or [])
            current.setdefault("documents_reviewed", []).extend(finding.get("documents_reviewed") or [])
    return [merged[category] for category in RISK_CATEGORIES if category in merged]


def _apply_mismatches(findings: list[dict[str, Any]], comparisons: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_category = {item["category"]: item for item in findings}
    for row in comparisons:
        if row["result"] != COMPARISON_MISMATCH:
            continue
        category = row["category"]
        finding = by_category[category]
        finding["status"] = STATUS_DETECTED
        if _RISK_RANK.get(row.get("severity") or RISK_HIGH, 0) >= _RISK_RANK.get(finding.get("risk_level") or RISK_INFO, 0):
            finding["risk_level"] = row.get("severity") or RISK_HIGH
        finding["summary"] = f"Potential issue detected. {row['explanation']}"
        finding.setdefault("findings", []).append(row["explanation"])
        finding.setdefault("evidence", []).append(
            {
                "document_id": row.get("document_a_id"),
                "document_type": None,
                "page_number": None,
                "source_text": f"{row.get('value_a')} vs {row.get('value_b')}",
                "extracted_field": row["field"],
                "confidence": None,
            }
        )
    return [by_category[category] for category in RISK_CATEGORIES]


def _unverified(findings: list[dict[str, Any]], uploaded_types: set[str]) -> list[dict[str, Any]]:
    rows = []
    for finding in findings:
        if finding["status"] != STATUS_NOT_VERIFIED:
            continue
        missing = [
            {"document_type": doc_type, "label": DOCUMENT_TYPE_LABELS.get(doc_type, doc_type), "reason": reason}
            for doc_type, reason in NEEDED.get(finding["category"], [])
            if doc_type not in uploaded_types
        ]
        rows.append(
            {
                "category": finding["category"],
                "category_label": finding["category_label"],
                "summary": finding["summary"],
                "missing_documents": missing,
            }
        )
    return rows


def persist_comparisons(db: Session, case_id, rows: list[dict[str, Any]]) -> list[DocumentComparison]:
    db.execute(delete(DocumentComparison).where(DocumentComparison.property_case_id == case_id))
    stored = []
    for row in rows:
        item = DocumentComparison(
            property_case_id=case_id,
            field=row["field"],
            document_a_id=row.get("document_a_id"),
            document_b_id=row.get("document_b_id"),
            value_a=row.get("value_a"),
            value_b=row.get("value_b"),
            result=row["result"],
            severity=row.get("severity"),
            explanation=row["explanation"],
        )
        db.add(item)
        stored.append(item)
    db.flush()
    for item, row in zip(stored, rows, strict=True):
        row["id"] = item.id
    return stored


def serialize_document(document: Document, db: Session) -> dict[str, Any]:
    analysis = latest_complete_analysis(db, document.id)
    return {
        "id": document.id,
        "original_filename": document.original_filename,
        "document_type": document.document_type,
        "document_type_label": DOCUMENT_TYPE_LABELS.get(document.document_type or "", document.document_type),
        "status": document.status,
        "analysis_status": analysis.analysis_status if analysis else None,
        "created_at": document.created_at,
        "processing_error": document.processing_error,
        "latest_analysis_id": analysis.id if analysis else None,
    }


def property_information(documents: list[Document], property_type: str) -> dict[str, Any]:
    merged: dict[str, Any] = {"property_type": property_type}
    preferred = sorted(documents, key=lambda item: 0 if item.document_type == "SALE_DEED" else 1)
    for document in preferred:
        data = document.extracted_data or {}
        prop = data.get("property") or {}
        ownership = data.get("ownership") or {}
        for key in ("survey_number", "khata_number", "area", "village", "hobli", "taluk", "district"):
            if not merged.get(key) and prop.get(key):
                merged[key] = prop[key]
        for key in ("seller_name", "buyer_name", "owner_name"):
            if not merged.get(key) and ownership.get(key):
                merged[key] = ownership[key]
    return merged


def recalculate_case(db: Session, case: PropertyCase) -> dict[str, Any]:
    docs = analyzed_documents(case)
    if not docs:
        raise ValueError("Analyze at least one document before recalculating this property file.")

    uploaded_types = {item.document_type for item in case.documents if item.document_type}
    per_document = []
    for document in docs:
        extracted = merge_extraction(document.extracted_data or {}, working_text(document), document.original_text)
        if extracted != (document.extracted_data or {}):
            document.extracted_data = extracted
            flag_modified(document, "extracted_data")
        findings = evaluate_risks(document, extracted, working_text(document), uploaded_types)
        reviewed = [DOCUMENT_TYPE_LABELS.get(document.document_type or "", document.original_filename)]
        for finding in findings:
            ensure_finding_evidence(document, finding, working_text(document))
            finding["category_label"] = RISK_CATEGORY_LABELS[finding["category"]]
            finding["documents_reviewed"] = reviewed
            finding["missing_documents"] = [
                {"document_type": doc_type, "label": DOCUMENT_TYPE_LABELS.get(doc_type, doc_type), "reason": reason}
                for doc_type, reason in NEEDED.get(finding["category"], [])
                if doc_type not in uploaded_types
            ]
        per_document.append(findings)

    comparisons = compare_documents(docs)
    persist_comparisons(db, case.id, comparisons)
    findings = _apply_mismatches(_merge_findings(per_document), comparisons)
    for finding in findings:
        finding["category_label"] = RISK_CATEGORY_LABELS[finding["category"]]
        finding["findings"] = finding.get("findings") or [finding["summary"]]

    recommendations = build_recommendations(findings, uploaded_types)
    score = risk_score(findings)
    level = overall_risk_level(findings, score)
    coverage = verification_coverage(findings, uploaded_types)
    info = property_information(docs, case.property_type)
    payload = {
        "property_case_id": case.id,
        "domain": case.domain,
        "property_type": case.property_type,
        "property_information": info,
        "documents": [serialize_document(item, db) for item in sorted(case.documents, key=lambda row: row.created_at or row.id)],
        "analyzed_document_count": len(docs),
        "uploaded_document_count": len(case.documents),
        "findings": findings,
        "comparisons": comparisons,
        "matches": [row for row in comparisons if row["result"] == "MATCH"],
        "mismatches": [row for row in comparisons if row["result"] == COMPARISON_MISMATCH],
        "not_available": [row for row in comparisons if row["result"] == COMPARISON_NOT_AVAILABLE],
        "risk_score": score,
        "risk_level": level,
        "score_reasons": score_reasons(findings),
        "verification_coverage": coverage,
        "recommendations": recommendations,
        "unverified": _unverified(findings, uploaded_types),
        "disclaimer": DISCLAIMER,
    }
    db.commit()
    return payload
