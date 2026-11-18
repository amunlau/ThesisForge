#!/usr/bin/env python3
"""Read-only manuscript inventory and bounded structural checks (stdlib, Python 3.9+)."""

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re
import sys


LIMIT_BYTES = 8 * 1024 * 1024
CODE_ENV = r"verbatim\*?|Verbatim|lstlisting|minted"
MATH_ENV = r"equation\*?|align\*?|alignat\*?|gather\*?|multline\*?|displaymath"
STRUCTURE = re.compile(r"\\(?P<cmd>input|include|subfile|bibliography|addbibresource|bibitem|label|ref|eqref|pageref|autoref|cref|Cref|cite|citep|citet|autocite|parencite|textcite|nocite)\*?(?:\s*\[[^\]\n]*\])*\s*\{(?P<value>[^{}\n]*)\}")
WORD = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]+(?:['’\-][A-Za-zÀ-ÖØ-öø-ÿ]+)*|\d+(?:[.,]\d+)*")
HAN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\U00020000-\U0002fa1f]")
UNIT = r"(?:ns|us|µs|μs|ms|s|min|h|Hz|kHz|MHz|GHz|W|mW|uW|µW|J|mJ|nJ|pJ|V|mV|A|mA|B|KB|MB|GB|KiB|MiB|GiB|bit|bits|byte|bytes|flit|flits|packet|packets|cycle|cycles|%|‰|百分点|百分比)"
NUMBER = r"(?:\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?|\.\d+)(?:[eE][+−-]?\d+)?"
QUANTITY = re.compile(r"(?<![A-Za-z0-9_.,])(?:(?:<=|>=|[<>≤≥=])\s*)?[+−-]?" + NUMBER + r"[ \t]*" + UNIT + r"(?![A-Za-z0-9_])")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: " + key)
        result[key] = value
    return result


def mask_range(chars, start, end):
    for i in range(start, end):
        if chars[i] not in "\r\n":
            chars[i] = "\0"


def clean_source(text, tex):
    """Keep offsets stable; neither execute macros nor read TeX-declared resources."""
    chars = list(text)
    if tex:
        # Resolve comments and verbatim spans in source order: a percent sign
        # inside \verb is data and must not hide live references later on the line.
        cursor = 0
        tokens = re.compile(r"%|\\begin\{(?P<env>" + CODE_ENV + r")\}|\\verb\*?(?P<delimiter>[^\w\s])")
        for m in tokens.finditer(text):
            if m.start() < cursor:
                continue
            backslashes = len(text[:m.start()]) - len(text[:m.start()].rstrip("\\"))
            if backslashes % 2:
                continue
            if m.group() == "%":
                end = text.find("\n", m.start())
                cursor = len(text) if end < 0 else end
            elif m["env"]:
                closing = "\\end{" + m["env"] + "}"
                end = text.find(closing, m.end())
                if end < 0:
                    continue  # Kept visible; source() reports unsupported code coverage.
                cursor = end + len(closing)
            else:
                end = text.find(m["delimiter"], m.end())
                newline = text.find("\n", m.end())
                if end < 0 or (newline >= 0 and newline < end):
                    continue
                cursor = end + 1
            mask_range(chars, m.start(), cursor)
    else:
        fence = None
        for m in re.finditer(r".*(?:\n|$)", text):
            line = m.group()
            marker = re.match(r" {0,3}(`{3,}|~{3,})", line)
            if fence:
                mask_range(chars, m.start(), m.end())
                if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence):
                    fence = None
            elif marker:
                fence = marker[1]
                mask_range(chars, m.start(), m.end())
        for m in re.finditer(r"`[^`\n]+`|<!--.*?-->", text, re.S):
            mask_range(chars, m.start(), m.end())
    return "".join(chars)


def prose_view(cleaned, tex):
    chars = list(cleaned)
    patterns = [r"\$\$.*?\$\$", r"(?<!\\)\$(?!\$).*?(?<!\\)\$", r"\\\[.*?\\\]", r"\\\(.*?\\\)",
                r"\\begin\{(" + MATH_ENV + r")\}.*?\\end\{\1\}"]
    for pattern in patterns:
        for m in re.finditer(pattern, cleaned, re.S):
            mask_range(chars, m.start(), m.end())
    if tex:
        for m in STRUCTURE.finditer(cleaned):
            mask_range(chars, m.start(), m.end())
        for m in re.finditer(r"\\(?:begin|end)\{[^{}]*\}|\\includegraphics(?:\[[^\]]*\])?\{[^{}]*\}", cleaned):
            mask_range(chars, m.start(), m.end())
        for m in re.finditer(r"\\[A-Za-z@]+\*?", cleaned):
            mask_range(chars, m.start(), m.end())
        for i, char in enumerate(chars):
            if char in "{}":
                chars[i] = "\0"
    return "".join(chars)


def quantities(text):
    return [(m.group(), m.start(), m.end()) for m in QUANTITY.finditer(text)]


class Audit:
    def __init__(self, root, encoding):
        self.root = root.resolve()
        self.encoding = encoding
        self.files = {}
        self.findings = []
        self.coverage = []
        self.labels = defaultdict(list)
        self.references = []
        self.citations = []
        self.bib_keys = defaultdict(list)
        self.bib_loaded = False
        self.dynamic = False
        self.active = set()
        self.prose = {}

    def position(self, path, text, start, end):
        return {"file": str(path), "line": text.count("\n", 0, start) + 1,
                "column": start - text.rfind("\n", 0, start), "start": start, "end": end,
                "excerpt": text[max(0, start - 35):min(len(text), end + 60)].strip()}

    def add(self, level, code, note, position=None):
        item = {"level": level, "code": code, "note": note}
        if position:
            item["location"] = position
        self.findings.append(item)

    def read(self, path):
        path = path.resolve()
        try:
            path.relative_to(self.root)
        except ValueError:
            raise ValueError("source is outside --root (including symlinks): " + str(path))
        if not path.is_file():
            raise ValueError("not a regular readable source: " + str(path))
        if path.stat().st_size > LIMIT_BYTES:
            raise ValueError("source exceeds 8 MiB limit: " + str(path))
        raw = path.read_bytes()
        text = raw.decode(self.encoding)
        if not text.strip() or "\x00" in text:
            raise ValueError("empty or binary-like source: " + str(path))
        self.files[str(path)] = {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw), "encoding": self.encoding}
        return text

    def resource(self, value, suffix, parent):
        rel = Path(value)
        if not rel.suffix:
            rel = rel.with_suffix(suffix)
        # TeX normally searches relative to its working directory, not each include.
        target = self.root / rel
        if not target.exists() and (parent / rel).exists():
            target = parent / rel
            self.coverage.append("include resolved relative to containing file; verify build search path: " + str(target))
        target = target.resolve()
        try:
            target.relative_to(self.root)
        except ValueError:
            raise ValueError("declared resource leaves --root: " + str(target))
        return target

    def bibliography(self, path):
        if str(path) in self.files:
            return
        text = self.read(path)
        self.bib_loaded = True
        # Consume complete entries so @ inside a braced comment is not a new item.
        cursor = 0
        entry = re.compile(r"(?P<comment>%[^\r\n]*)|@(?P<kind>[A-Za-z]+)\s*(?P<opener>[({])")
        while True:
            m = entry.search(text, cursor)
            if not m:
                break
            if m["comment"] is not None:
                cursor = m.end()
                continue
            opener = m["opener"]; closer = "}" if opener == "{" else ")"
            depth = 1; quote = False; i = m.end()
            while i < len(text) and depth:
                if text[i] == "\\":
                    i += 2; continue
                if text[i] == '"':
                    quote = not quote
                if not quote:
                    if text[i] == opener: depth += 1
                    elif text[i] == closer: depth -= 1
                i += 1
            if depth:
                self.coverage.append("incomplete bibliography entry: " + str(path))
                self.dynamic = True
                break
            if m["kind"].lower() not in {"comment", "preamble", "string"}:
                key = re.match(r"\s*([^\s,{}()]+)\s*,", text[m.end():i - 1])
                if key:
                    start = m.end() + key.start(1)
                    self.bib_keys[key[1]].append(self.position(path, text, start, start + len(key[1])))
                else:
                    self.coverage.append("unparsed bibliography entry: " + str(path))
                    self.dynamic = True
            cursor = i

    def source(self, path, tex_context=False):
        path = path.resolve()
        if path in self.active:
            self.add("error", "include_cycle", "literal include cycle", {"file": str(path)})
            return
        if str(path) in self.files:
            self.coverage.append("repeated include counted once: " + str(path))
            return
        if len(self.files) >= 100:
            raise ValueError("source graph exceeds 100 files")
        text = self.read(path)
        # TeX \input does not infer language from an included file's extension.
        tex = tex_context or path.suffix.lower() == ".tex"
        cleaned = clean_source(text, tex)
        self.prose[path] = (text, prose_view(cleaned, tex))
        if not tex:
            return
        if re.search(r"\\(?:newcommand|renewcommand|providecommand|DeclareRobustCommand|"
                     r"(?:New|Renew|Provide|Declare)Document(?:Command|Environment)|newenvironment|renewenvironment|"
                     r"[gex]?def|let|futurelet|csname|ExplSyntaxOn|includeonly|externaldocument|if\w*|catcode|input\s+[^\s{])\b", cleaned):
            self.dynamic = True
            self.coverage.append("macros, conditionals or unsupported input may change structure: " + str(path))
        if re.search(r"\\begin\{(" + CODE_ENV + r")\}", cleaned):
            self.coverage.append("unclosed or unsupported code environment: " + str(path))
        matches = list(STRUCTURE.finditer(cleaned))
        recognized = {m.start() for m in matches}
        for occurrence in re.finditer(r"\\(?:input|include|subfile|bibliography|addbibresource|bibitem|label|ref|eqref|pageref|autoref|cref|Cref|cite|citep|citet|autocite|parencite|textcite|nocite)\b", cleaned):
            preceding = len(cleaned[:occurrence.start()]) - len(cleaned[:occurrence.start()].rstrip("\\"))
            if not preceding % 2 and occurrence.start() not in recognized:
                self.dynamic = True
                self.coverage.append("unsupported structural argument at " + str(path) + ":" + str(text.count("\n", 0, occurrence.start()) + 1))
        self.active.add(path)
        for m in matches:
            preceding_slashes = len(cleaned[:m.start()]) - len(cleaned[:m.start()].rstrip("\\"))
            if preceding_slashes % 2:
                continue
            cmd, value = m["cmd"], m["value"].strip()
            loc = self.position(path, text, m.start(), m.end())
            if not value or "\\" in value or "#" in value:
                self.dynamic = True
                self.coverage.append("dynamic or empty structural argument at " + str(path) + ":" + str(loc["line"]))
                continue
            if cmd in {"input", "include", "subfile", "bibliography", "addbibresource"}:
                for token in value.split(",") if cmd == "bibliography" else [value]:
                    bib = cmd in {"bibliography", "addbibresource"}
                    target = self.resource(token.strip(), ".bib" if bib else ".tex", path.parent)
                    if not target.exists():
                        self.add("review", "missing_resource", "literal resource not found; may be generated or conditional: " + str(target), loc)
                        self.coverage.append("source graph incomplete: " + str(target))
                        self.dynamic = True
                    elif bib:
                        self.bibliography(target)
                    else:
                        self.source(target, tex_context=True)
            elif cmd == "label":
                self.labels[value].append(loc)
            elif cmd == "bibitem":
                self.bib_loaded = True
                self.bib_keys[value].append(loc)
            elif "cite" in cmd:
                self.citations.extend((v.strip(), loc) for v in value.split(",") if v.strip() != "*")
            elif cmd in {"cref", "Cref"}:
                self.references.extend((v.strip(), loc) for v in value.split(","))
            else:
                self.references.append((value, loc))
        self.active.remove(path)

    def check_structure(self):
        level = "review" if self.dynamic else "error"
        if self.dynamic:
            for item in self.findings:
                if item["code"] == "include_cycle":
                    item.update(level="review", note="literal include cycle in a dynamic source graph; execution was not evaluated")
        for key, positions in self.labels.items():
            if len(positions) > 1:
                self.add(level, "duplicate_label", "label occurs more than once: " + key, positions[-1])
        for key, loc in self.references:
            if key not in self.labels:
                self.add(level, "unresolved_reference", "no literal label in loaded source graph: " + key, loc)
        for key, positions in self.bib_keys.items():
            if len(positions) > 1:
                self.add(level, "duplicate_bib_key", "bibliography key occurs more than once: " + key, positions[-1])
        for key, loc in self.citations:
            if key not in self.bib_keys:
                self.add(level if self.bib_loaded else "review", "unresolved_citation", "no matching key in loaded bibliographies or literal bibitem entries: " + key, loc)
        if self.citations and not self.bib_loaded:
            self.coverage.append("no bibliography or literal bibitem loaded; generated/external libraries require review")


def load_terms(path):
    data = json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=unique_object)
    if not isinstance(data, dict) or set(data) != {"terms"} or not isinstance(data["terms"], list):
        raise ValueError("term map must contain a terms array")
    ids = set()
    for item in data["terms"]:
        if not isinstance(item, dict) or set(item) != {"id", "relation", "variants"}:
            raise ValueError("each term requires id, relation and variants only")
        if not isinstance(item["id"], str) or not item["id"].strip() or item["id"] in ids:
            raise ValueError("term IDs must be unique nonempty strings")
        ids.add(item["id"])
        if item["relation"] not in {"equivalent", "preference", "distinct"}:
            raise ValueError("term relation must be equivalent, preference or distinct")
        values = item["variants"]
        if not isinstance(values, list) or len(values) < 2 or any(not isinstance(v, str) or not v.strip() for v in values) or len(set(values)) != len(values):
            raise ValueError("term variants require at least two distinct nonempty strings")
    return data["terms"]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="UTF-8 .txt/.md or literal multi-file .tex entry")
    parser.add_argument("--root", type=Path, help="allowed project root and TeX resource search directory (default input parent)")
    parser.add_argument("--encoding", choices=["utf-8-sig", "gb18030"], default="utf-8-sig")
    parser.add_argument("--bib", type=Path, action="append", default=[], help="additional local bibliography; relative to invocation directory")
    parser.add_argument("--terms", type=Path, help="JSON term relation map; hints never rewrite text")
    parser.add_argument("--before", type=Path, help="compare literal number-unit pairs against a same-scope original; no semantic guarantee")
    parser.add_argument("--limit-words", type=int, help="limit mixed Latin/numeric tokens plus Han characters in loaded prose")
    parser.add_argument("--limit-chars", type=int, help="limit retained source characters including spaces, excluding line breaks")
    parser.add_argument("--per-line", action="store_true", help="apply limits separately to nonempty physical lines")
    parser.add_argument("--abbreviations", action="store_true", help="heuristic first-use uppercase abbreviation hints")
    parser.add_argument("--strict", action="store_true", help="exit 1 only for deterministic structure/length findings; review hints remain 0")
    parser.add_argument("--json", action="store_true", help="emit machine-readable report (default is also JSON)")
    args = parser.parse_args(argv)
    try:
        if any(v is not None and v < 0 for v in [args.limit_words, args.limit_chars]):
            raise ValueError("limits must be nonnegative")
        if args.input.suffix.lower() not in {".txt", ".md", ".tex"}:
            raise ValueError("supported sources: .txt, .md, .tex; export other formats with a declared coverage boundary")
        root = args.root or args.input.resolve().parent
        audit = Audit(root, args.encoding)
        audit.source(args.input)
        for bib in args.bib:
            audit.bibliography(bib.resolve())
        audit.check_structure()
        terms = load_terms(args.terms) if args.terms else []
        counts = []; totals = {"mixed_words": 0, "characters_including_spaces": 0}
        term_occurrences = defaultdict(list)
        for path, (original, prose) in audit.prose.items():
            scan = prose.replace("\0", " ")
            chunks = list(re.finditer(r"[^\n]+", prose)) if args.per_line else [re.match(r"[\s\S]*", prose)]
            for chunk in chunks:
                visible = chunk.group().replace("\0", "").replace("\r", "").replace("\n", "")
                if not visible.strip(): continue
                count = {"mixed_words": len(WORD.findall(chunk.group().replace("\0", " "))) + len(HAN.findall(chunk.group())), "characters_including_spaces": len(visible)}
                loc = audit.position(path, original, chunk.start(), chunk.end())
                counts.append(dict(count, file=str(path), line=loc["line"]))
                for name in totals: totals[name] += count[name]
                if args.per_line:
                    for name, limit in [("mixed_words", args.limit_words), ("characters_including_spaces", args.limit_chars)]:
                        if limit is not None and count[name] > limit:
                            audit.add("error", "length_limit", name + " exceeds supplied limit", loc)
            for item in terms:
                found = []
                occupied = set()
                for variant in sorted(item["variants"], key=len, reverse=True):
                    pattern = (r"(?<![A-Za-z0-9_])" if variant[0].isascii() and variant[0].isalnum() else "") + re.escape(variant) + (r"(?![A-Za-z0-9_])" if variant[-1].isascii() and variant[-1].isalnum() else "")
                    for m in re.finditer(pattern, scan):
                        if occupied.intersection(range(m.start(), m.end())): continue
                        occupied.update(range(m.start(), m.end()))
                        found.append((variant, audit.position(path, original, m.start(), m.end())))
                term_occurrences[item["id"]].extend(found)
            if args.abbreviations:
                seen = set()
                for m in re.finditer(r"\b[A-Z][A-Z0-9]{1,7}\b", scan):
                    if m.group() in seen: continue
                    seen.add(m.group())
                    if not (scan[max(0, m.start()-1):m.start()] in {"(", "（"} and scan[m.end():m.end()+1] in {")", "）"}):
                        audit.add("review", "abbreviation_first_use", "first uppercase occurrence is not parenthesized; check this section's definitions: " + m.group(), audit.position(path, original, m.start(), m.end()))
        for item in terms:
            found = term_occurrences[item["id"]]
            if len({v for v, _ in found}) > 1:
                audit.add("review", "term_cooccurrence", item["id"] + ": " + item["relation"] + "; definitions determine whether any edit is appropriate", found[0][1])
                audit.findings[-1]["occurrences"] = [{"variant": v, **loc} for v, loc in found]
        if not args.per_line:
            for name, limit in [("mixed_words", args.limit_words), ("characters_including_spaces", args.limit_chars)]:
                if limit is not None and totals[name] > limit:
                    audit.add("error", "length_limit", name + " exceeds supplied limit across unique loaded source files")
        if args.before:
            if len(audit.prose) != 1:
                raise ValueError("--before requires a single-file selection, not an expanded source graph")
            if args.before.resolve() == args.input.resolve():
                raise ValueError("--before and input must be different files")
            before = audit.read(args.before)
            after = audit.prose[args.input.resolve()][0]
            from collections import Counter
            previous, current = Counter(q[0] for q in quantities(before)), Counter(q[0] for q in quantities(after))
            if previous != current:
                audit.add("review", "quantity_difference", "literal number-unit pairs changed; normalize only after checking scope and meaning")
                audit.findings[-1].update(removed=dict(previous-current), added=dict(current-previous), before_locations=[audit.position(args.before.resolve(), before, s, e) for _, s, e in quantities(before)], after_locations=[audit.position(args.input.resolve(), after, s, e) for _, s, e in quantities(after)])
            audit.coverage.append("quantity comparison covers a finite unit list and plain/scientific numbers with optional comma thousands grouping; other locale separators may be omitted; identical multisets do not preserve ownership, formulas, interval semantics or claim strength")
        if not totals["mixed_words"] and not totals["characters_including_spaces"]:
            audit.coverage.append("no prose counted; semantic content may be in excluded math, code or unsupported constructs")
        errors = sum(f["level"] == "error" for f in audit.findings)
        report = {"schema": 1, "status": "ERRORS_FOUND" if errors else "REVIEW_NEEDED" if audit.findings else "NO_FINDINGS_WITHIN_COVERAGE", "files": audit.files, "counts": counts, "totals": totals, "counting": "Latin words/numeric tokens + individual Han characters; unique physical sources; retained source characters include spaces, exclude line breaks; formulas/code/citation commands are excluded, other markup may remain; not a rendered-text or journal portal algorithm", "findings": audit.findings, "coverage_notes": sorted(set(audit.coverage)), "not_checked": ["scientific validity", "citation support", "semantic fidelity", "mathematical symbol definitions", "tense", "rendered pages", "dynamic TeX execution"], "read_only": True}
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1 if args.strict and errors else 0
    except (ValueError, OSError, UnicodeError, TypeError, RecursionError) as exc:
        print(json.dumps({"status": "INPUT_ERROR", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    for stream in [sys.stdout, sys.stderr]:
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="strict")
    sys.exit(main())
