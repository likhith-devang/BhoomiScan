from __future__ import annotations

from app.constants import DOCUMENT_TYPE_LABELS, RISK_CATEGORY_LABELS, STATUS_DETECTED, STATUS_NOT_VERIFIED

NEEDED = {
    "OWNERSHIP": [
        ("PARENT_DEED", "Needed to check the earlier title chain."),
        ("ENCUMBRANCE_CERTIFICATE", "Needed to see whether the seller’s title is encumbered."),
        ("KHATA_PROPERTY_REGISTER", "Needed to match municipal ownership records."),
        ("MUTATION_REVENUE_RECORD", "Needed to match revenue mutation records."),
    ],
    "LITIGATION": [
        ("ENCUMBRANCE_CERTIFICATE", "Needed to look for recorded court attachments."),
        ("COURT_CASE_DOCUMENT", "Needed if a case number or dispute is mentioned."),
        ("COURT_ORDER", "Needed to see whether a stay or restriction is still in force."),
        ("LEGAL_NOTICE", "Needed if a dispute may exist outside the sale deed."),
        ("SELLER_AFFIDAVIT", "Needed as supporting disclosure from the seller."),
    ],
    "MORTGAGE": [
        ("ENCUMBRANCE_CERTIFICATE", "Needed to confirm whether a bank charge exists."),
        ("BANK_MORTGAGE_DOCUMENT", "Needed if a loan or mortgage is suspected."),
        ("LOAN_CLOSURE_NOC", "Needed to confirm a loan was closed."),
        ("RELEASE_DEED", "Needed to confirm a mortgage was released."),
        ("BANK_NOC", "Needed as the bank’s no-objection."),
    ],
    "APPROVAL": [
        ("BUILDING_PLAN", "Needed to check the sanctioned building plan."),
        ("BUILDING_PLAN_APPROVAL", "Needed to confirm plan approval."),
        ("COMMENCEMENT_CERTIFICATE", "Needed to confirm lawful start of construction."),
        ("OCCUPANCY_COMPLETION_CERTIFICATE", "Needed to confirm occupancy permission."),
        ("LAND_CONVERSION_DOCUMENT", "Needed if land use conversion matters for this property."),
    ],
    "PROPERTY_RECORD": [
        ("SURVEY_SKETCH", "Needed to compare survey shape and boundaries."),
        ("PROPERTY_TAX_RECEIPT", "Needed to match tax assessment details."),
        ("KHATA_PROPERTY_REGISTER", "Needed to match khata particulars."),
        ("SALE_DEED", "Needed to compare the schedule of the property."),
        ("SITE_LAYOUT_PLAN", "Needed to compare the approved site or layout plan."),
    ],
}


def build_recommendations(findings: list[dict], uploaded_types: set[str]) -> list[dict]:
    uploaded = set(uploaded_types or [])
    rows: list[dict] = []
    for finding in findings:
        category = finding["category"]
        if finding["status"] not in {STATUS_NOT_VERIFIED, STATUS_DETECTED}:
            continue
        for document_type, reason in NEEDED.get(category, []):
            if document_type in uploaded and document_type != "SALE_DEED":
                continue
            rows.append(
                {
                    "category": category,
                    "category_label": RISK_CATEGORY_LABELS[category],
                    "document_type": document_type,
                    "label": DOCUMENT_TYPE_LABELS.get(document_type, document_type),
                    "reason": reason,
                }
            )
    # Keep unique document types, first category wins.
    unique: list[dict] = []
    seen: set[str] = set()
    for row in rows:
        key = row["document_type"]
        if key in seen:
            continue
        seen.add(key)
        unique.append(row)
    return unique
