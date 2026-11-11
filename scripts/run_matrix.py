"""按 JSON 清单串行运行前台实验，重新核验后接续已完成的单元。"""

import argparse
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import re
import sys

# Also allow the documented environment probe's isolated interpreter (-I).
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_experiment import fingerprint, resolve_program, run, validate_output_paths


def strings(value, label, *, allow_empty=False):
    if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
        raise ValueError(f"{label} 需要字符串组成的数组")
    if not allow_empty and "" in value:
        raise ValueError(f"{label} 中的文件名不能为空")
    return value


def unique_fields(pairs):
    fields = {}
    for key, value in pairs:
        if key in fields:
            raise ValueError(f"清单中同一 JSON 对象的字段重复：{key}")
        fields[key] = value
    return fields


def load_plan(path):
    raw_plan = path.read_bytes()
    plan = json.loads(raw_plan.decode("utf-8-sig"), object_pairs_hook=unique_fields)
    if not isinstance(plan, dict) or set(plan) - {"inputs", "outputs", "cases"}:
        raise ValueError("清单支持 inputs、outputs、cases")
    common = strings(plan.get("inputs", []), "inputs")
    outputs = strings(plan.get("outputs"), "outputs")
    if not outputs:
        raise ValueError("outputs 至少含一个原始结果文件")
    reserved = {"run.json", "stdout.log", "stderr.log", "run.json.tmp"}
    for name in outputs:
        parts = name.split("/")
        if (any(part in {"", ".", ".."} for part in parts) or "\\" in name or ":" in name
                or parts[0].lower() in reserved):
            raise ValueError(f"outputs 使用运行目录下的相对文件名，以 / 分隔：{name}")
    validate_output_paths([Path(name) for name in outputs])
    cases = plan.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("cases 需要至少一个实验单元")
    cells = {}
    for case in cases:
        if not isinstance(case, dict) or set(case) - {"id", "argv", "inputs"}:
            raise ValueError("实验单元支持 id、argv、inputs")
        key = case.get("id")
        if not isinstance(key, str) or not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", key) or key in cells:
            raise ValueError(f"单元 id 需唯一，采用小写字母、数字、短横线和下划线：{key!r}")
        argv = strings(case.get("argv"), f"{key} argv", allow_empty=True)
        if not argv or not argv[0]:
            raise ValueError(f"{key} 缺少可执行命令")
        inputs = common + strings(case.get("inputs", []), f"{key} inputs")
        cells[key] = (argv, [path.parent / p for p in inputs])
    return outputs, cells, hashlib.sha256(raw_plan).hexdigest()


@contextmanager
def exclusive_root(root):
    root.mkdir(parents=True, exist_ok=True)
    marker = root / ".thesisforge-matrix"
    if marker.is_symlink():
        raise ValueError(f"矩阵锁文件指向其他路径：{marker}")
    if not marker.is_file() and any(root.iterdir()):
        raise ValueError(f"请选择专用的空目录或已有矩阵目录：{root}")
    with marker.open("a+b") as lock:
        lock.seek(0)
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise ValueError(f"无法独占矩阵目录（已有运行或文件系统不支持锁）：{root}") from exc
        yield  # Closing the file releases its OS lock, including after process exit.


def invocation(cwd, directory, argv, inputs):
    command = [arg.replace("{run_dir}", str(directory)) for arg in argv]
    program = resolve_program(cwd, command[0]) or command[0]
    command[0] = program
    # Keep the venv launcher path intact even when it is a symlink to system Python.
    files = list(inputs)
    if Path(program).is_file() and Path(program).is_absolute():
        files.append(Path(program))
    return command, list(dict.fromkeys(files))


def verified_record(cwd, directory, argv, inputs, outputs):
    try:
        record = json.loads((directory / "run.json").read_text(encoding="utf-8"))
        command, files = invocation(cwd, directory, argv, inputs)
        results = [directory / name for name in outputs]
        if (record["status"] != "succeeded" or record["exit_code"] != 0
                or record.get("inputs_verified_after_run", True) is not True
                or record["argv"] != command or record["cwd"] != str(cwd)
                or record["run_dir"] != str(directory)
                or any(p.resolve() != p for p in results)):
            return None
        for group, paths in (("inputs", files), ("outputs", results)):
            if record[group] != [{"path": str(p), **fingerprint(p)} for p in paths]:
                return None
        if all((directory / name).is_file() for name in ("stdout.log", "stderr.log")):
            return record
    except (OSError, ValueError, KeyError, TypeError):
        return None
    return None


def write_index(root, index):
    stage = root / "index.json.tmp"
    if stage.is_symlink():
        raise ValueError(f"索引暂存文件指向其他路径：{stage}")
    stage.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    stage.replace(root / "index.json")


def execute(manifest, root, outputs, cells, plan_digest):
    cwd = manifest.parent
    rows = {key: {"status": "pending"} for key in cells}
    index = {"manifest": str(manifest), "manifest_sha256": plan_digest,
             "status": "running", "cases": rows}
    key = None
    try:
        write_index(root, index)
        for key, (argv, inputs) in cells.items():
            cell = root / ("case-" + key)
            if cell.resolve() != cell:
                raise ValueError(f"实验单元目录指向其他位置：{cell}")
            cell.mkdir(exist_ok=True)
            latest = max((int(p.name) for p in cell.iterdir() if re.fullmatch(r"[0-9]+", p.name)),
                         default=0)
            directory = cell / str(latest)
            if latest and directory.resolve() == directory and verified_record(cwd, directory, argv, inputs, outputs):
                rows[key] = {"status": "succeeded", "reused": True,
                             "record": str((directory / "run.json").relative_to(root))}
                write_index(root, index)
                continue
            directory = cell / str(latest + 1)
            directory.mkdir()
            command, files = invocation(cwd, directory, argv, inputs)
            rows[key] = {"status": "running", "reused": False,
                         "record": str((directory / "run.json").relative_to(root))}
            write_index(root, index)
            status = run(cwd, directory, command, files, [directory / name for name in outputs])
            rows[key]["status"] = "failed"
            if status == 0:
                rows[key]["status"] = "succeeded"
            elif json.loads((directory / "run.json").read_text(encoding="utf-8"))["status"] == "interrupted":
                rows[key]["status"] = "interrupted"
                raise KeyboardInterrupt
            write_index(root, index)
        # A later cell may have changed an earlier cell's data or output.
        for key, (argv, inputs) in cells.items():
            row = rows[key]
            if row["status"] == "succeeded":
                directory = (root / row["record"]).parent
                record = verified_record(cwd, directory, argv, inputs, outputs)
                if record is None:
                    row["status"] = "failed"
                    row["error"] = "矩阵结束时复核失败，请检查输入与产物是否在运行期间变化。"
                else:
                    row["inputs_verified_after_run"] = record.get("inputs_verified_after_run")
        ok = all(row["status"] == "succeeded" for row in rows.values())
        index["status"] = "succeeded" if ok else "failed"
        write_index(root, index)
    except KeyboardInterrupt:
        index["status"] = "interrupted"
        for row in rows.values():
            if row["status"] == "running":
                row["status"] = "interrupted"
            elif row["status"] == "pending":
                row["status"] = "not_started"
        write_index(root, index)
        return 130
    except (OSError, ValueError) as exc:
        index["status"] = "failed"
        index["error"] = str(exc)
        if key is not None and rows[key]["status"] in {"pending", "running", "failed"}:
            rows[key].update(status="failed", error=str(exc))
        for row in rows.values():
            if row["status"] == "pending":
                row["status"] = "not_started"
        print(f"矩阵执行失败：{exc}", file=sys.stderr)
        try:
            write_index(root, index)
        except (OSError, ValueError) as index_error:
            print(f"未能更新终态索引 {root / 'index.json'}：{index_error}", file=sys.stderr)
        return 2
    print(root / "index.json")
    return 0 if ok else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--run-dir", required=True, type=Path, help="矩阵专用目录，相对清单定位")
    args = parser.parse_args()
    try:
        manifest = args.manifest.resolve(strict=True)
        outputs, cells, plan_digest = load_plan(manifest)
        root = (manifest.parent / args.run_dir).resolve()
        with exclusive_root(root):
            return execute(manifest, root, outputs, cells, plan_digest)
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="backslashreplace")
    sys.exit(main())
