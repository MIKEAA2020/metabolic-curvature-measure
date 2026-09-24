#!/bin/bash
# Build self-contained, compile-ready submission ZIPs for the v27 round
# (V22/V15 Zenodo-archive round):
# main = journal_manuscript_v22.tex (NEW versioned file from v21 via
#   scripts/v22_v15_zenodo_doi.py): the Data, Software, and Code
#   Availability statement now records the archival deposit of the
#   compile-ready submission package on Zenodo (version DOI
#   10.5281/zenodo.22941018; the deposited file is the v26 submission
#   ZIP, MD5 8e7e367183a8f84493e65796bc7ebad4, CC-BY 4.0, concept DOI
#   10.5281/zenodo.22941017), the reference-list \input pointer
#   retargeted to journal_manuscript_v22_dam_refs.tex, and the two
#   Reproducibility count sites refreshed to the v32 audit ledger
#   (372).
# companion = companion_categorical_v15.tex (NEW versioned file from
#   v14 via the same script): the Data and code availability paragraph
#   now records its Zenodo archive (version DOI
#   10.5281/zenodo.22940820; the deposited file is the v26 submission
#   ZIP, MD5 6fa2d8d08386daeef563328fdfafad63, CC-BY 4.0, concept DOI
#   10.5281/zenodo.22940819), the \bibliography pointer retargeted to
#   companion_refs_v15.bib, and the header's application-paper pointer
#   refreshed to the v22 file.
# v21/v14 and all earlier versions untouched.
# Changes vs build_submission_zips_v26.sh:
#   - Main: v21 -> v22 (Zenodo DOI in the availability statement +
#     count refresh to 372).
#   - Companion: v14 -> v15 (Zenodo DOI in the availability paragraph).
#   - All numerical claims re-verified: audit_v32_numbers.py 372/372
#     PASS (v31 ledger carried + 6 V22 gates, incl. byte-exact
#     minimal-diff reverse verification); tectonic main 37 pp /
#     companion 76 pp, 0 errors / 0 '??'.
# Each ZIP verified by fresh-dir tectonic compile.
set -euo pipefail
cd /home/z/my-project/metabolic-curvature-measure

STAGE=scripts/overleaf_stage_v27
rm -rf "$STAGE"
mkdir -p "$STAGE/main" "$STAGE/companion"

# ---------- MAIN (Discover Applied Mathematics) ----------
M=$STAGE/main
cp scripts/journal_manuscript_v22.tex             "$M/"
cp scripts/journal_manuscript_v22_dam_refs.tex    "$M/"
cp scripts/journal_manuscript_v22_refs.bib        "$M/"
mkdir -p "$M/m1_m3" "$M/alexandrov_bridge" "$M/association_robustness"
cp download/m1_m3/fig_m1_summary.png                    "$M/m1_m3/"
cp download/alexandrov_bridge/coupling_figures.png      "$M/alexandrov_bridge/"
cp download/association_robustness/v5_e24_recalibration.png    "$M/association_robustness/"
cp download/association_robustness/v7_path_robustness.png      "$M/association_robustness/"
cp download/association_robustness/v8_tiebreak_robustness.png  "$M/association_robustness/"
cp download/association_robustness/e32_event_measure_stabilization.png "$M/association_robustness/"
cat > "$M/README.md" << 'EOF'
# Main manuscript — Discover Applied Mathematics (Springer Nature)
# Compile-ready standalone package

Title: A discrete curvature measure for flux balance analysis predicts
transcriptional regulation in Escherichia coli

## How to compile
- Overleaf: upload this ZIP via New Project -> Upload Project, set the main
  document to journal_manuscript_v22.tex, recompile. (Run twice so natbib
  citations resolve; Overleaf does this automatically.)
- Command line: pdflatex journal_manuscript_v22.tex  (x2)

## Contents
- journal_manuscript_v22.tex          main source (main document)
- journal_manuscript_v22_dam_refs.tex reference list (input by the main file)
- journal_manuscript_v22_refs.bib     underlying BibTeX database (not required
  for compilation; included for editorial source completeness)
- m1_m3/, alexandrov_bridge/, association_robustness/  figure PNGs at the
  exact relative paths used by \includegraphics

## Discover Applied Mathematics submission notes (submission guidelines,
## live-verified: link.springer.com/journal/44585/submission-guidelines)
- Submission system: Snapp (the journal's manuscript tracking system);
  article type: Research.
- Abstract: 245 words (journal cap: less than 250), a single narrative
  arc from the biological question to the findings.
- Keywords: 6 terms (flux balance analysis; metabolic rerouting;
  active-set curvature; transcriptional regulation; translational
  buffering; epistasis).
- Citations: numeric, in square brackets (natbib [numbers,sort&compress,
  square]), per the journal's reference style; figure captions and the
  in-text references use the journal's "Fig. 1" label form.
- Review model: single-anonymous (reviewers know the author identity);
  author name, affiliation, corresponding e-mail, and ORCID are on the
  title page; e-mail and ORCID are clickable.
- The CRediT authorship contribution statement, competing-interests,
  funding, generative-AI, and research-data declarations are in the
  manuscript backmatter; the cover letter
  (download/cover_letter_dam.md in the repository) carries the full
  disclosures. A cover letter is required by the journal's submission
  checklist.
- Continuous line numbering is enabled via the lineno package.
- All articles in the journal are published open access; per the
  journal's open-access information the article processing charge is
  covered by the publisher's current arrangement.
- Data availability: the complete bundle (generation scripts, result
  artifacts, genome-scale models, SHA-256 manifests, verification
  scripts) is at github.com/MIKEAA2020/metabolic-curvature-measure,
  and this submission package is archived on Zenodo at
  DOI 10.5281/zenodo.22941018 (CC-BY 4.0).
- v22 Zenodo-archive round: the availability statement records the
  archival DOI; the same-gene transcript correlation is quoted
  as +0.419 everywhere (one audited value), and the protein-layer
  robustness sentence names its provenance (the per-gene path metric);
  every numerical claim is unchanged and re-verified by the 372-check
  numeric audit (372/372 PASS).
EOF

# ---------- COMPANION (Discover Applied Mathematics) ----------
C=$STAGE/companion
cp scripts/companion_categorical_v15.tex    "$C/"
cp scripts/companion_refs_v15.bib       "$C/"
cp download/lipschitz_constants_per_optic.png   "$C/"
cp download/cptc_zeno_contraction.png           "$C/"
cp download/inverse_limit_raf_hasse.png         "$C/"
cp download/inverse_limit_raf_extended_hasse.png "$C/"
cp download/claim_f_holonomy_plot.png           "$C/"
cp download/claims_ae_n4_nonabelian.png         "$C/"
cp download/claim_d_heavytail_stress.png        "$C/"
cp download/levy_stable_3half_derivation.png    "$C/"
cp download/claim_g_zeno_plot.png               "$C/"
cp download/t_iteration_convergence_plot.png     "$C/"
cp download/t_iteration_robustness_extension_axis_aligned.png "$C/"
cp download/t_iteration_robustness_extension_rotated.png      "$C/"
cat > "$C/README.md" << 'EOF'
# Companion manuscript — Discover Applied Mathematics (Springer Nature)
# Compile-ready standalone package

Title: A Geometric and Category-Theoretic Theory of Viability: How
Sequential Adaptations Induce Path-Dependent Risk

## How to compile
- Overleaf: upload this ZIP via New Project -> Upload Project, set the main
  document to companion_categorical_v15.tex, recompile (pdflatex + bibtex +
  pdflatex x2; Overleaf runs this automatically).
- Command line:
    pdflatex companion_categorical_v15.tex
    bibtex   companion_categorical_v15
    pdflatex companion_categorical_v15.tex
    pdflatex companion_categorical_v15.tex

## Contents
- companion_categorical_v15.tex  main source (main document)
- companion_refs_v15.bib BibTeX database (required by \bibliography)
- 12 figure PNGs at the flat paths used by \includegraphics

## Discover Applied Mathematics submission notes (submission
## guidelines, live-verified: link.springer.com/journal/44585/
## submission-guidelines)
- Submission system: Snapp (the journal's manuscript tracking system);
  article type: Research.
- Abstract: 248 words (journal cap: less than 250), with the six-axis
  validation sentence covering all three body categories (regime
  switches and nitrogen-source substitution).
- Keywords: 6 terms (applied category theory; optic category;
  stratified connection; homotopy type theory; holonomy; viability
  theory); the AMS 2020 Subject Classification (18D05; 18N99; 92B05)
  is retained below the abstract.
- Citations: numeric, in square brackets (natbib [numbers,sort&compress,
  square]), per the journal's reference style; figure captions and the
  in-text references use the journal's "Fig. 1" label form (v14 aligned
  the companion with the main paper's convention).
- Review model: single-anonymous (reviewers know the author identity);
  author identity is on the paper.
- The cover letter (download/cover_letter_dam_companion.md in the
  repository) carries the disclosures; a cover letter is required by
  the journal's submission checklist.
- Data availability: the machine-verification scripts, numerical
  artifacts, and SHA-256 manifests are in the public repository
  github.com/MIKEAA2020/metabolic-curvature-measure, and this
  submission package is archived on Zenodo at
  DOI 10.5281/zenodo.22940820 (CC-BY 4.0).

## Relation to the application paper (v22 division of labor)
- The application paper (journal_manuscript_v22.tex, Discover Applied
  Mathematics target) is written in measure-theoretic terms alone;
  one Discussion paragraph records the division of labor and cites this
  paper for the constructions, machine verifications, and proofs at the
  status marked per result.
- This paper is self-contained for its own claims: all categorical
  definitions, constructions, and proofs live here (the application
  paper's former brief adapted statement of them was removed in its
  v19 comprehension restructure and is carried here alone).
EOF

# ---------- ZIP ----------
OUT=/home/z/my-project/metabolic-curvature-measure/download
rm -f "$OUT/submission_main_dam.zip" "$OUT/submission_companion_dam.zip"
(cd "$STAGE/main"      && zip -qr "$OUT/submission_main_dam.zip" .)
(cd "$STAGE/companion" && zip -qr "$OUT/submission_companion_dam.zip" .)
cd /home/z/my-project/metabolic-curvature-measure

# download PDF copies (byte-identical to the scripts builds)
cp scripts/journal_manuscript_v22.pdf download/journal_manuscript_v22.pdf
cp scripts/companion_categorical_v15.pdf download/companion_categorical_v15.pdf

echo "=== ZIP contents (main) ==="
unzip -l download/submission_main_dam.zip
echo "=== ZIP contents (companion) ==="
unzip -l download/submission_companion_dam.zip

# ---------- Standalone compile verification (fresh dirs) ----------
rm -rf /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v27 && mkdir -p /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v27/main /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v27/companion
unzip -q download/submission_main_dam.zip -d /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v27/main
unzip -q download/submission_companion_dam.zip -d /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v27/companion
echo "=== fresh-dir compile: main v22 ==="
(cd /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v27/main && tectonic journal_manuscript_v22.tex 2>&1 | tail -2 && \
 pdfinfo journal_manuscript_v22.pdf | grep Pages)
echo "=== fresh-dir compile: companion v15 ==="
(cd /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v27/companion && tectonic companion_categorical_v15.tex 2>&1 | tail -2 && \
 pdfinfo companion_categorical_v15.pdf | grep Pages)
echo "ALL DONE"
