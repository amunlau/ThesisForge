"""Exercise the matrix through its CLI with real foreground child processes."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch


CLI = Path(__file__).resolve().parents[1] / "scripts" / "run_matrix.py"
WORKLOAD = """from pathlib import Path
import sys
value = Path(sys.argv[1]).read_text()
if value == 'fail': raise SystemExit(7)
Path(sys.argv[3]).write_text(str(int(value) * int(sys.argv[2])))
"""


class MatrixCLI(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix="thesisforge-matrix-")
        self.addCleanup(directory.cleanup)
        self.project = Path(directory.name)
        (self.project / "compute.py").write_text(WORKLOAD, encoding="utf-8")
        self.plan = {"inputs": ["compute.py"], "outputs": ["value.txt"], "cases": []}
        for name, factor in [("low", 2), ("high", 3)]:
            source = name + ".txt"
            (self.project / source).write_text("5")
            self.plan["cases"].append({"id": name, "inputs": [source], "argv":
                                       ["{python}", "-B", "compute.py", source, str(factor),
                                        "{run_dir}/value.txt"]})
        self.manifest = self.project / "matrix.json"
        self.root = self.project / "matrix runs"

    def run_cli(self, code=0):
        self.manifest.write_text(json.dumps(self.plan), encoding="utf-8")
        proc = subprocess.run([sys.executable, "-B", "-I", str(CLI), str(self.manifest),
                               "--run-dir", self.root.name],
                              capture_output=True, encoding="utf-8", timeout=20)
        self.assertEqual(proc.returncode, code, proc.stdout + proc.stderr)

    def rows(self):
        return json.loads((self.root / "index.json").read_text(encoding="utf-8"))["cases"]

    def test_reuse_then_parameter_input_and_artifact_changes(self):
        self.run_cli()
        self.assertEqual((self.root / "case-low/1/value.txt").read_text(), "10")
        self.assertEqual((self.root / "case-high/1/value.txt").read_text(), "15")
        self.run_cli()
        self.assertTrue(all(row["reused"] for row in self.rows().values()))
        self.plan["cases"][0]["argv"][-2] = "8"
        self.run_cli()
        self.assertEqual((self.root / "case-low/2/value.txt").read_text(), "40")
        self.assertTrue(self.rows()["high"]["reused"])
        (self.project / "high.txt").write_text("7")
        self.run_cli()
        self.assertEqual((self.root / "case-high/2/value.txt").read_text(), "21")
        self.assertTrue(self.rows()["low"]["reused"])
        (self.root / "case-high/2/value.txt").write_text("99")
        self.run_cli()
        self.assertEqual((self.root / "case-high/3/value.txt").read_text(), "21")
        self.assertEqual((self.root / "case-high/2/value.txt").read_text(), "99")

    def test_failed_case_retained_and_only_it_retried(self):
        (self.project / "low.txt").write_text("fail")
        self.run_cli(1)
        rows = self.rows()
        self.assertEqual(rows["low"]["status"], "failed")
        self.assertEqual(rows["high"]["status"], "succeeded")
        record = self.root / rows["low"]["record"]
        failure = record.read_bytes()
        self.assertEqual(json.loads(failure)["exit_code"], 7)
        (self.project / "low.txt").write_text("5")
        self.run_cli()
        self.assertTrue(self.rows()["high"]["reused"])
        self.assertEqual(record.read_bytes(), failure)
        self.assertEqual((self.root / "case-low/2/value.txt").read_text(), "10")

    def test_partial_attempts_and_shared_code_change(self):
        self.run_cli()
        # Simulate termination before the child wrote its run.json.
        (self.root / "case-low/2").mkdir()
        self.run_cli()
        self.assertTrue(self.rows()["high"]["reused"])
        self.assertEqual((self.root / "case-low/3/value.txt").read_text(), "10")
        code = self.project / "compute.py"
        code.write_text(WORKLOAD + "\n# updated source\n")
        self.run_cli()
        self.assertTrue(all(not row["reused"] for row in self.rows().values()))

    def test_directory_collision_records_terminal_failure_and_unstarted_work(self):
        self.run_cli()
        self.plan["cases"].extend(dict(self.plan["cases"][0], id=key) for key in ("blocked", "later"))
        conflict = self.root / "case-blocked"
        conflict.write_text("occupied")
        self.run_cli(2)
        index = json.loads((self.root / "index.json").read_text(encoding="utf-8"))
        self.assertEqual(index["status"], "failed")
        self.assertIn("case-blocked", index["error"])
        rows = index["cases"]
        self.assertTrue(rows["low"]["reused"])
        self.assertEqual(rows["blocked"]["status"], "failed")
        self.assertEqual(rows["blocked"]["error"], index["error"])
        self.assertEqual(rows["later"]["status"], "not_started")
        self.assertFalse((self.root / "case-later").exists())
        conflict.rename(self.root / "saved-conflict")
        self.run_cli()
        self.assertTrue(all(row["status"] == "succeeded" for row in self.rows().values()))

    def test_matrix_end_rechecks_earlier_inputs(self):
        code = self.project / "compute.py"
        code.write_text(WORKLOAD + "\nif sys.argv[1] == 'high.txt': Path('low.txt').write_text('7')\n")
        self.run_cli(1)
        self.assertEqual(self.rows()["low"]["status"], "failed")
        self.assertEqual(self.rows()["high"]["status"], "succeeded")
        self.run_cli()
        self.assertEqual((self.root / "case-low/2/value.txt").read_text(), "14")
        self.assertTrue(self.rows()["high"]["reused"])

    def test_invalid_manifest_launches_no_cells(self):
        self.plan["cases"][1]["id"] = self.plan["cases"][0]["id"]
        self.run_cli(2)
        self.assertFalse(self.root.exists())
        self.plan["cases"][1]["id"] = "high"
        self.plan["outputs"] = ["../value.txt"]
        self.run_cli(2)
        self.assertFalse(self.root.exists())

    def test_concurrent_driver_cannot_claim_active_matrix(self):
        code = self.project / "compute.py"
        gate = ("import time\nfrom pathlib import Path\nPath('started').touch()\n"
                "deadline = time.monotonic() + 12\n"
                "while not Path('release').exists() and time.monotonic() < deadline: time.sleep(.02)\n")
        code.write_text(gate + WORKLOAD)
        self.manifest.write_text(json.dumps(self.plan), encoding="utf-8")
        command = [sys.executable, "-B", str(CLI), str(self.manifest), "--run-dir", self.root.name]
        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as first:
            try:
                deadline = time.monotonic() + 10
                while not (self.project / "started").exists() and time.monotonic() < deadline:
                    time.sleep(.02)
                self.assertTrue((self.project / "started").exists())
                self.assertEqual(self.rows()["low"]["status"], "running")
                self.assertEqual(self.rows()["high"]["status"], "pending")
                contender = subprocess.run(command, capture_output=True, timeout=3)
                self.assertEqual(contender.returncode, 2, contender.stderr)
            finally:
                (self.project / "release").touch()
                out, err = first.communicate(timeout=5)
            self.assertEqual(first.returncode, 0, (out, err))
        self.run_cli()
        self.assertTrue(all(row["reused"] for row in self.rows().values()))

    def test_empty_argument_is_preserved_and_reusable(self):
        self.plan["cases"][0]["argv"].append("")
        self.run_cli()
        record = json.loads((self.root / self.rows()["low"]["record"]).read_text(encoding="utf-8"))
        self.assertEqual(record["argv"][-1], "")
        self.run_cli()
        self.assertTrue(self.rows()["low"]["reused"])

    def test_matrix_fingerprints_executable_from_project_relative_path(self):
        spec = importlib.util.spec_from_file_location("thesisforge_matrix", CLI)
        matrix = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(matrix)
        tools = self.project / "local tools"
        tools.mkdir()
        executable = tools / ("test-tool.exe" if os.name == "nt" else "test-tool")
        executable.touch()
        executable.chmod(0o755)
        with patch.dict(os.environ, {"PATH": tools.name}):
            command, files = matrix.invocation(self.project, self.root, ["test-tool", "a b"], [])
        self.assertEqual(Path(command[0]), executable)
        self.assertEqual(command[1:], ["a b"])
        self.assertEqual(files, [executable])

    def test_legacy_evidence_is_reusable_without_attesting_historical_input_check(self):
        self.run_cli()
        path = self.root / self.rows()["low"]["record"]
        record = json.loads(path.read_text(encoding="utf-8"))
        del record["inputs_verified_after_run"]
        path.write_text(json.dumps(record), encoding="utf-8")
        fixture = self.project / "low.txt"
        original = fixture.read_bytes()
        fixture.write_bytes(b"modified")
        fixture.write_bytes(original)
        self.run_cli()
        rows = self.rows()
        self.assertTrue(rows["low"]["reused"])
        self.assertIsNone(rows["low"]["inputs_verified_after_run"])
        self.assertTrue(rows["high"]["inputs_verified_after_run"])
        self.assertNotIn("inputs_verified_after_run", json.loads(path.read_text(encoding="utf-8")))
        record["inputs_verified_after_run"] = False
        path.write_text(json.dumps(record), encoding="utf-8")
        self.run_cli()
        self.assertFalse(self.rows()["low"]["reused"])
        self.assertTrue(self.rows()["low"]["inputs_verified_after_run"])

    def test_impossible_file_and_parent_outputs_rejected_before_start(self):
        self.plan["outputs"] = ["raw/metrics.csv", "raw"]
        self.run_cli(2)
        self.assertFalse(self.root.exists())

    def test_repeated_json_field_cannot_silently_replace_command(self):
        self.manifest.write_text('{"outputs":["value.txt"],"cases":[{"id":"low",'
                                 '"argv":["proposed"],"argv":["baseline"]}]}', encoding="utf-8")
        proc = subprocess.run([sys.executable, "-B", str(CLI), str(self.manifest),
                               "--run-dir", self.root.name], capture_output=True, encoding="utf-8")
        self.assertEqual(proc.returncode, 2, proc.stderr)
        self.assertIn("argv", proc.stderr)
        self.assertFalse(self.root.exists())

    def test_interrupt_marks_started_and_unstarted_cases(self):
        spec = importlib.util.spec_from_file_location("thesisforge_matrix", CLI)
        run_matrix = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(run_matrix)
        self.manifest.write_text(json.dumps(self.plan), encoding="utf-8")
        parsed = run_matrix.load_plan(self.manifest)
        with run_matrix.exclusive_root(self.root), patch.object(run_matrix, "run", side_effect=KeyboardInterrupt):
            self.assertEqual(run_matrix.execute(self.manifest, self.root, *parsed), 130)
        self.assertEqual(self.rows()["low"]["status"], "interrupted")
        self.assertEqual(self.rows()["high"]["status"], "not_started")


if __name__ == "__main__":
    unittest.main()
