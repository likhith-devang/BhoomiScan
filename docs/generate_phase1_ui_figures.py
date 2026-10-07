"""Paper figures: Phase I UI flow diagram and screenshot collage."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SHOT = Path(r"C:\Users\purus\AppData\Local\Temp\cursor\screenshots")
OUT_DIR = ROOT / "docs"

PANELS = [
    (SHOT / "ui_01_landing.png", "(a) Landing page"),
    (SHOT / "ui_02_signup.png", "(b) Sign up"),
    (SHOT / "ui_03_login.png", "(c) Login"),
    (SHOT / "ui_04_dashboard.png", "(d) Home / dashboard"),
    (SHOT / "ui_05_property_domain.png", "(e) Residential domain"),
    (SHOT / "ui_06_property_type.png", "(f) Property type"),
    (SHOT / "ui_07_upload.png", "(g) Document vault"),
    (SHOT / "ui_08_analysis_risk.png", "(h) Individual analysis"),
]

FLOW = [
    ("Landing", "Get Started"),
    ("Sign up / Login", "JWT session"),
    ("Home dashboard", "Start Analysis"),
    ("Property kind", "Homes only"),
    ("Home type", "Create case"),
    ("Document vault", "Upload PDF/PNG/JPG"),
    ("Analyze", "OCR + rules"),
    ("One-file result", "5 categories, 3 states"),
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
    for name in ("C:/Windows/Fonts/ariali.ttf", "C:/Windows/Fonts/timesi.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return font(size)


def save_all(img: Image.Image, name: str) -> None:
    targets = [
        OUT_DIR / name,
        Path.home() / "Desktop" / name,
        Path.home() / "OneDrive" / "Desktop" / name,
    ]
    for path in targets:
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            img.save(path, "PNG")
            print(path)
        except OSError as exc:
            print(f"skip {path}: {exc}")


def fit(im: Image.Image, box_w: int, box_h: int) -> Image.Image:
    im = im.convert("RGB")
    ratio = min(box_w / im.width, box_h / im.height)
    nw, nh = max(1, int(im.width * ratio)), max(1, int(im.height * ratio))
    resized = im.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (box_w, box_h), "#111318")
    canvas.paste(resized, ((box_w - nw) // 2, (box_h - nh) // 2))
    return canvas


def collage() -> None:
    cols, rows = 2, 4
    pad, label_h, title_h, cap_h = 22, 42, 90, 70
    panel_w, panel_h = 820, 460
    w = pad + cols * (panel_w + pad)
    h = title_h + rows * (label_h + panel_h + pad) + cap_h
    img = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(img)
    title_f, label_f, cap_f = font(32, True), font(20, True), italic(20)
    title = "Phase I User Interface Flow of BhoomiScan"
    d.text(((w - d.textlength(title, font=title_f)) / 2, 28), title, fill="#111111", font=title_f)

    for i, (path, label) in enumerate(PANELS):
        r, c = divmod(i, cols) if False else (i // cols, i % cols)
        x = pad + c * (panel_w + pad)
        y = title_h + r * (label_h + panel_h + pad)
        d.text((x, y), label, fill="#111111", font=label_f)
        shot = Image.open(path) if path.exists() else Image.new("RGB", (panel_w, panel_h), "#ddd")
        framed = fit(shot, panel_w, panel_h)
        img.paste(framed, (x, y + label_h))
        d.rectangle((x, y + label_h, x + panel_w, y + label_h + panel_h), outline="#333333", width=2)

    cap = "Fig. 5. College interface flow of BhoomiScan Phase I (landing to individual document analysis)."
    d.text(((w - d.textlength(cap, font=cap_f)) / 2, h - 46), cap, fill="#222222", font=cap_f)
    save_all(img, "Fig5_Phase1_UI_Collage.png")


def flowchart() -> None:
    w, h = 1500, 2100
    img = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(img)
    title_f, box_f, small_f, cap_f = font(32, True), font(22, True), font(16), italic(20)
    title = "User Interface Flow of BhoomiScan Phase I"
    d.text(((w - d.textlength(title, font=title_f)) / 2, 36), title, fill="#111111", font=title_f)

    box_w, box_h, gap = 720, 130, 48
    cx, left, top = w // 2, (w - 720) // 2, 120
    colors = [
        ("#C8E6C9", "#2E7D32"),
        ("#B2DFDB", "#00695C"),
        ("#BBDEFB", "#1565C0"),
        ("#BBDEFB", "#1565C0"),
        ("#BBDEFB", "#1565C0"),
        ("#E8EAF6", "#283593"),
        ("#FFE0B2", "#E65100"),
        ("#FFCDD2", "#C62828"),
    ]
    for i, ((name, note), (fill, edge)) in enumerate(zip(FLOW, colors)):
        y = top + i * (box_h + gap)
        radius = 58 if i in {0, len(FLOW) - 1} else 20
        d.rounded_rectangle((left, y, left + box_w, y + box_h), radius=radius, fill=fill, outline=edge, width=4)
        d.text((cx - d.textlength(name, font=box_f) / 2, y + 28), name, fill="#111111", font=box_f)
        d.text((cx - d.textlength(note, font=small_f) / 2, y + 72), note, fill="#333333", font=small_f)
        if i < len(FLOW) - 1:
            y1 = y + box_h + 4
            y2 = y + box_h + gap - 4
            d.line((cx, y1, cx, y2 - 12), fill="#222222", width=3)
            d.polygon([(cx, y2), (cx - 8, y2 - 14), (cx + 8, y2 - 14)], fill="#222222")

    last = top + (len(FLOW) - 1) * (box_h + gap) + box_h
    cap = "Fig. 6. Interface control flow used in Results (Phase I ends at one-file analysis)."
    d.text(((w - d.textlength(cap, font=cap_f)) / 2, last + 40), cap, fill="#222222", font=cap_f)
    crop = img.crop((0, 0, w, last + 110))
    save_all(crop, "Fig6_Phase1_UI_Flow.png")


if __name__ == "__main__":
    missing = [str(p) for p, _ in PANELS if not p.exists()]
    if missing:
        raise SystemExit("Missing screenshots:\n" + "\n".join(missing))
    collage()
    flowchart()
