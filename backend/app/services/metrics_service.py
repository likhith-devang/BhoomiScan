from __future__ import annotations

from typing import Iterable


def binary_scores(y_true: Iterable[bool], y_pred: Iterable[bool]) -> dict:
    """Precision / recall / F1 for rule-engine gold labels (not a trained ML model)."""
    truths = list(y_true)
    preds = list(y_pred)
    if len(truths) != len(preds) or not truths:
        return {
            "support": 0,
            "precision": 0.0,
            "recall": 0.0,
            "f1": 0.0,
            "accuracy": 0.0,
            "true_positive": 0,
            "false_positive": 0,
            "false_negative": 0,
            "true_negative": 0,
        }
    tp = sum(1 for t, p in zip(truths, preds) if t and p)
    fp = sum(1 for t, p in zip(truths, preds) if (not t) and p)
    fn = sum(1 for t, p in zip(truths, preds) if t and (not p))
    tn = sum(1 for t, p in zip(truths, preds) if (not t) and (not p))
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    accuracy = (tp + tn) / len(truths)
    return {
        "support": len(truths),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "accuracy": round(accuracy, 4),
        "true_positive": tp,
        "false_positive": fp,
        "false_negative": fn,
        "true_negative": tn,
        "note": (
            "These are statistical scores for deterministic risk rules on labelled fixtures, "
            "not training metrics for a neural network."
        ),
    }
