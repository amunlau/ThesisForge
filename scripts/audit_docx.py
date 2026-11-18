#!/usr/bin/env python3
"""Read-only DOCX structure inventory. No Office, macros, network or dependencies.

Exit 0: inventory produced; 1: --strict found broken structural references;
2: invalid input or output. Findings are review prompts, not school compliance.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import posixpath
import re
import sys
import xml.etree.ElementTree as ET
from zipfile import BadZipFile, ZipFile

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
STRICT_W = "http://purl.oclc.org/ooxml/wordprocessingml/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
MC = "http://schemas.openxmlformats.org/markup-compatibility/2006"
NS = {"w": W}
MAX_BYTES = 128 * 1024 * 1024


def q(name):
    return "{" + W + "}" + name


def val(node, default=None):
    return node.get(q("val"), default) if node is not None else default


def attrs(node):
    return {k.rsplit("}", 1)[-1]: v for k, v in node.attrib.items()} if node is not None else {}


def properties(node):
    """Flatten explicitly stored properties; not a full Word rendering cascade."""
    result = {}
    if node is None:
        return result
    for child in node:
        name = child.tag.rsplit("}", 1)[-1]
        if name.endswith("Change"):
            continue
        if list(child):
            for key, value in properties(child).items():
                result[name + "." + key] = value
        else:
            values = attrs(child)
            if not values:
                result[name] = "true"
            for key, value in values.items():
                result[name + "." + key] = value
    return result


def parse_xml(data, part):
    if re.search(br"<!\s*(DOCTYPE|ENTITY)\b", data.replace(b"\x00", b""), re.I):
        raise ValueError(f"DTD/entity declarations unsupported: {part}")
    root = ET.fromstring(data)
    # Strict WordprocessingML uses the same local names for this inventory.
    for node in root.iter():
        node.tag = node.tag.replace("{" + STRICT_W + "}", "{" + W + "}")
        node.attrib = {k.replace("{" + STRICT_W + "}", "{" + W + "}").replace(
            "{http://purl.oclc.org/ooxml/officeDocument/relationships}", "{" + R + "}"): v
            for k, v in node.attrib.items()}
    return root


def view_context(node, parents):
    """Record branches whose inclusion requires a revision/consumer decision."""
    result = []
    while node is not None:
        local = node.tag.rsplit("}", 1)[-1]
        if (node.tag.startswith("{" + W + "}") and
                (local in {"ins", "del", "moveFrom", "moveTo"} or local.endswith("Change"))):
            result.append(local)
        elif node.tag in {"{" + MC + "}Choice", "{" + MC + "}Fallback"}:
            result.append("AlternateContent:" + local)
        if node.tag in {q("tr"), q("tc")}:
            props = node.find(q("trPr" if node.tag == q("tr") else "tcPr"))
            if props is not None:
                for item in props:
                    if item.tag in {q(v) for v in ("ins", "del", "cellIns", "cellDel", "cellMerge")}:
                        result.append(local + ":" + item.tag.rsplit("}", 1)[-1])
        node = parents.get(node)
    return sorted(set(result))


def field_inventory(root, part, bookmarks):
    fields, limits, findings, stack = [], [], [], []
    parents = {child: parent for parent in root.iter() for child in parent}
    for node in root.iter():
        context = view_context(node, parents)
        for field in stack:
            field["view_dependent_context"] = sorted(set(field["view_dependent_context"] + context))
        if node.tag == q("fldSimple"):
            fields.append({"part": part, "instruction": node.get(q("instr"), ""),
                           "display": "".join(t.text or "" for t in node.iter(q("t"))),
                           "simple": True, "dirty": node.get(q("dirty")), "view_dependent_context": context})
        elif node.tag == q("fldChar"):
            kind = node.get(q("fldCharType"))
            if kind == "begin":
                stack.append({"part": part, "instruction": "", "display": "", "separated": False,
                              "nested": bool(stack), "dirty": node.get(q("dirty")), "view_dependent_context": context})
            elif kind == "separate":
                if stack:
                    stack[-1]["separated"] = True
                else:
                    limits.append(f"{part}: field separator without begin")
            elif kind == "end":
                if stack:
                    fields.append(stack.pop())
                else:
                    limits.append(f"{part}: field end without begin")
        elif node.tag == q("instrText") and stack and not stack[-1]["separated"]:
            stack[-1]["instruction"] += node.text or ""
        elif node.tag == q("t"):
            # Inner displayed fields also contribute to an outer displayed field.
            for field in stack:
                if field["separated"]:
                    field["display"] += node.text or ""
    if stack:
        limits.append(f"{part}: {len(stack)} unclosed field(s)")
    for field in fields:
        match = re.match(r'\s*(?:REF|PAGEREF|NOTEREF)\s+(?:"([^"]+)"|(\S+))',
                         field["instruction"], re.I)
        if match:
            field["target"] = match.group(1) or match.group(2)
            field["target_present"] = field["target"] in bookmarks
            if not field["target_present"]:
                findings.append({"kind": "missing_field_bookmark", "part": part,
                                 "target": field["target"], "instruction": field["instruction"],
                                 "view_dependent_context": field["view_dependent_context"]})
        if str(field.get("dirty", "")).lower() in ("true", "1", "on"):
            findings.append({"kind": "field_marked_dirty", "part": part,
                             "instruction": field["instruction"]})
    return fields, limits, findings


def audit(path):
    path = Path(path).resolve()
    if path.suffix.lower() != ".docx":
        raise ValueError("Expected .docx (macro-enabled documents are not supported)")
    raw = path.read_bytes()
    if len(raw) > MAX_BYTES:
        raise ValueError("DOCX exceeds 128 MiB input limit")
    findings, limits = [], []
    # Parse exactly the bytes whose fingerprint is included in the receipt.
    with ZipFile(io.BytesIO(raw)) as archive:
        entries = archive.infolist()
        names = [entry.filename for entry in entries]
        if len(names) != len(set(names)):
            raise ValueError("Duplicate ZIP member names")
        if len(names) > 10000 or sum(e.file_size for e in entries) > MAX_BYTES:
            raise ValueError("Expanded DOCX exceeds inventory limits")
        if "word/document.xml" not in names:
            raise ValueError("Missing word/document.xml")
        roots = {}
        for name in names:
            if name.startswith("word/") and name.endswith((".xml", ".rels")):
                roots[name] = parse_xml(archive.read(name), name)
        document = roots["word/document.xml"]
        if document.tag != q("document") or document.find(q("body")) is None:
            raise ValueError("Unsupported document root or missing body")

        style_root = roots.get("word/styles.xml", ET.Element(q("styles")))
        styles, default_style = {}, None
        defaults = properties(style_root.find("w:docDefaults/w:pPrDefault/w:pPr", NS))
        for style in style_root.findall("w:style", NS):
            if style.get(q("type")) != "paragraph":
                continue
            sid = style.get(q("styleId"))
            if not sid or sid in styles:
                raise ValueError("Missing/duplicate paragraph style ID")
            styles[sid] = {"name": val(style.find("w:name", NS), sid),
                           "based_on": val(style.find("w:basedOn", NS)),
                           "paragraph": properties(style.find("w:pPr", NS)),
                           "run": properties(style.find("w:rPr", NS))}
            if style.get(q("default")) in ("1", "true", "on"):
                default_style = sid

        def inherited(sid, context=None):
            chain, seen = [], set()
            while sid:
                if sid in seen:
                    detail = "style inheritance cycle: " + sid
                    limits.append(detail)
                    findings.append({"kind": "broken_style_reference", "detail": detail,
                                     "view_dependent_context": context or []})
                    break
                seen.add(sid)
                if sid not in styles:
                    detail = "missing paragraph style: " + sid
                    limits.append(detail)
                    findings.append({"kind": "broken_style_reference", "detail": detail,
                                     "view_dependent_context": context or []})
                    break
                chain.append(sid)
                sid = styles[sid]["based_on"]
            effective = dict(defaults)
            for item in reversed(chain):
                effective.update(styles[item]["paragraph"])
            return chain, effective

        for sid, style in styles.items():
            style["inheritance_chain"], style["effective_paragraph"] = inherited(sid)
        number_root = roots.get("word/numbering.xml", ET.Element(q("numbering")))
        abstract = {n.get(q("abstractNumId")): n for n in number_root.findall("w:abstractNum", NS)}
        numbering = {}
        for num in number_root.findall("w:num", NS):
            aid = val(num.find("w:abstractNumId", NS))
            numbering[num.get(q("numId"))] = {"abstract_id": aid,
                "levels": {level.get(q("ilvl")): properties(level)
                           for level in (abstract[aid].findall("w:lvl", NS) if aid in abstract else [])},
                "overrides": [properties(n) for n in num.findall("w:lvlOverride", NS)]}
            if aid not in abstract:
                limits.append("missing abstract numbering: " + str(aid))
                findings.append({"kind": "broken_style_reference", "detail": "missing abstract numbering: " + str(aid)})

        part_names = [n for n in roots if re.fullmatch(
            r"word/(?:document|header[^/]*|footer[^/]*|footnotes|endnotes|comments)\.xml", n)]
        bookmarks = {n.get(q("name")) for name in part_names for n in roots[name].iter(q("bookmarkStart"))}
        stable_bookmarks = set()
        for name in part_names:
            parents = {child: parent for parent in roots[name].iter() for child in parent}
            stable_bookmarks.update(n.get(q("name")) for n in roots[name].iter(q("bookmarkStart"))
                                    if not view_context(n, parents))
        paragraphs, fields = [], []
        revision_counts, external_links = {}, []
        for name in part_names:
            root = roots[name]
            parents = {child: parent for parent in root.iter() for child in parent}
            for index, para in enumerate(root.iter(q("p")), 1):
                ancestors, cursor = [], parents.get(para)
                while cursor is not None:
                    ancestors.append(cursor.tag.rsplit("}", 1)[-1])
                    cursor = parents.get(cursor)
                ppr = para.find("w:pPr", NS)
                sid = val(para.find("w:pPr/w:pStyle", NS), default_style)
                context = view_context(para, parents)
                chain, effective = inherited(sid, context)
                direct = properties(ppr)
                effective.update(direct)
                # Do not double-count textbox child paragraphs in the outer paragraph.
                texts, run_props = [], []
                def walk(node):
                    for child in node:
                        if child.tag == q("p"):
                            continue
                        if child.tag in (q("t"), q("delText")):
                            texts.append(child.text or "")
                        if child.tag == q("rPr"):
                            run_props.append(properties(child))
                        walk(child)
                walk(para)
                outline = effective.get("outlineLvl.val")
                row = {"part": name, "paragraph": index, "text": "".join(texts),
                       "in_table": "tc" in ancestors, "in_textbox": "txbxContent" in ancestors,
                       "revision_context": [v for v in ancestors if v in ("ins", "del", "moveFrom", "moveTo")],
                       "view_dependent_context": context,
                       "style_id": sid, "style_chain": chain, "direct_paragraph": direct,
                       "effective_paragraph_subset": effective, "direct_run_properties": run_props,
                       "heading_level": int(outline) + 1 if outline in tuple(map(str, range(9))) else None}
                paragraphs.append(row)
                numid = effective.get("numPr.numId.val")
                if numid and numid != "0" and numid not in numbering:
                    findings.append({"kind": "missing_numbering", "part": name, "paragraph": index, "num_id": numid,
                                     "view_dependent_context": context})
                if row["heading_level"] and any(k.startswith("ind.") and v not in ("0", "") for k, v in direct.items()):
                    findings.append({"kind": "heading_direct_indent", "part": name, "paragraph": index,
                                     "note": "Compare with school rules; an indent is not automatically an error."})
            found, gaps, review = field_inventory(root, name, bookmarks)
            for field in found:
                if field.get("target_present") and field["target"] not in stable_bookmarks:
                    field["target_view_dependent"] = True
                    review.append({"kind": "view_dependent_field_bookmark", "part": name, "target": field["target"],
                                   "note": "Target exists only in a revision or compatibility branch; resolve the document view."})
            fields.extend(found); limits.extend(gaps); findings.extend(review)
            for tag in ("ins", "del", "moveFrom", "moveTo", "pPrChange", "rPrChange", "sectPrChange",
                        "trPrChange", "tcPrChange", "tblPrChange", "cellIns", "cellDel", "cellMerge"):
                count = len(list(root.iter(q(tag))))
                if count:
                    revision_counts[name + ":" + tag] = count
            if list(root.iter(q("altChunk"))):
                limits.append(name + ": altChunk content is not expanded")
            if list(root.iter("{" + MC + "}AlternateContent")):
                limits.append(name + ": AlternateContent branches inventoried together; consumer selection was not evaluated")
        if revision_counts:
            limits.append("Tracked revisions inventoried; text is not an accepted/final revision view")
        if not paragraphs:
            limits.append("No paragraphs found; drawing-only or unsupported content needs visual review")
        for name, root in roots.items():
            if name.endswith(".rels"):
                for rel in root:
                    if rel.get("TargetMode") == "External":
                        external_links.append({"part": name, "id": rel.get("Id"), "target": rel.get("Target"), "type": rel.get("Type")})
        rels = {n.get("Id"): n for n in roots.get("word/_rels/document.xml.rels", [])}
        sections = []
        parents = {child: parent for parent in document.iter() for child in parent}
        for index, sect in enumerate(document.iter(q("sectPr")), 1):
            context = view_context(sect, parents)
            references = []
            for tag in ("headerReference", "footerReference"):
                for node in sect.findall("w:" + tag, NS):
                    rid = node.get("{" + R + "}id")
                    rel = rels.get(rid)
                    target = rel.get("Target", "") if rel is not None else None
                    resolved = posixpath.normpath(posixpath.join("word", target)) if target else None
                    if target and target.startswith("/"):
                        resolved = target.lstrip("/")
                    exists = resolved in names if resolved else False
                    references.append({"kind": tag, "type": node.get(q("type")), "relationship": rid,
                                       "target": target, "part_exists": exists})
                    if not exists:
                        findings.append({"kind": "missing_header_footer_part", "section": index, "relationship": rid,
                                         "view_dependent_context": context})
            sections.append({"section": index, "properties": properties(sect), "references": references,
                             "view_dependent_context": context,
                             "omitted_references": "may inherit previous section; not an error by itself"})
        table_rows = [{"part": name, "row": i, "properties": properties(row.find("w:trPr", NS))}
                      for name in part_names for i, row in enumerate(roots[name].iter(q("tr")), 1)]
        if any("vbaProject" in n for n in names):
            limits.append("VBA payload present; never executed or validated")
    blocking = [item for item in findings if item["kind"] in
                {"missing_field_bookmark", "missing_numbering", "missing_header_footer_part", "broken_style_reference"}
                and not item.get("view_dependent_context")]
    return {"schema": "thesisforge.docx-audit/1", "input": str(path),
            "input_sha256": hashlib.sha256(raw).hexdigest(), "read_only": True,
            "status": "REVIEW_NEEDED" if findings or limits else "INVENTORIED",
            "coverage": {"parts": part_names, "paragraph_count": len(paragraphs),
                         "table_paragraphs": sum(p["in_table"] for p in paragraphs),
                         "rendering": "NOT_RUN", "school_compliance": "NOT_CHECKED",
                         "limits": sorted(set(limits)),
                         "not_checked": ["effective run fonts/theme and full Word cascade", "visual pagination and clipping",
                                         "field display freshness", "scientific meaning", "images, OLE and embedded documents"]},
            "styles": styles, "numbering": numbering, "sections": sections, "paragraphs": paragraphs,
            "fields": fields, "table_rows": table_rows, "tracked_changes": revision_counts,
            "external_relationships_not_followed": external_links, "review_items": findings,
            "blocking_items": blocking}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, help="New JSON file; existing files are never overwritten")
    parser.add_argument("--strict", action="store_true", help="Exit 1 for broken structural references; heuristic/coverage notes do not block")
    args = parser.parse_args(argv)
    try:
        report = audit(args.input)
        payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            with args.output.open("x", encoding="utf-8") as stream:
                stream.write(payload)
        else:
            print(payload, end="")
        return 1 if args.strict and report["blocking_items"] else 0
    except (OSError, ValueError, BadZipFile, ET.ParseError, RuntimeError) as exc:
        print(json.dumps({"status": "INPUT_ERROR", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    raise SystemExit(main())
