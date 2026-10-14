#!/usr/bin/env python3
"""
Task 3: Multiset Fractional Retrieval Metric (MFRM) Implementation
Calculates Multiset Jaccard Similarity, Precision, Recall, and F1-Score
for Text-to-SQL predictions generated across different prompting frameworks.
"""

import csv
import json
import math
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path

# Resolve paths relative to this script
CURRENT_DIR = Path(__file__).resolve().parent
TASK2_DATA_DIR = (CURRENT_DIR.parent / "Task_2" / "data").resolve()

# Import load_database from Task 2's evaluation script
sys.path.insert(0, str(TASK2_DATA_DIR))
try:
    import evaluate_retrieval_predictions as eval_script
except ImportError as err:
    raise ImportError(f"Could not import evaluate_retrieval_predictions from {TASK2_DATA_DIR}: {err}")

LABELS_PATH = TASK2_DATA_DIR / "restaurants_dataset.csv"

PREDICTION_FILES = [
    ("CO-STAR", TASK2_DATA_DIR / "restaurants_dataset_predictions_costar.csv"),
    ("ICIO", TASK2_DATA_DIR / "restaurants_dataset_predictions_icio.csv"),
    ("Few-Shot", TASK2_DATA_DIR / "restaurants_dataset_predictions_fewshot.csv"),
]


def multiset_intersection_size(p_counter: Counter, e_counter: Counter) -> int:
    """Calculate the size of the multiset intersection: sum_x min(count_P(x), count_E(x))."""
    all_elements = set(p_counter.keys()) | set(e_counter.keys())
    return sum(min(p_counter[elem], e_counter[elem]) for elem in all_elements)


def multiset_union_size(p_counter: Counter, e_counter: Counter) -> int:
    """Calculate the size of the multiset union: sum_x max(count_P(x), count_E(x))."""
    all_elements = set(p_counter.keys()) | set(e_counter.keys())
    return sum(max(p_counter[elem], e_counter[elem]) for elem in all_elements)


def compute_multiset_metrics(predicted_rows, expected_rows):
    """
    Computes fine-grained fractional multiset retrieval metrics between
    predicted SQL result rows and expected ground truth rows.
    """
    p_counter = Counter(tuple(r) for r in predicted_rows)
    e_counter = Counter(tuple(r) for r in expected_rows)

    # Empty set edge cases
    if not predicted_rows and not expected_rows:
        return {
            "binary_exact": 1.0,
            "jaccard": 1.0,
            "precision": 1.0,
            "recall": 1.0,
            "f1": 1.0,
        }
    if not predicted_rows or not expected_rows:
        return {
            "binary_exact": 0.0,
            "jaccard": 0.0,
            "precision": 0.0,
            "recall": 0.0,
            "f1": 0.0,
        }

    intersection = multiset_intersection_size(p_counter, e_counter)
    union = multiset_union_size(p_counter, e_counter)

    binary_exact = 1.0 if p_counter == e_counter else 0.0
    jaccard = intersection / union if union > 0 else 1.0
    precision = intersection / len(predicted_rows) if len(predicted_rows) > 0 else 0.0
    recall = intersection / len(expected_rows) if len(expected_rows) > 0 else 0.0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        "binary_exact": binary_exact,
        "jaccard": jaccard,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


def mean_and_std(values):
    """Calculates mean and sample standard deviation."""
    n = len(values)
    if n == 0:
        return 0.0, 0.0
    mean = sum(values) / n
    variance = sum((x - mean) ** 2 for x in values) / (n - 1) if n > 1 else 0.0
    return mean, math.sqrt(variance)


def evaluate_all():
    csv.field_size_limit(1_000_000_000)
    connection = eval_script.load_database()

    results_summary = {}

    header_format = (
        f"{'Framework':<12} | {'Binary Acc':<11} | {'Mean Jaccard':<13} | "
        f"{'Mean Precision':<15} | {'Mean Recall':<12} | {'Mean F1-Score':<13}"
    )
    separator = "-" * len(header_format)

    print("\n" + "=" * len(header_format))
    print("TASK 3: MULTISET FRACTIONAL RETRIEVAL METRIC COMPARISON")
    print("=" * len(header_format))
    print(header_format)
    print(separator)

    try:
        for framework_name, pred_path in PREDICTION_FILES:
            # Reload labels queue for each framework
            labels_by_question = defaultdict(deque)
            with LABELS_PATH.open(encoding="utf-8", newline="") as source:
                for row in csv.DictReader(source):
                    labels_by_question[row["question"]].append(json.loads(row["result"]))

            metrics_list = []
            partial_credit_dist = {
                "exact_1_0": 0,
                "high_0_9_to_1_0": 0,
                "mid_0_5_to_0_9": 0,
                "low_0_0_to_0_5": 0,
                "zero_0_0": 0,
            }

            with pred_path.open(encoding="utf-8", newline="") as source:
                for line_num, row in enumerate(csv.DictReader(source), start=2):
                    q = row["question"]
                    sql = row["predicted_sql"]
                    expected_rows = labels_by_question[q].popleft()

                    try:
                        predicted_rows = connection.execute(sql).fetchall()
                    except Exception as err:
                        predicted_rows = []

                    m = compute_multiset_metrics(predicted_rows, expected_rows)
                    metrics_list.append(m)

                    # Categorize Jaccard score distribution
                    score = m["jaccard"]
                    if score == 1.0:
                        partial_credit_dist["exact_1_0"] += 1
                    elif score >= 0.9:
                        partial_credit_dist["high_0_9_to_1_0"] += 1
                    elif score >= 0.5:
                        partial_credit_dist["mid_0_5_to_0_9"] += 1
                    elif score > 0.0:
                        partial_credit_dist["low_0_0_to_0_5"] += 1
                    else:
                        partial_credit_dist["zero_0_0"] += 1

            total_q = len(metrics_list)
            bin_acc = sum(m["binary_exact"] for m in metrics_list) / total_q
            j_mean, j_std = mean_and_std([m["jaccard"] for m in metrics_list])
            p_mean, _ = mean_and_std([m["precision"] for m in metrics_list])
            r_mean, _ = mean_and_std([m["recall"] for m in metrics_list])
            f_mean, f_std = mean_and_std([m["f1"] for m in metrics_list])

            print(
                f"{framework_name:<12} | {bin_acc:>9.2%}   | {j_mean:>10.4f} ({j_mean:>6.2%}) | "
                f"{p_mean:>14.4f} | {r_mean:>11.4f} | {f_mean:>10.4f} ({f_mean:>6.2%})"
            )

            results_summary[framework_name] = {
                "total_questions": total_q,
                "binary_accuracy": round(bin_acc, 6),
                "multiset_jaccard_mean": round(j_mean, 6),
                "multiset_jaccard_std": round(j_std, 6),
                "multiset_precision_mean": round(p_mean, 6),
                "multiset_recall_mean": round(r_mean, 6),
                "multiset_f1_mean": round(f_mean, 6),
                "multiset_f1_std": round(f_std, 6),
                "partial_credit_distribution": partial_credit_dist,
            }

        print(separator + "\n")

    finally:
        connection.close()

    output_json_path = CURRENT_DIR / "multiset_metrics_summary.json"
    with output_json_path.open("w", encoding="utf-8") as f:
        json.dump(results_summary, f, indent=2)
    print(f"Detailed metric calculation summary saved to: {output_json_path.name}\n")

    return results_summary


if __name__ == "__main__":
    evaluate_all()
