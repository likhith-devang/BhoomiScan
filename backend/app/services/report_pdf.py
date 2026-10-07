"""PDF export for a finalized BhoomiScan risk report."""

from fpdf import FPDF
from fpdf.enums import XPos, YPos

from app.constants import DISCLAIMER


def _safe(text) -> str:
    return str(text or "").encode("latin-1", "replace").decode("latin-1")


class DueDiligencePDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(90, 90, 90)
        self.cell(0, 8, "BhoomiScan  |  Your AIvocate.  |  Risk report", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, "AI-assisted review only. Not a legal guarantee.", align="C")

    def heading(self, text: str):
        self.ln(3)
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(31, 79, 216)
        self.cell(0, 8, _safe(text), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(212, 175, 55)
        self.line(16, self.get_y(), 194, self.get_y())
        self.ln(3)
        self.set_text_color(20, 20, 20)

    def body(self, text: str):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5.2, _safe(text))
        self.ln(1)


def build_report_pdf(report) -> bytes:
    content = report.report_content or {}
    pdf = DueDiligencePDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_left_margin(16)
    pdf.set_right_margin(16)
    pdf.add_page()
    pdf.set_fill_color(11, 16, 32)
    pdf.rect(0, 0, 210, 40, "F")
    pdf.set_xy(16, 12)
    pdf.set_text_color(212, 175, 55)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 6, "BHOOMISCAN  |  YOUR AIVOCATE.")
    pdf.ln(8)
    pdf.set_x(16)
    pdf.set_text_color(246, 241, 230)
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 8, "Risk Report")
    pdf.ln(18)
    pdf.set_text_color(20, 20, 20)

    pdf.heading("Risk score")
    pdf.body(f"{report.risk_score} / 100\nRisk level: {report.risk_level}")

    pdf.heading("Because")
    reasons = content.get("score_reasons") or []
    if reasons:
        pdf.body("\n".join(f"- {item.get('reason')} (+{item.get('points')})" for item in reasons))
    else:
        issues = content.get("detected_issues") or []
        pdf.body(
            "\n".join(f"- {item.get('summary') or item.get('category_label')}" for item in issues)
            or "No DETECTED issues in the provided documents."
        )

    pdf.heading("Integrity")
    pdf.body(f"Report hash (SHA-256): {report.report_hash}\nVersion: {report.version}")

    pdf.heading("Disclaimer")
    pdf.body(content.get("disclaimer") or DISCLAIMER)
    return bytes(pdf.output())
