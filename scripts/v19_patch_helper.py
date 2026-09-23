#!/usr/bin/env python3
"""One-off: patch the NEW_ABSTRACT block (word-cap trim) and remove the
no-op audit-count placeholder edit in v19_comprehension_restructure.py."""
import io

P = "/home/z/my-project/metabolic-curvature-measure/scripts/v19_comprehension_restructure.py"
src = open(P).read()

lines = src.split("\n")
start = next(i for i, l in enumerate(lines)
             if l.startswith("NEW_ABSTRACT = "))
end = next(i for i, l in enumerate(lines)
           if lines[i] == '"""' and i > start)

new_abs = [
    'NEW_ABSTRACT = """When nutrients change, cells reroute metabolism through alternative',
    'pathways, and control must act at the switching points. Flux balance',
    'analysis (FBA) predicts metabolic states by solving linear',
    'optimization problems; as nutrient and enzyme capacities vary, the',
    'optimal response is piecewise linear, and ordinary curvature vanishes',
    'almost everywhere. Here we show that the true curvature of the',
    'optimal flux map is not a function but a discrete, matrix-valued',
    'measure concentrated on the boundaries where the active constraint',
    'set switches; in genome-scale \\\\emph{E.~coli} models, $93.4$--$100.0\\\\%$',
    'of the second-order response concentrates at these transitions.',
    'Integrating the measure along physiological paths assigns each enzyme',
    'a parameter-free rerouting burden, $\\\\kmu$. In carbon-starved',
    '\\\\emph{E.~coli}, $\\\\kmu$ predicts transcriptional induction across',
    '$424$ genes ($r = +0.395$, $p = 2.6 \\\\times 10^{-17}$); induced genes',
    'sit in operons of global carbon and energy regulons, and the',
    'rerouting mass concentrates on the fork metabolites of central carbon',
    'metabolism. The association survives five tie-breaking protocols and',
    'multiple stress axes, yet vanishes at the protein layer',
    '($r = -0.083$, $366$ genes, matched proteomics): cells transcribe',
    'standby capacity for rerouting while buffering translation.',
    'Cyclic-perturbation memory --- $66\\\\%$ of closed cycles fail to',
    'revert, with path-dependent drift scaling linearly in loop size',
    '(slope $1.00$) where smooth systems scale quadratically --- must live',
    'in fast post-translational state. Double-knockout epistasis mirrors',
    'active-set boundary overlaps ($\\\\rho_S = 0.865$). The framework',
    'unites linear programming, discrete geometry, and transcriptional',
    'regulation into a predictive foundation for metabolic systems',
    'biology.',
    '"""',
]
lines[start:end + 1] = new_abs
src = "\n".join(lines)

# remove the no-op audit-count placeholder edit block
noop = '''# (patched to the final audit count by v19_set_audit_count.py after
#  audit_v27 runs; initialized to the carried 344 figure)
rep("described under Reproducibility\\n($344$ checks).",
    "described under Reproducibility\\n($344$ checks).".replace(
        "344", "344"),
    "methods: audit count placeholder 1 (patched post-audit)")
'''
if noop in src:
    src = src.replace(noop, "# (the two '$344$ checks' mentions in Methods are patched to the final\n"
                            "#  audit_v27 count by scripts/v19_set_audit_count.py after the audit\n#  runs)\n")
    print("noop placeholder edit removed")
else:
    print("noop placeholder block not found (already removed?)")

open(P, "w").write(src)
print("patched NEW_ABSTRACT block:", start + 1, "-", end + 1)
