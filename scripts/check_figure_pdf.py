"""Inspect a one-page figure PDF at its intended, uniformly scaled placement width."""
import argparse
from collections import defaultdict
import json
import math
from pathlib import Path
import sys


def positive(text):
    value = float(text)
    if not math.isfinite(value) or value <= 0:
        raise argparse.ArgumentTypeError("a positive finite number is required")
    return value


def minimum_dpi(image, scale):
    # Map a single source pixel to page points. The largest singular value
    # gives the weakest sampling density, also for rotated or skewed images.
    a, b, c, d, _, _ = image["transform"]
    a, b = a / image["width"], b / image["width"]
    c, d = c / image["height"], d / image["height"]
    stretch = (math.hypot(a + d, b - c) + math.hypot(a - d, b + c)) / 2
    return 72 / (scale * stretch) if stretch > 0 else None


def inspect(page, width_mm, min_text_pt, min_dpi):
    mm_per_pt = 25.4 / 72
    source_width = page.rect.width * mm_per_pt
    scale = width_mm / source_width
    # Extraction coordinates are unrotated even when placement uses the rotated page.
    crop = page.rect * page.derotation_matrix
    # Under unequal horizontal and vertical scaling the two extraction modes
    # can report different point sizes. Compare the same glyph origins before
    # treating a text trace as a single measurable font size.
    sizes_at_origin = defaultdict(set)
    for block in page.get_text("rawdict", flags=0)["blocks"]:
        for line in block.get("lines", ()):
            for span in line["spans"]:
                for char in span["chars"]:
                    sizes_at_origin[char["origin"]].add(span["size"])
    sizes = []
    uncertain_spans = 0
    for span in page.get_texttrace():
        if span["type"] == 3 or not span["opacity"] or not span["chars"]:
            continue
        origins = [char[2] for char in span["chars"]
                   if not chr(char[0]).isspace() and crop.intersects(char[3])]
        if not origins:
            continue
        extracted = {value for origin in origins for value in sizes_at_origin.get(origin, (None,))}
        if None in extracted or any(not math.isclose(value, span["size"], rel_tol=1e-4, abs_tol=1e-4)
                                    for value in extracted):
            uncertain_spans += 1
        else:
            sizes.append(span["size"] * scale)
    densities = [minimum_dpi(im, scale) for im in page.get_image_info()
                 if crop.intersects(im["bbox"])]
    measurable = [v for v in densities if v is not None]
    failures = []
    unmeasured = []
    # PDF coordinates may be rounded by the exporter to a fraction of a point.
    if min_text_pt is not None:
        if uncertain_spans:
            unmeasured.append("ambiguous text size; inspect transformed or clipped labels at placement width")
        if not sizes and not uncertain_spans:
            unmeasured.append("no measurable text; inspect outlined or rasterized labels visually")
        if sizes and min(sizes) + 1e-4 < min_text_pt:
            failures.append("text below supplied point size")
    if min_dpi is not None:
        if len(measurable) != len(densities):
            unmeasured.append("unmeasurable raster placement")
        if measurable and min(measurable) + 1e-4 < min_dpi:
            failures.append("raster below supplied dpi")
    return {
        "source_width_mm": source_width, "placed_width_mm": width_mm,
        "placed_height_mm": page.rect.height * mm_per_pt * scale,
        "scale": scale, "measurable_text_spans": len(sizes),
        "unmeasurable_text_spans": uncertain_spans,
        "smallest_measurable_text_pt": min(sizes) if sizes else None,
        "raster_placements": len(densities),
        "lowest_measurable_raster_dpi": min(measurable) if measurable else None,
        "failures": failures, "unmeasured": unmeasured,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("figure", type=Path)
    parser.add_argument("--placed-width-mm", type=positive, required=True)
    parser.add_argument("--min-text-pt", type=positive)
    parser.add_argument("--min-image-dpi", type=positive)
    args = parser.parse_args()
    try:
        import pymupdf
    except ImportError:
        parser.exit(2, "Select a Python environment with PyMuPDF installed.\n")
    try:
        with pymupdf.open(args.figure) as document:
            if not document.is_pdf or document.needs_pass or len(document) != 1:
                parser.error("use an unencrypted one-page PDF of the figure itself")
            result = inspect(document[0], args.placed_width_mm, args.min_text_pt, args.min_image_dpi)
    except (OSError, RuntimeError, ValueError) as error:
        parser.exit(2, f"{error}\n")
    print(json.dumps(result, allow_nan=False, indent=2))
    if result["failures"]:
        return 1
    return 3 if result["unmeasured"] else 0


if __name__ == "__main__":
    sys.exit(main())
