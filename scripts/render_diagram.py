"""Render a diagram with an already installed Mermaid or draw.io CLI.

No package downloads, shell command strings, or edits to the original. Output
goes to a new directory with source, command logs and a JSON receipt. A successful
export still needs semantic and final-size visual review.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import signal
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from xml.parsers import expat


def file_info(path):
    raw = path.read_bytes()
    return {"path": str(path), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def inspect_output(path, fmt):
    raw = path.read_bytes()
    if not raw:
        raise ValueError("Renderer produced an empty file")
    if fmt == "svg":
        # Let the XML parser recognize declarations using the document encoding:
        # a byte substring check misses UTF-16 entity declarations. Expat does
        # not fetch external DTDs and parameter entity parsing stays disabled.
        guard = expat.ParserCreate()
        guard.SetParamEntityParsing(expat.XML_PARAM_ENTITY_PARSING_NEVER)
        def reject_entity(*_args):
            raise ValueError("SVG entity declarations are outside this static inspector's coverage")
        guard.EntityDeclHandler = reject_entity
        guard.Parse(raw, True)
        root = ET.fromstring(raw)
        if root.tag.split("}")[-1] != "svg":
            raise ValueError("Output is not an SVG root")
        tags = [node.tag.split("}")[-1] for node in root.iter()]
        return {"width": root.get("width"), "height": root.get("height"), "viewBox": root.get("viewBox"),
                "text_nodes": tags.count("text"), "images": tags.count("image"),
                "foreign_objects": tags.count("foreignObject"),
                "visual_review": "not_run", "note": "XML structure only; label clipping, overlap and final font size need rendering"}
    if fmt == "pdf" and not raw.startswith(b"%PDF-"):
        raise ValueError("Output does not have a PDF header")
    if fmt == "png" and not raw.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("Output does not have a PNG signature")
    return {"container_signature": "recognized", "visual_review": "not_run"}


def terminate_process_tree(process):
    """Terminate only this invocation's PID tree/session; report bounded cleanup."""
    cleanup = {"pid": process.pid, "status": "failed", "root_exited": False,
               "descendants_independently_verified": False}
    tree_requested = False
    if os.name == "nt":
        cleanup["method"] = "taskkill /PID <this invocation PID> /T /F"
        cleanup["scope"] = "Windows descendants still associated with this PID"
        try:
            result = subprocess.run(["taskkill.exe", "/PID", str(process.pid), "/T", "/F"],
                                    stdin=subprocess.DEVNULL, capture_output=True,
                                    timeout=5, creationflags=subprocess.CREATE_NO_WINDOW)
            cleanup["returncode"] = result.returncode
            cleanup["stdout"] = result.stdout.decode("utf-8", "replace")[:2000]
            cleanup["stderr"] = result.stderr.decode("utf-8", "replace")[:2000]
            tree_requested = result.returncode == 0
        except (OSError, subprocess.TimeoutExpired) as exc:
            cleanup["error"] = str(exc)
    else:
        cleanup["method"] = "killpg(SIGKILL)"
        cleanup["scope"] = "Process group in this invocation's new session; detached groups are outside coverage"
        try:
            os.killpg(process.pid, signal.SIGKILL)
            tree_requested = True
        except ProcessLookupError:
            cleanup["group_already_absent"] = True
            tree_requested = True
        except OSError as exc:
            cleanup["error"] = str(exc)
    # If group cleanup failed, at least terminate the directly owned process.
    if not tree_requested and process.poll() is None:
        try:
            process.kill()
            cleanup["root_fallback"] = "kill requested"
        except OSError as exc:
            cleanup["root_fallback"] = str(exc)
    try:
        process.wait(timeout=5)
        cleanup["root_exited"] = True
    except subprocess.TimeoutExpired:
        cleanup["root_wait"] = "timeout"
    cleanup["status"] = ("completed_within_scope" if tree_requested and cleanup["root_exited"]
                         else "partial" if cleanup["root_exited"] else "failed")
    return cleanup


def run_process(command, timeout, stdout, stderr, cwd=None):
    """File-backed streams prevent orphaned pipe handles from blocking timeout."""
    options = ({"creationflags": subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP}
               if os.name == "nt" else {"start_new_session": True})
    process = subprocess.Popen(command, cwd=cwd, stdin=subprocess.DEVNULL,
                               stdout=stdout, stderr=stderr, **options)
    execution = {"pid": process.pid, "status": "completed", "timeout_seconds": timeout}
    try:
        execution["returncode"] = process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        execution["status"] = "timeout"
        execution["cleanup"] = terminate_process_tree(process)
        execution["returncode"] = process.poll()
    return execution


def resolve_program(value):
    resolved = shutil.which(value)
    if not resolved:
        candidate = Path(value).expanduser().absolute()
        if candidate.is_file():
            resolved = str(candidate)
    if not resolved:
        raise ValueError(f"Renderer unavailable: {value}. Install/select a project-local tool explicitly")
    if os.name == "nt" and Path(resolved).suffix.lower() in {".cmd", ".bat", ".ps1"}:
        raise ValueError("Use a real executable; for Mermaid on Windows use --program node --entry <installed CLI JavaScript>")
    return str(Path(resolved).absolute())


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--backend", required=True, choices=("mermaid", "drawio"))
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--format", choices=("svg", "pdf", "png"), default="svg")
    parser.add_argument("--program", help="Actual executable; defaults to mmdc or drawio")
    parser.add_argument("--entry", type=Path, help="Optional script argument after the executable, e.g. Mermaid's local CLI JS")
    parser.add_argument("--config", type=Path, help="Mermaid JSON config; explicitly supplied and copied into the run")
    parser.add_argument("--timeout", type=float, default=60)
    parser.add_argument("--page", type=int, help="draw.io zero-based page index; omitted uses backend default, recorded below")
    args = parser.parse_args(argv)
    output = None
    record = {"schema": 1, "started_at": datetime.now(timezone.utc).isoformat(), "status": "failed",
              "backend": args.backend, "format": args.format, "semantic_review": "not_run", "visual_review": "not_run"}
    try:
        if not math.isfinite(args.timeout) or args.timeout <= 0:
            raise ValueError("Timeout must be positive and finite")
        if args.page is not None and (args.backend != "drawio" or args.page < 0):
            raise ValueError("--page is a nonnegative draw.io page index")
        if args.config and args.backend != "mermaid":
            raise ValueError("--config is only supported for Mermaid")
        source = args.input.resolve(strict=True)
        if not source.is_file():
            raise ValueError("Input must be a file")
        record["input"] = file_info(source)
        prefix = [resolve_program(args.program or ("mmdc" if args.backend == "mermaid" else "drawio"))]
        if args.entry:
            entry = args.entry.resolve(strict=True)
            if not entry.is_file():
                raise ValueError("--entry must be a file")
            prefix.append(str(entry))
            record["entry"] = file_info(entry)
        config_raw = None
        if args.config:
            config_raw = args.config.read_bytes()
            if not isinstance(json.loads(config_raw.decode("utf-8-sig")), dict):
                raise ValueError("Mermaid config must be a JSON object")
        output = args.output_dir.absolute()
        output.mkdir(parents=True, exist_ok=False)
        copied = output / ("source.mmd" if args.backend == "mermaid" else "source.drawio")
        shutil.copyfile(source, copied)
        record["source_copy"] = file_info(copied)
        if record["source_copy"]["sha256"] != record["input"]["sha256"]:
            raise ValueError("Input changed while being copied")
        artifact = output / ("figure." + args.format)
        if args.backend == "mermaid":
            command = prefix + ["-i", str(copied), "-o", str(artifact)]
            if config_raw is not None:
                config_path = output / "config.json"
                config_path.write_bytes(config_raw)
                command += ["-c", str(config_path)]
                record["config"] = file_info(config_path)
        else:
            command = prefix + ["--export", "--format", args.format, "--output", str(artifact), str(copied)]
            if args.page is not None:
                command += ["--page-index", str(args.page)]
            record["page_selection"] = args.page if args.page is not None else "backend default; not a verified all-pages export"
        record["command"] = command
        with tempfile.TemporaryFile() as version_stdout, tempfile.TemporaryFile() as version_stderr:
            version = run_process(prefix + ["--version"], min(args.timeout, 10), version_stdout, version_stderr)
            version_stdout.seek(0)
            version_stderr.seek(0)
            record["version_probe"] = dict(version, stdout=version_stdout.read(8000).decode("utf-8", "replace")[:2000],
                                           stderr=version_stderr.read(8000).decode("utf-8", "replace")[:2000])
        if version.get("cleanup", {}).get("status") in {"partial", "failed"}:
            raise ValueError("Version probe timed out and process tree cleanup was incomplete; inspect version_probe.cleanup")
        with (output / "stdout.log").open("wb") as stdout, (output / "stderr.log").open("wb") as stderr:
            execution = run_process(command, args.timeout, stdout, stderr, cwd=output)
        record["execution"] = execution
        record["returncode"] = execution["returncode"]
        if execution["status"] == "timeout":
            raise ValueError("Renderer timed out; inspect execution.cleanup and stdout.log/stderr.log")
        if execution["returncode"] != 0:
            raise ValueError(f"Renderer exited {execution['returncode']}; inspect stdout.log/stderr.log")
        if file_info(source)["sha256"] != record["input"]["sha256"]:
            raise ValueError("Original source changed during rendering")
        record["inspection"] = inspect_output(artifact, args.format)
        record["artifact"] = file_info(artifact)
        record["status"] = "exported_not_visually_verified"
    except (OSError, ValueError, ET.ParseError, expat.ExpatError, subprocess.TimeoutExpired) as exc:
        record["error"] = str(exc)
    finally:
        record["finished_at"] = datetime.now(timezone.utc).isoformat()
        # Only write a receipt in a directory successfully created by this run.
        if output is not None and "source_copy" in record:
            (output / "render.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0 if record["status"] == "exported_not_visually_verified" else 2


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="strict")
    raise SystemExit(main())
