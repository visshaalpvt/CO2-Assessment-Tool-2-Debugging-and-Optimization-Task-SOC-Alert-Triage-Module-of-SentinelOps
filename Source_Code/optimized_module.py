"""Optimised SentinelOps SOC alert-triage algorithms.

The functions preserve the corrected behaviour:
- stable descending severity sort;
- exact blocklist membership;
- all (including overlapping) signature matches;
- closest unordered pair of locations, with indices into the input.
"""
from math import inf, sqrt
from bisect import bisect_left, insort

def sort_alerts(alerts):
    """Stable O(n log n) sort for production batches; equal severities keep order."""
    # Python's Timsort is stable and adaptive to existing order.
    return sorted(alerts, key=lambda alert: alert[1], reverse=True)

def make_blocklist_index(blocklist):
    """Build once for repeated queries; expected O(b) build and O(1) lookup."""
    return set(blocklist)

def is_blocked(blocklist_index, ip):
    """Membership query against a set created by make_blocklist_index."""
    return ip in blocklist_index

def find_signature(log, pattern):
    """Brute-force matcher with no redundant character comparisons per alignment."""
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
    """Divide-and-conquer closest pair; returns ((i, j), Euclidean distance).

    Runs in O(n log n) time. The recursive strip only compares points close
    enough in x to the best known distance and stops by y-separation.
    """
    n = len(events)
    if n < 2:
        return None, inf
    points = [(float(x), float(y), i) for i, (x, y) in enumerate(events)]
    points.sort(key=lambda p: (p[0], p[1], p[2]))
    distance_computations = 0

    def d2(a, b):
        nonlocal distance_computations
        distance_computations += 1
        dx, dy = a[0] - b[0], a[1] - b[1]
        return dx * dx + dy * dy

    def solve(px):
        m = len(px)
        if m <= 3:
            best = inf
            pair = None
            for a in range(m):
                for b in range(a + 1, m):
                    value = d2(px[a], px[b])
                    if value < best:
                        best, pair = value, (px[a][2], px[b][2])
            return best, pair, sorted(px, key=lambda p: p[1])

        mid = m // 2
        mid_x = px[mid][0]
        left_best, left_pair, left_y = solve(px[:mid])
        right_best, right_pair, right_y = solve(px[mid:])
        if left_best <= right_best:
            best, pair = left_best, left_pair
        else:
            best, pair = right_best, right_pair

        # Merge children by y coordinate.
        merged = []
        i = j = 0
        while i < len(left_y) and j < len(right_y):
            if left_y[i][1] <= right_y[j][1]:
                merged.append(left_y[i]); i += 1
            else:
                merged.append(right_y[j]); j += 1
        merged.extend(left_y[i:]); merged.extend(right_y[j:])

        strip = [p for p in merged if (p[0] - mid_x) ** 2 < best]
        for a in range(len(strip)):
            b = a + 1
            while b < len(strip) and (strip[b][1] - strip[a][1]) ** 2 < best:
                value = d2(strip[a], strip[b])
                if value < best:
                    best, pair = value, (strip[a][2], strip[b][2])
                b += 1
        return best, pair, merged

    best_sq, pair, _ = solve(points)
    return pair, sqrt(best_sq)

def closest_logins_with_count(events):
    """Return pair, distance and actual squared-distance evaluations for experiments."""
    n = len(events)
    if n < 2:
        return None, inf, 0
    points = [(float(x), float(y), i) for i, (x, y) in enumerate(events)]
    points.sort(key=lambda p: (p[0], p[1], p[2]))
    count = 0
    def d2(a, b):
        nonlocal count
        count += 1
        dx, dy = a[0] - b[0], a[1] - b[1]
        return dx*dx + dy*dy
    def solve(px):
        m = len(px)
        if m <= 3:
            best, pair = inf, None
            for a in range(m):
                for b in range(a+1, m):
                    value = d2(px[a], px[b])
                    if value < best:
                        best, pair = value, (px[a][2], px[b][2])
            return best, pair, sorted(px, key=lambda p:p[1])
        mid = m//2
        mid_x = px[mid][0]
        lb, lp, ly = solve(px[:mid])
        rb, rp, ry = solve(px[mid:])
        best, pair = (lb, lp) if lb <= rb else (rb, rp)
        merged=[]; i=j=0
        while i<len(ly) and j<len(ry):
            if ly[i][1] <= ry[j][1]:
                merged.append(ly[i]); i+=1
            else:
                merged.append(ry[j]); j+=1
        merged.extend(ly[i:]); merged.extend(ry[j:])
        strip=[p for p in merged if (p[0]-mid_x)**2 < best]
        for a in range(len(strip)):
            b=a+1
            while b<len(strip) and (strip[b][1]-strip[a][1])**2 < best:
                value=d2(strip[a],strip[b])
                if value<best:
                    best, pair=value,(strip[a][2],strip[b][2])
                b+=1
        return best,pair,merged
    best,pair,_=solve(points)
    return pair, sqrt(best), count
