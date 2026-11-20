"""Track project evidence and file freshness; apply bounded edits to a new text file.

Standard library only. This checks recorded identities and links, not scientific
truth, experimental execution, citation support, or the completeness of a paper.
"""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile


STATES = {"supported", "qualified", "disputed", "unverified", "todo"}
KINDS = {"data", "code", "run", "analysis", "figure", "table", "manuscript", "report", "other"}


def now():
    return datetime.now(timezone.utc).isoformat()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"),
                      object_pairs_hook=unique_object,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def local_path(root, name):
    target = (root / name).resolve()
    if not target.is_relative_to(root):
        raise ValueError(f"Path leaves project root: {name}")
    return target


def fingerprint(path):
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            size += len(block)
            digest.update(block)
    return {"sha256": digest.hexdigest(), "bytes": size}


def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".ledger-", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


@contextmanager
def writer_lock(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    lock = path.with_name(path.name + ".lock")
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise ValueError(f"Ledger locked: {lock}; inspect the writer before removing a stale lock") from exc
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump({"pid": os.getpid(), "started_at": now()}, stream)
        yield
    finally:
        lock.unlink()


def entries(record, key):
    value = record.get(key)
    if not isinstance(value, list):
        raise ValueError(f"{key} must be an array")
    result = {}
    for row in value:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"].strip():
            raise ValueError(f"Every {key} entry needs a nonempty id")
        if row["id"] in result:
            raise ValueError(f"Duplicate {key} id: {row['id']}")
        result[row["id"]] = row
    return result


def load_record(path):
    value = read_json(path)
    if not isinstance(value, dict) or type(value.get("schema")) is not int or value["schema"] != 1:
        raise ValueError("Expected a schema 1 research ledger")
    for key in ("artifacts", "sources", "claims", "issues", "decisions", "checks"):
        entries(value, key)
    return value


def check_record(record, root):
    artifacts = entries(record, "artifacts")
    sources = entries(record, "sources")
    claims = entries(record, "claims")
    issues = entries(record, "issues")
    checks = entries(record, "checks")
    findings = []
    states = {}

    def flag(code, identity, detail):
        findings.append({"code": code, "id": identity, "detail": detail})

    visiting = set()

    def visit(identity):
        if identity in states:
            return states[identity]
        if identity not in artifacts:
            flag("missing_artifact", identity, "An artifact reference is not registered")
            return "missing"
        if identity in visiting:
            flag("dependency_cycle", identity, "Artifact dependencies must be acyclic")
            return "stale"
        visiting.add(identity)
        row = artifacts[identity]
        state = "current"
        try:
            if row.get("kind") not in KINDS:
                raise ValueError("Unknown artifact kind")
            if not isinstance(row.get("path"), str) or not row["path"]:
                raise ValueError("Missing artifact path")
            path = local_path(root, row["path"])
            actual = fingerprint(path)
            if row.get("sha256") != actual["sha256"] or row.get("bytes") != actual["bytes"]:
                state = "stale"
                flag("file_changed", identity, row["path"])
        except (OSError, ValueError) as exc:
            state = "missing"
            flag("file_unavailable", identity, str(exc))
        dependencies = row.get("inputs", {})
        if not isinstance(dependencies, dict):
            raise ValueError(f"{identity}.inputs must map artifact ids to SHA-256 values")
        for parent, expected in dependencies.items():
            parent_state = visit(parent)
            if parent_state != "current" or expected != artifacts.get(parent, {}).get("sha256"):
                state = "stale"
                flag("input_changed", identity, parent)
        visiting.remove(identity)
        states[identity] = state
        return state

    for identity in artifacts:
        visit(identity)

    for identity, row in sources.items():
        if row.get("read_scope") not in {"metadata", "abstract", "excerpt", "full", "unread"}:
            raise ValueError(f"{identity}: invalid source read_scope")
        if not row.get("locator") or not row.get("version"):
            flag("source_identity_incomplete", identity, "Record locator/URL and actual version/date")
        if row.get("artifact_id") is not None and visit(row["artifact_id"]) != "current":
            flag("source_file_stale", identity, str(row["artifact_id"]))

    claim_states = {}
    for identity, row in claims.items():
        if row.get("status") not in STATES or not isinstance(row.get("text"), str) or not row["text"].strip():
            raise ValueError(f"{identity}: a claim needs text and a valid status")
        evidence = row.get("evidence", [])
        if not isinstance(evidence, list):
            raise ValueError(f"{identity}.evidence must be an array")
        evidence_problems = set()

        def evidence_problem(state, code, detail):
            # Evidence order must not hide a stale item behind a later gap.
            evidence_problems.add(state)
            flag(code, identity, detail)

        def check_observed_hash(item, artifact_id):
            observed = item.get("observed_sha256")
            if (not isinstance(observed, str) or len(observed) != 64
                    or any(char not in "0123456789abcdefABCDEF" for char in observed)):
                evidence_problem("unverified", "claim_evidence_unfrozen",
                                 f"{artifact_id}: record observed_sha256 from the version actually reviewed")
            elif artifact_id in artifacts and observed.lower() != artifacts[artifact_id].get("sha256"):
                evidence_problem("stale", "claim_evidence_changed",
                                 f"{artifact_id}: registered file differs from observed_sha256")
            if visit(artifact_id) != "current":
                evidence_problem("stale", "claim_evidence_stale", artifact_id)

        if row["status"] in {"supported", "qualified"} and not evidence:
            evidence_problem("unverified", "unsupported_record",
                             "No registered evidence; support is not established by a status field")
        for item in evidence:
            if not isinstance(item, dict):
                raise ValueError(f"{identity}: evidence needs exactly one artifact_id or source_id")
            selectors = [key for key in ("artifact_id", "source_id") if key in item]
            if (len(selectors) != 1 or not isinstance(item[selectors[0]], str)
                    or not item[selectors[0]].strip()):
                raise ValueError(f"{identity}: evidence needs exactly one nonempty artifact_id or source_id")
            if not isinstance(item.get("locator"), str) or not item["locator"].strip():
                evidence_problem("unverified", "missing_evidence_location",
                                 "Provide actual section/page/row/figure or run location")
            if "artifact_id" in item:
                check_observed_hash(item, item["artifact_id"])
            else:
                source = sources.get(item["source_id"])
                if source is None:
                    evidence_problem("unverified", "missing_source", item["source_id"])
                    continue
                observed = item.get("observed_version")
                version = source.get("version")
                if not isinstance(observed, str) or not observed.strip():
                    evidence_problem("unverified", "claim_evidence_unfrozen",
                                     f"{item['source_id']}: record observed_version from the source actually reviewed")
                elif not isinstance(version, str) or not version.strip():
                    evidence_problem("unverified", "source_identity_incomplete", item["source_id"])
                elif observed != version:
                    evidence_problem("stale", "claim_evidence_changed",
                                     f"{item['source_id']}: source version differs from observed_version")
                if not isinstance(source.get("locator"), str) or not source["locator"].strip():
                    evidence_problem("unverified", "source_identity_incomplete", item["source_id"])
                observed_locator = item.get("observed_locator")
                if not isinstance(observed_locator, str) or not observed_locator.strip():
                    evidence_problem("unverified", "claim_evidence_unfrozen",
                                     f"{item['source_id']}: record observed_locator from the source actually reviewed")
                elif observed_locator != source.get("locator"):
                    evidence_problem("stale", "claim_evidence_changed",
                                     f"{item['source_id']}: source locator differs from observed_locator")
                if source.get("artifact_id") is not None:
                    check_observed_hash(item, source["artifact_id"])
                elif "observed_sha256" in item:
                    evidence_problem("unverified", "source_file_binding_missing",
                                     f"{item['source_id']}: captured file hash has no associated artifact to verify")
                if row["status"] in {"supported", "qualified"}:
                    # Read metadata may support bibliographic identity. An
                    # unread source cannot support even that narrower claim.
                    if (source.get("read_scope") == "unread" or
                            (source.get("read_scope") == "metadata" and row.get("kind") != "bibliographic")):
                        evidence_problem("unverified", "content_not_read", item["source_id"])
        if not row.get("locations"):
            flag("claim_usage_unmapped", identity, "Record manuscript/figure uses, or explain that this is a candidate")
        effective = ("stale" if "stale" in evidence_problems else
                     "unverified" if "unverified" in evidence_problems else row["status"])
        claim_states[identity] = {"declared": row["status"], "effective": effective}

    for identity, row in issues.items():
        if row.get("status") not in {"open", "resolved", "regressed", "deferred"}:
            raise ValueError(f"{identity}: invalid issue status")
        for claim in row.get("claim_ids", []):
            if claim not in claims:
                flag("issue_claim_missing", identity, claim)
        if row["status"] == "resolved" and not row.get("resolution"):
            flag("resolution_missing", identity, "Resolved issues need actual change/evidence locations")

    check_states = {}
    for identity, row in checks.items():
        if row.get("status") not in {"passed", "review", "failed", "not-run"}:
            raise ValueError(f"{identity}: invalid check status")
        inputs = row.get("inputs")
        if not isinstance(inputs, dict):
            raise ValueError(f"{identity}.inputs must be a map of captured file hashes")
        state = row["status"]
        if row["status"] != "not-run" and (not inputs or not row.get("method") or not row.get("checked_at")):
            flag("check_receipt_incomplete", identity, "Check needs method, timestamp and input identities")
            state = "review"
        for artifact, expected in inputs.items():
            if visit(artifact) != "current" or expected != artifacts.get(artifact, {}).get("sha256"):
                flag("check_stale", identity, artifact)
                state = "stale"
        check_states[identity] = state

    total = len(claims)
    return {
        "schema": 1, "checked_at": now(), "status": "review" if findings else ("empty" if not artifacts and not total else "consistent_within_coverage"),
        "artifacts": states, "claims": claim_states, "checks": check_states, "findings": findings,
        "coverage": {"registered_claims": total,
                     "declared_supported_or_qualified": sum(x["status"] in {"supported", "qualified"} for x in claims.values()),
                     "semantically_verified_by_this_tool": 0,
                     "unregistered_manuscript_claims": "not enumerated"},
        "limits": ["Hashes and references only; semantic support and research validity require review",
                   "No experiments, literature searches, layout reviews or statistical tests were run",
                   "Source read_scope and check receipts are recorded declarations, not independently certified actions"],
    }


def apply_patch_plan(root, filename, expected, plan, output):
    source = local_path(root, filename)
    destination = local_path(root, output)
    if source == destination or destination.exists():
        raise ValueError("Patch output must be a new file, distinct from the original")
    raw = source.read_bytes()
    before = hashlib.sha256(raw).hexdigest()
    if before != expected:
        raise ValueError("Source changed since the patch was prepared")
    text = raw.decode("utf-8")
    if not isinstance(plan, dict) or set(plan) != {"replacements"} or not isinstance(plan["replacements"], list) or not plan["replacements"]:
        raise ValueError("Patch requires a nonempty replacements array")
    spans = []
    for change in plan["replacements"]:
        if not isinstance(change, dict) or set(change) != {"old", "new"}:
            raise ValueError("Each replacement has only old and new fields")
        old, new = change["old"], change["new"]
        if not isinstance(old, str) or not old or not isinstance(new, str):
            raise ValueError("Each nonempty old fragment must match exactly once in the original")
        start = text.find(old)
        if start < 0 or text.find(old, start + 1) >= 0:
            raise ValueError("Each nonempty old fragment must match exactly once in the original")
        spans.append((start, start + len(old), new))
    spans.sort()
    if any(a[1] > b[0] for a, b in zip(spans, spans[1:])):
        raise ValueError("Patch fragments overlap")
    cursor, chunks = 0, []
    for start, end, new in spans:
        chunks.extend((text[cursor:start], new))
        cursor = end
    chunks.append(text[cursor:])
    updated = "".join(chunks).encode("utf-8")
    if fingerprint(source)["sha256"] != before:
        raise ValueError("Source changed during patch preparation")
    destination.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation never overwrites another writer's output. On failure
    # remove only the new file opened by this process.
    fd = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(updated)
            stream.flush()
            os.fsync(stream.fileno())
    except BaseException:
        destination.unlink(missing_ok=True)
        raise
    return {"source": str(source), "output": str(destination), "before_sha256": before,
            "after_sha256": hashlib.sha256(updated).hexdigest(), "replacements": len(spans),
            "semantic_fidelity": "not_checked", "original_unchanged": True}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True, help="Research project root, not the installed skill directory")
    parser.add_argument("--ledger", default=".thesisforge/research.json", help="Path inside --root")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init", help="Create an empty ledger; never replace an existing record")
    add = sub.add_parser("record-file", help="Capture a real file; dependent outputs/checks keep their old input hashes")
    add.add_argument("--id", required=True)
    add.add_argument("--path", required=True)
    add.add_argument("--kind", required=True, choices=sorted(KINDS))
    add.add_argument("--input", action="append", help="Registered input artifact ID; repeatable. Omission preserves existing input hashes")
    check = sub.add_parser("check", help="Read-only freshness and link checks, with explicit coverage")
    check.add_argument("--strict", action="store_true", help="Exit 1 for unresolved structural/freshness findings or empty ledger")
    patch = sub.add_parser("apply-patch", help="Apply exact nonoverlapping replacements to a NEW UTF-8 file")
    patch.add_argument("--file", required=True)
    patch.add_argument("--expected-sha256", required=True)
    patch.add_argument("--plan", type=Path, required=True)
    patch.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if not root.is_dir():
        parser.error("--root must be an existing directory")
    try:
        ledger = local_path(root, args.ledger)
        if args.command == "apply-patch":
            result = apply_patch_plan(root, args.file, args.expected_sha256, read_json(local_path(root, args.plan)), args.output)
        elif args.command == "check":
            result = check_record(load_record(ledger), root)
        else:
            with writer_lock(ledger):
                if args.command == "init":
                    if ledger.exists():
                        raise ValueError("Ledger already exists")
                    record = {"schema": 1, "created_at": now(), "scope": "Record actual project coverage here"}
                    record.update({key: [] for key in ("artifacts", "sources", "claims", "issues", "decisions", "checks")})
                else:
                    record = load_record(ledger)
                    if not args.id.strip():
                        raise ValueError("Artifact id cannot be blank")
                    artifacts = entries(record, "artifacts")
                    before = check_record(record, root)
                    inputs = dict(artifacts.get(args.id, {}).get("inputs", {})) if args.input is None else {}
                    for identity in args.input or []:
                        if identity == args.id or identity not in artifacts or before["artifacts"].get(identity) != "current":
                            raise ValueError(f"Input is missing, stale, or self-referential: {identity}")
                        inputs[identity] = artifacts[identity]["sha256"]
                    path = local_path(root, args.path)
                    if path == ledger or path == ledger.with_name(ledger.name + ".lock"):
                        raise ValueError("The ledger and its lock cannot be artifacts in their own record")
                    row = {"id": args.id, "kind": args.kind, "path": path.relative_to(root).as_posix(),
                           **fingerprint(path), "recorded_at": now(), "inputs": inputs}
                    record["artifacts"] = [r for r in record["artifacts"] if r["id"] != args.id] + [row]
                    after = check_record(record, root)
                    if any(f["code"] == "dependency_cycle" for f in after["findings"]):
                        raise ValueError("New dependency would introduce a cycle")
                atomic_json(ledger, record)
                result = {"ledger": str(ledger), "action": args.command,
                          "notice": "Recorded identities only; existing downstream checks are not refreshed"}
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        if args.command == "check" and args.strict and result["status"] != "consistent_within_coverage":
            return 1
        return 0
    except (OSError, ValueError, TypeError, KeyError, RecursionError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="strict")
    raise SystemExit(main())
