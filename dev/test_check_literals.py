"""Exercise the literal checker as a CLI, including its documented blind spots.

Run from the skill root with:
    python -B -X utf8 -m unittest discover -s dev -p test_check_literals.py -v

Every source and output sample lives in a temporary directory. Exit status is the
contract under test; the checks do not depend on a particular diagnostic wording.
"""

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_literals.py"


class LiteralCheckerCLI(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="thesisforge-literals-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def run_cli(self, *arguments, env=None):
        return subprocess.run(
            [sys.executable, "-B", "-X", "utf8", str(SCRIPT), *map(str, arguments)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=15,
            cwd=self.root,
            env=env,
            check=False,
        )

    def compare(self, before, after, *options, suffix=".md", encoding="utf-8"):
        original = self.root / ("before" + suffix)
        final = self.root / ("after" + suffix)
        original.write_text(before, encoding=encoding)
        final.write_text(after, encoding=encoding)
        return self.run_cli(original, final, *options)

    def assert_status(self, expected, result):
        self.assertEqual(
            expected,
            result.returncode,
            msg=f"stdout={result.stdout!r}; stderr={result.stderr!r}",
        )

    def test_unchanged_text(self):
        text = "A 组中位延迟 6 ms，B 组 9 ms，仅测 40 °C；误差为 ±0.3%。"
        self.assert_status(0, self.compare(text, text))

    def test_rephrasing_preserves_numeric_literals(self):
        self.assert_status(
            0,
            self.compare("在 25 °C 下测得 12 ms。", "测量条件为 25 °C，结果为 12 ms。"),
        )

    def test_utf8_bom_is_accepted(self):
        self.assert_status(0, self.compare("10³ Hz", "10^{3} Hz", encoding="utf-8-sig"))

    def test_number_change_returns_one(self):
        result = self.compare("中位延迟 6 ms。", "中位延迟 9 ms。")
        self.assert_status(1, result)
        self.assertTrue(result.stdout.strip())

    def test_changed_occurrence_count_is_detected(self):
        self.assert_status(1, self.compare("两次分别为 6 ms、6 ms。", "结果为 6 ms。"))

    def test_numeric_sign_change_is_detected(self):
        for before, after in (("−20", "20"), ("-20", "+20"), ("−0.5", "+0.5")):
            with self.subTest(before=before, after=after):
                self.assert_status(1, self.compare("范围 " + before, "范围 " + after))

    def test_percent_and_uncertainty_changes_are_detected(self):
        for before, after in (("18%", "18"), ("±0.3", "0.3"), ("±0.3", "∓0.3")):
            with self.subTest(before=before, after=after):
                self.assert_status(1, self.compare(before, after))

    def test_spaces_around_numeric_symbols_are_ignored(self):
        self.assert_status(0, self.compare("误差 ± 0.3 %，范围 ≤ 5。", "误差 ±0.3%，范围 ≤5。"))

    def test_tex_uncertainty_and_percent_are_equivalent(self):
        self.assert_status(0, self.compare("误差 ±0.3%", r"误差 \pm 0.3\%"))

    def test_changed_scientific_exponent_is_detected(self):
        self.assert_status(1, self.compare("1.2e-3", "1.2e3"))

    def test_changed_numeric_scripts_are_detected(self):
        for before, after in (("10³", "10²"), ("H₂O", "H₃O"), ("m²", "m₂")):
            with self.subTest(before=before, after=after):
                self.assert_status(1, self.compare(before, after))

    def test_equivalent_superscript_representations(self):
        for variant in ("10<sup>3</sup>", "10^{3}"):
            with self.subTest(variant=variant):
                self.assert_status(0, self.compare("10³", variant))

    def test_equivalent_subscript_representations(self):
        for variant in ("H<sub>2</sub>O", "H_{2}O"):
            with self.subTest(variant=variant):
                self.assert_status(0, self.compare("H₂O", variant))

    def test_inline_formatting_preserves_actual_comparisons_and_attribute_digits(self):
        self.assert_status(0, self.compare("阈值 ≤ 5", "阈值 ≤ <em><b>5</b></em>"))
        self.assert_status(1, self.compare("阈值 < 5", "阈值 > <em>5</em>"))
        self.assert_status(1, self.compare('<span data-id="11">5</span>',
                                           '<span data-id="12">5</span>'))

    def test_equivalent_signed_superscript_representations(self):
        for variant in ("m<sup>-2</sup>", "m^{-2}"):
            with self.subTest(variant=variant):
                self.assert_status(0, self.compare("m⁻²", variant))

    def test_html_attribute_numbers_remain_checked(self):
        self.assert_status(
            1,
            self.compare('m<sup data-index="2">2</sup>', 'm<sup data-index="3">2</sup>'),
        )

    def test_numeric_bases_keep_their_own_scripts(self):
        for original, revision in (("10³，2²", "10²，2³"), ("10₂，2₇", "10₇，2₂")):
            with self.subTest(original=original):
                self.assert_status(1, self.compare(original, revision))

    def test_charge_sign_including_without_magnitude(self):
        for element in ("Na", "Fe³"):
            with self.subTest(element=element):
                self.assert_status(1, self.compare(element + "⁺", element + "⁻"))
        self.assert_status(0, self.compare("Fe³⁺", "Fe<sup>3+</sup>"))

    def test_html_entities_in_bounds_and_scripts(self):
        self.assert_status(0, self.compare(
            "x &le; &minus;1.5，m<sup>&#x2212;2</sup>", "x ≤ −1.5，m⁻²"
        ))
        self.assert_status(1, self.compare("y &le; 8", "y &ge; 8"))

    def test_fullwidth_not_equal(self):
        self.assert_status(0, self.compare("x ！＝ 2", "x ≠ 2"))
        self.assert_status(1, self.compare("x ！＝ 2", "x ＝ 2"))

    def test_changed_numeric_comparisons_are_detected(self):
        cases = (
            ("x < 5", "x > 5"),
            ("x ≤ 5", "x ≥ 5"),
            ("x ＜＝ 5", "x ＞＝ 5"),
            (r"x \leq 5", r"x \geq 5"),
            ("0 < x", "0 > x"),
            ("0 < |x|", "0 > |x|"),
        )
        for before, after in cases:
            with self.subTest(before=before, after=after):
                self.assert_status(1, self.compare(before, after))

    def test_numeric_formula_operand_change_is_detected(self):
        self.assert_status(1, self.compare("$y = x + 4$", "$y = x - 4$"))

    def test_slanted_tex_inequalities_keep_direction_and_inclusion(self):
        self.assert_status(1, self.compare(r"x \leqslant 5", r"x \geqslant 5"))
        self.assert_status(1, self.compare(r"0 \leqslant x", "0 < x"))

    def test_equivalent_symbols_survive_typesetting_changes(self):
        self.assert_status(0, self.compare(r"x \geq -20\%", "x ≥ −20％"))
        self.assert_status(0, self.compare("5 ＜＝ x", r"5 \leqslant x"))

    def test_markdown_bullet_signs_are_ignored(self):
        self.assert_status(0, self.compare("- 4 ms\n- 6 ms\n", "+ 4 ms\n* 6 ms\n"))

    def test_plain_text_leading_signs_are_not_bullets(self):
        self.assert_status(1, self.compare("- 4\n", "+ 4\n", suffix=".txt"))

    def test_markdown_math_blocks_preserve_leading_signs(self):
        for opener, closer in (
            ("$$", "$$"),
            (r"\[", r"\]"),
            (r"\begin{align*}", r"\end{align*}"),
        ):
            with self.subTest(opener=opener):
                self.assert_status(
                    1,
                    self.compare(f"{opener}\n- 4\n{closer}\n", f"{opener}\n+ 4\n{closer}\n"),
                )

    def test_markdown_fenced_code_preserves_leading_signs(self):
        for fence in ("```", "~~~"):
            with self.subTest(fence=fence):
                self.assert_status(1, self.compare(f"{fence}\n- 4\n{fence}", f"{fence}\n+ 4\n{fence}"))

    def test_ams_display_subenvironments_preserve_leading_signs(self):
        for name in ("cases", "split", "aligned"):
            with self.subTest(name=name):
                math = "\\begin{" + name + "}\n- 4\n\\end{" + name + "}"
                self.assert_status(1, self.compare(math, math.replace("- 4", "+ 4")))
                self.assert_status(0, self.compare(math + "\n- 5", math + "\n+ 5"))

    def test_chinese_pipe_diagnostics_use_utf8(self):
        original, final = self.root / "source.txt", self.root / "result.txt"
        original.write_text("尚未测量", encoding="utf-8")
        final.write_text("已经测量", encoding="utf-8")
        env = dict(os.environ, PYTHONIOENCODING="ascii:strict")
        result = self.run_cli(original, final, "--keep", "尚未", env=env)
        self.assert_status(1, result)
        self.assertIn("尚未", result.stdout)
        missing = self.run_cli(original, final, "--keep", "缺失", env=env)
        self.assert_status(2, missing)
        self.assertIn("缺失", missing.stderr)

    def test_markdown_quoted_math_preserves_leading_signs(self):
        self.assert_status(1, self.compare(
            "> $$\n> - 4\n> $$\n- 6 ms\n",
            "> $$\n> + 4\n> $$\n+ 6 ms\n",
        ))

    def test_keep_detects_same_number_with_changed_unit(self):
        self.assert_status(1, self.compare("延迟 12 ms。", "延迟 12 s。", "--keep", "12 ms"))

    def test_keep_detects_lost_negation(self):
        self.assert_status(1, self.compare("其他工况尚未验证。", "其他工况已经验证。", "--keep", "尚未验证"))

    def test_keep_detects_changed_formula_without_numbers(self):
        self.assert_status(1, self.compare("$a+b$", "$a-b$", "--keep", "a+b"))

    def test_keep_accepts_hyphen_leading_fragment(self):
        self.assert_status(0, self.compare("运行 --dry-run", "运行 --dry-run", "--keep=--dry-run"))
        self.assert_status(1, self.compare("运行 --dry-run", "运行 --force", "--keep=--dry-run"))

    def test_repeated_keep_preserves_occurrence_check(self):
        self.assert_status(1, self.compare("未测，未测。", "未测。", "--keep", "未测", "--keep", "未测"))

    def test_invalid_keep_returns_two(self):
        for fragment in ("", "原文中不存在"):
            with self.subTest(fragment=fragment):
                self.assert_status(2, self.compare("已有材料", "已有材料", "--keep", fragment))

    def test_missing_file_returns_two(self):
        self.assert_status(2, self.run_cli(self.root / "absent-before.md", self.root / "absent-after.md"))

    def test_invalid_utf8_returns_two(self):
        before = self.root / "before.md"
        after = self.root / "after.md"
        before.write_bytes(b"\xff\xfe\x00")
        after.write_text("结果", encoding="utf-8")
        self.assert_status(2, self.run_cli(before, after))

    def test_missing_argument_returns_two(self):
        self.assert_status(2, self.run_cli())

    def test_blind_spot_group_value_swap(self):
        # This is an intentional limitation: equal counts do not preserve assignment.
        self.assert_status(0, self.compare("A 组 6 ms，B 组 9 ms。", "A 组 9 ms，B 组 6 ms。"))

    def test_blind_spot_same_number_with_changed_unit(self):
        # Unit semantics require --keep or a separate editorial check.
        self.assert_status(0, self.compare("延迟 12 ms。", "延迟 12 s。"))

    def test_blind_spot_formula_without_numbers(self):
        self.assert_status(0, self.compare("$a+b$", "$a-b$"))


if __name__ == "__main__":
    unittest.main()
