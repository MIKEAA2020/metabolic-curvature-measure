#!/usr/bin/env python3
"""Word-count calibration for the v13 abstract (Gemini-faithful adoption).

Counts with the EXACT method used by audit_v20_numbers.py JP-3:
tokens matching [A-Za-z0-9\\-]+ after stripping \\commands from the
abstract body.  Hard audit cap: <= 300.  Project/BMB guideline: <= 250.
"""
import re
import sys

def count(abstract_body: str) -> int:
    stripped = re.sub(r"\\[a-zA-Z]+", " ", abstract_body)
    return len(re.findall(r"[A-Za-z0-9\-]+", stripped))

CURRENT = r"""
When a cell's environment changes, its metabolic network reroutes: the
optimal fluxes move, and the map from environment to optimum is
piecewise linear, not smooth. We measure how this
map bends. Its second derivative, taken in the sense of distributions,
is a matrix-valued Radon measure concentrated on the boundaries
where the network switches between active constraint sets --- the
discrete curvature carrier of the network's
rerouting geometry. Parameter loops accumulate drift linearly in loop
size (measured slope $1.00$; a smooth map would scale
quadratically), and $93.4$--$100.0\%$ of second-order response mass
lands on active-set switches in every boundary-crossing sweep. Under
mesh refinement the atomic measure converges weakly to the smooth
curvature density and the dual-cell reconstruction converges strongly
in $L^1$, while total-variation convergence fails in general; a
resolution parameter $\sigma$ separates the discrete and smooth regimes
through the measured window $h \ll \sigma \ll L_{\mathrm{var}}$
($L_{\mathrm{var}}$: smooth variation scale). From the measure we derive a
gene-level sensitivity metric $\kmu$. On \emph{E.~coli} (M3D
microarray compendium, $n=424$ evaluated genes), it predicts
carbon-depletion transcriptional
response ($r = +0.395$, $p = 2.6 \times 10^{-17}$; partial $r = +0.269$
with reference-level control); the association is robust to the
tie-breaking convention and to random-panel sampling. It does not
propagate to the protein layer: cells transcribe rerouting potential
while buffering its translation. Double-knockout epistasis aligns with active-set
structure ($\rho_S = 0.865$), and genotype loops close with
phenotypic memory ($66\%$ non-reverting). The framework unifies the
atomic measure, its smooth coarse-grainings, and its trajectory
integrals as one object at different
resolutions.
"""

DRAFT = r"""
When a cell's environment changes, its metabolic network reroutes.
Parametric flux balance analysis defines a continuous, piecewise-affine
mapping from environmental and genetic constraints to optimal fluxes.
We measure how this map bends. Its distributional second derivative
is a matrix-valued Radon measure concentrated on the boundaries where
the network switches between active constraint sets --- the discrete
curvature carrier of rerouting geometry. Parameter loops accumulate
drift linearly in loop size (slope $1.00$; smooth maps scale
quadratically), and $93.4$--$100.0\%$ of second-order response mass
concentrates on active-set transitions in every boundary-crossing
sweep. We establish a refinement--resolution bridge to classical
differential geometry: under mesh refinement the measure converges
weakly to the smooth curvature density, dual-cell reconstructions
converge strongly in $L^1$, and total-variation convergence fails in
general. A resolution parameter $\sigma$ delineates the discrete and
smooth regimes across the measured window $h \ll \sigma \ll
L_{\mathrm{var}}$ ($h$: mesh scale; $L_{\mathrm{var}}$:
smooth-variation scale).

From this measure we derive a gene-level sensitivity metric, $\kmu$.
In \emph{E.~coli} (M3D compendium, $n = 424$ evaluated genes), $\kmu$
predicts transcriptional response to carbon depletion ($r = +0.395$,
$p = 2.6 \times 10^{-17}$; partial $r = +0.269$ controlling for
baseline expression). The association is robust to the tie-breaking
convention and to random-panel sampling. Strikingly, it vanishes at
the protein layer ($r = -0.083$ across $366$ genes in matched
quantitative proteomics): cells transcribe rerouting potential while
buffering its translation. Finally, double-knockout epistasis mirrors
active-set footprint overlap ($\rho_S = 0.865$), and cyclical genotype
modifications induce permanent phenotypic memory: $66\%$ of loops fail
to revert. Our results unify multi-parametric linear programming,
discrete differential geometry, and transcriptional regulation into
one predictive framework.
"""

if __name__ == "__main__":
    print(f"current v12 abstract : {count(CURRENT)} words (audit-style)")
    print(f"draft v13 abstract   : {count(DRAFT)} words (audit-style)")
    print(f"caps                 : audit<=300, guideline<=250")
