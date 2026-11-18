"""Behavior checks for read-only bibliography import (no network or extra deps)."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "import_bibliography.py"
SPEC = importlib.util.spec_from_file_location("bibliography_import", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class BibliographyTests(unittest.TestCase):
    def test_nested_braces_and_literal_tex_are_retained(self):
        text = '% comment\n@article{a, title={NoC {XY} and \\LaTeX}, year=2026, note="a {quoted} value"}\n'
        entries, bad, warnings, details = MODULE.parse_bibtex(text)
        self.assertEqual(len(entries), 1)
        self.assertFalse(bad or warnings)
        self.assertEqual(entries[0]["fields"]["title"], r"NoC {XY} and \LaTeX")
        self.assertEqual(entries[0]["line"], 2)
        self.assertEqual(text[entries[0]["start"]:entries[0]["end"]], entries[0]["raw"])

    def test_parenthesized_entry_and_quoted_brace(self):
        entries, bad, _, _ = MODULE.parse_bibtex('@book(a, title="literal {\\\"quote} and \\" end", year=2026)')
        self.assertEqual(len(entries) + len(bad), 1)
        # A conventional parenthesized record is independently checked.
        entries, bad, _, _ = MODULE.parse_bibtex('@book(a, title="A (B)", year=2026)')
        self.assertFalse(bad)
        self.assertEqual(entries[0]["fields"]["title"], "A (B)")

    def test_unsupported_macros_are_not_silently_expanded(self):
        text = '@string{j="Journal"}\n@article{a,title={x},journal=j}\n@article{b,title="x" # "y"}\n@article{c,title={safe}}'
        entries, bad, _, _ = MODULE.parse_bibtex(text)
        self.assertEqual([entry["source_key"] for entry in entries], ["c"])
        self.assertEqual(len(bad), 3)
        self.assertTrue(any("concatenation" in item["reason"] for item in bad))

    def test_duplicate_fields_reject_whole_entry(self):
        entries, bad, _, _ = MODULE.parse_bibtex('@article{a,title={one},TITLE={two}}')
        self.assertFalse(entries)
        self.assertIn("duplicate_field", bad[0]["reason"])

    def test_malformed_trailing_text_is_retained(self):
        text = '@misc{ok,title={safe}}\n@article{broken,title={oops}'
        entries, bad, _, _ = MODULE.parse_bibtex(text)
        self.assertEqual(len(entries), 1)
        self.assertEqual(len(bad), 1)
        self.assertIn("@article{broken", bad[0]["raw"])

    def test_bib_comments_not_counted_as_entries(self):
        entries, bad, _, details = MODULE.parse_bibtex('@comment{internal notes}\n@misc{x,title={T}}')
        self.assertEqual(len(entries), 1)
        self.assertFalse(bad)
        self.assertEqual(len(details["comments"]), 1)

    def test_ris_repeated_authors_and_continuation(self):
        text = 'TY  - JOUR\nID  - k\nAU  - A\nAU  - B\nTI  - line one\n  line two\nER  -\n'
        entries, bad, warnings, _ = MODULE.parse_ris(text)
        self.assertFalse(bad or warnings)
        self.assertEqual(entries[0]["fields"]["AU"], ["A", "B"])
        self.assertEqual(entries[0]["fields"]["TI"], ["line one\n  line two"])
        self.assertEqual(entries[0]["raw"], text)

    def test_missing_ris_end_does_not_eat_next_record(self):
        text = 'TY  - JOUR\nTI  - broken\nTY  - BOOK\nTI  - good\nER  -\n'
        entries, bad, _, _ = MODULE.parse_ris(text)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["type"], "BOOK")
        self.assertEqual(len(bad), 1)

    def test_unknown_ris_line_is_not_silently_dropped(self):
        entries, bad, _, _ = MODULE.parse_ris('TY  - JOUR\nmissing tag\nER  -\n')
        self.assertFalse(entries)
        self.assertIn("unrecognized_RIS_line", bad[0]["reason"])

    def test_missing_ris_type_is_rejected(self):
        entries, bad, _, _ = MODULE.parse_ris('TY  -\nTI  - title\nER  -\n')
        self.assertFalse(entries)
        self.assertIn("empty_RIS_type", bad[0]["reason"])

    def test_escaped_quotes_are_literal_values(self):
        entries, bad, _, _ = MODULE.parse_bibtex(r'@book(a, title="A (B) {\"quote} and \" end", year=2026)')
        self.assertFalse(bad)
        self.assertEqual(entries[0]["fields"]["title"], r'A (B) {\"quote} and \" end')
        self.assertEqual(entries[0]["fields"]["year"], "2026")

    def test_csl_and_bbt_objects_keep_unknown_fields(self):
        csl = '[{"id":1,"title":"题名","unknown":{"x":3}}]'
        entries, bad, _, _ = MODULE.parse_json(csl)
        self.assertFalse(bad)
        self.assertEqual(entries[0]["source_key"], "1")
        self.assertEqual(entries[0]["fields"]["unknown"], {"x": 3})
        entries, bad, _, details = MODULE.parse_json('{"config":{"version":1},"items":[{"citationKey":"a","itemType":"article"}]}')
        self.assertFalse(bad)
        self.assertEqual(entries[0]["json_pointer"], "/items/0")
        self.assertEqual(details["container_metadata"], {"config": {"version": 1}})

    def test_bad_json_entry_does_not_hide_other_entries(self):
        entries, bad, _, _ = MODULE.parse_json('[{},null,{"id":"ok"}]')
        self.assertEqual(len(entries), 1)
        self.assertEqual(len(bad), 2)

    def test_duplicate_json_keys_and_nonfinite_are_rejected(self):
        for text in ['[{"id":"a","id":"b"}]', '[{"title":NaN}]', '[{"value":1e999}]']:
            entries, bad, _, _ = MODULE.parse_json(text)
            self.assertFalse(entries)
            self.assertTrue(bad)

    def test_cross_file_duplicate_keys_are_not_merged(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp)/'a.bib', Path(tmp)/'b.ris'
            a.write_text('@misc{k,title={one}}', encoding='utf-8')
            b.write_text('TY  - JOUR\nID  - k\nTI  - two\nER  -\n', encoding='utf-8')
            report = MODULE.import_files([a, b])
            self.assertEqual(len(report['entries']), 2)
            self.assertEqual(report['duplicate_source_keys'][0]['entry_ids'], ['entry-1', 'entry-2'])
            self.assertEqual(report['status'], 'REVIEW_NEEDED')

    def test_encoding_explicit_bom_and_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'中文.bib'
            path.write_text('@misc{key,title={中文}}', encoding='utf-8-sig')
            self.assertEqual(MODULE.import_files([path])['status'], 'COMPLETE')
            path.write_bytes('@misc{key,title={中文}}'.encode('gb18030'))
            with self.assertRaises(UnicodeDecodeError):
                MODULE.import_files([path])
            report = MODULE.import_files([path], encoding='gb18030')
            self.assertEqual(report['entries'][0]['fields']['title'], '中文')
            path.write_text('', encoding='utf-8')
            self.assertEqual(MODULE.import_files([path])['status'], 'REVIEW_NEEDED')

    def test_cli_protects_source_and_existing_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, output = Path(tmp)/'a.bib', Path(tmp)/'out.json'
            original = b'@misc{x,title={safe}}'
            source.write_bytes(original)
            cmd = [sys.executable, '-B', str(SCRIPT), str(source), '--output', str(output)]
            result = subprocess.run(cmd, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            expected = output.read_bytes()
            result = subprocess.run(cmd, capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(output.read_bytes(), expected)
            self.assertEqual(source.read_bytes(), original)
            result = subprocess.run([sys.executable, '-B', str(SCRIPT), str(source), '--output', str(source)], capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(source.read_bytes(), original)

    def test_cli_reports_partial_import_and_input_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, output = Path(tmp)/'a.bib', Path(tmp)/'out.json'
            source.write_text('@misc{x,title={safe}}\n@misc{bad,title=unknown}', encoding='utf-8')
            result = subprocess.run([sys.executable, '-B', str(SCRIPT), str(source), '--output', str(output)], capture_output=True)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertEqual(json.loads(output.read_text(encoding='utf-8'))['summary']['rejected'], 1)
            missing = Path(tmp)/'does-not-exist.bib'
            next_output = Path(tmp)/'next.json'
            result = subprocess.run([sys.executable, '-B', str(SCRIPT), str(missing), '--output', str(next_output)], capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertFalse(next_output.exists())


    def test_query_combines_keyword_author_and_year_without_discarding(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'source.bib'
            path.write_text('@article{a,title={NoC routing},author={Li and Wang},year=2024}\n'
                            '@article{b,title={NoC placement},author={Smith},year=2025}\n'
                            '@article{c,title={NoC draft},author={Li}}', encoding='utf-8')
            report = MODULE.import_files([path])
            view = MODULE.query_entries(report['entries'], query='NOC', field='TITLE',
                                        author='li', year_from=2024, year_to=2024)
            self.assertEqual([item['source_key'] for item in view['matches']], ['a'])
            self.assertEqual(len(report['entries']), 3)
            self.assertEqual(view['source_entry_count'], 3)
            self.assertIn('year_unavailable', view['excluded'][1]['reasons'])
            self.assertEqual(view['matches'][0]['year_basis'], 'year')

    def test_query_supports_ris_csl_and_bbt_author_year_fields(self):
        raw = [
            ('ris', 'TY  - JOUR\nAU  - Wang\nPY  - 2024/02/03\nTI  - NoC\nER  -\n'),
            ('json', '[{"id":"a","author":[{"family":"Wang","given":"L"}],"issued":{"date-parts":[[2024,2,3]]}}]'),
            ('json', '{"items":[{"citationKey":"b","creators":[{"creatorType":"author","lastName":"Wang"}],"date":"2024-02-03"}]}'),
        ]
        entries = []
        for fmt, text in raw:
            parsed, bad, _, _ = MODULE.PARSERS[fmt](text)
            self.assertFalse(bad)
            parsed[0]['id'] = 'entry-' + str(len(entries)+1)
            entries.extend(parsed)
        view = MODULE.query_entries(entries, author='wang', year_from=2024, year_to=2024)
        self.assertEqual(view['matched_count'], 3)

    def test_query_missing_field_and_empty_results_are_explicit(self):
        entry = {'id':'entry-1','source_key':'x','fields':{'title':'alpha','editor':'Wang'}}
        view = MODULE.query_entries([entry], query='omega', field='abstract', author='Wang')
        self.assertEqual(view['status'], 'NO_MATCHES')
        self.assertEqual(view['matched_count'], 0)
        self.assertEqual(view['excluded'][0]['reasons'], ['field_missing','author_missing'])

    def test_query_cli_validation_and_zero_matches(self):
        with tempfile.TemporaryDirectory() as tmp:
            path, output = Path(tmp)/'a.bib', Path(tmp)/'out.json'
            path.write_text('@misc{x,title={alpha},year=2024}', encoding='utf-8')
            base = [sys.executable, '-B', str(SCRIPT), str(path), '--output', str(output)]
            for options in [['--query',''], ['--field','title'], ['--year-from','2025','--year-to','2024'],
                            ['--year','2024','--year-from','2024']]:
                result = subprocess.run(base+options, capture_output=True)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertFalse(output.exists())
            result = subprocess.run(base+['--query','omega'], capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(output.read_text(encoding='utf-8'))
            self.assertEqual(report['query']['status'], 'NO_MATCHES')
            self.assertEqual(len(report['entries']), 1)
            self.assertEqual(json.loads(result.stdout)['matched'], 0)


if __name__ == '__main__':
    unittest.main()
