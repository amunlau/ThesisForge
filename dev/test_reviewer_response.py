"""Behavioral evidence/coverage tests; synthetic manuscripts, no upstream code."""
import copy
from contextlib import redirect_stderr, redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import audit_reviewer_response as audit
from compare_manuscripts import extract_document


class ReviewerResponseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="thesisforge-response-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.docs = {}
        self.put("reviews", "专家意见.txt", "请解释边界并补充方法。\n", "reviews")
        self.put("before", "原稿.txt", "原来的方法说明。\n", "before")
        self.put("after", "修改稿.txt", "新增明确的边界及方法说明。\n", "after")
        self.case = {"schema": 1, "documents": self.docs,
                     "comments": [{"id": "R1.1", "source": self.sel("reviews", "请解释边界并补充方法。"),
                                   "aspect_ids": ["R1.1a", "R1.1b"]}],
                     "responses": [{"id": "A1", "comment_ids": ["R1.1"], "aspect_ids": ["R1.1a", "R1.1b"],
                                    "stance": "accept", "action_status": "completed", "text": "已补充边界及方法。",
                                    "evidence": [{"kind": "text", "description": "正文方法段修改",
                                                  "before": self.sel("before", "原来的方法说明。"),
                                                  "after": self.sel("after", "新增明确的边界及方法说明。")}]}]}

    def put(self, identity, name, content, role):
        path = self.root / name
        if isinstance(content, str):
            content = content.encode("utf-8")
        path.write_bytes(content)
        self.docs[identity] = {"path": name, "sha256": hashlib.sha256(content).hexdigest(), "role": role}
        return path

    def sel(self, identity, quote, unit="U000001"):
        return {"document_id": identity, "unit_id": unit, "quote": quote}

    def run_case(self):
        return audit.audit_case(self.case, self.root)

    def codes(self, report):
        return {f["code"] for f in report["findings"]}

    def cli(self, *args, case=None):
        path = self.root / "台账.json"
        path.write_text(json.dumps(case or self.case, ensure_ascii=False), encoding="utf-8")
        return subprocess.run([sys.executable, "-B", str(ROOT / "scripts/audit_reviewer_response.py"),
                               str(path), "--root", str(self.root), "--output", str(self.root / "核查.json"), *args],
                              cwd=self.root, capture_output=True, encoding="utf-8", timeout=20)

    def test_literal_difference_does_not_certify_resolution(self):
        result = self.run_case()
        self.assertEqual(result["counts"]["errors"], 0)
        self.assertEqual(result["counts"]["mapped_aspects"], 2)
        self.assertEqual(result["responses"][0]["evidence"][0]["literal_evidence_state"], "observed_text_difference")
        self.assertEqual(result["responses"][0]["semantic_coverage"], "not_assessed")
        self.assertEqual(result["visual_review"], "not_run")

    def test_missing_before_is_presence_only(self):
        (self.root / "原稿.txt").unlink()
        result = self.run_case()
        self.assertEqual(result["counts"]["errors"], 0)
        self.assertEqual(result["responses"][0]["evidence"][0]["literal_evidence_state"], "current_presence_only")
        self.assertIn("before_not_verified", self.codes(result))

    def test_missing_after_is_unverified_not_absent_revision(self):
        (self.root / "修改稿.txt").unlink()
        result = self.run_case()
        self.assertEqual(result["counts"]["errors"], 0)
        self.assertEqual(result["responses"][0]["evidence"][0]["literal_evidence_state"], "not_independently_verified")
        self.assertNotIn("quote_not_in_unit", self.codes(result))
        self.assertEqual(self.cli("--strict").returncode, 0)

    def test_recapturing_file_does_not_silently_reuse_old_hash(self):
        (self.root / "修改稿.txt").write_text("又一份不同稿件。", encoding="utf-8")
        result = self.run_case()
        self.assertIn("document_changed", self.codes(result))
        self.assertEqual(result["responses"][0]["evidence"][0]["literal_evidence_state"], "stale")

    def test_same_content_is_not_new_revision(self):
        self.put("after", "修改稿.txt", "原来的方法说明。\n", "after")
        self.case["responses"][0]["evidence"][0]["after"]["quote"] = "原来的方法说明。"
        result = self.run_case()
        self.assertIn("selected_text_already_present", self.codes(result))
        self.assertEqual(result["responses"][0]["evidence"][0]["literal_evidence_state"], "same_selected_text")

    def test_moved_text_is_not_certified_as_added(self):
        self.put("before", "原稿.txt", "原来的方法说明。\n新增明确的边界及方法说明。\n", "before")
        result = self.run_case()
        self.assertIn("after_quote_elsewhere_in_before", self.codes(result))
        self.assertEqual(result["responses"][0]["evidence"][0]["literal_evidence_state"], "prior_text_present_elsewhere")

    def test_same_file_same_view_different_fragments_do_not_prove_revision(self):
        self.put("before", "原稿.txt", "原来的方法说明。\n新增明确的边界及方法说明。\n", "before")
        self.docs["after"] = {**self.docs["before"], "role": "after"}
        self.case["responses"][0]["evidence"][0]["after"]["unit_id"] = "U000002"
        evidence = self.run_case()["responses"][0]["evidence"][0]
        self.assertEqual(evidence["literal_evidence_state"], "identical_extracted_text")
        self.assertFalse(evidence["comparison"]["source_bytes_differ"])

    def test_same_docx_body_different_packaging_does_not_prove_revision(self):
        ns = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
        body = (f'<w:document xmlns:w="{ns}"><w:body><w:p><w:r><w:t>原来的方法说明。</w:t>'
                '</w:r></w:p><w:p><w:r><w:t>新增明确的边界及方法说明。</w:t></w:r></w:p></w:body></w:document>')
        for identity in ("before", "after"):
            path = self.root / (identity + ".docx")
            with ZipFile(path, "w") as z:
                z.writestr("word/document.xml", body)
                z.writestr("docProps/core.xml", "<metadata>" + identity + "</metadata>")
            self.docs[identity] = {"path": path.name, "role": identity,
                                   "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        self.case["responses"][0]["evidence"][0]["after"]["unit_id"] = "U000002"
        evidence = self.run_case()["responses"][0]["evidence"][0]
        self.assertEqual(evidence["literal_evidence_state"], "identical_extracted_text")
        self.assertTrue(evidence["comparison"]["source_bytes_differ"])

    def test_unrelated_unchanged_anchor_cannot_bind_real_change_elsewhere(self):
        self.put("before", "原稿.txt", "保留的背景。\n原来的方法说明。\n", "before")
        self.put("after", "修改稿.txt", "保留的背景。\n新增明确的边界及方法说明。\n", "after")
        evidence = self.case["responses"][0]["evidence"][0]
        evidence["before"] = self.sel("before", "保留的背景。")
        evidence["after"]["unit_id"] = "U000002"
        result = self.run_case()["responses"][0]["evidence"][0]
        self.assertEqual(result["literal_evidence_state"], "different_selected_fragments_not_a_verified_revision")
        self.assertFalse(result["comparison"]["before_changed_unit"])
        self.assertTrue(result["comparison"]["after_changed_unit"])

    def test_actual_document_pair_comparison_is_reused(self):
        self.case["responses"][0]["evidence"].append(copy.deepcopy(self.case["responses"][0]["evidence"][0]))
        with patch.object(audit, "compare_snapshots", wraps=audit.compare_snapshots) as compare:
            result = self.run_case()
        self.assertEqual(compare.call_count, 1)
        self.assertTrue(all(e["literal_evidence_state"] == "observed_text_difference" for e in result["responses"][0]["evidence"]))

    def test_two_unchanged_units_cannot_be_compared_as_a_revision(self):
        self.put("before", "原稿.txt", "保留句甲。\n保留句乙。\n旧结果。\n", "before")
        self.put("after", "修改稿.txt", "保留句甲。\n保留句乙。\n新结果。\n", "after")
        item = self.case["responses"][0]["evidence"][0]
        item["before"] = self.sel("before", "保留句甲。")
        item["after"] = self.sel("after", "保留句乙。", "U000002")
        result = self.run_case()["responses"][0]["evidence"][0]
        self.assertNotEqual(result["literal_evidence_state"], "observed_text_difference")
        self.assertFalse(result["comparison"]["before_changed_unit"])
        self.assertFalse(result["comparison"]["after_changed_unit"])

    def test_missing_subrequest_cannot_be_hidden_by_parent_mapping(self):
        self.case["responses"][0]["aspect_ids"] = ["R1.1a"]
        result = self.run_case()
        self.assertEqual(result["counts"]["mapped_comments"], 1)
        self.assertEqual(result["counts"]["mapped_aspects"], 1)
        self.assertIn("aspect_without_response", self.codes(result))
        self.assertEqual(self.cli("--strict").returncode, 1)

    def test_wrong_parent_unknown_duplicate_links(self):
        self.case["comments"].append({"id": "R2", "source": self.sel("reviews", "请解释边界并补充方法。"),
                                      "aspect_ids": ["R2a"]})
        self.case["responses"][0]["aspect_ids"] += ["R2a", "UNKNOWN"]
        self.case["responses"][0]["comment_ids"] += ["X", "X"]
        codes = self.codes(self.run_case())
        self.assertTrue({"aspect_parent_mismatch", "unknown_aspect", "unknown_comment",
                         "duplicate_response_link", "comment_without_response"} <= codes)

    def test_shared_response_can_cover_multiple_comments(self):
        self.case["comments"].append({"id": "R2", "source": self.sel("reviews", "请解释边界并补充方法。"),
                                      "aspect_ids": ["R2a"]})
        self.case["responses"][0]["comment_ids"].append("R2")
        self.case["responses"][0]["aspect_ids"].append("R2a")
        result = self.run_case()
        self.assertEqual(result["counts"]["errors"], 0)
        self.assertEqual(result["counts"]["mapped_comments"], 2)
        self.assertEqual(result["counts"]["mapped_aspects"], 3)

    def test_duplicate_comment_response_and_aspect_ids_are_errors(self):
        self.case["comments"].append(copy.deepcopy(self.case["comments"][0]))
        self.case["comments"][0]["aspect_ids"].append("R1.1a")
        self.case["responses"].append(copy.deepcopy(self.case["responses"][0]))
        self.assertTrue({"duplicate_comments_id", "duplicate_responses_id", "duplicate_aspect_id"} <= self.codes(self.run_case()))

    def test_quote_mismatch_and_ambiguity_are_distinct(self):
        self.case["comments"][0]["source"]["quote"] = "不存在的专家原话"
        self.assertIn("quote_not_in_unit", self.codes(self.run_case()))
        self.put("reviews", "专家意见.txt", "重复重复\n", "reviews")
        self.case["comments"][0]["source"]["quote"] = "重复"
        result = self.run_case()
        self.assertIn("ambiguous_quote", self.codes(result))
        self.assertEqual(result["counts"]["errors"], 0)

    def test_decline_partial_future_and_heuristic_states(self):
        row = self.case["responses"][0]
        row.update(stance="decline", action_status="not_changed", text="维持设计；理由如下。", evidence=[])
        self.assertIn("decline_without_rationale", self.codes(self.run_case()))
        row["rationale"] = "原有独立对照已覆盖该条件。"
        self.assertEqual(self.run_case()["counts"]["errors"], 0)
        row.update(stance="partial", rationale="", remaining="")
        self.assertIn("partial_without_boundary", self.codes(self.run_case()))
        row.update(stance="future", action_status="completed")
        self.assertIn("future_marked_completed", self.codes(self.run_case()))
        row.update(action_status="planned", text="已修改方法。")
        result = self.run_case()
        self.assertIn("completion_wording_needs_review", self.codes(result))
        self.assertEqual(result["counts"]["errors"], 0)

    def test_nontext_change_cannot_be_closed_by_text_match(self):
        self.case["responses"][0]["evidence"][0]["kind"] = "figure"
        self.assertEqual(self.run_case()["responses"][0]["evidence"][0]["literal_evidence_state"], "nontext_review_required")

    def test_docx_comment_cannot_prove_manuscript_change(self):
        path = self.root / "带批注.docx"
        namespace = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
        with ZipFile(path, "w") as z:
            z.writestr("word/document.xml", f'<w:document xmlns:w="{namespace}"><w:body><w:p><w:r><w:t>未修改正文</w:t></w:r></w:p></w:body></w:document>')
            z.writestr("word/comments.xml", f'<w:comments xmlns:w="{namespace}"><w:comment w:id="0"><w:p><w:r><w:t>新增明确的边界及方法说明。</w:t></w:r></w:p></w:comment></w:comments>')
        self.docs["after"] = {"path": path.name, "role": "after", "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        unit = next(u for u in extract_document(path)["units"] if u["channel"] == "comment")
        self.case["responses"][0]["evidence"][0]["after"]["unit_id"] = unit["id"]
        self.assertIn("review_or_reply_used_as_manuscript", self.codes(self.run_case()))

    def test_reply_anchor_does_not_verify_entire_letter(self):
        self.put("reply", "回复.md", "已补充边界。\n还有未解决事项。\n", "response")
        self.case["responses"][0]["reply_source"] = self.sel("reply", "已补充边界。")
        self.assertIn("reply_fragment_only", self.codes(self.run_case()))

    def test_unbound_reply_body_is_explicit_review_not_strict_error(self):
        self.put("reply", "回复.md", "感谢意见。\n已补充边界及方法。\n我们还声称完成了未登记的研究。\n", "response")
        self.case["responses"][0]["reply_source"] = self.sel("reply", "已补充边界及方法。", "U000002")
        result = self.run_case()
        coverage = result["reply_document_coverage"]["reply"]
        self.assertEqual(coverage["body_units"], 3)
        self.assertEqual(coverage["units_with_bound_fragments"], 1)
        self.assertEqual([u["unit_id"] for u in coverage["unbound_units"]], ["U000001", "U000003"])
        self.assertIn("response_body_units_unbound", self.codes(result))
        self.assertEqual(result["counts"]["errors"], 0)
        self.assertEqual(self.cli("--strict").returncode, 0)

    def test_marked_view_cannot_masquerade_as_prior_content(self):
        self.docs["before"]["role"] = "marked"
        self.assertIn("wrong_marked_view", self.codes(self.run_case()))
        self.docs["before"]["view"] = "original"
        self.assertNotIn("wrong_marked_view", self.codes(self.run_case()))

    def test_original_projection_cannot_be_relabelled_as_revised_manuscript(self):
        path = self.root / "修改稿.docx"
        ns = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
        with ZipFile(path, "w") as archive:
            archive.writestr("word/document.xml", f'<w:document xmlns:w="{ns}"><w:body><w:p>'
                             '<w:del><w:r><w:delText>新增明确的边界及方法说明。</w:delText></w:r></w:del>'
                             '<w:ins><w:r><w:t>最终稿其实已删除该说明。</w:t></w:r></w:ins></w:p></w:body></w:document>')
        self.docs["after"] = {"path": path.name, "role": "after", "view": "original",
                              "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        result = self.run_case()
        self.assertIn("wrong_after_view", self.codes(result))
        self.assertNotEqual(result["responses"][0]["evidence"][0]["literal_evidence_state"], "observed_text_difference")

    def test_deleted_row_text_is_inspection_material_not_current_body_evidence(self):
        path = self.root / "带删除行.docx"
        ns = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
        with ZipFile(path, "w") as archive:
            archive.writestr("word/document.xml", f'<w:document xmlns:w="{ns}"><w:body><w:tbl><w:tr>'
                             '<w:trPr><w:del w:id="1"/></w:trPr><w:tc><w:p><w:r>'
                             '<w:t>新增明确的边界及方法说明。</w:t></w:r></w:p></w:tc></w:tr></w:tbl></w:body></w:document>')
        self.docs["after"] = {"path": path.name, "role": "after", "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        result = self.run_case()
        self.assertIn("ambiguous_manuscript_projection", self.codes(result))
        evidence = result["responses"][0]["evidence"][0]
        self.assertEqual(evidence["after"]["state"], "projection_needs_review")
        self.assertEqual(evidence["literal_evidence_state"], "not_independently_verified")
        self.assertEqual(result["counts"]["errors"], 0)

    def test_document_replaced_during_audit_requires_retry(self):
        compare = audit.compare_snapshots

        def replace_after_extraction(*args):
            result = compare(*args)
            (self.root / "修改稿.txt").write_text("审计中被另一进程换稿。", encoding="utf-8")
            return result

        with patch.object(audit, "compare_snapshots", side_effect=replace_after_extraction):
            with self.assertRaisesRegex(ValueError, "Document changed during audit"):
                self.run_case()

    def test_unknown_unit_and_document_are_not_silently_matched(self):
        self.case["comments"][0]["source"]["unit_id"] = "U999999"
        self.assertIn("unknown_unit", self.codes(self.run_case()))
        self.case["comments"][0]["source"]["document_id"] = "MISSING"
        self.assertIn("unknown_document", self.codes(self.run_case()))

    def test_duplicate_json_and_missing_input_output_alias_are_rejected(self):
        path = self.root / "duplicate.json"
        path.write_text('{"schema":1,"schema":1}', encoding="utf-8")
        with self.assertRaises(ValueError):
            audit.read_json(path)
        self.docs["after"]["path"] = "核查.json"
        result = self.cli()
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.root / "核查.json").exists())

    def test_empty_inventory_and_unfrozen_identity_are_not_full_coverage(self):
        result = audit.audit_case({"schema": 1, "documents": {}, "comments": [], "responses": []}, self.root)
        self.assertIn("empty_comment_inventory", self.codes(result))
        self.assertEqual(result["counts"]["registered_comments"], 0)
        self.docs["after"].pop("sha256")
        self.assertEqual(self.run_case()["documents"]["after"]["state"], "unfrozen")

    def test_path_escape_input_and_output_protection(self):
        self.docs["before"]["path"] = "../escape.txt"
        self.assertEqual(self.cli().returncode, 2)
        self.docs["before"]["path"] = "原稿.txt"
        (self.root / "核查.json").write_bytes(b"keep")
        self.assertEqual(self.cli().returncode, 2)
        self.assertEqual((self.root / "核查.json").read_bytes(), b"keep")

    def test_cli_handles_unicode_new_markdown_and_preserves_inputs(self):
        before = {n: (self.root / d["path"]).read_bytes() for n, d in self.docs.items()}
        result = self.cli("--markdown", str(self.root / "覆盖表.md"), "--strict")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.root / "覆盖表.md").is_file())
        self.assertEqual(before, {n: (self.root / d["path"]).read_bytes() for n, d in self.docs.items()})

    def test_saved_then_restored_ledger_cannot_mix_parsed_content_and_identity(self):
        case_path, output = self.root / "台账.json", self.root / "核查.json"
        original = b"\xef\xbb\xbf" + json.dumps(self.case, ensure_ascii=False).encode("utf-8")
        intermediate = copy.deepcopy(self.case)
        intermediate["responses"][0]["text"] = "另一份保存过程中的回复内容。"
        changed = json.dumps(intermediate, ensure_ascii=False).encode("utf-8")
        case_path.write_bytes(original)
        read_bytes, audit_case = Path.read_bytes, audit.audit_case
        replaced = []

        def read_then_save(path):
            raw = read_bytes(path)
            if path == case_path and not replaced:
                case_path.write_bytes(changed)
                replaced.append(True)
            return raw

        def restore_then_audit(case, root):
            case_path.write_bytes(original)
            return audit_case(case, root)

        with patch.object(Path, "read_bytes", read_then_save), \
                patch.object(audit, "audit_case", side_effect=restore_then_audit), \
                redirect_stdout(io.StringIO()):
            status = audit.main([str(case_path), "--root", str(self.root), "--output", str(output)])
        self.assertTrue(replaced)
        self.assertEqual(status, 0)
        report = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(report["case_source"]["sha256"], hashlib.sha256(original).hexdigest())
        self.assertEqual(report["responses"][0]["text"], self.case["responses"][0]["text"])
        self.assertEqual(case_path.read_bytes(), original)

    def test_frozen_byte_parser_rejects_duplicate_keys_and_nonfinite_values(self):
        case_path, output = self.root / "台账.json", self.root / "核查.json"
        inputs = ['{"schema":1,"schema":1,"documents":{},"comments":[],"responses":[]}', *(
            '{"schema":1,"documents":{},"comments":[],"responses":[],"extra":' + value + '}'
            for value in ("NaN", "Infinity", "-Infinity"))]
        for content in inputs:
            with self.subTest(content=content):
                case_path.write_text(content, encoding="utf-8")
                with redirect_stderr(io.StringIO()), redirect_stdout(io.StringIO()):
                    status = audit.main([str(case_path), "--root", str(self.root), "--output", str(output)])
                self.assertEqual(status, 2)
                self.assertFalse(output.exists())

    def test_pdf_pages_and_visual_statement_are_separate(self):
        try:
            import pymupdf as fitz
        except ImportError:
            try:
                import fitz
            except ImportError:
                self.skipTest("PyMuPDF optional for real PDF checks")
        path = self.root / "定稿.pdf"
        doc = fitz.open()
        doc.new_page().insert_text((72, 72), "Page i, printed line 12")
        doc.save(path)
        doc.close()
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        self.docs["pdf"] = {"path": path.name, "role": "final_pdf", "sha256": sha}
        location = {"document_id": "pdf", "pdf_page": 1, "printed_page": "i",
                    "printed_lines": "12", "verification": "visual", "verified_sha256": sha}
        self.case["responses"][0]["locations"] = [location]
        report = self.run_case()
        self.assertEqual(report["counts"]["errors"], 0)
        self.assertFalse(report["responses"][0]["locations"][0]["visual_independently_verified"])
        self.assertIn("printed_location_needs_visual_review", self.codes(report))
        location.update(pdf_page=2, verified_sha256="0" * 64)
        self.assertTrue({"pdf_page_out_of_range", "visual_location_stale"} <= self.codes(self.run_case()))


if __name__ == "__main__":
    unittest.main()
