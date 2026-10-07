from __future__ import annotations

from typing import Any

from app.constants import (
    COVERAGE_NOT_VERIFIED,
    COVERAGE_PARTIAL,
    COVERAGE_VERIFIED,
    RISK_CATEGORIES,
    RISK_CATEGORY_LABELS,
    RISK_HIGH,
    RISK_LOW,
    RISK_MEDIUM,
    RISK_SCORE_MAX,
    RISK_SCORE_POINTS,
    SCORE_REASON_BY_CATEGORY,
    STATUS_DETECTED,
    STATUS_NO_ISSUE_FOUND,
    STATUS_NOT_VERIFIED,
)
from app.services.recommendation_engine import NEEDED

# Coverage formula:
#   Verified (DETECTED or NO_ISSUE_FOUND) = 1.0
#   Partially Verified (NOT_VERIFIED but a related paper was uploaded) = 0.5
#   Not Verified = 0.0
#   coverage% = round(100 * sum(weights) / 5)
#
# Risk score formula:
#   Add 70 for each DETECTED HIGH, 15 for DETECTED MEDIUM, 10 for DETECTED LOW.
#   NOT_VERIFIED never adds points. Cap at 100.
#   Overall HIGH if any DETECTED HIGH or score >= 40; MEDIUM if score >= 10 or any DETECTED MEDIUM; else LOW.


def risk_score(findings: list[dict[str, Any]]) -> int:
    total = 0
    for finding in findings:
        if finding.get("status") != STATUS_DETECTED:
            continue
        total += RISK_SCORE_POINTS.get(finding.get("risk_level") or "", 0)
    return min(RISK_SCORE_MAX, total)


def score_reasons(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    reasons = []
    for finding in findings:
        if finding.get("status") != STATUS_DETECTED:
            continue
        points = RISK_SCORE_POINTS.get(finding.get("risk_level") or "", 0)
        if not points:
            continue
        category = finding.get("category") or ""
        reasons.append(
            {
                "category": category,
                "category_label": finding.get("category_label") or RISK_CATEGORY_LABELS.get(category, category),
                "points": points,
                "reason": SCORE_REASON_BY_CATEGORY.get(category) or finding.get("summary") or "Issue detected on the property",
            }
        )
    return reasons


def overall_risk_level(findings: list[dict[str, Any]], score: int) -> str:
    detected = [item for item in findings if item.get("status") == STATUS_DETECTED]
    if any(item.get("risk_level") == RISK_HIGH for item in detected) or score >= 40:
        return RISK_HIGH
    if any(item.get("risk_level") == RISK_MEDIUM for item in detected) or score >= 10:
        return RISK_MEDIUM
    return RISK_LOW


def _related_types(category: str) -> set[str]:
    return {item[0] for item in NEEDED.get(category, [])}


def coverage_for_category(category: str, status: str, uploaded_types: set[str]) -> str:
    if status in {STATUS_DETECTED, STATUS_NO_ISSUE_FOUND}:
        return COVERAGE_VERIFIED
    if uploaded_types.intersection(_related_types(category)):
        return COVERAGE_PARTIAL
    return COVERAGE_NOT_VERIFIED


def verification_coverage(findings: list[dict[str, Any]], uploaded_types: set[str]) -> dict[str, Any]:
    weights = {COVERAGE_VERIFIED: 1.0, COVERAGE_PARTIAL: 0.5, COVERAGE_NOT_VERIFIED: 0.0}
    categories = []
    total = 0.0
    by_category = {item["category"]: item for item in findings}
    for category in RISK_CATEGORIES:
        finding = by_category.get(category) or {}
        label = coverage_for_category(category, finding.get("status") or STATUS_NOT_VERIFIED, uploaded_types)
        total += weights[label]
        categories.append(
            {
                "category": category,
                "category_label": RISK_CATEGORY_LABELS[category],
                "coverage": label,
                "status": finding.get("status") or STATUS_NOT_VERIFIED,
            }
        )
    percent = int(round(100 * total / len(RISK_CATEGORIES)))
    return {
        "percent": percent,
        "explanation": "Coverage indicates how much of the requested due-diligence information was supported by uploaded documents. It is not a safety guarantee.",
        "categories": categories,
    }
