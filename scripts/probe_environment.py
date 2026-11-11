"""Inventory a compute environment, optionally execute selected backend checks; print JSON."""

import argparse
import csv
import ctypes
import heapq
import io
import json
import os
import platform
import re
import shutil
import statistics
import subprocess
import sys
import sysconfig
import tempfile
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path, PurePosixPath


# The default inventory reads package metadata without importing third-party modules.
PACKAGES = {
    "data": ("numpy", "pandas", "scipy"),
    "simulation": ("numpy", "scipy", "simpy"),
    "hdl": ("cocotb",),
    "ai": ("numpy", "scikit-learn", "torch", "tensorflow", "transformers"),
}
COMMANDS = {
    "data": (),
    "simulation": ("ngspice", "cmake"),
    "hdl": ("iverilog", "vvp", "verilator", "ghdl", "yosys"),
    "ai": ("nvidia-smi",),
}
FLAGS = {
    "ngspice": ("--version",),
    "cmake": ("--version",),
    "iverilog": ("-V",),
    "vvp": ("-V",),
    "verilator": ("--version",),
    "ghdl": ("--version",),
    "yosys": ("-V",),
    "nvidia-smi": ("--query-gpu=name,driver_version,memory.total", "--format=csv,noheader"),
}


def memory_bytes():
    """Host physical memory. Unknown values remain null. Job limits can be lower."""
    memory = {"total": None, "available": None}
    if os.name == "nt":
        class MemoryStatus(ctypes.Structure):
            _fields_ = [
                ("length", ctypes.c_uint32), ("load", ctypes.c_uint32),
                ("total_physical", ctypes.c_uint64), ("available_physical", ctypes.c_uint64),
                ("total_pagefile", ctypes.c_uint64), ("available_pagefile", ctypes.c_uint64),
                ("total_virtual", ctypes.c_uint64), ("available_virtual", ctypes.c_uint64),
                ("available_extended_virtual", ctypes.c_uint64),
            ]

        info = MemoryStatus()
        info.length = ctypes.sizeof(info)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(info)):
            memory.update(total=info.total_physical, available=info.available_physical)
    else:
        try:
            pages = os.sysconf("SC_PHYS_PAGES")
            page_size = os.sysconf("SC_PAGE_SIZE")
            if min(pages, page_size) > 0:
                memory["total"] = pages * page_size
        except (AttributeError, ValueError, OSError):
            pass
        if sys.platform.startswith("linux"):
            try:
                for line in Path("/proc/meminfo").read_text(encoding="ascii").splitlines():
                    if line.startswith("MemAvailable:") and line.endswith(" kB"):
                        memory["available"] = int(line.split()[1]) * 1024
                        break
            except (ValueError, OSError):
                pass
    return memory


def cpu_count_for_process():
    if hasattr(os, "process_cpu_count"):
        return os.process_cpu_count()
    if hasattr(os, "sched_getaffinity"):
        try:
            return len(os.sched_getaffinity(0))
        except OSError:
            pass
    return None


def cgroup_directory(membership, mountinfo):
    """Map the unified membership to a visible cgroup2 mount in this namespace."""
    group = next((line[3:] for line in membership.splitlines() if line.startswith("0::")), "")
    path = PurePosixPath(group)
    if not path.is_absolute() or ".." in path.parts:
        return None
    for line in mountinfo.splitlines():
        left, _, right = line.partition(" - ")
        fields = left.split()
        if not right.startswith("cgroup2 ") or len(fields) < 5:
            continue
        root, mount = (re.sub(r"\\([0-7]{3})", lambda m: chr(int(m[1], 8)), s) for s in fields[3:5])
        try:
            relative = path.relative_to(PurePosixPath(root))
        except ValueError:
            continue
        return Path(mount) / relative, Path(mount)
    return None


def linux_job_limits():
    """Bounds from visible cgroup v2 ancestors; null means no finite bound observed."""
    def read(path):
        try:
            return path.read_text().strip()
        except (OSError, UnicodeError):
            return ""

    paths = cgroup_directory(read(Path("/proc/self/cgroup")), read(Path("/proc/self/mountinfo")))
    if paths is None:
        return {"status": "unavailable"}
    current, mount = paths
    if not current.is_dir():
        return {"status": "unavailable"}
    memory_caps, headrooms, quotas = [], [], []
    while True:
        cap = read(current / "memory.max")
        if cap.isdecimal():
            memory_caps.append(int(cap))
            used = read(current / "memory.current")
            if used.isdecimal():
                headrooms.append(max(0, int(cap) - int(used)))
        fields = read(current / "cpu.max").split()
        if len(fields) == 2 and all(x.isdecimal() for x in fields) and int(fields[1]) > 0:
            quotas.append(int(fields[0]) / int(fields[1]))
        if current == mount:
            break
        current = current.parent
    return {"status": "visible_hierarchy", "path": str(paths[0]),
            "memory_cap_bytes": min(memory_caps, default=None),
            "memory_headroom_bytes": min(headrooms, default=None),
            "cpu_quota_equivalents": min(quotas, default=None)}


def package_info(name):
    try:
        version = metadata.version(name)
    except metadata.PackageNotFoundError:
        return {"status": "metadata_not_found"}
    except (ValueError, OSError) as error:
        return {"status": "unknown", "reason": type(error).__name__}
    return {"status": "metadata_only", "version": version}


def is_local(path, roots):
    return any(path == root or root in path.parents for root in roots)


def external_path(roots):
    """Exclude relative entries, workspace paths and links back into the project."""
    directories = []
    for entry in os.get_exec_path():
        path = Path(entry.strip('"'))
        if not path.is_absolute() or is_local(path, roots):
            continue
        try:
            resolved = path.resolve(strict=True)
        except (OSError, RuntimeError):
            continue
        if resolved.is_dir() and not is_local(resolved, roots):
            directories.append(resolved)
    return directories


def command_info(name, directories, roots):
    # An explicit filename also prevents Windows from searching cwd or invoking a .cmd.
    filename = name + ".exe" if os.name == "nt" else name
    for directory in directories:
        try:
            executable = (directory / filename).resolve(strict=True)
            if is_local(executable, roots) or not executable.is_file():
                continue
            if os.access(executable, os.X_OK):
                break
        except (OSError, RuntimeError):
            continue
    else:
        return {"status": "not_found_on_external_path"}

    # Keep nested PATH lookups outside the project too. Pass no project Python hooks.
    env = {"PATH": os.pathsep.join(map(str, directories)), "LC_ALL": "C"}
    for key in ("SystemRoot", "WINDIR"):
        if key in os.environ:
            env[key] = os.environ[key]
    arguments = [str(executable), *FLAGS[name]]
    result = {"path": str(executable), "args": list(FLAGS[name])}
    try:
        proc = subprocess.run(
            arguments, cwd=executable.parent, env=env, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=6, check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return dict(result, status="query_failed", reason=type(error).__name__)
    output = proc.stdout.decode("utf-8", errors="replace").strip()
    result.update(returncode=proc.returncode, output=output[:700])
    if proc.returncode or not output:
        result["status"] = "query_failed"
    else:
        result["status"] = "driver_query_only" if name == "nvidia-smi" else "version_query_only"
    return result


def smoke(workload):
    # These operations run only in memory. Each check describes exactly what it tested.
    if workload == "data":
        rows = csv.DictReader(io.StringIO("value\n2\n4\n6\n"))
        value = statistics.mean(int(row["value"]) for row in rows)
        return {"operation": "stdlib CSV read and mean", "passed": value == 4}
    if workload == "simulation":
        events = [(2, 1), (1, 2)]
        heapq.heapify(events)
        trace = [heapq.heappop(events) for _ in range(len(events))]
        return {"operation": "stdlib discrete-event queue order", "passed": trace == [(1, 2), (2, 1)]}
    if workload == "ai":
        # One scalar least-squares update on (x=2,y=4), then inference on x=3.
        weight = 0.0
        gradient = (weight * 2 - 4) * 2
        weight -= 0.25 * gradient
        return {"operation": "Python CPU scalar linear regression update and inference",
                "passed": weight * 3 == 6}
    return {"operation": "HDL compile and simulate", "passed": None}


BACKENDS = {"numpy": "data", "torch-cpu": "ai", "torch-cuda": "ai", "iverilog": "hdl"}

NUMPY_CHECK = """
import json
import numpy as np
result = np.array([[2, 3]]) @ np.array([[4], [1]])
if result.item() != 11:
    raise ValueError("unexpected matrix product")
print(json.dumps({"framework": "numpy", "version": np.__version__, "module": np.__file__,
                  "product": result.item()}))
"""

TORCH_CHECK = """
import json, sys
import torch
device = sys.argv[1]
if device == "cuda" and torch.version.cuda is None:
    raise RuntimeError("PyTorch was built without NVIDIA CUDA support")
w = torch.tensor([2., 3.], device=device, requires_grad=True)
loss = w.square().sum()
loss.backward()
observed = w.grad.tolist()
if loss.device.type != device or loss.item() != 13 or observed != [4., 6.]:
    raise ValueError("unexpected device, reduction, or gradient")
print(json.dumps({"framework": "torch", "version": str(torch.__version__),
                  "module": torch.__file__, "device": str(loss.device), "gradient": observed}))
"""

IVERILOG_CHECK = """
module probe;
    reg clk = 0;
    reg value = 1;
    reg sampled;
    always @(posedge clk) sampled <= value;
    initial begin
        #1 clk = 1;
        #1 if (sampled !== 1'b1) $fatal(1, "first edge");
        clk = 0; value = 0;
        #1 clk = 1;
        #1 if (sampled !== 1'b0) $fatal(1, "second edge");
        $display("THESISFORGE_EDGES_OK");
        $finish;
    end
endmodule
"""


def checked_command(command, **kwargs):
    result = subprocess.run(command, stdin=subprocess.DEVNULL, capture_output=True,
                            timeout=60, check=False, **kwargs)
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).decode("utf-8", errors="replace")
        raise ValueError(f"{Path(command[0]).name} exited {result.returncode}: {detail[-800:].strip()}")
    return result.stdout.decode("utf-8", errors="replace")


def verify_backend(name, hdl_tools, directories):
    try:
        if name == "iverilog":
            compiler, simulator = (hdl_tools[tool].get("path") for tool in ("iverilog", "vvp"))
            if not compiler or not simulator:
                raise ValueError("iverilog and vvp are both required on the external PATH")
            env = os.environ.copy()
            env["PATH"] = os.pathsep.join(map(str, directories))
            with tempfile.TemporaryDirectory(prefix="thesisforge-rtl-") as directory:
                (Path(directory) / "probe.sv").write_text(IVERILOG_CHECK, encoding="ascii")
                checked_command([compiler, "-g2012", "-s", "probe", "-o", "probe.vvp", "probe.sv"],
                                cwd=directory, env=env)
                output = checked_command([simulator, "probe.vvp"], cwd=directory, env=env)
                if "THESISFORGE_EDGES_OK" not in output.splitlines():
                    raise ValueError("simulation ended without the self-check marker")
            evidence = {"compiler": compiler, "simulator": simulator, "checked_edges": 2}
        else:
            args = [NUMPY_CHECK] if name == "numpy" else [TORCH_CHECK, name.split("-")[1]]
            # Match the invoking interpreter's import policy. In particular, -I hides
            # user-site installs, which can be valid when the real experiment uses them.
            flags = [flag for enabled, flag in (
                (sys.flags.isolated, "-I"), (sys.flags.no_site, "-S"),
                (sys.flags.no_user_site, "-s"), (sys.flags.ignore_environment, "-E"),
                (getattr(sys.flags, "safe_path", False) and not sys.flags.isolated, "-P"),
            ) if enabled]
            # Changing cwd below must not rebase explicitly configured relative
            # PYTHONPATH entries (including an empty component denoting cwd).
            env = os.environ.copy()
            if env.get("PYTHONPATH") and not sys.flags.ignore_environment:
                entries = env["PYTHONPATH"].split(os.pathsep)
                env["PYTHONPATH"] = os.pathsep.join(os.path.abspath(path) for path in entries)
            output = checked_command([sys.executable, *flags, "-B", "-c", *args],
                                     cwd=Path(sys.executable).parent, env=env)
            evidence = json.loads(output.strip().splitlines()[-1]) if output.strip() else None
            if not isinstance(evidence, dict):
                raise ValueError("backend produced no result object")
        return {"passed": True, "result": evidence}
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        reason = "backend check exceeded 60 seconds" if isinstance(error, subprocess.TimeoutExpired) else str(error)
        return {"passed": False, "reason": reason}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workload", action="append", choices=["all", *PACKAGES],
                        help="repeat to select several workloads (default: selected backends, otherwise all)")
    parser.add_argument("--workspace", type=Path, default=Path.cwd(),
                        help="existing research directory for free space and local path exclusion")
    parser.add_argument("--verify", action="append", choices=BACKENDS, default=[],
                        help="run a small operation on this backend; repeat to require several")
    args = parser.parse_args()
    workspace = args.workspace.resolve()
    if not workspace.is_dir():
        parser.error("--workspace must be an existing directory")
    roots = (workspace, Path.cwd().resolve(), Path(__file__).resolve().parents[1])
    directories = external_path(roots)
    workloads = list(args.workload or [])
    if "all" in workloads or (not workloads and not args.verify):
        workloads = list(PACKAGES)
    workloads.extend(BACKENDS[item] for item in args.verify)
    try:
        disk_free = shutil.disk_usage(workspace).free
    except OSError:
        disk_free = None
    report = {
        "schema_version": 1,
        "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "system": {
            "os": platform.system(), "os_release": platform.release(),
            "architecture": platform.machine() or None, "logical_cpus": os.cpu_count(),
            "process_logical_cpus": cpu_count_for_process(),
            "host_physical_memory_bytes": memory_bytes(),
            "workspace": str(workspace), "workspace_free_bytes": disk_free,
            "python": {"executable": sys.executable, "version": platform.python_version(),
                       "build_platform": sysconfig.get_platform(),
                       "implementation": platform.python_implementation(),
                       "isolated": bool(sys.flags.isolated), "no_user_site": bool(sys.flags.no_user_site)},
        },
        "workloads": {},
    }
    for name in dict.fromkeys(workloads):
        report["workloads"][name] = {
            "smoke": smoke(name),
            "packages": {pkg: package_info(pkg) for pkg in PACKAGES[name]},
            "commands": {cmd: command_info(cmd, directories, roots) for cmd in COMMANDS[name]},
        }
    if sys.platform.startswith("linux"):
        report["system"]["linux_cgroup_v2"] = linux_job_limits()
    if args.verify:
        hdl_tools = report["workloads"].get("hdl", {}).get("commands", {})
        checks = {name: verify_backend(name, hdl_tools, directories) for name in dict.fromkeys(args.verify)}
        report["backend_checks"] = checks
    print(json.dumps(report, indent=2, allow_nan=False))
    return int(any(not item["passed"] for item in report.get("backend_checks", {}).values()))


if __name__ == "__main__":
    sys.exit(main())
