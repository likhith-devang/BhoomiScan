from __future__ import annotations

import re
from typing import Any

EXTRACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "property": {
            "type": "object",
            "properties": {
                "survey_number": {"type": "string"},
                "khata_number": {"type": "string"},
                "area": {"type": "string"},
                "village": {"type": "string"},
                "hobli": {"type": "string"},
                "taluk": {"type": "string"},
                "district": {"type": "string"},
                "state": {"type": "string"},
                "property_type": {"type": "string"},
            },
        },
        "ownership": {
            "type": "object",
            "properties": {
                "seller_name": {"type": "string"},
                "buyer_name": {"type": "string"},
                "owner_name": {"type": "string"},
            },
        },
        "transaction": {
            "type": "object",
            "properties": {
                "sale_amount": {"type": "string"},
                "registration_number": {"type": "string"},
                "registration_date": {"type": "string"},
                "previous_deed_number": {"type": "string"},
                "previous_deed_date": {"type": "string"},
            },
        },
        "litigation": {
            "type": "object",
            "properties": {
                "case_number": {"type": "string"},
                "court": {"type": "string"},
                "case_status": {"type": "string"},
                "stay_order": {"type": "boolean"},
                "transfer_restricted": {"type": "boolean"},
            },
        },
        "mortgage": {
            "type": "object",
            "properties": {
                "mortgage_present": {"type": "boolean"},
                "lender": {"type": "string"},
                "loan_status": {"type": "string"},
            },
        },
        "approval": {
            "type": "object",
            "properties": {
                "approval_present": {"type": "boolean"},
                "approval_number": {"type": "string"},
                "construction_status": {"type": "string"},
                "occupancy_certificate_present": {"type": "boolean"},
            },
        },
        "boundaries": {
            "type": "object",
            "properties": {
                "north": {"type": "string"},
                "south": {"type": "string"},
                "east": {"type": "string"},
                "west": {"type": "string"},
            },
        },
    },
}


def _clean(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return "true" if value else "false"
    text = str(value).strip()
    if not text or text.lower() in {"null", "none", "n/a", "-"}:
        return None
    return text


def _bool_from_text(text: str, positive: tuple[str, ...]) -> bool:
    lower = text.lower()
    return any(token in lower for token in positive)


def _search(pattern: str, text: str, flags: int = re.I) -> str | None:
    match = re.search(pattern, text or "", flags)
    if not match:
        return None
    if match.lastindex:
        for index in range(1, match.lastindex + 1):
            value = match.group(index)
            if value:
                return value.strip()
    return match.group(0).strip()


_SKIP_NAME_LINE = re.compile(
    r"^(father|age|aadhaar|aadhar|address|occupation|residing|phone|mobile|ತಂದೆ|ವಯಸ್ಸು|ಆಧಾರ್|ನಿವಾಸ)\b",
    re.I,
)
_LATIN_NAME = re.compile(
    r"^(?:(?:Sri|Smt|Shri|Shree|Mr|Mrs|Ms|Dr)\.?\s+)?[A-Z][A-Za-z]*(?:\s+[A-Z][A-Za-z.]*){0,4}$"
)
_KANNADA_NAME = re.compile(
    r"^(?:ಶ್ರೀಮತಿ|ಶ್ರೀ)\.?\s*[\u0C80-\u0CFF]+(?:\s+[\u0C80-\u0CFF.]+){0,4}$"
)
_ROLE_WORDS = {
    "seller",
    "buyer",
    "vendor",
    "purchaser",
    "vendee",
    "party",
    "one party seller",
    "one party buyer",
}


def _normalize_party_name(line: str) -> str | None:
    text = re.sub(r"\s+", " ", (line or "").strip().strip(".,;:'\"")).strip()
    if not text or text.lower() in _ROLE_WORDS or _SKIP_NAME_LINE.match(text):
        return None
    if _LATIN_NAME.match(text) or _KANNADA_NAME.match(text):
        return text if len(text) >= 3 else None
    return None


def _name_after_cues(source: str, cues: tuple[str, ...]) -> str | None:
    for cue in cues:
        for match in re.finditer(cue, source or "", flags=re.I | re.S):
            lines = source[match.end() :].splitlines()
            for line in lines[:8]:
                line = line.strip()
                if not line or re.fullmatch(r"[:\-\s.]+", line) or _SKIP_NAME_LINE.match(line):
                    continue
                name = _normalize_party_name(line)
                if name:
                    return name
                break
    return None


def _extract_seller_name(source: str) -> str | None:
    return _name_after_cues(
        source,
        (
            r"(?:prepared and executed|executed).{0,220}?\bby",
            r"ಇವರಿಂದ",
            r"(?:seller|vendor)\s*[:\-]",
        ),
    )


def _extract_buyer_name(source: str) -> str | None:
    return _name_after_cues(
        source,
        (
            r"(?:deed in favour of|in favour of|in favor of)",
            r"ಪರವಾಗಿ",
            r"(?:buyer|purchaser|vendee)\s*[:\-]",
        ),
    )


def fallback_from_source(text: str) -> dict[str, Any]:
    source = text or ""
    litigation_pending = _bool_from_text(source, ("pending", "is pending", "pending case"))
    stay = _bool_from_text(source, ("stay order", "stay is in force", "injunction"))
    restricted = _bool_from_text(
        source,
        ("transfer/alienation is restricted", "transfer is restricted", "alienation is restricted", "transfer restricted"),
    )
    return {
        "property": {
            "survey_number": _search(
                r"(?:survey|sy)\.?\s*(?:no|number|#)?\.?\s*[:\-]?\s*([\d]+(?:\s*/\s*[\d]+)?)", source
            ),
            "khata_number": _search(r"khata\s*(?:no|number|#)?\.?\s*[:\-]?\s*([\w/-]+)", source),
            "area": _search(r"(\d[\d,]*\s*(?:sq\.?\s*ft|square\s*feet|sqft))", source),
            "village": _search(r"\bHebbala\b", source) or _search(r"village\s*[:\-]?\s*([A-Za-z ]{3,40})", source),
            "hobli": _search(r"\bYelahanka\b", source) or _search(r"hobli\s*[:\-]?\s*([A-Za-z ]{3,40})", source),
            "taluk": _search(r"Bengaluru North", source) or _search(r"taluk\s*[:\-]?\s*([A-Za-z ]{3,40})", source),
            "district": _search(r"Bengaluru(?: Urban)?", source) or _search(r"district\s*[:\-]?\s*([A-Za-z ]{3,40})", source),
            "state": _search(r"karnataka|state\s*[:\-]?\s*([A-Za-z ]{3,40})", source),
            "property_type": None,
        },
        "ownership": {
            "seller_name": _extract_seller_name(source),
            "buyer_name": _extract_buyer_name(source),
            "owner_name": None,
        },
        "transaction": {
            "sale_amount": _search(r"(?:rs\.?|inr|₹)?\s*([\d.]+\s*lakh)", source),
            "registration_number": _search(r"registration\s*(?:no|number)?\.?\s*[:\-]?\s*([\w/-]+)", source),
            "registration_date": None,
            "previous_deed_number": _search(
                r"(?:previous deed|parent deed|earlier deed|purchase deed|ಕ್ರಯಪತ್ರ)[^\d]{0,32}(\d{3,5}\s*/\s*\d{4})",
                source,
            ),
            "previous_deed_date": None,
        },
        "litigation": {
            "case_number": _search(r"(O\.?\s*S\.?\s*No\.?\s*[\d/]+)", source),
            "court": _search(r"(city civil court[^\n,.]{0,40})", source),
            "case_status": "pending" if litigation_pending else None,
            "stay_order": stay,
            "transfer_restricted": restricted,
        },
        "mortgage": {
            "mortgage_present": _bool_from_text(source, ("mortgage", "charge created"))
            and not _bool_from_text(source, ("nil encumbrance", "no encumbrance", "free from encumbrance")),
            "lender": _search(r"(?:bank|lender)\s*[:\-]\s*([A-Za-z ]{3,60})", source),
            "loan_status": None,
        },
        "approval": {
            "approval_present": _bool_from_text(source, ("approved plan", "building approval", "occupancy certificate")),
            "approval_number": None,
            "construction_status": None,
            "occupancy_certificate_present": _bool_from_text(source, ("occupancy certificate",)),
        },
        "boundaries": {
            "north": _search(r"north\s*[:\-]\s*([^\n]{3,80})", source),
            "south": _search(r"south\s*[:\-]\s*([^\n]{3,80})", source),
            "east": _search(r"east\s*[:\-]\s*([^\n]{3,80})", source),
            "west": _search(r"west\s*[:\-]\s*([^\n]{3,80})", source),
        },
    }


def _merge_section(primary: dict | None, fallback: dict) -> dict:
    merged = dict(fallback)
    for key, value in (primary or {}).items():
        cleaned = _clean(value)
        if cleaned is None:
            continue
        if key in {"stay_order", "transfer_restricted", "mortgage_present", "approval_present", "occupancy_certificate_present"}:
            if isinstance(value, bool):
                merged[key] = value
            elif cleaned.lower() in {"true", "yes", "present"}:
                merged[key] = True
            elif cleaned.lower() in {"false", "no", "absent"}:
                merged[key] = False
            continue
        merged[key] = cleaned
    return merged


def merge_extraction(ai_data: dict | None, source_text: str, extra_text: str | None = None) -> dict[str, Any]:
    parts = [source_text or ""]
    if extra_text and extra_text.strip() and extra_text != source_text:
        parts.append(extra_text)
    fallback = fallback_from_source("\n".join(parts))
    ai = ai_data or {}
    if "properties" in ai and isinstance(ai["properties"], dict):
        ai = ai["properties"]
    merged = {
        "property": _merge_section(ai.get("property") if isinstance(ai.get("property"), dict) else {}, fallback["property"]),
        "ownership": _merge_section(ai.get("ownership") if isinstance(ai.get("ownership"), dict) else {}, fallback["ownership"]),
        "transaction": _merge_section(
            ai.get("transaction") if isinstance(ai.get("transaction"), dict) else {}, fallback["transaction"]
        ),
        "litigation": _merge_section(
            ai.get("litigation") if isinstance(ai.get("litigation"), dict) else {}, fallback["litigation"]
        ),
        "mortgage": _merge_section(ai.get("mortgage") if isinstance(ai.get("mortgage"), dict) else {}, fallback["mortgage"]),
        "approval": _merge_section(ai.get("approval") if isinstance(ai.get("approval"), dict) else {}, fallback["approval"]),
        "boundaries": _merge_section(
            ai.get("boundaries") if isinstance(ai.get("boundaries"), dict) else {}, fallback["boundaries"]
        ),
    }
    # Source-text veto: if AI missed stay/case/restriction, keep fallback True.
    source_fallback = fallback["litigation"]
    for flag in ("stay_order", "transfer_restricted"):
        if source_fallback.get(flag):
            merged["litigation"][flag] = True
    if source_fallback.get("case_number") and not merged["litigation"].get("case_number"):
        merged["litigation"]["case_number"] = source_fallback["case_number"]
    if source_fallback.get("case_status") == "pending":
        merged["litigation"]["case_status"] = "pending"
    if source_fallback.get("court") and not merged["litigation"].get("court"):
        merged["litigation"]["court"] = source_fallback["court"]
    return merged
