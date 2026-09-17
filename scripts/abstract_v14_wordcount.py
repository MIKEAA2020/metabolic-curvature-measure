#!/usr/bin/env python3
"""Word-count calibration for the v14 abstract (Gemini-register trim, cap 255).

Counts with the EXACT method used by the audit's JP-3 gate: tokens matching
[A-Za-z0-9\\-]+ after stripping \\commands from the abstract body.
Author-imposed cap for v14: <= 255 audit-style words.
"""
import re

BASE = "/home/z/my-project/metabolic-curvature-measure/scripts/"


def count(abstract_body: str) -> int:
    stripped = re.sub(r"\\[a-zA-Z]+", " ", abstract_body)
    return len(re.findall(r"[A-Za-z0-9\-]+", stripped))


def rendered_count(abstract_body: str) -> int:
    """Rough rendered-words estimate: collapse math to single pseudo-words."""
    s = re.sub(r"\$[^$]*\$", " MATH ", abstract_body)
    s = re.sub(r"\\[a-zA-Z]+", " ", s)
    s = re.sub(r"[^A-Za-z0-9\- ]", " ", s)
    return len([t for t in s.split() if t])


# CURRENT = the live v13 abstract, extracted from the file (exact baseline)
v13 = open(BASE + "journal_manuscript_v13.tex").read()
CURRENT = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", v13, re.S).group(1)

# ---- Draft A: four register-safe cuts (Gemini-side redundancy only) ----
#   A1 "boundaries where the network switches between active constraint sets"
#      -> "boundaries between active constraint sets"        (in-words gloss kept)
#   A2 "in every boundary-crossing sweep" dropped (the 93.4-100.0% range
#      already encodes the sweep variability; Gemini's sentence ends here)
#   A3 "fails in general" -> "fails generically"  (Gemini's exact word)
#   A4 "robust to the tie-breaking convention and to random-panel sampling"
#      -> "robust to tie-breaking convention and random-panel sampling"
#   A5 "evaluated" dropped (Gemini: "across 424 metabolic genes")
DRAFT_A = r"""
\noindent
When a cell's environment changes, its metabolic network reroutes.
Parametric flux balance analysis defines a continuous, piecewise-affine
mapping from environmental and genetic constraints to optimal fluxes.
We measure how this map bends. Its distributional second derivative
is a matrix-valued Radon measure concentrated on the boundaries
between active constraint sets --- the discrete curvature carrier of
rerouting geometry. Parameter loops accumulate drift linearly in loop
size (slope $1.00$; smooth maps scale quadratically), and $93.4$--$100.0\%$
of second-order response mass concentrates on active-set transitions.
We establish a refinement--resolution bridge to classical differential
geometry: under mesh refinement the measure converges weakly to the
smooth curvature density, dual-cell reconstructions converge strongly
in $L^1$, and total-variation convergence fails generically. A
resolution parameter $\sigma$ delineates the discrete and smooth
regimes across the measured window $h \ll \sigma \ll L_{\mathrm{var}}$
($h$: mesh scale; $L_{\mathrm{var}}$: smooth-variation scale).

From this measure we derive a gene-level sensitivity metric, $\kmu$.
In \emph{E.~coli} (M3D compendium, $n = 424$ genes), $\kmu$ predicts
transcriptional response to carbon depletion ($r = +0.395$,
$p = 2.6 \times 10^{-17}$; partial $r = +0.269$ controlling for
baseline expression). The association is robust to tie-breaking
convention and random-panel sampling. Strikingly, it vanishes at
the protein layer ($r = -0.083$ across $366$ genes in matched
quantitative proteomics): cells transcribe rerouting potential while
buffering its translation. Finally, double-knockout epistasis mirrors
active-set footprint overlap ($\rho_S = 0.865$), and cyclical genotype
modifications induce permanent phenotypic memory: $66\%$ of loops fail
to revert. Our results unify multi-parametric linear programming,
discrete differential geometry, and transcriptional regulation into
one predictive framework.
"""

# ---- Draft F (CHOSEN): A + four more zero/near-zero-drift trims ----
#   F6 "$n = 424$" -> "$424$"      (Gemini: "across 424 metabolic genes")
#   F7 "delineates the discrete and smooth regimes"
#      -> "delineates discrete and smooth regimes"        (article drop)
#   F8 "across the measured window" -> "across the window"
#   Keeps: "Finally,", "matched quantitative proteomics" (Gemini's exact
#   phrase), both h/L_var in-words glosses, and every number.
DRAFT_F = DRAFT_A
DRAFT_F = DRAFT_F.replace("(M3D compendium, $n = 424$ genes)",
                          "(M3D compendium, $424$ genes)")
DRAFT_F = DRAFT_F.replace("delineates the discrete and smooth",
                          "delineates discrete and smooth")
DRAFT_F = DRAFT_F.replace("across the measured window",
                          "across the window")

if __name__ == "__main__":
    print(f"current v13 abstract : {count(CURRENT)} words (audit-style), "
          f"~{rendered_count(CURRENT)} rendered")
    for name, d in [("A", DRAFT_A), ("F", DRAFT_F)]:
        c, r = count(d), rendered_count(d)
        verdict = "OK  (<= 255)" if c <= 255 else "OVER"
        print(f"draft {name}            : {c} words (audit-style), "
              f"~{r} rendered  -> {verdict}")
    print("cap                  : author directive v14 <= 255")
