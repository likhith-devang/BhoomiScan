ALLOWED_DOMAINS = ("RESIDENTIAL", "AGRICULTURAL", "COMMERCIAL", "INDUSTRIAL")
ACTIVE_DOMAIN = "RESIDENTIAL"

RESIDENTIAL_PROPERTY_TYPES = (
    "VACANT_LAND",
    "INDEPENDENT_HOUSE",
    "APARTMENT_FLAT",
    "VILLA",
    "RESIDENTIAL_PLOT",
)

CASE_STATUS_ACTIVE = "ACTIVE"
DOCUMENT_STATUS_UPLOADED = "UPLOADED"
DOCUMENT_STATUS_PROCESSING = "PROCESSING"
DOCUMENT_STATUS_ANALYZED = "ANALYZED"
DOCUMENT_STATUS_FAILED = "FAILED"
DOCUMENT_STATUS_DISCARDED = "DISCARDED"

# Role-based access: SUPER_ADMIN sees all; ADMIN manages; SECONDARY_ADMIN may generate PDFs; BUYER owns own cases.
ROLE_SUPER_ADMIN = "SUPER_ADMIN"
ROLE_ADMIN = "ADMIN"
ROLE_SECONDARY_ADMIN = "SECONDARY_ADMIN"
ROLE_BUYER = "BUYER"
USER_ROLES = (ROLE_SUPER_ADMIN, ROLE_ADMIN, ROLE_SECONDARY_ADMIN, ROLE_BUYER)
DEFAULT_SIGNUP_ROLE = ROLE_BUYER
PDF_ROLES = (ROLE_SUPER_ADMIN, ROLE_ADMIN, ROLE_SECONDARY_ADMIN)
STAFF_ROLES = (ROLE_SUPER_ADMIN, ROLE_ADMIN, ROLE_SECONDARY_ADMIN)
# Staff (including secondary admins) may open cases to generate PDFs; buyers only see their own.
ALL_CASE_ACCESS_ROLES = (ROLE_SUPER_ADMIN, ROLE_ADMIN, ROLE_SECONDARY_ADMIN)
ROLE_ASSIGN_ROLES = (ROLE_SUPER_ADMIN, ROLE_ADMIN)

DOCUMENT_TYPES = (
    "SALE_DEED",
    "PARENT_DEED",
    "ENCUMBRANCE_CERTIFICATE",
    "KHATA_PROPERTY_REGISTER",
    "MUTATION_REVENUE_RECORD",
    "COURT_CASE_DOCUMENT",
    "COURT_ORDER",
    "LEGAL_NOTICE",
    "SELLER_AFFIDAVIT",
    "BANK_MORTGAGE_DOCUMENT",
    "LOAN_CLOSURE_NOC",
    "RELEASE_DEED",
    "BANK_NOC",
    "BUILDING_PLAN",
    "BUILDING_PLAN_APPROVAL",
    "COMMENCEMENT_CERTIFICATE",
    "OCCUPANCY_COMPLETION_CERTIFICATE",
    "LAND_CONVERSION_DOCUMENT",
    "SURVEY_SKETCH",
    "PROPERTY_TAX_RECEIPT",
    "SITE_LAYOUT_PLAN",
    "OTHER",
)

DOCUMENT_TYPE_LABELS = {
    "SALE_DEED": "Sale Deed",
    "PARENT_DEED": "Previous Sale Deed / Parent Deed",
    "ENCUMBRANCE_CERTIFICATE": "Encumbrance Certificate",
    "KHATA_PROPERTY_REGISTER": "Khata / Property Register",
    "MUTATION_REVENUE_RECORD": "Mutation / Revenue Record",
    "COURT_CASE_DOCUMENT": "Court Case Document",
    "COURT_ORDER": "Court Order / Judgment",
    "LEGAL_NOTICE": "Legal Notice",
    "SELLER_AFFIDAVIT": "Seller Affidavit",
    "BANK_MORTGAGE_DOCUMENT": "Bank Loan / Mortgage Document",
    "LOAN_CLOSURE_NOC": "Loan Closure / No-Dues Certificate",
    "RELEASE_DEED": "Release Deed",
    "BANK_NOC": "Bank NOC",
    "BUILDING_PLAN": "Approved Building Plan",
    "BUILDING_PLAN_APPROVAL": "Building Plan Approval",
    "COMMENCEMENT_CERTIFICATE": "Commencement Certificate",
    "OCCUPANCY_COMPLETION_CERTIFICATE": "Occupancy / Completion Certificate",
    "LAND_CONVERSION_DOCUMENT": "Land Conversion / Land Use Document",
    "SURVEY_SKETCH": "Survey Sketch",
    "PROPERTY_TAX_RECEIPT": "Property Tax Receipt",
    "SITE_LAYOUT_PLAN": "Approved Site / Layout Plan",
    "OTHER": "Other document",
}

RISK_CATEGORIES = (
    "OWNERSHIP",
    "LITIGATION",
    "MORTGAGE",
    "APPROVAL",
    "PROPERTY_RECORD",
)

RISK_CATEGORY_LABELS = {
    "OWNERSHIP": "Ownership / Title",
    "LITIGATION": "Litigation",
    "MORTGAGE": "Mortgage / Encumbrance",
    "APPROVAL": "Approval / Construction",
    "PROPERTY_RECORD": "Property Record / Boundary",
}

STATUS_DETECTED = "DETECTED"
STATUS_NO_ISSUE_FOUND = "NO_ISSUE_FOUND"
STATUS_NOT_VERIFIED = "NOT_VERIFIED"

RISK_HIGH = "HIGH"
RISK_MEDIUM = "MEDIUM"
RISK_LOW = "LOW"
RISK_INFO = "INFO"

ANALYSIS_COMPLETE = "COMPLETE"
ANALYSIS_FAILED = "FAILED"
ANALYSIS_PROCESSING = "PROCESSING"

REPORT_STATUS_FINAL = "FINAL"
LEDGER_GENESIS_HASH = "GENESIS"

COMPARISON_MATCH = "MATCH"
COMPARISON_MISMATCH = "MISMATCH"
COMPARISON_NOT_AVAILABLE = "NOT_AVAILABLE"

COVERAGE_VERIFIED = "Verified"
COVERAGE_PARTIAL = "Partially Verified"
COVERAGE_NOT_VERIFIED = "Not Verified"

# Risk score uses only DETECTED findings. NOT_VERIFIED does not add points.
RISK_SCORE_POINTS = {
    "HIGH": 70,
    "MEDIUM": 15,
    "LOW": 10,
    "INFO": 0,
}

SCORE_REASON_BY_CATEGORY = {
    "LITIGATION": "Litigation on the property",
    "OWNERSHIP": "Ownership / title issue on the property",
    "MORTGAGE": "Mortgage or encumbrance on the property",
    "APPROVAL": "Approval or construction issue on the property",
    "PROPERTY_RECORD": "Property record or boundary issue on the property",
}
RISK_SCORE_MAX = 100

COMPARISON_FIELDS = (
    ("seller_name", "ownership", "seller_name", "OWNERSHIP", "Seller name", "HIGH"),
    ("buyer_name", "ownership", "buyer_name", "OWNERSHIP", "Buyer name", "HIGH"),
    ("owner_name", "ownership", "owner_name", "OWNERSHIP", "Owner name", "HIGH"),
    ("survey_number", "property", "survey_number", "PROPERTY_RECORD", "Survey number", "HIGH"),
    ("khata_number", "property", "khata_number", "PROPERTY_RECORD", "Khata number", "MEDIUM"),
    ("area", "property", "area", "PROPERTY_RECORD", "Area", "MEDIUM"),
    ("village", "property", "village", "PROPERTY_RECORD", "Village", "MEDIUM"),
    ("hobli", "property", "hobli", "PROPERTY_RECORD", "Hobli", "MEDIUM"),
    ("taluk", "property", "taluk", "PROPERTY_RECORD", "Taluk", "MEDIUM"),
    ("district", "property", "district", "PROPERTY_RECORD", "District", "MEDIUM"),
    ("property_type", "property", "property_type", "PROPERTY_RECORD", "Property type", "MEDIUM"),
    ("north", "boundaries", "north", "PROPERTY_RECORD", "North boundary", "HIGH"),
    ("south", "boundaries", "south", "PROPERTY_RECORD", "South boundary", "HIGH"),
    ("east", "boundaries", "east", "PROPERTY_RECORD", "East boundary", "HIGH"),
    ("west", "boundaries", "west", "PROPERTY_RECORD", "West boundary", "HIGH"),
    ("registration_number", "transaction", "registration_number", "OWNERSHIP", "Registration number", "MEDIUM"),
    ("registration_date", "transaction", "registration_date", "OWNERSHIP", "Registration date", "MEDIUM"),
    ("previous_deed_number", "transaction", "previous_deed_number", "OWNERSHIP", "Previous deed number", "MEDIUM"),
)

DISCLAIMER = (
    "This report is an AI-assisted document review and is based only on the documents provided. "
    "It does not replace advice from a qualified lawyer, surveyor, government authority, or other professional."
)

KANNADA_LANGUAGE = "kn-IN"
ENGLISH_LANGUAGE = "en-IN"
TRANSLATE_CHUNK_SIZE = 1800
SARVAM_TERMINAL_STATUSES = {"completed", "partially_completed", "failed", "rejected"}
CLASSIFICATION_MIN_CONFIDENCE = 0.45

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}
ALLOWED_MIME_TYPES = {"application/pdf", "image/png", "image/jpeg", "image/jpg"}

FILE_SIGNATURES = {
    ".pdf": (b"%PDF",),
    ".png": (b"\x89PNG\r\n\x1a\n",),
    ".jpg": (b"\xff\xd8\xff",),
    ".jpeg": (b"\xff\xd8\xff",),
}
