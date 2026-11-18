#!/usr/bin/env python3
"""Read-only text evidence from manuscripts and reviewer comments.

DOCX/text use the standard library; PDF requires an existing PyMuPDF installation.
Extraction and literal differences do not establish semantic or visual correctness.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
from difflib import SequenceMatcher
import hashlib
import io
import json
from pathlib import Path
import re
import sys
from zipfile import BadZipFile, ZipFile
from xml.etree.ElementTree import ParseError

# Resolve the companion shipped in the same skill, not a research-project module.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_docx import parse_xml, q, MAX_BYTES


TEXT_SUFFIXES = {".md", ".txt", ".tex", ".ltx", ".csv"}
ALTERNATE = "{http://schemas.openxmlformats.org/markup-compatibility/2006}AlternateContent"


def identity(path, raw):
    return {"path": str(path), "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}


def unique_json(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key: " + key)
        result[key] = value
    return result


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"), object_pairs_hook=unique_json,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def write_new_json(path, value):
    with Path(path).open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")


def docx_units(raw, view):
    units, notes = [], []
    counts = Counter()
    hidden = {q("del"), q("moveFrom")} if view == "final" else {q("ins"), q("moveTo")}
    with ZipFile(io.BytesIO(raw)) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)) or len(names) > 10000:
            raise ValueError("Duplicate or excessive DOCX package entries")
        if sum(item.file_size for item in archive.infolist()) > MAX_BYTES:
            raise ValueError("DOCX expanded data exceeds 128 MiB")
        if "word/document.xml" not in names:
            raise ValueError("DOCX has no word/document.xml")
        selected = ["word/document.xml"] + sorted(name for name in names if re.fullmatch(
            r"word/(?:header[^/]*|footer[^/]*|footnotes|endnotes|comments)\.xml", name))
        for part in selected:
            root = parse_xml(archive.read(part), part)
            if part == "word/document.xml" and (root.tag != q("document") or root.find(q("body")) is None):
                raise ValueError("Invalid DOCX main part: expected w:document containing w:body")
            for node in root.iter():
                tag = node.tag.rsplit("}", 1)[-1]
                if node.tag == ALTERNATE:
                    counts["unresolved_alternate_content"] += 1
                if tag in {"ins", "del", "moveFrom", "moveTo", "drawing", "pict", "oMath",
                           "altChunk", "fldSimple", "fldChar", "pPrChange", "rPrChange",
                           "trPrChange", "tblPrChange", "tcPrChange", "cellDel", "cellIns", "cellMerge", "vMerge"}:
                    counts[tag] += 1
            parents = {child: parent for parent in root.iter() for child in parent}

            def ancestors(node):
                while node in parents:
                    node = parents[node]
                    yield node

            def visible_text(node, top=True):
                if node.tag in hidden or node.tag == ALTERNATE or (not top and node.tag == q("p")):
                    return ""
                if node.tag in {q("t"), q("delText")}:
                    return node.text or ""
                if node.tag == q("tab"):
                    return "\t"
                if node.tag in {q("br"), q("cr")}:
                    return "\n"
                return "".join(visible_text(child, False) for child in node)

            for index, paragraph in enumerate(root.iter(q("p")), 1):
                ancestry = list(ancestors(paragraph))
                if any(node.tag in hidden or node.tag == ALTERNATE for node in ancestry):
                    continue
                text = visible_text(paragraph)
                if not text.strip():
                    continue
                channel = ("body" if part == "word/document.xml" else
                           "comment" if part == "word/comments.xml" else "supplement")
                locator = {"part": part, "paragraph": index, "view": view,
                           "inside_table": any(node.tag == q("tc") for node in ancestry),
                           "inside_textbox": any(node.tag == q("txbxContent") for node in ancestry)}
                # These revisions live in properties, not enclosing run wrappers.
                # Keep their text available for inspection but never silently
                # assert that it belongs to the selected editor view.
                ambiguities = set()
                for owner in [paragraph, *ancestry]:
                    if owner.tag == q("tr"):
                        props, markers, label = owner.find(q("trPr")), {q("ins"), q("del"), q("trPrChange")}, "table_row_revision"
                    elif owner.tag == q("tc"):
                        props, markers, label = owner.find(q("tcPr")), {q("cellIns"), q("cellDel"), q("cellMerge"), q("tcPrChange")}, "table_cell_revision"
                    elif owner.tag == q("p"):
                        props, markers, label = owner.find(q("pPr")), {q("ins"), q("del"), q("moveFrom"), q("moveTo")}, "paragraph_mark_revision"
                    else:
                        continue
                    if props is not None and any(node.tag in markers for node in props.iter()):
                        ambiguities.add(label)
                if ambiguities:
                    locator["projection_ambiguities"] = sorted(ambiguities)
                for node in ancestry:
                    if node.tag == q("comment"):
                        locator.update({"comment_id": node.get(q("id")),
                                        "author": node.get(q("author")), "date": node.get(q("date"))})
                        break
                anchors = sorted({n.get(q("id")) for n in paragraph.iter()
                                  if n.tag in {q("commentRangeStart"), q("commentReference")}
                                  and n.get(q("id")) is not None})
                if anchors:
                    locator["comment_anchor_ids"] = anchors
                units.append({"channel": channel, "text": text, "locator": locator})
    notes.extend([
        "DOCX text projection only: final/original filter run insertion/deletion and move wrappers; source revisions are not accepted or rejected.",
        "Paragraph-mark, table/row/cell and property revisions are not fully reconstructed; resolve ambiguous views with the target editor.",
        "Units marked projection_ambiguities are inspection text, not verified final/original-view manuscript evidence.",
        "Cached field results may be old; style-generated numbering, equations, drawings, pagination, hidden-text settings and embedded objects need separate inspection.",
        "Classic comments are separate units; modern threaded comments, replies, anchors spanning paragraphs and resolved state may be incomplete.",
    ])
    if counts["unresolved_alternate_content"]:
        notes.append("AlternateContent compatibility branches excluded: the target editor must determine which branch is displayed; neither branch is body evidence here.")
    return units, notes, {"parts_read": selected, "objects": dict(counts)}


def pdf_units(raw):
    try:
        import pymupdf as fitz
    except ImportError:
        try:
            import fitz
        except ImportError as exc:
            raise ValueError("PDF extraction requires PyMuPDF in this interpreter; no dependency was installed") from exc
    units, notes, empty_pages = [], [], []
    with fitz.open(stream=raw, filetype="pdf") as document:
        if document.needs_pass:
            raise ValueError("Encrypted PDF needs a separately authorized unlocked working copy")
        for page in document:
            locator = {"pdf_page": page.number + 1, "pdf_label": page.get_label(),
                       "printed_page": None, "printed_line": None}
            blocks = page.get_text("blocks", sort=True)
            found = False
            for index, block in enumerate(blocks, 1):
                if len(block) >= 7 and block[6] == 0 and str(block[4]).strip():
                    found = True
                    units.append({"channel": "body", "text": str(block[4]),
                                  "locator": {**locator, "block": index, "bbox": list(block[:4])}})
            if not found:
                empty_pages.append(page.number + 1)
            for annotation in page.annots() or ():
                info = annotation.info or {}
                content = info.get("content", "")
                units.append({"channel": "comment", "text": content,
                              "locator": {**locator, "annotation_xref": annotation.xref,
                                          "annotation_type": annotation.type[1],
                                          "author": info.get("title", ""),
                                          "bbox": list(annotation.rect),
                                          "vertices": annotation.vertices}})
        details = {"pages_read": document.page_count, "pages_without_extracted_text": empty_pages}
    notes.extend([
        "PDF page index and embedded page label are not the printed page or printed line number; those require visual confirmation against this exact PDF.",
        "Text order, mathematical layout, annotation highlights without comment text and scanned pages need visual review; OCR was not run.",
        "Text blocks and comment contents only; no visual, image or scientific comparison was performed.",
    ])
    if empty_pages:
        notes.append("Pages without extracted text must not be treated as empty manuscript pages: " + str(empty_pages))
    return units, notes, details


def extract_document(path, view="final", encoding="utf-8-sig"):
    if view not in {"final", "original"}:
        raise ValueError("view must be final or original")
    path = Path(path).resolve(strict=True)
    if not path.is_file() or path.stat().st_size > MAX_BYTES:
        raise ValueError("Input must be a regular file up to 128 MiB")
    raw = path.read_bytes()
    if path.suffix.lower() == ".docx":
        units, notes, details = docx_units(raw, view)
    elif path.suffix.lower() == ".pdf":
        units, notes, details = pdf_units(raw)
    elif path.suffix.lower() in TEXT_SUFFIXES:
        text = raw.decode(encoding)
        if "\x00" in text:
            raise ValueError("Binary-like text input")
        units = [{"channel": "body", "text": line, "locator": {"line": n}}
                 for n, line in enumerate(text.splitlines(), 1) if line.strip()]
        notes = ["Single-file literal text; markup, TeX includes/macros and displayed equations were not expanded; blank-only line changes are excluded."]
        details = {"encoding": encoding, "lines": len(text.splitlines())}
    else:
        raise ValueError("Supported input: DOCX, PDF, MD, TXT, TEX, LTX, CSV")
    for index, unit in enumerate(units, 1):
        unit["id"] = "U%06d" % index
    if len(units) > 30000:
        raise ValueError("More than 30000 extracted units; compare selected chapters/files with explicit scope")
    return {"schema": "thesisforge.manuscript-snapshot/1", "source": identity(path, raw),
            "view": view, "created_at": datetime.now(timezone.utc).isoformat(),
            "units": units, "coverage": {"mode": "text_only", "notes": notes, **details},
            "semantic_review": "not_run", "visual_review": "not_run"}


def compare_snapshots(before, after):
    # Include the channel so a reviewer comment cannot become evidence of body edits.
    old, new = before["units"], after["units"]
    matcher = SequenceMatcher(None, [(u["channel"], u["text"]) for u in old],
                              [(u["channel"], u["text"]) for u in new], autojunk=True)
    changes = []
    for tag, i, j, a, b in matcher.get_opcodes():
        if tag != "equal":
            changes.append({"id": "C%05d" % (len(changes) + 1), "operation": tag,
                            "before": old[i:j], "after": new[a:b]})
    return {"schema": "thesisforge.manuscript-comparison/1", "before": before["source"],
            "after": after["source"], "before_view": before["view"], "after_view": after["view"],
            "source_bytes_differ": before["source"]["sha256"] != after["source"]["sha256"],
            "extracted_text_equal": not changes, "changes": changes,
            "limitations": ["Literal ordered text comparison with heuristic alignment, not a semantic or visual redline.",
                            "Moves may appear as deletion plus insertion; changed text can regress earlier correct content.",
                            "No text differences cannot close figure, formatting, equation or other uncovered concerns.",
                            "Change counts measure extraction/alignment operations, not reviewer issues or scientific improvements."],
            "semantic_review": "not_run", "visual_review": "not_run"}


def markdown_text(value):
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(
        ">", "&gt;").replace("\\", "\\\\").replace("|", "\\|").replace(
        "[", "\\[").replace("]", "\\]").replace("\n", "<br>")


def comparison_markdown(report):
    lines = ["# 原稿与修改稿：字面差异", "", "这是提取文本的对照，未判定语义、图表或版式是否正确。", "",
             "- 原稿：" + markdown_text(report["before"]["path"]) + "；SHA-256：" + report["before"]["sha256"] + "；提取视图：" + report["before_view"],
             "- 修改稿：" + markdown_text(report["after"]["path"]) + "；SHA-256：" + report["after"]["sha256"] + "；提取视图：" + report["after_view"],
             "- 正文、批注和页眉/注释等分别标出。Word 视图只是文本投影，PDF 页标签不是印刷页行；字段、图像、公式、版式及未解析对象另核。完整提取覆盖见同目录 before.json / after.json。", "",
             "| 差异 ID | 操作 | 原稿位置与文本 | 修改稿位置与文本 |", "|---|---|---|---|"]
    for change in report["changes"]:
        values = []
        for side in ("before", "after"):
            values.append("<br>".join(markdown_text(u["id"] + " [" + u["channel"] + "] " + json.dumps(u["locator"], ensure_ascii=False)
                                                  + " " + u["text"]) for u in change[side]) or "（无）")
        lines.append("| " + " | ".join([change["id"], change["operation"], *values]) + " |")
    if not report["changes"]:
        lines += ["", "提取范围内没有字面差异；仍须检查未覆盖对象及提取是否完整。"]
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    snapshot = commands.add_parser("snapshot", help="Extract text, comments and source identity")
    snapshot.add_argument("input", type=Path)
    snapshot.add_argument("--view", choices=("final", "original"), default="final")
    snapshot.add_argument("--output", type=Path, required=True)
    compare = commands.add_parser("compare", help="Compare two actual supplied manuscript files")
    compare.add_argument("before", type=Path)
    compare.add_argument("after", type=Path)
    compare.add_argument("--before-view", choices=("final", "original"), default="final")
    compare.add_argument("--after-view", choices=("final", "original"), default="final")
    compare.add_argument("--output-dir", type=Path, required=True)
    for command in (snapshot, compare):
        command.add_argument("--encoding", choices=("utf-8-sig", "gb18030"), default="utf-8-sig")
    args = parser.parse_args(argv)
    try:
        if args.command == "snapshot":
            if args.output.exists():
                raise ValueError("Output already exists")
            result = extract_document(args.input, args.view, args.encoding)
            write_new_json(args.output, result)
            print(json.dumps({"status": "extracted_not_semantically_verified", "units": len(result["units"]),
                              "output": str(args.output)}, ensure_ascii=True))
        else:
            if args.output_dir.exists():
                raise ValueError("Output directory already exists")
            old = extract_document(args.before, args.before_view, args.encoding)
            new = extract_document(args.after, args.after_view, args.encoding)
            result = compare_snapshots(old, new)
            args.output_dir.mkdir(parents=True, exist_ok=False)
            write_new_json(args.output_dir / "before.json", old)
            write_new_json(args.output_dir / "after.json", new)
            write_new_json(args.output_dir / "changes.json", result)
            with (args.output_dir / "changes.md").open("x", encoding="utf-8", newline="\n") as out:
                out.write(comparison_markdown(result))
            print(json.dumps({"status": "compared_not_semantically_verified", "changes": len(result["changes"]),
                              "output_dir": str(args.output_dir)}, ensure_ascii=True))
        return 0
    except (OSError, ValueError, KeyError, RuntimeError, BadZipFile, ParseError) as exc:
        print(json.dumps({"status": "error", "message": str(exc)}, ensure_ascii=True), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
