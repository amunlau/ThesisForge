"""Select policies on training traces, freeze them and replay on held-out traces."""
import argparse
import csv
import io
import itertools
import random
from pathlib import Path

from mesh import traffic, trace_hash, simulate, metrics


PATTERNS = ("uniform", "hotspot")
TRAIN = {"uniform": range(100, 104), "hotspot": range(200, 204)}
TEST = {"uniform": range(1000, 1012), "hotspot": range(2000, 2012)}
SPACE = tuple(itertools.product(range(1, 5), range(-3, 4), range(-3, 4)))
POP = 6
BUDGET = 24
HEURISTIC = (1, 0, -1)


def weights_text(weights):
    return " ".join(map(str, weights)) if weights is not None else "fifo"


def search(method, train):
    rng = random.Random(314159)
    initial = rng.sample(SPACE, POP)
    seen = set()
    records = []
    parents = []
    for trial in range(BUDGET):
        if trial < POP:
            candidate = initial[trial]
        elif method == "random":
            candidate = rng.choice([w for w in SPACE if w not in seen])
        else:
            # Elitist (6+6) search; mutate one coordinate of a surviving parent.
            if trial % POP == 0:
                parents = [r[1] for r in sorted(records)[:POP]]
            neighbors = [w for w in SPACE if w not in seen and
                         any(sum(a != b for a, b in zip(w, p)) == 1 for p in parents)]
            candidate = rng.choice(neighbors)
        assert candidate not in seen
        seen.add(candidate)
        total_latency = sum(sum(t - p.release for t, p in zip(simulate(trace, candidate), trace))
                            for trace in train)
        records.append((total_latency, candidate, trial + 1))
    best = min(records)[1]  # ties broken lexicographically by weights
    history = [{"search": method, "trial": trial, "weights": weights_text(w),
                "train_latency_sum": score, "selected": int(w == best)}
               for score, w, trial in records]
    return best, history


def csv_bytes(rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def run():
    train = [traffic(pattern, seed) for pattern in PATTERNS for seed in TRAIN[pattern]]
    train_hashes = {trace_hash(trace) for trace in train}
    assert len(train_hashes) == len(train)
    assert not {s for seeds in TRAIN.values() for s in seeds} & {s for seeds in TEST.values() for s in seeds}
    policies = {"fifo": None, "heuristic": HEURISTIC}
    history = []
    for method in ("random", "evolution"):
        policies[method], trials = search(method, train)
        history.extend(trials)
    results = []
    test_hashes = set()
    for pattern in PATTERNS:
        for seed in TEST[pattern]:
            trace = traffic(pattern, seed)
            digest = trace_hash(trace)
            assert digest not in train_hashes and digest not in test_hashes
            test_hashes.add(digest)
            for name, weights in policies.items():
                results.append({
                    "pattern": pattern, "seed": seed, "trace_sha256": digest,
                    "method": name, "weights": weights_text(weights), "offered": len(trace),
                    **metrics(trace, simulate(trace, weights)),
                })
    return {"search.csv": history, "paired.csv": results}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True, help="new directory for this execution")
    directory = parser.parse_args().out
    directory.mkdir(parents=True, exist_ok=False)
    for name, rows in run().items():
        (directory / name).write_bytes(csv_bytes(rows))
