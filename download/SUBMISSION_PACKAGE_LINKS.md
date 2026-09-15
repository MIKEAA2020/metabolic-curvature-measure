# Submission Package Links — Two-Paper Package

Generated 2026-09-15 (six-axis round). All repository links follow
the repo/blob/main pattern verified live in the 2026-09-03 pass; journal
links verified against the official journal or society pages. Repository
is public, so every link is directly accessible.

Revision note (2026-09-14): main is now `journal_manuscript_v4.tex`
(28 pp) and the companion is `companion_categorical_v3.tex` (70 pp).
The companion implements the eight-item repair set of the external
audit's synthesized ledger (one optic formalism, corrected
optic-colimit scope, one Hordijk-Steel catalysis condition, gluing
hypothesis alignment, Lévy-area normalization, enlarged contraction
box, battery-table consistency, restricted envelope domination),
restores the six audit-mandated citations (Hirota, Segura, Dittrich,
Handorf, Becker, Bravetti), and adds the external-data closures
(Keio E12/E15/E16; the COT/NE structural benchmark). The main paper
carries the four line-level corrections of its cross-check (bridge
sentence softened, generic-weights uniqueness step, semiconvexity
law, label/title fixes) plus the selection-rule count harmonization;
its figure directory is renamed `association_robustness/` (was
`association_robustness/`).

Revision note (2026-09-14, second perturbation probe round): the
companion adds the oxygen-limited medium probe (the second
perturbation axis, beyond the carbon-source correction): a four-
level dose response on iJO1366 (EX_o2_e at −10/−5/−2.5) plus the
cross-rebuild and non-degenerate anaerobic endpoint on iML1515
(−5 and 0). Labels are invariant at every non-anaerobic level in
both reconstructions (zero flips; κ = 1.000) with the association
degrading only gracefully (held-out AUC ≥ 0.971, 0.9999 at −10);
the anaerobic endpoint re-stratifies 7/1516 labels (lower
glycolysis + hemN gained; fabZ lost), and the iJO1366 anaerobic
zero-growth is disclosed as a model-level degeneracy. The abstract
promotes the medium-robustness finding (262 words).

Revision note (2026-09-14, third perturbation axis round): the
companion adds the nitrogen-source probe (the third medium axis):
an ammonium-limitation gradient (EX_nh4_e at −10/−5/−2.5 on
iJO1366; −2.5 on iML1515) plus full nitrogen-source substitution
(ammonium closed; sole donor L-glutamate at −10 — nitrogen flux
matched to the NH4 −10 level, both optima 0.9259 — or L-arginine
at −10, a four-nitrogen carbon co-substrate with optimum 1.2595,
28% above the glucose-minimal baseline). Labels are invariant along
the entire limitation gradient (289/289 and 286/286; zero flips;
κ = 1.000; WT down 76%); substitution re-stratifies exactly the
assimilation module, losses only (glutamate −5 iJO / −7 iML:
gltA, acnA, acnB, icd, amtB, + gltB/gltD on iML; arginine −14/−15:
those plus the eight arginine-biosynthesis genes and astC), every
rescue substitution-mediated (closing the donor returns all 41
backgrounds to zero growth). The plain-FBA association collapses on
the nitrogen-limited levels — diagnosed by at-optimum FVA
(phosphoglucose-isomerase range 45–177 vs 0.0 at baseline, 4.3
under oxygen limitation) as flux-solution degeneracy, not biology —
and canonical (parsimonious FBA) vertex selection restores it
everywhere (r ≥ +0.872, AUC ≥ 0.979; baseline sharpened
r +0.603 → +0.945). The abstract now carries the three-axis
medium-robustness statement (263 words, under the 265 cap).
audit_v7: 143/143 PASS. Companion 66 → 67 pp, 0 errors /
0 undefined / 0 overfull.

Revision note (2026-09-14, fourth axis + canonical-selection round):
the companion adds the phosphate-limitation probe (the fourth
medium axis, chosen over sulfur by a dose-response pre-screen:
baseline phosphate uptake 0.948/0.793 mmol/gDW/h gives a three-level
gradient spanning 47–89% growth reduction, where sulfur's 0.25
uptake compresses to one informative level). Labels are invariant
at every level in both reconstructions (289/289/289 on iJO1366,
286/286 on iML1515; zero flips; κ = 1.000) — the supply side of
the invariance claim is now closed on all four classical
macronutrient axes (carbon source, electron acceptor, nitrogen,
phosphate). The reported association statistics are homogenized
under canonical (parsimonious) vertex selection across all four
axes (new subsection with an 18-level table): canonical r in
[+0.87, +0.95], held-out AUC ≥ 0.979, labels κ = 1.000 at every
level, the baselines sharpened (iJO r +0.603 → +0.945; iML
+0.875 → +0.937), and the iML1515 anaerobic endpoint restored
across the regime switch itself (r +0.258 → +0.949) — the switch
moves labels only. The homogenization audit surfaced and corrected
eight solver-tolerance artifacts (all trace-quota genes — the
biotin and ubiquinone-side-chain drains scale with growth and fall
to 2–3×10⁻⁷ mmol/gDW/h at low optima, within ~2× of the simplex's
primal feasibility tolerance): the deposited anaerobic fabZ "loss"
(the corrected endpoint is 286 → 292, six gains, no losses; fabZ
is essential in every regime through OGMEACPD/OPMEACPD) and seven
calls at the phosphate −0.1 levels, all re-adjudicated with an
independent LP engine (HiGHS two-stage split-variable pFBA) and
cross-checked to 0 discrepancies in 24,282 gene-level comparisons
across 17 levels. The abstract now carries the four-axis
medium-robustness statement (264 words, under the 265 cap).
audit_v8: 226/226 PASS. Companion 67 → 70 pp, 0 errors /
0 undefined / 0 overfull.

Revision note (2026-09-15, sixth-axis round, merged): the companion
adds the non-medium ATPM-maintenance-stress probe (the
temperature-style surrogate, selected over proton-leak forcing by
pre-screen) with plain + canonical arms in both reconstructions, and
extends the trace-ququota integrity protocol to the new axis: six
corrupted calls at the -90% endpoints (plain fabZ/bioH iJO; plain
bioD/fabZ and canonical bioF/fabI iML) settled at biomass exactly
zero by the independent HiGHS engine and corrected -- the endpoint
re-stratification is purely one-directional (energy-transduction
gains only, atp/cyo/nuo operons, OXPHOS enriched eight-fold) and
the plain-vs-canonical arm agreement is kappa 1.000 at all seven
levels. The canonical-selection subsection gains the measured
near-tie boundary (iML ATPM L1 near-ties, dL1 1.2e-6 relative,
782/1129 compensables at the ~200.01 floor) and the sixth feature;
tab:canonical-selection extended to six axes; the nh4_-5 canonical
level restored (r +0.922). Companion 71 -> 73 pp, 0 errors / 0
undefined / 0 overfull; abstract six-axis, 264 words < 265;
audit_v10 271/271 PASS. New artifacts: keio_atpm_stress_e12/e16,
keio_atpm_pfba_control[_iml]_atpm_*, keio_atpm_stress_summary.txt,
keio_nonmedium_prescreen.json,
keio_atpm_integrity_adjudication.json,
keio_atpm_neartie_measurement.json, keio_floor_tolerance_check.json,
multiaxis_canonical_table.json/.txt,
keio_multiaxis_canonical_response.png (scripts
atpm_stress_keio_probe.py, atpm_integrity_adjudication.py,
atpm_integrity_fix.py, multiaxis_table.py, multiaxis_figure.py,
sixth_axis_artifacts.py; audit_v10_numbers.py).

Revision note (2026-09-15, fifth axis + arginine symmetry round): the
companion adds the iron-limitation probe (the trace-metal fifth
axis, chosen over zinc and manganese by a dose-response pre-screen;
iron pinned to the single ferrous channel, the ferric exchange
closed — the closure leaves the wild-type optimum unchanged to
solver noise): iJO1366 EX_fe2_e at −0.01/−0.005/−0.0025 (37/68/84%
WT reduction) and iML1515 at −0.005/−0.0025 (62/81%). The pre-screen
finds the iron dose response identical on both reconstructions to
six decimals (shared quota; b = fe2/0.0161) — the purest supply
axis of the battery. Labels are invariant at every level (289/289
and 286/286; zero flips; κ = 1.000); the plain-FBA statistics
collapse with the degeneracy signature (PGI FVA width up to 192;
plain r down to −0.037) and canonical vertex selection restores
them everywhere (r +0.800 to +0.957, AUC 0.986–0.988, MCC
0.904–0.965). The arginine-substitution levels re-run under
canonical selection complete the axis × selection table symmetry
(25 levels; iJO +0.802 → +0.953, iML +0.915 → +0.850 with AUC
0.997 / MCC 0.993 — the plain reading was already well posed there,
so the declared rule is reported uniformly rather than
cherry-picked). Integrity: a cross-arm scan of the iron levels
(7,133 gene comparisons, max |Δb| 6×10⁻⁸, no false-viability-band
calls at WT 0.156, just above the 0.14 tolerance boundary); one
GLPK simplex hang (b0887, the cysteine/glutathione ABC-exporter
ATPase) disclosed and settled by the HiGHS engine with the row
marked as an engine substitution; a patch-F rendering defect
(double-escaped \emph / \S\ref commands) caught and fixed.
audit_v9: 251/251 PASS. Companion 70 → 71 pp, 0 errors / 0
undefined / 0 overfull.

- Repository: https://github.com/MIKEAA2020/metabolic-curvature-measure
  (renamed 2026-09-03 from the earlier internal name; GitHub redirects
  the old URLs, but the links below already use the new name)
- Blob links open the GitHub file viewer (PDFs render in-browser; "Download"
  button on the right of each viewer page). Raw links download directly.

---

## Paper 1 (Main) — Bulletin of Mathematical Biology

**Title:** A Measure-Theoretic Discrete Curvature Framework for Metabolic Gene
Sensitivity: From Active-Set Geometry to Transcriptional Response
(Original Research Article; 28 pp; subscription route — no author charges).


### Journal / submission-portal links (all verified)

| Resource | Link |
|---|---|
| Journal home (Springer) | https://link.springer.com/journal/11538 |
| Submission guidelines | https://link.springer.com/journal/11538/submission-guidelines |
| How to publish with us | https://link.springer.com/journal/11538/how-to-publish-with-us |
| Submission portal (Editorial Manager) | https://www.editorialmanager.com/bmab |
| Society page (SMB, official journal of the society) | https://smb.org/Bulletin-of-Mathematical-Biology |

> Portal code verified as **bmab** (via the SMB society page and multiple
> journal directories). Do not confuse with `editorialmanager.com/jomb`,
> which is the *Journal of Mathematical Biology* — a different Springer journal.

### Package files (GitHub)

| Item | View (blob) | Direct download (raw) |
|---|---|---|
| **One-file upload ZIP (compile-ready)** | — | [download/submission_main_bmb.zip](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/submission_main_bmb.zip) |
| Manuscript PDF (28 pp, full proofs in appendices, declarations in backmatter) | [download/journal_manuscript_v4.pdf](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/journal_manuscript_v4.pdf) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/journal_manuscript_v4.pdf) |
| Cover letter (with declarations, companion disclosure) | [download/cover_letter_bmb.md](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/cover_letter_bmb.md) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/cover_letter_bmb.md) |
| LaTeX source | [scripts/journal_manuscript_v4.tex](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/scripts/journal_manuscript_v4.tex) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/journal_manuscript_v4.tex) |
| Reference list (BMB alphabetical, 27 entries) | [scripts/journal_manuscript_v3_bmb_refs.tex](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/scripts/journal_manuscript_v3_bmb_refs.tex) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/journal_manuscript_v3_bmb_refs.tex) |
| BibTeX database | [scripts/journal_manuscript_v2_refs.bib](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/scripts/journal_manuscript_v2_refs.bib) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/journal_manuscript_v2_refs.bib) |
| Reference-list generator (audit-checked) | [scripts/build_bmb_refs.py](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/scripts/build_bmb_refs.py) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/build_bmb_refs.py) |

Figures (embedded in the PDF; source PNGs if the portal requests separate files):

| Figure | Link |
|---|---|
| Fig. M1 summary (active-set sweep) | [download/m1_m3/fig_m1_summary.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/m1_m3/fig_m1_summary.png) |
| Coupling figures (Alexandrov bridge) | [download/alexandrov_bridge/coupling_figures.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/alexandrov_bridge/coupling_figures.png) |
| E24 recalibration | [download/association_robustness/v5_e24_recalibration.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/association_robustness/v5_e24_recalibration.png) |
| V7 path robustness | [download/association_robustness/v7_path_robustness.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/association_robustness/v7_path_robustness.png) |
| V8 tie-break robustness (E-V8) | [download/association_robustness/v8_tiebreak_robustness.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/association_robustness/v8_tiebreak_robustness.png) |
| E32 event-measure stabilization | [download/association_robustness/e32_event_measure_stabilization.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/association_robustness/e32_event_measure_stabilization.png) |

Build note: for Overleaf or any standalone compiler, upload **the ZIP** (it
contains the .tex, the input'ed reference list, the .bib database, and all
six figures at the exact relative subpaths the .tex expects — verified to
compile standalone, 28 pp, 0 errors). If instead you upload individual
files, upload them together with `journal_manuscript_v3_bmb_refs.tex` and
the three figure subfolders (`m1_m3/`, `alexandrov_bridge/`,
`association_robustness/`) so the paths resolve; the .tex now searches both the
upload directory and the repository layout
(`\graphicspath{{./}{../download/}}`).

---

## Paper 2 (Companion) — Theory and Applications of Categories

**Title:** Stratified Connections, Optic Composition, and the Homotopy
Fixed-Point Extension: A Categorical Framework for Viability-Weighted
Curvature (Research Article; 71 pp; electronic-only, free — no author charges).

### Journal / submission links (all verified)

| Resource | Link |
|---|---|
| Journal home | http://www.tac.mta.ca/tac/ |
| Author information (format for submission) | http://www.tac.mta.ca/tac/authinfo.html |
| Editorial board / general info | http://www.tac.mta.ca/tac/geninfo.html |
| Managing Editor contact | tac@mta.ca |

Submission route (from the official author information, fetched and verified):
submit the article as **a PDF compiled from TeX source to any member of the
Editorial Board except the Managing Editor or TeXnical editors**, copying
every submission to the Managing Editor at **tac@mta.ca**; an article may be
submitted to only one Editor; TeX source plus a compiled PDF are required
only after acceptance.

### Package files (GitHub)

| Item | View (blob) | Direct download (raw) |
|---|---|---|
| **One-file upload ZIP (compile-ready)** | — | [download/submission_companion_tac.zip](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/submission_companion_tac.zip) |
| Manuscript PDF (73 pp, + sixth-axis revision: prop:keio-atpm + rem:keio-multiaxis -- the non-medium ATPM-maintenance-stress probe with the trace-quota integrity corrections (six HiGHS-adjudicated calls; endpoint re-stratification purely one-directional) and the measured near-tie boundary in the canonical-selection subsection (now a six-axis, 32-row table), plus the restored nh4_-5 canonical level -- on top of the fifth-axis/arginine-symmetry revision: prop:keio-iron + rem:keio-iron-invariance -- the trace-metal axis closing the supply side across all five classical nutrient classes, the arginine-substitution canonical levels completing the axis x selection table symmetry -- on top of the fourth-axis/canonical-selection revision: prop:keio-phosphate + rem:keio-p-invariance + the canonical-selection subsection with the solver-tolerance integrity disclosures, the nitrogen-axis, oxygen-probe, glucose-only, viability-kernel + Poincare/averaging, 3rd-wave repair, and restoration revisions) | [download/companion_categorical_v3.pdf](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/companion_categorical_v3.pdf) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/companion_categorical_v3.pdf) |
| Cover letter | [download/cover_letter_tac.md](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/cover_letter_tac.md) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/cover_letter_tac.md) |
| LaTeX source | [scripts/companion_categorical_v3.tex](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/scripts/companion_categorical_v3.tex) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/companion_categorical_v3.tex) |

Figures (embedded in the PDF; source PNGs):

| Figure | Link |
|---|---|
| Per-optic Lipschitz constants | [download/lipschitz_constants_per_optic.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/lipschitz_constants_per_optic.png) |
| CPTP Zeno contraction | [download/cptc_zeno_contraction.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/cptc_zeno_contraction.png) |
| Inverse-limit RAF Hasse diagram | [download/inverse_limit_raf_hasse.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/inverse_limit_raf_hasse.png) |
| Extended Hasse diagram | [download/inverse_limit_raf_extended_hasse.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/inverse_limit_raf_extended_hasse.png) |
| Claim F holonomy (commuting-control test) | [download/claim_f_holonomy_plot.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/claim_f_holonomy_plot.png) |
| Claims A--E in the n=4 non-abelian regime | [download/claims_ae_n4_nonabelian.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/claims_ae_n4_nonabelian.png) |
| Claim D heavy-tail stress test | [download/claim_d_heavytail_stress.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/claim_d_heavytail_stress.png) |
| Levy 3/2 derivation (exact kernel constant) | [download/levy_stable_3half_derivation.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/levy_stable_3half_derivation.png) |
| Claim G Zeno scaling | [download/claim_g_zeno_plot.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/claim_g_zeno_plot.png) |
| T-iteration convergence | [download/t_iteration_convergence_plot.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/t_iteration_convergence_plot.png) |
| T-iteration robustness (axis-aligned) | [download/t_iteration_robustness_extension_axis_aligned.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/t_iteration_robustness_extension_axis_aligned.png) |
| T-iteration robustness (rotated) | [download/t_iteration_robustness_extension_rotated.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/t_iteration_robustness_extension_rotated.png) |

---

## Supporting documentation (GitHub)

| Item | Link |
|---|---|
| Two-paper submission package evaluation | [download/Two_Paper_Submission_Package_Evaluation.md](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/Two_Paper_Submission_Package_Evaluation.md) |
| Declarations & final scan evaluation | [download/Declarations_and_Final_Scan_Evaluation.md](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/Declarations_and_Final_Scan_Evaluation.md) |
| Journal submission pass evaluation | [download/Journal_Submission_Pass_Evaluation.md](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/Journal_Submission_Pass_Evaluation.md) |
| Package-repo browsing: `download/` directory | https://github.com/MIKEAA2020/metabolic-curvature-measure/tree/main/download |
| Package-repo browsing: `scripts/` directory | https://github.com/MIKEAA2020/metabolic-curvature-measure/tree/main/scripts |

---

## Pre-submission checklist (already resolved / remaining)

Resolved: BMB-formatted main paper (natbib author-year, 27 alphabetical refs,
keywords, declarations in backmatter, cover letter with companion disclosure);
self-contained TAC companion (no v21 pointers, proof statuses labeled, cover
letter); zero cross-paper verbatim prose overlap; 98/98 audit checks PASS;
no-fee venue for both.

Remaining at submission time: fill the cover-letter `[Submission date]`
placeholders; replace the sole-author placeholder "X" with the real author
name at all authorship sites (title blocks, pdfauthor, bib entries, cover
letters); select the receiving Editorial Board member for TAC (from
geninfo.html); register/log in at the BMB Editorial Manager portal.

Repository rename COMPLETED (2026-09-03): the repository is now
`metabolic-curvature-measure`; the URL string has been updated in both
manuscripts (Data Availability), both cover letters, and this document.

Formal cleanup executed (2026-09-02): all "Artifact: ... .png/.json"
caption lines removed (source-data linkage now carried by the Data
Availability statement); all internal experiment codes (E-V5, M4b, V8,
Route 5, RC6, BT1, D-N1...), bracketed block tags, changelog/diary
references to predecessor versions, and self-commentary wording removed
from both papers; the Reproducibility and counts-appendix sections were
reworded to formal conventions; the audit passes 98/98 after the edits
(main then 21 pp, companion 35 pp, 0 errors, 0 undefined refs).

Restoration revision executed (2026-09-03), on new frozen-lineage files
(journal_manuscript_v3.tex + journal_manuscript_v3_bmb_refs.tex;
companion_categorical_v3.tex — the v2 main and v1 companion are frozen
and untouched at tag manuscript-v2-final): full proofs for every main-
paper result (two long technical proofs in a second appendix, textbook
material cited); companion restoration of the lost empirical battery —
Claims F/G verdicts, the n=4 non-abelian regime, the Claim D heavy-tail
stress test, the Levy 3/2 derivation REPAIRED to the exact kernel
constant C_fat = sqrt(5 nu)/2 (verified against the frozen Monte-Carlo
data to 1.5%; the figure regenerated with the corrected theoretical
curve), the CPTP-Zeno lift with the Holevo ensemble correction, the
375-configuration contraction battery, the P4-repaired smooth-envelope
chain, the terminal-coalgebra characterization of the maximal RAF
(deflationary closure operator, full proof in the appendix, the
functorial-realization statement demoted to a conjecture), and the
network closure-test battery (A--K summary, RAF-to-Zeno transfer bound,
persistent-homology Phase III test, fixed-model essentiality validation
at kappa = 0.835). Main then 27 pp, companion 57 pp; both compiled with
0 errors and 0 undefined refs; the v3 audit passed 98/98; every
restored number was artifact-traced; ZIPs rebuilt and standalone-
reverified. Remaining script-name mentions in the companion were
formalized to deposited-artifact conventions.

3rd-wave repair round executed (2026-09-14), on new frozen-lineage
files (journal_manuscript_v4.tex; companion_categorical_v3.tex — the
v3 main and v2 companion are frozen and untouched): the companion
implements the external audit's eight-item repair set (one optic
formalism via Riley pairs + a strict feedback representative form;
the optic-colimit theorem restated in corrected scope — Set-level
union, adapter-level (colimit, limit) form, general case open; one
Hordijk-Steel catalysis condition via the food-closure across
definition, operator, and appendix; the gluing hypothesis aligned
with the (O3) gauge transform and the piecewise-F remainder
relabeled O(eps^2); the Levy-area normalization corrected to
Var(X2) = 1/4 with the fluctuation-language restatement of Claims
C/D; the contraction box enlarged to [-1.5, 1.5]^d with K
instantiated; the battery table/AcCoA remark made consistent
(conversions at H and I, not G) and the step-(v) protocol gap
disclosed; the envelope domination restricted to active
surrogates), restores the six audit-mandated citations (Hirota,
Segura, Dittrich, Handorf, Becker, Bravetti; plus Bousfield-Kan),
and adds the external-data closures: the Keio anchor (E12
transitive, E15 direct, E16 cross-rebuild, with the medium-audit
note) and the COT/NE structural benchmark (E14). The main paper
carries the four line-level corrections of the cross-check plus
framing edits, and its figure directory is renamed
association_robustness/. Main now 28 pp, companion 65 pp; both
compile with 0 errors and 0 undefined refs; the v5 audit passes
110/110 (the v4 audit's 98 plus the 12 new Keio-section checks); the RAF enumeration was re-verified under the corrected
catalysis condition (16 RAFs / 21 inclusions / R_max unchanged);
ZIPs rebuilt as the v4 round and standalone-reverified (28 / 65
pp).

Follow-up round (same files, amended in place on the live heads;
frozen lineage untouched): the glucose-only Keio re-run executed
with the trehalose exchange closed as the sole change — both
in-silico essentiality sets unchanged (289/1367 and 286/1516, zero
label changes), every rank-level association strengthened (E12
Pearson 0.370→0.603, held-out AUC 0.953→0.977, MCC 0.719→0.882;
E15 Pearson 0.085→0.230, AUC 0.713→0.737), and the E16
cross-rebuild negative verdict reversed as a medium artifact
(Pearson −0.018→+0.376, AUC 0.428→0.813) — plus the T7b
viability-kernel bridge (closure test as a finite-time,
feedback-certifying probe of kernel/capture-basin membership) and
the T7c Poincare/averaging bridge (occupation fraction as a
phase-invariant orbit statistic); companion 63→65 pp, 0 errors/0
undefined/0 overfull; audit_v5 110/110 PASS; new artifacts
download/keio_glucose_only_e12/e15/e16 (csv/txt/json/png).

Second-probe round (same files, amended in place on the live heads;
frozen lineage untouched): the oxygen-limited medium probe executed
on the electron-acceptor axis (glucose-only medium retained, EX_o2_e
tightened) — iJO1366 dose response at −10/−5/−2.5 with wild-type
optima 0.711/0.491/0.367 (overflow, then fermentation physiology) and
289/1367 essential at every level (zero label changes, κ = 1.000;
calibration r +0.775/+0.607/+0.519, held-out AUC 0.9999/0.980/0.971,
MCC 0.993/0.939/0.887, P@200 = 1.0 at −10); iML1515 at −5 (WT 0.353,
286/1516 unchanged, r +0.559, AUC 0.994, direct AUC 0.818) and at
the anaerobic endpoint 0 (WT 0.134): 286→291 labels (+6/−1: eno,
pgk, gapA, gpmA, gpmM, hemN gained; fabZ lost; κ = 0.985, 5/7 flips
glycolysis-enriched), calibration r +0.260/AUC 0.672, direct
+0.118/AUC 0.673, model gaps unchanged at 13; the iJO1366 anaerobic
zero-growth disclosed as a model-level degeneracy (OPHHX + PDX5POi
lack anaerobic alternatives in that reconstruction; 0.01 mmol/gDW/h
O₂ restores 0.231; iML1515 carries the O₂-free OPHHX3 route);
landed as prop:keio-o2-limited + rem:keio-o2-invariance; abstract
promoted to the medium-robustness statement (262 words < 265);
companion 65→66 pp, 0 errors/0 undefined/0 overfull; audit_v6
125/125 PASS (the v5 audit's 110 plus 15 new O2 checks; two
rounding defects found and fixed: iML −5 AUC 0.995→0.994, WT
reduction 62%→63%); new artifacts download/keio_o2_limited_e12/
e16 (sweep csv + results json), keio_o2_limited_summary.txt,
keio_o2_limited_dose_response.png, keio_o2_anaerobic_diagnostic.json
(scripts o2_limited_keio_probe.py + o2_anaerobic_diagnostic.py).
