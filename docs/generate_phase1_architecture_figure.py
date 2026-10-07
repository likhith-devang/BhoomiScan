"""IEEE-style Fig. 4: BhoomiScan Phase I system architecture."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUTS = [
    ROOT / "docs" / "Fig4_Phase1_System_Architecture.png",
    Path.home() / "Desktop" / "Fig4_Phase1_System_Architecture.png",
    Path.home() / "OneDrive" / "Desktop" / "Fig4_Phase1_System_Architecture.png",
]

LAYERS = [
    ("User Interface Layer", "React.js + Vite portal: login, residential case, upload, pipeline status, findings, evidence, recommendations", "#E3F2FD", "#1565C0"),
    ("Application Layer", "FastAPI REST API: JWT (HS256) auth, case and document routes, analyze orchestration", "#E0F2F1", "#00695C"),
    ("Document Processing Layer", "Sarvam Document AI: OCR digitization, Kannada detection, translation, schema extraction, type classification", "#E8EAF6", "#283593"),
    ("Validation and Risk Layer", "Regex merge, source-text veto, five-category rule engine, three states, evidence and recommendations", "#FFF3E0", "#E65100"),
    ("Data Storage Layer", "PostgreSQL 16 (users, cases, documents, findings) and local disk (original PDF / PNG / JPG bytes)", "#F5F5F5", "#424242"),
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    names = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf",
    ]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def italic(size: int) -> ImageFont.FreeTypeFont:
    for name in ("C:/Windows/Fonts/ariali.ttf", "C:/Windows/Fonts/calibrii.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return font(size)


def rounded(draw, box, radius, fill, outline, width=3):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow_down(draw, x, y1, y2):
    draw.line((x, y1, x, y2 - 12), fill="#222222", width=3)
    draw.polygon([(x, y2), (x - 8, y2 - 14), (x + 8, y2 - 14)], fill="#222222")


def draw() -> None:
    w, h = 1700, 2100
    img = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(img)
    title_f = font(34, bold=True)
    layer_f = font(24, bold=True)
    body_f = font(20)
    small_f = font(18, bold=True)
    cap_f = italic(22)

    title = "System Architecture of BhoomiScan Phase I"
    tw = d.textlength(title, font=title_f)
    d.text(((w - tw) / 2, 36), title, fill="#111111", font=title_f)

    user_box = (560, 100, 1140, 175)
    rounded(d, user_box, 40, "#C8E6C9", "#2E7D32", 4)
    label = "Property Buyer (Web Browser)"
    d.text((850 - d.textlength(label, font=layer_f) / 2, 122), label, fill="#111111", font=layer_f)

    left, right = 80, 1200
    y = 210
    box_h = 168
    gap = 46
    cx = (left + right) // 2
    layer_bottoms = []

    arrow_down(d, 850, 175, 208)

    for i, (name, desc, fill, edge) in enumerate(LAYERS):
        box = (left, y, right, y + box_h)
        rounded(d, box, 18, fill, edge, 4)
        d.text((left + 28, y + 22), f"{i + 1}. {name}", fill="#111111", font=layer_f)
        # wrap description
        words = desc.split()
        lines, cur = [], ""
        for word in words:
            trial = f"{cur} {word}".strip()
            if d.textlength(trial, font=body_f) < (right - left - 56):
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        ty = y + 68
        for line in lines[:3]:
            d.text((left + 28, ty), line, fill="#333333", font=body_f)
            ty += 28
        layer_bottoms.append(y + box_h)
        if i < len(LAYERS) - 1:
            arrow_down(d, cx, y + box_h + 2, y + box_h + gap - 2)
        y += box_h + gap

    # External service
    ext = (1260, 520, 1640, 820)
    rounded(d, ext, 18, "#F3E5F5", "#6A1B9A", 4)
    d.text((1280, 545), "External Service", fill="#111111", font=small_f)
    d.text((1280, 585), "Sarvam Document AI", fill="#111111", font=layer_f)
    for i, line in enumerate(["OCR (kn-IN)", "Translate (en-IN)", "Schema extract", "Called only on Analyze"]):
        d.text((1280, 640 + i * 32), f"- {line}", fill="#333333", font=body_f)

    # connector from processing layer (index 2) to Sarvam
    proc_mid_y = 210 + 2 * (box_h + gap) + box_h // 2
    d.line((right, proc_mid_y, 1260, 670), fill="#6A1B9A", width=3)
    d.polygon([(1260, 670), (1244, 662), (1244, 678)], fill="#6A1B9A")

    note = "Phase I ends at individual document analysis. No public blockchain, Neo4j, or live court APIs."
    last = layer_bottoms[-1]
    nw = d.textlength(note, font=body_f)
    d.text(((w - nw) / 2, last + 36), note, fill="#444444", font=body_f)

    caption = "Fig. 4. System Architecture of BhoomiScan Phase I."
    cw = d.textlength(caption, font=cap_f)
    d.text(((w - cw) / 2, last + 78), caption, fill="#222222", font=cap_f)

    crop = img.crop((0, 0, w, last + 140))
    for path in OUTS:
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            crop.save(path, "PNG")
            print(path)
        except OSError as exc:
            print(f"skip {path}: {exc}")


if __name__ == "__main__":
    draw()
