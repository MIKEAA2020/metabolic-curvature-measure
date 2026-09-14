#!/usr/bin/env python3
"""Re-verify the extended-network RAF enumeration of
Construction con:invlim-extended (|M|=13, |R|=11) under the
CORRECTED closure-based catalysis condition of companion v3's
Definition def:raf / def:deflationary (catalysts AND reactants both
in cl_S(F), the Hordijk-Steel closure), replacing the earlier
product-pool catalyst condition. Confirms: 16 non-trivial RAFs,
21 Hasse covering inclusions, R_max = {r1..r11}, D-iteration from U
stabilizes at R_max, and per-RAF closure conditions hold."""
import itertools
from itertools import combinations

# The extended network of con:invlim-extended
RXNS = {
    1:  ({"a", "b"}, {"c"}, {"d", "e"}),
    2:  ({"a", "c"}, {"d"}, {"c"}),
    3:  ({"b", "d"}, {"e"}, {"c", "d"}),
    4:  ({"c", "d"}, {"f"}, {"e"}),
    5:  ({"a", "d"}, {"g"}, {"c"}),
    6:  ({"f", "g"}, {"h"}, {"c", "e"}),
    7:  ({"b", "f"}, {"i"}, {"d", "g"}),
    8:  ({"g", "h"}, {"j"}, {"e", "i"}),
    9:  ({"h", "i"}, {"k"}, {"j", "c"}),
    10: ({"j", "k"}, {"l"}, {"f", "g"}),
    11: ({"k", "l"}, {"m"}, {"h", "i"}),
}
FOOD = {"a", "b"}
U = set(RXNS.keys())


def hs_closure(S):
    """Hordijk-Steel closure cl_S(F): least set containing F closed
    under the reactants AND products of applicable reactions of S."""
    cur = set(FOOD)
    while True:
        added = False
        for r in S:
            react, prod, _ = RXNS[r]
            if react <= cur and not (react | prod) <= cur:
                cur |= react | prod
                added = True
        if not added:
            return cur


def is_raf_new(S):
    """Corrected condition: every r in S catalyzed by some element of
    cl_S(F), and every reactant of every r in S in cl_S(F)."""
    if not S:
        return False
    cl = hs_closure(S)
    for r in S:
        react, prod, cat = RXNS[r]
        if not (react <= cl):
            return False
        if not (cat & cl):
            return False
    return True


def is_raf_old(S):
    """Old condition (v2): catalyst in prod(S) U F; reactants in
    cl(F U prod(S)) -- degenerate reactant condition."""
    if not S:
        return False
    prods = set().union(*[RXNS[r][1] for r in S]) if S else set()
    pool = prods | FOOD
    for r in S:
        react, prod, cat = RXNS[r]
        if not (react <= pool):
            return False
        if not (cat & pool):
            return False
    return True


# enumerate all non-empty subsets (2^11 - 1 = 2047)
rafs_new, rafs_old = [], []
for k in range(1, 12):
    for S in combinations(sorted(U), k):
        S = frozenset(S)
        if is_raf_new(S):
            rafs_new.append(S)
        if is_raf_old(S):
            rafs_old.append(S)

print(f"non-trivial RAFs (new closure-based condition): {len(rafs_new)}")
print(f"non-trivial RAFs (old product-pool condition):  {len(rafs_old)}")

rmax_new = frozenset(U)
print(f"R_max = all 11 reactions is a RAF (new): {is_raf_new(rmax_new)}")
print(f"R_max is the union of all RAFs: "
      f"{frozenset().union(*rafs_new) == rmax_new}")

# D-iteration from U under the new Phi
def phi_new(S):
    cl = hs_closure(S)
    out = set()
    for r in U:
        react, prod, cat = RXNS[r]
        if (cat & cl) and (react <= cl):
            out.add(r)
    return out

S = set(U)
steps = 0
while True:
    S2 = S & phi_new(S)
    steps += 1
    if S2 == S:
        break
    S = S2
print(f"D-iteration from U stabilizes at: {sorted(S)} in {steps} steps")
print(f"stable set == R_max: {S == set(U)}")

# Hasse covering inclusions among the new RAFs
cov = 0
for A in rafs_new:
    for B in rafs_new:
        if A < B and not any(A < C < B for C in rafs_new):
            cov += 1
print(f"Hasse covering inclusions: {cov}")

# the futile-cycle sanity check: mutually catalyzing X->Y, Y->X with
# nothing food-reachable must be EXCLUDED by the new condition.
# Model it as a 2-reaction universe over {a, X, Y} with food {a}:
RXNS_FUT = {
    1: ({"X"}, {"Y"}, {"Y"}),
    2: ({"Y"}, {"X"}, {"X"}),
}
def closure_on(rxns, S, food):
    cur = set(food)
    while True:
        added = False
        for r in S:
            react, prod, _ = rxns[r]
            if react <= cur and not (react | prod) <= cur:
                cur |= react | prod
                added = True
        if not added:
            return cur
cl_futile = closure_on(RXNS_FUT, {1, 2}, {"a"})
in_cl = ("X" in cl_futile) or ("Y" in cl_futile)
# new condition: r1 needs catalyst in cl -> cat {Y} intersect cl empty -> fails
r1_ok = bool(RXNS_FUT[1][2] & cl_futile)
print(f"futile-cycle closure from food {{a}}: X or Y present = {in_cl}")
print(f"futile cycle r1 catalyzed under the new condition: {r1_ok}")

# old-vs-new difference: which subsets were RAFs under the old
# (weaker) condition but are not under the corrected one?
only_old = sorted(rafs_old and [S for S in set(rafs_old) - set(rafs_new)])
print(f"subsets RAF only under the old (weaker) condition: "
      f"{len(only_old)} -> {[sorted(s) for s in only_old][:8]}")
