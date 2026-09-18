#!/usr/bin/env python3
"""Recompute the six-signal score published at rizzmaster.net/best-ai-dating-simulators/
from inputs.csv. No dependencies. Formula text: METHOD.md.

  python3 score.py   -> writes scores.csv
"""
import csv, math

def rating_signal(stars): return stars * 20
def volume_signal(n): return 0 if n <= 0 else min(100, max(0, 40 + 10 * math.log10(n)))
def newest_reviews_signal(avg, n, median, penalty):
    if not n: return median
    raw = max(0, avg * 20 - penalty)   # integrity penalty hits the raw signal, then the pull toward the median
    w = n / (n + 50)
    return w * raw + (1 - w) * median
def freshness_signal(days):
    if days <= 30: return 100
    return max(0, 100 * (1 - ((days - 30) / 1065) ** 0.84))
def features_signal(documented): return documented / 9 * 100
def quality_signal(p, m, n, neutral):
    if neutral or (p + m + n) < 3: return 50
    return (p + 0.5 * m + 1) / (p + m + n + 2) * 100

def score_row(r):
    f = lambda k: float(r[k]) if r[k] not in ("", None) else None
    s = {
        "rating": rating_signal(f("rating_weighted")),
        "volume": volume_signal(int(float(r["rating_count_total"] or 0))),
        "newest_reviews": newest_reviews_signal(f("newest_reviews_avg") or 0, int(float(r["newest_reviews_n"] or 0)), f("cohort_median"), f("integrity_penalty") or 0),
        "freshness": freshness_signal(int(float(r["days_since_update"]))) if r["days_since_update"] else 0,
        "features": features_signal(int(r["feature_checks_documented"])),
        "quality": quality_signal(int(r["quality_p"]), int(r["quality_m"]), int(r["quality_n"]), r["quality_neutral"] == "true"),
    }
    s["score"] = sum(s.values()) / 6
    return s

def main():
    rows = list(csv.DictReader(open("inputs.csv", newline="", encoding="utf-8")))
    out = []
    for r in rows:
        s = score_row(r)
        out.append({"slug": r["slug"], "name": r["name"], **{k: f"{v:.2f}" for k, v in s.items()}})
    out.sort(key=lambda x: (-float(x["score"]), x["slug"]))
    with open("scores.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["slug","name","rating","volume","newest_reviews","freshness","features","quality","score"], lineterminator="\n")
        w.writeheader(); w.writerows(out)
    print(f"{len(out)} products scored")

if __name__ == "__main__":
    main()
