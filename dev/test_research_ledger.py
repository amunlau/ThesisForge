"""Behavioral checks for evidence freshness and bounded UTF-8 edits."""
import hashlib
import json
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/research_ledger.py"
API = runpy.run_path(str(SCRIPT))


class ResearchLedgerTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(prefix="thesisforge-ledger-")
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.record = {"schema": 1, **{k: [] for k in ("artifacts", "sources", "claims", "issues", "decisions", "checks")}}

    def artifact(self, name, text="value", inputs=None):
        path = self.root / (name + ".txt")
        path.write_text(text, encoding="utf-8")
        row = {"id": name, "path": path.name, "kind": "data", **API["fingerprint"](path), "inputs": inputs or {}}
        self.record["artifacts"].append(row)
        return row

    def check(self):
        return API["check_record"](self.record, self.root)

    def invoke(self, *args):
        return subprocess.run([sys.executable, "-B", str(SCRIPT), "--root", str(self.root), *args],
                              capture_output=True, encoding="utf-8", timeout=15)

    def test_changed_data_invalidates_transitive_figure_claim_and_check(self):
        data = self.artifact("data")
        chart = self.artifact("chart", inputs={"data": data["sha256"]})
        self.artifact("paper", inputs={"chart": chart["sha256"]})
        self.record["claims"] = [{"id": "C1", "text": "a bounded observation", "status": "qualified", "locations": ["paper section 2"],
                                  "evidence": [{"artifact_id": "chart", "locator": "panel a", "observed_sha256": chart["sha256"]}]}]
        self.record["checks"] = [{"id": "V1", "status": "passed", "method": "visual review", "checked_at": "2026-11-18",
                                  "inputs": {"chart": chart["sha256"]}}]
        self.assertEqual(self.check()["status"], "consistent_within_coverage")
        (self.root / "data.txt").write_text("changed", encoding="utf-8")
        result = self.check()
        self.assertEqual(result["artifacts"], {"data": "stale", "chart": "stale", "paper": "stale"})
        self.assertEqual(result["claims"]["C1"]["effective"], "stale")
        self.assertEqual(result["checks"]["V1"], "stale")
        self.assertEqual(result["coverage"]["semantically_verified_by_this_tool"], 0)

    def test_recapturing_source_does_not_refresh_old_chart_inputs(self):
        self.assertEqual(self.invoke("init").returncode, 0)
        for name in ("data", "chart"):
            (self.root / (name + ".txt")).write_text("first", encoding="utf-8")
        self.assertEqual(self.invoke("record-file", "--id", "D", "--path", "data.txt", "--kind", "data").returncode, 0)
        self.assertEqual(self.invoke("record-file", "--id", "F", "--path", "chart.txt", "--kind", "figure", "--input", "D").returncode, 0)
        (self.root / "data.txt").write_text("second", encoding="utf-8")
        self.assertEqual(self.invoke("record-file", "--id", "D", "--path", "data.txt", "--kind", "data").returncode, 0)
        # Recapturing chart without explicitly rebuilding against D must keep
        # its old dependency snapshot, not erase it.
        self.assertEqual(self.invoke("record-file", "--id", "F", "--path", "chart.txt", "--kind", "figure").returncode, 0)
        result = self.invoke("check", "--strict")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["artifacts"]["F"], "stale")

    def test_cycles_missing_links_and_metadata_are_not_passed_as_evidence(self):
        a = self.artifact("a")
        b = self.artifact("b", inputs={"a": a["sha256"]})
        a["inputs"] = {"b": b["sha256"]}
        self.record["sources"] = [{"id": "S1", "locator": "https://example.org/record", "version": "v1", "read_scope": "metadata"}]
        self.record["claims"] = [{"id": "C1", "text": "improved latency", "status": "supported", "locations": ["abstract"],
                                  "evidence": [{"source_id": "S1", "locator": "metadata title", "observed_version": "v1"}]}]
        result = self.check()
        self.assertIn("dependency_cycle", {x["code"] for x in result["findings"]})
        self.assertEqual(result["claims"]["C1"]["effective"], "unverified")
        self.record["claims"][0]["evidence"] = [{"artifact_id": "missing", "locator": "row 1"}]
        self.assertIn("missing_artifact", {x["code"] for x in self.check()["findings"]})

    def test_registering_changed_file_does_not_refresh_direct_or_source_claim(self):
        data = self.artifact("data", "first observation")
        old_hash = data["sha256"]
        self.record["sources"] = [{"id": "S1", "locator": "data.txt", "version": "v1",
                                   "read_scope": "full", "artifact_id": "data"}]
        self.record["claims"] = [
            {"id": "C1", "text": "first observation", "status": "supported", "locations": ["results"],
             "evidence": [{"artifact_id": "data", "locator": "row 1", "observed_sha256": old_hash}]},
            {"id": "C2", "text": "first observation", "status": "qualified", "locations": ["discussion"],
             "evidence": [{"source_id": "S1", "locator": "row 1", "observed_locator": "data.txt", "observed_version": "v1", "observed_sha256": old_hash}]},
        ]
        ledger = self.root / ".thesisforge/research.json"
        API["atomic_json"](ledger, self.record)
        self.assertEqual(self.invoke("check", "--strict").returncode, 0)
        (self.root / "data.txt").write_text("second observation", encoding="utf-8")
        self.assertEqual(self.invoke("record-file", "--id", "data", "--path", "data.txt", "--kind", "data").returncode, 0)
        result = self.invoke("check", "--strict")
        self.assertEqual(result.returncode, 1)
        report = json.loads(result.stdout)
        self.assertEqual(report["artifacts"]["data"], "current")
        self.assertEqual({value["effective"] for value in report["claims"].values()}, {"stale"})
        stored = API["read_json"](ledger)
        self.assertEqual([row["evidence"][0]["observed_sha256"] for row in stored["claims"]], [old_hash, old_hash])
        # Only an explicit new review receipt can bind claims to the new file.
        for claim in stored["claims"]:
            claim["evidence"][0]["observed_sha256"] = stored["artifacts"][0]["sha256"]
        API["atomic_json"](ledger, stored)
        self.assertEqual(self.invoke("check", "--strict").returncode, 0)

    def test_source_version_change_remains_stale_until_explicitly_rebound(self):
        self.record["sources"] = [{"id": "S1", "locator": "https://example.org/paper", "version": "v1", "read_scope": "excerpt"}]
        claim = {"id": "C1", "text": "a bounded finding", "status": "qualified", "locations": ["background"],
                 "evidence": [{"source_id": "S1", "locator": "section 2", "observed_locator": "https://example.org/paper", "observed_version": "v1"}]}
        self.record["claims"] = [claim]
        self.assertEqual(self.check()["claims"]["C1"]["effective"], "qualified")
        self.record["sources"][0]["version"] = "v2"
        self.assertEqual(self.check()["claims"]["C1"]["effective"], "stale")
        claim["evidence"][0]["observed_version"] = "v2"
        self.assertEqual(self.check()["claims"]["C1"]["effective"], "qualified")

    def test_source_replacement_cannot_reuse_same_version_for_old_claim(self):
        source = {"id": "S1", "locator": "https://example.org/paper-a", "version": "v1", "read_scope": "full"}
        self.record["sources"] = [source]
        evidence = {"source_id": "S1", "locator": "section 2", "observed_version": "v1"}
        self.record["claims"] = [{"id": "C1", "text": "bounded finding", "status": "qualified",
                                  "locations": ["background"], "evidence": [evidence]}]
        # Existing schema-1 ledgers still load, but a missing source identity is
        # not silently rebound to whichever URL is in the mutable source row.
        self.assertEqual(self.check()["claims"]["C1"]["effective"], "unverified")
        evidence["observed_locator"] = source["locator"]
        self.assertEqual(self.check()["claims"]["C1"]["effective"], "qualified")
        source["locator"] = "https://example.org/paper-b"
        self.assertEqual(self.check()["claims"]["C1"]["effective"], "stale")
        self.assertEqual(evidence["observed_locator"], "https://example.org/paper-a")

    def test_removing_local_source_binding_does_not_refresh_stale_claim(self):
        data = self.artifact("source", "version actually reviewed")
        source = {"id": "S1", "locator": "https://example.org/paper", "version": "v1",
                  "read_scope": "full", "artifact_id": data["id"]}
        evidence = {"source_id": "S1", "locator": "section 2", "observed_locator": source["locator"],
                    "observed_version": "v1", "observed_sha256": data["sha256"]}
        self.record["sources"] = [source]
        self.record["claims"] = [{"id": "C1", "text": "bounded finding", "status": "supported",
                                  "locations": ["results"], "evidence": [evidence]}]
        self.assertEqual(self.check()["claims"]["C1"]["effective"], "supported")
        (self.root / data["path"]).write_text("a later document", encoding="utf-8")
        self.assertEqual(self.check()["claims"]["C1"]["effective"], "stale")
        del source["artifact_id"]
        self.record["artifacts"] = []
        result = self.check()
        self.assertEqual(result["claims"]["C1"]["effective"], "unverified")
        self.assertIn("source_file_binding_missing", {x["code"] for x in result["findings"]})
        self.assertEqual(evidence["observed_sha256"], data["sha256"])

    def test_unfrozen_evidence_cannot_establish_support(self):
        data = self.artifact("data")
        self.record["sources"] = [
            {"id": "S1", "locator": "https://example.org/paper", "version": "v1", "read_scope": "full"},
            {"id": "S2", "locator": "data.txt", "version": "v1", "read_scope": "full", "artifact_id": "data"},
        ]
        cases = [
            {"artifact_id": "data"},
            {"artifact_id": "data", "observed_sha256": "not a hash"},
            {"source_id": "S1"},
            {"source_id": "S1", "observed_version": 1},
            {"source_id": "S2", "observed_version": "v1"},
            {"source_id": "S2", "observed_sha256": data["sha256"]},
        ]
        for item in cases:
            with self.subTest(item=item):
                self.record["claims"] = [{"id": "C1", "text": "bounded finding", "status": "supported", "locations": ["results"],
                                          "evidence": [{**item, "locator": "row 1"}]}]
                result = self.check()
                self.assertEqual(result["claims"]["C1"]["effective"], "unverified")
                self.assertIn("claim_evidence_unfrozen", {x["code"] for x in result["findings"]})

    def test_stale_evidence_dominates_gaps_in_either_order(self):
        data = self.artifact("data")
        stale = {"artifact_id": "data", "locator": "row 1", "observed_sha256": "0" * 64}
        gaps = [
            {"artifact_id": "data", "locator": "row 1"},
            {"artifact_id": "data", "observed_sha256": data["sha256"]},
            {"source_id": "missing", "locator": "section 1", "observed_version": "v1"},
        ]
        for gap in gaps:
            for evidence in ([stale, gap], [gap, stale]):
                with self.subTest(evidence=evidence):
                    self.record["claims"] = [{"id": "C1", "text": "bounded finding", "status": "supported",
                                              "locations": ["results"], "evidence": evidence}]
                    self.assertEqual(self.check()["claims"]["C1"]["effective"], "stale")

    def test_valid_frozen_evidence_does_not_upgrade_declared_status(self):
        data = self.artifact("data")
        for status in ("supported", "qualified", "disputed", "unverified", "todo"):
            with self.subTest(status=status):
                self.record["claims"] = [{"id": "C1", "text": "bounded finding", "status": status, "locations": ["results"],
                                          "evidence": [{"artifact_id": "data", "locator": "row 1", "observed_sha256": data["sha256"]}]}]
                self.assertEqual(self.check()["claims"]["C1"], {"declared": status, "effective": status})

    def test_unread_source_cannot_support_even_bibliographic_identity(self):
        source = {"id": "S1", "locator": "https://example.org/paper", "version": "v1",
                  "read_scope": "unread"}
        self.record["sources"] = [source]
        claim = {"id": "C1", "kind": "bibliographic", "text": "The supplied citation identifies this paper.",
                 "status": "supported", "locations": ["references"],
                 "evidence": [{"source_id": "S1", "locator": "publication record",
                               "observed_locator": source["locator"], "observed_version": "v1"}]}
        self.record["claims"] = [claim]
        result = self.check()
        self.assertEqual(result["claims"]["C1"]["effective"], "unverified")
        self.assertIn("content_not_read", {x["code"] for x in result["findings"]})
        # A declaration that metadata was actually read is a distinct state;
        # it can support bibliographic identity, but not scientific findings.
        source["read_scope"] = "metadata"
        self.assertEqual(self.check()["claims"]["C1"]["effective"], "supported")
        claim["kind"] = "scientific"
        self.assertEqual(self.check()["claims"]["C1"]["effective"], "unverified")

    def test_input_error_empty_ledger_and_writer_lock_are_distinct(self):
        self.assertEqual(self.invoke("init").returncode, 0)
        self.assertEqual(self.invoke("check", "--strict").returncode, 1)
        path = self.root / ".thesisforge/research.json"
        raw = path.read_bytes()
        path.with_name(path.name + ".lock").write_text("another writer", encoding="utf-8")
        self.assertEqual(self.invoke("init").returncode, 2)
        self.assertEqual(path.read_bytes(), raw)
        path.write_text('{"schema":1,"schema":1}', encoding="utf-8")
        self.assertEqual(self.invoke("check").returncode, 2)

    def test_patch_preserves_original_bom_crlf_and_unrelated_text(self):
        source = self.root / "原文.tex"
        raw = b"\xef\xbb\xbf" + "第一行\r\nlatency is 5 ms.\r\n\\cite{keep}\r\n".encode("utf-8")
        source.write_bytes(raw)
        result = API["apply_patch_plan"](self.root, source.name, hashlib.sha256(raw).hexdigest(),
                                          {"replacements": [{"old": "latency is", "new": "Latency remains"}]}, "改文.tex")
        self.assertEqual(source.read_bytes(), raw)
        self.assertEqual((self.root / "改文.tex").read_bytes(), raw.replace(b"latency is", b"Latency remains"))
        self.assertEqual(result["semantic_fidelity"], "not_checked")

    def test_patch_rejects_stale_ambiguous_overlapping_and_existing_outputs(self):
        source = self.root / "a.md"
        source.write_text("abc abc def", encoding="utf-8")
        digest = API["fingerprint"](source)["sha256"]
        apply = API["apply_patch_plan"]
        cases = [("0" * 64, [{"old": "def", "new": "ghi"}], "new.md"),
                 (digest, [{"old": "abc", "new": "x"}], "new.md"),
                 (digest, [{"old": "abc abc", "new": "x"}, {"old": "abc def", "new": "y"}], "new.md"),
                 (digest, [{"old": "def", "new": "ghi"}], "a.md"),
                 (digest, [{"old": "def", "new": "ghi"}], "../escape.md")]
        for expected, replacements, output in cases:
            with self.subTest(output=output, replacements=replacements), self.assertRaises(ValueError):
                apply(self.root, "a.md", expected, {"replacements": replacements}, output)
        self.assertFalse((self.root / "new.md").exists())

    def test_patch_rejects_overlapping_occurrences_of_one_fragment(self):
        source = self.root / "repeated.md"
        raw = b"the the the"
        source.write_bytes(raw)
        digest = hashlib.sha256(raw).hexdigest()
        with self.assertRaisesRegex(ValueError, "exactly once"):
            API["apply_patch_plan"](self.root, source.name, digest,
                                    {"replacements": [{"old": "the the", "new": "X"}]}, "new.md")
        self.assertEqual(source.read_bytes(), raw)
        self.assertFalse((self.root / "new.md").exists())
        API["apply_patch_plan"](self.root, source.name, digest,
                                {"replacements": [{"old": "the the the", "new": "X"}]}, "new.md")
        self.assertEqual((self.root / "new.md").read_bytes(), b"X")
        self.assertEqual(source.read_bytes(), raw)

    def test_path_escape_cannot_be_used_as_registered_artifact(self):
        self.record["artifacts"] = [{"id": "X", "kind": "data", "path": "../outside.txt", "sha256": "0" * 64, "bytes": 0}]
        result = self.check()
        self.assertEqual(result["artifacts"]["X"], "missing")
        self.assertIn("file_unavailable", {x["code"] for x in result["findings"]})


if __name__ == "__main__":
    unittest.main()
