"""Evidence extraction must not turn comments, stale fields or views into edits."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/compare_manuscripts.py"
spec = importlib.util.spec_from_file_location("tf_comparison", SCRIPT)
api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api)
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def word_file(path, body, comments=None, extra=None):
    with ZipFile(path, "w") as archive:
        archive.writestr("word/document.xml", f'<w:document xmlns:w="{W}"><w:body>{body}</w:body></w:document>')
        if comments is not None:
            archive.writestr("word/comments.xml", f'<w:comments xmlns:w="{W}">{comments}</w:comments>')
        for name, data in (extra or {}).items():
            archive.writestr(name, data)


class ManuscriptComparisonTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory(prefix="tf-revision-")
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)

    def cli(self, *args):
        return subprocess.run([sys.executable, "-B", str(SCRIPT), *map(str, args)],
                              capture_output=True, cwd=self.root, timeout=20)

    def text(self, name, text):
        path = self.root / name
        path.write_text(text, encoding="utf-8")
        return path

    def test_two_actual_versions_have_hashes_and_exact_changed_spans(self):
        old = self.text("原稿.txt", "条件不变\n时延 10 ms\n结论保持\n")
        new = self.text("修改稿.txt", "条件不变\n时延 12 ms\n结论保持\n")
        before, after = api.extract_document(old), api.extract_document(new)
        report = api.compare_snapshots(before, after)
        self.assertTrue(report["source_bytes_differ"])
        self.assertEqual(len(report["changes"]), 1)
        change = report["changes"][0]
        self.assertEqual(change["before"][0]["text"], "时延 10 ms")
        self.assertEqual(change["after"][0]["locator"]["line"], 2)
        self.assertEqual(before["source"]["sha256"], hashlib.sha256(old.read_bytes()).hexdigest())
        self.assertEqual(report["semantic_review"], "not_run")

    def test_tracking_views_do_not_accept_or_modify_source(self):
        path = self.root / "修改.docx"
        word_file(path, '<w:p><w:r><w:t>结果 </w:t></w:r><w:del><w:r><w:delText>10</w:delText></w:r></w:del>'
                  '<w:ins><w:r><w:t>12</w:t></w:r></w:ins><w:r><w:t> ms</w:t></w:r></w:p>')
        raw = path.read_bytes()
        self.assertEqual(api.extract_document(path, "original")["units"][0]["text"], "结果 10 ms")
        self.assertEqual(api.extract_document(path, "final")["units"][0]["text"], "结果 12 ms")
        self.assertEqual(raw, path.read_bytes())

    def test_comments_are_distinct_from_body_and_have_anchor_ids(self):
        path = self.root / "review.docx"
        word_file(path, '<w:p><w:commentRangeStart w:id="7"/><w:r><w:t>已有定义</w:t></w:r>'
                  '<w:r><w:commentReference w:id="7"/></w:r></w:p>',
                  '<w:comment w:id="7" w:author="专家甲"><w:p><w:r><w:t>请补实验</w:t></w:r></w:p></w:comment>')
        result = api.extract_document(path)
        self.assertEqual([u["channel"] for u in result["units"]], ["body", "comment"])
        self.assertEqual(result["units"][0]["locator"]["comment_anchor_ids"], ["7"])
        self.assertEqual(result["units"][1]["locator"]["comment_id"], "7")

    def test_tables_textboxes_and_headers_are_located_without_double_counting(self):
        path = self.root / "parts.docx"
        word_file(path, '<w:tbl><w:tr><w:tc><w:p><w:r><w:t>表中数值</w:t></w:r></w:p></w:tc></w:tr></w:tbl>'
                  '<w:p><w:r><w:t>外层</w:t></w:r><w:txbxContent><w:p><w:r><w:t>文本框</w:t></w:r></w:p></w:txbxContent></w:p>',
                  extra={"word/header1.xml": f'<w:hdr xmlns:w="{W}"><w:p><w:r><w:t>页眉</w:t></w:r></w:p></w:hdr>'})
        units = api.extract_document(path)["units"]
        self.assertEqual([u["text"] for u in units], ["表中数值", "外层", "文本框", "页眉"])
        self.assertTrue(units[0]["locator"]["inside_table"])
        self.assertTrue(units[2]["locator"]["inside_textbox"])
        self.assertEqual(units[3]["channel"], "supplement")

    def test_move_wrappers_and_whole_paragraph_revisions_follow_view(self):
        path = self.root / "moves.docx"
        word_file(path, '<w:moveFrom><w:p><w:r><w:t>原位置</w:t></w:r></w:p></w:moveFrom>'
                  '<w:moveTo><w:p><w:r><w:t>新位置</w:t></w:r></w:p></w:moveTo>')
        self.assertEqual([u["text"] for u in api.extract_document(path, "original")["units"]], ["原位置"])
        self.assertEqual([u["text"] for u in api.extract_document(path, "final")["units"]], ["新位置"])

    def test_property_revisions_are_local_projection_ambiguities(self):
        path = self.root / "table-revisions.docx"
        word_file(path, '<w:p><w:r><w:t>普通段落</w:t></w:r></w:p>'
                  '<w:tbl><w:tr><w:trPr><w:del w:id="1"/></w:trPr><w:tc><w:p><w:r><w:t>删除行</w:t></w:r></w:p></w:tc></w:tr>'
                  '<w:tr><w:tc><w:tcPr><w:cellIns w:id="2"/></w:tcPr><w:p><w:r><w:t>修订单元格</w:t></w:r></w:p></w:tc></w:tr>'
                  '<w:tr><w:tc><w:tcPr><w:vMerge w:val="restart"/></w:tcPr><w:p><w:r><w:t>普通合并单元格</w:t></w:r></w:p></w:tc></w:tr></w:tbl>'
                  '<w:p><w:pPr><w:rPr><w:del w:id="3"/></w:rPr></w:pPr><w:r><w:t>段落标记修订</w:t></w:r></w:p>')
        for view in ("original", "final"):
            with self.subTest(view=view):
                units = api.extract_document(path, view)["units"]
                self.assertNotIn("projection_ambiguities", units[0]["locator"])
                self.assertEqual(units[1]["locator"]["projection_ambiguities"], ["table_row_revision"])
                self.assertEqual(units[2]["locator"]["projection_ambiguities"], ["table_cell_revision"])
                self.assertNotIn("projection_ambiguities", units[3]["locator"])
                self.assertEqual(units[4]["locator"]["projection_ambiguities"], ["paragraph_mark_revision"])

    def test_comment_only_change_is_not_body_change(self):
        old, new = self.root / "old.docx", self.root / "new.docx"
        body = '<w:p><w:r><w:t>正文未改</w:t></w:r></w:p>'
        word_file(old, body)
        word_file(new, body, '<w:comment w:id="1"><w:p><w:r><w:t>已补实验</w:t></w:r></w:p></w:comment>')
        changes = api.compare_snapshots(api.extract_document(old), api.extract_document(new))["changes"]
        self.assertEqual(changes[0]["after"][0]["channel"], "comment")
        self.assertFalse(changes[0]["before"])

    def test_nontext_changes_are_not_claimed_unchanged_document(self):
        old, new = self.root / "old.docx", self.root / "new.docx"
        word_file(old, '<w:p><w:r><w:t>same</w:t></w:r></w:p>')
        word_file(new, '<w:p><w:pPr><w:spacing w:after="240"/></w:pPr><w:r><w:t>same</w:t></w:r></w:p>')
        report = api.compare_snapshots(api.extract_document(old), api.extract_document(new))
        self.assertTrue(report["extracted_text_equal"])
        self.assertTrue(report["source_bytes_differ"])
        self.assertEqual(report["visual_review"], "not_run")

    def test_dtd_and_bad_zip_are_input_error_not_success(self):
        path = self.root / "bad.docx"
        path.write_bytes(b"not a zip")
        self.assertEqual(self.cli("snapshot", path, "--output", self.root / "out.json").returncode, 2)
        with ZipFile(path, "w") as archive:
            archive.writestr("word/document.xml", '<!DOCTYPE x [<!ENTITY x "oops">]><x/>')
        self.assertEqual(self.cli("snapshot", path, "--output", self.root / "out.json").returncode, 2)
        self.assertFalse((self.root / "out.json").exists())

    def test_wrong_main_xml_root_is_not_a_valid_empty_document(self):
        path = self.root / "wrong.docx"
        with ZipFile(path, "w") as archive:
            archive.writestr("word/document.xml", '<not-a-word-document/>')
        result = self.cli("snapshot", path, "--output", self.root / "out.json")
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.root / "out.json").exists())

    def test_alternate_compatibility_branches_cannot_supply_body_evidence(self):
        path = self.root / "alternate.docx"
        word_file(path, '<w:p><w:r><w:t>确定可读</w:t></w:r></w:p>'
                  '<mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006">'
                  '<mc:Choice Requires="w14"><w:p><w:r><w:t>一种版本</w:t></w:r></w:p></mc:Choice>'
                  '<mc:Fallback><w:p><w:r><w:t>另一个版本</w:t></w:r></w:p></mc:Fallback></mc:AlternateContent>')
        result = api.extract_document(path)
        self.assertEqual([u["text"] for u in result["units"]], ["确定可读"])
        self.assertEqual(result["coverage"]["objects"]["unresolved_alternate_content"], 1)
        self.assertTrue(any("excluded" in note for note in result["coverage"]["notes"]))

    def test_standalone_markdown_retains_version_view_and_comment_channel(self):
        old, new = self.root / "old.docx", self.root / "new.docx"
        word_file(old, '<w:p><w:r><w:t>原文</w:t></w:r></w:p>')
        word_file(new, '<w:p><w:r><w:t>原文</w:t></w:r></w:p>',
                  '<w:comment w:id="1"><w:p><w:r><w:t>声明</w:t></w:r></w:p></w:comment>')
        report = api.compare_snapshots(api.extract_document(old), api.extract_document(new))
        text = api.comparison_markdown(report)
        self.assertIn(report["before"]["sha256"], text)
        self.assertIn("final", text)
        self.assertIn("comment", text)

    def test_bom_legacy_encoding_and_unexpanded_tex_are_explicit(self):
        path = self.root / "chapter.tex"
        path.write_bytes("\ufeff\\input{other}\n原文".encode("utf-8"))
        result = api.extract_document(path)
        self.assertEqual(result["units"][0]["text"], "\\input{other}")
        self.assertIn("not expanded", result["coverage"]["notes"][0])
        path.write_bytes("中文原稿".encode("gb18030"))
        with self.assertRaises(UnicodeError):
            api.extract_document(path)
        self.assertEqual(api.extract_document(path, encoding="gb18030")["units"][0]["text"], "中文原稿")

    def test_empty_input_does_not_claim_semantic_or_visual_acceptance(self):
        path = self.text("blank.txt", "\n \n")
        result = api.extract_document(path)
        self.assertFalse(result["units"])
        self.assertEqual(result["semantic_review"], "not_run")

    def test_cli_preserves_input_and_refuses_existing_outputs(self):
        old, new = self.text("old.md", "原句"), self.text("new.md", "新句")
        originals = (old.read_bytes(), new.read_bytes())
        output = self.root / "对照"
        p = self.cli("compare", old, new, "--output-dir", output)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(set(x.name for x in output.iterdir()), {"before.json", "after.json", "changes.json", "changes.md"})
        self.assertEqual(self.cli("compare", old, new, "--output-dir", output).returncode, 2)
        self.assertEqual(self.cli("snapshot", old, "--output", old).returncode, 2)
        self.assertEqual((old.read_bytes(), new.read_bytes()), originals)

    def test_markdown_output_does_not_insert_raw_html_or_table_cells(self):
        value = api.markdown_text('<script>x</script> [link](x) |\ntext')
        self.assertNotIn("<script>", value)
        self.assertIn("\\|", value)
        self.assertIn("\\[", value)


try:
    import pymupdf as fitz
except ImportError:
    try:
        import fitz
    except ImportError:
        fitz = None


class PDFEvidenceTests(unittest.TestCase):
    @unittest.skipIf(fitz is None, "PyMuPDF is optional")
    def test_pdf_page_label_is_not_inferred_printed_page_and_annotations_are_separate(self):
        with tempfile.TemporaryDirectory(prefix="tf-pdf-") as folder:
            path = Path(folder) / "reviews.pdf"
            with fitz.open() as document:
                page = document.new_page()
                page.insert_text((72, 72), "Figure 1. Actual result")
                annotation = page.add_text_annot((90, 100), "Please state the sample size.")
                annotation.set_info(title="Reviewer 1")
                document.new_page()
                document.set_page_labels([{"startpage": 0, "prefix": "", "style": "r", "firstpagenum": 1}])
                document.save(path)
            snapshot = api.extract_document(path)
            self.assertEqual(snapshot["coverage"]["pages_read"], 2)
            self.assertEqual(snapshot["coverage"]["pages_without_extracted_text"], [2])
            body, comment = snapshot["units"][:2]
            self.assertEqual(body["locator"]["pdf_page"], 1)
            self.assertEqual(body["locator"]["pdf_label"], "i")
            self.assertIsNone(body["locator"]["printed_page"])
            self.assertIsNone(body["locator"]["printed_line"])
            self.assertEqual(comment["channel"], "comment")
            self.assertEqual(comment["text"], "Please state the sample size.")


if __name__ == "__main__":
    unittest.main()
