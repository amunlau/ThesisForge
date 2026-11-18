#!/usr/bin/env python3
"""Audit registered review concerns, supplied versions and literal change evidence.

No semantic, scientific or visual certification; unavailable material is not
evidence that a promised revision is absent. Python 3.9+, stdlib except PDF.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
from xml.etree.ElementTree import ParseError
from zipfile import BadZipFile

sys.path.insert(0, str(Path(__file__).resolve().parent))
from compare_manuscripts import compare_snapshots, extract_document, markdown_text, read_json, unique_json

ROLES = {"before", "after", "reviews", "response", "final_pdf", "marked"}
STANCES = {"accept", "partial", "clarify", "decline", "future", "pending"}
ACTIONS = {"completed", "planned", "not_changed", "unknown"}
SHA = re.compile(r"[0-9a-fA-F]{64}\Z")


def nonempty(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(name + " must be a nonempty string")
    return value


def strings(value, name):
    if not isinstance(value, list):
        raise ValueError(name + " must be an array")
    return [nonempty(x, name) for x in value]


def within(root, value):
    path = (root / value).resolve()
    if not path.is_relative_to(root):
        raise ValueError("Path leaves --root: " + str(value))
    return path


def audit_case(case, root):
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("--root must be an existing directory")
    if not isinstance(case, dict) or type(case.get("schema")) is not int or case["schema"] != 1:
        raise ValueError("Expected schema 1 reviewer-response ledger")
    documents = case.get("documents")
    if not isinstance(documents, dict):
        raise ValueError("documents must map IDs to document records")
    findings = []

    def flag(level, code, identity, detail):
        findings.append({"level": level, "code": code, "id": identity, "detail": detail})

    snapshots, doc_states = {}, {}
    for identity, row in documents.items():
        nonempty(identity, "document ID")
        if not isinstance(row, dict) or row.get("role") not in ROLES:
            raise ValueError(identity + ": unknown document role")
        path = within(root, nonempty(row.get("path"), identity + ".path"))
        view, encoding = row.get("view", "final"), row.get("encoding", "utf-8-sig")
        if view not in {"final", "original"} or encoding not in {"utf-8-sig", "gb18030"}:
            raise ValueError(identity + ": invalid view or encoding")
        try:
            snapshot = extract_document(path, view=view, encoding=encoding)
        except (OSError, ValueError, RuntimeError, BadZipFile, ParseError) as exc:
            doc_states[identity] = {"state": "unavailable", "path": str(path), "reason": str(exc)}
            flag("review", "document_unavailable", identity,
                 "Cannot independently verify material; this is not proof of an absent revision: " + str(exc))
            continue
        snapshots[identity] = snapshot
        expected = row.get("sha256")
        state = "current"
        if not isinstance(expected, str) or not SHA.fullmatch(expected):
            state = "unfrozen"
            flag("review", "document_identity_unfrozen", identity, "Record the SHA-256 of the actually reviewed version")
        elif expected.lower() != snapshot["source"]["sha256"]:
            state = "stale"
            flag("error", "document_changed", identity, "File differs from its registered version; old checks are invalid")
        doc_states[identity] = {"state": state, "source": snapshot["source"], "view": view,
                               "role": row["role"], "coverage": snapshot["coverage"]}

    def selector(value, owner, purpose):
        if not isinstance(value, dict):
            raise ValueError(owner + ": selector must be an object")
        doc = nonempty(value.get("document_id"), "selector.document_id")
        unit_id = nonempty(value.get("unit_id"), "selector.unit_id")
        quote = nonempty(value.get("quote"), "selector.quote")
        result = {"document_id": doc, "unit_id": unit_id, "quote": quote,
                  "state": "unverified", "purpose": purpose}
        if doc not in documents:
            flag("error", "unknown_document", owner, doc)
            return result
        state = doc_states[doc]["state"]
        if state in {"unavailable", "stale"}:
            result["state"] = state
            return result
        snapshot = snapshots[doc]
        unit = next((u for u in snapshot["units"] if u["id"] == unit_id), None)
        if unit is None:
            flag("error", "unknown_unit", owner, doc + ":" + unit_id)
            return result
        result.update({"channel": unit["channel"], "locator": unit["locator"],
                       "actual_sha256": snapshot["source"]["sha256"]})
        count = unit["text"].count(quote)
        result["literal_matches_in_unit"] = count
        if count == 0:
            flag("error", "quote_not_in_unit", owner, doc + ":" + unit_id)
            return result
        if count > 1:
            flag("review", "ambiguous_quote", owner, "Fragment occurs repeatedly in selected unit; choose a unique anchor")
            return result
        if purpose in {"before", "after"}:
            if unit["channel"] == "comment" or documents[doc]["role"] in {"reviews", "response"}:
                flag("error", "review_or_reply_used_as_manuscript", owner,
                     "A review or response fragment cannot establish a manuscript revision")
                return result
            allowed = {"before", "marked"} if purpose == "before" else {"after", "marked", "final_pdf"}
            if documents[doc]["role"] not in allowed:
                flag("error", "wrong_manuscript_role", owner, purpose + " points to " + documents[doc]["role"])
                return result
            if documents[doc]["role"] == "marked" and snapshot["view"] != ("original" if purpose == "before" else "final"):
                flag("error", "wrong_marked_view", owner, "A marked manuscript needs original view for before and final view for after")
                return result
            if purpose == "after" and snapshot["view"] != "final":
                flag("error", "wrong_after_view", owner, "Revised-manuscript evidence must use the final view, even when the role is after")
                return result
            if unit["locator"].get("projection_ambiguities"):
                result["state"] = "projection_needs_review"
                flag("review", "ambiguous_manuscript_projection", owner,
                     "Unresolved paragraph/table revisions require target-editor verification of this unit's displayed view")
                return result
        elif purpose == "comment" and documents[doc]["role"] != "reviews" and unit["channel"] != "comment":
            flag("review", "review_source_role_unclear", owner, "Confirm that this is the expert's original comment")
        elif purpose == "reply" and documents[doc]["role"] != "response":
            flag("review", "reply_source_role_unclear", owner, "Document is not registered as the response letter")
        result["state"] = "matched_current" if state == "current" else "matched_unfrozen"
        return result

    def indexed(name):
        rows = case.get(name)
        if not isinstance(rows, list):
            raise ValueError(name + " must be an array")
        result = {}
        for row in rows:
            if not isinstance(row, dict):
                raise ValueError(name + " entries must be objects")
            identity = nonempty(row.get("id"), name + ".id")
            if identity in result:
                flag("error", "duplicate_" + name + "_id", identity, "Duplicate row was not merged")
            else:
                result[identity] = row
        return result

    comments, responses = indexed("comments"), indexed("responses")
    aspect_parent, comment_results = {}, {}
    for identity, row in comments.items():
        aspects = strings(row.get("aspect_ids"), identity + ".aspect_ids")
        for aspect in aspects:
            if aspect in aspect_parent:
                flag("error", "duplicate_aspect_id", aspect, "Aspect IDs must be globally unique")
            else:
                aspect_parent[aspect] = identity
        comment_results[identity] = {"id": identity, "source": selector(row.get("source"), identity, "comment"),
                                     "aspect_ids": aspects, "response_ids": []}

    aspect_responses = defaultdict(list)
    compared_pairs = {}
    bound_reply_units = defaultdict(set)
    response_results = []
    completion = re.compile(r"(?:we\s+have\s+(?:revised|added|changed|completed)|已(?:经)?(?:修改|补充|完成|新增))", re.I)
    for identity, row in responses.items():
        comment_ids = strings(row.get("comment_ids"), identity + ".comment_ids")
        aspect_ids = strings(row.get("aspect_ids"), identity + ".aspect_ids")
        stance, action = row.get("stance"), row.get("action_status")
        if stance not in STANCES or action not in ACTIONS:
            raise ValueError(identity + ": invalid stance/action_status")
        text = nonempty(row.get("text"), identity + ".text")
        for optional in ("rationale", "remaining"):
            if optional in row and row[optional] is not None and not isinstance(row[optional], str):
                raise ValueError(identity + "." + optional + " must be text")
        if not comment_ids:
            flag("error", "response_without_comment", identity, "Link reply to its originating comments")
        for field, ids in (("comment_ids", comment_ids), ("aspect_ids", aspect_ids)):
            if len(set(ids)) != len(ids):
                flag("error", "duplicate_response_link", identity, field)
        for comment in dict.fromkeys(comment_ids):
            if comment not in comments:
                flag("error", "unknown_comment", identity, comment)
            else:
                comment_results[comment]["response_ids"].append(identity)
        for aspect in dict.fromkeys(aspect_ids):
            if aspect not in aspect_parent:
                flag("error", "unknown_aspect", identity, aspect)
            elif aspect_parent[aspect] not in comment_ids:
                flag("error", "aspect_parent_mismatch", identity, aspect)
            else:
                aspect_responses[aspect].append(identity)
        if stance == "future" and action == "completed":
            flag("error", "future_marked_completed", identity, "Future work cannot be a completed action")
        if stance == "decline" and not (row.get("rationale") or "").strip():
            flag("error", "decline_without_rationale", identity, "Deliberate non-change needs its reason")
        if stance == "partial" and not any((row.get(k) or "").strip() for k in ("rationale", "remaining")):
            flag("error", "partial_without_boundary", identity, "Describe remaining requirements or partial-acceptance reason")
        if action in {"planned", "unknown", "not_changed"} and completion.search(text):
            flag("review", "completion_wording_needs_review", identity,
                 "Completion wording may conflict with action; check negations and historical context")
        reply = selector(row["reply_source"], identity, "reply") if row.get("reply_source") is not None else None
        if reply is not None and reply["state"] == "matched_current":
            bound_reply_units[reply["document_id"]].add(reply["unit_id"])
        if reply is not None and reply["quote"] != text:
            flag("review", "reply_fragment_only", identity, "The selected fragment does not bind the entire final reply")
        evidence = row.get("evidence", [])
        if not isinstance(evidence, list):
            raise ValueError(identity + ".evidence must be an array")
        checks = []
        for number, item in enumerate(evidence, 1):
            if not isinstance(item, dict) or item.get("kind") not in {"text", "figure", "format", "analysis"}:
                raise ValueError(identity + ": invalid evidence kind")
            description = nonempty(item.get("description"), identity + ".evidence.description")
            label = identity + ":evidence:" + str(number)
            before = selector(item["before"], label, "before") if item.get("before") is not None else None
            after = selector(item["after"], label, "after") if item.get("after") is not None else None
            state = "not_independently_verified"
            comparison = None
            if any(x and x["state"] == "stale" for x in (before, after)):
                state = "stale"
            elif item["kind"] != "text":
                state = "nontext_review_required"
            elif after and after["state"] == "matched_current":
                if before and before["state"] == "matched_current":
                    pair = (before["document_id"], after["document_id"])
                    if pair not in compared_pairs:
                        compared_pairs[pair] = compare_snapshots(snapshots[pair[0]], snapshots[pair[1]])
                    actual_diff = compared_pairs[pair]
                    before_changes = {c["id"] for c in actual_diff["changes"]
                                      if any(u["id"] == before["unit_id"] for u in c["before"])}
                    after_changes = {c["id"] for c in actual_diff["changes"]
                                     if any(u["id"] == after["unit_id"] for u in c["after"])}
                    comparison = {"source_bytes_differ": actual_diff["source_bytes_differ"],
                                  "extracted_text_equal": actual_diff["extracted_text_equal"],
                                  "before_changed_unit": bool(before_changes),
                                  "after_changed_unit": bool(after_changes),
                                  "shared_change_ids": sorted(before_changes & after_changes),
                                  "alignment": "heuristic literal unit alignment, not semantic correspondence"}
                    if before["quote"] == after["quote"]:
                        state = "same_selected_text"
                        flag("review", "selected_text_already_present", label,
                             "Same selected text does not prove a new change; clarification/nontext changes may still be valid")
                    elif actual_diff["extracted_text_equal"]:
                        state = "identical_extracted_text"
                        flag("review", "different_anchors_in_identical_text", label,
                             "Different selected fragments do not establish a revision when extracted documents are identical")
                    elif any(after["quote"] in u["text"] for u in snapshots[pair[0]]["units"] if u["channel"] != "comment"):
                        state = "prior_text_present_elsewhere"
                        flag("review", "after_quote_elsewhere_in_before", label,
                             "The fragment appears in the prior manuscript; moving or selecting different anchors does not establish newly added content")
                    elif before_changes & after_changes:
                        state = "observed_text_difference"
                    else:
                        state = "different_selected_fragments_not_a_verified_revision"
                        flag("review", "selected_anchors_not_paired_change", label,
                             "Both selected units must belong to the same actual text-difference range; unmatched anchors need review")
                else:
                    state = "current_presence_only"
                    flag("review", "before_not_verified", label, "Current presence does not establish newly added content")
            if state in {"not_independently_verified", "nontext_review_required"}:
                flag("review", "evidence_needs_review", label, "Inspect actual missing material, figure, format or analysis")
            checks.append({"kind": item["kind"], "description": description, "before": before, "after": after,
                           "literal_evidence_state": state, "comparison": comparison,
                           "semantic_sufficiency": "not_assessed"})
        if action == "completed" and not evidence:
            flag("review", "completion_without_evidence", identity, "Declared completion is not independently verified")
        locations = row.get("locations", [])
        if not isinstance(locations, list):
            raise ValueError(identity + ".locations must be an array")
        location_checks = []
        for location in locations:
            if not isinstance(location, dict):
                raise ValueError(identity + ": location must be an object")
            doc = nonempty(location.get("document_id"), "location.document_id")
            page = location.get("pdf_page")
            if type(page) is not int or page < 1 or location.get("verification") not in {"visual", "unverified"}:
                raise ValueError("location needs positive one-based pdf_page and verification status")
            checked = {**location, "page_bounds_checked": False, "visual_independently_verified": False}
            if doc not in documents:
                flag("error", "unknown_location_document", identity, doc)
            elif doc_states[doc]["state"] != "current":
                flag("review", "location_document_not_current", identity, doc)
            elif Path(documents[doc]["path"]).suffix.lower() != ".pdf":
                flag("error", "location_not_pdf", identity, doc)
            else:
                pages = snapshots[doc]["coverage"].get("pages_read")
                checked["page_bounds_checked"] = isinstance(pages, int)
                if isinstance(pages, int) and page > pages:
                    flag("error", "pdf_page_out_of_range", identity, f"{doc}: requested {page}, actual {pages}")
                if location["verification"] == "visual":
                    expected = location.get("verified_sha256")
                    if not isinstance(expected, str) or not SHA.fullmatch(expected):
                        flag("review", "visual_identity_missing", identity, "Record the hash of the actually viewed PDF")
                    elif expected.lower() != snapshots[doc]["source"]["sha256"]:
                        flag("error", "visual_location_stale", identity, "Visual declaration belongs to another PDF version")
                flag("review", "printed_location_needs_visual_review", identity,
                     "PDF index/label do not verify printed page/line; declared visual review is not independently checked")
            location_checks.append(checked)
        response_results.append({"id": identity, "comment_ids": comment_ids, "aspect_ids": aspect_ids,
                                 "stance": stance, "declared_action_status": action, "text": text,
                                 "reply_source": reply, "rationale": row.get("rationale"), "remaining": row.get("remaining"),
                                 "evidence": checks, "locations": location_checks, "semantic_coverage": "not_assessed"})

    reply_document_coverage = {}
    for identity, row in documents.items():
        if row["role"] != "response":
            continue
        if identity not in snapshots:
            reply_document_coverage[identity] = {"state": "unavailable", "body_units": None,
                                                  "units_with_bound_fragments": None, "unbound_units": None}
            continue
        body = [u for u in snapshots[identity]["units"] if u["channel"] == "body"]
        bound = bound_reply_units[identity]
        unbound = [{"unit_id": u["id"], "locator": u["locator"], "excerpt": u["text"][:240]}
                   for u in body if u["id"] not in bound]
        reply_document_coverage[identity] = {"state": doc_states[identity]["state"], "body_units": len(body),
            "units_with_bound_fragments": sum(u["id"] in bound for u in body), "unbound_units": unbound,
            "meaning": "A bound fragment does not prove the entire unit or letter was read or semantically checked"}
        if unbound:
            flag("review", "response_body_units_unbound", identity,
                 f"{len(unbound)} of {len(body)} extracted reply-body units lack current reply_source anchors; these may include thanks or substantive claims")

    for identity, result in comment_results.items():
        result["unmapped_aspect_ids"] = [a for a in result["aspect_ids"] if not aspect_responses[a]]
        if not result["response_ids"]:
            flag("error", "comment_without_response", identity, "No registered response links to this comment")
        for aspect in result["unmapped_aspect_ids"]:
            flag("error", "aspect_without_response", identity, aspect)
        result["mapping_state"] = "mapped" if result["response_ids"] and not result["unmapped_aspect_ids"] else "incomplete"
        result["semantic_coverage"] = "not_assessed"
    if not comments:
        flag("review", "empty_comment_inventory", "case", "No registered comments; cannot claim full coverage")
    # Extraction is a captured byte snapshot. Refuse to label anchors current if
    # any supplied material was replaced while the other documents were read or
    # the report was assembled. This is a conflict check, not a filesystem lock.
    for snapshot in snapshots.values():
        path = Path(snapshot["source"]["path"])
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
        if digest.hexdigest() != snapshot["source"]["sha256"]:
            raise ValueError("Document changed during audit; retry: " + str(path))
    severity = Counter(x["level"] for x in findings)
    return {"schema": "thesisforge.reviewer-response-audit/1", "checked_at": datetime.now(timezone.utc).isoformat(),
            "status": "structural_errors" if severity["error"] else "review_needed" if severity["review"] else "structure_consistent_within_registered_scope",
            "documents": doc_states, "comments": list(comment_results.values()), "responses": response_results,
            "reply_document_coverage": reply_document_coverage,
            "findings": findings, "counts": {"registered_comments": len(comments), "registered_aspects": len(aspect_parent),
                "mapped_comments": sum(bool(x["response_ids"]) for x in comment_results.values()),
                "mapped_aspects": sum(bool(aspect_responses[a]) for a in aspect_parent),
                "registered_responses": len(responses), "errors": severity["error"], "review_items": severity["review"]},
            "semantic_review": "not_run", "visual_review": "not_run",
            "limits": ["Denominator is only explicitly registered comments/aspects, not all original concerns.",
                       "Mapping does not establish semantic coverage. Stance, action and evidence verification are separate.",
                       "Literal matches/differences cannot validate science, execution, figures or formatting.",
                       "Current presence without both authoritative versions does not establish a new revision.",
                       "Replies without reply_source are ledger text; bound fragments do not certify entire reply units. Unbound body units are reported separately.",
                       "PDF labels are not printed page/line numbers; visual declarations are not authenticated here."]}


def render_markdown(report):
    lines = ["# 专家意见与回复覆盖核查", "", "仅检查登记项、身份与字面锚点；未判定科学充分性或最终版面。", "",
             "| 意见 ID | 原话核对 | 关联回复 | 未关联子问题 |", "|---|---|---|---|"]
    for row in report["comments"]:
        values = (row["id"], row["source"]["state"], ", ".join(row["response_ids"]), ", ".join(row["unmapped_aspect_ids"]))
        lines.append("| " + " | ".join(markdown_text(v) for v in values) + " |")
    lines += ["", "| 回复 ID | 立场 | 声明动作 | 字面证据 |", "|---|---|---|---|"]
    for row in report["responses"]:
        values = (row["id"], row["stance"], row["declared_action_status"],
                  ", ".join(e["literal_evidence_state"] for e in row["evidence"]) or "not_independently_verified")
        lines.append("| " + " | ".join(markdown_text(v) for v in values) + " |")
    if report["reply_document_coverage"]:
        lines += ["", "## 最终回复正文的绑定范围", "",
                  "绑定仅表示单元内存在已核短引，不代表该单元全部内容或整封回复已核实。", "",
                  "| 回复文件 | 提取正文单元 | 含已绑定短引的单元 | 未绑定正文单元 |", "|---|---|---|---|"]
        for identity, coverage in report["reply_document_coverage"].items():
            unbound = coverage["unbound_units"]
            values = (identity, coverage["body_units"], coverage["units_with_bound_fragments"],
                      ", ".join(u["unit_id"] for u in unbound) if unbound is not None else "unavailable")
            lines.append("| " + " | ".join(markdown_text(v) for v in values) + " |")
    lines += ["", "## 确定问题与待核事项", "", "| 类型 | 编号 | 对象 | 说明 |", "|---|---|---|---|"]
    for item in report["findings"]:
        lines.append("| " + " | ".join(markdown_text(item[k]) for k in ("level", "code", "id", "detail")) + " |")
    lines += ["", "登记统计：" + json.dumps(report["counts"], ensure_ascii=False), "",
              "无结构问题不代表专家要求已解决；语义、非文本对象和页行号需另行复核。"]
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", type=Path)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--markdown", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)
    try:
        root = args.root.resolve(strict=True)
        source = within(root, args.case)
        targets = [within(root, args.output)] + ([within(root, args.markdown)] if args.markdown else [])
        if len(set(targets)) != len(targets) or any(p.exists() or p == source for p in targets):
            raise ValueError("Outputs must be distinct new files")
        raw = source.read_bytes()
        # Parse exactly the bytes whose identity is reported. A second path read
        # could see an intermediate save even if the original is later restored.
        case = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=unique_json,
                          parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))
        if not isinstance(case, dict):
            raise ValueError("Case must be an object")
        if isinstance(case.get("documents"), dict):
            for value in case["documents"].values():
                if isinstance(value, dict) and isinstance(value.get("path"), str) and within(root, value["path"]) in targets:
                    raise ValueError("Output aliases a declared document, including an unavailable one")
        report = audit_case(case, root)
        report["case_source"] = {"path": str(source), "sha256": hashlib.sha256(raw).hexdigest()}
        if source.read_bytes() != raw:
            raise ValueError("Ledger changed during audit; retry")
        rendered = [json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n"]
        if args.markdown:
            rendered.append(render_markdown(report))
        for target, content in zip(targets, rendered):
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(content)
        print(json.dumps({"status": report["status"], "output": str(targets[0]), **report["counts"]}, ensure_ascii=True))
        return 1 if args.strict and report["counts"]["errors"] else 0
    except (OSError, ValueError, TypeError, KeyError, RecursionError, BadZipFile, ParseError) as exc:
        print(json.dumps({"status": "input_error", "error": str(exc)}, ensure_ascii=True), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
