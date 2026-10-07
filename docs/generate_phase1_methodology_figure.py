"""IEEE-style Fig. 3: BhoomiScan Phase I proposed methodology flowchart."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUTS = [
    ROOT / "docs" / "Fig3_Phase1_Proposed_Methodology.png",
    Path.home() / "Desktop" / "Fig3_Phase1_Proposed_Methodology.png",
    Path.home() / "OneDrive" / "Desktop" / "Fig3_Phase1_Proposed_Methodology.png",
]

STEPS = [
    ("Start", "start"),
    ("Login and Create Residential Case", "auth"),
    ("Upload Document (PDF, PNG, JPG)", "upload"),
    ("Document Digitization / OCR (Sarvam)", "read"),
    ("Kannada Detection and Translation", "read"),
    ("Information Extraction and Classification", "read"),
    ("Regex Merge and Source-Text Veto", "rule"),
    ("Risk Engine (Five Categories)", "risk"),
    ("DETECTED / NO_ISSUE_FOUND / NOT_VERIFIED", "risk"),
    ("Evidence Snippets and Recommendations", "result"),
    ("Individual Document Analysis", "result"),
    ("End", "end"),
]

COLORS = {
    "start": ("#C8E6C9", "#2E7D32"),
    "auth": ("#B2DFDB", "#00695C"),
    "upload": ("#B2DFDB", "#00695C"),
    "read": ("#BBDEFB", "#1565C0"),
    "rule": ("#90CAF9", "#0D47A1"),
    "risk": ("#FFE0B2", "#E65100"),
    "result": ("#EEEEEE", "#424242"),
    "end": ("#FFCDD2", "#C62828"),
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    names = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf",
        "C:/Windows/Fonts/timesbd.ttf" if bold else "C:/Windows/Fonts/times.ttf",
    ]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def rounded_rect(draw: ImageDraw.ImageDraw, box, radius, fill, outline, width=3):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_arrow(draw: ImageDraw.ImageDraw, x: int, y1: int, y2: int) -> None:
    draw.line((x, y1, x, y2 - 10), fill="#222222", width=3)
    draw.polygon([(x, y2), (x - 8, y2 - 14), (x + 8, y2 - 14)], fill="#222222")


def draw() -> None:
    w, h = 1400, 3200
    img = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(img)
    title_f = font(36, bold=True)
    box_f = font(26, bold=True)
    cap_f = font(22)
    italic_try = None
    for name in ("C:/Windows/Fonts/ariali.ttf", "C:/Windows/Fonts/calibrii.ttf", "C:/Windows/Fonts/timesi.ttf"):
        try:
            italic_try = ImageFont.truetype(name, 22)
            break
        except OSError:
            pass
    cap_f = italic_try or cap_f

    title = "Proposed Methodology of BhoomiScan Phase I"
    tw = d.textlength(title, font=title_f)
    d.text(((w - tw) / 2, 40), title, fill="#111111", font=title_f)

    box_w, box_h = 980, 118
    cx = w // 2
    left = cx - box_w // 2
    top = 130
    gap = 52
    centers = []

    for i, (label, kind) in enumerate(STEPS):
        y = top + i * (box_h + gap)
        centers.append(y + box_h // 2)
        face, edge = COLORS[kind]
        radius = 58 if kind in {"start", "end"} else 22
        rounded_rect(d, (left, y, left + box_w, y + box_h), radius, face, edge, width=4)
        lw = d.textlength(label, font=box_f)
        d.text((cx - lw / 2, y + box_h / 2 - 18), label, fill="#111111", font=box_f)

    for i in range(len(STEPS) - 1):
        y1 = top + i * (box_h + gap) + box_h
        y2 = top + (i + 1) * (box_h + gap)
        draw_arrow(d, cx, y1 + 4, y2 - 2)

    caption = "Fig. 3. Proposed Methodology of BhoomiScan Phase I (single-document pipeline)."
    cw = d.textlength(caption, font=cap_f)
    last_bottom = top + (len(STEPS) - 1) * (box_h + gap) + box_h
    d.text(((w - cw) / 2, last_bottom + 48), caption, fill="#222222", font=cap_f)

    crop_h = last_bottom + 130
    img = img.crop((0, 0, w, crop_h))

    for path in OUTS:
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            img.save(path, "PNG")
            print(path)
        except OSError as exc:
            print(f"skip {path}: {exc}")


if __name__ == "__main__":
    draw()
