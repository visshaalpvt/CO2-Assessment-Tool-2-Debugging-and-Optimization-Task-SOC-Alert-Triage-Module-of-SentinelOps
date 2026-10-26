"""Corrected, readable reference implementation for the SentinelOps task."""
import math

def sort_alerts(alerts):
    """Stable insertion sort by severity, descending; returns a new list."""
    result = list(alerts)
    for i in range(1, len(result)):
        key = result[i]
        j = i - 1
        while j >= 0 and result[j][1] < key[1]:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key
    return result

def is_blocked(blocklist, ip):
    """Sequentially checks whether ip appears in blocklist."""
    for item in blocklist:
        if item == ip:
            return True
    return False

def find_signature(log, pattern):
    """Return all starting indices of exact, overlapping pattern matches."""
    if pattern == "":
        return list(range(len(log) + 1))
    n, m = len(log), len(pattern)
    hits = []
    for i in range(n - m + 1):
        j = 0
        while j < m and log[i + j] == pattern[j]:
            j += 1
        if j == m:
            hits.append(i)
    return hits

def closest_logins(events):
    """Brute-force closest pair, with each unordered pair checked once."""
    n = len(events)
    if n < 2:
        return None, math.inf
    best_sq = math.inf
    pair = None
    for i in range(n - 1):
        for j in range(i + 1, n):
            dx = events[i][0] - events[j][0]
            dy = events[i][1] - events[j][1]
            d_sq = dx * dx + dy * dy
            if d_sq < best_sq:
                best_sq = d_sq
                pair = (i, j)
    return pair, math.sqrt(best_sq)
