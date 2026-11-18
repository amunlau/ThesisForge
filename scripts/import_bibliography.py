#!/usr/bin/env python3
"""Read local BibTeX, RIS or CSL/Better BibTeX JSON without executing or fetching.

Imports preserve source keys, raw records and file fingerprints. Unsupported
BibTeX expressions are rejected, not expanded. Duplicate keys remain separate.
Exit 0: complete; 1: warnings/rejections need review; 2: input/output error.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path


class ParseProblem(ValueError):
    pass


def location(text: str, start: int, end: int) -> dict:
    return {"start": start, "end": end,
            "line": text.count("\n", 0, start) + 1,
            "end_line": text.count("\n", 0, max(start, end - 1)) + 1}


def rejected(raw: str, reason: str, **where) -> dict:
    return {"raw": raw, "reason": reason, **where}


def skip_space(text: str, pos: int) -> int:
    while pos < len(text):
        if text[pos].isspace():
            pos += 1
        elif text[pos] == "%":
            end = text.find("\n", pos)
            pos = len(text) if end < 0 else end + 1
        else:
            break
    return pos


def braced_end(text: str, start: int) -> int:
    """Find a braced literal's close; quotes within braces are literal text."""
    depth = 0
    escaped = False
    for i in range(start, len(text)):
        char = text[i]
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return i
    raise ParseProblem("unclosed_braced_value")


def quoted_end(text: str, start: int) -> int:
    depth = 0
    escaped = False
    for i in range(start + 1, len(text)):
        char = text[i]
        if escaped:
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == "{":
            depth += 1
        elif char == "}":
            if depth == 0:
                raise ParseProblem("unbalanced_quoted_value")
            depth -= 1
        elif char == '"' and depth == 0:
            return i
    raise ParseProblem("unclosed_quoted_value")


def container_end(text: str, start: int) -> int:
    close = "}" if text[start] == "{" else ")"
    pos = start + 1
    while pos < len(text):
        char = text[pos]
        if char == close:
            return pos
        if char == "{":
            pos = braced_end(text, pos) + 1
        elif char == '"':
            pos = quoted_end(text, pos) + 1
        elif char == "%":
            end = text.find("\n", pos)
            pos = len(text) if end < 0 else end + 1
        else:
            pos += 1
    raise ParseProblem("unclosed_entry; remaining_text_not_parsed")


def parse_bib_fields(body: str) -> tuple[str, dict]:
    match = re.match(r"\s*([^\s,{}()]+)\s*,", body)
    if not match:
        raise ParseProblem("missing_citation_key_or_comma")
    key = match.group(1)
    fields: dict[str, str] = {}
    pos = match.end()
    while True:
        pos = skip_space(body, pos)
        if pos >= len(body):
            break
        match = re.match(r"([A-Za-z][A-Za-z0-9_:-]*)\s*=\s*", body[pos:])
        if not match:
            raise ParseProblem("invalid_field_assignment")
        name = match.group(1).lower()
        if name in fields:
            raise ParseProblem("duplicate_field:" + name)
        pos += match.end()
        pos = skip_space(body, pos)
        if pos >= len(body):
            raise ParseProblem("missing_value:" + name)
        if body[pos] == "{":
            end = braced_end(body, pos)
            value = body[pos + 1:end]
            pos = end + 1
        elif body[pos] == '"':
            end = quoted_end(body, pos)
            value = body[pos + 1:end]
            pos = end + 1
        else:
            number = re.match(r"[0-9]+(?=\s|,|$)", body[pos:])
            if not number:
                raise ParseProblem("unsupported_macro_or_expression:" + name)
            value = number.group(0)
            pos += len(value)
        pos = skip_space(body, pos)
        if pos < len(body) and body[pos] == "#":
            raise ParseProblem("unsupported_string_concatenation:" + name)
        fields[name] = value
        if pos >= len(body):
            break
        if body[pos] != ",":
            raise ParseProblem("missing_field_separator:" + name)
        pos += 1
    if not fields:
        raise ParseProblem("entry_has_no_fields")
    return key, fields


def parse_bibtex(text: str) -> tuple[list, list, list, dict]:
    entries, rejects, notes = [], [], []
    pos = 0
    while pos < len(text):
        pos = skip_space(text, pos)
        if pos >= len(text):
            break
        start = pos
        match = re.match(r"@([A-Za-z][A-Za-z0-9_-]*)\s*([({])", text[pos:])
        if not match:
            nxt = text.find("@", pos + 1)
            pos = len(text) if nxt < 0 else nxt
            rejects.append(rejected(text[start:pos], "unparsed_text", **location(text, start, pos)))
            continue
        kind = match.group(1).lower()
        opening = pos + match.end() - 1
        try:
            end = container_end(text, opening)
        except ParseProblem as exc:
            rejects.append(rejected(text[start:], str(exc), **location(text, start, len(text))))
            break
        pos = end + 1
        raw = text[start:pos]
        where = location(text, start, pos)
        if kind == "comment":
            notes.append({"kind": "comment", "raw": raw, **where})
            continue
        if kind in {"string", "preamble"}:
            rejects.append(rejected(raw, "unsupported_directive:" + kind, **where))
            continue
        try:
            key, fields = parse_bib_fields(text[opening + 1:end])
            entries.append({"source_key": key, "type": kind, "fields": fields,
                            "raw": raw, **where})
        except ParseProblem as exc:
            rejects.append(rejected(raw, str(exc), **where))
    return entries, rejects, [], {"comments": notes,
        "coverage": "static literal fields; no macro expansion, concatenation, TeX execution or metadata verification"}


def parse_ris(text: str) -> tuple[list, list, list, dict]:
    entries, rejects, warnings = [], [], []
    active: dict | None = None
    offset = 0
    tag_pattern = re.compile(r"^([A-Z0-9]{2})[ \t]{2}-[ \t]?(.*)$")

    def finish(end: int, error: str | None = None) -> None:
        nonlocal active
        if active is None:
            return
        raw = text[active["start"]:end]
        where = location(text, active["start"], end)
        reasons = active["errors"] + ([error] if error else [])
        if reasons:
            rejects.append(rejected(raw, "; ".join(reasons), **where))
        else:
            fields = active["fields"]
            keys = fields.get("ID", [])
            entries.append({"source_key": keys[0] if keys else None,
                            "type": fields["TY"][0], "fields": fields, "raw": raw, **where})
            if len(keys) > 1:
                warnings.append({"reason": "multiple_RIS_ID_values", **where})
        active = None

    for line in text.splitlines(keepends=True):
        body = line.rstrip("\r\n")
        match = tag_pattern.match(body)
        if match and match.group(1) == "TY":
            if active is not None:
                finish(offset, "missing_ER_before_next_TY")
            active = {"start": offset, "fields": {"TY": [match.group(2)]},
                      "last_tag": "TY", "errors": [] if match.group(2).strip() else ["empty_RIS_type"]}
        elif match and match.group(1) == "ER":
            if active is None:
                rejects.append(rejected(line, "ER_without_TY", **location(text, offset, offset + len(line))))
            else:
                if match.group(2).strip():
                    active["errors"].append("nonempty_ER")
                finish(offset + len(line))
        elif active is not None and match:
            tag, value = match.groups()
            active["fields"].setdefault(tag, []).append(value)
            active["last_tag"] = tag
        elif active is not None and body and body[0].isspace():
            active["fields"][active["last_tag"]][-1] += "\n" + body
        elif body.strip():
            if active is None:
                rejects.append(rejected(line, "text_outside_RIS_record", **location(text, offset, offset + len(line))))
            else:
                active["errors"].append("unrecognized_RIS_line:" + str(text.count("\n", 0, offset) + 1))
        offset += len(line)
    if active is not None:
        finish(len(text), "missing_ER_at_end")
    return entries, rejects, warnings, {"coverage": "TY/ER-delimited RIS; repeated tags and indented continuation lines preserved"}


def parse_json(text: str) -> tuple[list, list, list, dict]:
    duplicate_keys: list[str] = []

    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                duplicate_keys.append(key)
            result[key] = value
        return result

    def reject_constant(value):
        raise ValueError("nonfinite_JSON_constant:" + value)

    def finite_float(value):
        parsed = float(value)
        if not math.isfinite(parsed):
            raise ValueError("nonfinite_JSON_number:" + value)
        return parsed

    try:
        obj = json.loads(text, object_pairs_hook=pairs, parse_constant=reject_constant,
                         parse_float=finite_float)
    except (ValueError, RecursionError) as exc:
        return [], [rejected(text, "invalid_JSON:" + str(exc))], [], {}
    if duplicate_keys:
        return [], [rejected(text, "duplicate_JSON_keys:" + ",".join(duplicate_keys))], [], {}
    metadata = {}
    if isinstance(obj, list):
        items, prefix = obj, ""
    elif isinstance(obj, dict) and isinstance(obj.get("items"), list):
        items, prefix = obj["items"], "/items"
        metadata = {key: value for key, value in obj.items() if key != "items"}
    else:
        return [], [rejected(text, "expected_CSL_list_or_object_with_items_list")], [], {}
    entries, rejects, warnings = [], [], []
    for i, item in enumerate(items):
        pointer = f"{prefix}/{i}"
        if not isinstance(item, dict) or not item:
            rejects.append({"json_pointer": pointer, "raw_object": item,
                            "reason": "entry_must_be_nonempty_object"})
            continue
        key = item.get("citationKey", item.get("id", item.get("key")))
        if key is not None and (isinstance(key, bool) or not isinstance(key, (str, int))):
            warnings.append({"json_pointer": pointer, "reason": "non_scalar_source_key"})
            key = None
        entries.append({"source_key": str(key) if key is not None else None,
                        "type": item.get("type", item.get("itemType")),
                        "fields": item, "raw_object": item, "json_pointer": pointer})
    return entries, rejects, warnings, {"container_metadata": metadata,
        "coverage": "CSL list or Better BibTeX items; parsed objects preserved, original source bytes authoritative"}


PARSERS = {"bibtex": parse_bibtex, "ris": parse_ris, "json": parse_json}


def field_value(fields: dict, name: str):
    """Case-insensitive original field/tag lookup, without changing source data."""
    return next((value for key, value in fields.items() if key.casefold() == name.casefold()), None)


def text_values(value) -> str:
    if isinstance(value, dict):
        return " ".join(text_values(item) for item in value.values())
    if isinstance(value, list):
        return " ".join(text_values(item) for item in value)
    return "" if value is None else str(value)


def bibliographic_year(fields: dict) -> tuple[int | None, str | None]:
    issued = field_value(fields, "issued")
    if isinstance(issued, dict):
        parts = issued.get("date-parts")
        if (isinstance(parts, list) and parts and isinstance(parts[0], list) and parts[0]
                and isinstance(parts[0][0], int) and not isinstance(parts[0][0], bool)):
            return parts[0][0], "issued.date-parts[0][0]"
    for name in ("year", "PY", "Y1", "date"):
        value = field_value(fields, name)
        if isinstance(value, list):
            value = value[0] if value else None
        if isinstance(value, (str, int)) and not isinstance(value, bool):
            match = re.match(r"^\s*([0-9]{4})(?=$|[-/ ])", str(value))
            if match:
                return int(match.group(1)), name
    return None, None


def author_text(fields: dict) -> str:
    values = [field_value(fields, name) for name in ("author", "AU", "A1")]
    creators = field_value(fields, "creators")
    if isinstance(creators, list):
        values.extend(item for item in creators
                      if isinstance(item, dict) and item.get("creatorType") == "author")
    return text_values(values).strip()


def query_entries(entries: list, *, query: str | None = None, field: str | None = None,
                  author: str | None = None, year_from: int | None = None,
                  year_to: int | None = None) -> dict:
    """Return a view with explicit exclusions; never delete imported records."""
    matched, excluded = [], []
    for entry in entries:
        fields = entry["fields"]
        reasons = []
        year, year_basis = bibliographic_year(fields)
        if query is not None:
            value = field_value(fields, field) if field else fields
            if value is None:
                reasons.append("field_missing")
            elif query.casefold() not in text_values(value).casefold():
                reasons.append("keyword_not_matched")
        if author is not None:
            authors = author_text(fields)
            if not authors:
                reasons.append("author_missing")
            elif author.casefold() not in authors.casefold():
                reasons.append("author_not_matched")
        if year_from is not None or year_to is not None:
            if year is None:
                reasons.append("year_unavailable")
            elif (year_from is not None and year < year_from) or (year_to is not None and year > year_to):
                reasons.append("year_out_of_range")
        result = {"entry_id": entry["id"], "source_key": entry["source_key"],
                  "year": year, "year_basis": year_basis}
        if reasons:
            excluded.append({**result, "reasons": reasons})
        else:
            matched.append(result)
    return {"status": "MATCHES" if matched else "NO_MATCHES",
            "criteria": {"keyword": query, "field": field, "author": author,
                         "year_from": year_from, "year_to": year_to},
            "matching": "case-insensitive literal substring, criteria combined with AND; no fuzzy or TeX normalization",
            "source_entry_count": len(entries), "matched_count": len(matched),
            "matches": matched, "excluded": excluded}


def import_files(paths: list[Path], fmt: str = "auto", encoding: str = "utf-8-sig") -> dict:
    files, all_entries, rejects, warnings = [], [], [], []
    for number, path in enumerate(paths, 1):
        resolved = path.resolve(strict=True)
        if not resolved.is_file():
            raise ValueError("not_a_file:" + str(path))
        raw = resolved.read_bytes()
        text = raw.decode(encoding, errors="strict")
        selected = fmt
        if selected == "auto":
            selected = {".bib": "bibtex", ".bibtex": "bibtex", ".ris": "ris", ".json": "json"}.get(resolved.suffix.lower(), "")
            if not selected:
                raise ValueError("unknown_extension; select --format:" + str(path))
        source_id = f"source-{number}"
        entries, bad, alerts, details = PARSERS[selected](text)
        if not text.strip():
            bad.append(rejected(text, "empty_input"))
        elif not entries and not bad:
            alerts.append({"reason": "no_bibliographic_entries"})
        for entry in entries:
            entry["id"] = f"entry-{len(all_entries) + 1}"
            entry["source_id"] = source_id
            all_entries.append(entry)
        rejects.extend(dict(item, source_id=source_id) for item in bad)
        warnings.extend(dict(item, source_id=source_id) for item in alerts)
        files.append({"id": source_id, "path": str(resolved), "format": selected,
                      "encoding": encoding, "bytes": len(raw),
                      "sha256": hashlib.sha256(raw).hexdigest(), "imported": len(entries),
                      "rejected": len(bad), "parser_details": details})
    by_key: dict[str, list[str]] = {}
    for entry in all_entries:
        if entry["source_key"] is not None:
            by_key.setdefault(entry["source_key"], []).append(entry["id"])
    duplicates = [{"source_key": key, "entry_ids": ids} for key, ids in by_key.items() if len(ids) > 1]
    needs_review = bool(rejects or warnings or duplicates)
    return {"schema_version": 1, "status": "REVIEW_NEEDED" if needs_review else "COMPLETE",
            "scope": "Local bibliographic import only; not identity, citation-support, peer-review or scientific verification.",
            "sources": files, "entries": all_entries, "rejections": rejects,
            "warnings": warnings, "duplicate_source_keys": duplicates,
            "summary": {"sources": len(files), "imported": len(all_entries),
                        "rejected": len(rejects), "warnings": len(warnings),
                        "duplicate_key_groups": len(duplicates)}}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path, help="Explicit local bibliography files; folders and URLs are not fetched.")
    parser.add_argument("--output", required=True, type=Path, help="New UTF-8 JSON report. Existing files are never overwritten.")
    parser.add_argument("--format", choices=["auto", *PARSERS], default="auto")
    parser.add_argument("--encoding", choices=["utf-8-sig", "gb18030"], default="utf-8-sig", help="Strict decoding; select GB18030 explicitly for older Chinese files.")
    parser.add_argument("--query", help="Optional case-insensitive literal keyword in values, not field names.")
    parser.add_argument("--field", help="Restrict --query to this original field/tag (case-insensitive); e.g. title or TI.")
    parser.add_argument("--author", help="Optional author substring; BibTeX author, RIS AU/A1, CSL author, BBT author creators.")
    parser.add_argument("--year", type=int, help="Optional exact publication year.")
    parser.add_argument("--year-from", type=int, help="Inclusive year lower bound.")
    parser.add_argument("--year-to", type=int, help="Inclusive year upper bound.")
    args = parser.parse_args(argv)
    try:
        if args.field is not None and args.query is None:
            raise ValueError("--field_requires_--query")
        if any(value is not None and not value.strip() for value in (args.query, args.field, args.author)):
            raise ValueError("empty_query_field_or_author; omit filters to import all entries")
        if args.year is not None and (args.year_from is not None or args.year_to is not None):
            raise ValueError("--year_cannot_be_combined_with_year_range")
        year_from = args.year if args.year is not None else args.year_from
        year_to = args.year if args.year is not None else args.year_to
        if any(value is not None and not 1 <= value <= 9999 for value in (year_from, year_to)):
            raise ValueError("year_outside_1_to_9999")
        if year_from is not None and year_to is not None and year_from > year_to:
            raise ValueError("year_range_reversed")
        if args.output.exists():
            raise FileExistsError("output_already_exists:" + str(args.output))
        report = import_files(args.inputs, args.format, args.encoding)
        query_summary = {}
        if any(value is not None for value in (args.query, args.author, year_from, year_to)):
            report["query"] = query_entries(report["entries"], query=args.query, field=args.field,
                                           author=args.author, year_from=year_from, year_to=year_to)
            query_summary = {"query_status": report["query"]["status"],
                             "matched": report["query"]["matched_count"]}
        serialized = json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
        with args.output.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(serialized)
        print(json.dumps({"status": report["status"], "output": str(args.output.resolve()),
                          **report["summary"], **query_summary}, ensure_ascii=True))
        return 1 if report["status"] == "REVIEW_NEEDED" else 0
    except (OSError, ValueError, RecursionError) as exc:
        print(json.dumps({"status": "ERROR", "error": str(exc)}, ensure_ascii=True), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
