#!/usr/bin/env python3
"""比较两个 UTF-8 文本中数值和指定片段的出现次数。"""

import argparse
from collections import Counter
from html import unescape
from pathlib import Path
import re
import sys


HSPACE = r"[^\S\r\n]*"
DIGITS = r"\d+"
SCRIPT_VALUE = rf"(?:[+-]{DIGITS}|{DIGITS}[+-]?|[+-])"
SCRIPT = rf"[_^]\{{{SCRIPT_VALUE}\}}"
MANTISSA = r"(?:\d+(?:\.\d+)?|\.\d+)"
DECIMAL = rf"{MANTISSA}(?:[Ee][+-]?{DIGITS})?"
RELATION = r"[<>=≤≥≠≈≪≫]"
NUMBER = re.compile(
    rf"(?:({RELATION}){HSPACE})?"
    rf"(?:([+±∓-]){HSPACE})?"
    rf"({DECIMAL}(?:{SCRIPT})*|(?:{SCRIPT})+)"
    rf"(?:{HSPACE}([%‰‱]))?"
)
RIGHT_RELATION = re.compile(rf"{HSPACE}({RELATION})")

SYMBOLS = str.maketrans("−＋－＜＞＝％！", "-+-<>=%!")
COMMANDS = {
    "le": "≤", "leq": "≤", "leqslant": "≤", "lt": "<",
    "ge": "≥", "geq": "≥", "geqslant": "≥", "gt": ">",
    "ne": "≠", "neq": "≠", "approx": "≈", "ll": "≪", "gg": "≫",
    "pm": "±", "mp": "∓",
}
SUPER = "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻"
SUB = "₀₁₂₃₄₅₆₇₈₉₊₋"
SCRIPT_DIGITS = str.maketrans(SUPER + SUB, "0123456789+-" * 2)
UNICODE_SCRIPT = re.compile(rf"[{SUPER}]+|[{SUB}]+")
HTML_SCRIPT = re.compile(
    rf"""<(?P<tag>sup|sub)\b(?P<attrs>(?:[^>"']|"[^"]*"|'[^']*')*)>
        \s*(?P<value>{SCRIPT_VALUE})\s*</(?P=tag)\s*>""",
    re.IGNORECASE | re.VERBOSE,
)
INLINE_TAG = re.compile(
    r"""<(?P<end>/?)(?P<tag>em|strong|i|b|span|mark|u|small)(?=[\s>])"""
    r"""(?P<attrs>(?:[^<>"']|"[^"]*"|'[^']*')*)>""", re.IGNORECASE,
)
TEX_SCRIPT = re.compile(rf"([_^])(?:\{{\s*({SCRIPT_VALUE})\s*\}}|([0-9]))")

QUOTE = re.compile(r" {0,3}>[ \t]?")
BULLET = re.compile(r"^( {0,3})[-+*][ \t]+")
FENCE = re.compile(r" {0,3}(`{3,}|~{3,})(.*)")
MATH_OPEN = re.compile(
    r" {0,3}(\$\$|\\\[|\\\(|"
    r"\\begin\{(?:equation|align(?:ed)?(?:at)?|gather(?:ed)?|multline[d]?|flalign|"
    r"displaymath|eqnarray|[dr]?cases|split|[pbBvV]?matrix|smallmatrix|array)\*?\})"
)


def markdown_body(text):
    """Remove list and quote markers while retaining signs inside math and code."""
    lines = []
    fence_end = None
    math_end = None
    block_depth = 0
    for line in text.splitlines():
        depth = 0
        while not (fence_end or math_end) or depth < block_depth:
            quote = QUOTE.match(line)
            if not quote:
                break
            line = line[quote.end():]
            depth += 1

        if depth < block_depth:
            fence_end = math_end = None
        if fence_end:
            if fence_end.fullmatch(line):
                fence_end = None
        elif math_end:
            if math_end in line:
                math_end = None
        else:
            line = BULLET.sub(r"\1", line, count=1)
            fence = FENCE.fullmatch(line)
            if fence and not (fence[1][0] == "`" and "`" in fence[2]):
                run = fence[1]
                fence_end = re.compile(rf" {{0,3}}{run[0]}{{{len(run)},}}[ \t]*")
            else:
                opener = MATH_OPEN.match(line)
                if opener:
                    token = opener[1]
                    closer = {"$$": "$$", r"\[": r"\]", r"\(": r"\)"}.get(
                        token, token.replace(r"\begin", r"\end")
                    )
                    if closer not in line[opener.end():]:
                        math_end = closer
            block_depth = depth if fence_end or math_end else 0
        lines.append(line)
    return "\n".join(lines)


def typeset_numbers(text):
    # Only paired presentation tags are markup. Bare '<' / '>' may be math;
    # an escaped literal tag is text, so identify markup before decoding entities.
    attributes = []
    opened = {}
    paired = set()
    for match in INLINE_TAG.finditer(text):
        name = match["tag"].lower()
        if not match["end"]:
            opened.setdefault(name, []).append(match)
        elif opened.get(name):
            start = opened[name].pop()
            paired.update((start.start(), match.start()))
            attributes.append(start["attrs"])
    if paired:
        text = INLINE_TAG.sub(lambda m: "" if m.start() in paired else m[0], text)
    # Only decode complete references; an ampersand by itself is valid TeX.
    text = re.sub(r"&(?:#\d+|#[xX][a-fA-F0-9]+|[a-zA-Z][a-zA-Z0-9]*);",
                  lambda match: unescape(match[0]), text)
    text = text.translate(SYMBOLS)
    text = re.sub(r"\\([a-zA-Z]+)", lambda m: COMMANDS.get(m[1], m[0]), text)
    for spelling, symbol in (("<=", "≤"), (">=", "≥"), ("!=", "≠"), (r"\%", "%")):
        text = text.replace(spelling, symbol)

    def html_number(match):
        # Attribute digits are independent literals, too.
        attributes.append(match["attrs"])
        op = "^" if match["tag"].lower() == "sup" else "_"
        return op + "{" + match["value"] + "}"

    text = HTML_SCRIPT.sub(html_number, text)
    text = "\n".join([text, *attributes])
    text = TEX_SCRIPT.sub(lambda m: m[1] + "{" + (m[2] or m[3]) + "}", text)

    def unicode_number(match):
        chars = match[0]
        op = "^" if chars[0] in SUPER else "_"
        return op + "{" + chars.translate(SCRIPT_DIGITS) + "}"

    return UNICODE_SCRIPT.sub(unicode_number, text)


def numeric_counts(text, path):
    if path.suffix.lower() in {".md", ".markdown", ".mdown", ".mkd", ".qmd", ".rmd"}:
        text = markdown_body(text)
    text = typeset_numbers(text)
    counts = Counter()
    for match in NUMBER.finditer(text):
        right = RIGHT_RELATION.match(text, match.end())
        spelling = "".join(part for part in match.groups() if part)
        counts[spelling + (right[1] if right else "")] += 1
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", type=Path, help="原文的 UTF-8 文本")
    parser.add_argument("after", type=Path, help="成稿的 UTF-8 文本")
    parser.add_argument("--keep", action="append", default=[], metavar="TEXT",
                        help="核对指定连续片段的次数，可重复使用")
    args = parser.parse_args()
    try:
        before = args.before.read_text(encoding="utf-8-sig")
        after = args.after.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        parser.error(f"读取文本失败：{exc}")

    fragments = dict.fromkeys(args.keep)
    for fragment in fragments:
        if not fragment or fragment not in before:
            parser.error(f"--keep 需要原文中出现过的非空片段，收到 {fragment!r}")

    old = numeric_counts(before, args.before)
    new = numeric_counts(after, args.after)
    differences = []
    for value in sorted(old.keys() | new.keys()):
        if old[value] != new[value]:
            differences.append(("数值", value, old[value], new[value]))
    for value in fragments:
        original, revised = before.count(value), after.count(value)
        if original != revised:
            differences.append(("片段", value, original, revised))
    for kind, value, original, revised in differences:
        print(f"{kind} {value!r} 在原文出现 {original} 次，在成稿出现 {revised} 次。")
    if differences:
        return 1
    print("所查数值与指定片段的出现次数一致。")
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="backslashreplace")
    sys.exit(main())
