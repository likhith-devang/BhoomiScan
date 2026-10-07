from __future__ import annotations

import re

from app.constants import CLASSIFICATION_MIN_CONFIDENCE, DOCUMENT_TYPE_LABELS

KEYWORD_MAP: list[tuple[str, tuple[str, ...]]] = [
    ("SALE_DEED", ("sale deed", "deed of sale", "conveyance", "vendor", "vendee", "consideration")),
    ("PARENT_DEED", ("parent deed", "previous deed", "earlier deed", "mother deed")),
    ("ENCUMBRANCE_CERTIFICATE", ("encumbrance certificate", "encumbrance", "nil encumbrance")),
    ("KHATA_PROPERTY_REGISTER", ("khata", "katha", "property register", "form 9", "form 11")),
    ("MUTATION_REVENUE_RECORD", ("mutation", "rtc", "pahani", "revenue record")),
    ("COURT_CASE_DOCUMENT", ("plaint", "written statement", "o.s. no", "os no", "case number")),
    ("COURT_ORDER", ("court order", "judgment", "decree", "injunction order")),
    ("LEGAL_NOTICE", ("legal notice", "advocate notice")),
    ("SELLER_AFFIDAVIT", ("affidavit", "sworn statement")),
    ("BANK_MORTGAGE_DOCUMENT", ("mortgage", "equitable mortgage", "loan agreement", "charge created")),
    ("LOAN_CLOSURE_NOC", ("loan closure", "no dues", "no-dues", "loan closed")),
    ("RELEASE_DEED", ("release deed", "discharge of mortgage")),
    ("BANK_NOC", ("bank noc", "no objection certificate")),
    ("BUILDING_PLAN", ("building plan", "sanctioned plan", "approved plan")),
    ("BUILDING_PLAN_APPROVAL", ("plan approval", "building plan approval", "bbmp approval")),
    ("COMMENCEMENT_CERTIFICATE", ("commencement certificate", "cc issued")),
    ("OCCUPANCY_COMPLETION_CERTIFICATE", ("occupancy certificate", "completion certificate")),
    ("LAND_CONVERSION_DOCUMENT", ("land conversion", "change of land use", "clu")),
    ("SURVEY_SKETCH", ("survey sketch", "tippani", "akarband")),
    ("PROPERTY_TAX_RECEIPT", ("property tax", "tax paid", "tax receipt")),
    ("SITE_LAYOUT_PLAN", ("layout plan", "site plan", "approved layout")),
]


def classify_document(text: str, filename: str = "") -> dict:
    haystack = f"{filename}\n{text}".lower()
    scores: dict[str, int] = {}
    for doc_type, keywords in KEYWORD_MAP:
        score = sum(1 for word in keywords if word in haystack)
        if score:
            scores[doc_type] = score
    if not scores:
        return {
            "document_type": "OTHER",
            "confidence": 0.2,
            "note": "Document type could not be confidently identified.",
        }
    best_type, best_score = max(scores.items(), key=lambda item: item[1])
    total = sum(scores.values())
    confidence = round(min(0.95, 0.35 + (best_score / max(total, 1)) * 0.6), 2)
    if confidence < CLASSIFICATION_MIN_CONFIDENCE:
        return {
            "document_type": "OTHER",
            "confidence": confidence,
            "note": "Document type could not be confidently identified.",
        }
    return {
        "document_type": best_type,
        "confidence": confidence,
        "note": f"Identified as {DOCUMENT_TYPE_LABELS.get(best_type, best_type)}.",
    }


def looks_like_kannada(text: str) -> bool:
    kannada = len(re.findall(r"[\u0C80-\u0CFF]", text or ""))
    latin = len(re.findall(r"[A-Za-z]", text or ""))
    if kannada == 0:
        return False
    return kannada >= 8 or kannada > latin
