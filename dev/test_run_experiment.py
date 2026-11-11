"""CLI regression checks for experiment records. All fixture data is temporary."""

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


RUNNER = Path(__file__).resolve().parents[1] / "scripts" / "run_experiment.py"


class ExperimentRunnerCLI(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="thesisforge-experiment-")
        self.addCleanup(temp.cleanup)
        self.base = Path(temp.name)
        self.cwd = self.base / "project with spaces"
        self.cwd.mkdir()

    def run_cli(self, options, command, run_dir="runs/one", env=None):
        return subprocess.run(
            [sys.executable, "-B", str(RUNNER), "--cwd", str(self.cwd),
             "--run-dir", run_dir, *options, "--", *command],
            cwd=self.base, env=env, capture_output=True, encoding="utf-8", timeout=20,
        )

    def record(self, run_dir="runs/one"):
        return json.loads((self.cwd / run_dir / "run.json").read_text(encoding="utf-8"))

    def test_success_records_argument_boundaries_logs_cwd_and_hashes(self):
        payload = b"\x00\xffsample"
        (self.cwd / "fixture.bin").write_bytes(payload)
        script = (
            "from pathlib import Path\nimport os, sys\n"
            "assert sys.argv[1:] == ['a b', 'x&y', '--', '--four']\n"
            "output = Path(os.environ['THESISFORGE_RUN_DIR']) / 'result.bin'\n"
            "output.write_bytes(Path('fixture.bin').read_bytes())\n"
            "sys.stdout.buffer.write(b'out\\x00'); sys.stderr.buffer.write(b'err')\n"
        )
        command = [sys.executable, "-c", script, "a b", "x&y", "--", "--four"]
        result = self.run_cli(["--input", "fixture.bin", "--output", "runs/one/result.bin"], command)
        self.assertEqual(result.returncode, 0, result.stderr)
        record = self.record()
        self.assertEqual(record["argv"], command)
        self.assertEqual(record["status"], "succeeded")
        self.assertTrue(record["inputs_verified_after_run"])
        self.assertEqual(record["exit_code"], 0)
        self.assertLessEqual(record["started_at"], record["finished_at"])
        self.assertGreaterEqual(record["elapsed_seconds"], record["command_elapsed_seconds"])
        for group in ("inputs", "outputs"):
            self.assertEqual(record[group][0]["sha256"], hashlib.sha256(payload).hexdigest())
            self.assertEqual(record[group][0]["bytes"], len(payload))
        directory = self.cwd / "runs/one"
        self.assertEqual((directory / record["stdout"]).read_bytes(), b"out\x00")
        self.assertEqual((directory / record["stderr"]).read_bytes(), b"err")

    def test_failure_keeps_partial_artifact_and_nonzero_exit(self):
        command = [sys.executable, "-c", "open('partial', 'wb').close(); raise SystemExit(7)"]
        result = self.run_cli(["--output", "partial"], command)
        self.assertNotEqual(result.returncode, 0)
        record = self.record()
        self.assertEqual(record["status"], "failed")
        self.assertEqual(record["exit_code"], 7)
        self.assertEqual(record["outputs"][0]["bytes"], 0)

    def test_python_placeholder_uses_invoking_executable_and_preserves_unicode_arguments(self):
        name = "试验 数据.csv"
        program = "import sys; from pathlib import Path; Path(sys.argv[1]).write_text(sys.executable, encoding='utf-8')"
        result = self.run_cli(["--output", name], ["{python}", "-c", program, name])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.cwd / name).read_text(encoding="utf-8"), sys.executable)

    def test_relative_path_entries_use_experiment_directory(self):
        tool_dir = self.cwd / "tool bin"
        tool_dir.mkdir()
        if os.name == "nt":
            executable = tool_dir / "tfprint.exe"
            shutil.copy2(Path(os.environ["SystemRoot"]) / "System32" / "cmd.exe", executable)
            arguments = ["/d", "/c", "echo project-tool"]
        else:
            executable = tool_dir / "tfprint"
            executable.write_text("#!/bin/sh\necho project-tool\n", encoding="utf-8")
            executable.chmod(0o755)
            arguments = []
        result = self.run_cli([], ["tfprint", *arguments], env=dict(os.environ, PATH="tool bin"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.cwd / "runs/one/stdout.log").read_bytes().strip(), b"project-tool")
        self.assertEqual(Path(self.record()["executable"]), executable)

    def test_exit_zero_with_missing_output_is_failed(self):
        result = self.run_cli(["--output", "missing.csv"], [sys.executable, "-c", "pass"])
        self.assertNotEqual(result.returncode, 0)
        record = self.record()
        self.assertEqual(record["exit_code"], 0)
        self.assertEqual(record["status"], "failed")
        self.assertNotIn("sha256", record["outputs"][0])
        self.assertTrue(record["errors"])

    def test_exit_zero_after_declared_input_changes_is_failed(self):
        source = self.cwd / "config.json"
        source.write_bytes(b"first")
        script = ("from pathlib import Path; src=Path('config.json'); "
                  "Path('metrics').write_bytes(src.read_bytes()); src.write_bytes(b'second')")
        result = self.run_cli(["--input", "config.json", "--output", "metrics"],
                              [sys.executable, "-c", script])
        self.assertEqual(result.returncode, 1)
        record = self.record()
        self.assertEqual(record["exit_code"], 0)
        self.assertEqual(record["status"], "failed")
        self.assertEqual(record["inputs"][0]["sha256"], hashlib.sha256(b"first").hexdigest())
        self.assertFalse(record["inputs_verified_after_run"])
        self.assertEqual(record["outputs"][0]["sha256"], hashlib.sha256(b"first").hexdigest())
        self.assertIn("config.json", " ".join(record["errors"]))

    def test_old_output_refused_before_launch(self):
        old = self.cwd / "old.csv"
        old.write_bytes(b"old")
        command = [sys.executable, "-c", "open('attempt', 'w').close(); open('old.csv', 'w').close()"]
        result = self.run_cli(["--output", "old.csv"], command)
        self.assertNotEqual(result.returncode, 0)
        record = self.record()
        self.assertEqual(record["status"], "failed")
        self.assertIsNone(record["exit_code"])
        self.assertNotIn("sha256", record["outputs"][0])
        self.assertEqual(old.read_bytes(), b"old")
        self.assertFalse((self.cwd / "attempt").exists())

    def test_rerun_cannot_replace_record(self):
        command = [sys.executable, "-c", "print(42)"]
        self.assertEqual(self.run_cli([], command).returncode, 0)
        first = (self.cwd / "runs/one/run.json").read_bytes()
        self.assertNotEqual(self.run_cli([], command).returncode, 0)
        self.assertEqual((self.cwd / "runs/one/run.json").read_bytes(), first)
        self.assertEqual(self.run_cli([], command, "runs/two").returncode, 0)
        self.assertEqual(self.record("runs/two")["status"], "succeeded")

    def test_launch_failure_has_record(self):
        result = self.run_cli([], [str(self.cwd / "absent-program")])
        self.assertNotEqual(result.returncode, 0)
        self.assertIsNone(self.record()["exit_code"])
        self.assertEqual(self.record()["status"], "failed")


if __name__ == "__main__":
    unittest.main()
