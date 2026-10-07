"""Shared academic PDF helpers for BhoomiScan Phase 1 and Phase 2 papers."""

from pathlib import Path

from fpdf import FPDF
from fpdf.enums import XPos, YPos

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DESKTOP = Path.home() / "Desktop"
ONEDRIVE_DESKTOP = Path.home() / "OneDrive" / "Desktop"

# Same abstract for Phase I and Phase II papers (university requirement).
SHARED_ABSTRACT = (
    "In the real estate sector, ownership disputes, forged property papers, and weak "
    "transparency in land transactions remain common problems. BhoomiScan is a "
    "property-document verification platform that uses artificial intelligence, "
    "multilingual natural language processing, and blockchain-based hash records to "
    "make validation more reliable. The platform is designed to accept, assess, and "
    "verify property documents written in regional languages as well as in English. "
    "Optical character recognition and natural language processing extract key fields "
    "from the uploaded files, including owner names, survey numbers, registration "
    "details, and property descriptions. The extracted data are then compared across "
    "documents to flag inconsistencies, conflicting ownership details, and other "
    "irregular or fabricated-looking entries. Hashes of documents and verification "
    "records are stored on a blockchain-style ledger so that later tampering can be "
    "detected and the trail of checks remains auditable. The novelty of this work is "
    "not the use of OCR or hashing by themselves. It is a hybrid method in which "
    "document AI is used only to read text, while deterministic rules assign each "
    "risk category one of three states: DETECTED, NO_ISSUE_FOUND, or NOT_VERIFIED. "
    "Missing papers are never treated as a clean title. A source-text veto restores "
    "stay orders and case details if the extractor omits them. Survey numbers, names, "
    "and areas are compared across files with explicit MATCH or MISMATCH, not against "
    "a government portal. Verification coverage and the numeric risk score are kept "
    "as two different measures so completeness is not confused with safety. Integrity "
    "is a local SHA-256 GENESIS hash chain that is recomputed on verify; it is not a "
    "public blockchain. By supporting Indian-language papers and reducing purely "
    "manual reading, BhoomiScan aims to simplify property verification, lower the "
    "human effort required for a first-pass review, and reduce the chance that "
    "fraudulent land and real estate documents pass unnoticed."
)
SHARED_KEYWORDS = (
    "property document verification, hybrid OCR and rules, three-state verification, "
    "cross-document comparison, SHA-256 hash chain, multilingual NLP"
)


def ascii(text: str) -> str:
    return str(text or "").encode("latin-1", "replace").decode("latin-1")


class AcademicPaper(FPDF):
    def __init__(self, running_title: str):
        super().__init__(format="A4")
        self.running_title = running_title
        self.collected_pages = {}
        self.set_auto_page_break(auto=True, margin=16)
        self.set_left_margin(16)
        self.set_right_margin(16)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Times", "I", 8)
        self.set_text_color(80, 80, 80)
        usable = self.w - self.l_margin - self.r_margin
        self.set_x(self.l_margin)
        self.cell(usable - 16, 6, ascii(self.running_title), align="L")
        self.cell(16, 6, str(self.page_no()), align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(120, 120, 120)
        self.set_line_width(0.2)
        self.line(16, self.get_y(), 194, self.get_y())
        self.ln(3)

    def footer(self):
        self.set_y(-12)
        self.set_font("Times", "I", 8)
        self.set_text_color(110, 110, 110)
        self.cell(0, 8, ascii("BhoomiScan student research paper. Not a legal opinion."), align="C")

    def mark(self, title: str):
        self.collected_pages[title] = self.page_no()

    def title_block(self, title: str, subtitle: str, meta_lines: list[str]):
        self.set_x(self.l_margin)
        self.set_font("Times", "B", 16)
        self.set_text_color(20, 20, 20)
        self.multi_cell(0, 7.2, ascii(title), align="C")
        self.ln(1)
        self.set_x(self.l_margin)
        self.set_font("Times", "I", 11)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 5.5, ascii(subtitle), align="C")
        self.ln(2)
        self.set_font("Times", "", 10)
        self.set_text_color(40, 40, 40)
        for line in meta_lines:
            self.set_x(self.l_margin)
            self.multi_cell(0, 5, ascii(line), align="C")
        self.ln(3)
        self.set_draw_color(30, 30, 30)
        self.line(60, self.get_y(), 150, self.get_y())
        self.ln(4)

    def abstract_box(self, text: str, keywords: str):
        self.set_x(self.l_margin)
        self.set_font("Times", "B", 11)
        self.cell(0, 6, "Abstract", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_x(self.l_margin)
        self.set_font("Times", "", 10)
        self.multi_cell(0, 5.1, ascii(text))
        self.ln(2)
        self.set_x(self.l_margin)
        self.set_font("Times", "B", 10)
        self.cell(22, 5.1, "Keywords:")
        self.set_font("Times", "I", 10)
        self.multi_cell(0, 5.1, ascii(keywords))
        self.ln(3)

    def section(self, title: str):
        if self.get_y() + 16 > self.page_break_trigger:
            self.add_page()
        self.ln(2)
        self.mark(title)
        self.set_x(self.l_margin)
        self.set_font("Times", "B", 12)
        self.set_text_color(20, 20, 20)
        self.multi_cell(0, 6.2, ascii(title))
        self.ln(1)

    def subsection(self, title: str):
        if self.get_y() + 12 > self.page_break_trigger:
            self.add_page()
        self.set_x(self.l_margin)
        self.set_font("Times", "B", 11)
        self.set_text_color(20, 20, 20)
        self.multi_cell(0, 5.6, ascii(title))
        self.ln(0.6)

    def body(self, text: str):
        self.set_x(self.l_margin)
        self.set_font("Times", "", 10)
        self.set_text_color(25, 25, 25)
        self.multi_cell(0, 5.15, ascii(text))
        self.ln(1.2)

    def bullets(self, items: list[str]):
        self.set_font("Times", "", 10)
        for item in items:
            if self.get_y() + 9 > self.page_break_trigger:
                self.add_page()
            self.set_x(self.l_margin)
            self.multi_cell(0, 5.1, ascii("    -  %s" % item))
        self.ln(1.2)

    def numbered(self, items: list[str]):
        self.set_font("Times", "", 10)
        for i, item in enumerate(items, 1):
            if self.get_y() + 9 > self.page_break_trigger:
                self.add_page()
            self.set_x(self.l_margin)
            self.multi_cell(0, 5.1, ascii("    %s)  %s" % (i, item)))
        self.ln(1.2)

    def equation(self, text: str):
        if self.get_y() + 10 > self.page_break_trigger:
            self.add_page()
        self.set_x(self.l_margin)
        self.set_font("Times", "I", 10)
        self.multi_cell(0, 5.2, ascii(text), align="C")
        self.ln(1.5)

    def diagram(self, lines: list[str], caption: str):
        if self.get_y() + 10 + 3.8 * len(lines) > self.page_break_trigger:
            self.add_page()
        self.set_font("Courier", "", 7)
        self.set_text_color(20, 20, 20)
        for line in lines:
            if self.get_y() + 5 > self.page_break_trigger:
                self.add_page()
                self.set_font("Courier", "", 7)
            self.set_x(self.l_margin)
            self.cell(0, 3.8, ascii(line), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)
        self.set_font("Times", "I", 9)
        self.multi_cell(0, 4.6, ascii(caption), align="C")
        self.ln(2)

    def table(self, headers: list[str], rows: list[list[str]], widths: list[float] | None = None, caption: str = ""):
        usable = self.w - self.l_margin - self.r_margin
        if not widths:
            widths = [usable / len(headers)] * len(headers)
        if self.get_y() + 18 > self.page_break_trigger:
            self.add_page()
        self.set_x(self.l_margin)
        self.set_fill_color(230, 230, 230)
        self.set_font("Times", "B", 8)
        for header, width in zip(headers, widths):
            self.cell(width, 6.2, ascii(header)[: int(width * 0.72)], fill=True, border=1)
        self.ln()
        self.set_font("Times", "", 8)
        for row in rows:
            if self.get_y() + 7 > self.page_break_trigger:
                self.add_page()
                self.set_x(self.l_margin)
                self.set_font("Times", "B", 8)
                for header, width in zip(headers, widths):
                    self.cell(width, 6.2, ascii(header)[: int(width * 0.72)], fill=True, border=1)
                self.ln()
                self.set_font("Times", "", 8)
            self.set_x(self.l_margin)
            for cell, width in zip(row, widths):
                self.cell(width, 6, ascii(cell)[: int(width * 0.85)], border=1)
            self.ln()
        if caption:
            self.ln(1)
            self.set_font("Times", "I", 9)
            self.multi_cell(0, 4.6, ascii(caption), align="C")
        self.ln(2)


def export_pdf(pdf: AcademicPaper, filename: str) -> list[str]:
    out = DOCS / filename
    out.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(out))
    data = out.read_bytes()
    written = [str(out)]
    for dest in (DESKTOP / filename, ONEDRIVE_DESKTOP / filename):
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            written.append(str(dest))
        except OSError as exc:
            print("skip %s: %s" % (dest, exc))
    print("pages=%s bytes=%s" % (pdf.page_no(), len(data)))
    for path in written:
        print(path)
    return written
