"""Verify a staged skill copy and its resources in isolated host directories."""
from contextlib import redirect_stdout
from io import StringIO
import os
from pathlib import Path
import re
import runpy
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
INSTALL = ROOT / "install.py"


class InstallTests(unittest.TestCase):
    def setUp(self):
        workspace = tempfile.TemporaryDirectory(prefix="thesisforge-test-")
        self.addCleanup(workspace.cleanup)
        self.project = Path(workspace.name) / "中文 project"
        self.project.mkdir()

    def invoke(self, host, *extra):
        return subprocess.run(
            [sys.executable, "-B", str(INSTALL), "--host", host,
             "--project", str(self.project), *extra],
            cwd=self.project, capture_output=True, timeout=45,
        )

    def test_both_project_installations_can_load_their_own_resources(self):
        result = self.invoke("both")
        self.assertEqual(result.returncode, 0, result.stderr)
        for host in (".agents", ".claude"):
            skill = self.project / host / "skills" / "thesisforge"
            front = (skill / "SKILL.md").read_text(encoding="utf-8")
            self.assertRegex(front.split("---", 2)[1], r"""(?m)^name:\s*['"]?thesisforge['"]?\s*$""")
            for page in skill.rglob("*.md"):
                for target in re.findall(r"\]\(([^()\s]+)\)", page.read_text(encoding="utf-8")):
                    if "://" in target or target.startswith(("#", "mailto:")):
                        continue
                    relative = target.split("#")[0]
                    self.assertTrue((page.parent / relative).exists(), (page, relative))
            self.assertTrue((skill / "agents" / "openai.yaml").is_file())
            for name in ("LICENSE", "NOTICE"):
                self.assertEqual((skill / name).read_bytes(), (ROOT / name).read_bytes())
            self.assertFalse((skill / "dev" / "iteration-log.md").exists())
            replay = subprocess.run(
                [sys.executable, "-B", str(skill / "dev" / "noc-smoke" / "test_mesh.py")],
                cwd=self.project, capture_output=True, timeout=45,
            )
            self.assertEqual(replay.returncode, 0, replay.stderr)

    def test_matching_installation_is_reused_and_update_backs_up_local_edits(self):
        skill = self.project / ".claude" / "skills" / "thesisforge"
        self.assertEqual(self.invoke("claude").returncode, 0)
        note = skill / "private-note.txt"
        note.write_bytes(b"personal notes")
        self.assertEqual(self.invoke("claude").returncode, 0)
        self.assertEqual(note.read_bytes(), b"personal notes")
        guide = skill / "references" / "data-analysis.md"
        guide.write_bytes(b"local edits")
        self.assertNotEqual(self.invoke("both").returncode, 0)
        self.assertEqual(guide.read_bytes(), b"local edits")
        self.assertFalse((self.project / ".agents" / "skills" / "thesisforge").exists())

        result = self.invoke("claude", "--update")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(guide.read_bytes(), (ROOT / "references" / "data-analysis.md").read_bytes())
        saved = [p for p in self.project.rglob("private-note.txt") if skill.parent not in p.parents]
        self.assertEqual(len(saved), 1)
        self.assertEqual(saved[0].read_bytes(), b"personal notes")
        self.assertEqual((saved[0].parent / "references" / "data-analysis.md").read_bytes(), b"local edits")

    def test_explicit_update_backs_up_a_retired_tool(self):
        skill = self.project / ".agents" / "skills" / "thesisforge"
        self.assertEqual(self.invoke("codex").returncode, 0)
        retired = skill / "scripts" / "retired.py"
        retired.write_text("# previous release", encoding="utf-8")
        self.assertEqual(self.invoke("codex", "--update").returncode, 0)
        self.assertFalse(retired.exists())
        backup = self.project / ".agents" / "thesisforge-backups"
        self.assertEqual([p.read_bytes() for p in backup.rglob("retired.py")], [b"# previous release"])

    def test_explicit_update_cannot_replace_an_unrelated_skill(self):
        skill = self.project / ".agents" / "skills" / "thesisforge"
        skill.mkdir(parents=True)
        front = b"---\nname: other-skill\ndescription: Different purpose.\n---\n"
        (skill / "SKILL.md").write_bytes(front)
        result = self.invoke("codex", "--update")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((skill / "SKILL.md").read_bytes(), front)

    def test_both_hosts_are_prepared_before_installation(self):
        blocked = self.project / ".claude" / "skills"
        blocked.parent.mkdir()
        blocked.write_bytes(b"occupied")
        result = self.invoke("both")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.project / ".agents/skills/thesisforge").exists())
        self.assertEqual(blocked.read_bytes(), b"occupied")

    def test_failed_second_replacement_restores_both_previous_copies(self):
        self.assertEqual(self.invoke("both").returncode, 0)
        api = runpy.run_path(str(INSTALL))
        targets = api["install_targets"]("both", self.project)
        for target in targets:
            (target / "NOTICE").write_bytes(target.parent.parent.name.encode())
        rename = Path.rename

        def fail_second_publish(source, destination):
            if destination == targets[1] and source.parent.name.startswith(".thesisforge-stage-"):
                raise OSError("simulated second-host replacement failure")
            return rename(source, destination)

        with patch.object(Path, "rename", new=fail_second_publish):
            with self.assertRaisesRegex(OSError, "second-host"):
                api["install_copies"](targets, api["package_files"](), True)
        for target in targets:
            self.assertEqual((target / "NOTICE").read_bytes(), target.parent.parent.name.encode())
            config = target.parent.parent
            self.assertFalse(list(config.glob(".thesisforge-stage-*")))
            self.assertFalse(list((config / "thesisforge-backups").iterdir()))

    def test_user_targets_honor_the_claude_config_directory(self):
        home = self.project / "isolated-user"
        custom = self.project / "claude config"
        args = [str(INSTALL), "--host", "both", "--user"]
        with patch.object(Path, "home", return_value=home), patch.object(sys, "argv", args), \
                patch.dict(os.environ, {"CLAUDE_CONFIG_DIR": str(custom)}), redirect_stdout(StringIO()):
            runpy.run_path(str(INSTALL), run_name="__main__")
        self.assertTrue((home / ".agents/skills/thesisforge/SKILL.md").is_file())
        self.assertTrue((custom / "skills/thesisforge/SKILL.md").is_file())
        self.assertFalse((home / ".claude/skills/thesisforge").exists())


if __name__ == "__main__":
    unittest.main()
