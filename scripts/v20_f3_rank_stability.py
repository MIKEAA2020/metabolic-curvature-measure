#!/usr/bin/env python3
"""F3 follow-up (causal-coherence review round): compute the DIRECT per-gene
rank stability between the reference path P0 and the substituted paths
P1 (oxygen limitation) / P2 (acetate switch), from the deposited per-gene
artifacts (download/deepseek_bridge/v7_P{0,1,2}_*.csv, 433 genes each,
columns gene,kappa_mu,...).

The v19 manuscript sentence "the per-gene ranking is largely
trajectory-independent" was an indirect inference (P1/P2 predictors vs the
primary carbon response, r = +0.378/+0.391). The review (finding F3) noted
the direct statistic is one computation away. This script computes it:
Spearman rho of kappa_mu between paths, on (a) the union of genes nonzero
on either side of each comparison, and (b) all 433 genes with ties (for
context). Pearson r on log10(x+1) is also recorded for scale-stability
context.

Output artifact: download/deepseek_bridge/v20_path_rank_stability.json
(no existing artifact is modified).
"""
import csv
import json
import math
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRIDGE = os.path.join(BASE, "download", "deepseek_bridge")

FILES = {
    "P0": os.path.join(BRIDGE, "v7_P0_glucose_decline.csv"),
    "P1": os.path.join(BRIDGE, "v7_P1_oxygen_limitation.csv"),
    "P2": os.path.join(BRIDGE, "v7_P2_acetate_switch.csv"),
}


def load(path):
    d = {}
    with open(path) as fh:
        for row in csv.DictReader(fh):
            d[row["gene"]] = float(row["kappa_mu"])
    return d


def spearman(xs, ys):
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1.0
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r

    rx, ry = ranks(xs), ranks(ys)
    n = len(xs)
    mx = sum(rx) / n
    my = sum(ry) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    vx = sum((a - mx) ** 2 for a in rx)
    vy = sum((b - my) ** 2 for b in ry)
    if vx == 0 or vy == 0:
        return None
    return cov / math.sqrt(vx * vy)


def pearson(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    vx = sum((a - mx) ** 2 for a in xs)
    vy = sum((b - my) ** 2 for b in ys)
    if vx == 0 or vy == 0:
        return None
    return cov / math.sqrt(vx * vy)


def main():
    data = {k: load(p) for k, p in FILES.items()}
    out = {
        "experiment": "v20 F3 direct per-gene rank stability across trajectories (kappa_mu, deposited v7 path CSVs)",
        "inputs": {k: os.path.basename(p) for k, p in FILES.items()},
        "n_genes_per_path": {k: len(v) for k, v in data.items()},
        "n_nonzero_per_path": {k: sum(1 for x in v.values() if x > 0) for k, v in data.items()},
        "comparisons": {},
    }
    for a, b in (("P0", "P1"), ("P0", "P2")):
        common = sorted(set(data[a]) & set(data[b]))
        both_nonzero = [g for g in common if data[a][g] > 0 and data[b][g] > 0]
        union_nonzero = [g for g in common if data[a][g] > 0 or data[b][g] > 0]
        va_all = [data[a][g] for g in common]
        vb_all = [data[b][g] for g in common]
        va_u = [data[a][g] for g in union_nonzero]
        vb_u = [data[b][g] for g in union_nonzero]
        va_b = [data[a][g] for g in both_nonzero]
        vb_b = [data[b][g] for g in both_nonzero]
        comp = {
            "n_common_genes": len(common),
            "n_union_nonzero": len(union_nonzero),
            "n_both_nonzero": len(both_nonzero),
            "spearman_all_433_with_ties": round(spearman(va_all, vb_all), 4),
            "spearman_union_nonzero": round(spearman(va_u, vb_u), 4),
            "spearman_both_nonzero": round(spearman(va_b, vb_b), 4),
            "pearson_both_nonzero": round(pearson(va_b, vb_b), 4),
            "pearson_log10p1_both_nonzero": round(
                pearson([math.log10(x + 1) for x in va_b],
                        [math.log10(x + 1) for x in vb_b]), 4),
        }
        out["comparisons"][f"{a}_vs_{b}"] = comp

    dest = os.path.join(BRIDGE, "v20_path_rank_stability.json")
    with open(dest, "w") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps(out, indent=2))
    print("\nSaved:", dest)


if __name__ == "__main__":
    main()
