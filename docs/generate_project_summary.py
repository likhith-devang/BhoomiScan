"""Generate a downloadable BhoomiScan complete project summary PDF."""

from pathlib import Path

from fpdf import FPDF
from fpdf.enums import XPos, YPos

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DESKTOP = Path.home() / "Desktop"
ONEDRIVE_DESKTOP = Path.home() / "OneDrive" / "Desktop"


def ascii(text: str) -> str:
    return str(text or "").encode("latin-1", "replace").decode("latin-1")


class SummaryPDF(FPDF):
    def __init__(self):
        super().__init__(format="A4")
        self.subtitle = "Complete Project Summary"
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
        self.cell(0, 8, "BhoomiScan - Your AIvocate.  Student project summary. Not a legal opinion.", align="C")

    def cover(self):
        self.set_fill_color(11, 16, 32)
        self.rect(0, 0, 210, 92, "F")
        self.set_xy(16, 22)
        self.set_text_color(212, 175, 55)
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 7, "BHOOMISCAN  |  YOUR AIVOCATE.")
        self.ln(12)
        self.set_x(16)
        self.set_text_color(246, 241, 230)
        self.set_font("Helvetica", "B", 24)
        self.multi_cell(0, 10, "Complete Project Summary")
        self.ln(2)
        self.set_x(16)
        self.set_font("Helvetica", "", 11)
        self.set_text_color(180, 190, 210)
        self.multi_cell(
            0,
            6,
            "Introduction, problem, objectives, methodology, implementation, architecture, tech stack, flow, tests, limitations, and conclusion.\n"
            "Source brief for a detailed report, PPT, or viva.\n"
            "16 September 2026  |  Version 0.1.0  |  Final-year college project",
        )
        self.ln(14)
        self.set_text_color(20, 20, 20)

    def heading(self, text: str):
        needed = 22
        if self.get_y() + needed > self.page_break_trigger:
            self.add_page()
        self.ln(4)
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(31, 79, 216)
        self.cell(0, 8, ascii(text), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(212, 175, 55)
        self.set_line_width(0.4)
        y = self.get_y()
        self.line(16, y, 194, y)
        self.ln(4)
        self.set_text_color(20, 20, 20)

    def sub(self, text: str):
        if self.get_y() + 16 > self.page_break_trigger:
            self.add_page()
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(11, 16, 32)
        self.multi_cell(0, 6, ascii(text))
        self.set_text_color(20, 20, 20)
        self.ln(1)

    def body(self, text: str):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.2, ascii(text))
        self.ln(1.5)

    def bullets(self, items: list[str]):
        self.set_font("Helvetica", "", 10)
        for item in items:
            if self.get_y() + 10 > self.page_break_trigger:
                self.add_page()
            self.set_x(self.l_margin)
            self.multi_cell(0, 5.1, ascii(f"- {item}"))
        self.ln(1.5)

    def kv(self, rows: list[tuple[str, str]]):
        usable = self.w - self.l_margin - self.r_margin
        col1 = 58
        col2 = usable - col1
        for i, (k, v) in enumerate(rows):
            if self.get_y() + 9 > self.page_break_trigger:
                self.add_page()
            self.set_fill_color(245, 247, 252) if i % 2 == 0 else self.set_fill_color(255, 255, 255)
            self.set_x(self.l_margin)
            self.set_font("Helvetica", "B", 8)
            self.cell(col1, 7, ascii(f"  {k}")[:42], fill=True, border=0)
            self.set_font("Helvetica", "", 8)
            self.cell(col2, 7, ascii(v)[:92], fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(3)


def build() -> SummaryPDF:
    pdf = SummaryPDF()
    pdf.add_page()
    pdf.cover()

    pdf.heading("1. Introduction")
    pdf.body(
        "BhoomiScan (tagline: Your AIvocate.) is an AI-assisted residential property due-diligence web application. "
        "A logged-in user creates a residential property file, uploads PDFs or images, runs Sarvam Document AI for OCR and Kannada-to-English translation, "
        "then a deterministic Python risk engine (not an LLM) scores five risk categories, compares multiple documents, "
        "builds a versioned report, SHA-256 hashes it, stores a local blockchain-style hash chain, and verifies integrity."
    )
    pdf.body(
        "It helps a buyer check papers before buying. It is not a lawyer, not a government portal, not a payment product, and not a legal guarantee. "
        "Focus: Karnataka-style papers, including Kannada scans. UI: dark navy, gold, ivory type, rounded royal cards, simple English."
    )
    pdf.kv(
        [
            ("Product", "BhoomiScan - Your AIvocate."),
            ("Type", "Final-year college project"),
            ("Version", "0.1.0"),
            ("Frontend", "http://localhost:5173"),
            ("Backend", "http://127.0.0.1:8000"),
            ("Health", "GET /health"),
            ("Workspace", "BhoomiScanV18"),
        ]
    )

    pdf.heading("2. Problem statement")
    pdf.bullets(
        [
            "Property papers are scanned, often in Kannada, and hard for a buyer to read.",
            "Risk sits in five areas: ownership/title, litigation, mortgage/encumbrance, approval/construction, property record/boundary.",
            "Buyers often treat missing papers as no problem. That is dangerous.",
            "Cross-document mismatches (Sale Deed survey 45/3 vs Survey Sketch 45/4) are easy to miss.",
            "There was no simple local student tool that does OCR, translate, extract, evidence, risk, recommend more papers, combine the case, report, and tamper-evident hash.",
            "Commercial tools may be costly, English-only, or overclaim that a property is legally clear.",
        ]
    )
    pdf.body(
        "Academic question: Can a student-scale full-stack system use Indic Document AI plus deterministic rules to show DETECTED / NOT_VERIFIED / NO_ISSUE_FOUND with evidence, without faking AI, payments, or a public blockchain?"
    )

    pdf.heading("3. Objectives")
    pdf.sub("3.1 Primary")
    pdf.body(
        "Build an end-to-end local web system: Upload -> AI analysis -> more documents -> compare -> recalculate risks -> coverage and risk score -> final report -> SHA-256 -> local ledger -> verify."
    )
    pdf.sub("3.2 Specific")
    pdf.bullets(
        [
            "JWT auth (username + password, bcrypt).",
            "Property case per user; only RESIDENTIAL analysis is live.",
            "Upload PDF/PNG/JPG, max 10 MB, magic-byte check, disk + PostgreSQL metadata.",
            "Sarvam digitise, Kannada translate in 1800-char chunks, optional structured extract.",
            "Classify document type (sale deed, EC, khata, and others).",
            "Five risk categories; statuses DETECTED / NO_ISSUE_FOUND / NOT_VERIFIED; levels HIGH / MEDIUM / LOW / INFO.",
            "Never treat missing evidence as a clean title.",
            "Recommend missing documents; multi-document vault; delete own files.",
            "Deterministic comparison (no LLM for MATCH/MISMATCH).",
            "Recalculate from stored OCR/translation/extraction; do not re-call Sarvam unless Analyze is clicked.",
            "Verification coverage percent is not the same as risk score.",
            "Versioned report PDF + JSON; new version if regenerated; never silently edit a finalized report.",
            "SHA-256 of canonical JSON; local GENESIS hash chain; integrity VALID or TAMPERED.",
            "401/403/404 ownership; pytest with Sarvam mocked.",
        ]
    )
    pdf.sub("3.3 Not implemented (do not invent these)")
    pdf.bullets(
        [
            "Public blockchain, Bitcoin, Ethereum, mining, wallets, smart contracts, cryptocurrency.",
            "Real payments / UPI / cards. Subscription page is UI only (Get Subscription).",
            "Real Google / X / phone OAuth (demo buttons only).",
            "Government portal scraping (Kaveri, Bhoomi, BBMP, etc.).",
            "Custom ML training, microservices, Kubernetes.",
            "Agricultural / Commercial / Industrial analysis (names kept; gated to subscription UI).",
            "Any claim that the property is legally clear or guaranteed safe.",
        ]
    )

    pdf.heading("4. Scope by phase")
    pdf.sub("Phase 1 - Foundation")
    pdf.body(
        "Landing, signup, login, JWT, dashboard, domain select, residential types, property case, document upload, protected routes, dark royal UI. "
        "Agricultural / Commercial / Industrial show Get Subscription (not Coming Soon and not homes-only). 13 tests in tests/test_phase1.py."
    )
    pdf.sub("Phase 2 - Real AI document analysis")
    pdf.body(
        "Sarvam digitise + translate + extract; classifier; merge extraction with source-text veto (AI cannot hide a stay/case if the text has it); "
        "evidence snippets; Python risk engine; recommendations; analysis UI. 7 tests in tests/test_phase2.py. Sarvam mocked in pytest."
    )
    pdf.sub("Phase 3 - Case-level due diligence")
    pdf.body(
        "Vault, multi-doc, delete, recalculate, MATCH/MISMATCH/NOT_AVAILABLE, coverage, risk score, finalize dialog, versioned reports, SHA-256, ledger, verify, PDF. "
        "tests/test_phase3.py. Last known combined pytest: 36 passed."
    )

    pdf.heading("5. Methodology")
    pdf.sub("5.1 Hybrid AI + rules")
    pdf.body(
        "Sarvam Document AI reads, OCRs, translates, and optionally extracts JSON. Python classifies (fallback), merges fields, decides risk, compares documents, scores, hashes, and writes the ledger. "
        "An LLM does not decide risk or MATCH/MISMATCH."
    )
    pdf.sub("5.2 Three-state verification (critical)")
    pdf.body(
        "DETECTED = explicit adverse evidence (stay, mismatch, incomplete names, unauthorized construction, uncleared mortgage). "
        "NO_ISSUE_FOUND = a relevant document explicitly clears it (example: EC says nil encumbrance). "
        "NOT_VERIFIED = not enough supporting papers. This is the default for absence. Wrong: No EC means no mortgage. Right: No EC means Mortgage NOT_VERIFIED."
    )
    pdf.sub("5.3 Evidence-first")
    pdf.body(
        "Findings cite source snippets. If seller/buyer names are missing but survey 45/3 exists, evidence still shows the survey snippet and notes that names were not found."
    )
    pdf.sub("5.4 Case vs document")
    pdf.body(
        "Document analysis is one file and may call Sarvam. Case recalculate uses all analyzed files, reuses stored text/JSON, merges risks, compares, and scores."
    )
    pdf.sub("5.5 Coverage vs risk")
    pdf.body(
        "Risk score: points only from DETECTED findings. HIGH=20, MEDIUM=10, LOW=5, cap 100. NOT_VERIFIED adds 0. "
        "Coverage: Verified=1.0 (DETECTED or NO_ISSUE_FOUND), Partial=0.5 (NOT_VERIFIED but a related paper was uploaded), Not Verified=0.0. Percent = round(100 * sum / 5). Coverage is not a safety guarantee."
    )
    pdf.sub("5.6 Tamper evidence")
    pdf.body(
        "Canonical JSON -> SHA-256 report_hash. Ledger hashes report_id, report_hash, previous_hash, timestamp. First previous_hash is GENESIS. Verify recomputes hashes; it does not blindly trust the stored hash. Chain is checked by report version, not timestamps, to avoid timezone false tamper."
    )
    pdf.sub("5.7 Testing")
    pdf.body("FastAPI TestClient, SQLite in-memory, StaticPool, mocked Sarvam. Live UI uses SARVAM_API_KEY in the project-root .env.")

    pdf.heading("6. Tech stack")
    pdf.sub("Backend")
    pdf.bullets(
        [
            "Python 3.11+ (development also ran 3.14.7).",
            "FastAPI, Uvicorn, SQLAlchemy 2 with UUID primary keys.",
            "PostgreSQL 16 via Docker Compose: database/user/password bhoomiscan, port 5432.",
            "Tests use SQLite in-memory.",
            "Pydantic v2, pydantic-settings, PyJWT HS256, bcrypt.",
            "python-multipart uploads; sarvamai SDK (digitise, status, results, download, translate).",
            "requests/httpx; fpdf2 PDFs; pytest.",
        ]
    )
    pdf.sub("Frontend")
    pdf.bullets(
        [
            "React 19, Vite 6, React Router 7, Tailwind 3, Framer Motion, Axios.",
            "localStorage key bhoomiscan.token.",
            "VITE_API_URL example http://localhost:8000. Analyze timeout 180 seconds.",
        ]
    )
    pdf.sub("Environment")
    pdf.body(
        "Root .env: DATABASE_URL, JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_MINUTES (1440), MAX_FILE_SIZE_MB (10), CORS_ORIGINS, SARVAM_API_KEY, poll 3s, max wait 120s. "
        "Never expose API key, JWT secret, password hashes, or filesystem paths to the frontend. Files live at storage/documents/{case_id}/. Single FastAPI process and single Vite app. No extra microservices."
    )

    pdf.heading("7. Architecture")
    pdf.body(
        "Browser SPA talks to FastAPI with Bearer JWT. Routers: auth, property cases and uploads, per-document analyze, recalculate/compare, finalize/hash/ledger/verify/PDF. "
        "PostgreSQL holds metadata, OCR text, extracted JSON, analyses, comparisons, reports, ledger. Disk holds original files. Sarvam is called only on Analyze, not on Recalculate."
    )
    pdf.body(
        "Layers: (1) UI royal theme and protected routes. (2) REST with ownership checks. (3) Domain services. (4) SQLAlchemy models. (5) Sarvam I/O. "
        "Split AI reading from deterministic rules so results are explainable and testable."
    )

    pdf.heading("8. User flow")
    pdf.body(
        "Landing -> Signup (username, password, confirm) -> Login (JWT) -> Dashboard/Home (Start Property Analysis + upgrade cards; no fake stats) -> Property domain. "
        "RESIDENTIAL continues. AGRICULTURAL / COMMERCIAL / INDUSTRIAL go to /subscription (Get Subscription). "
        "Residential types: vacant land, independent house, apartment/flat, villa, plot. Create property case. Document vault: upload, Analyze, recommended papers, Recalculate. "
        "Due diligence: overall risk, score /100, coverage %, five cards, evidence, MATCH/MISMATCH/NOT_AVAILABLE, unverified CTAs. "
        "Finalize dialog: Some checks may remain unverified. Missing documents do not block the report. "
        "Report: VALID/TAMPERED, SHA-256, record number, timestamp, Verify Integrity, Download PDF."
    )
    pdf.sub("Main demo (Kannada litigation sale deed)")
    pdf.bullets(
        [
            "Upload SaleDeed_01_Litigation_Kannada.pdf and Analyze. May classify as SALE_DEED or COURT_CASE_DOCUMENT if O.S. No. dominates keywords. Litigation DETECTED/HIGH (stay, pending O.S. 234/2019, transfer restriction). Mortgage and approval NOT_VERIFIED.",
            "Upload EC with explicit nil encumbrance, Analyze, Recalculate. Mortgage may become NO_ISSUE_FOUND.",
            "Upload Survey Sketch. Equal survey MATCH; different survey MISMATCH HIGH.",
            "Upload Building Approval with explicit approval. Approval may become NO_ISSUE_FOUND.",
            "Recalculate -> Finalize -> Verify VALID.",
        ]
    )

    pdf.heading("9. Data model")
    pdf.bullets(
        [
            "User: id, unique username, password_hash, timestamps.",
            "PropertyCase: user_id, domain, property_type, status ACTIVE.",
            "Document: filenames, file_path, mime, size, status UPLOADED/PROCESSING/ANALYZED/FAILED, document_type, confidence, language, original_text, translated_text, extracted_data JSON, processing_error.",
            "Analysis: case_id, document_id, COMPLETE/FAILED/PROCESSING, pipeline_steps, extracted_data.",
            "RiskFinding: category, status, risk_level, summary, finding_data JSON.",
            "EvidenceItem: document_id, type, page, source_text, extracted_field, confidence.",
            "Recommendation: category, document_type, reason.",
            "DocumentComparison: field, document A/B, values, MATCH/MISMATCH/NOT_AVAILABLE, severity, explanation.",
            "FinalReport: version, report_content JSON, report_hash, risk_score, risk_level, verification_coverage. Not silently edited; regenerate = new version.",
            "LedgerRecord: report_id unique, report_hash, previous_hash, record_hash, hashed_at ISO UTC.",
        ]
    )
    pdf.body("Startup: create_all plus ensure_schema adds Phase 2 columns on existing documents tables without dropping data.")

    pdf.heading("10. API endpoints")
    pdf.body("JWT required except signup, login, and health. Case/document/report routes check ownership (401/403/404).")
    pdf.kv(
        [
            ("POST /auth/signup", "201; 409 duplicate; 422 mismatch"),
            ("POST /auth/login", "Bearer access_token"),
            ("GET /auth/me", "Current user"),
            ("POST /property-cases", "Residential only; else 400 subscription"),
            ("GET /property-cases", "Own cases"),
            ("GET /property-cases/{id}", "403/404"),
            ("POST .../{id}/documents", "Upload"),
            ("GET .../{id}/documents", "List"),
            ("DELETE .../documents/{doc}", "Owner; delete file"),
            ("POST .../documents/{doc}/analyze", "Sarvam; long timeout"),
            ("GET .../documents/{doc}/analysis", "Latest document analysis"),
            ("GET .../{id}/analysis", "Latest analysis on the case"),
            ("GET .../{id}/recommendations", "From latest analysis"),
            ("GET .../{id}/evidence/{fid}", "Finding evidence"),
            ("POST .../{id}/recalculate", "All analyzed documents"),
            ("GET .../{id}/due-diligence", "Same as recalculate"),
            ("GET .../{id}/comparisons", "Stored comparisons"),
            ("POST .../{id}/finalize", "New report + ledger"),
            ("GET .../{id}/reports", "Version list"),
            ("GET .../reports/{rid}", "One report"),
            ("GET .../reports/{rid}/verify", "VALID or TAMPERED"),
            ("GET .../reports/{rid}/pdf", "Download PDF"),
            ("GET /health", "Public"),
        ]
    )
    pdf.body("The frontend must not send risk scores for the backend to trust. The backend always computes them.")

    pdf.heading("11. Frontend routes")
    pdf.body(
        "Public: / Landing, /login, /signup. Protected: /dashboard Home, /ai, /profile, /profile/settings, /contact, /subscription, /property-domain, /property-type, "
        "/property-case/:id/upload vault, /property-case/:caseId/documents/:documentId/analysis, /property-case/:id/due-diligence, /property-case/:id/reports/:reportId. "
        "Logged-in nav: Home, AI, profile, Sign Out. Stepper: Property kind, Home type, Document vault, Due diligence."
    )

    pdf.heading("12. Implementation algorithms")
    pdf.sub("12.1 Upload")
    pdf.body("Check extension, declared MIME, and magic bytes (%PDF, PNG, JPEG). Reject empty/too large files. Sanitize names. Never execute uploads.")
    pdf.sub("12.2 Analyze pipeline")
    pdf.bullets(
        [
            "Status PROCESSING.",
            "Sarvam digitise (Kannada); poll; read get_results page blocks; ZIP download fallback; strip NUL before PostgreSQL TEXT.",
            "If Kannada script, translate in 1800-character chunks to English.",
            "Keyword classifier on filename+text; confidence below 0.45 -> OTHER.",
            "Sarvam extract by schema; on failure use empty object.",
            "merge_extraction: regex fallback + AI; source veto for stay/case/restriction.",
            "evaluate_risks + build_recommendations; persist; ANALYZED or FAILED.",
        ]
    )
    pdf.body(
        "Extracted groups: property (survey, khata, area, village, hobli, taluk, district, state, type); ownership (seller, buyer, owner); "
        "transaction (sale amount, registration, previous deed); litigation; mortgage; approval; boundaries N/S/E/W."
    )
    pdf.sub("12.3 Risk engine")
    pdf.bullets(
        [
            "Ownership: missing seller/buyer -> DETECTED MEDIUM; identifiers without title-support docs -> NOT_VERIFIED; never auto-clear title.",
            "Litigation: pending/stay/restriction/case number/source hits -> DETECTED; explicit no pending litigation on verify-types -> NO_ISSUE_FOUND; else NOT_VERIFIED. Word-boundary lien so alienation is not a mortgage.",
            "Mortgage: charge without closure -> DETECTED; EC + nil/no/free from encumbrance -> NO_ISSUE_FOUND; else NOT_VERIFIED.",
            "Approval: unauthorized/deviation -> DETECTED; approval-type docs + present/OC -> NO_ISSUE_FOUND; a sale deed alone is not permission.",
            "Property record: identifiers still NOT_VERIFIED until cross-doc; mismatches on recalculate -> DETECTED.",
            "Case merge: DETECTED wins; else any NO_ISSUE_FOUND; else NOT_VERIFIED; then overlay MISMATCH.",
        ]
    )
    pdf.sub("12.4 Comparison")
    pdf.body(
        "Compare seller, buyer, owner, survey, khata, area, village, hobli, taluk, district, property type, four boundaries, registration number/date, previous deed number. "
        "Normalize whitespace, punctuation, prefixes (Survey No., Sy. No.). Names: collapse space and casefold; do not merge different names. "
        "Area to sq ft (sq m * 10.7639), 2% tolerance. Fewer than two documents with a value -> NOT_AVAILABLE. Else pairwise MATCH or MISMATCH with severity and explanation."
    )
    pdf.sub("12.5 Overall risk")
    pdf.body("HIGH if any DETECTED HIGH or score >= 40. MEDIUM if any DETECTED MEDIUM or score >= 10. Else LOW.")
    pdf.sub("12.6 Report, hash, ledger")
    pdf.body(
        "report_content includes property info, documents, risk summary, overall, coverage, detected issues, evidence, mismatches, unverified, recommendations, disclaimer. "
        "report_hash = SHA-256(canonical JSON with sorted keys). record_hash = SHA-256 of report_id, report_hash, previous_hash, timestamp. "
        "Verify: content hash matches; ledger material hash matches; previous is GENESIS or prior version record_hash."
    )
    pdf.sub("12.7 Recommendations")
    pdf.body(
        "If a category is DETECTED or NOT_VERIFIED, suggest missing types not already uploaded: parent deed, EC, khata, mutation, court order, bank NOC, building approval, survey sketch, and related papers."
    )

    pdf.heading("13. Legal language")
    pdf.body(
        "Allowed: Potential issue detected. Based on the documents provided. Could not be verified. Further verification is recommended. AI-assisted document review. "
        "Forbidden: Property is completely safe / legally clear / guaranteed clean. Do not say no litigation exists unless a proper document explicitly says so (then NO_ISSUE_FOUND, still not a court guarantee)."
    )
    pdf.body(
        "Disclaimer stored in reports: This report is an AI-assisted document review and is based only on the documents provided. "
        "It does not replace advice from a qualified lawyer, surveyor, government authority, or other professional."
    )

    pdf.heading("14. Security")
    pdf.bullets(
        [
            "Passwords hashed with bcrypt; never returned.",
            "JWT Authorization header; 401 without token; 403 other user's case.",
            "Non-residential case creation is gated; not a real payment.",
            "Upload type sniffing; strip NUL from OCR; CORS limited to Vite origins.",
            "Secrets only in server .env.",
        ]
    )

    pdf.heading("15. Tests")
    pdf.kv(
        [
            ("Phase 1", "test_phase1.py - signup/login/JWT, residential case, commercial 400, PDF upload, 403/404, reject txt"),
            ("Phase 2", "test_phase2.py - analyze auth, mocked Kannada deed, 403/404, litigation evidence, absence is not NO_ISSUE_FOUND, recommendations"),
            ("Phase 3", "test_phase3.py - multi-doc, MATCH/MISMATCH, recalculate, EC clears mortgage, coverage, score, finalize, hash, GENESIS, VALID, tamper TAMPERED, 403"),
            ("Frontend", "npm run build (Vite)"),
            ("Last known run", "36 passed"),
        ]
    )

    pdf.heading("16. Known limitations")
    pdf.bullets(
        [
            "Live OCR depends on Sarvam and scan quality.",
            "A litigation-heavy sale deed may classify as Court Case Document.",
            "Boundary OCR lines can concatenate (north absorbing south/east/west).",
            "Kannada party names may not extract; ownership DETECTED incomplete by design, not clear.",
            "Ledger is a local hash chain, not Ethereum.",
            "Subscription / Google / X / phone are UI demos. No live government fetch.",
            "Recalculate does not re-OCR. Local student deployment, not production-hardened.",
        ]
    )

    pdf.heading("17. Key source files")
    pdf.body(
        "Backend: app/main.py, config.py, constants.py, database.py, db_migrate.py, deps.py. "
        "Routers: auth, property_cases, analysis, reports. Models: user, property_case, document, analysis, report. "
        "Services: auth, storage, sarvam_service, document_classifier, extraction_service, evidence_service, risk_engine, recommendation_engine, analysis_service, comparison_service, scoring_service, case_analysis_service, hashing, ledger_service, report_service, report_pdf."
    )
    pdf.body(
        "Frontend pages: Landing, Login, Signup, Home, PropertyDomain, PropertyType, DocumentUpload (vault), DocumentAnalysis, DueDiligence, FinalReport, Subscription, Profile, AI, Contact. "
        "Also docs/Phase1_Test_Case_Report.pdf and Phase2_Test_Case_Report.pdf."
    )

    pdf.heading("18. Conclusion")
    pdf.body(
        "BhoomiScan is a complete local, explainable pipeline for residential due diligence: Indic Document AI to read Kannada papers, Python rules for risk and comparison, "
        "and a tamper-evident report without fake payments or a public blockchain."
    )
    pdf.body(
        "Academic points: (1) three-state verification so missing papers stay NOT_VERIFIED; (2) hybrid AI plus rules; (3) case-level comparison and coverage versus risk; "
        "(4) SHA-256 plus GENESIS hash chain with recomputed integrity. A buyer can go from signup to a versioned PDF with evidence and VALID/TAMPERED verification, while the system refuses to call an unverified property clear."
    )

    pdf.heading("19. Future work (not built)")
    pdf.bullets(
        [
            "Better party-name NER and user-confirmed document type.",
            "Government API integration (optional, if legally allowed).",
            "Real payments if a product is needed.",
            "Optional RFC 3161 timestamps; mobile app.",
        ]
    )

    pdf.heading("20. How to expand this PDF into a full report")
    pdf.body(
        "Another writer or AI can turn this into a 15-25 page report, a 12-15 slide PPT, or viva Q&A. Include introduction, problem, objectives, related work (manual due diligence vs this tool), methodology, architecture diagrams, module-wise implementation, algorithms, ER-style model, API table, screens (landing, vault, analysis, due diligence, VALID report), tests, limitations, future work, conclusion, and disclaimer. "
        "Do not invent live blockchain, live UPI, live OAuth, agricultural analysis, or legal certainty. Do not omit the NOT_VERIFIED rule, five categories, Sarvam vs Python split, GENESIS ledger, 36 tests, or Get Subscription gating for Agricultural, Commercial, and Industrial."
    )
    return pdf


def main():
    pdf = build()
    out = DOCS / "BhoomiScan_Complete_Project_Summary.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(out))
    data = out.read_bytes()
    copies = [
        DESKTOP / "BhoomiScan_Complete_Project_Summary.pdf",
        ONEDRIVE_DESKTOP / "BhoomiScan_Complete_Project_Summary.pdf",
    ]
    for dest in copies:
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            print(dest)
        except OSError as exc:
            print(f"skip {dest}: {exc}")
    print(out)


if __name__ == "__main__":
    main()
