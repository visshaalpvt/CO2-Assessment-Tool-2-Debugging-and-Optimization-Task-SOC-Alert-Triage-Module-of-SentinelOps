"""Comprehensive Unit Test Suite for SentinelOps SOC Alert-Triage Module.

Tests both the corrected reference implementation (corrected_reference.py)
and the optimised production implementation (optimized_module.py) across
all required categories and edge/boundary cases specified in the PRD.
"""

import math
import random
import unittest
import sys
from pathlib import Path

# Add Source_Code to path so test_harness can be run from any working directory
SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import corrected_reference as ref
import optimized_module as opt


class TestCorrectedReference(unittest.TestCase):
    """Unit tests for corrected baseline implementation."""

    # --- Sorting Tests ---
    def test_sorting_supplied_sample(self):
        sample = [("A1", 3), ("A2", 9), ("A3", 5), ("A4", 9), ("A5", 1)]
        expected = [("A2", 9), ("A4", 9), ("A3", 5), ("A1", 3), ("A5", 1)]
        self.assertEqual(ref.sort_alerts(sample), expected)

    def test_sorting_empty_list(self):
        self.assertEqual(ref.sort_alerts([]), [])

    def test_sorting_single_alert(self):
        self.assertEqual(ref.sort_alerts([("A1", 5)]), [("A1", 5)])

    def test_sorting_already_sorted_data(self):
        data = [("A1", 10), ("A2", 8), ("A3", 5), ("A4", 2)]
        self.assertEqual(ref.sort_alerts(data), data)

    def test_sorting_reverse_ordered_data(self):
        data = [("A1", 1), ("A2", 3), ("A3", 7), ("A4", 10)]
        expected = [("A4", 10), ("A3", 7), ("A2", 3), ("A1", 1)]
        self.assertEqual(ref.sort_alerts(data), expected)

    def test_sorting_equal_severities(self):
        data = [("A1", 7), ("A2", 7), ("A3", 7), ("A4", 7)]
        self.assertEqual(ref.sort_alerts(data), data)

    def test_sorting_stable_ordering(self):
        # A2 and A4 have equal severity 9; A2 arrived first and must remain before A4
        data = [("A1", 3), ("A2", 9), ("A3", 5), ("A4", 9), ("A5", 1)]
        result = ref.sort_alerts(data)
        indices = [item[0] for item in result if item[1] == 9]
        self.assertEqual(indices, ["A2", "A4"])

    def test_sorting_no_lost_or_duplicated_alerts(self):
        data = [("A1", 3), ("A2", 9), ("A3", 5), ("A4", 9), ("A5", 1)]
        result = ref.sort_alerts(data)
        self.assertEqual(sorted([x[0] for x in result]), sorted([x[0] for x in data]))
        self.assertEqual(len(result), len(data))

    # --- Blocklist Tests ---
    def test_blocklist_first_position(self):
        blocklist = ["10.0.0.5", "10.0.0.9", "172.16.4.2"]
        self.assertTrue(ref.is_blocked(blocklist, "10.0.0.5"))

    def test_blocklist_later_position(self):
        blocklist = ["10.0.0.5", "10.0.0.9", "172.16.4.2"]
        self.assertTrue(ref.is_blocked(blocklist, "10.0.0.9"))
        self.assertTrue(ref.is_blocked(blocklist, "172.16.4.2"))

    def test_blocklist_absent_ip(self):
        blocklist = ["10.0.0.5", "10.0.0.9", "172.16.4.2"]
        self.assertFalse(ref.is_blocked(blocklist, "8.8.8.8"))

    def test_blocklist_empty(self):
        self.assertFalse(ref.is_blocked([], "10.0.0.5"))

    def test_blocklist_multiple_repeated_queries(self):
        blocklist = ["10.0.0.5", "10.0.0.9", "172.16.4.2"]
        queries = ["10.0.0.9", "8.8.8.8", "10.0.0.5", "192.168.1.1"]
        expected = [True, False, True, False]
        actual = [ref.is_blocked(blocklist, q) for q in queries]
        self.assertEqual(actual, expected)

    # --- Signature Matching Tests ---
    def test_signature_supplied_sample(self):
        self.assertEqual(ref.find_signature("FAILFAIXFAIL", "FAIL"), [0, 8])

    def test_signature_at_beginning(self):
        self.assertEqual(ref.find_signature("FAIL_SECURE_LOG", "FAIL"), [0])

    def test_signature_at_end(self):
        self.assertEqual(ref.find_signature("SECURE_LOG_FAIL", "FAIL"), [11])

    def test_signature_multiple_occurrences(self):
        self.assertEqual(ref.find_signature("WARN_WARN_WARN", "WARN"), [0, 5, 10])

    def test_signature_overlapping_occurrences(self):
        self.assertEqual(ref.find_signature("aaaa", "aa"), [0, 1, 2])

    def test_signature_no_match(self):
        self.assertEqual(ref.find_signature("CLEAN_TRAFFIC", "ATTACK"), [])

    def test_signature_pattern_longer_than_log(self):
        self.assertEqual(ref.find_signature("abc", "abcd"), [])

    def test_signature_empty_log(self):
        self.assertEqual(ref.find_signature("", "FAIL"), [])

    def test_signature_empty_pattern(self):
        # Documented convention: empty pattern matches at all positions 0..len(log)
        self.assertEqual(ref.find_signature("abc", ""), [0, 1, 2, 3])

    # --- Closest Pair Tests ---
    def test_closest_pair_supplied_sample(self):
        events = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
        pair, dist = ref.closest_logins(events)
        self.assertEqual(sorted(pair), [0, 5])
        self.assertAlmostEqual(dist, math.sqrt(2), places=7)

    def test_closest_pair_empty_event_list(self):
        pair, dist = ref.closest_logins([])
        self.assertIsNone(pair)
        self.assertTrue(math.isinf(dist))

    def test_closest_pair_one_event(self):
        pair, dist = ref.closest_logins([(10, 20)])
        self.assertIsNone(pair)
        self.assertTrue(math.isinf(dist))

    def test_closest_pair_two_events(self):
        events = [(1, 1), (4, 5)]
        pair, dist = ref.closest_logins(events)
        self.assertEqual(sorted(pair), [0, 1])
        self.assertAlmostEqual(dist, 5.0, places=7)

    def test_closest_pair_duplicate_coordinates(self):
        events = [(2, 3), (10, 20), (2, 3)]
        pair, dist = ref.closest_logins(events)
        self.assertAlmostEqual(dist, 0.0, places=7)
        self.assertEqual(sorted(pair), [0, 2])

    def test_closest_pair_multiple_equally_close_pairs(self):
        # (0,0) to (0,1) is 1.0; (0,1) to (0,2) is 1.0
        events = [(0, 0), (0, 1), (0, 2)]
        pair, dist = ref.closest_logins(events)
        self.assertAlmostEqual(dist, 1.0, places=7)


class TestOptimizedModule(unittest.TestCase):
    """Unit tests for optimised production implementation."""

    # --- Sorting Tests ---
    def test_opt_sorting_supplied_sample(self):
        sample = [("A1", 3), ("A2", 9), ("A3", 5), ("A4", 9), ("A5", 1)]
        expected = [("A2", 9), ("A4", 9), ("A3", 5), ("A1", 3), ("A5", 1)]
        self.assertEqual(opt.sort_alerts(sample), expected)

    def test_opt_sorting_empty_list(self):
        self.assertEqual(opt.sort_alerts([]), [])

    def test_opt_sorting_single_alert(self):
        self.assertEqual(opt.sort_alerts([("A1", 5)]), [("A1", 5)])

    def test_opt_sorting_already_sorted_data(self):
        data = [("A1", 10), ("A2", 8), ("A3", 5), ("A4", 2)]
        self.assertEqual(opt.sort_alerts(data), data)

    def test_opt_sorting_reverse_ordered_data(self):
        data = [("A1", 1), ("A2", 3), ("A3", 7), ("A4", 10)]
        expected = [("A4", 10), ("A3", 7), ("A2", 3), ("A1", 1)]
        self.assertEqual(opt.sort_alerts(data), expected)

    def test_opt_sorting_equal_severities(self):
        data = [("A1", 7), ("A2", 7), ("A3", 7), ("A4", 7)]
        self.assertEqual(opt.sort_alerts(data), data)

    def test_opt_sorting_stable_ordering(self):
        data = [("A1", 3), ("A2", 9), ("A3", 5), ("A4", 9), ("A5", 1)]
        result = opt.sort_alerts(data)
        indices = [item[0] for item in result if item[1] == 9]
        self.assertEqual(indices, ["A2", "A4"])

    def test_opt_sorting_no_lost_or_duplicated_alerts(self):
        data = [("A1", 3), ("A2", 9), ("A3", 5), ("A4", 9), ("A5", 1)]
        result = opt.sort_alerts(data)
        self.assertEqual(sorted([x[0] for x in result]), sorted([x[0] for x in data]))
        self.assertEqual(len(result), len(data))

    # --- Blocklist Tests ---
    def test_opt_blocklist_first_position(self):
        blocklist = ["10.0.0.5", "10.0.0.9", "172.16.4.2"]
        idx = opt.make_blocklist_index(blocklist)
        self.assertTrue(opt.is_blocked(idx, "10.0.0.5"))

    def test_opt_blocklist_later_position(self):
        blocklist = ["10.0.0.5", "10.0.0.9", "172.16.4.2"]
        idx = opt.make_blocklist_index(blocklist)
        self.assertTrue(opt.is_blocked(idx, "10.0.0.9"))
        self.assertTrue(opt.is_blocked(idx, "172.16.4.2"))

    def test_opt_blocklist_absent_ip(self):
        blocklist = ["10.0.0.5", "10.0.0.9", "172.16.4.2"]
        idx = opt.make_blocklist_index(blocklist)
        self.assertFalse(opt.is_blocked(idx, "8.8.8.8"))

    def test_opt_blocklist_empty(self):
        idx = opt.make_blocklist_index([])
        self.assertFalse(opt.is_blocked(idx, "10.0.0.5"))

    def test_opt_blocklist_multiple_repeated_queries(self):
        blocklist = ["10.0.0.5", "10.0.0.9", "172.16.4.2"]
        idx = opt.make_blocklist_index(blocklist)
        queries = ["10.0.0.9", "8.8.8.8", "10.0.0.5", "192.168.1.1"]
        expected = [True, False, True, False]
        actual = [opt.is_blocked(idx, q) for q in queries]
        self.assertEqual(actual, expected)

    # --- Signature Matching Tests ---
    def test_opt_signature_supplied_sample(self):
        self.assertEqual(opt.find_signature("FAILFAIXFAIL", "FAIL"), [0, 8])

    def test_opt_signature_at_beginning(self):
        self.assertEqual(opt.find_signature("FAIL_SECURE_LOG", "FAIL"), [0])

    def test_opt_signature_at_end(self):
        self.assertEqual(opt.find_signature("SECURE_LOG_FAIL", "FAIL"), [11])

    def test_opt_signature_multiple_occurrences(self):
        self.assertEqual(opt.find_signature("WARN_WARN_WARN", "WARN"), [0, 5, 10])

    def test_opt_signature_overlapping_occurrences(self):
        self.assertEqual(opt.find_signature("aaaa", "aa"), [0, 1, 2])

    def test_opt_signature_no_match(self):
        self.assertEqual(opt.find_signature("CLEAN_TRAFFIC", "ATTACK"), [])

    def test_opt_signature_pattern_longer_than_log(self):
        self.assertEqual(opt.find_signature("abc", "abcd"), [])

    def test_opt_signature_empty_log(self):
        self.assertEqual(opt.find_signature("", "FAIL"), [])

    def test_opt_signature_empty_pattern(self):
        self.assertEqual(opt.find_signature("abc", ""), [0, 1, 2, 3])

    # --- Closest Pair Tests ---
    def test_opt_closest_pair_supplied_sample(self):
        events = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
        pair, dist = opt.closest_logins(events)
        self.assertEqual(sorted(pair), [0, 5])
        self.assertAlmostEqual(dist, math.sqrt(2), places=7)

    def test_opt_closest_pair_empty_event_list(self):
        pair, dist = opt.closest_logins([])
        self.assertIsNone(pair)
        self.assertTrue(math.isinf(dist))

    def test_opt_closest_pair_one_event(self):
        pair, dist = opt.closest_logins([(10, 20)])
        self.assertIsNone(pair)
        self.assertTrue(math.isinf(dist))

    def test_opt_closest_pair_two_events(self):
        events = [(1, 1), (4, 5)]
        pair, dist = opt.closest_logins(events)
        self.assertEqual(sorted(pair), [0, 1])
        self.assertAlmostEqual(dist, 5.0, places=7)

    def test_opt_closest_pair_duplicate_coordinates(self):
        events = [(2, 3), (10, 20), (2, 3)]
        pair, dist = opt.closest_logins(events)
        self.assertAlmostEqual(dist, 0.0, places=7)
        self.assertEqual(sorted(pair), [0, 2])

    def test_opt_closest_pair_multiple_equally_close_pairs(self):
        events = [(0, 0), (0, 1), (0, 2)]
        pair, dist = opt.closest_logins(events)
        self.assertAlmostEqual(dist, 1.0, places=7)

    def test_opt_closest_pair_random_datasets_cross_check(self):
        """Cross-checks divide-and-conquer against independent brute force across 40 random sets."""
        rng = random.Random(20261026)
        for n in range(2, 42):
            pts = [(rng.uniform(-1000, 1000), rng.uniform(-1000, 1000)) for _ in range(n)]
            opt_pair, opt_dist = opt.closest_logins(pts)

            # Independent brute force calculation
            best_sq = math.inf
            for i in range(n - 1):
                for j in range(i + 1, n):
                    d_sq = (pts[i][0] - pts[j][0]) ** 2 + (pts[i][1] - pts[j][1]) ** 2
                    if d_sq < best_sq:
                        best_sq = d_sq
            bf_dist = math.sqrt(best_sq)

            self.assertAlmostEqual(opt_dist, bf_dist, places=7,
                                   msg=f"Discrepancy at n={n}: opt={opt_dist}, bf={bf_dist}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
