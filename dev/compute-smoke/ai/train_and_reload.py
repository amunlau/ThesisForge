"""CPU training and checkpoint smoke test. Run with NumPy, redirect JSON stdout if desired."""

import hashlib
import json
import platform
import tempfile
from pathlib import Path

import numpy as np


def synthetic_split(rows, seed):
    rng = np.random.default_rng(seed)
    features = rng.normal(size=(rows, 3))
    noise = rng.normal(scale=0.45, size=rows)
    labels = (features @ [1.0, 0.6, -0.7] - 0.25 + noise > 0).astype(np.int64)
    return features, labels


def metrics(logits, labels):
    correct = int(np.count_nonzero((logits >= 0) == labels))
    return {
        "rows": len(labels),
        "correct": correct,
        "accuracy": correct / len(labels),
        "mean_log_loss": float(np.mean(np.logaddexp(0, logits) - labels * logits)),
    }


def main():
    x_train, y_train = synthetic_split(256, 8901)
    x_valid, y_valid = synthetic_split(96, 521)
    # Fit only on the training rows. Select epoch by lowest validation loss.
    epochs = (5, 25, 100)
    learning_rate = 0.24
    weights = np.zeros(x_train.shape[1])
    bias = 0.0
    candidates = []
    for epoch in range(1, max(epochs) + 1):
        logits = x_train @ weights + bias
        error = 1 / (1 + np.exp(-logits)) - y_train
        weights -= learning_rate * (x_train.T @ error / len(y_train))
        bias -= learning_rate * float(np.mean(error))
        if epoch in epochs:
            valid = metrics(x_valid @ weights + bias, y_valid)
            candidates.append((valid["mean_log_loss"], epoch, weights.copy(), bias))
    _, selected_epoch, fitted_weights, fitted_bias = min(candidates, key=lambda item: item[:2])
    train_prevalence = float(np.mean(y_train))
    baseline_logit = np.log(train_prevalence / (1 - train_prevalence))

    # Freeze both predictors before generating any test rows. Read the NPZ back from disk.
    with tempfile.TemporaryFile(mode="w+b") as checkpoint:
        np.savez(checkpoint, weights=fitted_weights, bias=fitted_bias)
        checkpoint.seek(0)
        with np.load(checkpoint, allow_pickle=False) as restored:
            loaded_weights = restored["weights"]
            loaded_bias = restored["bias"].item()
    x_test, y_test = synthetic_split(128, 3671)
    original = x_test @ fitted_weights + fitted_bias
    reloaded = x_test @ loaded_weights + loaded_bias
    baseline = metrics(np.full(len(y_test), baseline_logit), y_test)
    model = metrics(reloaded, y_test)
    identical = bool(np.array_equal(original, reloaded))
    if not identical or model["mean_log_loss"] >= baseline["mean_log_loss"]:
        raise RuntimeError("checkpoint round-trip or synthetic learning check failed")

    print(json.dumps({
        "task": "CPU binary logistic regression smoke test",
        "python": platform.python_version(),
        "numpy": np.__version__,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "data": "Synthetic, generated locally. Three independent standard normal predictors; "
                "positive if x0 + 0.6*x1 - 0.7*x2 - 0.25 + N(0, 0.45^2) > 0.",
        "splits": {
            "train": {"rows": len(y_train), "seed": 8901, "positive": int(y_train.sum())},
            "validation": {"rows": len(y_valid), "seed": 521, "positive": int(y_valid.sum())},
            "test": {"rows": len(y_test), "seed": 3671, "positive": int(y_test.sum())},
        },
        "training": {
            "optimizer": "full-batch gradient descent, zero initialization",
            "learning_rate": learning_rate,
            "selection": "minimum validation mean log loss, earliest epoch on tie",
            "validation_mean_log_loss": {str(epoch): loss for loss, epoch, _, _ in candidates},
            "selected_epoch": selected_epoch,
        },
        "checkpoint": {
            "format_tested": "NPZ, float64, disk-backed temporary file",
            "weights": loaded_weights.tolist(), "bias": loaded_bias,
            "all_test_logits_exactly_equal_after_reload": identical,
        },
        "held_out_test": {
            "baseline": {"predictor": "constant training positive prevalence",
                         "probability": train_prevalence, **baseline},
            "model": {"predictor": "reloaded logistic regression", **model},
        },
    }, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
