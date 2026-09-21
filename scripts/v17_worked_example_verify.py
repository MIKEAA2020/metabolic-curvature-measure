#!/usr/bin/env python3
"""v17 worked-example machine verification.

Verifies, by LP re-solves, every number used in the manuscript's
worked-example subsection ("A worked example: three chambers, two
walls"):

Network (two-pathway switch):
  one pool M; v0 = import (0 <= v0 <= theta), v1 = high-yield pathway
  (0 <= v1 <= c), v2 = low-yield pathway (0 <= v2 <= d);
  mass balance v0 = v1 + v2; growth Phi = a v1 + b v2 with a > b.

Instance used in the manuscript: a = 2, b = 1, c = 1, d = 2,
sweep theta in [0, 4] (so T = 4; the 1/T normalization of
Definition 2.2 rescales all kappa values by the same constant and is
omitted in the manuscript's statement).

Checks:
  A. phase structure: v* = (theta, theta, 0) / (theta, c, theta-c) /
     (c+d, c, d) on the three phases; Phi = 2theta / theta+1 / 5.
  B. slope jumps: v1 jump -1 at theta=c; v2 jumps +1 at c and -1 at
     c+d; v0 jump -1 at c+d; Phi jumps (b-a)=-1 at c and -b=-1 at c+d.
  C. coupling identity D2 Phi = c_r D2 v_r at both walls (exact).
  D. kappa by hand: kappa(g1)=1, kappa(g2)=2 (raw path-integrated
     masses; ratio 2:1).
  E. degenerate variant a=b=2: Phi = 2 min(theta,3) -> value layer has
     NO kink at theta=1 (growth-silent wall; coupling contraction
     2*(-1)+2*(+1) = 0) and a single kink of mass -2 at theta=3;
     under the v1-preferring tie-break the flux layer keeps the kink
     at theta=1 (v1 = min(1,theta), v2 = max(0, theta-1)); under the
     v2-preferring tie-break the kink moves to theta=d=2
     (v2 = min(2,theta), v1 = max(0, theta-2)).
"""
import json
import numpy as np
from scipy.optimize import linprog

DL = "/home/z/my-project/metabolic-curvature-measure/download"


def solve(theta, a, b, c, d, prefer="v1"):
    """Lexicographic 3-stage solve: max a*v1+b*v2; then min L1; then
    prefer the named pathway (stage-3 surrogate: minimize the other
    pathway's flux).  Variables (v0, v1, v2) >= 0.

    Constraints: v0 - v1 - v2 = 0; v0 <= theta; v1 <= c; v2 <= d.
    """
    A_eq = [[1.0, -1.0, -1.0]]
    b_eq = [0.0]
    A_ub = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    b_ub = [theta, c, d]
    # stage 1: max growth = a*v1 + b*v2 (c = (0, a, b) on (v0,v1,v2))
    r1 = linprog([0.0, -a, -b], A_ub=A_ub, b_ub=b_ub, A_eq=A_eq,
                 b_eq=b_eq, bounds=(0, None), method="highs")
    assert r1.status == 0
    # stage 2: min L1 = v0 (v0 = v1 + v2 fixes it given growth);
    # at the optimum v0 is already determined by the growth value, so
    # stage 2 is vacuous here; keep it for form.
    r2 = linprog([1.0, 0.0, 0.0], A_ub=A_ub, b_ub=b_ub, A_eq=A_eq,
                 b_eq=b_eq, bounds=(0, None), method="highs")
    assert r2.status == 0
    # stage 3: prefer pathway (minimize the disfavored one) subject to
    # optimal growth: -(a v1 + b v2) <= r1.fun  (r1.fun = -growth_opt)
    A_aug = A_ub + [[0.0, -a, -b]]
    b_aug = b_ub + [r1.fun]
    obj3 = [0.0, 0.0, 1.0] if prefer == "v1" else [0.0, 1.0, 0.0]
    r3 = linprog(obj3, A_ub=A_aug, b_ub=b_aug, A_eq=A_eq, b_eq=b_eq,
                 bounds=(0, None), method="highs")
    assert r3.status == 0, r3.message
    return r1.fun * -1.0, np.array(r3.x)


def slopes(f, xs):
    return np.array([f(x) for x in xs])


checks = []


def check(name, claim, value, ok):
    checks.append({"name": name, "claim": claim, "value": value,
                   "status": "PASS" if ok else "FAIL"})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {claim} | {value}")


a, b, c, d = 2.0, 1.0, 1.0, 2.0

# ---- A. phase structure --------------------------------------------------
thetas = [0.2, 0.5, 0.9, 1.0, 1.1, 1.5, 2.0, 2.9, 3.0, 3.1, 3.5, 4.0]
worst = 0.0
for t in thetas:
    Phi, v = solve(t, a, b, c, d, prefer="v1")
    if t <= c:
        want = np.array([t, t, 0.0]); Phi_want = a * t
    elif t <= c + d:
        want = np.array([t, c, t - c]); Phi_want = a * c + b * (t - c)
    else:
        want = np.array([c + d, c, d]); Phi_want = a * c + b * d
    worst = max(worst, np.abs(v - want).max(), abs(Phi - Phi_want))
check("A-phase", "phase formulas on 12 sample thetas", f"max err {worst:.2e}",
      worst < 1e-9)

# ---- B. slope jumps (finite differences across the walls) ----------------
h = 1e-6


def fluxes(t, prefer="v1", aa=None, bb=None):
    return solve(t, aa if aa is not None else a,
                 bb if bb is not None else b, c, d, prefer)[1]


def Phi_of(t, prefer="v1"):
    return solve(t, a, b, c, d, prefer)[0]


for wall, comp, want in [(c, 1, -1.0), (c, 2, +1.0), (c + d, 2, -1.0),
                         (c + d, 0, -1.0)]:
    # slope jump = slope_after - slope_before across the wall:
    sl_before = (fluxes(wall)[comp] - fluxes(wall - h)[comp]) / h
    sl_after = (fluxes(wall + h)[comp] - fluxes(wall)[comp]) / h
    jump = sl_after - sl_before
    check(f"B-jump-v{comp}-at-{wall}", f"slope jump {want:+.0f}",
          f"{jump:+.6f}", abs(jump - want) < 1e-3)

for wall, want in [(c, b - a), (c + d, -b)]:
    sl_before = (Phi_of(wall) - Phi_of(wall - h)) / h
    sl_after = (Phi_of(wall + h) - Phi_of(wall)) / h
    jump = sl_after - sl_before
    check(f"B-jump-Phi-at-{wall}", f"Phi slope jump {want:+.0f}",
          f"{jump:+.6f}", abs(jump - want) < 1e-3)

# ---- C. coupling identity ------------------------------------------------
cvec = np.array([0.0, a, b])
for wall in [c, c + d]:
    lhs = (Phi_of(wall + h) - 2 * Phi_of(wall) + Phi_of(wall - h))
    rhs = sum(cvec[r] * (fluxes(wall + h)[r] - 2 * fluxes(wall)[r]
                         + fluxes(wall - h)[r]) for r in range(3))
    check(f"C-coupling-{wall}", "D2 Phi = sum c_r D2 v_r (2nd difference)",
          f"lhs {lhs:+.2e} rhs {rhs:+.2e}", abs(lhs - rhs) < 1e-6)

# ---- D. kappa by hand ----------------------------------------------------
# raw path-integrated masses over [0, 4] with T-normalization 1/4:
# kappa(g1) = |jump in v1 at c| = 1 ; kappa(g2) = |+1| + |-1| = 2
k1 = abs((fluxes(c + h)[1] - fluxes(c)[1]) / h
         - (fluxes(c)[1] - fluxes(c - h)[1]) / h)
k2 = abs((fluxes(c + h)[2] - fluxes(c)[2]) / h
         - (fluxes(c)[2] - fluxes(c - h)[2]) / h) + \
    abs((fluxes(c + d + h)[2] - fluxes(c + d)[2]) / h
        - (fluxes(c + d)[2] - fluxes(c + d - h)[2]) / h)
check("D-kappa-g1", "kappa(g1) = 1", f"{k1:.6f}", abs(k1 - 1.0) < 1e-3)
check("D-kappa-g2", "kappa(g2) = 2", f"{k2:.6f}", abs(k2 - 2.0) < 1e-3)

# ---- E. degenerate variant a = b ----------------------------------------
a2 = 2.0
Phi2 = lambda t: solve(t, a2, a2, c, d, prefer="v1")[0]
# value layer kink at theta = c must vanish (growth-silent wall):
sl_b = (Phi2(c) - Phi2(c - h)) / h
sl_a = (Phi2(c + h) - Phi2(c)) / h
check("E-silent-wall", "a=b: Phi has no kink at theta=c",
      f"jump {sl_a - sl_b:+.2e}", abs(sl_a - sl_b) < 1e-6)
# value layer kink at theta = c+d has mass -b*2 = -4 (slope 2 -> 0):
sl_b = (Phi2(c + d) - Phi2(c + d - h)) / h
sl_a = (Phi2(c + d + h) - Phi2(c + d)) / h
check("E-visible-wall", "a=b: Phi slope jumps 2 -> 0 at theta=3",
      f"jump {sl_a - sl_b:+.6f}", abs((sl_a - sl_b) + 2.0) < 1e-3)
# flux layer under v1-preference keeps the kink at theta=c (a=b regime,
# where the kink is a tie-break choice, not a forced vertex switch):
sl_b = (fluxes(c, "v1", a2, a2)[1] - fluxes(c - h, "v1", a2, a2)[1]) / h
sl_a = (fluxes(c + h, "v1", a2, a2)[1] - fluxes(c, "v1", a2, a2)[1]) / h
check("E-flux-kink-stays", "v1-first tie-break: v1 kinks at theta=c",
      f"jump {sl_a - sl_b:+.6f}", abs((sl_a - sl_b) + 1.0) < 1e-3)
# under v2-preference the kink moves to theta=d (not c), a=b regime:
sl_b = (fluxes(d, "v2", a2, a2)[2] - fluxes(d - h, "v2", a2, a2)[2]) / h
sl_a = (fluxes(d + h, "v2", a2, a2)[2] - fluxes(d, "v2", a2, a2)[2]) / h
check("E-kink-moves", "v2-first tie-break: v2 kinks at theta=d=2",
      f"jump {sl_a - sl_b:+.6f}", abs((sl_a - sl_b) + 1.0) < 1e-3)
# v1 under v2-preference is 0 until theta=d then theta-d (kink at d):
sl_b = (fluxes(d, "v2", a2, a2)[1] - fluxes(d - h, "v2", a2, a2)[1]) / h
sl_a = (fluxes(d + h, "v2", a2, a2)[1] - fluxes(d, "v2", a2, a2)[1]) / h
check("E-kink-moves-v1", "v2-first tie-break: v1 activates at theta=d",
      f"jump {sl_a - sl_b:+.6f}", abs((sl_a - sl_b) - 1.0) < 1e-3)

out = {"n_pass": sum(c["status"] == "PASS" for c in checks),
       "n_fail": sum(c["status"] == "FAIL" for c in checks),
       "checks": checks}
with open(f"{DL}/v17_worked_example_verification.json", "w") as f:
    json.dump(out, f, indent=1)
print(f"\n{out['n_pass']} PASS / {out['n_fail']} FAIL -> "
      f"{DL}/v17_worked_example_verification.json")
