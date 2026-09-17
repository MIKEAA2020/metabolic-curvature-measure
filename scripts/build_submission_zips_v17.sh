#!/bin/bash
# Build self-contained, compile-ready submission ZIPs for the v17 round:
# main = journal_manuscript_v14.tex (BMB), companion = companion_categorical_v9.tex (TAC).
# Changes vs build_submission_zips_v16.sh (v16 round):
#   - Main only: new versioned file journal_manuscript_v14.tex (from v13)
#     plus its refs copies. Abstract cap round per the author directive --
#     the abstract trimmed under the 255-word cap (269 -> 254 audit-style
#     words) with the register kept on Gemini's abstract: the M1 sweep
#     qualifier and the statistics conventions "n ="/"evaluated" dropped
#     per Gemini's own plain forms, "fails in general" -> "fails
#     generically" (Gemini's exact word), the boundaries gloss compressed,
#     "the measured window" -> "the window", and two function words
#     tightened. Every number, both in-words glosses (h, L_var), and the
#     full connective arc kept. Body untouched.
#     Companion UNCHANGED (companion_categorical_v9.tex; zero edits).
#   - All numerical claims unchanged; audit_v22_numbers.py 301/301 PASS;
#     pattern_sweep_v16 16/16 clean; verify_v14_completeness.py ALL
#     COMPLETE (body byte-identical outside the abstract; zero numeric
#     token changes in the abstract swap).
# Each ZIP verified by fresh-dir tectonic compile.
set -euo pipefail
cd /home/z/my-project/metabolic-curvature-measure

STAGE=scripts/overleaf_stage_v17
rm -rf "$STAGE"
mkdir -p "$STAGE/main" "$STAGE/companion"

# ---------- MAIN (Bulletin of Mathematical Biology) ----------
M=$STAGE/main
cp scripts/journal_manuscript_v14.tex          "$M/"
cp scripts/journal_manuscript_v14_bmb_refs.tex "$M/"
cp scripts/journal_manuscript_v14_refs.bib     "$M/"
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
  document to journal_manuscript_v14.tex, recompile. (Run twice so natbib
  citations resolve; Overleaf does this automatically.)
- Command line: pdflatex journal_manuscript_v14.tex  (x2)

## Contents
- journal_manuscript_v14.tex        main source (main document)
- journal_manuscript_v14_bmb_refs.tex  reference list (input by the main file)
- journal_manuscript_v14_refs.bib   underlying BibTeX database (not required
  for compilation; included for editorial source completeness)
- m1_m3/, alexandrov_bridge/, association_robustness/  figure PNGs at the
  exact relative paths used by \includegraphics

## Formatting notes (Springer BMB submission guidelines)
- Author identity, affiliation, corresponding e-mail, and ORCID appear on the
  title page (\thanks footnote); e-mail and ORCID are clickable.
- Abstract: 254 words (within the author's 255-word cap), in two paragraphs
  (theory; biology).
- Keywords: 6 (guideline: 4-6).
- Continuous line numbering is enabled via the lineno package.
- The cover letter (download/cover_letter_bmb.md in the repository) carries
  the Statements and Declarations disclosures.
EOF

# ---------- COMPANION (Theory and Applications of Categories) ----------
C=$STAGE/companion
cp scripts/companion_categorical_v9.tex    "$C/"
cp scripts/companion_refs_v9.bib       "$C/"
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
# Companion manuscript — Theory and Applications of Categories
# Compile-ready standalone package

Title: Stratified Connections, Optic Composition, and the Homotopy
Fixed-Point Extension: A Categorical Framework for Viability-Weighted
Curvature

## How to compile
- Overleaf: upload this ZIP via New Project -> Upload Project, set the main
  document to companion_categorical_v9.tex, recompile (pdflatex + bibtex +
  pdflatex x2; Overleaf runs this automatically).
- Command line:
    pdflatex companion_categorical_v9.tex
    bibtex   companion_categorical_v9
    pdflatex companion_categorical_v9.tex
    pdflatex companion_categorical_v9.tex

## Contents
- companion_categorical_v9.tex  main source (main document)
- companion_refs_v9.bib BibTeX database (required by \bibliography)
- 12 figure PNGs at the flat paths used by \includegraphics

## Submission route (TAC author information)
- Initial submission: email the compiled PDF to one Editorial Board member
  (not the Managing Editor or TeXnical editors), cc tac@mta.ca. The cover
  letter (download/cover_letter_tac.md in the repository) is addressed to
  the chosen Transmitting Editor.
- Review model: not anonymized (no double-blind option at TAC); author
  identity is on the paper.
- Keywords and AMS 2020 Subject Classification (18D05; 18N99; 92B05) are
  included per TAC's external-indexing requirements; the final accepted
  version will be reformatted with the journal's tac.cls (12pt).
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
rm -rf /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v17 && mkdir -p /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v17/main /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v17/companion
unzip -q download/submission_main_bmb.zip -d /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v17/main
unzip -q download/submission_companion_tac.zip -d /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v17/companion
echo "=== fresh-dir compile: main v14 ==="
(cd /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v17/main && tectonic journal_manuscript_v14.tex 2>&1 | tail -2 && \
 pdfinfo journal_manuscript_v14.pdf | grep Pages)
echo "=== fresh-dir compile: companion v9 ==="
(cd /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v17/companion && tectonic companion_categorical_v9.tex 2>&1 | tail -2 && \
 pdfinfo companion_categorical_v9.pdf | grep Pages)
echo "ALL DONE"
