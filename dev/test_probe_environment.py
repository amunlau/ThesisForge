"""Regression checks for backend evidence, exit status, and visible Linux job limits."""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "probe_environment.py"
spec = importlib.util.spec_from_file_location("probe_environment", SCRIPT)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


class RuntimeProbeTests(unittest.TestCase):
    def test_backend_child_inherits_import_policy_and_reports_loaded_module(self):
        class Flags:
            no_site = False
            no_user_site = False
            ignore_environment = False

        for isolated in (False, True):
            flags = Flags()
            flags.isolated = isolated
            with self.subTest(isolated=isolated), patch.object(sys, "flags", flags), \
                    patch.object(probe, "checked_command", return_value='{"module":"from selected environment"}') as run:
                evidence = probe.verify_backend("numpy", {}, [])
                self.assertEqual("-I" in run.call_args.args[0], isolated)
                self.assertEqual(evidence["result"]["module"], "from selected environment")

    def test_relative_import_paths_still_refer_to_original_directory(self):
        configured = os.pathsep.join(["vendor", "", "src"])
        with patch.dict(os.environ, {"PYTHONPATH": configured}), \
                patch.object(sys, "flags", isolated=False, no_site=False, no_user_site=False,
                             ignore_environment=False, safe_path=True), \
                patch.object(probe, "checked_command", return_value='{"product":11}') as run:
            self.assertTrue(probe.verify_backend("numpy", {}, [])["passed"])
        paths = run.call_args.kwargs["env"]["PYTHONPATH"].split(os.pathsep)
        self.assertEqual(paths, [os.path.abspath(p) for p in ("vendor", "", "src")])
        self.assertIn("-P", run.call_args.args[0])

    def test_mounted_subtree_and_escaped_mount_point(self):
        membership = "0::/jobs/batch/task"
        mounts = r"25 19 0:1 /jobs/batch /sys/job\040group rw - cgroup2 cgroup2 rw"
        base = Path("/sys/job group")
        self.assertEqual(probe.cgroup_directory(membership, mounts), (base / "task", base))
        self.assertIsNone(probe.cgroup_directory("0::/elsewhere", mounts))
        self.assertIsNone(probe.cgroup_directory("0::/../outside", mounts))

    def test_limit_and_headroom_can_come_from_different_ancestors(self):
        root = Path("/sys/fs/cgroup")
        files = {
            Path("/proc/self/cgroup"): "0::/batch/task",
            Path("/proc/self/mountinfo"): "25 19 0:1 / /sys/fs/cgroup rw - cgroup2 cgroup2 rw",
            root / "batch/task/memory.max": "6000",
            root / "batch/task/memory.current": "1000",
            root / "batch/task/cpu.max": "max 100000",
            root / "batch/memory.max": "8000",
            root / "batch/memory.current": "7000",
            root / "batch/cpu.max": "150000 100000",
        }

        def fixture_read(path):
            if path in files:
                return files[path]
            raise FileNotFoundError(path)

        with patch.object(Path, "read_text", fixture_read), patch.object(Path, "is_dir", return_value=True):
            limits = probe.linux_job_limits()
        self.assertEqual(limits["memory_cap_bytes"], 6000)
        self.assertEqual(limits["memory_headroom_bytes"], 1000)
        self.assertEqual(limits["cpu_quota_equivalents"], 1.5)

    def test_optional_verification_causes_failure_and_preserves_inventory(self):
        with patch.object(sys, "argv", ["probe", "--workload", "data", "--verify", "iverilog"]), \
                patch.object(probe, "external_path", return_value=[]), \
                contextlib.redirect_stdout(io.StringIO()) as stdout:
            self.assertEqual(probe.main(), 1)
        result = json.loads(stdout.getvalue())
        self.assertFalse(result["backend_checks"]["iverilog"]["passed"])
        self.assertTrue(result["workloads"]["data"]["smoke"]["passed"])

    def test_absent_optional_tools_do_not_fail_inventory(self):
        with patch.object(sys, "argv", ["probe", "--workload", "hdl"]), \
                patch.object(probe, "external_path", return_value=[]), \
                contextlib.redirect_stdout(io.StringIO()) as stdout:
            self.assertEqual(probe.main(), 0)
        result = json.loads(stdout.getvalue())
        self.assertNotIn("backend_checks", result)
        self.assertIsNone(result["workloads"]["hdl"]["smoke"]["passed"])


if __name__ == "__main__":
    unittest.main()
