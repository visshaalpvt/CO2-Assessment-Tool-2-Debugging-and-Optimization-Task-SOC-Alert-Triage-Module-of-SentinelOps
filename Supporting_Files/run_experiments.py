"""Experimental Analysis Script for SentinelOps SOC Alert-Triage Module.

Executes real benchmarks for:
1. Closest-pair distance computations and runtimes (brute-force vs divide-and-conquer)
   across batch sizes: 1000, 2000, 4000, 8000 events.
2. Insertion-sort key comparisons across input sizes: 1000, 5000, 10000 alerts
   under already-descending, nearly-descending, and random distributions.
3. Stable production sort (Timsort) runtimes across the same distributions.
4. Generates publication-quality charts (PNG) and structured CSV/JSON results.
"""

from pathlib import Path
import csv
import json
import math
import random
import sys
import time

ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR.parent / "Source_Code"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import optimized_module as opt


def brute_force_closest_pair(points):
    """Reference brute force evaluating all p*(p-1)//2 pairs."""
    n = len(points)
    if n < 2:
        return None, math.inf, 0
    best_sq = math.inf
    pair = None
    count = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            count += 1
            dx = points[i][0] - points[j][0]
            dy = points[i][1] - points[j][1]
            d_sq = dx * dx + dy * dy
            if d_sq < best_sq:
                best_sq = d_sq
                pair = (i, j)
    return pair, math.sqrt(best_sq), count


def count_insertion_sort_comparisons(items):
    """Count key comparisons in stable descending insertion sort."""
    arr = list(items)
    comparisons = 0
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if arr[j][1] < key[1]:
                arr[j + 1] = arr[j]
                j -= 1
            else:
                break
        arr[j + 1] = key
    return comparisons


def run_closest_pair_experiments():
    batch_sizes = [1000, 2000, 4000, 8000]
    results = []
    print("=" * 70)
    print("RUNNING CLOSEST-PAIR EXPERIMENTS (BATCHES: 1000, 2000, 4000, 8000)")
    print("=" * 70)

    for n in batch_sizes:
        # Deterministic pseudo-random generation with fixed seed
        rng = random.Random(20261026 + n)
        points = [(rng.uniform(0, 1_000_000), rng.uniform(0, 1_000_000)) for _ in range(n)]

        # Benchmark Brute Force
        t0 = time.perf_counter()
        bf_pair, bf_dist, bf_count = brute_force_closest_pair(points)
        bf_time = time.perf_counter() - t0

        # Benchmark Optimised Divide-and-Conquer
        t0 = time.perf_counter()
        opt_pair, opt_dist, opt_count = opt.closest_logins_with_count(points)
        opt_time = time.perf_counter() - t0

        agree = math.isclose(bf_dist, opt_dist, rel_tol=1e-9, abs_tol=1e-9)

        row = {
            "batch_size": n,
            "brute_force_distance_computations": bf_count,
            "optimized_distance_computations": opt_count,
            "brute_force_seconds": round(bf_time, 6),
            "optimized_seconds": round(opt_time, 6),
            "brute_force_distance": round(bf_dist, 6),
            "optimized_distance": round(opt_dist, 6),
            "distances_agree": agree
        }
        results.append(row)
        print(f"Batch {n:5d}: BF comps = {bf_count:10,d} ({bf_time:.4f}s) | "
              f"Opt comps = {opt_count:6,d} ({opt_time:.4f}s) | Dist Agree: {agree}")

    # Write closest_pair_experiments.csv
    csv_path = ROOT_DIR / "closest_pair_experiments.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)
    print(f"Saved: {csv_path}")
    return results


def run_sorting_experiments():
    input_sizes = [1000, 5000, 10000]
    comparison_results = []
    timing_results = []

    print("\n" + "=" * 70)
    print("RUNNING SORTING EXPERIMENTS (SIZES: 1000, 5000, 10000)")
    print("=" * 70)

    for n in input_sizes:
        rng = random.Random(404 + n)

        # Datasets
        descending_data = [(f"A_{i}", n - i) for i in range(n)]
        nearly_descending = list(descending_data)
        # Swap 1% of elements
        for i in range(0, n - 1, max(1, n // 100)):
            nearly_descending[i], nearly_descending[i + 1] = nearly_descending[i + 1], nearly_descending[i]
        random_data = [(f"A_{i}", rng.randint(1, 1000)) for i in range(n)]

        distributions = [
            ("already_descending", descending_data),
            ("nearly_descending", nearly_descending),
            ("random", random_data)
        ]

        for dist_name, dataset in distributions:
            # Measure insertion sort comparisons
            comp_count = count_insertion_sort_comparisons(dataset)
            comparison_results.append({
                "input_size": n,
                "distribution": dist_name,
                "insertion_sort_key_comparisons": comp_count
            })

            # Measure Timsort runtime
            t0 = time.perf_counter()
            opt.sort_alerts(dataset)
            timsort_time = time.perf_counter() - t0
            timing_results.append({
                "input_size": n,
                "distribution": dist_name,
                "timsort_seconds": round(timsort_time, 6)
            })

            print(f"Size {n:5d} | {dist_name:18s} | Comparisons: {comp_count:10,d} | Timsort: {timsort_time:.6f}s")

    # Write insertion_sort_comparisons.csv
    comp_csv = ROOT_DIR / "insertion_sort_comparisons.csv"
    with comp_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(comparison_results[0].keys()))
        writer.writeheader()
        writer.writerows(comparison_results)
    print(f"Saved: {comp_csv}")

    # Write sort_timing_experiments.csv
    timing_csv = ROOT_DIR / "sort_timing_experiments.csv"
    with timing_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(timing_results[0].keys()))
        writer.writeheader()
        writer.writerows(timing_results)
    print(f"Saved: {timing_csv}")

    return comparison_results, timing_results


def generate_plots(cp_results, sort_results):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        # Plot 1: Closest Pair Computations
        plt.figure(figsize=(9, 5.5), dpi=300)
        batch_sizes = [r["batch_size"] for r in cp_results]
        bf_comps = [r["brute_force_distance_computations"] for r in cp_results]
        opt_comps = [r["optimized_distance_computations"] for r in cp_results]

        plt.plot(batch_sizes, bf_comps, marker="o", color="#d9534f", linewidth=2.5,
                 label="Brute-Force: $O(p^2)$ [Exact $p(p-1)/2$]")
        plt.plot(batch_sizes, opt_comps, marker="s", color="#2e6da4", linewidth=2.5,
                 label="Optimised Divide-and-Conquer: $O(p \\log p)$")

        plt.yscale("log")
        plt.title("Closest-Pair Distance Computations vs Batch Size (Log Scale)", fontsize=13, fontweight="bold", pad=12)
        plt.xlabel("Batch Size (Number of Login Events $p$)", fontsize=11, labelpad=8)
        plt.ylabel("Squared-Distance Evaluations (Log Scale)", fontsize=11, labelpad=8)
        plt.xticks(batch_sizes, [f"{b:,}" for b in batch_sizes])
        plt.grid(True, which="both", linestyle="--", alpha=0.6)
        plt.legend(fontsize=10, loc="upper left")
        plt.tight_layout()

        cp_plot_path = ROOT_DIR / "closest_pair_computations.png"
        plt.savefig(cp_plot_path)
        plt.close()
        print(f"Generated plot: {cp_plot_path}")

        # Plot 2: Insertion Sort Comparisons
        plt.figure(figsize=(9, 5.5), dpi=300)
        sizes = [1000, 5000, 10000]
        dist_labels = ["already_descending", "nearly_descending", "random"]
        colors = {"already_descending": "#5cb85c", "nearly_descending": "#f0ad4e", "random": "#d9534f"}
        display_names = {
            "already_descending": "Already Descending (Best Case: O(n))",
            "nearly_descending": "Nearly Descending (Adaptive: O(n))",
            "random": "Random Distribution (Worst/Avg Case: O(n²))"
        }

        for dist in dist_labels:
            comps = [r["insertion_sort_key_comparisons"] for r in sort_results if r["distribution"] == dist]
            plt.plot(sizes, comps, marker="o", linewidth=2.2, color=colors[dist], label=display_names[dist])

        plt.yscale("log")
        plt.title("Insertion-Sort Key Comparisons Across Input Distributions", fontsize=13, fontweight="bold", pad=12)
        plt.xlabel("Input Size (Number of Alerts $n$)", fontsize=11, labelpad=8)
        plt.ylabel("Key Comparisons (Log Scale)", fontsize=11, labelpad=8)
        plt.xticks(sizes, [f"{s:,}" for s in sizes])
        plt.grid(True, which="both", linestyle="--", alpha=0.6)
        plt.legend(fontsize=10, loc="upper left")
        plt.tight_layout()

        sort_plot_path = ROOT_DIR / "insertion_sort_comparisons.png"
        plt.savefig(sort_plot_path)
        plt.close()
        print(f"Generated plot: {sort_plot_path}")

    except Exception as e:
        print(f"Plot generation failed: {e}")


def main():
    cp_results = run_closest_pair_experiments()
    sort_comp_results, sort_timing_results = run_sorting_experiments()

    # Save experimental_results.json
    all_data = {
        "metadata": {
            "student_name": "R.VISSHAAL",
            "registration_number": "192421025",
            "course": "CSA06 - Design and Analysis of Algorithms",
            "task": "CO2 Debugging and Optimisation - SentinelOps SOC Alert-Triage",
            "seed_closest_pair_base": 20261026,
            "seed_sorting_base": 404
        },
        "closest_pair_benchmarks": cp_results,
        "insertion_sort_comparisons": sort_comp_results,
        "timsort_timings": sort_timing_results
    }
    json_path = ROOT_DIR / "experimental_results.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2)
    print(f"Saved: {json_path}")

    # Generate charts
    generate_plots(cp_results, sort_comp_results)
    print("\nAll experiments and artifact generations completed successfully.")


if __name__ == "__main__":
    main()
