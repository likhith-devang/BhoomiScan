"""Generate a downloadable BhoomiScan file-structure guide for viva."""

from pathlib import Path

from fpdf import FPDF
from fpdf.enums import XPos, YPos

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DESKTOP = Path.home() / "Desktop"
ONEDRIVE = Path.home() / "OneDrive" / "Desktop"


def ascii(text: str) -> str:
    return str(text or "").encode("latin-1", "replace").decode("latin-1")


class GuidePDF(FPDF):
    def __init__(self):
        super().__init__(format="A4")
        self.set_auto_page_break(auto=True, margin=18)
        self.set_left_margin(16)
        self.set_right_margin(16)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(90, 90, 90)
        self.cell(0, 8, f"BhoomiScan  |  File Structure Guide  |  Page {self.page_no()}", align="R")
        self.ln(4)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, "BhoomiScan - Your AIvocate.  Open this PDF in viva to find any file.", align="C")

    def cover(self):
        self.set_fill_color(11, 16, 32)
        self.rect(0, 0, 210, 88, "F")
        self.set_xy(16, 20)
        self.set_text_color(212, 175, 55)
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 7, "BHOOMISCAN  |  YOUR AIVOCATE.")
        self.ln(12)
        self.set_x(16)
        self.set_text_color(246, 241, 230)
        self.set_font("Helvetica", "B", 22)
        self.multi_cell(0, 10, "File Structure and File Guide")
        self.ln(2)
        self.set_x(16)
        self.set_font("Helvetica", "", 11)
        self.set_text_color(180, 190, 210)
        self.multi_cell(
            0,
            6,
            "Every project file, what it does, and which file to open when a teacher asks.\n"
            "16 September 2026  |  BhoomiScanV18",
        )
        self.ln(16)
        self.set_text_color(20, 20, 20)

    def heading(self, text: str):
        if self.get_y() + 22 > self.page_break_trigger:
            self.add_page()
        self.ln(3)
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(31, 79, 216)
        self.cell(0, 8, ascii(text), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(212, 175, 55)
        self.line(16, self.get_y(), 194, self.get_y())
        self.ln(4)
        self.set_text_color(20, 20, 20)

    def sub(self, text: str):
        if self.get_y() + 14 > self.page_break_trigger:
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
        self.ln(1.2)

    def file_row(self, path: str, meaning: str):
        if self.get_y() + 16 > self.page_break_trigger:
            self.add_page()
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(11, 16, 32)
        self.multi_cell(0, 4.8, ascii(path))
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 4.6, ascii(meaning))
        self.set_text_color(20, 20, 20)
        self.ln(1.4)

    def kv(self, rows: list[tuple[str, str]]):
        usable = self.w - self.l_margin - self.r_margin
        col1 = 62
        col2 = usable - col1
        for i, (k, v) in enumerate(rows):
            if self.get_y() + 10 > self.page_break_trigger:
                self.add_page()
            self.set_fill_color(245, 247, 252) if i % 2 == 0 else self.set_fill_color(255, 255, 255)
            self.set_x(self.l_margin)
            y = self.get_y()
            self.set_font("Helvetica", "B", 8)
            self.multi_cell(col1, 5.5, ascii(f"  {k}"), fill=True)
            h = self.get_y() - y
            self.set_xy(self.l_margin + col1, y)
            self.set_font("Helvetica", "", 8)
            self.multi_cell(col2, 5.5, ascii(v), fill=True)
            self.set_y(max(y + h, self.get_y()))
        self.ln(3)


def build() -> GuidePDF:
    pdf = GuidePDF()
    pdf.add_page()
    pdf.cover()

    pdf.heading("1. How to use this guide in viva")
    pdf.body(
        "When the teacher says 'show me X', use Section 2 first. Then open the file path in Cursor "
        "(Ctrl+P and type the file name). Do not open node_modules, .venv, or frontend/dist. Those are libraries and build output, not your code."
    )

    pdf.heading("2. Teacher asks... open this file")
    pdf.kv(
        [
            ("Login / JWT / signup", "backend/app/routers/auth.py  and  frontend/src/pages/Login.jsx"),
            ("Database tables", "backend/app/models/  (user, document, analysis, report)"),
            ("Upload PDF", "backend/app/services/storage.py  and  frontend/src/pages/DocumentUpload.jsx"),
            ("Sarvam AI / OCR", "backend/app/services/sarvam_service.py"),
            ("Analyze pipeline", "backend/app/services/analysis_service.py"),
            ("Litigation / risk", "backend/app/services/risk_engine.py"),
            ("Seller / buyer names", "backend/app/services/extraction_service.py"),
            ("Risk score 70", "backend/app/services/scoring_service.py  and  constants.py"),
            ("Blockchain / hash", "backend/app/services/hashing.py  and  ledger_service.py"),
            ("Show hash as a file", "storage/ledger/CHAIN.json"),
            ("VALID / TAMPERED", "backend/app/services/report_service.py"),
            ("Simple report screen", "frontend/src/pages/FinalReport.jsx"),
            ("API routes list", "backend/app/main.py  and  frontend/src/App.jsx"),
            ("Phase 1 tests", "backend/tests/test_phase1.py"),
            ("Phase 2 tests", "backend/tests/test_phase2.py"),
            ("Phase 3 tests", "backend/tests/test_phase3.py"),
            ("Navy / gold theme", "frontend/src/index.css  and  tailwind.config.js"),
            ("Env / API key", "root .env  (never commit)  and  .env.example"),
            ("Postgres Docker", "docker-compose.yml"),
        ]
    )

    pdf.heading("3. Folder tree (your code only)")
    pdf.body(
        "BhoomiScanV18/\n"
        "  README.md, .env, .env.example, docker-compose.yml, .gitignore\n"
        "  backend/                 FastAPI API (port 8000)\n"
        "    requirements.txt, .venv/\n"
        "    app/                   application code\n"
        "      main.py, config.py, constants.py, database.py, deps.py\n"
        "      models/              SQLAlchemy tables\n"
        "      schemas/             request/response shapes\n"
        "      routers/             HTTP endpoints\n"
        "      services/            business logic\n"
        "    tests/                 pytest Phase 1, 2, 3\n"
        "  frontend/                React + Vite (port 5173)\n"
        "    index.html, package.json, vite.config.js, tailwind.config.js\n"
        "    src/pages/             screens\n"
        "    src/components/        reusable UI\n"
        "    src/hooks/, services/, constants/\n"
        "  storage/documents/       uploaded PDFs on disk\n"
        "  storage/ledger/          CHAIN.json hash-chain files\n"
        "  docs/                    test reports and this guide"
    )
    pdf.body("Not listed below: backend/.venv, node_modules, frontend/dist, __pycache__. Those are generated.")

    pdf.heading("4. Root files")
    for path, meaning in [
        ("README.md", "How to start Postgres, backend, and frontend."),
        (".env", "Secrets on your PC: DATABASE_URL, JWT_SECRET, SARVAM_API_KEY. Do not put this in Git."),
        (".env.example", "Safe template of env names without real keys. Show this, not .env."),
        ("docker-compose.yml", "Starts PostgreSQL 16 as container bhoomiscan-db on port 5432."),
        (".gitignore", "Keeps .env, venv, node_modules, and uploaded files out of Git."),
    ]:
        pdf.file_row(path, meaning)

    pdf.heading("5. Backend core")
    for path, meaning in [
        ("backend/requirements.txt", "Python packages: FastAPI, SQLAlchemy, pytest, sarvamai, fpdf2, bcrypt."),
        ("backend/app/main.py", "App entry. Creates tables, mounts routers, health check GET /health."),
        ("backend/app/config.py", "Reads .env. Database URL, JWT, upload size, storage folder, Sarvam wait times."),
        ("backend/app/constants.py", "Enums: document types, risk statuses DETECTED/NOT_VERIFIED/NO_ISSUE_FOUND, score HIGH=70, GENESIS, disclaimer."),
        ("backend/app/database.py", "SQLAlchemy engine and get_db() session for Postgres (tests use SQLite)."),
        ("backend/app/deps.py", "get_current_user: reads Bearer JWT. Protects all case/report routes."),
        ("backend/app/db_migrate.py", "Adds new columns on startup so old Phase 1 rows keep working."),
        ("backend/app/__init__.py", "Marks app as a Python package."),
    ]:
        pdf.file_row(path, meaning)

    pdf.heading("6. Backend models (database tables)")
    pdf.body("Teacher: 'Where is data stored?' Open models, then say PostgreSQL database bhoomiscan.")
    for path, meaning in [
        ("backend/app/models/__init__.py", "Imports all models so tables are created together."),
        ("backend/app/models/user.py", "Table users: username, bcrypt password hash."),
        ("backend/app/models/property_case.py", "Table property_cases: one file per property (domain, type, owner)."),
        ("backend/app/models/document.py", "Table documents: filename, disk path, OCR text, extracted JSON, type."),
        ("backend/app/models/analysis.py", "Tables analyses, risk_findings, evidence, recommendations."),
        ("backend/app/models/report.py", "Tables document_comparisons, final_reports (JSON + SHA-256), ledger_records (previous_hash, record_hash)."),
    ]:
        pdf.file_row(path, meaning)

    pdf.heading("7. Backend schemas (API JSON shape)")
    for path, meaning in [
        ("backend/app/schemas/auth.py", "Signup/login request and token response."),
        ("backend/app/schemas/property_case.py", "Create-case body: domain and property type."),
        ("backend/app/schemas/document.py", "Upload metadata returned to the UI."),
        ("backend/app/schemas/analysis.py", "Analysis, findings, evidence JSON for the analysis page."),
        ("backend/app/schemas/report.py", "Recalculate payload, final report, integrity VALID/TAMPERED."),
        ("backend/app/schemas/__init__.py", "Package marker."),
    ]:
        pdf.file_row(path, meaning)

    pdf.heading("8. Backend routers (URLs)")
    for path, meaning in [
        ("backend/app/routers/__init__.py", "Package marker."),
        ("backend/app/routers/auth.py", "POST /auth/signup, /auth/login, GET /auth/me."),
        ("backend/app/routers/property_cases.py", "Create case, list cases, upload file, list/delete documents."),
        ("backend/app/routers/analysis.py", "POST analyze, GET analysis, recommendations, evidence."),
        ("backend/app/routers/reports.py", "Recalculate, due-diligence, finalize, list reports, verify, PDF download."),
    ]:
        pdf.file_row(path, meaning)

    pdf.heading("9. Backend services (logic)")
    pdf.body("Teacher: 'Where is the AI / risk / blockchain?' This folder. Routers call these; they do not talk to the UI directly.")
    for path, meaning in [
        ("backend/app/services/auth.py", "Hash password with bcrypt. Create and decode JWT."),
        ("backend/app/services/storage.py", "Save uploaded PDF/PNG/JPG under storage/documents/<case-id>/."),
        ("backend/app/services/sarvam_service.py", "Live Sarvam: digitise (OCR), translate Kannada to English, extract JSON. Tests mock this."),
        ("backend/app/services/document_classifier.py", "Guesses document type from keywords (sale deed vs court paper)."),
        ("backend/app/services/extraction_service.py", "Reads survey, seller, buyer, case number from text. Fixes Indian deed 'executed by' names."),
        ("backend/app/services/evidence_service.py", "Cuts source snippets around extracted values. Never hides missing names."),
        ("backend/app/services/risk_engine.py", "Five checks: ownership, litigation, mortgage, approval, property record. DETECTED / NOT_VERIFIED / NO_ISSUE_FOUND."),
        ("backend/app/services/recommendation_engine.py", "Suggests missing papers (EC, parent deed, plan approval)."),
        ("backend/app/services/analysis_service.py", "One-document pipeline: OCR -> translate -> classify -> extract -> risk -> save."),
        ("backend/app/services/comparison_service.py", "Compares fields across documents: MATCH / MISMATCH / NOT_AVAILABLE."),
        ("backend/app/services/scoring_service.py", "Risk score. DETECTED HIGH = 70 (litigation). Reasons list. Coverage math. NOT_VERIFIED adds 0."),
        ("backend/app/services/case_analysis_service.py", "Recalculate whole case from all analyzed papers. Merges findings."),
        ("backend/app/services/hashing.py", "Canonical JSON then SHA-256. Same content always same hash."),
        ("backend/app/services/ledger_service.py", "Local hash chain. First previous_hash = GENESIS. Writes CHAIN.json too."),
        ("backend/app/services/report_service.py", "Finalize: store report JSON, hash it, append ledger, verify VALID or TAMPERED."),
        ("backend/app/services/report_pdf.py", "Builds the downloadable risk-report PDF (score, because, hash)."),
        ("backend/app/services/__init__.py", "Package marker."),
    ]:
        pdf.file_row(path, meaning)

    pdf.heading("10. Backend tests")
    for path, meaning in [
        ("backend/tests/test_phase1.py", "13 tests: signup, login, JWT, residential case, upload, 401/403. No AI."),
        ("backend/tests/test_phase2.py", "7 tests: analyze auth, mocked Sarvam, litigation DETECTED, missing evidence is NOT_VERIFIED."),
        ("backend/tests/test_phase3.py", "19 tests: vault, MATCH/MISMATCH, score 70, GENESIS ledger, VALID, TAMPERED, names extraction."),
    ]:
        pdf.file_row(path, meaning)

    pdf.heading("11. Frontend config")
    for path, meaning in [
        ("frontend/package.json", "npm scripts: dev, build. React 19, Vite 6, Tailwind, Router, Axios, Framer Motion."),
        ("frontend/package-lock.json", "Exact library versions. Do not edit by hand."),
        ("frontend/vite.config.js", "Vite bundler. Dev server http://localhost:5173."),
        ("frontend/tailwind.config.js", "Colors: royal navy, gold, ivory, void."),
        ("frontend/postcss.config.js", "Required for Tailwind."),
        ("frontend/index.html", "HTML shell. Title: BhoomiScan."),
        ("frontend/.env.example", "VITE_API_URL=http://localhost:8000"),
        ("frontend/.env", "Local API URL for the browser. Only VITE_ names are exposed."),
        ("frontend/src/main.jsx", "React start: Router, AuthProvider, ToastProvider."),
        ("frontend/src/index.css", "Global dark theme, royal-frame cards, gold line."),
        ("frontend/src/App.jsx", "All routes. Protected pages need login."),
    ]:
        pdf.file_row(path, meaning)

    pdf.heading("12. Frontend pages (screens)")
    for path, meaning in [
        ("frontend/src/pages/Landing.jsx", "Public home. Your AIvocate. Get Started / Login."),
        ("frontend/src/pages/Signup.jsx", "Create username + password."),
        ("frontend/src/pages/Login.jsx", "JWT login. Demo Google/X/phone buttons are not real OAuth."),
        ("frontend/src/pages/Home.jsx", "Dashboard after login. Start analysis."),
        ("frontend/src/pages/Dashboard.jsx", "Older/alias dashboard pieces if used."),
        ("frontend/src/pages/PropertyDomain.jsx", "Residential vs Agricultural/Commercial/Industrial. Last three go to Get Subscription."),
        ("frontend/src/pages/PropertyType.jsx", "Villa, plot, independent house, etc."),
        ("frontend/src/pages/DocumentUpload.jsx", "Document vault. Upload, analyze, delete, Get risk report."),
        ("frontend/src/pages/DocumentAnalysis.jsx", "One-document AI result. Risk cards. Document text toggle (hidden by default)."),
        ("frontend/src/pages/DueDiligence.jsx", "Does not show the old complex page. Recalculates, finalizes, jumps to the simple report."),
        ("frontend/src/pages/FinalReport.jsx", "THE report: Risk score, Because reasons, VALID integrity, Download PDF."),
        ("frontend/src/pages/AI.jsx", "In-app chat page (demo helper, not Sarvam analysis)."),
        ("frontend/src/pages/Profile.jsx", "User profile."),
        ("frontend/src/pages/ProfileSettings.jsx", "Profile settings."),
        ("frontend/src/pages/Contact.jsx", "Contact Us."),
        ("frontend/src/pages/Subscription.jsx", "Get Subscription screen for non-residential domains."),
    ]:
        pdf.file_row(path, meaning)

    pdf.heading("13. Frontend components, hooks, services")
    for path, meaning in [
        ("frontend/src/components/AppHeader.jsx", "Top bar: logo, Home, AI, profile menu. Sign Out is only inside the menu."),
        ("frontend/src/components/Navbar.jsx", "Re-exports AppHeader."),
        ("frontend/src/components/Logo.jsx", "BhoomiScan globe + Your AIvocate."),
        ("frontend/src/components/PageShell.jsx", "Page layout with header and atmosphere."),
        ("frontend/src/components/Atmosphere.jsx", "Background glow."),
        ("frontend/src/components/Button.jsx", "Gold / ghost / primary buttons."),
        ("frontend/src/components/Input.jsx", "Form fields."),
        ("frontend/src/components/Card.jsx", "Generic card."),
        ("frontend/src/components/ErrorMessage.jsx", "Red error text."),
        ("frontend/src/components/LoadingSpinner.jsx", "Analyzing / signing-in spinner."),
        ("frontend/src/components/ProtectedRoute.jsx", "Redirects to /login if no token."),
        ("frontend/src/components/ProfilePill.jsx", "Name chip that opens the menu."),
        ("frontend/src/components/ProfileDropdown.jsx", "Profile, Settings, Contact, Subscription, Sign Out."),
        ("frontend/src/components/UploadBox.jsx", "Drag-and-drop file box."),
        ("frontend/src/components/DocumentCard.jsx", "One uploaded paper with Analyze / delete."),
        ("frontend/src/components/FlowStepper.jsx", "Steps: property kind, home type, vault, risk report."),
        ("frontend/src/components/AnalysisProgress.jsx", "Reading / extracting / checking steps."),
        ("frontend/src/components/RiskCategoryCard.jsx", "One of five risk tiles on analysis."),
        ("frontend/src/components/ExtractedDetails.jsx", "Survey, seller, buyer after analysis."),
        ("frontend/src/components/EvidencePanel.jsx", "Source snippets popup."),
        ("frontend/src/components/RecommendationList.jsx", "Upload EC / parent deed suggestions."),
        ("frontend/src/components/ComparisonTable.jsx", "MATCH/MISMATCH table (API still has it; simple report UI hides it)."),
        ("frontend/src/components/ConfirmDialog.jsx", "Yes/cancel dialog."),
        ("frontend/src/components/PropertyCard.jsx", "Domain card on dashboard flow."),
        ("frontend/src/components/PropertyTypeCard.jsx", "Home-type card."),
        ("frontend/src/components/PropertySummaryCard.jsx", "Dashboard property summary."),
        ("frontend/src/components/ActivityCard.jsx", "Recent activity tile."),
        ("frontend/src/components/SubscriptionCard.jsx", "Plan card."),
        ("frontend/src/components/UpgradeCard.jsx", "Upgrade prompt."),
        ("frontend/src/components/AIChat.jsx", "Chat UI."),
        ("frontend/src/components/DemoAuthButton.jsx", "Fake Google/X/phone control. Not real OAuth."),
        ("frontend/src/components/icons.jsx", "Small SVG icons."),
        ("frontend/src/hooks/useAuth.jsx", "Login state. Token in localStorage key bhoomiscan.token."),
        ("frontend/src/hooks/useToast.jsx", "Popup messages."),
        ("frontend/src/hooks/useSubscription.js", "Subscription flag for gated domains."),
        ("frontend/src/services/api.js", "Axios calls to FastAPI including analyze, finalize, verify, PDF."),
        ("frontend/src/services/auth.js", "Auth helper wrappers."),
        ("frontend/src/services/ai.js", "Chat helper."),
        ("frontend/src/constants/property.js", "Domains, property types, token key."),
        ("frontend/src/constants/analysis.js", "Risk labels for UI."),
        ("frontend/src/constants/subscription.js", "Subscription copy."),
        ("frontend/src/lib/userDisplay.js", "Display name initials."),
    ]:
        pdf.file_row(path, meaning)

    pdf.heading("14. Storage, ledger files, docs")
    for path, meaning in [
        ("storage/documents/<case-id>/", "Original uploaded PDFs. Show this for 'where are the papers stored?'"),
        ("storage/ledger/CHAIN.json", "Human-readable hash chain. previous_hash GENESIS then linked hashes. SHOW THIS for blockchain."),
        ("storage/ledger/report_v1.json", "One finalized report's hash, score, timestamp."),
        ("docs/generate_test_reports.py", "Builds Phase 1/2/3 test-case PDFs."),
        ("docs/generate_project_summary.py", "Builds the complete project summary PDF."),
        ("docs/generate_file_structure.py", "This guide's generator."),
        ("docs/Phase1_Test_Case_Report.pdf", "Phase 1 test report."),
        ("docs/Phase2_Test_Case_Report.pdf", "Phase 2 test report."),
        ("docs/Phase3_Test_Case_Report.pdf", "Phase 3 test report."),
        ("docs/BhoomiScan_Complete_Project_Summary.pdf", "Long written summary for report/PPT."),
    ]:
        pdf.file_row(path, meaning)

    pdf.heading("15. What to say in one sentence")
    pdf.body(
        "React UI talks to FastAPI. FastAPI stores users, papers, findings, and reports in PostgreSQL. "
        "Sarvam only runs on Analyze. Python decides risk. Finalize SHA-256 hashes the report and appends a local GENESIS ledger, "
        "also written to storage/ledger/CHAIN.json. The student UI is a simple score-and-reason report with VALID/TAMPERED integrity."
    )
    return pdf


def copy_to(src: Path, folder: Path, name: str) -> Path | None:
    try:
        folder.mkdir(parents=True, exist_ok=True)
        dest = folder / name
        dest.write_bytes(src.read_bytes())
        return dest
    except OSError:
        return None


def main():
    pdf = build()
    docs_path = DOCS / "BhoomiScan_File_Structure_Guide.pdf"
    docs_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(docs_path))
    name = "BhoomiScan_File_Structure_Guide.pdf"
    copies = [docs_path]
    for folder in (DESKTOP, ONEDRIVE):
        dest = copy_to(docs_path, folder, name)
        if dest:
            copies.append(dest)
    for item in copies:
        print(item)


if __name__ == "__main__":
    main()
