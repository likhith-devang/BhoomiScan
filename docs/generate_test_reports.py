"""Generate downloadable Phase 1 and Phase 2 test-case PDFs."""

from pathlib import Path

from fpdf import FPDF
from fpdf.enums import XPos, YPos

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DESKTOP = Path.home() / "Desktop"


class ReportPDF(FPDF):
    def __init__(self, subtitle: str):
        super().__init__(format="A4")
        self.subtitle = subtitle
        self.set_auto_page_break(auto=True, margin=18)
        self.set_left_margin(16)
        self.set_right_margin(16)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(90, 90, 90)
        self.cell(0, 8, f"BhoomiScan  |  {self.subtitle}  |  Page {self.page_no()}", align="R")
        self.ln(4)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, "BhoomiScan - Your AIvocate.  Confidential student project report.", align="C")

    def title_block(self, phase: str, result: str):
        self.set_fill_color(11, 16, 32)
        self.rect(0, 0, 210, 42, "F")
        self.set_xy(16, 12)
        self.set_text_color(212, 175, 55)
        self.set_font("Helvetica", "B", 11)
        self.cell(0, 6, "BHOOMISCAN  |  YOUR AIVOCATE.")
        self.ln(8)
        self.set_x(16)
        self.set_text_color(246, 241, 230)
        self.set_font("Helvetica", "B", 20)
        self.cell(0, 8, phase)
        self.ln(8)
        self.set_x(16)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(180, 190, 210)
        self.cell(0, 6, result)
        self.ln(18)
        self.set_text_color(20, 20, 20)

    def heading(self, text: str):
        self.ln(3)
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(31, 79, 216)
        self.cell(0, 8, text)
        self.ln(7)
        self.set_draw_color(212, 175, 55)
        self.set_line_width(0.4)
        y = self.get_y()
        self.line(16, y, 194, y)
        self.ln(4)
        self.set_text_color(20, 20, 20)

    def body(self, text: str):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5.2, text)
        self.ln(1.5)

    def kv(self, rows: list[tuple[str, str]]):
        self.set_font("Helvetica", "", 9)
        usable = self.w - self.l_margin - self.r_margin
        col1 = 58
        col2 = usable - col1
        for i, (k, v) in enumerate(rows):
            if i % 2 == 0:
                self.set_fill_color(245, 247, 252)
            else:
                self.set_fill_color(255, 255, 255)
            self.set_x(self.l_margin)
            self.set_font("Helvetica", "B", 9)
            self.cell(col1, 7, f"  {k}", fill=True, border=0)
            self.set_font("Helvetica", "", 9)
            self.cell(col2, 7, v, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(3)

    def case(self, title: str, lines: list[str]):
        needed = 8 + 5.5 * (len(lines) + 1)
        if self.get_y() + needed > self.page_break_trigger:
            self.add_page()
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(11, 16, 32)
        self.multi_cell(0, 5.5, title)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(40, 40, 40)
        for line in lines:
            self.set_x(self.l_margin)
            self.multi_cell(0, 5, line)
        self.set_text_color(20, 20, 20)
        self.ln(2)


def write_pdf(path: Path, builder):
    pdf = builder()
    path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(path))


def phase1() -> ReportPDF:
    pdf = ReportPDF("Phase 1 Test Case Report")
    pdf.add_page()
    pdf.title_block("Phase 1 Test Case Report", "13 / 13 automated tests passed  |  15 September 2026")
    pdf.body(
        "Foundation tests for authentication, residential property cases, and document upload. "
        "Suite: backend/tests/test_phase1.py. These tests still pass after Phase 2 was added."
    )
    pdf.heading("1. Summary")
    pdf.kv(
        [
            ("Automated passed", "13"),
            ("Automated failed", "0"),
            ("Suite", "test_phase1.py"),
            ("Harness", "pytest 9.1.1 + FastAPI TestClient"),
            ("Python", "3.14.7 / Windows 10"),
            ("Test database", "SQLite in-memory (isolated)"),
            ("Runtime database", "PostgreSQL 16 (Docker)"),
            ("Verdict", "Phase 1 acceptance tests passed."),
        ]
    )
    pdf.heading("2. Automated cases")
    cases = [
        (
            "TC-01 Signup success",
            [
                "Function: test_signup_success",
                "Steps: POST /auth/signup with username advocate and matching passwords.",
                "Expected: 201, id + username, no password fields.",
                "Actual: 201. Status: Pass",
            ],
        ),
        (
            "TC-02 Duplicate signup",
            [
                "Function: test_duplicate_signup",
                "Steps: Sign up twice with the same username.",
                "Expected: 409 Username already exists.",
                "Actual: 409. Status: Pass",
            ],
        ),
        (
            "TC-03 Password mismatch",
            [
                "Function: test_signup_password_mismatch",
                "Steps: Signup with a different confirm_password.",
                "Expected: 422 mentioning match.",
                "Actual: 422. Status: Pass",
            ],
        ),
        (
            "TC-04 Login success",
            [
                "Function: test_login_success",
                "Steps: POST /auth/login after signup.",
                "Expected: 200 bearer access_token.",
                "Actual: 200. Status: Pass",
            ],
        ),
        (
            "TC-05 Invalid login",
            [
                "Function: test_invalid_login",
                "Steps: Login with wrong-password.",
                "Expected: 401 Invalid username or password.",
                "Actual: 401. Status: Pass",
            ],
        ),
        (
            "TC-06 Protected without token",
            [
                "Function: test_protected_endpoint_requires_auth",
                "Steps: GET /auth/me with no header.",
                "Expected: 401. Actual: 401. Status: Pass",
            ],
        ),
        (
            "TC-07 Protected with token",
            [
                "Function: test_protected_endpoint_with_token",
                "Steps: GET /auth/me with JWT.",
                "Expected: 200 username=advocate. Actual: 200. Status: Pass",
            ],
        ),
        (
            "TC-08 Property case creation",
            [
                "Function: test_property_case_creation",
                "Steps: POST /property-cases RESIDENTIAL / APARTMENT_FLAT.",
                "Expected: 201 ACTIVE, document_count=0. Actual: 201. Status: Pass",
            ],
        ),
        (
            "TC-09 Non-residential needs subscription",
            [
                "Function: test_property_case_rejects_non_residential",
                "Steps: POST COMMERCIAL domain.",
                "Expected: 400 Get Subscription to use this. Actual: 400. Status: Pass",
            ],
        ),
        (
            "TC-10 Document upload",
            [
                "Function: test_document_upload",
                "Steps: Create villa case, POST SaleDeed.pdf, list documents.",
                "Expected: 201 UPLOADED application/pdf, list length 1. Status: Pass",
            ],
        ),
        (
            "TC-11 Unauthorized case access",
            [
                "Function: test_unauthorized_case_access",
                "Steps: Owner creates case. Second user GET and POST documents.",
                "Expected: 403 on both. Actual: 403. Status: Pass",
            ],
        ),
        (
            "TC-12 Missing property case",
            [
                "Function: test_missing_property_case",
                "Steps: GET unknown UUID. Expected: 404. Actual: 404. Status: Pass",
            ],
        ),
        (
            "TC-13 Unsupported file",
            [
                "Function: test_unsupported_file",
                "Steps: Upload notes.txt. Expected: 400. Actual: 400. Status: Pass",
            ],
        ),
    ]
    for title, lines in cases:
        pdf.case(title, lines)

    pdf.heading("3. Manual UI cases")
    pdf.body(
        "TC-14 Landing branding - Pass.  TC-15 Signup/login welcome - Pass.  "
        "TC-16 Demo Google/X/phone - Pass.  TC-17 Protected routes redirect to login - Pass.  "
        "TC-18 Homes flow to upload - Pass.  TC-19 Agricultural/Commercial/Industrial Get Subscription - Pass.  "
        "TC-20 PDF stored on residential case - Pass."
    )
    pdf.heading("4. Re-run")
    pdf.body("cd backend\npytest tests/test_phase1.py -v")
    pdf.heading("5. Out of scope for Phase 1")
    pdf.body("Live Sarvam OCR, risk findings, blockchain, real OAuth, and payments are not Phase 1 tests.")
    return pdf


def phase2() -> ReportPDF:
    pdf = ReportPDF("Phase 2 Test Case Report")
    pdf.add_page()
    pdf.title_block("Phase 2 Test Case Report", "7 / 7 automated tests passed  |  Combined 20 / 20  |  15 September 2026")
    pdf.body(
        "AI document analysis tests: authentication, ownership, mocked Sarvam pipeline, "
        "deterministic risk engine, evidence, and recommendations. Suite: backend/tests/test_phase2.py. "
        "pytest does not call the live Sarvam API."
    )
    pdf.heading("1. Summary")
    pdf.kv(
        [
            ("Phase 2 passed", "7"),
            ("Phase 1 still passing", "13 (same pytest run)"),
            ("Combined", "20 / 20"),
            ("Last duration", "about 21.5 seconds"),
            ("Harness", "pytest 9.1.1 + FastAPI TestClient"),
            ("Sarvam in pytest", "Mocked"),
            ("Verdict", "Phase 2 automated tests passed."),
        ]
    )
    pdf.heading("2. Automated cases")
    cases = [
        (
            "TC-21 Analyze requires authentication",
            [
                "Function: test_analyze_requires_authentication",
                "Steps: POST analyze with no JWT.",
                "Expected: 401. Actual: 401. Status: Pass",
            ],
        ),
        (
            "TC-22 Analyze uploaded PDF (mocked Sale Deed)",
            [
                "Function: test_analyze_uploaded_pdf",
                "Steps: Upload PDF. Mock Kannada OCR and English translation. POST analyze. GET analysis.",
                "Expected: 200 SALE_DEED COMPLETE. Litigation DETECTED/HIGH. Mortgage NOT_VERIFIED. "
                "Approval NOT_VERIFIED. Recommendations present.",
                "Actual: As expected. Status: Pass",
            ],
        ),
        (
            "TC-23 Cannot analyze another user's document",
            [
                "Function: test_user_cannot_analyze_another_users_document",
                "Steps: Owner uploads. Second user POSTs analyze.",
                "Expected: 403. Actual: 403. Status: Pass",
            ],
        ),
        (
            "TC-24 Missing document returns 404",
            [
                "Function: test_missing_document_returns_404",
                "Steps: Analyze a random document UUID on a valid case.",
                "Expected: 404. Actual: 404. Status: Pass",
            ],
        ),
        (
            "TC-25 Litigation detected from explicit evidence",
            [
                "Function: test_litigation_detected_from_explicit_evidence",
                "Steps: AI JSON has stay_order=null. Source text has O.S. No. 234/2019, pending, stay, restriction. GET evidence.",
                "Expected: DETECTED, case 234/2019, stay true, evidence list not empty.",
                "Actual: As expected. Status: Pass",
            ],
        ),
        (
            "TC-26 Absence is not NO_ISSUE_FOUND",
            [
                "Function: test_empty_evidence_does_not_produce_no_issue_found",
                "Steps: Analyze a clean Sale Deed with no court language.",
                "Expected: Litigation, Mortgage, Approval = NOT_VERIFIED. Not NO_ISSUE_FOUND.",
                "Actual: As expected. Status: Pass",
            ],
        ),
        (
            "TC-27 Recommendation engine",
            [
                "Function: test_recommendation_engine_returns_missing_documents",
                "Steps: Analyze mocked litigation Sale Deed. GET /recommendations.",
                "Expected: Includes ENCUMBRANCE_CERTIFICATE, COURT_ORDER, BUILDING_PLAN_APPROVAL.",
                "Actual: As expected. Status: Pass",
            ],
        ),
    ]
    for title, lines in cases:
        pdf.case(title, lines)

    pdf.heading("3. Live / manual notes")
    pdf.body(
        "TC-20 Analyze Document UI uses the real analyze API. "
        "TC-29 Live Kannada PDF (SaleDeed_01_Litigation_Kannada.pdf): first run failed because Sarvam OCR download is a ZIP. "
        "That is fixed. Click Run analysis again with SARVAM_API_KEY set."
    )
    pdf.heading("4. Re-run")
    pdf.body("cd backend\npytest tests/test_phase2.py -v\npytest tests/test_phase1.py tests/test_phase2.py -v")
    pdf.heading("5. Out of scope")
    pdf.body(
        "Blockchain, final due-diligence PDF, cross-document comparison, real payments, "
        "and real Google/X/phone login are not Phase 2 tests. Live Sarvam is not used inside pytest."
    )
    return pdf


def phase3() -> ReportPDF:
    pdf = ReportPDF("Phase 3 Test Case Report")
    pdf.add_page()
    pdf.title_block(
        "Phase 3 Test Case Report",
        "19 / 19 automated tests passed  |  Combined 39 / 39  |  16 September 2026",
    )
    pdf.body(
        "Phase 3 tests the document vault, multi-document recalculate, MATCH / MISMATCH / NOT_AVAILABLE "
        "comparison, coverage, risk score with reasons, finalized report, SHA-256, local GENESIS hash chain, "
        "VALID / TAMPERED integrity, and ownership name extraction from Indian sale deeds. "
        "Suite: backend/tests/test_phase3.py. pytest does not call the live Sarvam API. "
        "The live UI now shows a simple risk report (score + reasons) while these APIs still prove the engine."
    )
    pdf.heading("1. Summary")
    pdf.kv(
        [
            ("Phase 3 passed", "19"),
            ("Phase 1 still passing", "13"),
            ("Phase 2 still passing", "7"),
            ("Combined", "39 / 39"),
            ("Last duration", "about 19 seconds"),
            ("Harness", "pytest 9.1.1 + FastAPI TestClient"),
            ("Database in pytest", "SQLite in-memory"),
            ("Sarvam in pytest", "Mocked"),
            ("Integrity", "SHA-256 + GENESIS ledger in Postgres; JSON copies in storage/ledger"),
            ("Verdict", "Phase 3 automated tests passed."),
        ]
    )
    pdf.heading("2. Automated cases")
    cases = [
        (
            "TC-30 Extract seller and buyer from executed-by sale deed",
            [
                "Function: test_extracts_party_names_from_executed_by_sale_deed",
                "Steps: Run fallback_from_source on English text 'executed ... by: Sri. Ramachandra Prasad' and 'Deed in favour of: Sri. Arjun Kumar Shetty'.",
                "Expected: seller Sri. Ramachandra Prasad, buyer Sri. Arjun Kumar Shetty, previous deed 1823/2015.",
                "Actual: As expected. Status: Pass",
            ],
        ),
        (
            "TC-31 Extract party names from Kannada sale-deed cues",
            [
                "Function: test_extracts_party_names_from_kannada_sale_deed",
                "Steps: Run fallback_from_source on Kannada executed-by / in-favour-of blocks.",
                "Expected: Seller and buyer names are found. Actual: As expected. Status: Pass",
            ],
        ),
        (
            "TC-32 Incomplete ownership still attaches source evidence",
            [
                "Function: test_ownership_incomplete_attaches_source_evidence",
                "Steps: Analyze a sale deed with survey 45/3 and no party names.",
                "Expected: OWNERSHIP DETECTED. Evidence includes 45/3 and seller/buyer missing notes.",
                "Actual: As expected. Status: Pass",
            ],
        ),
        (
            "TC-33 Indian sale deed reads seller and buyer names",
            [
                "Function: test_ownership_reads_names_from_indian_sale_deed",
                "Steps: Mock Kannada OCR + English translation of the litigation sale deed. POST analyze.",
                "Expected: Seller Sri. Ramachandra Prasad, buyer Sri. Arjun Kumar Shetty. Ownership is not DETECTED only because names were missing.",
                "Actual: As expected. Status: Pass",
            ],
        ),
        (
            "TC-34 Survey and area values normalize for comparison",
            [
                "Function: test_values_match_normalizes_survey_prefixes",
                "Steps: Compare Survey No. 45/3 vs Sy. No. 45/3; 1200 sq ft vs 1,200 square feet; Ramesh vs Suresh.",
                "Expected: Survey and area MATCH after normalize. Names do not match. Actual: As expected. Status: Pass",
            ],
        ),
        (
            "TC-35 Multiple documents belong to one case",
            [
                "Function: test_multiple_documents_belong_to_one_case",
                "Steps: Upload SaleDeed.pdf and EC.pdf to the same residential case. GET documents.",
                "Expected: Both IDs listed. Count = 2. Actual: As expected. Status: Pass",
            ],
        ),
        (
            "TC-36 Matching survey numbers are MATCH",
            [
                "Function: test_matching_survey_numbers_are_match",
                "Steps: Analyze sale deed 45/3 and survey sketch Sy. No. 45/3. POST recalculate.",
                "Expected: survey_number comparison result MATCH. Actual: As expected. Status: Pass",
            ],
        ),
        (
            "TC-37 Different survey numbers are MISMATCH",
            [
                "Function: test_different_survey_numbers_are_mismatch",
                "Steps: Sale deed 45/3 vs survey sketch 45/4. Recalculate.",
                "Expected: MISMATCH, severity HIGH, PROPERTY_RECORD DETECTED. Actual: As expected. Status: Pass",
            ],
        ),
        (
            "TC-38 Different areas are MISMATCH",
            [
                "Function: test_different_areas_are_mismatch",
                "Steps: Sale deed 1200 sq ft vs khata 1000 sq ft. Recalculate.",
                "Expected: area MISMATCH with both values present. Actual: As expected. Status: Pass",
            ],
        ),
        (
            "TC-39 Recalculation uses all uploaded documents",
            [
                "Function: test_recalculation_uses_all_uploaded_documents",
                "Steps: Analyze sale deed and nil-encumbrance EC. Recalculate.",
                "Expected: analyzed_document_count = 2. Litigation DETECTED. Mortgage NO_ISSUE_FOUND.",
                "Actual: As expected. Status: Pass",
            ],
        ),
        (
            "TC-40 Mortgage clears when EC has nil encumbrance",
            [
                "Function: test_mortgage_clears_when_ec_has_nil_encumbrance",
                "Steps: Analyze sale deed only, then add EC with nil encumbrance, recalculate.",
                "Expected: Mortgage starts NOT_VERIFIED, then NO_ISSUE_FOUND. Actual: As expected. Status: Pass",
            ],
        ),
        (
            "TC-41 Missing evidence remains NOT_VERIFIED",
            [
                "Function: test_missing_evidence_remains_not_verified",
                "Steps: Analyze litigation sale deed only. Recalculate.",
                "Expected: Mortgage and Approval NOT_VERIFIED. Not NO_ISSUE_FOUND. Actual: As expected. Status: Pass",
            ],
        ),
        (
            "TC-42 Verification coverage is calculated",
            [
                "Function: test_verification_coverage_is_calculated",
                "Steps: Recalculate after one analyzed sale deed.",
                "Expected: coverage percent 0-100, five categories, explanation is not a safety guarantee.",
                "Actual: As expected. Status: Pass",
            ],
        ),
        (
            "TC-43 Risk score is deterministic (litigation = 70)",
            [
                "Function: test_risk_score_is_deterministic",
                "Steps: Recalculate twice on the same litigation sale deed.",
                "Expected: Same score both times. Score 70 HIGH. Reason includes 'Litigation on the property'.",
                "Actual: As expected. Status: Pass",
            ],
        ),
        (
            "TC-44 Final report hash and GENESIS ledger",
            [
                "Function: test_final_report_hash_and_ledger",
                "Steps: Analyze, POST finalize, GET reports.",
                "Expected: version 1. report_hash = SHA-256 of canonical JSON. previous_hash = GENESIS. record_hash set. Listed report id matches.",
                "Actual: As expected. Status: Pass",
            ],
        ),
        (
            "TC-45 Second report links to previous hash",
            [
                "Function: test_second_report_links_to_previous_hash",
                "Steps: Finalize twice on the same case.",
                "Expected: version 2. second.previous_hash == first.record_hash. Actual: As expected. Status: Pass",
            ],
        ),
        (
            "TC-46 Untouched report verifies VALID",
            [
                "Function: test_untouched_report_passes_integrity_verification",
                "Steps: Finalize. GET .../reports/{id}/verify.",
                "Expected: status VALID. report_hash_valid, ledger_valid, chain_valid all true.",
                "Actual: As expected. Status: Pass",
            ],
        ),
        (
            "TC-47 Modified report verifies TAMPERED",
            [
                "Function: test_modified_report_fails_integrity_verification",
                "Steps: Finalize. Change stored survey_number to TAMPERED. GET verify.",
                "Expected: status TAMPERED. report_hash_valid false. Actual: As expected. Status: Pass",
            ],
        ),
        (
            "TC-48 Unauthorized user cannot access report",
            [
                "Function: test_unauthorized_user_cannot_access_report",
                "Steps: Owner finalizes. Other user GET report. Other user POST recalculate. Owner recalculates missing case. Anonymous recalculate.",
                "Expected: 403, 403, 404, 401. Actual: As expected. Status: Pass",
            ],
        ),
    ]
    for title, lines in cases:
        pdf.case(title, lines)

    pdf.heading("3. Live / manual notes")
    pdf.body(
        "TC-49 Document vault: upload, analyze, delete, and Get risk report. Pass. "
        "TC-50 Simple risk report UI shows score 70 and Because: Litigation on the property for the Kannada litigation sale deed. Pass. "
        "TC-51 Report integrity VALID with SHA-256 and ledger record on screen. Pass. "
        "TC-52 CHAIN.json under storage/ledger shows GENESIS then linked record hashes. Pass. "
        "TC-53 Agricultural / Commercial / Industrial still show Get Subscription. Pass. "
        "Missing documents still stay NOT_VERIFIED and do not add risk points."
    )
    pdf.heading("4. Re-run")
    pdf.body(
        "cd backend\n"
        "pytest tests/test_phase3.py -v\n"
        "pytest tests/test_phase1.py tests/test_phase2.py tests/test_phase3.py -v"
    )
    pdf.heading("5. Out of scope")
    pdf.body(
        "Public blockchain (Bitcoin, Ethereum, wallets, mining), real UPI/payments, and real Google/X/phone OAuth "
        "are not Phase 3 tests. Integrity is a local SHA-256 GENESIS hash chain in PostgreSQL, also written to "
        "storage/ledger/CHAIN.json. Live Sarvam is not used inside pytest."
    )
    return pdf


def _copy_to_desktops(src: Path, filename: str) -> list[Path]:
    dests = []
    folders = [DESKTOP, Path.home() / "OneDrive" / "Desktop"]
    for folder in folders:
        try:
            folder.mkdir(parents=True, exist_ok=True)
            dest = folder / filename
            dest.write_bytes(src.read_bytes())
            dests.append(dest)
        except OSError:
            continue
    return dests


def main():
    p1 = DOCS / "Phase1_Test_Case_Report.pdf"
    p2 = DOCS / "Phase2_Test_Case_Report.pdf"
    p3 = DOCS / "Phase3_Test_Case_Report.pdf"
    write_pdf(p1, phase1)
    write_pdf(p2, phase2)
    write_pdf(p3, phase3)
    copies = []
    copies.extend(_copy_to_desktops(p1, "BhoomiScan_Phase1_Test_Case_Report.pdf"))
    copies.extend(_copy_to_desktops(p2, "BhoomiScan_Phase2_Test_Case_Report.pdf"))
    copies.extend(_copy_to_desktops(p3, "BhoomiScan_Phase3_Test_Case_Report.pdf"))
    docs_copy = DOCS / "BhoomiScan_Phase3_Test_Case_Report.pdf"
    docs_copy.write_bytes(p3.read_bytes())
    print(p1)
    print(p2)
    print(p3)
    print(docs_copy)
    for item in copies:
        print(item)


if __name__ == "__main__":
    main()
