"""Behavior checks using disposable manuscript sources; never runs TeX."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit_manuscript.py"


class ManuscriptAudit(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="thesisforge-manuscript-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def put(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def run_cli(self, source, *args):
        result = subprocess.run([sys.executable, "-B", str(SCRIPT), str(source), *map(str, args)], cwd=self.root,
                                capture_output=True, text=True, encoding="utf-8", timeout=10)
        self.assertIn(result.returncode, [0, 1, 2], result.stderr)
        return result, json.loads(result.stdout if result.stdout else result.stderr)

    def test_simple_text_count_and_no_modification(self):
        path = self.put("正文.txt", "方法测得 3.2 ms。\n")
        original = path.read_bytes()
        result, report = self.run_cli(path)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(report["totals"]["mixed_words"], 6)
        self.assertEqual(report["files"][str(path)]["sha256"], hashlib.sha256(original).hexdigest())
        self.assertEqual(path.read_bytes(), original)

    def test_empty_and_invalid_utf8_fail(self):
        path = self.put("empty.txt", "  \n")
        self.assertEqual(self.run_cli(path)[0].returncode, 2)
        path.write_bytes(b"\xff\xfe")
        self.assertEqual(self.run_cli(path)[0].returncode, 2)

    def test_explicit_legacy_encoding(self):
        path = self.root / "legacy.txt"
        path.write_bytes("方法可行".encode("gb18030"))
        self.assertEqual(self.run_cli(path)[0].returncode, 2)
        self.assertEqual(self.run_cli(path, "--encoding", "gb18030")[1]["totals"]["mixed_words"], 4)

    def test_bom(self):
        path = self.root / "bom.txt"
        path.write_bytes(b"\xef\xbb\xbf" + "测试".encode("utf-8"))
        self.assertEqual(self.run_cli(path)[1]["totals"]["mixed_words"], 2)

    def test_multifile_resolves_actual_labels_and_bib(self):
        path = self.put("main.tex", r"\input{sections/results}" + "\n" + r"\ref{sec:result}\cite{one}\bibliography{refs}")
        leaf = self.put("sections/results.tex", r"\section{Results}\label{sec:result}Measured latency is 5 ms.")
        self.put("refs.bib", '@article{one, title={A {nested} title}}')
        result, report = self.run_cli(path, "--strict")
        self.assertEqual(result.returncode, 0, report)
        self.assertEqual(len(report["files"]), 3)
        self.assertIn(str(leaf), report["files"])

    def test_unresolved_literal_ref_and_cite_are_errors(self):
        path = self.put("main.tex", r"\ref{missing}\cite{absent}\bibliography{refs}")
        self.put("refs.bib", '@article{one, title={A}}')
        result, report = self.run_cli(path, "--strict")
        self.assertEqual(result.returncode, 1)
        self.assertEqual({x["code"] for x in report["findings"]}, {"unresolved_reference", "unresolved_citation"})

    def test_conditional_structure_is_review_not_false_error(self):
        path = self.put("main.tex", r"\iffalse\ref{inactive}\fi" + "\n" + r"\newcommand{\a}{1}")
        result, report = self.run_cli(path, "--strict")
        self.assertEqual(result.returncode, 0)
        self.assertTrue(report["coverage_notes"])
        self.assertEqual(report["findings"][0]["level"], "review")

    def test_comments_and_code_do_not_create_citations(self):
        path = self.put("main.tex", "% \\ref{ghost}\n" + r"\begin{verbatim}\ref{ghost2}\end{verbatim}" + "\nReadable words.")
        self.assertEqual(self.run_cli(path, "--strict")[1]["findings"], [])

    def test_verbatim_percent_does_not_hide_following_live_reference(self):
        for code in (r"\verb|50%|", r"\begin{verbatim}50%\end{verbatim}"):
            with self.subTest(code=code):
                path = self.put("main.tex", code + r" \ref{missing}")
                result, report = self.run_cli(path, "--strict")
                self.assertEqual(result.returncode, 1, report)
                self.assertEqual([item["code"] for item in report["findings"]], ["unresolved_reference"])

    def test_commented_verbatim_start_does_not_hide_live_reference(self):
        path = self.put("main.tex", "% \\begin{verbatim}\n" + r"\ref{missing}\end{verbatim}")
        result, report = self.run_cli(path, "--strict")
        self.assertEqual(result.returncode, 1, report)

    def test_modern_command_and_environment_definitions_are_dynamic(self):
        for definition in (r"\NewDocumentCommand{\unused}{}{\label{a}}",
                           r"\newenvironment{unused}{\label{a}}{}"):
            with self.subTest(definition=definition):
                path = self.put("main.tex", definition + r"\label{a}")
                result, report = self.run_cli(path, "--strict")
                self.assertEqual(result.returncode, 0, report)
                self.assertEqual(report["findings"][0]["level"], "review")

    def test_escaped_command_is_not_a_reference(self):
        path = self.put("a.tex", r"\\ref{literal-text} is not a reference command.")
        self.assertEqual(self.run_cli(path, "--strict")[1]["findings"], [])

    def test_external_labels_mark_structure_partial(self):
        path = self.put("a.tex", r"\externaldocument{other}\ref{outside}")
        result, report = self.run_cli(path, "--strict")
        self.assertEqual(result.returncode, 0)
        self.assertTrue(report["coverage_notes"])

    def test_nested_or_malformed_structural_argument_is_partial(self):
        path = self.put("a.tex", r"\cite{prefix{key}} Text \ref{missing}")
        result, report = self.run_cli(path, "--strict")
        self.assertEqual(result.returncode, 0)
        self.assertTrue(any("unsupported structural argument" in n for n in report["coverage_notes"]))

    def test_bib_comment_does_not_create_key(self):
        path = self.put("main.tex", r"\cite{fake}\bibliography{refs}")
        self.put("refs.bib", '@comment{\n@article{fake, title={Not a source}}\n}\n@article{real,title={Source}}')
        result, report = self.run_cli(path, "--strict")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["findings"][0]["code"], "unresolved_citation")

    def test_bib_percent_comments_do_not_create_keys_or_hide_real_entries(self):
        path = self.put("main.tex", r"\cite{fake,real}\bibliography{refs}")
        self.put("refs.bib", '% @article{fake,title={Not a record}}\n'
                 '@article{real,title={100% efficiency},note={An @example within a field}} % @article{fake,title={Also not a record}}')
        result, report = self.run_cli(path, "--strict")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(len(report["findings"]), 1, report)
        self.assertEqual(report["findings"][0]["code"], "unresolved_citation")
        self.assertTrue(report["findings"][0]["note"].endswith(": fake"))

    def test_comma_in_ordinary_reference_is_one_key_but_cref_is_a_list(self):
        path = self.put("main.tex", r"\label{a,b}\ref{a,b}\eqref{a,b}\pageref{a,b}\autoref{a,b}"
                        r"\label{a}\label{b}\cref{a,b}\Cref{a,b}")
        result, report = self.run_cli(path, "--strict")
        self.assertEqual(result.returncode, 0, report)
        self.assertEqual(report["findings"], [])
        path.write_text(r"\label{a}\label{b}\ref{a,b}", encoding="utf-8")
        result, report = self.run_cli(path, "--strict")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(len(report["findings"]), 1)
        self.assertTrue(report["findings"][0]["note"].endswith(": a,b"))

    def test_external_bibliography_and_literal_bibitems_can_coexist(self):
        path = self.put("main.tex", r"\cite{inline,real}\bibliography{refs}"
                        r"\begin{thebibliography}{1}\bibitem[Author(2020)]{inline} Entry\end{thebibliography}")
        self.put("refs.bib", '@article{real,title={Source}}')
        result, report = self.run_cli(path, "--strict")
        self.assertEqual(result.returncode, 0, report)
        self.assertEqual(report["findings"], [])
        path.write_text(r"\cite{unknown}\bibitem{known} Entry", encoding="utf-8")
        result, report = self.run_cli(path, "--strict")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["findings"][0]["code"], "unresolved_citation")

    def test_dynamic_bibitem_downgrades_external_citation_check(self):
        path = self.put("main.tex", r"\cite{inline}\bibliography{refs}\bibitem{\generatedkey} Entry")
        self.put("refs.bib", '@article{real,title={Source}}')
        result, report = self.run_cli(path, "--strict")
        self.assertEqual(result.returncode, 0, report)
        self.assertEqual(report["findings"][0]["level"], "review")
        self.assertTrue(report["coverage_notes"])

    def test_escaped_percent_before_real_comment(self):
        path = self.put("a.tex", r"Rate is 5\% % \ref{not-a-reference}" + "\n")
        self.assertEqual(self.run_cli(path, "--strict")[1]["findings"], [])

    def test_include_escape_rejected(self):
        path = self.put("project/main.tex", r"\input{../outside}")
        self.put("outside.tex", "Outside")
        self.assertEqual(self.run_cli(path)[0].returncode, 2)

    def test_include_cycle_and_missing_resource(self):
        path = self.put("main.tex", r"\input{main}")
        self.assertEqual(self.run_cli(path, "--strict")[0].returncode, 1)
        path.write_text(r"\input{generated}", encoding="utf-8")
        result, report = self.run_cli(path, "--strict")
        self.assertEqual(result.returncode, 0)
        self.assertTrue(report["coverage_notes"])

    def test_conditional_include_cycle_is_only_a_review_hint(self):
        path = self.put("main.tex", r"\iffalse\input{main}\fi")
        result, report = self.run_cli(path, "--strict")
        self.assertEqual(result.returncode, 0, report)
        self.assertEqual(report["findings"][0]["code"], "include_cycle")
        self.assertEqual(report["findings"][0]["level"], "review")

    def test_tex_include_inherits_tex_parsing_for_other_extensions(self):
        path = self.put("main.tex", r"\input{part.ltx}\ref{fig:a}")
        self.put("part.ltx", "% \\label{ignored}\n" + r"\label{fig:a} Text")
        result, report = self.run_cli(path, "--strict")
        self.assertEqual(result.returncode, 0, report)
        self.assertEqual(report["findings"], [])

    def test_limits_are_user_supplied_not_default(self):
        path = self.put("highlights.txt", "One finding\nSecond finding longer\n")
        self.assertEqual(self.run_cli(path, "--strict")[0].returncode, 0)
        result, report = self.run_cli(path, "--per-line", "--limit-chars", 12, "--strict")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["findings"][0]["location"]["line"], 2)

    def test_terms_keep_concept_distinction_and_positions(self):
        path = self.put("terms.md", "带宽描述链路。吞吐量描述交付。\n")
        term_map = self.put("map.json", json.dumps({"terms": [{"id": "capacity", "relation": "distinct", "variants": ["带宽", "吞吐量"]}]}, ensure_ascii=False))
        result, report = self.run_cli(path, "--terms", term_map, "--strict")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(report["findings"][0]["level"], "review")
        self.assertEqual(len(report["findings"][0]["occurrences"]), 2)
        self.assertEqual(path.read_text(encoding="utf-8"), "带宽描述链路。吞吐量描述交付。\n")

    def test_term_configuration_rejects_duplicate_json(self):
        path = self.put("a.txt", "text")
        term_map = self.put("map.json", '{"terms":[],"terms":[]}')
        self.assertEqual(self.run_cli(path, "--terms", term_map)[0].returncode, 2)

    def test_term_variants_across_chapters(self):
        path = self.put("a.tex", r"\input{one}\input{two}")
        self.put("one.tex", "带宽")
        self.put("two.tex", "吞吐量")
        term_map = self.put("map.json", json.dumps({"terms": [{"id": "capacity", "relation": "distinct", "variants": ["带宽", "吞吐量"]}]}, ensure_ascii=False))
        result, report = self.run_cli(path, "--terms", term_map, "--strict")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(len(report["findings"][0]["occurrences"]), 2)

    def test_quantities_detect_unit_and_chinese_percentage_change(self):
        before = self.put("before.txt", "时延5 ms，提升2%。")
        after = self.put("after.txt", "时延5 ns，提升3%。")
        result, report = self.run_cli(after, "--before", before, "--strict")
        self.assertEqual(result.returncode, 0)
        change = report["findings"][0]
        self.assertEqual(change["code"], "quantity_difference")
        self.assertIn("5 ms", change["removed"])
        self.assertIn("3%", change["added"])
        self.assertTrue(report["coverage_notes"])

    def test_quantities_keep_whole_comma_grouped_numbers(self):
        before = self.put("before.txt", "Latency 1,000 ms; energy -1,200.50e-3 mJ.")
        after = self.put("after.txt", "Latency 2,000 ms; energy -2,200.50e-3 mJ.")
        result, report = self.run_cli(after, "--before", before, "--strict")
        self.assertEqual(result.returncode, 0, report)
        change = report["findings"][0]
        self.assertEqual(change["removed"], {"1,000 ms": 1, "-1,200.50e-3 mJ": 1})
        self.assertEqual(change["added"], {"2,000 ms": 1, "-2,200.50e-3 mJ": 1})
        self.assertEqual(change["before_locations"][0]["start"], 8)
        self.assertEqual(change["before_locations"][0]["end"], 16)
        before.write_text("Unsupported comma decimal: 1,25 ms.", encoding="utf-8")
        after.write_text("Unsupported comma decimal: 1,75 ms.", encoding="utf-8")
        result, report = self.run_cli(after, "--before", before)
        self.assertEqual(report["findings"], [], "Must not invent a partial 25 ms/75 ms quantity")
        self.assertTrue(any("other locale separators may be omitted" in note for note in report["coverage_notes"]))

    def test_abbreviations_are_opt_in_hints(self):
        path = self.put("a.txt", "NOC uses FIFO. Network (ABC) uses ABC.")
        self.assertEqual(self.run_cli(path)[1]["findings"], [])
        result, report = self.run_cli(path, "--abbreviations", "--strict")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(len(report["findings"]), 2)

    def test_duplicate_labels_and_library_entries(self):
        path = self.put("a.tex", r"\label{a}\label{a}\bibliography{refs}")
        self.put("refs.bib", '@article{k,title={First}}\n@article{k,title={Second}}')
        result, report = self.run_cli(path, "--strict")
        self.assertEqual(result.returncode, 1)
        self.assertEqual({x["code"] for x in report["findings"]}, {"duplicate_label", "duplicate_bib_key"})


if __name__ == "__main__":
    unittest.main()
