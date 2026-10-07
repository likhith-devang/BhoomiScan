from __future__ import annotations

import re


def snippet_around(text: str, needle: str, width: int = 180) -> str | None:
    if not text or not needle:
        return None
    lower = text.lower()
    index = lower.find(str(needle).lower())
    if index < 0:
        return None
    start = max(0, index - width // 3)
    end = min(len(text), index + len(str(needle)) + width)
    snippet = text[start:end].strip()
    if start > 0:
        snippet = "…" + snippet
    if end < len(text):
        snippet = snippet + "…"
    return snippet


def collect_matches(text: str, patterns: list[str]) -> list[str]:
    found: list[str] = []
    source = text or ""
    for pattern in patterns:
        match = re.search(pattern, source, flags=re.I | re.S)
        if match:
            piece = match.group(0).strip()
            if piece and piece not in found:
                found.append(piece[:400])
    return found


def evidence_payload(
    document_id,
    document_type: str | None,
    source_text: str,
    extracted_field: str,
    page_number: int | None = None,
    confidence: float | None = None,
) -> dict:
    return {
        "document_id": str(document_id) if document_id else None,
        "document_type": document_type,
        "page_number": page_number,
        "source_text": source_text,
        "extracted_field": extracted_field,
        "confidence": confidence,
    }


def _has_field(evidence: list[dict], field: str) -> bool:
    return any(item.get("extracted_field") == field for item in evidence)


def ensure_finding_evidence(document, finding: dict, source_text: str) -> dict:
    """Attach source snippets for extracted fields, including already-stored findings."""
    evidence = [item for item in (finding.get("evidence") or []) if item.get("source_text")]
    data = finding.get("finding_data") or {}
    for field, value in data.items():
        if field in {"findings"} or value in (None, "", False):
            continue
        if isinstance(value, (list, dict, bool)):
            continue
        if _has_field(evidence, field):
            continue
        snippet = snippet_around(source_text, str(value)) or str(value)
        evidence.append(
            evidence_payload(
                getattr(document, "id", None),
                getattr(document, "document_type", None),
                snippet,
                field,
            )
        )
    if finding.get("category") == "OWNERSHIP":
        for field, label in (("seller_name", "seller name"), ("buyer_name", "buyer name")):
            if data.get(field) or _has_field(evidence, field) or _has_field(evidence, f"{field}_missing"):
                continue
            excerpt = (source_text or "").strip()[:240]
            note = f"{label.capitalize()} could not be found in the uploaded document."
            if excerpt:
                note = f"{note} Excerpt reviewed: {excerpt}"
            evidence.append(
                evidence_payload(
                    getattr(document, "id", None),
                    getattr(document, "document_type", None),
                    note,
                    f"{field}_missing",
                )
            )
    finding["evidence"] = evidence
    return finding
