from __future__ import annotations

import itertools
import re
from typing import Any

from app.constants import (
    COMPARISON_FIELDS,
    COMPARISON_MATCH,
    COMPARISON_MISMATCH,
    COMPARISON_NOT_AVAILABLE,
    DOCUMENT_TYPE_LABELS,
)


_PREFIXES = (
    r"survey\s*(?:no|number|#)?\.?",
    r"sy\.?\s*no\.?",
    r"khata\s*(?:no|number|#)?\.?",
    r"reg(?:istration)?\s*(?:no|number|#)?\.?",
    r"previous\s*deed(?:\s*(?:no|number))?",
    r"area\s*(?:is|:)?",
    r"village\s*(?:name)?",
    r"hobli",
    r"taluk",
    r"district",
)


def _raw(extracted: dict[str, Any] | None, section: str, key: str) -> str | None:
    value = ((extracted or {}).get(section) or {}).get(key)
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def normalize_generic(value: str) -> str:
    text = str(value or "").casefold()
    text = re.sub(r"[\u00a0]", " ", text)
    for prefix in _PREFIXES:
        text = re.sub(rf"^\s*{prefix}\s*[:.\-]?\s*", "", text)
    text = re.sub(r"[^\w/\.]+", " ", text, flags=re.UNICODE)
    return re.sub(r"\s+", " ", text).strip()


def normalize_survey(value: str) -> str:
    text = normalize_generic(value)
    text = re.sub(r"^(?:survey|sy)\s*(?:no|number)?\s*", "", text)
    text = text.replace(" ", "")
    return text


def normalize_name(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip().casefold()


def parse_area_sqft(value: str) -> float | None:
    text = str(value or "").casefold().replace(",", "")
    match = re.search(r"(\d+(?:\.\d+)?)\s*(sq\.?\s*m|square\s*metres?|sqm|sq\.?\s*ft|square\s*feet|sqft|sft)?", text)
    if not match:
        return None
    amount = float(match.group(1))
    unit = (match.group(2) or "sqft").replace(".", "").replace(" ", "")
    if unit in {"sqm", "squaremetres", "squaremetre"}:
        return round(amount * 10.7639, 2)
    return round(amount, 2)


def values_match(field: str, left: str, right: str) -> bool:
    if field in {"seller_name", "buyer_name", "owner_name"}:
        return normalize_name(left) == normalize_name(right)
    if field == "survey_number":
        return normalize_survey(left) == normalize_survey(right)
    if field == "area":
        a = parse_area_sqft(left)
        b = parse_area_sqft(right)
        if a is not None and b is not None:
            larger = max(a, b) or 1
            return abs(a - b) / larger <= 0.02
        return normalize_generic(left) == normalize_generic(right)
    return normalize_generic(left) == normalize_generic(right)


def _label(document) -> str:
    kind = DOCUMENT_TYPE_LABELS.get(document.document_type or "", document.document_type or "Document")
    return f"{kind} ({document.original_filename})"


def compare_documents(documents: list[Any]) -> list[dict[str, Any]]:
    """Deterministic pairwise comparison. No LLM is used."""
    rows: list[dict[str, Any]] = []
    analyzed = [item for item in documents if getattr(item, "extracted_data", None)]
    for field, section, key, category, label, severity in COMPARISON_FIELDS:
        holders = []
        for document in analyzed:
            value = _raw(document.extracted_data, section, key)
            if value:
                holders.append((document, value))
        if len(holders) < 2:
            rows.append(
                {
                    "field": field,
                    "field_label": label,
                    "category": category,
                    "document_a_id": holders[0][0].id if holders else None,
                    "document_b_id": None,
                    "document_a_name": _label(holders[0][0]) if holders else None,
                    "document_b_name": None,
                    "value_a": holders[0][1] if holders else None,
                    "value_b": None,
                    "result": COMPARISON_NOT_AVAILABLE,
                    "severity": None,
                    "explanation": f"{label} could not be compared because it appears in fewer than two analyzed documents.",
                }
            )
            continue
        for left, right in itertools.combinations(holders, 2):
            doc_a, value_a = left
            doc_b, value_b = right
            matched = values_match(field, value_a, value_b)
            if matched:
                explanation = f"{label} matches between the {DOCUMENT_TYPE_LABELS.get(doc_a.document_type or '', 'first document')} and the {DOCUMENT_TYPE_LABELS.get(doc_b.document_type or '', 'second document')}."
                result = COMPARISON_MATCH
                row_severity = None
            else:
                explanation = f"{label} differs between the {DOCUMENT_TYPE_LABELS.get(doc_a.document_type or '', 'first document')} and the {DOCUMENT_TYPE_LABELS.get(doc_b.document_type or '', 'second document')}."
                result = COMPARISON_MISMATCH
                row_severity = severity
            rows.append(
                {
                    "field": field,
                    "field_label": label,
                    "category": category,
                    "document_a_id": doc_a.id,
                    "document_b_id": doc_b.id,
                    "document_a_name": _label(doc_a),
                    "document_b_name": _label(doc_b),
                    "value_a": value_a,
                    "value_b": value_b,
                    "result": result,
                    "severity": row_severity,
                    "explanation": explanation,
                }
            )
    return rows
