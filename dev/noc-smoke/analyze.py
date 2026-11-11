"""Verify the long-form records and summarize within-trace paired differences."""
import argparse
import csv
from pathlib import Path
from statistics import mean, stdev

from experiment import BUDGET, HEURISTIC, PATTERNS, SPACE, TEST, weights_text
from mesh import BURSTS, BURST_SIZE, NODES, trace_hash, traffic


def read_rows(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def summarize(directory):
    trials = read_rows(directory / "search.csv")
    assert len(trials) == BUDGET * 2
    policies = {"fifo": "fifo", "heuristic": weights_text(HEURISTIC)}
    allowed_weights = {weights_text(w) for w in SPACE}
    for method in ("random", "evolution"):
        group = [r for r in trials if r["search"] == method]
        assert len(group) == len({r["weights"] for r in group}) == BUDGET
        assert [int(r["trial"]) for r in group] == list(range(1, BUDGET + 1))
        for row in group:
            if row["weights"] not in allowed_weights or int(row["train_latency_sum"]) <= 0:
                raise ValueError(f"{method} trial {row['trial']}: invalid weights or training latency")
            if row["selected"] not in ("0", "1"):
                raise ValueError(f"{method} trial {row['trial']}: invalid selection flag")
        selected, = [r for r in group if r["selected"] == "1"]
        assert selected == min(group, key=lambda r: (int(r["train_latency_sum"]),
                                                     tuple(map(int, r["weights"].split()))))
        policies[method] = selected["weights"]

    paired = {}
    for r in read_rows(directory / "paired.csv"):
        pattern, seed, method = r["pattern"], int(r["seed"]), r["method"]
        assert seed in TEST[pattern] and r["weights"] == policies[method]
        assert int(r["offered"]) == int(r["delivered"]) == NODES * BURSTS * BURST_SIZE
        assert 0 < int(r["p95"]) <= int(r["last_arrival"])
        key = (pattern, seed)
        cell = paired.setdefault(key, {})
        assert method not in cell
        cell[method] = r
    for pattern in PATTERNS:
        for seed in TEST[pattern]:
            cell = paired[pattern, seed]
            assert set(cell) == set(policies)
            trace = traffic(pattern, seed)
            assert {r["trace_sha256"] for r in cell.values()} == {trace_hash(trace)}
            hop_sum = sum(len(packet.path) for packet in trace)
            release_sum = sum(packet.release for packet in trace)
            n = len(trace)
            rank = (95 * n + 99) // 100  # nearest-rank p95
            for row in cell.values():
                p95, last = int(row["p95"]), int(row["last_arrival"])
                # Every delay is at least one hop and at most last minus release.
                # At least n-rank+1 delays are >= p95 and at least rank are <= p95.
                minimum = max(hop_sum, rank - 1 + (n - rank + 1) * p95)
                maximum = min(n * last - release_sum, rank * p95 + (n - rank) * last)
                if not minimum <= int(row["latency_sum"]) <= maximum:
                    raise ValueError(f"{pattern} seed {seed}, {row['method']}: inconsistent latency_sum")

    # n counts independently generated traces within one pattern. Lower latency wins.
    lines = ["pattern,method,comparator,n,mean_cycles,comparator_mean_cycles,"
             "paired_delta,paired_sd,delta_min,delta_max,wins,ties,losses"]
    for pattern in PATTERNS:
        for method, baseline in (("heuristic", "fifo"), ("random", "fifo"),
                                 ("evolution", "fifo"), ("evolution", "heuristic"),
                                 ("evolution", "random")):
            averages = []
            baselines = []
            for seed in TEST[pattern]:
                cell = paired[pattern, seed]
                count = int(cell[method]["offered"])
                averages.append(int(cell[method]["latency_sum"]) / count)
                baselines.append(int(cell[baseline]["latency_sum"]) / count)
            deltas = [a - b for a, b in zip(averages, baselines)]
            values = [mean(averages), mean(baselines), mean(deltas), stdev(deltas), min(deltas), max(deltas)]
            wins, ties = sum(d < 0 for d in deltas), deltas.count(0)
            lines.append(",".join([pattern, method, baseline, str(len(deltas)),
                                   *(f"{v:.6f}" for v in values), str(wins),
                                   str(ties), str(len(deltas) - wins - ties)]))
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, nargs="?", default=Path(__file__).parent / "results")
    parser.add_argument("--write", action="store_true", help="write summary.csv alongside the inputs")
    args = parser.parse_args()
    summary = summarize(args.directory)
    if args.write:
        with (args.directory / "summary.csv").open("x", encoding="utf-8", newline="") as stream:
            stream.write(summary)
    print(summary, end="")
