#!/bin/bash
# Build self-contained, compile-ready submission ZIPs for the v4 round:
# main = journal_manuscript_v4.tex (BMB), companion = companion_categorical_v3.tex (TAC).
# Changes vs build_submission_zips.sh (v3 round):
#   - main v4 (C2/C5/C1 framing, APP-1/2/3/5 fixes)
#   - companion v3 (8-point repair set + P0 citations + Keio/E14 closures)
#   - figure directory renamed deepseek_bridge -> association_robustness
# Each ZIP verified by fresh-dir tectonic compile.
set -euo pipefail
cd /home/z/my-project/metabolic-curvature-measure

STAGE=scripts/overleaf_stage_v4
rm -rf "$STAGE"
mkdir -p "$STAGE/main" "$STAGE/companion"

# ---------- MAIN (Bulletin of Mathematical Biology) ----------
M=$STAGE/main
cp scripts/journal_manuscript_v4.tex          "$M/"
cp scripts/journal_manuscript_v3_bmb_refs.tex "$M/"
cp scripts/journal_manuscript_v2_refs.bib     "$M/"
mkdir -p "$M/m1_m3" "$M/alexandrov_bridge" "$M/association_robustness"
cp download/m1_m3/fig_m1_summary.png                    "$M/m1_m3/"
cp download/alexandrov_bridge/coupling_figures.png      "$M/alexandrov_bridge/"
cp download/association_robustness/v5_e24_recalibration.png    "$M/association_robustness/"
cp download/association_robustness/v7_path_robustness.png      "$M/association_robustness/"
cp download/association_robustness/v8_tiebreak_robustness.png  "$M/association_robustness/"
cp download/association_robustness/e32_event_measure_stabilization.png "$M/association_robustness/"
cat > "$M/README.md" << 'EOF'
# Main manuscript — Bulletin of Mathematical Biology
# Compile-ready standalone package

Title: A Measure-Theoretic Discrete Curvature Framework for Metabolic Gene
Sensitivity: From Active-Set Geometry to Transcriptional Response

## How to compile
- Overleaf: upload this ZIP via New Project -> Upload Project, set the main
  document to journal_manuscript_v4.tex, recompile. (Run twice so natbib
  citations resolve; Overleaf does this automatically.)
- Command line: pdflatex journal_manuscript_v4.tex  (x2)

## Contents
- journal_manuscript_v4.tex        main source (main document)
- journal_manuscript_v3_bmb_refs.tex  reference list (input by the main file)
- journal_manuscript_v2_refs.bib   underlying BibTeX database (not required
  for compilation; included for editorial source completeness)
- m1_m3/, alexandrov_bridge/, association_robustness/  figure PNGs at the
  exact relative paths used by \includegraphics

## Before submitting
- Replace the sole-author placeholder "X" with the real author name.
- The [Submission date] placeholder in the cover letter (separate file in
  the repository) must be filled.
EOF

# ---------- COMPANION (Theory and Applications of Categories) ----------
C=$STAGE/companion
cp scripts/companion_categorical_v3.tex    "$C/"
cp scripts/journal_manuscript_refs.bib  "$C/"
cp download/lipschitz_constants_per_optic.png   "$C/"
cp download/cptc_zeno_contraction.png           "$C/"
cp download/inverse_limit_raf_hasse.png         "$C/"
cp download/inverse_limit_raf_extended_hasse.png "$C/"
cp download/claim_f_holonomy_plot.png           "$C/"
cp download/claims_ae_n4_nonabelian.png         "$C/"
cp download/claim_d_heavytail_stress.png        "$C/"
cp download/levy_stable_3half_derivation.png    "$C/"
cp download/claim_g_zeno_plot.png               "$C/"
cp download/t_iteration_convergence_plot.png    "$C/"
cp download/t_iteration_robustness_extension_axis_aligned.png "$C/"
cp download/t_iteration_robustness_extension_rotated.png      "$C/"
cat > "$C/README.md" << 'EOF'
# Companion manuscript — Theory and Applications of Categories
# Compile-ready standalone package

Title: Stratified Connections, Optic Composition, and the Homotopy
Fixed-Point Extension: A Categorical Framework for Viability-Weighted
Curvature

## How to compile
- Overleaf: upload this ZIP via New Project -> Upload Project, set the main
  document to companion_categorical_v3.tex, recompile (pdflatex + bibtex +
  pdflatex x2; Overleaf runs this automatically).
- Command line:
    pdflatex companion_categorical_v3.tex
    bibtex   companion_categorical_v3
    pdflatex companion_categorical_v3.tex
    pdflatex companion_categorical_v3.tex

## Contents
- companion_categorical_v3.tex  main source (main document)
- journal_manuscript_refs.bib BibTeX database (required by \bibliography)
- 12 figure PNGs at the flat paths used by \includegraphics

## Before submitting
- Replace the sole-author placeholder "X" with the real author name.
- TAC submission route: email the compiled PDF to one Editorial Board member
  (not the Managing Editor or TeXnical editors), cc tac@mta.ca.
EOF

# ---------- ZIP ----------
OUT=/home/z/my-project/metabolic-curvature-measure/download
rm -f "$OUT/submission_main_bmb.zip" "$OUT/submission_companion_tac.zip"
(cd "$STAGE/main"      && zip -qr "$OUT/submission_main_bmb.zip" .)
(cd "$STAGE/companion" && zip -qr "$OUT/submission_companion_tac.zip" .)
cd /home/z/my-project/metabolic-curvature-measure

echo "=== ZIP contents (main) ==="
unzip -l download/submission_main_bmb.zip
echo "=== ZIP contents (companion) ==="
unzip -l download/submission_companion_tac.zip

# ---------- Standalone compile verification (fresh dirs) ----------
rm -rf scripts/zipcheck_v4 && mkdir -p scripts/zipcheck_v4/main scripts/zipcheck_v4/companion
unzip -q download/submission_main_bmb.zip -d scripts/zipcheck_v4/main
unzip -q download/submission_companion_tac.zip -d scripts/zipcheck_v4/companion
echo "=== fresh-dir compile: main v4 ==="
(cd scripts/zipcheck_v4/main && tectonic journal_manuscript_v4.tex 2>&1 | tail -2 && \
 pdfinfo journal_manuscript_v4.pdf | grep Pages)
echo "=== fresh-dir compile: companion v3 ==="
(cd scripts/zipcheck_v4/companion && tectonic companion_categorical_v3.tex 2>&1 | tail -2 && \
 pdfinfo companion_categorical_v3.pdf | grep Pages)
echo "ALL DONE"
