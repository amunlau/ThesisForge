"""Validate adapter failure handling with an explicitly synthetic renderer."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from types import SimpleNamespace
import unittest
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/render_diagram.py"
SPEC = importlib.util.spec_from_file_location("render_diagram_tested", SCRIPT)
RENDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RENDER)
STUB = '''import pathlib,sys
if '--version' in sys.argv:
    print('synthetic-test-renderer 1'); raise SystemExit(0)
source=pathlib.Path(sys.argv[sys.argv.index('-i')+1]).read_text(encoding='utf-8')
output=pathlib.Path(sys.argv[sys.argv.index('-o')+1])
if source=='fail': raise SystemExit(3)
if source=='missing': raise SystemExit(0)
if source=='invalid': output.write_text('not SVG'); raise SystemExit(0)
output.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 30"><text x="1" y="20">demo</text></svg>',encoding='utf-8')
'''
TREE_STUB = '''import pathlib,subprocess,sys,time
root=pathlib.Path(__file__).parent
version='--version' in sys.argv
if (version and (root/'version-timeout').exists()) or (not version and (root/'export-timeout').exists()):
    child="import pathlib,time,sys; root=pathlib.Path(sys.argv[1]); (root/'child.ready').write_text(str(__import__('os').getpid())); time.sleep(2); (root/'child.survived').write_text('orphan')"
    subprocess.Popen([sys.executable,'-c',child,str(root)])
    time.sleep(10)
if version:
    print('synthetic-test-renderer 1'); raise SystemExit(0)
output=pathlib.Path(sys.argv[sys.argv.index('-o')+1])
output.write_text('<svg xmlns="http://www.w3.org/2000/svg"/>',encoding='utf-8')
'''


class RenderDiagramTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(prefix="thesisforge-diagram-")
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.stub = self.root / "test renderer.py"
        self.stub.write_text(STUB, encoding="utf-8")
        self.source = self.root / "原图 & specimen.mmd"
        self.source.write_text("graph TD; A-->B", encoding="utf-8")

    def invoke(self, output, *args):
        result = subprocess.run([sys.executable, "-B", str(SCRIPT), str(self.source), "--backend", "mermaid",
                                 "--program", sys.executable, "--entry", str(self.stub), "--output-dir", str(output), *args],
                                capture_output=True, encoding="utf-8", timeout=15)
        return result, json.loads(result.stdout)

    def test_success_has_identity_and_never_claims_visual_or_semantic_acceptance(self):
        original = self.source.read_bytes()
        result, record = self.invoke(self.root / "图形 output")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(record["status"], "exported_not_visually_verified")
        self.assertEqual(record["inspection"]["text_nodes"], 1)
        self.assertEqual(record["semantic_review"], "not_run")
        self.assertEqual(self.source.read_bytes(), original)
        self.assertTrue((self.root / "图形 output/render.json").is_file())

    def test_existing_directory_cannot_supply_a_stale_success(self):
        output = self.root / "existing"
        output.mkdir()
        old = output / "figure.svg"
        old.write_bytes(b"old PDF/figure must not be trusted")
        result, record = self.invoke(output)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(record["status"], "failed")
        self.assertEqual(old.read_bytes(), b"old PDF/figure must not be trusted")
        self.assertFalse((output / "render.json").exists())

    def test_failure_missing_and_invalid_outputs_are_not_success(self):
        for mode in ("fail", "missing", "invalid"):
            with self.subTest(mode=mode):
                self.source.write_text(mode, encoding="utf-8")
                result, record = self.invoke(self.root / mode)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(record["status"], "failed")
                self.assertTrue((self.root / mode / "render.json").is_file())

    def test_standard_external_svg_doctype_is_allowed_without_loading_dtd(self):
        svg = self.root / "external.svg"
        for uri in ("http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd", "file:///nonexistent-thesisforge-dtd.dtd"):
            with self.subTest(uri=uri):
                svg.write_text('<?xml version="1.0"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "' + uri + '"><svg xmlns="http://www.w3.org/2000/svg"><text>demo</text></svg>', encoding="utf-8")
                result = RENDER.inspect_output(svg, "svg")
                self.assertEqual(result["text_nodes"], 1)
                self.assertEqual(result["visual_review"], "not_run")

    def test_entity_declarations_are_rejected_in_utf8_and_utf16(self):
        svg = self.root / "entity.svg"
        for encoding in ("utf-8", "utf-16", "utf-16-le", "utf-16-be"):
            for declaration in ('<!ENTITY payload "unsafe">', '<!ENTITY % payload "unsafe">', '<!ENTITY payload SYSTEM "file:///private-data">'):
                with self.subTest(encoding=encoding, declaration=declaration):
                    xml_encoding = "UTF-8" if encoding == "utf-8" else "UTF-16"
                    body = '<?xml version="1.0" encoding="' + xml_encoding + '"?><!DOCTYPE svg [' + declaration + ']><svg xmlns="http://www.w3.org/2000/svg"/>'
                    svg.write_bytes(body.encode(encoding))
                    with self.assertRaisesRegex(ValueError, "entity declarations"):
                        RENDER.inspect_output(svg, "svg")

    def test_utf16_svg_with_external_doctype_and_predefined_entity_is_allowed(self):
        svg = self.root / "normal.svg"
        svg.write_bytes(('<?xml version="1.0" encoding="UTF-16"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"><svg xmlns="http://www.w3.org/2000/svg"><text>A &amp; B</text></svg>').encode("utf-16"))
        self.assertEqual(RENDER.inspect_output(svg, "svg")["text_nodes"], 1)

    def test_export_timeout_cleans_actual_child_and_records_receipt(self):
        self.stub.write_text(TREE_STUB, encoding="utf-8")
        (self.root / "export-timeout").touch()
        output = self.root / "timed out"
        result, record = self.invoke(output, "--timeout", "0.8")
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(record["execution"]["status"], "timeout")
        self.assertEqual(record["execution"]["cleanup"]["status"], "completed_within_scope", record)
        self.assertTrue(record["execution"]["cleanup"]["root_exited"])
        self.assertFalse(record["execution"]["cleanup"]["descendants_independently_verified"])
        self.assertTrue((self.root / "child.ready").is_file(), "The test must actually launch its child")
        time.sleep(1.7)
        self.assertFalse((self.root / "child.survived").exists(), "Timed-out child was left running")
        self.assertEqual(json.loads((output / "render.json").read_text(encoding="utf-8"))["execution"], record["execution"])

    def test_version_probe_timeout_also_cleans_actual_child(self):
        self.stub.write_text(TREE_STUB, encoding="utf-8")
        (self.root / "version-timeout").touch()
        result, record = self.invoke(self.root / "version probe", "--timeout", "0.8")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(record["version_probe"]["status"], "timeout")
        self.assertEqual(record["version_probe"]["cleanup"]["status"], "completed_within_scope", record)
        self.assertTrue((self.root / "child.ready").exists())
        time.sleep(1.7)
        self.assertFalse((self.root / "child.survived").exists())
        self.assertEqual(record["visual_review"], "not_run")

    def test_cleanup_failure_is_reported_partial_even_if_root_is_killed(self):
        process = mock.Mock(pid=987654321)
        process.poll.return_value = None
        process.wait.return_value = 0
        if os.name == "nt":
            patcher = mock.patch.object(RENDER.subprocess, "run", return_value=SimpleNamespace(returncode=1, stdout=b"", stderr=b"denied"))
        else:
            patcher = mock.patch.object(RENDER.os, "killpg", side_effect=PermissionError("denied"))
        with patcher:
            result = RENDER.terminate_process_tree(process)
        self.assertEqual(result["status"], "partial")
        self.assertTrue(result["root_exited"])
        process.kill.assert_called_once_with()

    def test_process_is_isolated_using_platform_specific_option(self):
        process = mock.Mock(pid=987654321)
        process.wait.return_value = 0
        with mock.patch.object(RENDER.subprocess, "Popen", return_value=process) as popen:
            execution = RENDER.run_process(["synthetic"], 1, subprocess.DEVNULL, subprocess.DEVNULL)
        options = popen.call_args.kwargs
        if os.name == "nt":
            self.assertTrue(options["creationflags"] & subprocess.CREATE_NEW_PROCESS_GROUP)
            self.assertTrue(options["creationflags"] & subprocess.CREATE_NO_WINDOW)
        else:
            self.assertTrue(options["start_new_session"])
        self.assertEqual(execution["status"], "completed")


if __name__ == "__main__":
    unittest.main()
