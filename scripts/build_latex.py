#!/usr/bin/env python3
"""Build a trusted LaTeX project in a new working copy, with a JSON receipt.

No tool installation, shell escape, or reuse of old build products. This is
not an operating-system sandbox. Exit 0: fresh PDF and no unresolved-reference
warning; 1: failed/incomplete build; 2: invalid input or unavailable dependency.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import time

ENGINES = ("pdflatex", "xelatex", "lualatex")
SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", ".agents", ".claude", "node_modules"}
BUILD_SUFFIXES = {".aux", ".log", ".toc", ".lof", ".lot", ".bcf", ".blg", ".out",
                  ".fls", ".fdb_latexmk", ".synctex", ".nav", ".snm", ".vrb"}
UNRESOLVED = re.compile(r"(?:Citation|Reference)\b[^\n]*undefined|There were undefined|"
                        r"Rerun to get cross-references right|Label\(s\) may have changed|"
                        r"Please\s+(?:\(re\)run|rerun)\s+(?:Biber|LaTeX|BibTeX)", re.I)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def probe():
    results = {}
    for name in (*ENGINES, "bibtex", "biber"):
        exe = shutil.which(name)
        item = {"path": exe, "available": bool(exe), "version": None}
        if exe:
            try:
                proc = subprocess.run([exe, "--version"], capture_output=True, timeout=8,
                                      encoding="utf-8", errors="replace")
                item["version"] = (proc.stdout or proc.stderr).splitlines()[0] if (proc.stdout or proc.stderr) else None
                item["version_exit_code"] = proc.returncode
            except (OSError, subprocess.TimeoutExpired) as exc:
                item["version_error"] = str(exc)
        results[name] = item
    return results


def run_step(command, cwd, env, timeout, log_path):
    start = time.monotonic()
    cleanup = None
    with Path(log_path).open("xb") as stream:
        proc = subprocess.Popen(command, cwd=cwd, env=env, stdout=stream, stderr=subprocess.STDOUT,
                                start_new_session=os.name != "nt",
                                creationflags=(subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP)
                                if os.name == "nt" else 0)
        timed_out = False
        try:
            code = proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            cleanup = {"scope": "Windows process tree" if os.name == "nt" else "created POSIX process group",
                       "errors": [], "descendants_independently_verified": False}
            tree_requested = False
            try:
                if os.name == "nt":
                    killer = subprocess.run(["taskkill.exe", "/PID", str(proc.pid), "/T", "/F"],
                                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5,
                                            creationflags=subprocess.CREATE_NO_WINDOW)
                    tree_requested = killer.returncode == 0
                    if not tree_requested:
                        cleanup["errors"].append("taskkill exited " + str(killer.returncode))
                else:
                    os.killpg(proc.pid, signal.SIGKILL)
                    tree_requested = True
            except ProcessLookupError:
                tree_requested = True
            except (OSError, subprocess.SubprocessError) as exc:
                cleanup["errors"].append(str(exc))
            # A missing/failing tree helper must not bypass root-process cleanup.
            try:
                if proc.poll() is None:
                    proc.kill()
                code = proc.wait(timeout=5)
            except (OSError, subprocess.SubprocessError) as exc:
                cleanup["errors"].append(str(exc))
                code = proc.poll()
            cleanup["root_stopped"] = code is not None
            cleanup["status"] = ("completed_within_scope" if tree_requested else "partial") if code is not None else "failed"
    result = {"command": command, "cwd": str(cwd), "exit_code": code, "timed_out": timed_out,
              "seconds": round(time.monotonic() - start, 3), "log": str(log_path)}
    if cleanup is not None:
        result["cleanup"] = cleanup
    return result


def snapshot(root, entry, output):
    files, size = [], 0
    for directory, dirs, names in os.walk(root, followlinks=False):
        directory = Path(directory)
        keep = []
        for name in dirs:
            path = directory / name
            if name in SKIP_DIRS or path.resolve() == output:
                continue
            if path.is_symlink() or getattr(path, "is_junction", lambda: False)():
                raise ValueError(f"Project directory link not copied: {path}")
            keep.append(name)
        dirs[:] = keep
        for name in names:
            path = directory / name
            if path.is_symlink():
                raise ValueError(f"Project file link not copied: {path}")
            if path == entry.with_suffix(".pdf") or path.suffix in BUILD_SUFFIXES or name.endswith((".synctex.gz", ".run.xml")):
                continue
            if name == ".env" or name.startswith(".env."):
                continue
            size += path.stat().st_size
            if size > 512 * 1024 * 1024 or len(files) >= 10000:
                raise ValueError("Project exceeds 512 MiB/10000 files; choose a narrower project root")
            files.append({"path": path.relative_to(root).as_posix(), "sha256": digest(path)})
    return files


def build(entry, root, output, engine="xelatex", bibliography="auto", passes=3, timeout=120):
    root, entry, output = Path(root).resolve(), Path(entry).resolve(), Path(output).resolve()
    if not root.is_dir() or not entry.is_file() or entry.suffix.lower() != ".tex":
        raise ValueError("Require an existing project directory and .tex entry file")
    if not entry.is_relative_to(root):
        raise ValueError("Entry must be inside --project-root")
    if output == root or root.is_relative_to(output) or output.exists():
        raise ValueError("--output-dir must be new and must not contain the project root")
    if passes < 1 or passes > 10 or not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("Use 1–10 passes and a positive per-command timeout")
    tools = probe()
    if not tools[engine]["available"]:
        return {"schema": "thesisforge.latex-build/1", "status": "TOOL_UNAVAILABLE",
                "tool": engine, "tools": tools, "rendering": "NOT_RUN"}, 2
    inputs = snapshot(root, entry, output)
    output.mkdir(parents=True)
    work = output / "source"
    artifacts = output / "artifacts"
    artifacts.mkdir()
    report = {"schema": "thesisforge.latex-build/1", "status": "BUILD_FAILED", "entry": str(entry),
              "project_root": str(root), "output_dir": str(output), "tools": tools,
              "inputs": inputs, "commands": [], "shell_escape": False, "sandboxed": False,
              "visual_review": "NOT_RUN", "pdf": None, "unresolved": [], "source_changed": []}
    code = 1
    try:
        for item in inputs:
            src, target = root / item["path"], work / item["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, target)
            if digest(target) != item["sha256"]:
                raise ValueError("Source changed while copying: " + item["path"])
        cwd = work / entry.relative_to(root).parent
        # TeX's include auxiliary files may need matching relative directories.
        for directory in [cwd, *(p for p in cwd.rglob("*") if p.is_dir())]:
            (artifacts / directory.relative_to(cwd)).mkdir(parents=True, exist_ok=True)
        env = os.environ.copy()
        env["openout_any"] = "p"
        env["BIBINPUTS"] = str(cwd) + "//" + os.pathsep + env.get("BIBINPUTS", "")
        env["BSTINPUTS"] = str(cwd) + "//" + os.pathsep + env.get("BSTINPUTS", "")
        command = [tools[engine]["path"], "-no-shell-escape", "-halt-on-error", "-interaction=nonstopmode",
                   "-file-line-error", "-recorder", "-output-directory=" + str(artifacts), "./" + entry.name]

        def execute(cmd, directory, label):
            result = run_step(cmd, directory, env, timeout, output / (label + ".log"))
            report["commands"].append(result)
            if result["exit_code"] or result["timed_out"]:
                raise RuntimeError("Command failed or timed out: " + label)

        execute(command, cwd, "tex-1")
        aux = artifacts / (entry.stem + ".aux")
        chosen = bibliography
        if chosen == "auto":
            chosen = "biber" if (artifacts / (entry.stem + ".bcf")).exists() else (
                "bibtex" if any(re.search(r"\\bibdata\s*\{", p.read_text(encoding="utf-8", errors="replace"))
                                for p in artifacts.rglob("*.aux")) else "none")
        report["bibliography_backend"] = chosen
        if chosen != "none":
            if not tools[chosen]["available"]:
                report["missing_tool"] = chosen
                report["status"] = "TOOL_UNAVAILABLE"
                code = 2
                raise RuntimeError("Bibliography backend unavailable: " + chosen)
            execute([tools[chosen]["path"], entry.stem], artifacts, "bibliography")
        for run in range(2, passes + 1):
            execute(command, cwd, f"tex-{run}")
        final_log = artifacts / (entry.stem + ".log")
        log_text = final_log.read_text(encoding="utf-8", errors="replace") if final_log.exists() else ""
        if not final_log.exists():
            raise RuntimeError("Engine did not produce a fresh TeX log")
        report["unresolved"] = [line.strip() for line in log_text.splitlines() if UNRESOLVED.search(line)]
        if chosen != "none" and passes < 2:
            report["unresolved"].append("Bibliography ran after the last TeX pass; rerun TeX to include its updated output")
        pdf = artifacts / (entry.stem + ".pdf")
        if not pdf.exists() or not pdf.read_bytes().startswith(b"%PDF-"):
            raise RuntimeError("Engine did not produce a fresh PDF")
        report["pdf"] = {"path": str(pdf), "sha256": digest(pdf), "bytes": pdf.stat().st_size}
        report["status"] = "REVIEW_NEEDED" if report["unresolved"] else "BUILT"
        code = 1 if report["unresolved"] else 0
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        report["error"] = str(exc)
    finally:
        for item in inputs:
            try:
                unchanged = digest(root / item["path"]) == item["sha256"]
            except OSError:
                unchanged = False
            if not unchanged:
                report["source_changed"].append(item["path"])
        if report["source_changed"]:
            report["status"] = "SOURCE_CHANGED"
            code = 1
        with (output / "build-report.json").open("x", encoding="utf-8") as stream:
            json.dump(report, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
    return report, code


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entry", type=Path, nargs="?")
    parser.add_argument("--project-root", type=Path)
    parser.add_argument("--output-dir", type=Path, help="New directory; receipts and working copy remain available after failure")
    parser.add_argument("--engine", choices=ENGINES, default="xelatex")
    parser.add_argument("--bib", choices=("auto", "none", "bibtex", "biber"), default="auto")
    parser.add_argument("--passes", type=int, default=3, help="TeX passes including initial pass (1–10); unresolved references still fail")
    parser.add_argument("--timeout", type=float, default=120, help="Seconds per command")
    parser.add_argument("--probe", action="store_true", help="Only probe executables and versions, without compiling")
    args = parser.parse_args(argv)
    if args.probe:
        print(json.dumps({"tools": probe(), "rendering": "NOT_RUN"}, ensure_ascii=False, indent=2))
        return 0
    if not all((args.entry, args.project_root, args.output_dir)):
        parser.error("entry, --project-root and --output-dir are required without --probe")
    try:
        report, code = build(args.entry, args.project_root, args.output_dir, args.engine, args.bib, args.passes, args.timeout)
    except (OSError, ValueError) as exc:
        report, code = {"status": "INPUT_ERROR", "error": str(exc)}, 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    raise SystemExit(main())
