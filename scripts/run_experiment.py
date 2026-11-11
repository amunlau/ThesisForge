"""运行一条前台实验命令，并在全新目录记录参数、日志、耗时和文件摘要。"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def save_record(directory, record):
    staging = directory / "run.json.tmp"
    staging.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    staging.replace(directory / "run.json")


def fingerprint(path):
    if not path.is_file():
        raise ValueError(f"需要普通文件：{path}")
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
            size += len(block)
    return {"bytes": size, "sha256": digest.hexdigest()}


def resolve_program(cwd, program):
    """Resolve external programs against the experiment directory on both platforms."""
    if program == "{python}":
        return sys.executable
    path = Path(program)
    if os.path.dirname(program):
        directories = [cwd / path.parent]
    else:
        entries = os.get_exec_path()
        directories = [cwd / (entry.strip('"') if os.name == "nt" else entry) for entry in entries]
    names = [path.name]
    if os.name == "nt" and not path.suffix:
        extensions = os.environ.get("PATHEXT") or ".COM;.EXE;.BAT;.CMD"
        names.extend(path.name + ext for ext in extensions.split(os.pathsep) if ext)
    for directory in directories:
        for name in names:
            candidate = directory / name
            if candidate.is_file() and os.access(candidate, os.X_OK):
                # Keep venv symlinks as invoked: resolving them can select another environment.
                return str(candidate)
    return None


def validate_output_paths(paths):
    names = set(paths)
    if len(names) != len(paths):
        raise ValueError("声明的输出文件路径重复")
    for path in paths:
        if any(parent in names for parent in path.parents):
            raise ValueError(f"输出文件不能同时作为另一项输出的目录：{path}")


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description=__doc__,
        usage="%(prog)s --cwd DIR --run-dir NEW_DIR [--input FILE] [--output FILE] -- COMMAND [ARG ...]",
        epilog="相对路径以 --cwd 为基准。子进程可通过 THESISFORGE_RUN_DIR 取得绝对记录目录。"
               "COMMAND 可用 {python} 指定启动本工具的解释器。命令应在前台运行至文件写完。",
    )
    parser.add_argument("--cwd", required=True, type=Path, help="命令的工作目录")
    parser.add_argument("--run-dir", required=True, type=Path, help="本次运行的新目录")
    parser.add_argument("--input", action="append", default=[], type=Path,
                        help="声明应保持不变的输入文件，启动前与成功退出后核对内容，可重复")
    parser.add_argument("--output", action="append", default=[], type=Path, help="命令应新建的文件，可重复")
    split = argv.index("--") if "--" in argv else len(argv)
    options = parser.parse_args(argv[:split])
    command = argv[split + 1:]
    if not command or not command[0]:
        parser.error("在 -- 后指定可执行程序及参数")
    return options, command


def run(cwd, directory, command, inputs, outputs):
    # Resolve parent directories, preserving a final symlink for the existence check.
    paths = [path.parent.resolve() / path.name for path in (cwd / item for item in outputs)]
    reserved = {directory / name for name in ("run.json", "run.json.tmp", "stdout.log", "stderr.log")}
    started = time.monotonic()
    record = {
        "status": "preparing", "cwd": str(cwd), "run_dir": str(directory), "argv": command,
        "started_at": utc_now(), "finished_at": None, "elapsed_seconds": None,
        "command_elapsed_seconds": None, "exit_code": None, "errors": [],
        "inputs": [{"path": str(cwd / path)} for path in inputs],
        "inputs_verified_after_run": None, "executable": None,
        "outputs": [{"path": str(path)} for path in paths],
        "stdout": "stdout.log", "stderr": "stderr.log",
    }
    save_record(directory, record)
    try:
        with (directory / "stdout.log").open("xb") as stdout, (directory / "stderr.log").open("xb") as stderr:
            validate_output_paths(paths)
            for path in paths:
                if path in reserved or any(p in reserved for p in path.parents) or os.path.lexists(path):
                    raise ValueError(f"预期新输出与已有路径或记录文件冲突：{path}")
            for item in record["inputs"]:
                item.update(fingerprint(Path(item["path"])))

            env = os.environ.copy()
            env["THESISFORGE_RUN_DIR"] = str(directory)
            executable = resolve_program(cwd, command[0])
            if executable is None:
                raise FileNotFoundError(f"找不到可执行程序：{command[0]}")
            record["executable"] = executable
            argv = [executable, *command[1:]] if command[0] == "{python}" else command
            record["status"] = "running"
            save_record(directory, record)
            command_start = time.monotonic()
            try:
                process = subprocess.run(
                    argv, executable=executable, cwd=cwd, env=env, shell=False,
                    stdout=stdout, stderr=stderr, check=False,
                )
                record["exit_code"] = process.returncode
            finally:
                record["command_elapsed_seconds"] = time.monotonic() - command_start

        if process.returncode:
            record["errors"].append(f"命令退出码为 {process.returncode}")
        for item, path in zip(record["outputs"], paths):
            try:
                if path.is_symlink():
                    raise ValueError(f"预期新输出是符号链接：{path}")
                item.update(fingerprint(path))
            except (OSError, ValueError) as exc:
                record["errors"].append(str(exc))
        if not record["errors"]:
            record["inputs_verified_after_run"] = False
            for item in record["inputs"]:
                source = Path(item["path"])
                if fingerprint(source)["sha256"] != item["sha256"]:
                    record["errors"].append(f"运行结束时声明输入的内容已改变：{source}")
            record["inputs_verified_after_run"] = not record["errors"]
        record["status"] = "failed" if record["errors"] else "succeeded"
    except (OSError, ValueError) as exc:
        record["status"] = "failed"
        record["errors"].append(str(exc))
    except KeyboardInterrupt:
        record["status"] = "interrupted"
        record["errors"].append("用户中断运行")

    record["finished_at"] = utc_now()
    record["elapsed_seconds"] = time.monotonic() - started
    save_record(directory, record)
    print(directory / "run.json")
    for error in record["errors"]:
        print(error, file=sys.stderr)
    return 0 if record["status"] == "succeeded" else 1


def main():
    args, command = parse_args(sys.argv[1:])
    try:
        cwd = args.cwd.resolve(strict=True)
        if not cwd.is_dir():
            raise ValueError(f"工作目录无效：{cwd}")
        directory = (cwd / args.run_dir).absolute()
        directory.mkdir(parents=True, exist_ok=False)
        return run(cwd, directory.resolve(), command, args.input, args.output)
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="backslashreplace")
    sys.exit(main())
