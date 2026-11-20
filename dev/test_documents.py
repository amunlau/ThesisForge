"""Document backend regressions; external TeX/Word are not required by unit tests."""
import importlib.util
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


docx = load("audit_docx")
latex = load("build_latex")
W = docx.W


def make_docx(path, body, styles="", extras=None):
    entries = {
        "[Content_Types].xml": '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
            '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
            '</Types>',
        "_rels/.rels": '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="r1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            '</Relationships>',
        "word/_rels/document.xml.rels": '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="styles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
            '</Relationships>',
        "word/document.xml": f'<w:document xmlns:w="{W}" xmlns:r="{docx.R}"><w:body>{body}</w:body></w:document>',
        "word/styles.xml": f'<w:styles xmlns:w="{W}">{styles}</w:styles>'}
    entries.update(extras or {})
    with ZipFile(path, "w") as archive:
        for name, content in entries.items():
            archive.writestr(name, content)


class DocumentAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="tf-documents-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = self.root / "thesis.docx"

    def test_dynamic_inheritance_table_and_direct_override(self):
        styles = '<w:style w:type="paragraph" w:styleId="Base"><w:pPr><w:outlineLvl w:val="1"/>' \
            '<w:ind w:firstLineChars="200"/></w:pPr></w:style>' \
            '<w:style w:type="paragraph" w:styleId="MyHeading"><w:basedOn w:val="Base"/></w:style>'
        make_docx(self.path, '<w:tbl><w:tr><w:tc><w:p><w:pPr><w:pStyle w:val="MyHeading"/>'
            '<w:ind w:firstLineChars="0"/></w:pPr><w:r><w:t>Heading in table</w:t></w:r></w:p></w:tc></w:tr></w:tbl>', styles)
        before = self.path.read_bytes()
        result = docx.audit(self.path)
        row = result["paragraphs"][0]
        self.assertEqual(row["heading_level"], 2)
        self.assertTrue(row["in_table"])
        self.assertEqual(row["style_chain"], ["MyHeading", "Base"])
        self.assertEqual(row["effective_paragraph_subset"]["ind.firstLineChars"], "0")
        self.assertEqual(before, self.path.read_bytes())

    def test_content_and_fingerprint_use_the_same_frozen_bytes(self):
        make_docx(self.path, '<w:p><w:r><w:t>old snapshot</w:t></w:r></w:p>')
        before = self.path.read_bytes()
        original = Path.read_bytes
        def changed_after_read(path):
            data = original(path)
            if path == self.path:
                make_docx(self.path, '<w:p><w:r><w:t>new on disk</w:t></w:r></w:p>')
            return data
        with patch.object(Path, "read_bytes", changed_after_read):
            report = docx.audit(self.path)
        self.assertEqual(report["input_sha256"], hashlib.sha256(before).hexdigest())
        self.assertEqual(report["paragraphs"][0]["text"], "old snapshot")

    def test_split_field_result_is_not_error(self):
        make_docx(self.path, '<w:p><w:bookmarkStart w:id="0" w:name="fig1"/><w:bookmarkEnd w:id="0"/>'
            '<w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText> REF </w:instrText></w:r>'
            '<w:r><w:instrText>fig1 </w:instrText></w:r><w:r><w:fldChar w:fldCharType="separate"/></w:r>'
            '<w:r><w:t>Figure </w:t></w:r><w:r><w:t>1</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>')
        report = docx.audit(self.path)
        self.assertEqual(report["fields"][0]["display"], "Figure 1")
        self.assertTrue(report["fields"][0]["target_present"])
        self.assertFalse(report["review_items"])

    def test_nested_fields_and_unclosed_coverage(self):
        make_docx(self.path, '<w:p><w:r><w:fldChar w:fldCharType="begin"/></w:r>'
            '<w:r><w:instrText> IF </w:instrText></w:r><w:r><w:fldChar w:fldCharType="begin"/></w:r>'
            '<w:r><w:instrText> REF missing </w:instrText></w:r><w:r><w:fldChar w:fldCharType="separate"/></w:r>'
            '<w:r><w:t>old</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>')
        report = docx.audit(self.path)
        self.assertTrue(report["fields"][0]["nested"])
        self.assertTrue(report["coverage"]["limits"])
        self.assertEqual(report["review_items"][0]["kind"], "missing_field_bookmark")

    def test_revisions_are_not_silently_accepted(self):
        make_docx(self.path, '<w:p><w:ins><w:r><w:t>new</w:t></w:r></w:ins>'
            '<w:del><w:r><w:delText>old</w:delText></w:r></w:del></w:p>')
        report = docx.audit(self.path)
        self.assertEqual(report["paragraphs"][0]["text"], "newold")
        self.assertTrue(report["tracked_changes"])
        self.assertTrue(any("revision" in x.lower() for x in report["coverage"]["limits"]))

    def test_missing_style_and_cyclic_style_report_limits(self):
        make_docx(self.path, '<w:p><w:pPr><w:pStyle w:val="Missing"/></w:pPr></w:p>',
            '<w:style w:type="paragraph" w:styleId="a"><w:basedOn w:val="b"/></w:style>'
            '<w:style w:type="paragraph" w:styleId="b"><w:basedOn w:val="a"/></w:style>')
        limits = docx.audit(self.path)["coverage"]["limits"]
        self.assertTrue(any("cycle" in x for x in limits))
        self.assertTrue(any("Missing" in x for x in limits))

    def test_strict_namespace_and_missing_header(self):
        make_docx(self.path, '<w:p><w:r><w:t>Text</w:t></w:r></w:p>'
            '<w:sectPr><w:titlePg w:val="0"/><w:headerReference w:type="default" r:id="gone"/></w:sectPr>')
        with ZipFile(self.path) as archive:
            entries = {n: archive.read(n).replace(W.encode(), docx.STRICT_W.encode()) for n in archive.namelist()}
        with ZipFile(self.path, "w") as archive:
            for name, content in entries.items():
                archive.writestr(name, content)
        result = docx.audit(self.path)
        self.assertEqual(result["sections"][0]["properties"]["titlePg.val"], "0")
        self.assertEqual(result["review_items"][0]["kind"], "missing_header_footer_part")

    def test_textbox_no_double_count(self):
        make_docx(self.path, '<w:p><w:r><w:t>Outer</w:t><w:pict><w:txbxContent><w:p><w:r><w:t>Inner</w:t>'
            '</w:r></w:p></w:txbxContent></w:pict></w:r></w:p>')
        rows = docx.audit(self.path)["paragraphs"]
        self.assertEqual([x["text"] for x in rows], ["Outer", "Inner"])
        self.assertTrue(rows[1]["in_textbox"])

    def test_numbering_definition_and_missing_reference(self):
        numbering = f'<w:numbering xmlns:w="{W}"><w:abstractNum w:abstractNumId="5">' \
            '<w:nsid w:val="11223344"/><w:lvl w:ilvl="0"><w:numFmt w:val="decimal"/></w:lvl>' \
            '</w:abstractNum><w:num w:numId="9"><w:abstractNumId w:val="5"/></w:num></w:numbering>'
        make_docx(self.path, '<w:p><w:pPr><w:numPr><w:numId w:val="9"/></w:numPr></w:pPr></w:p>'
            '<w:p><w:pPr><w:numPr><w:numId w:val="10"/></w:numPr></w:pPr></w:p>', extras={"word/numbering.xml": numbering})
        report = docx.audit(self.path)
        self.assertEqual(set(report["numbering"]["9"]["levels"]), {"0"})
        self.assertEqual(report["review_items"][0]["num_id"], "10")

    def test_utf16_dtd_is_not_expanded(self):
        bad = f'<?xml version="1.0" encoding="utf-16"?><!DOCTYPE x [<!ENTITY v "text">]>' \
            f'<w:document xmlns:w="{W}"><w:body><w:p><w:r><w:t>&v;</w:t></w:r></w:p></w:body></w:document>'
        make_docx(self.path, '', extras={"word/document.xml": bad.encode('utf-16')})
        with self.assertRaises(ValueError):
            docx.audit(self.path)

    def test_invalid_package_is_error_not_pass(self):
        self.path.write_text("not zip", encoding="utf-8")
        proc = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/audit_docx.py"), str(self.path)], capture_output=True)
        self.assertEqual(proc.returncode, 2)

    def test_strict_does_not_block_heuristic_or_revision_notes(self):
        make_docx(self.path, '<w:p><w:pPr><w:outlineLvl w:val="0"/><w:ind w:firstLineChars="200"/></w:pPr>'
            '<w:ins><w:r><w:t>Text</w:t></w:r></w:ins></w:p>')
        proc = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/audit_docx.py"), str(self.path), "--strict"],
                              capture_output=True, encoding="utf-8")
        self.assertEqual(proc.returncode, 0)
        report = json.loads(proc.stdout)
        self.assertEqual(report["status"], "REVIEW_NEEDED")
        self.assertTrue(report["coverage"]["limits"])
        self.assertFalse(report["blocking_items"])

    def test_strict_blocks_broken_reference(self):
        make_docx(self.path, '<w:p><w:fldSimple w:instr="REF missing"><w:r><w:t>1</w:t></w:r></w:fldSimple></w:p>')
        proc = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/audit_docx.py"), str(self.path), "--strict"],
                              capture_output=True, encoding="utf-8")
        self.assertEqual(proc.returncode, 1)
        self.assertTrue(json.loads(proc.stdout)["blocking_items"])

    def test_revision_branch_findings_require_view_resolution(self):
        make_docx(self.path, '<w:del><w:p><w:pPr><w:pStyle w:val="Removed"/>'
            '<w:numPr><w:numId w:val="99"/></w:numPr></w:pPr>'
            '<w:fldSimple w:instr="REF gone"><w:r><w:t>1</w:t></w:r></w:fldSimple></w:p></w:del>'
            '<w:sectPr><w:sectPrChange><w:sectPr><w:headerReference w:type="default" r:id="old"/>'
            '</w:sectPr></w:sectPrChange></w:sectPr>')
        report = docx.audit(self.path)
        self.assertFalse(report["blocking_items"])
        self.assertEqual({x["kind"] for x in report["review_items"]},
                         {"broken_style_reference", "missing_numbering", "missing_field_bookmark", "missing_header_footer_part"})
        self.assertTrue(all(x["view_dependent_context"] for x in report["review_items"]))

    def test_compatibility_branch_and_deleted_row_are_review_only(self):
        make_docx(self.path, '<mc:AlternateContent xmlns:mc="' + docx.MC + '"><mc:Choice Requires="x">'
            '<w:p><w:fldSimple w:instr="REF gone"/></w:p></mc:Choice><mc:Fallback><w:p/></mc:Fallback>'
            '</mc:AlternateContent><w:tbl><w:tr><w:trPr><w:del/></w:trPr><w:tc><w:p>'
            '<w:fldSimple w:instr="REF alsoGone"/></w:p></w:tc></w:tr></w:tbl>')
        report = docx.audit(self.path)
        self.assertFalse(report["blocking_items"])
        self.assertEqual(len(report["review_items"]), 2)
        self.assertTrue(any("AlternateContent" in item for item in report["coverage"]["limits"]))

    def test_bookmark_only_in_revision_is_not_verified_final_target(self):
        make_docx(self.path, '<w:p><w:del><w:bookmarkStart w:id="0" w:name="gone"/></w:del>'
            '<w:fldSimple w:instr="REF gone"/></w:p>')
        report = docx.audit(self.path)
        self.assertTrue(report["fields"][0]["target_view_dependent"])
        self.assertEqual(report["review_items"][0]["kind"], "view_dependent_field_bookmark")

    def test_revision_elsewhere_does_not_hide_unconditional_broken_reference(self):
        make_docx(self.path, '<w:p><w:ins><w:r><w:t>new</w:t></w:r></w:ins>'
            '<w:fldSimple w:instr="REF gone"/></w:p>')
        self.assertEqual(len(docx.audit(self.path)["blocking_items"]), 1)

    def test_output_does_not_overwrite_input(self):
        make_docx(self.path, '<w:p><w:r><w:t>ok</w:t></w:r></w:p>')
        before = self.path.read_bytes()
        proc = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/audit_docx.py"), str(self.path), "--output", str(self.path)], capture_output=True)
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(before, self.path.read_bytes())


class LatexBuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="tf-latex-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "project"
        self.source.mkdir()
        self.entry = self.source / "paper.tex"
        self.entry.write_text("document source", encoding="utf-8")
        self.output = self.root / "new build"
        self.tools = {n: {"path": n, "available": True} for n in (*latex.ENGINES, "bibtex", "biber")}

    def fake_engine(self, command, cwd, env, timeout, log_path):
        Path(log_path).write_text("fixture engine invocation", encoding="utf-8")
        if command[0] in latex.ENGINES:
            artifacts = Path(next(v.split("=", 1)[1] for v in command if v.startswith("-output-directory=")))
            (artifacts / "paper.pdf").write_bytes(b"%PDF-fixture-only")
            (artifacts / "paper.log").write_text("no warnings", encoding="utf-8")
        return {"command": command, "exit_code": 0, "timed_out": False, "log": str(log_path)}

    def test_fresh_build_and_source_preservation(self):
        (self.source / "paper.pdf").write_bytes(b"%PDF-old")
        (self.source / "figure.pdf").write_bytes(b"%PDF-real-figure")
        with patch.object(latex, "probe", return_value=self.tools), patch.object(latex, "run_step", side_effect=self.fake_engine):
            report, code = latex.build(self.entry, self.source, self.output)
        self.assertEqual(code, 0)
        self.assertFalse((self.output / "source/paper.pdf").exists())
        self.assertTrue((self.output / "source/figure.pdf").exists())
        self.assertEqual((self.source / "paper.pdf").read_bytes(), b"%PDF-old")
        self.assertEqual(report["source_changed"], [])

    def test_directory_redirect_is_rejected_without_junction_api(self):
        linked = self.source / "linked"
        linked.mkdir()
        redirected = self.root / "outside"
        redirected.mkdir()
        resolve = Path.resolve

        def simulate_redirect(path, *args, **kwargs):
            return redirected if path == linked else resolve(path, *args, **kwargs)

        with patch.object(Path, "resolve", new=simulate_redirect), \
                patch.object(Path, "is_junction", return_value=False, create=True), \
                patch.object(latex, "probe", return_value=self.tools), \
                patch.object(latex, "run_step") as run:
            with self.assertRaisesRegex(ValueError, "directory link not copied"):
                latex.build(self.entry, self.source, self.output)
        run.assert_not_called()
        self.assertFalse(self.output.exists())
        self.assertEqual(self.entry.read_text(encoding="utf-8"), "document source")

    @unittest.skipUnless(sys.platform == "win32", "Windows directory junction")
    def test_real_junction_cannot_copy_files_outside_project(self):
        import _winapi
        target = self.root / "outside"
        target.mkdir()
        sentinel = target / "external.txt"
        sentinel.write_text("outside fixture", encoding="utf-8")
        linked = self.source / "linked"
        try:
            _winapi.CreateJunction(str(target), str(linked))
        except (AttributeError, OSError) as exc:
            self.skipTest("directory junction unavailable: " + str(exc))
        self.addCleanup(linked.rmdir)
        # Emulate the old fallback while preserving a real directory junction.
        with patch.object(Path, "is_junction", return_value=False, create=True):
            with self.assertRaisesRegex(ValueError, "directory link not copied"):
                latex.snapshot(self.source, self.entry, self.output)
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "outside fixture")

    def test_bibliography_failure_does_not_accept_first_pass_pdf(self):
        def fake(command, cwd, env, timeout, log):
            result = self.fake_engine(command, cwd, env, timeout, log)
            if command[0] in latex.ENGINES:
                artifacts = Path(next(v.split("=", 1)[1] for v in command if v.startswith("-output-directory=")))
                (artifacts / "paper.aux").write_text(r"\bibdata{references}", encoding="utf-8")
            else:
                result["exit_code"] = 7
            return result
        with patch.object(latex, "probe", return_value=self.tools), patch.object(latex, "run_step", side_effect=fake):
            report, code = latex.build(self.entry, self.source, self.output)
        self.assertEqual(code, 1)
        self.assertEqual(report["status"], "BUILD_FAILED")
        self.assertIsNone(report["pdf"])
        self.assertEqual(len(report["commands"]), 2)

    def test_bibliography_without_later_tex_pass_is_incomplete(self):
        with patch.object(latex, "probe", return_value=self.tools), patch.object(latex, "run_step", side_effect=self.fake_engine):
            report, code = latex.build(self.entry, self.source, self.output, bibliography="bibtex", passes=1)
        self.assertEqual(code, 1)
        self.assertEqual(report["status"], "REVIEW_NEEDED")
        self.assertTrue(any("after the last TeX pass" in item for item in report["unresolved"]))

    def test_missing_tool_reports_not_run(self):
        self.tools["xelatex"]["available"] = False
        with patch.object(latex, "probe", return_value=self.tools):
            report, code = latex.build(self.entry, self.source, self.output)
        self.assertEqual(code, 2)
        self.assertEqual(report["rendering"], "NOT_RUN")
        self.assertFalse(self.output.exists())

    def test_missing_auto_bibliography_is_dependency_error_with_partial_receipt(self):
        for backend in ("bibtex", "biber"):
            with self.subTest(backend=backend):
                output = self.root / ("missing-" + backend)
                tools = {name: dict(value) for name, value in self.tools.items()}
                tools[backend].update(available=False, path=None)

                def fake(command, cwd, env, timeout, log):
                    result = self.fake_engine(command, cwd, env, timeout, log)
                    artifacts = Path(next(v.split("=", 1)[1] for v in command if v.startswith("-output-directory=")))
                    if backend == "biber":
                        (artifacts / "paper.bcf").write_text("fixture", encoding="utf-8")
                    else:
                        (artifacts / "paper.aux").write_text(r"\bibdata{references}", encoding="utf-8")
                    return result

                with patch.object(latex, "probe", return_value=tools), patch.object(latex, "run_step", side_effect=fake):
                    report, code = latex.build(self.entry, self.source, output)
                self.assertEqual(code, 2)
                self.assertEqual(report["status"], "TOOL_UNAVAILABLE")
                self.assertEqual(report["missing_tool"], backend)
                self.assertEqual(len(report["commands"]), 1)
                self.assertIsNone(report["pdf"])
                self.assertTrue((output / "artifacts/paper.pdf").exists())
                saved = json.loads((output / "build-report.json").read_text(encoding="utf-8"))
                self.assertEqual(saved["status"], "TOOL_UNAVAILABLE")

    def test_existing_output_refused(self):
        self.output.mkdir()
        saved = self.output / "paper.pdf"
        saved.write_bytes(b"old")
        with self.assertRaises(ValueError):
            latex.build(self.entry, self.source, self.output)
        self.assertEqual(saved.read_bytes(), b"old")

    def test_nonfinite_timeout_rejected_before_launch(self):
        for value in (float('nan'), float('inf')):
            with patch.object(latex, "probe") as probe:
                with self.assertRaises(ValueError):
                    latex.build(self.entry, self.source, self.output, timeout=value)
                probe.assert_not_called()
        self.assertFalse(self.output.exists())

    def test_unresolved_references_never_claim_clean_build(self):
        def fake(command, cwd, env, timeout, log):
            result = self.fake_engine(command, cwd, env, timeout, log)
            artifacts = Path(next(v.split("=", 1)[1] for v in command if v.startswith("-output-directory=")))
            (artifacts / "paper.log").write_text("LaTeX Warning: There were undefined references.", encoding="utf-8")
            return result
        with patch.object(latex, "probe", return_value=self.tools), patch.object(latex, "run_step", side_effect=fake):
            report, code = latex.build(self.entry, self.source, self.output)
        self.assertEqual(code, 1)
        self.assertEqual(report["status"], "REVIEW_NEEDED")

    def test_timeout_kills_step_and_preserves_log(self):
        result = latex.run_step([sys.executable, "-c", "import time; time.sleep(20)"], self.root, None, 0.1, self.root / "timeout.log")
        self.assertTrue(result["timed_out"])
        self.assertNotEqual(result["exit_code"], 0)
        self.assertTrue(result["cleanup"]["root_stopped"])

    @unittest.skipUnless(sys.platform == "win32", "Windows process-tree fallback")
    def test_timeout_helper_failure_still_kills_root_and_records_partial_cleanup(self):
        with patch.object(latex.subprocess, "run", side_effect=OSError("taskkill unavailable")):
            result = latex.run_step([sys.executable, "-c", "import time; time.sleep(20)"],
                                    self.root, None, 0.1, self.root / "fallback.log")
        self.assertTrue(result["timed_out"])
        self.assertTrue(result["cleanup"]["root_stopped"])
        self.assertEqual(result["cleanup"]["status"], "partial")
        self.assertTrue(result["cleanup"]["errors"])


if __name__ == "__main__":
    unittest.main()
