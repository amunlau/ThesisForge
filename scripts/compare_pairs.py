"""Compare two methods on the same predeclared experimental units using CSV inputs."""

import argparse
import csv
from decimal import Decimal, InvalidOperation
from fractions import Fraction
import hashlib
import io
import json
import math
from pathlib import Path
import statistics


class DigestReader(io.RawIOBase):
    """Hash the exact bytes decoded by the CSV reader, including the BOM and newlines."""

    def __init__(self, source):
        super().__init__()
        self.source = source
        self.digest = hashlib.sha256()
        self.byte_count = 0

    def readable(self):
        return True

    def readinto(self, buffer):
        size = self.source.readinto(buffer)
        self.digest.update(memoryview(buffer)[:size])
        self.byte_count += size
        return size


def records(path, required, expected=None):
    with path.open("rb") as source:
        raw = source if expected is None else DigestReader(source)
        with io.TextIOWrapper(raw, encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream, strict=True)
            fields = reader.fieldnames or []
            if len(fields) != len(set(fields)) or not required.issubset(fields):
                raise ValueError(f"{path}: expected unique headers including {sorted(required)}")
            for row in reader:
                if None in row or None in row.values():
                    raise ValueError(f"{path}:{reader.line_num}: unequal number of fields")
                yield f"{path}:{reader.line_num}", row
        if expected is not None and (expected["bytes"] != raw.byte_count
                                     or expected["sha256"] != raw.digest.hexdigest()):
            raise ValueError(f"file content changed since execution: {path}")


def identifier(row, fields):
    values = tuple(row[field] for field in fields)
    if any(not value.strip() for value in values):
        raise ValueError(f"empty identifier in {dict(zip(fields, values))}")
    return values


def measurement(text):
    # Keep decimal CSV values exact through per-unit division and subtraction.
    value = Decimal(text)
    approximate = float(value)
    if not math.isfinite(approximate) or (approximate == 0 and value):
        raise ValueError("measurement outside the finite output range")
    return Fraction(value) if value else Fraction(0)


def json_number(value):
    if value.denominator == 1:
        return value.numerator
    rounded = float(value)
    if value and rounded == 0:
        raise ValueError("nonzero result below the numeric output range")
    return rounded


def matrix_files(index_file, artifact):
    root = index_file.resolve().parent
    index = json.loads(index_file.read_text(encoding="utf-8-sig"))
    if (not isinstance(index, dict) or index.get("status") != "succeeded"
            or not isinstance(index.get("cases"), dict) or not index["cases"]):
        raise ValueError("matrix incomplete: reconcile failed or pending runs before paired comparison")
    files = []
    for name, cell in index["cases"].items():
        record_file = (root / cell["record"]).resolve()
        case_dir = root / ("case-" + name)
        if (cell["status"] != "succeeded" or case_dir.parent != root
                or record_file.parent.parent != case_dir or not record_file.parent.name.isdecimal()
                or record_file.name != "run.json"):
            raise ValueError(f"{name}: invalid case or record location")
        record = json.loads(record_file.read_text(encoding="utf-8"))
        if not isinstance(record, dict):
            raise ValueError(f"{name}: invalid run record")
        # Older records omit this check; their index may explicitly say null.
        index_check = cell.get("inputs_verified_after_run")
        record_check = record.get("inputs_verified_after_run", True)
        if record_check is not True or (index_check is not None and index_check is not True):
            raise ValueError(f"{name}: inconsistent or unsuccessful post-run input verification")
        path = (record_file.parent / artifact).resolve()
        expected = {Path(item["path"]): item for item in record["outputs"]}
        if (record["status"] != "succeeded" or record["exit_code"] != 0
                or Path(record["run_dir"]) != record_file.parent
                or record_file.parent not in path.parents or path not in expected):
            raise ValueError(f"{name}: {artifact} is not a declared output of a successful run")
        files.append((path, expected[path]))
    return files


def sample_sd(differences):
    if len(differences) == 1:
        return None
    low = min(differences)
    span = max(differences) - low
    if not span:
        return 0.0
    # Scale the exact differences before taking the square root, so tiny but
    # representable variation survives even on Python versions that square floats.
    scaled_sd = statistics.stdev((value - low) / span for value in differences)
    return float(json_number(span * Fraction(scaled_sd)))


def compare(args):
    keys = args.group + args.unit
    roles = keys + [args.method, args.value] + args.match
    if args.denominator:
        roles.append(args.denominator)
    if len(set(roles)) != len(roles) or args.candidate == args.baseline:
        raise ValueError("use distinct column names for each role and two different methods")
    cells = {}
    planned_matches = {}
    for source, row in records(args.plan, set(keys)):
        key = identifier(row, keys)
        if key in cells:
            raise ValueError(f"{source}: duplicate planned unit {key}")
        cells[key] = {}
        fields = [field for field in args.match if field in row]
        planned_matches[key] = dict(zip(fields, identifier(row, fields)))
    if not cells:
        raise ValueError("the plan contains no units")

    arms = (args.candidate, args.baseline)
    datasets = (matrix_files(args.matrix, args.artifact) if args.matrix
                else [(path, None) for path in args.data])
    required = set(roles)
    observations = (record for path, expected in datasets for record in records(path, required, expected))
    for source, row in observations:
        method = row[args.method]
        if method not in arms:
            continue
        key = identifier(row, keys)
        if key not in cells or method in cells[key]:
            raise ValueError(f"{source}: unplanned or duplicate observation {key}, {method}")
        try:
            value = measurement(row[args.value])
            denominator = measurement(row[args.denominator]) if args.denominator else 1
        except (InvalidOperation, ValueError) as error:
            raise ValueError(f"{source}: invalid metric or denominator for {key}, {method}") from error
        if args.denominator:
            if denominator <= 0:
                raise ValueError(f"{source}: expected a finite positive denominator")
            value /= denominator
        if not math.isfinite(value):
            raise ValueError(f"{source}: nonfinite measurement")
        for field, expected in planned_matches[key].items():
            if row[field] != expected:
                raise ValueError(f"{source}: {key} {method} differs from plan on {field}: "
                                 f"expected {expected!r}, got {row[field]!r}")
        cells[key][method] = (value, identifier(row, args.match))

    grouped = {}
    for key, cell in cells.items():
        missing = [method for method in arms if method not in cell]
        if missing:
            raise ValueError(f"planned unit {key} missing {', '.join(missing)}")
        candidate, baseline = (cell[method] for method in arms)
        if candidate[1] != baseline[1]:
            raise ValueError(f"pair {key} differs on {args.match}: {candidate[1]} vs {baseline[1]}")
        delta = candidate[0] - baseline[0]
        if not math.isfinite(delta):
            raise ValueError(f"paired difference exceeds numeric range for {key}")
        group = key[:len(args.group)]
        grouped.setdefault(group, []).append({
            "unit": dict(zip(args.unit, key[len(args.group):])),
            "candidate": candidate[0], "baseline": baseline[0], "difference": delta,
        })

    summaries = []
    for group, pairs in grouped.items():
        differences = [p["difference"] for p in pairs]
        summaries.append({
            "group": dict(zip(args.group, group)), "n_pairs": len(pairs),
            "candidate_mean": json_number(statistics.mean(p["candidate"] for p in pairs)),
            "baseline_mean": json_number(statistics.mean(p["baseline"] for p in pairs)),
            "mean_difference": json_number(statistics.mean(differences)),
            "sd_difference": sample_sd(differences),
            "min_difference": json_number(min(differences)),
            "max_difference": json_number(max(differences)),
            "pairs": [{"unit": p["unit"], "candidate": json_number(p["candidate"]),
                       "baseline": json_number(p["baseline"]), "difference": json_number(p["difference"])}
                      for p in pairs],
        })
    return {"candidate": arms[0], "baseline": arms[1], "value_column": args.value,
            "denominator_column": args.denominator, "matched_columns": args.match,
            "difference": "candidate minus baseline, equal weight per planned unit", "groups": summaries}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True, type=Path, help="one row per planned group/unit")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--data", nargs="+", type=Path,
                        help="one or more CSVs, one measured row per group/unit/method")
    source.add_argument("--matrix", type=Path, help="index.json created by run_matrix.py")
    parser.add_argument("--artifact", help="declared per-attempt CSV to read with --matrix")
    parser.add_argument("--group", nargs="+", default=[], help="report each condition separately")
    parser.add_argument("--unit", nargs="+", required=True, help="columns identifying a repetition within a group")
    parser.add_argument("--method", default="method", help="column containing the method names")
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--value", required=True, help="numeric response or its numerator")
    parser.add_argument("--denominator", help="divide each row by its own positive denominator first")
    parser.add_argument("--match", nargs="+", default=[],
                        help="columns that must match within pairs and the plan when specified there")
    args = parser.parse_args()
    if bool(args.matrix) != bool(args.artifact):
        parser.error("supply --matrix and --artifact together")
    try:
        result = compare(args)
        print(json.dumps(result, ensure_ascii=True, allow_nan=False, indent=2))
    except (OSError, ValueError, csv.Error, OverflowError, KeyError, TypeError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
