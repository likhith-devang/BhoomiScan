"""Generate a detailed academic project report PDF for BhoomiScan."""

from pathlib import Path

from fpdf import FPDF
from fpdf.enums import XPos, YPos

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DESKTOP = Path.home() / "Desktop"
ONEDRIVE_DESKTOP = Path.home() / "OneDrive" / "Desktop"


def ascii(text: str) -> str:
    return str(text or "").encode("latin-1", "replace").decode("latin-1")


class ReportPDF(FPDF):
    def __init__(self, toc_pages=None):
        super().__init__(format="A4")
        self.toc_pages = toc_pages or {}
        self.collected_pages = {}
        self.set_auto_page_break(auto=True, margin=18)
        self.set_left_margin(18)
        self.set_right_margin(18)

    def header(self):
        if self.page_no() <= 2:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(90, 90, 90)
        self.cell(0, 8, "BhoomiScan  |  Detailed Project Report  |  Page %s" % self.page_no(), align="R")
        self.ln(5)
        self.set_draw_color(212, 175, 55)
        self.set_line_width(0.3)
        self.line(18, self.get_y(), 192, self.get_y())
        self.ln(3)

    def footer(self):
        self.set_y(-14)
        self.set_draw_color(200, 200, 200)
        self.line(18, self.get_y(), 192, self.get_y())
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(
            0,
            8,
            "BhoomiScan - Your AIvocate.  Student project report. Not a legal opinion.",
            align="C",
        )

    def cover(self):
        self.set_fill_color(11, 16, 32)
        self.rect(0, 0, 210, 297, "F")
        self.set_fill_color(212, 175, 55)
        self.rect(0, 0, 8, 297, "F")
        self.set_xy(24, 28)
        self.set_text_color(212, 175, 55)
        self.set_font("Helvetica", "B", 11)
        self.cell(0, 7, "FINAL YEAR COLLEGE PROJECT REPORT")
        self.set_xy(24, 52)
        self.set_font("Helvetica", "B", 13)
        self.cell(0, 8, "BHOOMISCAN  |  YOUR AIVOCATE.")
        self.set_xy(24, 68)
        self.set_text_color(246, 241, 230)
        self.set_font("Helvetica", "B", 26)
        self.multi_cell(160, 11, "AI-Powered Property\nDue Diligence Platform")
        self.set_xy(24, 100)
        self.set_font("Helvetica", "", 12)
        self.set_text_color(180, 190, 210)
        self.multi_cell(
            160,
            6.2,
            "A detailed project report covering abstract, introduction, methodology, "
            "requirements, design, implementation, testing, results, conclusion, "
            "and references.",
        )
        self.set_xy(24, 148)
        self.set_text_color(212, 175, 55)
        self.set_font("Helvetica", "B", 11)
        self.cell(0, 7, "Submitted in partial fulfilment of the academic project")
        rows = [
            ("Product", "BhoomiScan - Your AIvocate."),
            ("Workspace", "BhoomiScanV18"),
            ("Version", "0.1.0"),
            ("Stack", "React 19, FastAPI, PostgreSQL 16, Sarvam Document AI"),
            ("Date", "September 2026"),
        ]
        y = 168
        for label, value in rows:
            self.set_xy(24, y)
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(212, 175, 55)
            self.cell(32, 7, label)
            self.set_font("Helvetica", "", 9)
            self.set_text_color(230, 230, 235)
            self.cell(0, 7, value)
            y += 8
        self.set_xy(24, 250)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(150, 160, 180)
        self.multi_cell(
            160,
            5,
            "Disclaimer: This system is an AI-assisted document review. It is not a lawyer, "
            "not a government portal, and not a legal guarantee of a clean title.",
        )

    def mark(self, title: str):
        self.collected_pages[title] = self.page_no()

    def chapter(self, number: str, title: str):
        self.add_page()
        full = "%s  %s" % (number, title)
        self.mark(full)
        self.set_fill_color(11, 16, 32)
        self.rect(18, self.get_y(), 174, 16, "F")
        self.set_xy(22, self.get_y() + 4)
        self.set_text_color(212, 175, 55)
        self.set_font("Helvetica", "B", 13)
        self.cell(0, 8, ascii(full))
        self.ln(16)
        self.set_text_color(20, 20, 20)

    def heading(self, text: str):
        needed = 20
        if self.get_y() + needed > self.page_break_trigger:
            self.add_page()
        self.ln(3)
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(31, 79, 216)
        self.multi_cell(0, 6.5, ascii(text))
        self.set_draw_color(212, 175, 55)
        self.set_line_width(0.35)
        y = self.get_y()
        self.line(18, y, 192, y)
        self.ln(3)
        self.set_text_color(20, 20, 20)

    def sub(self, text: str):
        if self.get_y() + 14 > self.page_break_trigger:
            self.add_page()
        self.ln(1)
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 10.5)
        self.set_text_color(11, 16, 32)
        self.multi_cell(0, 5.6, ascii(text))
        self.set_text_color(20, 20, 20)
        self.ln(0.8)

    def body(self, text: str):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.3, ascii(text))
        self.ln(1.4)

    def bullets(self, items: list[str]):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        for item in items:
            if self.get_y() + 10 > self.page_break_trigger:
                self.add_page()
            self.set_x(self.l_margin)
            self.multi_cell(0, 5.2, ascii("-  %s" % item))
        self.ln(1.4)

    def numbered(self, items: list[str]):
        self.set_font("Helvetica", "", 10)
        for i, item in enumerate(items, 1):
            if self.get_y() + 10 > self.page_break_trigger:
                self.add_page()
            self.set_x(self.l_margin)
            self.multi_cell(0, 5.2, ascii("%s.  %s" % (i, item)))
        self.ln(1.4)

    def kv(self, rows: list[tuple[str, str]]):
        usable = self.w - self.l_margin - self.r_margin
        col1 = 58
        col2 = usable - col1
        for i, (k, v) in enumerate(rows):
            if self.get_y() + 8 > self.page_break_trigger:
                self.add_page()
            self.set_fill_color(245, 247, 252) if i % 2 == 0 else self.set_fill_color(255, 255, 255)
            self.set_x(self.l_margin)
            self.set_font("Helvetica", "B", 8)
            self.cell(col1, 7, ascii("  %s" % k)[:44], fill=True, border=0)
            self.set_font("Helvetica", "", 8)
            self.cell(col2, 7, ascii(v)[:96], fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(3)

    def table(self, headers: list[str], rows: list[list[str]], widths: list[float] | None = None):
        usable = self.w - self.l_margin - self.r_margin
        if not widths:
            widths = [usable / len(headers)] * len(headers)
        if self.get_y() + 16 > self.page_break_trigger:
            self.add_page()
        self.set_x(self.l_margin)
        self.set_fill_color(11, 16, 32)
        self.set_text_color(246, 241, 230)
        self.set_font("Helvetica", "B", 8)
        for header, width in zip(headers, widths):
            self.cell(width, 7, ascii(header)[: int(width * 0.7)], fill=True, border=0)
        self.ln()
        self.set_text_color(30, 30, 30)
        self.set_font("Helvetica", "", 8)
        for i, row in enumerate(rows):
            if self.get_y() + 8 > self.page_break_trigger:
                self.add_page()
                self.set_x(self.l_margin)
                self.set_fill_color(11, 16, 32)
                self.set_text_color(246, 241, 230)
                self.set_font("Helvetica", "B", 8)
                for header, width in zip(headers, widths):
                    self.cell(width, 7, ascii(header)[: int(width * 0.7)], fill=True, border=0)
                self.ln()
                self.set_text_color(30, 30, 30)
                self.set_font("Helvetica", "", 8)
            self.set_fill_color(245, 247, 252) if i % 2 == 0 else self.set_fill_color(255, 255, 255)
            self.set_x(self.l_margin)
            for cell, width in zip(row, widths):
                self.cell(width, 6.5, ascii(cell)[: int(width * 0.85)], fill=True, border=0)
            self.ln()
        self.ln(3)

    def diagram(self, lines: list[str]):
        if self.get_y() + 8 + 4 * len(lines) > self.page_break_trigger:
            self.add_page()
        self.set_fill_color(247, 248, 252)
        self.set_x(self.l_margin)
        self.set_font("Courier", "", 7.2)
        self.set_text_color(20, 20, 20)
        for line in lines:
            if self.get_y() + 6 > self.page_break_trigger:
                self.add_page()
                self.set_font("Courier", "", 7.2)
            self.set_x(self.l_margin)
            self.cell(0, 4.1, ascii(line), fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(3)
        self.set_font("Helvetica", "", 10)

    def toc_line(self, title: str):
        page = self.toc_pages.get(title, "")
        if self.get_y() + 9 > self.page_break_trigger:
            self.add_page()
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 11)
        self.set_text_color(30, 30, 30)
        label = ascii(title)
        dots = "." * 90
        self.cell(150, 7, "%s  %s" % (label, dots[: max(4, 78 - len(label))]))
        self.cell(0, 7, str(page), align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def fill(pdf: ReportPDF) -> None:
    pdf.add_page()
    pdf.cover()

    pdf.add_page()
    pdf.mark("Table of Contents")
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(11, 16, 32)
    pdf.cell(0, 10, "Table of Contents", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_draw_color(212, 175, 55)
    pdf.line(18, pdf.get_y(), 192, pdf.get_y())
    pdf.ln(8)
    chapters = [
        "Chapter 1  Abstract",
        "Chapter 2  Introduction",
        "Chapter 3  Methodology and Proposed System",
        "Chapter 4  System Requirements Specification",
        "Chapter 5  System Design",
        "Chapter 6  Implementation",
        "Chapter 7  System Testing",
        "Chapter 8  Results",
        "Chapter 9  Conclusion and Future Enhancement",
        "Chapter 10  References",
    ]
    for title in chapters:
        pdf.toc_line(title)
    pdf.ln(8)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(90, 90, 90)
    pdf.multi_cell(
        0,
        5,
        ascii(
            "List of figures in this report includes architecture, data flow, entity "
            "relationships, and the analysis pipeline. Tables include requirements, "
            "API endpoints, risk rules, and test cases."
        ),
    )

    # ------------------------------------------------------------------ #
    pdf.chapter("Chapter 1", "Abstract")
    pdf.body(
        "Property purchase in India, especially in Karnataka, depends on a bundle of "
        "scanned papers: sale deeds, encumbrance certificates, khata extracts, survey "
        "sketches, building approvals, and court papers. Many of these documents are "
        "in Kannada, poorly scanned, and written in legal language that a first-time "
        "buyer cannot reliably interpret. Missing papers are often treated as the "
        "absence of a problem. Cross-document mismatches, such as a sale deed quoting "
        "survey number 45/3 while a survey sketch quotes 45/4, are easy to miss when "
        "files are checked one at a time. Commercial due-diligence services exist, "
        "but they are costly, often English-only, or overclaim that a property is "
        "legally clear."
    )
    pdf.body(
        "BhoomiScan (tagline: Your AIvocate.) is a student-scale full-stack web "
        "application that helps a buyer check residential property papers before "
        "purchase. A logged-in user creates a residential property case, uploads "
        "PDF or image files, and runs analysis. Sarvam Document AI performs optical "
        "character recognition and Kannada-to-English translation. A deterministic "
        "Python risk engine, not a large language model, then classifies documents, "
        "extracts structured fields, evaluates five risk categories, compares values "
        "across files, scores risk, and produces a versioned report. The report is "
        "hashed with SHA-256 and appended to a local GENESIS hash chain so later "
        "tampering can be detected."
    )
    pdf.body(
        "The academic contribution is a hybrid, explainable pipeline: Indic Document "
        "AI is used only to read text, while Python rules decide DETECTED, "
        "NO_ISSUE_FOUND, or NOT_VERIFIED. Absence of evidence is never treated as a "
        "clean title. The implemented system covers JWT authentication, document "
        "vault, analysis, case-level recalculation, comparison, coverage versus risk "
        "score, PDF export, and integrity verification. Automated pytest coverage "
        "comprises 39 cases across three phases, with Sarvam mocked so tests remain "
        "deterministic. The system does not scrape government portals, process live "
        "payments, train custom models, or claim legal certainty."
    )
    pdf.kv(
        [
            ("Title", "BhoomiScan - AI-Powered Property Due Diligence"),
            ("Domain", "Residential property document review"),
            ("Languages handled", "English and Kannada (OCR + translation)"),
            ("AI role", "Read and extract; Python decides risk"),
            ("Integrity", "SHA-256 + local GENESIS ledger"),
            ("Tests", "39 pytest cases (13 + 7 + 19)"),
        ]
    )

    # ------------------------------------------------------------------ #
    pdf.chapter("Chapter 2", "Introduction")
    pdf.heading("2.1 Overview")
    pdf.body(
        "Buying a home is one of the largest financial decisions a family makes. "
        "In the Indian registration and revenue system, title is reconstructed from "
        "documents rather than from a single conclusive online register that a buyer "
        "can trust without reading papers. BhoomiScan is a local web product that "
        "gives a buyer a structured first pass over those papers. It stores files "
        "in a case vault, reads them, highlights potential issues with evidence "
        "snippets, recommends missing documents, and writes a tamper-evident report."
    )
    pdf.body(
        "The product is intentionally modest in legal claims. Allowed language "
        "includes phrases such as Potential issue detected, Based on the documents "
        "provided, Could not be verified, and Further verification is recommended. "
        "Forbidden language includes Property is completely safe, legally clear, or "
        "guaranteed clean. The on-screen and stored disclaimer states that the "
        "report does not replace a qualified lawyer, surveyor, or government authority."
    )
    pdf.heading("2.2 Problem statement")
    pdf.body(
        "Buyers receive a folder of scans. Some pages are in Kannada. Some are "
        "photos of bound registers. Risk is distributed across five practical "
        "questions: who owns the property, whether a court case or stay exists, "
        "whether a bank charge is open, whether construction was approved, and "
        "whether survey, khata, area, and boundary details match across papers. "
        "Manual review is slow and inconsistent. Spreadsheet checklists do not "
        "OCR Kannada. Generic chatbots may invent a clean title when a document "
        "is silent. The problem addressed by this project is:"
    )
    pdf.body(
        "Can a student-scale full-stack system combine Indic Document AI with "
        "deterministic rules to present DETECTED / NOT_VERIFIED / NO_ISSUE_FOUND "
        "with evidence, without faking AI, payments, OAuth, or a public blockchain?"
    )
    pdf.heading("2.3 Motivation")
    pdf.bullets(
        [
            "Kannada sale deeds and court extracts are common in Karnataka residential deals.",
            "A missing encumbrance certificate must remain Mortgage NOT_VERIFIED, not a green tick.",
            "Survey mismatches between a deed and a sketch are a frequent source of later dispute.",
            "Students need an end-to-end artefact that is explainable in a viva: upload, OCR, rules, hash.",
            "Existing tools either stay fully manual or hide scoring inside an opaque LLM prompt.",
        ]
    )
    pdf.heading("2.4 Objectives")
    pdf.sub("2.4.1 Primary objective")
    pdf.body(
        "Build an end-to-end local web system: sign up and log in, create a "
        "residential case, upload documents, run AI analysis, recommend more "
        "papers, compare values, recalculate case-level risk, finalize a versioned "
        "report, hash it, write a local ledger, and verify integrity."
    )
    pdf.sub("2.4.2 Specific objectives")
    pdf.numbered(
        [
            "Provide username/password authentication with bcrypt hashes and JWT access tokens.",
            "Restrict live analysis to RESIDENTIAL property types; gate other domains to a subscription UI.",
            "Accept PDF, PNG, and JPEG uploads up to 10 MB with magic-byte validation.",
            "Call Sarvam Document AI to digitise pages and translate Kannada text in 1800-character chunks.",
            "Classify document type by keywords with a confidence floor of 0.45.",
            "Evaluate five risk categories using three statuses and four severity levels.",
            "Never treat missing evidence as NO_ISSUE_FOUND.",
            "Compare extracted fields across documents with MATCH / MISMATCH / NOT_AVAILABLE.",
            "Keep verification coverage percent independent of the numeric risk score.",
            "Store SHA-256 of canonical report JSON and chain records from GENESIS.",
            "Protect case ownership with 401, 403, and 404 responses.",
            "Cover the pipeline with pytest using an in-memory SQLite database and mocked Sarvam.",
        ]
    )
    pdf.sub("2.4.3 Non-objectives")
    pdf.bullets(
        [
            "Public blockchain, wallets, mining, smart contracts, or cryptocurrency.",
            "Live UPI, card, or subscription billing. Get Subscription is a user-interface placeholder.",
            "Real Google, X, or phone OAuth. Those buttons are demo-only.",
            "Scraping Kaveri, Bhoomi, BBMP, or other government portals.",
            "Custom machine-learning training, microservices, or Kubernetes.",
            "Agricultural, commercial, or industrial analysis engines.",
            "Any statement that the property is legally clear.",
        ]
    )
    pdf.heading("2.5 Scope")
    pdf.sub("Phase 1 - Foundation")
    pdf.body(
        "Landing page, signup, login, JWT, dashboard, property domain, residential "
        "types, property case, document upload, protected routes, and a dark royal "
        "user interface. Agricultural, commercial, and industrial domains show "
        "Get Subscription. Thirteen automated tests live in tests/test_phase1.py."
    )
    pdf.sub("Phase 2 - Document analysis")
    pdf.body(
        "Sarvam digitise, translate, and extract; classifier; merge extraction with "
        "a source-text veto so an AI JSON object cannot hide a stay order present "
        "in OCR text; evidence snippets; Python risk engine; recommendations; "
        "analysis screens. Seven tests live in tests/test_phase2.py."
    )
    pdf.sub("Phase 3 - Case-level due diligence")
    pdf.body(
        "Multi-document vault, delete, recalculate without re-calling Sarvam, "
        "comparison table, coverage, risk score, finalize dialog, versioned "
        "reports, SHA-256, ledger, verify, and PDF download. Nineteen tests live "
        "in tests/test_phase3.py."
    )
    pdf.heading("2.6 Organization of the report")
    pdf.body(
        "Chapter 1 states the abstract. Chapter 2 introduces the problem and "
        "objectives. Chapter 3 describes methodology and the proposed system. "
        "Chapter 4 records software requirements. Chapter 5 presents architecture "
        "and data design. Chapter 6 explains implementation. Chapter 7 documents "
        "testing. Chapter 8 reports results and observations. Chapter 9 concludes "
        "and lists future work. Chapter 10 lists references."
    )

    # ------------------------------------------------------------------ #
    pdf.chapter("Chapter 3", "Methodology and Proposed System")
    pdf.heading("3.1 Existing system")
    pdf.body(
        "Today a buyer, a family member, or a junior advocate reads papers page by "
        "page. Checklists may exist in Word or Excel. Translation of Kannada pages "
        "is informal. There is no automatic cross-check of survey numbers. There "
        "is no stored evidence trail that a later reader can verify. If a file is "
        "edited after a verbal all-clear, nothing in the folder proves what was "
        "reviewed. Paid opinion letters exist, but they are not a self-serve "
        "student tool and they do not expose a testable rule engine."
    )
    pdf.heading("3.2 Limitations of the existing approach")
    pdf.bullets(
        [
            "Language barrier: Kannada OCR and translation are not part of a typical checklist.",
            "Absence bias: no EC is read as no loan.",
            "No comparison: two files are not normalized and compared field by field.",
            "No integrity: a PDF can be swapped after a review.",
            "Opaque AI: a chatbot answer cannot be unit-tested as MATCH or MISMATCH.",
        ]
    )
    pdf.heading("3.3 Proposed system")
    pdf.body(
        "BhoomiScan is a browser single-page application talking to a FastAPI "
        "backend. PostgreSQL stores users, cases, document metadata, OCR text, "
        "extracted JSON, findings, comparisons, reports, and ledger rows. Original "
        "bytes stay on disk under storage/documents/{case_id}/. Sarvam is invoked "
        "only when the user clicks Analyze. Recalculate reuses stored text so the "
        "buyer can add an encumbrance certificate later without paying for OCR again."
    )
    pdf.heading("3.4 Hybrid AI plus rules")
    pdf.body(
        "Sarvam Document AI is treated as an input device. It digitises pages, "
        "optionally extracts a JSON object matching a declared schema, and "
        "translates Kannada. Python then classifies the document, merges AI fields "
        "with regular-expression fallbacks, applies a source-text veto for "
        "litigation language, evaluates risks, compares documents, scores, hashes, "
        "and writes the ledger. An LLM does not decide risk status or MATCH versus "
        "MISMATCH. This split is the core methodological choice: reading can be "
        "probabilistic; verdicts must be deterministic and testable."
    )
    pdf.heading("3.5 Three-state verification")
    pdf.body(
        "Each of the five categories receives exactly one status:"
    )
    pdf.bullets(
        [
            "DETECTED: explicit adverse evidence exists (stay order, pending case, incomplete names, unauthorized construction, uncleared mortgage, or a high-severity mismatch).",
            "NO_ISSUE_FOUND: a relevant document explicitly clears the category (for example an encumbrance certificate stating nil encumbrance).",
            "NOT_VERIFIED: supporting papers are missing or silent. This is the default. Wrong rule: no EC means no mortgage. Right rule: no EC means Mortgage NOT_VERIFIED.",
        ]
    )
    pdf.body(
        "This three-state model is more honest than a binary safe/unsafe flag. "
        "It forces the interface to show unverified work instead of a false green tick."
    )
    pdf.heading("3.6 Evidence-first findings")
    pdf.body(
        "A finding stores a summary plus evidence rows: source snippet, optional "
        "page, document type, extracted field, and confidence. If seller and buyer "
        "names are missing but survey 45/3 appears in the OCR, the ownership finding "
        "can still attach the survey snippet and state that names were not found. "
        "The user can open an evidence panel instead of trusting a score alone."
    )
    pdf.heading("3.7 Document analysis versus case recalculation")
    pdf.body(
        "Document analysis operates on one file and may call Sarvam. Case "
        "recalculation loads every analyzed file in the vault, merges category "
        "statuses with DETECTED winning over NO_ISSUE_FOUND winning over "
        "NOT_VERIFIED, overlays MISMATCH results, recomputes coverage and score, "
        "and refreshes recommendations. Recalculate does not re-OCR."
    )
    pdf.heading("3.8 Coverage versus risk score")
    pdf.body(
        "Two numbers are shown on due diligence so a high score is not confused "
        "with completeness, and a high coverage is not confused with safety."
    )
    pdf.bullets(
        [
            "Risk score: points only from DETECTED findings. HIGH adds 70, MEDIUM adds 15, LOW adds 10, cap 100. NOT_VERIFIED adds zero.",
            "Overall level: HIGH if any DETECTED HIGH or score >= 40; MEDIUM if any DETECTED MEDIUM or score >= 10; otherwise LOW.",
            "Coverage: Verified = 1.0 (DETECTED or NO_ISSUE_FOUND), Partially Verified = 0.5 (NOT_VERIFIED but a related paper was uploaded), Not Verified = 0.0. Percent = round(100 * sum / 5).",
        ]
    )
    pdf.heading("3.9 Tamper evidence")
    pdf.body(
        "When the user finalizes, the backend builds a canonical JSON object with "
        "sorted keys, computes report_hash = SHA-256(canonical JSON), and writes a "
        "ledger row. record_hash = SHA-256 of report_id, report_hash, previous_hash, "
        "and timestamp. The first previous_hash is the literal GENESIS. A later "
        "version links to the previous record_hash. Verify recomputes hashes; it "
        "does not blindly trust the stored value. Chain order uses report version, "
        "not wall-clock timestamps, to avoid false TAMPERED results from time zones."
    )
    pdf.heading("3.10 Development methodology")
    pdf.body(
        "Work was delivered in three incremental phases with automated tests at "
        "each gate. Phase 1 proved auth and upload. Phase 2 proved analysis with "
        "mocked OCR. Phase 3 proved comparison, scoring, and the ledger. This is "
        "iterative delivery with a stable REST contract rather than a single "
        "waterfall dump. Frontend and backend stay as one Vite app and one FastAPI "
        "process. No extra microservice was introduced."
    )
    pdf.heading("3.11 Proposed user journey")
    pdf.numbered(
        [
            "Landing -> Sign up with username and matching password -> Login (JWT stored in localStorage key bhoomiscan.token).",
            "Dashboard -> Start Property Analysis -> choose RESIDENTIAL -> choose vacant land, house, flat, villa, or plot.",
            "Create property case -> document vault -> upload PDF/PNG/JPG -> Analyze (up to 180 seconds).",
            "Review extracted fields, five risk cards, evidence, and recommended papers.",
            "Upload more files (EC, sketch, approval) -> Analyze each -> Recalculate.",
            "Due diligence shows overall risk, score /100, coverage %, MATCH/MISMATCH, unverified calls to action.",
            "Finalize with the warning that some checks may remain unverified. Missing documents do not block the report.",
            "Open report: VALID or TAMPERED, SHA-256, record number, Verify Integrity, Download PDF.",
        ]
    )

    # ------------------------------------------------------------------ #
    pdf.chapter("Chapter 4", "System Requirements Specification")
    pdf.heading("4.1 Product perspective")
    pdf.body(
        "BhoomiScan is a standalone local application. The browser talks to "
        "http://localhost:8000. The Vite development server serves "
        "http://localhost:5173. PostgreSQL listens on 5432 via Docker Compose "
        "(database, user, and password all set to bhoomiscan). Live OCR requires "
        "SARVAM_API_KEY in the project-root .env file. Secrets never ship to the "
        "React bundle; only VITE_API_URL is exposed to the frontend."
    )
    pdf.heading("4.2 Functional requirements")
    pdf.table(
        ["ID", "Requirement", "Priority"],
        [
            ["FR-01", "Sign up with unique username and matching passwords", "Must"],
            ["FR-02", "Login and return JWT; /auth/me for current user", "Must"],
            ["FR-03", "Create residential property case for the owner", "Must"],
            ["FR-04", "Reject non-residential case creation with 400", "Must"],
            ["FR-05", "Upload PDF/PNG/JPG; reject other types and oversize", "Must"],
            ["FR-06", "List and delete own documents", "Must"],
            ["FR-07", "Analyze: OCR, translate Kannada, extract, risk", "Must"],
            ["FR-08", "Show evidence snippets per finding", "Must"],
            ["FR-09", "Recommend missing document types", "Must"],
            ["FR-10", "Recalculate case using stored analyses", "Must"],
            ["FR-11", "Compare fields: MATCH / MISMATCH / NOT_AVAILABLE", "Must"],
            ["FR-12", "Compute coverage % and risk score separately", "Must"],
            ["FR-13", "Finalize versioned report; never silent-edit", "Must"],
            ["FR-14", "SHA-256 + GENESIS ledger; verify VALID/TAMPERED", "Must"],
            ["FR-15", "Download due-diligence PDF", "Must"],
            ["FR-16", "Ownership 401/403/404 on all case routes", "Must"],
            ["FR-17", "Subscription UI for non-residential domains", "Should"],
            ["FR-18", "Demo social login buttons (non-functional)", "Could"],
        ],
        [18, 118, 20],
    )
    pdf.heading("4.3 Non-functional requirements")
    pdf.table(
        ["ID", "Quality", "Specification"],
        [
            ["NFR-01", "Security", "bcrypt passwords; JWT HS256; CORS allow-list"],
            ["NFR-02", "Integrity", "NUL bytes stripped from OCR before PostgreSQL"],
            ["NFR-03", "Safety of files", "Uploads stored, never executed"],
            ["NFR-04", "Usability", "Simple English; dark navy, gold, ivory UI"],
            ["NFR-05", "Performance", "Analyze timeout 180s; Sarvam poll 3s, max 120s"],
            ["NFR-06", "Testability", "SQLite in-memory tests; Sarvam mocked"],
            ["NFR-07", "Maintainability", "Routers + services + SQLAlchemy models"],
            ["NFR-08", "Portability", "Windows/macOS/Linux with Docker Postgres"],
            ["NFR-09", "Legal tone", "Disclaimer on reports; no clear-title claim"],
            ["NFR-10", "Reliability", "Recalculate works if Sarvam is later down"],
        ],
        [18, 32, 106],
    )
    pdf.heading("4.4 Hardware requirements")
    pdf.kv(
        [
            ("Processor", "Any modern dual-core CPU suitable for Node and Python"),
            ("Memory", "8 GB RAM recommended (Docker + Node + Python)"),
            ("Disk", "About 2 GB for images, venv, node_modules, and uploads"),
            ("Display", "1280 x 720 or larger for the royal-themed SPA"),
            ("Network", "Internet required only for Sarvam OCR/translate"),
        ]
    )
    pdf.heading("4.5 Software requirements")
    pdf.kv(
        [
            ("OS", "Windows 10/11 (developed on Windows 10.0.26200)"),
            ("Python", "3.11+ (also ran on 3.14.7)"),
            ("Node.js", "18+ (development used 22.14.0)"),
            ("Database", "PostgreSQL 16 Alpine via Docker Compose"),
            ("Runtime DB URL", "postgresql+psycopg://bhoomiscan:bhoomiscan@localhost:5432/bhoomiscan"),
            ("Test DB", "SQLite in-memory with StaticPool"),
            ("Backend packages", "FastAPI, Uvicorn, SQLAlchemy 2, PyJWT, bcrypt, fpdf2, pytest"),
            ("AI SDK", "sarvamai plus requests for download URLs"),
            ("Frontend", "React 19, Vite 6, React Router 7, Tailwind 3, Axios, Framer Motion"),
        ]
    )
    pdf.heading("4.6 Actors and use cases")
    pdf.sub("Actors")
    pdf.bullets(
        [
            "Guest: sees landing, signup, and login.",
            "Authenticated buyer: owns cases, uploads, analyzes, finalizes.",
            "System / Sarvam: external OCR and translation provider.",
            "Database and disk: persist metadata and original files.",
        ]
    )
    pdf.sub("Primary use cases")
    pdf.table(
        ["Use case", "Actor", "Result"],
        [
            ["UC-01 Register", "Guest", "User row; password hash stored"],
            ["UC-02 Login", "Guest", "JWT for subsequent calls"],
            ["UC-03 Create case", "Buyer", "RESIDENTIAL case ACTIVE"],
            ["UC-04 Upload paper", "Buyer", "File on disk + documents row"],
            ["UC-05 Analyze", "Buyer + Sarvam", "OCR, risks, evidence"],
            ["UC-06 Recalculate", "Buyer", "Merged case view, no OCR"],
            ["UC-07 Finalize", "Buyer", "New report version + ledger"],
            ["UC-08 Verify", "Buyer", "VALID or TAMPERED"],
            ["UC-09 Download PDF", "Buyer", "fpdf2 risk report"],
            ["UC-10 Delete file", "Buyer", "Own document removed"],
        ],
        [40, 40, 76],
    )
    pdf.heading("4.7 External interface requirements")
    pdf.body(
        "Human interface: React pages at / , /login, /signup, /dashboard, "
        "/property-domain, /property-type, /property-case/:id/upload, analysis, "
        "due-diligence, and reports. Software interface: REST JSON with Authorization "
        "Bearer tokens. Communication: HTTP on loopback. Sarvam is reached with the "
        "official SDK using the server-side API key."
    )
    pdf.heading("4.8 Constraints, assumptions, and dependencies")
    pdf.bullets(
        [
            "Assumption: the buyer uploads genuine scans of the property they intend to buy.",
            "Assumption: Kannada Unicode in OCR is a sufficient language detector (8+ Kannada letters or more Kannada than Latin).",
            "Constraint: OCR quality depends on scan contrast and Sarvam availability.",
            "Constraint: only kn-IN and en-IN are first-class languages in the pipeline.",
            "Dependency: Docker engine must be running for PostgreSQL.",
            "Dependency: SARVAM_API_KEY for live Analyze; tests do not need it.",
            "Constraint: JWT_SECRET must remain on the server.",
        ]
    )
    pdf.heading("4.9 Allowed document types")
    pdf.body(
        "The classifier and recommendation engine know the following types: Sale Deed, "
        "Parent Deed, Encumbrance Certificate, Khata / Property Register, Mutation, "
        "Court Case Document, Court Order, Legal Notice, Seller Affidavit, Bank Mortgage "
        "Document, Loan Closure NOC, Release Deed, Bank NOC, Building Plan, Building Plan "
        "Approval, Commencement Certificate, Occupancy / Completion Certificate, Land "
        "Conversion, Survey Sketch, Property Tax Receipt, Site Layout Plan, and Other. "
        "Confidence below 0.45 maps to Other."
    )

    # ------------------------------------------------------------------ #
    pdf.chapter("Chapter 5", "System Design")
    pdf.heading("5.1 Architectural style")
    pdf.body(
        "The system is a layered client-server application. Layer 1 is the React "
        "SPA with protected routes and a royal visual theme. Layer 2 is REST "
        "routers with JWT and ownership checks. Layer 3 is domain services "
        "(auth, storage, Sarvam, classifier, extraction, risk, comparison, "
        "scoring, hashing, ledger, PDF). Layer 4 is SQLAlchemy models on "
        "PostgreSQL. Layer 5 is the Sarvam network I/O boundary. This split keeps "
        "AI reading away from rule decisions so both can be tested."
    )
    pdf.heading("5.2 System architecture")
    pdf.diagram(
        [
            "  +------------------+     JWT Bearer      +---------------------------+",
            "  |  React + Vite    | ------------------> |  FastAPI (Uvicorn :8000)  |",
            "  |  localhost:5173  | <------------------ |  auth / cases / analysis  |",
            "  +------------------+     JSON + PDF      |  reports / health         |",
            "                                           +-------------+-------------+",
            "                                                         |",
            "                    +----------------------+-------------+------------+",
            "                    |                      |                          |",
            "                    v                      v                          v",
            "           +----------------+    +------------------+      +------------------+",
            "           | PostgreSQL 16  |    | Disk storage     |      | Sarvam Document  |",
            "           | metadata, OCR, |    | documents/caseId |      | AI: digitise,    |",
            "           | JSON, ledger   |    | original bytes   |      | translate,extract|",
            "           +----------------+    +------------------+      +------------------+",
        ]
    )
    pdf.heading("5.3 Context (Level-0) data flow")
    pdf.body(
        "The buyer provides credentials and document files. BhoomiScan returns "
        "risk findings, recommendations, a score, coverage, and a hashed report. "
        "Sarvam receives file bytes during Analyze and returns text or JSON. "
        "PostgreSQL and disk are data stores, not external actors."
    )
    pdf.heading("5.4 Level-1 data flow")
    pdf.diagram(
        [
            "  [Buyer] --credentials--> (Auth) --JWT--> [Buyer]",
            "  [Buyer] --file bytes--> (Storage) --path--> (Analyze)",
            "  (Analyze) --bytes--> [Sarvam] --OCR/JSON--> (Analyze)",
            "  (Analyze) --text--> (Classifier / Extract / Risk / Evidence)",
            "  (Risk) --findings--> (Recommend)",
            "  [Buyer] --recalculate--> (Case merge + Compare + Score)",
            "  [Buyer] --finalize--> (Report JSON) --SHA-256--> (Ledger)",
            "  [Buyer] --verify--> (Hash recompute) --VALID/TAMPERED--> [Buyer]",
        ]
    )
    pdf.heading("5.5 Sequence: Analyze one document")
    pdf.numbered(
        [
            "Frontend POST /property-cases/{id}/documents/{doc}/analyze with JWT.",
            "Router loads the document, confirms the case belongs to the user, sets status PROCESSING.",
            "digitise_document sends bytes to Sarvam with language kn-IN, polls until completed, reads page blocks, falls back to ZIP download URL.",
            "looks_like_kannada inspects Unicode range U+0C80 to U+0CFF. If Kannada, translate_text chunks at 1800 characters to en-IN.",
            "classify_document scores filename plus working text against type keywords.",
            "extract_fields asks Sarvam for schema JSON; on failure uses {}.",
            "merge_extraction combines AI JSON, regex fallbacks, and source-text veto for stay/case/restriction.",
            "evaluate_risks and build_recommendations persist findings, evidence, and recommendations.",
            "Status ANALYZED or FAILED. Frontend polls or navigates to the analysis page.",
        ]
    )
    pdf.heading("5.6 Entity-relationship design")
    pdf.body(
        "UUID primary keys are used throughout. Cascades delete child rows when a "
        "case or analysis is removed. Document deletion sets comparison document "
        "foreign keys to NULL where needed."
    )
    pdf.table(
        ["Entity", "Key attributes", "Relates to"],
        [
            ["User", "id, username, password_hash", "1..* PropertyCase"],
            ["PropertyCase", "domain, property_type, status", "User, Documents, Analyses"],
            ["Document", "path, type, OCR, extracted JSON", "Case, Analyses"],
            ["Analysis", "status, pipeline_steps, JSON", "Case, Document, Findings"],
            ["RiskFinding", "category, status, level", "Analysis, Evidence"],
            ["EvidenceItem", "source_text, page, field", "Finding, Document"],
            ["Recommendation", "category, document_type", "Analysis"],
            ["DocumentComparison", "field, values, result", "Case, two Documents"],
            ["FinalReport", "version, hash, score", "Case, LedgerRecord"],
            ["LedgerRecord", "previous_hash, record_hash", "FinalReport (1:1)"],
        ],
        [40, 70, 46],
    )
    pdf.body(
        "Startup calls Base.metadata.create_all and ensure_schema so Phase 2 "
        "columns such as detected_language can be added on an existing documents "
        "table without dropping user data."
    )
    pdf.heading("5.7 Module design")
    pdf.sub("Backend routers")
    pdf.bullets(
        [
            "auth.py: signup, login, me.",
            "property_cases.py: cases, upload, list, delete.",
            "analysis.py: analyze, get analysis, recommendations, evidence, recalculate, due-diligence, comparisons.",
            "reports.py: finalize, list, get, verify, PDF.",
        ]
    )
    pdf.sub("Backend services")
    pdf.bullets(
        [
            "sarvam_service.py: live digitise, translate, extract.",
            "analysis_service.py: one-document pipeline.",
            "case_analysis_service.py: merge all analyzed files.",
            "risk_engine.py and recommendation_engine.py: category rules.",
            "comparison_service.py: normalized pairwise compare.",
            "scoring_service.py: points, overall level, coverage.",
            "hashing.py and ledger_service.py: SHA-256 chain.",
            "report_service.py and report_pdf.py: versioned JSON and PDF.",
            "storage.py: safe filenames and magic-byte checks.",
        ]
    )
    pdf.sub("Frontend pages")
    pdf.bullets(
        [
            "Public: Landing, Login, Signup.",
            "Protected: Home, AI helper chat (demo, not Sarvam), Profile, Settings, Contact, Subscription.",
            "Flow: PropertyDomain, PropertyType, DocumentUpload vault, DocumentAnalysis, DueDiligence, FinalReport.",
            "Shared: ProtectedRoute, FlowStepper, EvidencePanel, ComparisonTable, RiskCategoryCard.",
        ]
    )
    pdf.heading("5.8 User-interface design")
    pdf.body(
        "The visual language is dark navy backgrounds, gold accents, ivory type, "
        "and rounded cards. Motion uses Framer Motion page transitions. Copy is "
        "kept in simple English so a non-lawyer can follow the five checks. The "
        "stepper shows Property kind, Home type, Document vault, and Due diligence. "
        "Logged-in navigation shows Home, AI, profile, and Sign Out. Dashboard "
        "does not invent fake statistics."
    )
    pdf.heading("5.9 Security design")
    pdf.bullets(
        [
            "Passwords hashed with bcrypt; hashes never returned in JSON.",
            "Protected endpoints require Authorization: Bearer <token>; else 401.",
            "Another user's case or document returns 403; unknown id returns 404.",
            "Uploads checked by extension, declared MIME, and file signatures (%PDF, PNG, JPEG).",
            "CORS origins limited to http://localhost:5173 and http://127.0.0.1:5173.",
            "Frontend never computes a trusted risk score; the backend always recomputes.",
            "API keys remain in server .env only.",
        ]
    )
    pdf.heading("5.10 Report content design")
    pdf.body(
        "report_content JSON includes property info, document list, risk summary, "
        "overall level, coverage, detected issues, evidence, mismatches, unverified "
        "categories, recommendations, score reasons, and the legal disclaimer. A "
        "new finalize always increments version. Historical reports are immutable."
    )

    # ------------------------------------------------------------------ #
    pdf.chapter("Chapter 6", "Implementation")
    pdf.heading("6.1 Technology stack")
    pdf.body(
        "Python FastAPI was chosen for typed request models, automatic OpenAPI, "
        "and easy TestClient tests. SQLAlchemy 2 provides mapped models with UUID "
        "keys. React 19 with Vite gives a fast SPA. Tailwind expresses the royal "
        "theme without a heavy component library. fpdf2 writes Latin-1-safe PDFs. "
        "Docker Compose pins PostgreSQL 16 so classmates can start the database "
        "with one command."
    )
    pdf.heading("6.2 Environment and configuration")
    pdf.body(
        "Pydantic Settings reads the root .env: DATABASE_URL, JWT_SECRET, "
        "JWT_ALGORITHM (HS256), JWT_EXPIRE_MINUTES (1440), MAX_FILE_SIZE_MB (10), "
        "CORS_ORIGINS, SARVAM_API_KEY, SARVAM_POLL_SECONDS (3), "
        "SARVAM_MAX_WAIT_SECONDS (120). Frontend .env contains only VITE_API_URL."
    )
    pdf.heading("6.3 Authentication implementation")
    pdf.body(
        "Signup validates matching passwords and unique usernames (409 if taken). "
        "Login verifies bcrypt and returns access_token. deps.py decodes JWT and "
        "loads the user. Tokens expire after 24 hours by default. Google, X, and "
        "phone buttons are visual only."
    )
    pdf.heading("6.4 Property case and upload implementation")
    pdf.body(
        "POST /property-cases accepts domain and property_type. If domain is not "
        "RESIDENTIAL the API returns 400 directing the client to subscription. "
        "Allowed residential types are vacant land, independent house, apartment "
        "or flat, villa, and residential plot. Upload writes a sanitized filename "
        "under storage/documents/{property_case_id}/ and a documents row with "
        "status UPLOADED. Empty files and files over the limit are rejected."
    )
    pdf.heading("6.5 Sarvam integration")
    pdf.body(
        "sarvam_service.py constructs a SarvamAI client from the API key. Digitise "
        "submits (filename, bytes, mime), polls get_status until a terminal status "
        "in {completed, partially_completed, failed, rejected}, then prefers "
        "get_results page content and blocks. If results are empty it downloads a "
        "URL which may be a ZIP of markdown or HTML. Translate uses "
        "sarvam-translate:v1 from kn-IN to en-IN. Extract sends EXTRACTION_SCHEMA "
        "as JSON. Any extract failure is swallowed into {} so regex fallback can "
        "still run. Missing API key raises a clear SarvamError."
    )
    pdf.heading("6.6 Extraction schema and merge")
    pdf.body(
        "The schema groups property identifiers (survey, khata, area, village, "
        "hobli, taluk, district, state, type), ownership names, transaction "
        "amounts and registration numbers, litigation flags, mortgage flags, "
        "approval flags, and four boundaries. merge_extraction fills blanks from "
        "regular expressions on working text and original text. A source-text veto "
        "reasserts stay, pending case, or transfer restriction if those words exist "
        "even when the AI JSON omitted them. That rule is essential: the model "
        "must not be allowed to hide a court stay."
    )
    pdf.heading("6.7 Classification")
    pdf.body(
        "document_classifier.py scores known phrases in filename and text. A "
        "litigation-heavy sale deed that repeats O.S. No. may classify as Court "
        "Case Document; that is a known limitation, not a crash. looks_like_kannada "
        "counts Kannada versus Latin letters."
    )
    pdf.heading("6.8 Risk engine")
    pdf.sub("Ownership / Title")
    pdf.body(
        "Missing seller or buyer names produce DETECTED at MEDIUM. Identifiers "
        "without supporting title documents remain NOT_VERIFIED. Title is never "
        "auto-cleared from a survey number alone."
    )
    pdf.sub("Litigation")
    pdf.body(
        "Pending case, stay, restriction, or a case number in source text produces "
        "DETECTED, typically HIGH. Explicit no pending litigation on a verifying "
        "document type may become NO_ISSUE_FOUND. Otherwise NOT_VERIFIED. The word "
        "lien is matched on word boundaries so alienation is not treated as a mortgage."
    )
    pdf.sub("Mortgage / Encumbrance")
    pdf.body(
        "An open charge without closure is DETECTED. An encumbrance certificate "
        "with nil / no / free from encumbrance can become NO_ISSUE_FOUND after "
        "recalculate. Silence remains NOT_VERIFIED."
    )
    pdf.sub("Approval / Construction")
    pdf.body(
        "Unauthorized construction or deviation is DETECTED. Approval-type documents "
        "plus present or occupancy certificate can become NO_ISSUE_FOUND. A sale "
        "deed alone is not building permission."
    )
    pdf.sub("Property record / Boundary")
    pdf.body(
        "Identifiers stay NOT_VERIFIED until cross-document comparison. A survey "
        "or boundary MISMATCH overlays DETECTED at HIGH or MEDIUM depending on field."
    )
    pdf.sub("Case merge")
    pdf.body(
        "When several documents speak, DETECTED wins. Else any NO_ISSUE_FOUND is "
        "kept. Else NOT_VERIFIED. Mismatches then overlay the merged set."
    )
    pdf.heading("6.9 Comparison algorithm")
    pdf.body(
        "comparison_service.py compares seller, buyer, owner, survey, khata, area, "
        "village, hobli, taluk, district, property type, north/south/east/west, "
        "registration number and date, and previous deed number. Normalization "
        "strips extra whitespace, punctuation, and prefixes such as Survey No. and "
        "Sy. No. Person names collapse spaces and case; different names are not "
        "merged. Area converts to square feet (square metres * 10.7639) with 2% "
        "tolerance. If fewer than two documents carry a value the result is "
        "NOT_AVAILABLE. Otherwise pairwise MATCH or MISMATCH with severity and a "
        "plain-language explanation."
    )
    pdf.heading("6.10 Scoring implementation")
    pdf.body(
        "scoring_service.py sums RISK_SCORE_POINTS only for DETECTED rows and caps "
        "at 100. score_reasons attach category labels for the Because section of "
        "the PDF. verification_coverage walks the five categories and related "
        "uploaded types from the recommendation map so Partial credit is possible "
        "when a related paper exists but the category is still NOT_VERIFIED."
    )
    pdf.heading("6.11 Report, hash, and ledger implementation")
    pdf.body(
        "finalize creates FinalReport with an incremented version, stores "
        "report_content, computes report_hash, and inserts LedgerRecord. Verify "
        "recomputes the content hash, recomputes the ledger material hash, and "
        "checks that previous_hash is GENESIS or the prior version's record_hash. "
        "A modified JSON yields TAMPERED. PDF export uses fpdf2 with the same "
        "disclaimer footer used in this academic report's spirit: not a legal guarantee."
    )
    pdf.heading("6.12 Frontend implementation notes")
    pdf.body(
        "Axios in services/api.js attaches the JWT and uses a long timeout for "
        "analyze. ProtectedRoute redirects guests to login. ConfirmDialog warns "
        "before finalize. AnalysisProgress lists uploaded, reading, extracting, "
        "checking, and complete. The in-app AI page is a demo helper chatbot, not "
        "the Sarvam analysis path, and must not be confused with document OCR."
    )
    pdf.heading("6.13 API catalogue")
    pdf.table(
        ["Method", "Path", "Auth"],
        [
            ["POST", "/auth/signup", "No"],
            ["POST", "/auth/login", "No"],
            ["GET", "/auth/me", "JWT"],
            ["POST", "/property-cases", "JWT"],
            ["GET", "/property-cases", "JWT"],
            ["GET", "/property-cases/{id}", "JWT"],
            ["POST", "/property-cases/{id}/documents", "JWT"],
            ["GET", "/property-cases/{id}/documents", "JWT"],
            ["DELETE", ".../documents/{doc}", "JWT"],
            ["POST", ".../documents/{doc}/analyze", "JWT"],
            ["GET", ".../documents/{doc}/analysis", "JWT"],
            ["GET", "/property-cases/{id}/analysis", "JWT"],
            ["GET", ".../{id}/recommendations", "JWT"],
            ["GET", ".../{id}/evidence/{fid}", "JWT"],
            ["POST", ".../{id}/recalculate", "JWT"],
            ["GET", ".../{id}/due-diligence", "JWT"],
            ["GET", ".../{id}/comparisons", "JWT"],
            ["POST", ".../{id}/finalize", "JWT"],
            ["GET", ".../{id}/reports", "JWT"],
            ["GET", ".../reports/{rid}", "JWT"],
            ["GET", ".../reports/{rid}/verify", "JWT"],
            ["GET", ".../reports/{rid}/pdf", "JWT"],
            ["GET", "/health", "No"],
        ],
        [22, 108, 26],
    )
    pdf.heading("6.14 How to run the implementation")
    pdf.body(
        "Start Docker Desktop, then from the project root run docker compose up -d. "
        "In backend, activate .venv and run python -m uvicorn app.main:app --reload "
        "--host 127.0.0.1 --port 8000. In frontend run npm run dev. Open "
        "http://localhost:5173. Health check: GET http://127.0.0.1:8000/health."
    )

    # ------------------------------------------------------------------ #
    pdf.chapter("Chapter 7", "System Testing")
    pdf.heading("7.1 Test strategy")
    pdf.body(
        "Testing follows the same three phases as delivery. Automated tests use "
        "pytest and FastAPI TestClient. Each test gets an isolated SQLite "
        "in-memory database. Sarvam HTTP calls are monkeypatched so CI and laptops "
        "without an API key still pass. Live UI testing of OCR requires "
        "SARVAM_API_KEY and a real Kannada PDF. Frontend production bundling is "
        "checked with npm run build."
    )
    pdf.heading("7.2 Test environment")
    pdf.kv(
        [
            ("Harness", "pytest + FastAPI TestClient"),
            ("Automated DB", "SQLite in-memory, StaticPool"),
            ("Runtime DB", "PostgreSQL 16 Docker"),
            ("AI in pytest", "Mocked digitise / translate / extract"),
            ("AI in UI", "Live Sarvam when key is set"),
            ("Suites", "test_phase1.py, test_phase2.py, test_phase3.py"),
            ("Count", "13 + 7 + 19 = 39 test functions"),
        ]
    )
    pdf.heading("7.3 Phase 1 test cases (foundation)")
    pdf.table(
        ["ID", "Function", "Expected"],
        [
            ["TC-01", "test_signup_success", "201; username returned; no password"],
            ["TC-02", "test_duplicate_signup", "409 Username already exists"],
            ["TC-03", "test_signup_password_mismatch", "422 passwords must match"],
            ["TC-04", "test_login_success", "JWT access_token"],
            ["TC-05", "test_invalid_login", "401 invalid credentials"],
            ["TC-06", "test_protected_endpoint_requires_auth", "401 without token"],
            ["TC-07", "test_protected_endpoint_with_token", "200 with token"],
            ["TC-08", "test_property_case_creation", "Residential case created"],
            ["TC-09", "test_property_case_rejects_non_residential", "400"],
            ["TC-10", "test_document_upload", "PDF stored; metadata saved"],
            ["TC-11", "test_unauthorized_case_access", "403 other user's case"],
            ["TC-12", "test_missing_property_case", "404"],
            ["TC-13", "test_unsupported_file", "Reject .txt"],
        ],
        [18, 92, 46],
    )
    pdf.heading("7.4 Phase 2 test cases (analysis)")
    pdf.table(
        ["ID", "Function", "Expected"],
        [
            ["TC-14", "test_analyze_requires_authentication", "401"],
            ["TC-15", "test_analyze_uploaded_pdf", "Mocked OCR pipeline completes"],
            ["TC-16", "test_user_cannot_analyze_another_users_document", "403"],
            ["TC-17", "test_missing_document_returns_404", "404"],
            ["TC-18", "test_litigation_detected_from_explicit_evidence", "DETECTED"],
            ["TC-19", "test_empty_evidence_does_not_produce_no_issue_found", "NOT_VERIFIED"],
            ["TC-20", "test_recommendation_engine_returns_missing_documents", "Suggestions"],
        ],
        [18, 100, 38],
    )
    pdf.body(
        "TC-19 is the academic linchpin: empty evidence must not collapse into "
        "NO_ISSUE_FOUND. That encodes the ethical rule that silence is not safety."
    )
    pdf.heading("7.5 Phase 3 test cases (case-level diligence)")
    pdf.table(
        ["ID", "Focus", "Expected"],
        [
            ["TC-21", "Party names from executed-by deed", "Names extracted"],
            ["TC-22", "Kannada sale-deed name extraction", "Fallback still works"],
            ["TC-23", "Incomplete ownership evidence", "Snippet attached"],
            ["TC-24", "Indian sale-deed name patterns", "Seller/buyer found"],
            ["TC-25", "Survey prefix normalization", "Sy. No. matches Survey No."],
            ["TC-26", "Multiple documents one case", "Shared case id"],
            ["TC-27", "Equal survey numbers", "MATCH"],
            ["TC-28", "Different survey numbers", "MISMATCH HIGH"],
            ["TC-29", "Different areas", "MISMATCH"],
            ["TC-30", "Recalculate uses all files", "Merged findings"],
            ["TC-31", "EC nil encumbrance", "Mortgage NO_ISSUE_FOUND"],
            ["TC-32", "Missing evidence", "Stays NOT_VERIFIED"],
            ["TC-33", "Coverage percent", "Formula applied"],
            ["TC-34", "Risk score deterministic", "DETECTED points only"],
            ["TC-35", "Finalize hash and ledger", "GENESIS then record_hash"],
            ["TC-36", "Second report previous_hash", "Links to prior record"],
            ["TC-37", "Untouched report verify", "VALID"],
            ["TC-38", "Modified report verify", "TAMPERED"],
            ["TC-39", "Unauthorized report access", "403"],
        ],
        [18, 78, 60],
    )
    pdf.heading("7.6 Manual test plan")
    pdf.numbered(
        [
            "Landing -> Get Started -> sign up -> login -> dashboard.",
            "Choose Residential -> Independent House -> create case.",
            "Upload a PDF; confirm it appears as stored, not analyzed yet.",
            "With SARVAM_API_KEY, Analyze a Kannada litigation sale deed. Expect Litigation DETECTED/HIGH; mortgage and approval NOT_VERIFIED.",
            "Upload an EC that explicitly says nil encumbrance, Analyze, Recalculate. Mortgage may become NO_ISSUE_FOUND.",
            "Upload a survey sketch with a different survey number. Expect MISMATCH HIGH.",
            "Finalize. Confirm warning that unverified checks remain. Download PDF. Click Verify Integrity: VALID.",
            "Attempt another user's URL: 403. Open /health without auth: ok.",
        ]
    )
    pdf.heading("7.7 Tools and re-run commands")
    pdf.body(
        "From backend with the virtual environment active: pytest -q. To run one "
        "phase: pytest tests/test_phase1.py -v. Frontend: npm run build. These "
        "commands do not call the live Sarvam API."
    )

    # ------------------------------------------------------------------ #
    pdf.chapter("Chapter 8", "Results")
    pdf.heading("8.1 Delivered system")
    pdf.body(
        "The implemented product is a working local application. A buyer can move "
        "from a public landing page to a hashed PDF without leaving the browser, "
        "provided Docker, the API, the Vite server, and (for live OCR) Sarvam are "
        "available. The royal-themed interface presents five checks in plain "
        "English: who owns it, court cases, bank loans, permissions, and land records."
    )
    pdf.heading("8.2 Functional results")
    pdf.table(
        ["Area", "Result observed"],
        [
            ["Authentication", "Unique users, JWT session, protected routes"],
            ["Residential gating", "Non-residential create blocked; subscription UI shown"],
            ["Upload safety", "PDF/PNG/JPEG accepted; txt rejected"],
            ["Kannada path", "OCR language kn-IN; translate when Kannada detected"],
            ["English path", "Translation skipped when no Kannada letters"],
            ["Litigation demo", "Stay / O.S. language yields DETECTED HIGH"],
            ["Absence rule", "No EC keeps Mortgage NOT_VERIFIED"],
            ["EC clearing", "Explicit nil encumbrance can clear mortgage"],
            ["Survey MATCH", "Normalized prefixes compare equal"],
            ["Survey MISMATCH", "45/3 vs 45/4 becomes HIGH mismatch"],
            ["Coverage vs score", "Independent meters on due-diligence page"],
            ["Integrity", "Unchanged report VALID; edited JSON TAMPERED"],
            ["Ownership", "Cross-user access denied"],
        ],
        [44, 112],
    )
    pdf.heading("8.3 Representative walkthrough")
    pdf.body(
        "Upload SaleDeed_01_Litigation_Kannada.pdf and Analyze. The pipeline may "
        "classify the file as SALE_DEED or COURT_CASE_DOCUMENT if case numbers "
        "dominate keywords. Litigation is DETECTED at HIGH when stay, pending "
        "O.S. 234/2019, or transfer restriction appears. Mortgage and approval "
        "remain NOT_VERIFIED. Adding an EC with explicit nil encumbrance and "
        "recalculating can move mortgage to NO_ISSUE_FOUND. Adding a survey sketch "
        "with the same survey produces MATCH; a different survey produces MISMATCH. "
        "Finalize then Verify yields VALID for an untouched report."
    )
    pdf.heading("8.4 Scoring example")
    pdf.body(
        "A single DETECTED HIGH finding contributes 70 points and forces overall "
        "HIGH. Two DETECTED MEDIUM findings contribute 30 points and overall "
        "MEDIUM unless a HIGH is also present. A case that is entirely "
        "NOT_VERIFIED has score 0 and overall LOW, while coverage may still be "
        "0% or 50% depending on whether related papers were uploaded. This result "
        "is deliberate: an empty vault is not a safe property; it is an incomplete file."
    )
    pdf.heading("8.5 User-interface results")
    pdf.bullets(
        [
            "Landing states Your AIvocate. and lists the five checks.",
            "Vault lists files with Analyze actions and recommended papers.",
            "Analysis page shows pipeline steps, extracted groups, and evidence.",
            "Due diligence shows five category cards, comparison table, and unverified CTAs.",
            "Final report shows hash, ledger record, VALID/TAMPERED, and PDF download.",
        ]
    )
    pdf.heading("8.6 Test results")
    pdf.body(
        "The repository contains 39 automated test functions. Phase 1 and Phase 2 "
        "were previously recorded as 20/20 passing in the Phase 1-2 test-case "
        "report. Phase 3 extends coverage to comparison, scoring, hashing, and "
        "tamper detection. Pytest does not bill Sarvam. A live Kannada PDF once "
        "failed when the OCR download was a ZIP; sarvam_service.py now unpacks ZIP "
        "payloads, which is a concrete result of testing against the real API."
    )
    pdf.heading("8.7 Limitations observed")
    pdf.bullets(
        [
            "Live OCR depends on scan quality and Sarvam uptime.",
            "A litigation-heavy sale deed may classify as Court Case Document.",
            "Boundary OCR lines can concatenate (north absorbing south/east/west).",
            "Kannada party names may fail extraction; incomplete ownership stays DETECTED, not cleared.",
            "OCR is requested as Kannada, so Hindi or Tamil pages are not first-class.",
            "The ledger is a local hash chain, not Ethereum or a public timestamp authority.",
            "Subscription and social login are UI demonstrations.",
            "Recalculate never re-OCRs; a bad first digitise must be re-run via Analyze.",
            "Deployment is local-student grade, not production-hardened.",
        ]
    )
    pdf.heading("8.8 Discussion")
    pdf.body(
        "The main result is not a higher machine-learning F1 score. The main result "
        "is an honest interface: missing papers stay visible, evidence is quoted, "
        "and a hash can prove whether the JSON still matches what was finalized. "
        "Splitting Sarvam from Python made the viva story simple: AI reads, rules "
        "decide, tests freeze the rules. That is a stronger academic artefact than "
        "an untestable prompt that declares a title clear."
    )

    # ------------------------------------------------------------------ #
    pdf.chapter("Chapter 9", "Conclusion and Future Enhancement")
    pdf.heading("9.1 Conclusion")
    pdf.body(
        "This project designed and implemented BhoomiScan, an AI-assisted "
        "residential property due-diligence web application. It addresses a real "
        "buyer problem: scanned Kannada and English papers that hide ownership, "
        "litigation, mortgage, approval, and survey issues. The proposed hybrid "
        "method uses Sarvam Document AI only to digitise, translate, and extract, "
        "while a deterministic Python engine classifies, vetoes hidden litigation "
        "language, scores five categories with three honest states, compares "
        "documents, and seals a versioned report with SHA-256 and a GENESIS ledger."
    )
    pdf.body(
        "Requirements for authentication, upload safety, analysis, comparison, "
        "and integrity were met in code and in automated tests. The system refuses "
        "to call an unverified property clear. It does not pretend to be a public "
        "blockchain, a payment product, or a government portal. Within those "
        "honest bounds, a student can demonstrate a complete path from signup to "
        "a VALID or TAMPERED report PDF."
    )
    pdf.heading("9.2 Contributions")
    pdf.numbered(
        [
            "Three-state verification so missing papers remain NOT_VERIFIED.",
            "Hybrid Indic OCR plus rules, with a source-text veto on extraction.",
            "Case-level comparison with normalized survey prefixes and area tolerance.",
            "Separation of coverage percent from risk score.",
            "Tamper-evident local ledger with recomputed verification.",
            "A 39-case pytest suite that mocks the paid AI boundary.",
        ]
    )
    pdf.heading("9.3 Future enhancement")
    pdf.bullets(
        [
            "Named-entity recognition for Kannada party names, with user confirmation of document type.",
            "Optional support for additional Indian languages if the OCR provider exposes them.",
            "Government API integration where legally permitted, never scraping.",
            "Real payment processing only if the product is commercialized.",
            "RFC 3161 trusted timestamps to complement the local GENESIS chain.",
            "Mobile application and better handling of bound-register photographs.",
            "Human-in-the-loop review where an advocate can override a status with an audit note.",
            "Stronger production hardening: rate limits, object storage, secret rotation.",
        ]
    )
    pdf.heading("9.4 Closing remark")
    pdf.body(
        "BhoomiScan is a first pass, not a final legal opinion. Used that way, it "
        "can help a buyer ask better questions before money changes hands. Used "
        "as a rubber stamp, it would be harmful. The software is written to make "
        "the first use natural and the second use difficult."
    )

    # ------------------------------------------------------------------ #
    pdf.chapter("Chapter 10", "References")
    pdf.heading("10.1 Software and frameworks")
    pdf.numbered(
        [
            "FastAPI documentation. https://fastapi.tiangolo.com/",
            "SQLAlchemy 2.0 documentation. https://docs.sqlalchemy.org/",
            "PostgreSQL 16 documentation. https://www.postgresql.org/docs/16/",
            "React documentation. https://react.dev/",
            "Vite documentation. https://vite.dev/",
            "Tailwind CSS documentation. https://tailwindcss.com/docs",
            "Uvicorn. https://www.uvicorn.org/",
            "Pydantic Settings. https://docs.pydantic.dev/",
            "PyJWT. https://pyjwt.readthedocs.io/",
            "fpdf2. https://py-pdf.github.io/fpdf2/",
            "pytest. https://docs.pytest.org/",
            "Docker Compose. https://docs.docker.com/compose/",
        ]
    )
    pdf.heading("10.2 AI and language technology")
    pdf.numbered(
        [
            "Sarvam AI, Document AI and translation APIs. https://www.sarvam.ai/",
            "Unicode Consortium, Kannada block U+0C80 to U+0CFF.",
            "National Institute of Standards and Technology, FIPS 180-4, Secure Hash Standard (SHA-256).",
        ]
    )
    pdf.heading("10.3 Domain and academic context")
    pdf.numbered(
        [
            "The Registration Act, 1908 (India), on registration of documents.",
            "The Transfer of Property Act, 1882 (India), on sale and mortgages of immovable property.",
            "Karnataka land records and registration practice (Bhoomi / Kaveri context) as publicly described by state departments. This project does not scrape those portals.",
            "Pressman, R. S., Software Engineering: A Practitioner's Approach, McGraw-Hill.",
            "Sommerville, I., Software Engineering, Pearson.",
            "IEEE Recommended Practice for Software Requirements Specifications, IEEE Std 830.",
        ]
    )
    pdf.heading("10.4 Project artefacts")
    pdf.numbered(
        [
            "BhoomiScanV18 source repository: backend FastAPI application and frontend React SPA.",
            "README.md, run instructions and Phase 1 journey.",
            "docs/BhoomiScan_Test_Case_Report.md and generated Phase 1 / Phase 2 test PDFs.",
            "backend/tests/test_phase1.py, test_phase2.py, test_phase3.py.",
            "This report generated by docs/generate_detailed_project_report.py.",
        ]
    )
    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(80, 80, 80)
    pdf.multi_cell(
        0,
        5,
        ascii(
            "End of report. BhoomiScan - Your AIvocate. AI-assisted document review only. "
            "Not a legal guarantee."
        ),
    )


def build(toc_pages=None) -> ReportPDF:
    pdf = ReportPDF(toc_pages=toc_pages)
    fill(pdf)
    return pdf


def main():
    first = build()
    pdf = build(toc_pages=first.collected_pages)
    out = DOCS / "BhoomiScan_Detailed_Project_Report.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(out))
    data = out.read_bytes()
    copies = [
        DESKTOP / "BhoomiScan_Detailed_Project_Report.pdf",
        ONEDRIVE_DESKTOP / "BhoomiScan_Detailed_Project_Report.pdf",
    ]
    printed = [str(out)]
    for dest in copies:
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            printed.append(str(dest))
        except OSError as exc:
            print("skip %s: %s" % (dest, exc))
    for path in printed:
        print(path)
    print("pages=%s bytes=%s" % (pdf.page_no(), len(data)))


if __name__ == "__main__":
    main()
