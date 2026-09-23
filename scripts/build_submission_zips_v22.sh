#!/bin/bash
# Build self-contained, compile-ready submission ZIPs for the v22 round:
# main = journal_manuscript_v19.tex (v19 comprehension restructure, BMB
# target), companion = companion_categorical_v10.tex (TAC, unchanged).
# Changes vs build_submission_zips_v21.sh (v18/JTB round):
#   - Main: new versioned file journal_manuscript_v19.tex built from v18
#     by scripts/v19_comprehension_restructure.py per the post-JTB-
#     rejection directive: plain title, bio-first abstract (243 words,
#     every audited number kept), keywords 6, three question-led intro
#     paragraphs, categorical subsection removed, refinement-resolution
#     bridge moved to Appendix A, counts-disambiguation appendix folded
#     into Methods, refs journal_manuscript_v19_bmb_refs.tex.
#   - Package renamed submission_main_jtb.zip -> submission_main_bmb.zip
#     (venue decision: BMB target after the JTB desk rejection; the
#     ZIP itself remains venue-neutral and compiles identically for any
#     Springer/Elsevier target).
#   - Highlights: JTB-only requirement; highlights_jtb.docx stays in the
#     repository as JTB-path history but is NOT part of the BMB package.
#   - Companion: unchanged (companion_categorical_v10.tex, TAC route).
#   - All numerical claims re-verified: audit_v27_numbers.py 349/349
#     PASS (347 carried v26 checks + 2 new V19 gates; JTB gates recapped
#     to BMB); pattern_sweep_v16 16/16 clean on both; v19 structural
#     gates PASS; verify_v19_completeness.py ALL COMPLETE (every removed
#     numeric token traced to an intentionally deleted/rewritten
#     region); tectonic 37 pp, 0 errors / 0 undefined.
# Each ZIP verified by fresh-dir tectonic compile.
set -euo pipefail
cd /home/z/my-project/metabolic-curvature-measure

STAGE=scripts/overleaf_stage_v22
rm -rf "$STAGE"
mkdir -p "$STAGE/main" "$STAGE/companion"

# ---------- MAIN (Bulletin of Mathematical Biology) ----------
M=$STAGE/main
cp scripts/journal_manuscript_v19.tex             "$M/"
cp scripts/journal_manuscript_v19_bmb_refs.tex    "$M/"
cp scripts/journal_manuscript_v19_refs.bib        "$M/"
mkdir -p "$M/m1_m3" "$M/alexandrov_bridge" "$M/association_robustness"
cp download/m1_m3/fig_m1_summary.png                    "$M/m1_m3/"
cp download/alexandrov_bridge/coupling_figures.png      "$M/alexandrov_bridge/"
cp download/association_robustness/v5_e24_recalibration.png    "$M/association_robustness/"
cp download/association_robustness/v7_path_robustness.png      "$M/association_robustness/"
cp download/association_robustness/v8_tiebreak_robustness.png  "$M/association_robustness/"
cp download/association_robustness/e32_event_measure_stabilization.png "$M/association_robustness/"
cat > "$M/README.md" << 'EOF'
# Main manuscript — Bulletin of Mathematical Biology (Springer)
# Compile-ready standalone package

Title: A discrete curvature measure for flux balance analysis predicts
transcriptional regulation and translational buffering in Escherichia
coli

## How to compile
- Overleaf: upload this ZIP via New Project -> Upload Project, set the main
  document to journal_manuscript_v19.tex, recompile. (Run twice so natbib
  citations resolve; Overleaf does this automatically.)
- Command line: pdflatex journal_manuscript_v19.tex  (x2)

## Contents
- journal_manuscript_v19.tex          main source (main document)
- journal_manuscript_v19_bmb_refs.tex reference list (input by the main file)
- journal_manuscript_v19_refs.bib     underlying BibTeX database (not required
  for compilation; included for editorial source completeness)
- m1_m3/, alexandrov_bridge/, association_robustness/  figure PNGs at the
  exact relative paths used by \includegraphics

## Bulletin of Mathematical Biology submission notes (instructions to
## authors, live-verified earlier in the project)
- Article type: Original Research.
- Abstract: 243 words (Springer/BMB guideline: 150-250), a single
  narrative arc from the biological question to the findings.
- Keywords: 6 (BMB range 4-6): flux balance analysis; metabolic
  rerouting; active-set curvature; transcriptional regulation;
  translational buffering; epistasis.
- Author-contribution statement: included in the backmatter (CRediT
  taxonomy; single author, roles listed).
- Declaration of competing interests, funding sources, declaration of
  generative AI use, and the research-data statement: all included in
  the manuscript backmatter; the cover letter
  (download/cover_letter_bmb.md in the repository) carries the full
  disclosures.
- Author identity, affiliation, corresponding e-mail, and ORCID appear on
  the title page (\thanks footnote); e-mail and ORCID are clickable.
- Continuous line numbering is enabled via the lineno package.
- Reference style: author-year (natbib), alphabetical; Springer accepts
  any consistent style at first submission.
EOF

# ---------- COMPANION (Theory and Applications of Categories) ----------
C=$STAGE/companion
cp scripts/companion_categorical_v10.tex    "$C/"
cp scripts/companion_refs_v10.bib       "$C/"
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

Title: A Geometric and Category-Theoretic Theory of Viability: How
Sequential Adaptations Induce Path-Dependent Risk

## How to compile
- Overleaf: upload this ZIP via New Project -> Upload Project, set the main
  document to companion_categorical_v10.tex, recompile (pdflatex + bibtex +
  pdflatex x2; Overleaf runs this automatically).
- Command line:
    pdflatex companion_categorical_v10.tex
    bibtex   companion_categorical_v10
    pdflatex companion_categorical_v10.tex
    pdflatex companion_categorical_v10.tex

## Contents
- companion_categorical_v10.tex  main source (main document)
- companion_refs_v10.bib BibTeX database (required by \bibliography)
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
rm -f "$OUT/submission_main_jtb.zip" "$OUT/submission_companion_tac.zip"
(cd "$STAGE/main"      && zip -qr "$OUT/submission_main_bmb.zip" .)
(cd "$STAGE/companion" && zip -qr "$OUT/submission_companion_tac.zip" .)
cd /home/z/my-project/metabolic-curvature-measure

# download PDF copy (byte-identical to the scripts build)
cp scripts/journal_manuscript_v19.pdf download/journal_manuscript_v19.pdf

echo "=== ZIP contents (main) ==="
unzip -l download/submission_main_bmb.zip
echo "=== ZIP contents (companion) ==="
unzip -l download/submission_companion_tac.zip

# ---------- Standalone compile verification (fresh dirs) ----------
rm -rf /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v22 && mkdir -p /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v22/main /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v22/companion
unzip -q download/submission_main_bmb.zip -d /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v22/main
unzip -q download/submission_companion_tac.zip -d /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v22/companion
echo "=== fresh-dir compile: main v19 ==="
(cd /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v22/main && tectonic journal_manuscript_v19.tex 2>&1 | tail -2 && \
 pdfinfo journal_manuscript_v19.pdf | grep Pages)
echo "=== fresh-dir compile: companion v10 ==="
(cd /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v22/companion && tectonic companion_categorical_v10.tex 2>&1 | tail -2 && \
 pdfinfo companion_categorical_v10.pdf | grep Pages)
echo "ALL DONE"
