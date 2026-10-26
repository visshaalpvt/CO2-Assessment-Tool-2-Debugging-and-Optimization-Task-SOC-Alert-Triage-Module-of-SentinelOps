# SentinelOps SOC Alert-Triage Module
## CSA06 — Design and Analysis of Algorithms | CO2 Debugging & Optimisation Task

**Student Name:** R.VISSHAAL  
**Registration Number:** 192421025  
**Course Code & Title:** CSA06 — Design and Analysis of Algorithms  
**Assessment Component:** Continuous Assessment (CO2) — Debugging and Optimisation Task  
**Department:** Computer Science and Engineering  
**Submission Date:** 26 October 2026  
**GitHub Repository:** [https://github.com/visshaalpvt/CO2-Assessment-Tool-2-Debugging-and-Optimization-Task-SOC-Alert-Triage-Module-of-SentinelOps.git](https://github.com/visshaalpvt/CO2-Assessment-Tool-2-Debugging-and-Optimization-Task-SOC-Alert-Triage-Module-of-SentinelOps.git)

---

## 1. Project Overview & Problem Description

The **SentinelOps Security Operations Centre (SOC) Alert-Triage Module** is an incident-response pipeline responsible for:
1. **Alert Prioritisation:** Sorting incoming threat alerts by severity (highest first) while strictly preserving the arrival order of equal-severity alerts (stability).
2. **Blocklist Filtering:** Rapidly verifying whether incoming suspect IP addresses belong to a known malicious blocklist.
3. **Attack Signature Matching:** Scanning raw network security logs to locate all occurrences (including overlapping patterns) of known cyber-attack signatures.
4. **Geographical Closest-Pair Detection:** Finding the two closest login event locations from coordinates (in kilometres) to detect concurrent anomalous multi-location intrusions.

The original codebase (`Source_Code/original_buggy.py`) contained **nine critical defects** spanning index-boundary errors, loop-termination bugs, false negative and false positive logic, inverted sorting comparisons, and distance-maximisation defects.

This project delivers:
- Systematic isolation, identification, and cataloguing of all 9 defects in `defect_register.csv`.
- A verified, minimally modified baseline implementation in `Source_Code/corrected_reference.py`.
- A high-performance production-ready module in `Source_Code/optimized_module.py` scaling to 50,000 alerts and 8,000 login events.
- Four standalone pseudocode specifications in `Pseudocode/`.
- A full 57-test unit test harness in `Source_Code/test_harness.py`.
- Benchmark experiments, CSV logs, JSON exports, and high-resolution plots in `Supporting_Files/`.
- A formal 5-page academic PDF report in `Report/CO2_Debugging_Optimisation_Report.pdf`.

---

## 2. Repository Structure

```
CO2_Debugging_Optimisation/
│
├── Pseudocode/
│   ├── 01_sort_alerts.txt             # Pseudocode for stable descending alert sorting
│   ├── 02_blocklist_search.txt        # Pseudocode for set index blocklist lookup
│   ├── 03_signature_matching.txt      # Pseudocode for brute-force signature matching
│   └── 04_closest_pair.txt            # Pseudocode for divide-and-conquer closest pair
│
├── Source_Code/
│   ├── original_buggy.py              # Exact reproduction of faulty original code (9 defects)
│   ├── corrected_reference.py         # Corrected baseline (insertion sort, sequential search, etc.)
│   ├── optimized_module.py            # Production module (Timsort, set index, O(p log p) closest pair)
│   ├── test_harness.py                # 57-test automated test suite (unittest)
│   └── requirements.txt               # Dependencies (matplotlib, reportlab)
│
├── Report/
│   ├── CO2_Debugging_Optimisation_Report.pdf  # Formal academic report
│   └── screenshots/                   # Folder for environment execution screenshots
│       └── README.txt
│
├── Supporting_Files/
│   ├── test_datasets/                 # Deterministic test inputs in JSON format
│   │   ├── alerts_test_data.json
│   │   ├── blocklist_test_data.json
│   │   ├── signature_test_data.json
│   │   └── closest_pair_test_data.json
│   │
│   ├── defect_register.csv            # Comprehensive register detailing all 9 defects
│   ├── closest_pair_experiments.csv   # Benchmarks across batch sizes 1000, 2000, 4000, 8000
│   ├── insertion_sort_comparisons.csv # Comparison counts across sizes and distributions
│   ├── sort_timing_experiments.csv    # Production Timsort runtime benchmarks
│   ├── execution_log.txt              # Complete execution trace and benchmark log
│   ├── unit_test_output.txt           # Verbatim unit test outputs from both directories
│   ├── closest_pair_computations.png  # Comparison plot: Brute-force vs Divide-and-Conquer
│   ├── insertion_sort_comparisons.png # Comparison plot: Insertion sort distributions
│   ├── experimental_results.json      # Structured experimental data
│   ├── run_experiments.py             # Benchmark reproduction script
│   └── generate_report_pdf.py         # Academic PDF report generation script
│
├── README.md                          # Primary project documentation
└── .gitignore                         # Git exclusion rules
```

---

## 3. The Nine Identified Defects

| Defect # | Function | Line | Faulty Statement | Root Cause | Actual Output | Expected Output | Correction |
|:---:|:---|:---:|:---|:---|:---|:---|:---|
| **1** | `sort_alerts` | 7 | `while j > 0 and ...` | Halts before index 0; head element cannot shift | Alerts lost/corrupted | Stable descending | `while j >= 0 and ...` |
| **2** | `sort_alerts` | 10 | `alerts[j] = key` | Overwrites index `j`; duplicates shifted item at `j+1` | `A1`, `A2` lost; `A3`, `A5` duplicated | Preserves all alerts | `alerts[j + 1] = key` |
| **3** | `is_blocked` | 16 | `return False` | Inverted boolean return upon match | Blocked IP reported safe | Return `True` on match | `return True` |
| **4** | `is_blocked` | 18 | `else: return False` | Inner else exits prematurely on index 0 | `10.0.0.9 -> False` | Checks entire list | Remove inner `else` |
| **5** | `find_signature` | 23 | `for i in range(n - m):` | Loop excludes valid end index `n - m` | Misses pattern at end | Checks all $n-m+1$ | `for i in range(n - m + 1):` |
| **6** | `find_signature` | 27 | `if j == m - 1:` | Accepts mismatch breaking on last character | Falsely accepts `'FAIX'` | Matches full pattern | `if j == m:` |
| **7** | `closest_logins` | 32 | `min_dist = 0` | Initial minimum is 0; no non-negative distance is `< 0` | Fails distance minimization | Initialise to infinity | `best_sq = math.inf` |
| **8** | `closest_logins` | 34-35 | Full $n \times n$ nested loops | Evaluates self-pairs ($i=j$) and duplicate pairs | $n^2$ redundant checks | $n(n-1)/2$ unordered pairs | `i in 0..n-2, j in i+1..n-1` |
| **9** | `closest_logins` | 38 | `if d > min_dist:` | Searches for maximum distance instead of minimum | Selects farthest pair (~60.4 km) | Selects closest pair (~1.41 km) | `if d_sq < best_sq:` |

---

## 4. Algorithm & Complexity Summary

| Task / Operation | Corrected Baseline | Optimised Module | Time Complexity Gain | Auxiliary Space |
|:---|:---|:---|:---:|:---:|
| **Alert Sorting** | Insertion Sort (stable) | Adaptive Timsort | $O(n^2) \to O(n \log n)$ | $O(n)$ |
| **Blocklist Search** | Sequential Scan | Hash Set Index | $O(q \cdot b) \to O(b + q)$ [$O(1)$ query] | $O(b)$ |
| **Signature Matching** | Brute Force ($n-m+1$) | Brute Force (early mismatch exit) | Preserves $O((L-m+1)m)$ bound | $O(k)$ matches |
| **Closest Pair** | All-Pairs Brute Force | Divide-and-Conquer | $O(p^2) \to O(p \log p)$ | $O(p)$ recursion |

---

## 5. Sample Expected Outputs

When supplied with the assessment's official test data:
```python
# 1. Alert Sorting
alerts = [("A1", 3), ("A2", 9), ("A3", 5), ("A4", 9), ("A5", 1)]
sort_alerts(alerts)
# Output: [('A2', 9), ('A4', 9), ('A3', 5), ('A1', 3), ('A5', 1)]

# 2. Blocklist Query
blocklist = ["10.0.0.5", "10.0.0.9", "172.16.4.2"]
# Queries: '10.0.0.9' -> True, '10.0.0.5' -> True, '8.8.8.8' -> False

# 3. Signature Matching
find_signature("FAILFAIXFAIL", "FAIL")
# Output: [0, 8]

# 4. Closest Login Pair
events = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
closest_logins(events)
# Output: ((0, 5), 1.4142135623730951)  # sqrt(2) km
```

---

## 6. Requirements & Setup

### Environment
- Python 3.10 or later (tested on Python 3.11.9, Windows).
- Python standard library handles all core algorithms and unit testing.

### Dependencies
Install dependencies (for benchmark plotting and PDF report generation):
```bash
python -m pip install -r Source_Code/requirements.txt
```

`requirements.txt` contains:
```
matplotlib>=3.7.0
reportlab>=4.0.0
```

---

## 7. Execution Guide

### 7.1 Running the Automated Test Suite

Run the full 57-test suite from the repository root:
```bash
python -m unittest -v Source_Code/test_harness.py
```

Or from within the `Source_Code/` directory:
```bash
cd Source_Code
python -m unittest -v test_harness.py
```

All 57 tests execute and pass in approximately 0.016 seconds.

### 7.2 Reproducing Benchmark Experiments

To run the real-world benchmarks across all batch sizes (1,000 to 8,000 login events) and alert distributions:
```bash
python Supporting_Files/run_experiments.py
```
This updates:
- `Supporting_Files/closest_pair_experiments.csv`
- `Supporting_Files/insertion_sort_comparisons.csv`
- `Supporting_Files/sort_timing_experiments.csv`
- `Supporting_Files/experimental_results.json`
- `Supporting_Files/closest_pair_computations.png`
- `Supporting_Files/insertion_sort_comparisons.png`

### 7.3 Rebuilding the Academic PDF Report

To re-render the formal 5-page PDF report:
```bash
python Supporting_Files/generate_report_pdf.py
```
Output: `Report/CO2_Debugging_Optimisation_Report.pdf`.

---

## 8. Experimental Results Summary

### Closest-Pair Scalability ($p = 1,000$ to $8,000$)
| Batch Size ($p$) | Brute-Force Evaluations | Optimised Evaluations | Evaluation Reduction | Brute Time (s) | Optimised Time (s) | Speedup Factor |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1,000** | 499,500 | 1,145 | 99.77% | 0.1523s | 0.0089s | **17.1x** |
| **2,000** | 1,999,000 | 2,316 | 99.88% | 0.6024s | 0.0169s | **35.6x** |
| **4,000** | 7,998,000 | 4,618 | 99.94% | 2.4657s | 0.0357s | **69.1x** |
| **8,000** | 31,996,000 | 9,344 | **99.97%** | 7.1572s | 0.0544s | **131.6x** |

*All batch distances agree 100% with the brute-force reference.*

### Insertion-Sort Comparisons Across Distributions
| Alerts ($n$) | Already Descending ($O(n)$) | Nearly Descending ($O(n)$) | Random ($O(n^2)$) | Timsort Runtime ($s$) |
|:---:|:---:|:---:|:---:|:---:|
| **1,000** | 999 | 1,098 | 250,789 | 0.000159s |
| **5,000** | 4,999 | 5,098 | 6,289,295 | 0.000763s |
| **10,000** | 9,999 | 10,098 | 25,017,572 | 0.001440s |

---

## 9. GitHub Publication Information

- **Repository URL:** `https://github.com/visshaalpvt/CO2-Assessment-Tool-2-Debugging-and-Optimization-Task-SOC-Alert-Triage-Module-of-SentinelOps.git`
- **Main Branch:** `master` / `main`
- **Submission Commit:** Includes all source code, tests, experimental outputs, graphs, report PDF, and pseudocode.
