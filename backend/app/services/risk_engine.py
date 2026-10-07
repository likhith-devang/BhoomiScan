from __future__ import annotations

from typing import Any

from app.constants import (
    RISK_HIGH,
    RISK_INFO,
    RISK_LOW,
    RISK_MEDIUM,
    STATUS_DETECTED,
    STATUS_NO_ISSUE_FOUND,
    STATUS_NOT_VERIFIED,
)
from app.services.evidence_service import collect_matches, ensure_finding_evidence, evidence_payload, snippet_around

LITIGATION_VERIFY_TYPES = {
    "ENCUMBRANCE_CERTIFICATE",
    "COURT_CASE_DOCUMENT",
    "COURT_ORDER",
    "LEGAL_NOTICE",
    "SELLER_AFFIDAVIT",
}
MORTGAGE_VERIFY_TYPES = {
    "ENCUMBRANCE_CERTIFICATE",
    "BANK_MORTGAGE_DOCUMENT",
    "LOAN_CLOSURE_NOC",
    "RELEASE_DEED",
    "BANK_NOC",
}
APPROVAL_VERIFY_TYPES = {
    "BUILDING_PLAN",
    "BUILDING_PLAN_APPROVAL",
    "COMMENCEMENT_CERTIFICATE",
    "OCCUPANCY_COMPLETION_CERTIFICATE",
    "LAND_CONVERSION_DOCUMENT",
}
TITLE_SUPPORT_TYPES = {
    "PARENT_DEED",
    "ENCUMBRANCE_CERTIFICATE",
    "KHATA_PROPERTY_REGISTER",
    "MUTATION_REVENUE_RECORD",
}


def _truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"true", "yes", "present", "pending", "active"}


def _pending(value: Any) -> bool:
    if value is None:
        return False
    return "pend" in str(value).lower()


def _add_evidence(items: list[dict], document, field: str, text: str | None, source: str) -> None:
    if not text:
        return
    snippet = snippet_around(source, str(text)) or str(text)
    items.append(
        evidence_payload(
            getattr(document, "id", None),
            getattr(document, "document_type", None),
            snippet,
            field,
        )
    )


def evaluate_risks(document, extracted: dict[str, Any], source_text: str, uploaded_types: set[str]) -> list[dict]:
    uploaded_types = set(uploaded_types or [])
    uploaded_types.add(getattr(document, "document_type", None) or "OTHER")
    return [
        _ownership(document, extracted, source_text, uploaded_types),
        _litigation(document, extracted, source_text, uploaded_types),
        _mortgage(document, extracted, source_text, uploaded_types),
        _approval(document, extracted, source_text, uploaded_types),
        _property_record(document, extracted, source_text),
    ]


def _ownership(document, extracted, source_text, uploaded_types) -> dict:
    ownership = extracted.get("ownership") or {}
    transaction = extracted.get("transaction") or {}
    prop = extracted.get("property") or {}
    seller = ownership.get("seller_name")
    buyer = ownership.get("buyer_name")
    previous = transaction.get("previous_deed_number")
    survey = prop.get("survey_number")
    khata = prop.get("khata_number")
    evidence: list[dict] = []
    codes: list[str] = []
    details: dict[str, Any] = {
        "seller_name": seller,
        "buyer_name": buyer,
        "previous_deed_number": previous,
        "survey_number": survey,
        "khata_number": khata,
    }

    if not seller:
        codes.append("SELLER_NAME_MISSING")
    else:
        _add_evidence(evidence, document, "seller_name", seller, source_text)
    if not buyer:
        codes.append("BUYER_NAME_MISSING")
    else:
        _add_evidence(evidence, document, "buyer_name", buyer, source_text)
    if not previous:
        codes.append("PREVIOUS_DEED_MISSING")
    else:
        _add_evidence(evidence, document, "previous_deed_number", previous, source_text)
    if survey:
        _add_evidence(evidence, document, "survey_number", survey, source_text)
    if khata:
        _add_evidence(evidence, document, "khata_number", khata, source_text)
    if not survey and not khata:
        codes.append("PROPERTY_IDENTIFIER_MISSING")

    if codes:
        details["findings"] = codes
        if "SELLER_NAME_MISSING" in codes or "BUYER_NAME_MISSING" in codes:
            finding = {
                "category": "OWNERSHIP",
                "status": STATUS_DETECTED,
                "risk_level": RISK_MEDIUM,
                "summary": "Ownership information in the uploaded document is incomplete.",
                "finding_data": details,
                "evidence": evidence,
            }
            return ensure_finding_evidence(document, finding, source_text)
        details["findings"] = codes
        return {
            "category": "OWNERSHIP",
            "status": STATUS_NOT_VERIFIED,
            "risk_level": RISK_INFO,
            "summary": (
                "Ownership information found in the uploaded document. Full title-chain verification "
                "requires previous deeds and supporting ownership records."
            ),
            "finding_data": details,
            "evidence": evidence,
        }

    if not uploaded_types.intersection(TITLE_SUPPORT_TYPES):
        return {
            "category": "OWNERSHIP",
            "status": STATUS_NOT_VERIFIED,
            "risk_level": RISK_INFO,
            "summary": (
                "Ownership information found in the uploaded document. Full title-chain verification "
                "requires previous deeds and supporting ownership records."
            ),
            "finding_data": details,
            "evidence": evidence,
        }

    return {
        "category": "OWNERSHIP",
        "status": STATUS_NOT_VERIFIED,
        "risk_level": RISK_LOW,
        "summary": (
            "Ownership names were found, but title is not treated as fully clear until the full deed chain is checked."
        ),
        "finding_data": details,
        "evidence": evidence,
    }


def _litigation(document, extracted, source_text, uploaded_types) -> dict:
    litigation = extracted.get("litigation") or {}
    case_number = litigation.get("case_number")
    court = litigation.get("court")
    pending = _pending(litigation.get("case_status")) or _truthy(litigation.get("case_status"))
    stay = _truthy(litigation.get("stay_order"))
    restricted = _truthy(litigation.get("transfer_restricted"))
    source_hits = collect_matches(
        source_text,
        [
            r"O\.?\s*S\.?\s*No\.?\s*[\d/]+",
            r"stay order[^\n.]{0,80}",
            r"transfer/alienation is restricted[^\n.]{0,40}",
            r"pending[^\n.]{0,80}",
            r"legal notice[^\n.]{0,80}",
            r"injunction[^\n.]{0,80}",
        ],
    )
    evidence = [
        evidence_payload(getattr(document, "id", None), getattr(document, "document_type", None), hit, "litigation")
        for hit in source_hits
    ]
    details = {
        "case_number": case_number,
        "court": court,
        "case_status": "pending" if pending else litigation.get("case_status"),
        "stay_order": stay,
        "transfer_restricted": restricted,
    }

    explicit_clear = bool(
        document.document_type in LITIGATION_VERIFY_TYPES
        and collect_matches(source_text, [r"no (pending )?litigation", r"no pending case", r"not subject to any case"])
    )

    if pending or stay or restricted or case_number or source_hits:
        level = RISK_HIGH if pending or stay or restricted else RISK_MEDIUM
        summary = "An active court case is mentioned in the uploaded document."
        if stay:
            summary = "A stay order is mentioned in the uploaded document."
        if restricted:
            summary = "Transfer or alienation is restricted according to the uploaded document."
        return {
            "category": "LITIGATION",
            "status": STATUS_DETECTED,
            "risk_level": level,
            "summary": summary,
            "finding_data": details,
            "evidence": evidence,
        }

    if explicit_clear:
        return {
            "category": "LITIGATION",
            "status": STATUS_NO_ISSUE_FOUND,
            "risk_level": RISK_LOW,
            "summary": "A relevant uploaded document states there is no pending litigation.",
            "finding_data": details,
            "evidence": evidence,
        }

    return {
        "category": "LITIGATION",
        "status": STATUS_NOT_VERIFIED,
        "risk_level": RISK_INFO,
        "summary": "Litigation is not verified. Missing court records or an encumbrance certificate are needed.",
        "finding_data": details,
        "evidence": evidence,
    }


def _mortgage(document, extracted, source_text, uploaded_types) -> dict:
    mortgage = extracted.get("mortgage") or {}
    present = _truthy(mortgage.get("mortgage_present"))
    loan_status = str(mortgage.get("loan_status") or "")
    hits = collect_matches(
        source_text,
        [r"\bmortgage\b[^\n.]{0,80}", r"\bencumbrance\b[^\n.]{0,80}", r"charge created[^\n.]{0,80}", r"\blien\b[^\n.]{0,40}"],
    )
    closed = collect_matches(
        source_text,
        [r"no dues", r"loan clos", r"mortgage released", r"nil encumbrance", r"no encumbrance", r"free from encumbrance"],
    )
    evidence = [
        evidence_payload(getattr(document, "id", None), getattr(document, "document_type", None), hit, "mortgage")
        for hit in hits + closed
    ]
    details = {
        "mortgage_present": present,
        "lender": mortgage.get("lender"),
        "loan_status": loan_status or None,
    }
    has_ec = "ENCUMBRANCE_CERTIFICATE" in uploaded_types
    if (present or hits) and not closed:
        return {
            "category": "MORTGAGE",
            "status": STATUS_DETECTED,
            "risk_level": RISK_HIGH,
            "summary": "A mortgage or charge is mentioned, and closure papers were not found.",
            "finding_data": details,
            "evidence": evidence,
        }
    if has_ec and closed:
        return {
            "category": "MORTGAGE",
            "status": STATUS_NO_ISSUE_FOUND,
            "risk_level": RISK_LOW,
            "summary": "Based on the documents provided, the encumbrance record explicitly shows no encumbrance for the available period.",
            "finding_data": details,
            "evidence": evidence,
        }
    return {
        "category": "MORTGAGE",
        "status": STATUS_NOT_VERIFIED,
        "risk_level": RISK_INFO,
        "summary": "Mortgage status is not verified because an Encumbrance Certificate has not been provided.",
        "finding_data": details,
        "evidence": evidence,
    }


def _approval(document, extracted, source_text, uploaded_types) -> dict:
    approval = extracted.get("approval") or {}
    present = _truthy(approval.get("approval_present"))
    oc = _truthy(approval.get("occupancy_certificate_present"))
    unauthorized = collect_matches(
        source_text, [r"unauthori[sz]ed construction", r"deviation", r"without approval", r"illegal construction"]
    )
    evidence = [
        evidence_payload(getattr(document, "id", None), getattr(document, "document_type", None), hit, "approval")
        for hit in unauthorized
    ]
    details = {
        "approval_present": present,
        "approval_number": approval.get("approval_number"),
        "occupancy_certificate_present": oc,
        "construction_status": approval.get("construction_status"),
    }
    if unauthorized:
        return {
            "category": "APPROVAL",
            "status": STATUS_DETECTED,
            "risk_level": RISK_HIGH,
            "summary": "The uploaded document indicates unapproved or mismatched construction.",
            "finding_data": details,
            "evidence": evidence,
        }
    if uploaded_types.intersection(APPROVAL_VERIFY_TYPES) and (present or oc):
        if approval.get("approval_number"):
            _add_evidence(evidence, document, "approval_number", approval.get("approval_number"), source_text)
        return {
            "category": "APPROVAL",
            "status": STATUS_NO_ISSUE_FOUND,
            "risk_level": RISK_LOW,
            "summary": "Approval evidence in the uploaded papers is consistent for this check.",
            "finding_data": details,
            "evidence": evidence,
        }
    return {
        "category": "APPROVAL",
        "status": STATUS_NOT_VERIFIED,
        "risk_level": RISK_INFO,
        "summary": "Construction approval is not verified. A sale deed alone does not prove planning permission.",
        "finding_data": details,
        "evidence": evidence,
    }


def _property_record(document, extracted, source_text) -> dict:
    prop = extracted.get("property") or {}
    bounds = extracted.get("boundaries") or {}
    identifiers = {
        "survey_number": prop.get("survey_number"),
        "khata_number": prop.get("khata_number"),
        "area": prop.get("area"),
        "village": prop.get("village"),
        "hobli": prop.get("hobli"),
        "taluk": prop.get("taluk"),
        "district": prop.get("district"),
        "north": bounds.get("north"),
        "south": bounds.get("south"),
        "east": bounds.get("east"),
        "west": bounds.get("west"),
    }
    evidence: list[dict] = []
    for field, value in identifiers.items():
        if value:
            _add_evidence(evidence, document, field, str(value), source_text)
    present = [key for key, value in identifiers.items() if value]
    if not present:
        return {
            "category": "PROPERTY_RECORD",
            "status": STATUS_NOT_VERIFIED,
            "risk_level": RISK_INFO,
            "summary": "Property identifiers were not verified from the uploaded document.",
            "finding_data": identifiers,
            "evidence": evidence,
        }
    return {
        "category": "PROPERTY_RECORD",
        "status": STATUS_NOT_VERIFIED,
        "risk_level": RISK_INFO,
        "summary": "Property identifiers extracted successfully, but cross-document verification requires additional records.",
        "finding_data": identifiers,
        "evidence": evidence,
    }
