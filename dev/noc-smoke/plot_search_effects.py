"""Draw the NoC held-out paired effects from the per-trace records (ReportLab)."""
import argparse
import csv
from pathlib import Path
from statistics import mean

from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from analyze import summarize
from experiment import PATTERNS, TEST

HERE = Path(__file__).resolve().parent
GROUPS = [("uniform", "均匀流量", 94), ("hotspot", "热点流量", 51)]
AXIS_LABEL = "平均时延差（进化策略减随机策略，周期/包）"
TRACE_LABEL = "单条轨迹的配对差"
MEAN_LABEL = "组内均值"


def measurements(directory):
    summarize(directory)  # Check all four methods, loads, counts and shared traces.
    values = {}
    with (directory / "paired.csv").open(encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            key = row["pattern"], int(row["seed"]), row["method"]
            values[key] = int(row["latency_sum"]) / int(row["delivered"])
    return {pattern: [values[pattern, seed, "evolution"] - values[pattern, seed, "random"]
                      for seed in TEST[pattern]] for pattern in PATTERNS}


def make_figure(output, font, series):
    labels = TTFont("Labels", str(font))
    text = AXIS_LABEL + TRACE_LABEL + MEAN_LABEL + "0123456789."
    text += "".join(title for _, title, _ in GROUPS)
    missing = sorted({ord(c) for c in text if not labels.face.charToGlyph.get(ord(c))})
    if missing:
        codes = ", ".join(f"U+{n:04X}" for n in missing)
        raise ValueError(f"{font}: missing figure glyphs ({codes}); choose a Chinese TrueType font")
    pdfmetrics.registerFont(labels)
    page = canvas.Canvas(str(output), pagesize=(88.9 * mm, 144), invariant=1,
                         initialFontName="Labels", initialFontSize=9)
    page.setTitle("NoC source injection: paired differences on held-out traces")
    ink = HexColor("#1A2630")
    blue = HexColor("#165E80")
    grid = HexColor("#D5DEE4")
    page.setFont("Labels", 9)
    left, right = 44, 239
    low, high = -0.025, 0.20

    def xpos(value):
        if not low <= value <= high:
            raise ValueError("Observed difference outside the declared display range")
        return left + (value - low) * (right - left) / (high - low)

    for tick in (0, 0.05, 0.10, 0.15, 0.20):
        x = xpos(tick)
        page.setStrokeColor(ink if tick == 0 else grid)
        page.setLineWidth(0.7 if tick == 0 else 0.4)
        page.line(x, 30, x, 115)
        page.setFillColor(ink)
        page.drawCentredString(x, 19, f"{tick:.2f}" if tick else "0")

    for key, title, y in GROUPS:
        values = series[key]
        placed = []
        page.setFillColor(ink)
        page.drawString(2, y - 3, title)
        page.setStrokeColor(blue)
        page.setLineWidth(0.9)
        for value in sorted(values):
            x = xpos(value)
            # Stack only in the non-data direction; keep the true x coordinate.
            for lane in (0, 1, -1, 2, -2, 3, -3, 4, -4, 5, -5):
                yy = y + 4.9 * lane
                if all((x - px)**2 + (yy - py)**2 >= 4.8**2 for px, py in placed):
                    break
            else:
                raise ValueError("Dot stack has exceeded its display lanes")
            placed.append((x, yy))
            page.circle(x, yy, 1.85, fill=0, stroke=1)
        triangle(page, xpos(mean(values)), y + 22, ink)

    page.setFillColor(ink)
    page.drawCentredString(126, 3, AXIS_LABEL)
    page.setStrokeColor(blue)
    page.circle(49, 131, 1.85)
    page.drawString(56, 128, TRACE_LABEL)
    triangle(page, 164, 131, ink)
    page.drawString(171, 128, MEAN_LABEL)
    page.showPage()
    page.save()


def triangle(page, x, y, color):
    path = page.beginPath()
    path.moveTo(x, y - 3)
    path.lineTo(x - 3.3, y + 2.5)
    path.lineTo(x + 3.3, y + 2.5)
    path.close()
    page.setFillColor(color)
    page.drawPath(path, fill=1, stroke=0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font", required=True, type=Path, help="embeddable TTF with Chinese glyphs")
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    make_figure(args.out, args.font, measurements(HERE / "results"))
