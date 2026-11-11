"""Regression tests for pairing predeclared units and recomputing recorded NoC results."""

import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "compare_pairs.py"
sys.path.insert(0, str(SCRIPT.parent))
from compare_pairs import records


class PairedTests(unittest.TestCase):
    def csv_file(self, contents):
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="",
                                         suffix=".csv", delete=False) as stream:
            stream.write(contents)
        path = Path(stream.name)
        self.addCleanup(path.unlink)
        return str(path)

    def run_pair(self, plan, datasets, *args):
        return subprocess.run([sys.executable, "-B", str(SCRIPT), "--plan", plan, "--data",
                               *datasets, "--unit", "seed", "--candidate", "a", "--baseline",
                               "b", "--value", "v", *args], capture_output=True, text=True)

    def test_pair_independently_of_row_order(self):
        plan = self.csv_file("seed\n01\n02\n")
        header = "seed,method,v,count,trace\n"
        first = self.csv_file(header + "02,b,6,2,y\n01,a,3,1,x\n")
        second = self.csv_file(header + "01,b,8,2,x\n02,a,2,2,y\n")
        result = self.run_pair(plan, [first, second], "--denominator", "count", "--match", "trace")
        self.assertEqual(0, result.returncode, result.stderr)
        group = json.loads(result.stdout)["groups"][0]
        self.assertEqual([-1.0, -2.0], [pair["difference"] for pair in group["pairs"]])
        self.assertEqual(-1.5, group["mean_difference"])
        self.assertAlmostEqual(2 ** -0.5, group["sd_difference"])

    def test_invalid_data_cannot_generate_summary(self):
        plan = self.csv_file("seed\n01\n02\n")
        head = "seed,method,v,count,trace\n"
        valid = "01,a,1,1,x\n01,b,1,1,x\n02,a,2,1,y\n02,b,1,1,y\n"
        for cause, bad in {
            "missing": valid.split("02,a")[0],  # both observations missing for a planned unit
            "duplicate": valid + "02,a,2,1,y\n",
            "unplanned": valid + "03,b,1,1,z\n",
            "identity": valid.replace("02,b,1,1,y", "02,b,1,1,z"),
            "denominator": valid.replace("02,b,1,1", "02,b,1,0"),
            "nonfinite": valid.replace("02,b,1,1", "02,b,nan,1"),
        }.items():
            with self.subTest(cause=cause):
                data = self.csv_file(head + bad)
                result = self.run_pair(plan, [data], "--denominator", "count", "--match", "trace")
                self.assertNotEqual(0, result.returncode)
                self.assertEqual("", result.stdout)

    def test_large_counter_difference_survives_per_unit_division(self):
        plan = self.csv_file("seed\n01\n")
        data = self.csv_file("seed,method,v,count\n01,a,9007199254740993,2\n"
                             "01,b,9007199254740992,2\n")
        result = self.run_pair(plan, [data], "--denominator", "count")
        self.assertEqual(0, result.returncode, result.stderr)
        group = json.loads(result.stdout)["groups"][0]
        self.assertEqual(group["mean_difference"], 0.5)
        self.assertEqual(group["pairs"][0]["difference"], 0.5)

    def test_matched_arms_must_use_trace_specified_by_plan(self):
        plan = self.csv_file("seed,trace\n01,expected\n")
        data = self.csv_file("seed,method,v,trace,config\n01,a,4,another,fast\n"
                             "01,b,5,another,fast\n")
        result = self.run_pair(plan, [data], "--match", "trace", "config")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("differs from plan on trace", result.stderr)
        self.assertEqual("", result.stdout)

    def test_matrix_digest_checked_on_consumed_csv_bytes(self):
        path = Path(self.csv_file(""))
        original = b"\xef\xbb\xbfseed,v\r\n1,4\r\n"
        expected = {"bytes": len(original), "sha256": hashlib.sha256(original).hexdigest()}
        path.write_bytes(original)
        self.assertEqual(dict(seed="1", v="4"), list(records(path, {"v"}, expected))[0][1])
        path.write_bytes(original.replace(b"1,4", b"1,5"))
        with self.assertRaisesRegex(ValueError, "content changed"):
            list(records(path, {"v"}, expected))

    def test_matrix_pairing_honors_case_identity_and_failed_input_checks(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            manifest = root / "matrix.json"
            writer = "from pathlib import Path; import sys; Path(sys.argv[1]).write_bytes(sys.argv[2].encode())"
            plan = {"outputs": ["metrics.csv"], "cases": [
                {"id": arm, "argv": ["{python}", "-c", writer, "{run_dir}/metrics.csv",
                                     f"seed,method,v\n01,{arm},{value}\n"]}
                for arm, value in (("a", 3), ("b", 1))]}
            manifest.write_text(json.dumps(plan), encoding="utf-8")
            subprocess.run([sys.executable, "-B", str(SCRIPT.with_name("run_matrix.py")), str(manifest),
                            "--run-dir", "runs"], check=True, capture_output=True)
            index = root / "runs/index.json"
            original = json.loads(index.read_text(encoding="utf-8"))
            cli = [sys.executable, "-B", str(SCRIPT), "--plan", self.csv_file("seed\n01\n"),
                   "--matrix", str(index), "--artifact", "metrics.csv", "--unit", "seed",
                   "--candidate", "a", "--baseline", "b", "--value", "v"]
            self.assertEqual(json.loads(subprocess.check_output(cli))["groups"][0]["mean_difference"], 2)
            rows = original["cases"]
            rows["a"]["record"], rows["b"]["record"] = rows["b"]["record"], rows["a"]["record"]
            index.write_text(json.dumps(original), encoding="utf-8")
            self.assertNotEqual(subprocess.run(cli, capture_output=True).returncode, 0)
            rows["a"]["record"], rows["b"]["record"] = rows["b"]["record"], rows["a"]["record"]
            index.write_text(json.dumps(original), encoding="utf-8")
            record_path = index.parent / rows["a"]["record"]
            record = json.loads(record_path.read_text(encoding="utf-8"))
            record["inputs_verified_after_run"] = False
            record_path.write_text(json.dumps(record), encoding="utf-8")
            failed = subprocess.run(cli, capture_output=True)
            self.assertNotEqual(failed.returncode, 0)
            self.assertFalse(failed.stdout)

    def test_nonzero_sd_never_reported_as_zero(self):
        plan = self.csv_file("seed\n01\n02\n")
        first = "1e-308"
        for second, representable in (("1.1e-308", True), ("1." + "0" * 31 + "1e-308", False)):
            data = self.csv_file(f"seed,method,v\n01,a,{first}\n01,b,0\n02,a,{second}\n02,b,0\n")
            result = self.run_pair(plan, [data])
            if representable:
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertGreater(json.loads(result.stdout)["groups"][0]["sd_difference"], 0)
            else:
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(result.stdout)

    def test_recomputes_archived_noc_contrast(self):
        results = ROOT / "dev" / "noc-smoke" / "results"
        plan = "pattern,seed\n" + "".join(f"{name},{s}\n" for name, start in
                    [("uniform", 1000), ("hotspot", 2000)] for s in range(start, start + 12))
        cmd = [sys.executable, "-B", str(SCRIPT), "--plan", self.csv_file(plan),
               "--data", str(results / "paired.csv"), "--unit", "seed", "--group", "pattern",
               "--candidate", "evolution", "--baseline", "random", "--match", "trace_sha256",
               "--value", "latency_sum", "--denominator", "delivered"]
        observed = json.loads(subprocess.check_output(cmd, text=True))["groups"]
        with (results / "summary.csv").open(encoding="utf-8", newline="") as stream:
            ref = {r["pattern"]: r for r in csv.DictReader(stream)
                   if r["method"] == "evolution" and r["comparator"] == "random"}
        self.assertEqual(2, len(observed))
        for group in observed:
            row = ref[group["group"]["pattern"]]
            self.assertEqual(group["n_pairs"], int(row["n"]))
            self.assertEqual(f'{group["mean_difference"]:.6f}', row["paired_delta"])
            self.assertEqual(f'{group["sd_difference"]:.6f}', row["paired_sd"])


if __name__ == "__main__":
    unittest.main()
