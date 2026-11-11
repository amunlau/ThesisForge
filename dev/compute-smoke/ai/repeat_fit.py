"""Fit full and reduced classifiers on paired synthetic splits, then evaluate from disk."""

import argparse
import csv
import hashlib
from pathlib import Path
import subprocess
import sys

import numpy as np

from train_and_reload import metrics, synthetic_split


METHODS = {"full": 3, "two_features": 2}


def fit(x, y, valid_x, valid_y):
    weights = np.zeros(x.shape[1])
    bias = 0.0
    candidates = []
    for epoch in range(1, 101):
        logits = x @ weights + bias
        error = 1 / (1 + np.exp(-logits)) - y
        weights -= 0.24 * (x.T @ error / len(y))
        bias -= 0.24 * error.mean()
        if epoch in (5, 25, 100):
            loss = metrics(valid_x @ weights + bias, valid_y)["mean_log_loss"]
            candidates.append((loss, epoch, weights.copy(), bias))
    return min(candidates, key=lambda candidate: candidate[:2])


def train(seed, directory):
    train_seed, validation_seed, _ = np.random.SeedSequence(seed).spawn(3)
    x, y = synthetic_split(256, train_seed)
    valid_x, valid_y = synthetic_split(96, validation_seed)
    for method, width in METHODS.items():
        loss, epoch, weights, bias = fit(x[:, :width], y, valid_x[:, :width], valid_y)
        reference = valid_x[:, :width] @ weights + bias
        with (directory / f"{method}.npz").open("xb") as stream:
            np.savez(stream, weights=weights, bias=bias, reference=reference,
                     seed=seed, epoch=epoch, validation_loss=loss)


def evaluate(seed, directory):
    _, validation_seed, test_seed = np.random.SeedSequence(seed).spawn(3)
    valid_x, _ = synthetic_split(96, validation_seed)
    x, y = synthetic_split(128, test_seed)
    digest = hashlib.sha256(x.tobytes() + y.tobytes()).hexdigest()
    with (directory / "predictions.csv").open("x", newline="", encoding="utf-8") as predictions, \
            (directory / "metrics.csv").open("x", newline="", encoding="utf-8") as summary:
        scores = csv.writer(predictions, lineterminator="\n")
        rows = csv.writer(summary, lineterminator="\n")
        scores.writerow(["seed", "method", "row", "label", "logit"])
        rows.writerow(["seed", "method", "test_sha256", "epoch", "rows", "correct", "mean_log_loss"])
        for method, width in METHODS.items():
            with np.load(directory / f"{method}.npz", allow_pickle=False) as ckpt:
                weights, bias = ckpt["weights"], ckpt["bias"].item()
                if ckpt["seed"].item() != seed or weights.shape != (width,):
                    raise ValueError("checkpoint identity mismatch")
                np.testing.assert_allclose(valid_x[:, :width] @ weights + bias,
                                           ckpt["reference"], rtol=1e-12, atol=1e-12)
                logits = x[:, :width] @ weights + bias
                measured = metrics(logits, y)
                if not np.isfinite(logits).all():
                    raise ValueError("nonfinite prediction")
                rows.writerow([seed, method, digest, ckpt["epoch"].item(), len(y),
                               measured["correct"], measured["mean_log_loss"]])
                scores.writerows((seed, method, i, int(label), float(logit))
                                 for i, (label, logit) in enumerate(zip(y, logits)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--out", type=Path, required=True, help="existing attempt directory")
    parser.add_argument("--evaluate", action="store_true", help="evaluate saved checkpoints only")
    args = parser.parse_args()
    if args.evaluate:
        evaluate(args.seed, args.out)
    else:
        train(args.seed, args.out)
        subprocess.run([sys.executable, "-B", str(Path(__file__).resolve()), "--evaluate",
                        "--seed", str(args.seed), "--out", str(args.out)], check=True)
