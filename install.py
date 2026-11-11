"""Install ThesisForge for Claude Code or Codex using the Python standard library."""

import argparse
from contextlib import ExitStack
from datetime import datetime, timezone
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
from uuid import uuid4


SOURCE = Path(__file__).resolve().parent
NAME = "thesisforge"
RESOURCE_PATTERNS = ("references/*.md", "templates/*.md", "scripts/*.py")


def package_files():
    paths = [Path("SKILL.md"), Path("LICENSE"), Path("NOTICE"), Path("agents/openai.yaml")]
    for pattern in RESOURCE_PATTERNS:
        paths.extend(path.relative_to(SOURCE) for path in sorted(SOURCE.glob(pattern)))
    # These are the runnable example and archived inputs linked by the figure guide.
    example = Path("dev/noc-smoke")
    paths.extend(example / name for name in (
        "README.md", "article.md", "mesh.py", "test_mesh.py", "experiment.py", "analyze.py",
        "plot_search_effects.py", "paired-search-effects.pdf", "paired-search-effects.png",
        "results/.gitattributes", "results/paired.csv", "results/search.csv", "results/summary.csv",
    ))
    for path in paths:
        if not (SOURCE / path).is_file():
            raise ValueError(f"Source file missing: {path}")
    return paths


def install_targets(host, project):
    base = project.expanduser().resolve() if project else Path.home()
    configs = {"codex": base / ".agents", "claude": base / ".claude"}
    if project is None and os.environ.get("CLAUDE_CONFIG_DIR"):
        configs["claude"] = Path(os.environ["CLAUDE_CONFIG_DIR"]).expanduser()
    hosts = configs if host == "both" else (host,)
    # The two host directories may already share a physical skills directory.
    return list(dict.fromkeys((configs[key] / "skills").resolve() / NAME for key in hosts))


def install_state(target, files, update):
    if not os.path.lexists(target):
        return "new"
    if target.resolve() == SOURCE:
        return "current"
    if target.is_dir() and all(
        (target / path).is_file() and (target / path).read_bytes() == (SOURCE / path).read_bytes()
        for path in files
    ):
        # A release can retire a guide or tool without changing any remaining file.
        if not update or all(
            path.relative_to(target) in files
            for pattern in RESOURCE_PATTERNS for path in target.glob(pattern)
        ):
            return "current"
    if target.is_symlink() or target.resolve() != target or not target.is_dir():
        raise ValueError(f"Target is a file or a redirected directory: {target}")
    if not update:
        raise ValueError(f"Different installation at {target}. Use --update to back it up and replace it.")
    manifest = target / "SKILL.md"
    if not manifest.is_file():
        raise ValueError(f"Existing directory has no SKILL.md: {target}")
    front = re.match(r"^---\r?\n(.*?)\r?\n---(?:\r?\n|$)",
                     manifest.read_text(encoding="utf-8-sig"), re.DOTALL)
    if not front or not re.search(r"""^name:[ \t]*['"]?thesisforge['"]?[ \t]*$""",
                                  front[1], re.MULTILINE | re.IGNORECASE):
        raise ValueError(f"Existing skill has a different name: {target}")
    if SOURCE.is_relative_to(target):
        raise ValueError(f"Target contains the source checkout: {target}")
    return "update"


def stage_copy(target, files, staging):
    # Keep the temporary copy outside the host's scanned skills directory.
    target.parent.mkdir(parents=True, exist_ok=True)
    scratch = staging.enter_context(tempfile.TemporaryDirectory(
        prefix=".thesisforge-stage-", dir=target.parent.parent))
    staged = Path(scratch) / NAME
    for path in files:
        dest = staged / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SOURCE / path, dest)
    return staged


def install_copies(targets, files, update):
    states = {target: install_state(target, files, update) for target in targets}
    backups = {}
    with ExitStack() as staging, ExitStack() as rollback:
        copies = {target: stage_copy(target, files, staging)
                  for target in targets if states[target] != "current"}
        for target, staged in copies.items():
            if states[target] == "update":
                stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
                backup = target.parent.parent / "thesisforge-backups" / f"{stamp}-{uuid4().hex}" / NAME
                backup.parent.mkdir(parents=True)
                rollback.callback(backup.parent.rmdir)
                target.rename(backup)
                rollback.callback(backup.rename, target)
                backups[target] = backup
            staged.rename(target)
            rollback.callback(target.rename, staged)
        rollback.pop_all()

    for target, state in states.items():
        if target in backups:
            print(f"Previous copy: {backups[target]}")
        print(f"{'Already installed' if state == 'current' else 'Installed'}: {target}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", required=True, choices=("claude", "codex", "both"))
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--project", type=Path, metavar="DIRECTORY", help="install for this research project")
    scope.add_argument("--user", action="store_true", help="install for the current OS user")
    parser.add_argument("--update", action="store_true", help="back up a differing copy before replacing it")
    args = parser.parse_args()
    try:
        files = package_files()
        targets = install_targets(args.host, args.project)
        install_copies(targets, files, args.update)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"{exc}\n")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="backslashreplace")
    main()
