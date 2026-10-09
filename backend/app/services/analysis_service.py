from __future__ import annotations

import logging

from sqlalchemy.orm import Session

from app.constants import (
    ANALYSIS_COMPLETE,
    ANALYSIS_FAILED,
    DOCUMENT_STATUS_ANALYZED,
    DOCUMENT_STATUS_FAILED,
    DOCUMENT_STATUS_PROCESSING,
    DOCUMENT_TYPE_LABELS,
    ENGLISH_LANGUAGE,
    KANNADA_LANGUAGE,
    RISK_CATEGORY_LABELS,
)
from app.models.analysis import Analysis, EvidenceItem, Recommendation, RiskFinding
from app.models.document import Document
from app.services.document_classifier import classify_document, looks_like_kannada
from app.services.evidence_service import ensure_finding_evidence
from app.services.extraction_service import EXTRACTION_SCHEMA, merge_extraction
from app.services.property_gate import is_property_document, validate_english_working_text
from app.services.recommendation_engine import build_recommendations
from app.services.risk_engine import evaluate_risks
from app.services.sarvam_service import SarvamError, digitise_document, extract_fields, translate_text

logger = logging.getLogger(__name__)


class PropertyGateError(Exception):
    """Raised when AI is blocked because the file is not a property document."""


def _steps(*done: str) -> list[dict]:
    catalog = [
        ("uploaded", "Document uploaded"),
        ("reading", "Reading document"),
        ("extracting", "Extracting information"),
        ("checking", "Checking risks"),
        ("complete", "Analysis complete"),
    ]
    finished = set(done)
    return [{"id": key, "label": label, "done": key in finished} for key, label in catalog]


def analyze_document(db: Session, document: Document, case_documents: list[Document]) -> Analysis:
    document.status = DOCUMENT_STATUS_PROCESSING
    document.processing_error = None
    db.add(document)
    db.commit()
    db.refresh(document)

    try:
        original_text = digitise_document(
            document.file_path,
            document.original_filename,
            document.file_type,
            language=KANNADA_LANGUAGE,
        )
        detected = KANNADA_LANGUAGE if looks_like_kannada(original_text) else ENGLISH_LANGUAGE
        translated = None
        working_text = original_text
        if detected == KANNADA_LANGUAGE:
            translated = translate_text(original_text)
            working_text = translated or original_text

        classification = classify_document(working_text, document.original_filename)
        allowed, gate_reason = is_property_document(
            classification["document_type"],
            working_text,
            document.original_filename,
        )
        if not allowed:
            raise PropertyGateError(gate_reason)

        classified_property = classification["document_type"] != "OTHER"
        language_check = validate_english_working_text(
            working_text,
            detected,
            classified_property_type=classified_property,
        )
        if not language_check["ok"]:
            raise PropertyGateError(
                language_check["notes"][0]
                if language_check["notes"]
                else "Document text could not be validated for analysis."
            )

        try:
            ai_extract = extract_fields(
                document.file_path,
                document.original_filename,
                document.file_type,
                EXTRACTION_SCHEMA,
            )
        except SarvamError:
            ai_extract = {}
        extracted = merge_extraction(ai_extract, working_text, original_text)

        document.original_text = (original_text or "").replace("\x00", "")
        document.translated_text = (translated or "").replace("\x00", "") or None
        document.detected_language = detected
        document.document_type = classification["document_type"]
        document.classification_confidence = classification["confidence"]
        document.extracted_data = extracted

        uploaded_types = {item.document_type for item in case_documents if item.document_type}
        uploaded_types.add(document.document_type)
        findings = evaluate_risks(document, extracted, working_text, uploaded_types)
        recommendations = build_recommendations(findings, uploaded_types)

        analysis = Analysis(
            property_case_id=document.property_case_id,
            document_id=document.id,
            analysis_status=ANALYSIS_COMPLETE,
            pipeline_steps=_steps("uploaded", "reading", "extracting", "checking", "complete"),
            extracted_data=extracted,
        )
        db.add(analysis)
        db.flush()

        for finding in findings:
            row = RiskFinding(
                analysis_id=analysis.id,
                category=finding["category"],
                status=finding["status"],
                risk_level=finding["risk_level"],
                summary=finding["summary"],
                finding_data=finding.get("finding_data"),
            )
            db.add(row)
            db.flush()
            for item in finding.get("evidence") or []:
                db.add(
                    EvidenceItem(
                        finding_id=row.id,
                        document_id=document.id,
                        document_type=item.get("document_type") or document.document_type,
                        page_number=item.get("page_number"),
                        source_text=item.get("source_text") or "",
                        extracted_field=item.get("extracted_field"),
                        confidence=item.get("confidence"),
                    )
                )
        for rec in recommendations:
            db.add(
                Recommendation(
                    analysis_id=analysis.id,
                    category=rec["category"],
                    document_type=rec["document_type"],
                    reason=rec["reason"],
                )
            )

        document.status = DOCUMENT_STATUS_ANALYZED
        db.commit()
        db.refresh(analysis)
        return analysis
    except (SarvamError, PropertyGateError) as exc:
        document.status = DOCUMENT_STATUS_FAILED
        document.processing_error = str(exc)
        analysis = Analysis(
            property_case_id=document.property_case_id,
            document_id=document.id,
            analysis_status=ANALYSIS_FAILED,
            pipeline_steps=_steps("uploaded", "reading"),
            extracted_data=None,
        )
        db.add(analysis)
        db.add(document)
        db.commit()
        db.refresh(analysis)
        return analysis
    except Exception:
        logger.exception("Document analysis failed.")
        document.status = DOCUMENT_STATUS_FAILED
        document.processing_error = "We could not finish this analysis. Please try again."
        analysis = Analysis(
            property_case_id=document.property_case_id,
            document_id=document.id,
            analysis_status=ANALYSIS_FAILED,
            pipeline_steps=_steps("uploaded"),
            extracted_data=None,
        )
        db.add(analysis)
        db.add(document)
        db.commit()
        db.refresh(analysis)
        return analysis


def serialize_analysis(analysis: Analysis, document: Document) -> dict:
    classification_note = None
    if document.document_type == "OTHER":
        classification_note = "Document type could not be confidently identified."
    elif document.document_type:
        classification_note = f"Identified as {DOCUMENT_TYPE_LABELS.get(document.document_type, document.document_type)}."

    source = document.translated_text or document.original_text or ""
    extracted = merge_extraction(
        analysis.extracted_data or document.extracted_data,
        source,
        document.original_text,
    )
    live = {
        item["category"]: item
        for item in evaluate_risks(
            document,
            extracted,
            source,
            {document.document_type} if document.document_type else set(),
        )
    }

    findings = []
    for finding in analysis.findings:
        updated = live.get(finding.category) or {}
        payload = {
            "id": finding.id,
            "category": finding.category,
            "category_label": RISK_CATEGORY_LABELS.get(finding.category, finding.category),
            "status": updated.get("status") or finding.status,
            "risk_level": updated.get("risk_level") or finding.risk_level,
            "summary": updated.get("summary") or finding.summary,
            "finding_data": updated.get("finding_data") or finding.finding_data,
            "evidence": list(updated.get("evidence") or []),
        }
        if not payload["evidence"]:
            payload["evidence"] = [
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
        ensure_finding_evidence(document, payload, source)
        findings.append(payload)
    recommendations = [
        {
            "id": rec.id,
            "category": rec.category,
            "category_label": RISK_CATEGORY_LABELS.get(rec.category, rec.category),
            "document_type": rec.document_type,
            "label": DOCUMENT_TYPE_LABELS.get(rec.document_type, rec.document_type),
            "reason": rec.reason,
        }
        for rec in analysis.recommendations
    ]
    return {
        "id": analysis.id,
        "property_case_id": analysis.property_case_id,
        "document_id": analysis.document_id,
        "analysis_status": analysis.analysis_status,
        "document_name": document.original_filename,
        "document_status": document.status,
        "document_type": document.document_type,
        "document_type_label": DOCUMENT_TYPE_LABELS.get(document.document_type or "", document.document_type),
        "classification_confidence": document.classification_confidence,
        "classification_note": classification_note,
        "detected_language": document.detected_language,
        "original_text": document.original_text,
        "translated_text": document.translated_text,
        "extracted_data": extracted,
        "pipeline_steps": analysis.pipeline_steps or [],
        "findings": findings,
        "recommendations": recommendations,
        "processing_error": document.processing_error,
        "created_at": analysis.created_at,
    }
