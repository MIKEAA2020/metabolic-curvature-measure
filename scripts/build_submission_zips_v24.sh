#!/bin/bash
# Build self-contained, compile-ready submission ZIPs for the v24 round:
# main = journal_manuscript_v19.tex (BMB target, UNCHANGED from the v22
# package), companion = companion_categorical_v12.tex (V12 companion-
# comprehension round, NEW versioned file built from v11 by
# scripts/companion_v12_structure.py; v11 and all earlier versions
# untouched).
# Changes vs build_submission_zips_v23.sh:
#   - Companion: targeted structural re-alignment for clarity and human
#     comprehension -- abstract fragment repair (the opening fragment
#     'When adaptive systems navigate ... to remain viable.', the
#     telegraphic 'Four pillars.', the pillar-(iv) fragment; run-on
#     splits; 264 words < 265 cap with the six-axis sentence intact), a
#     plan-of-the-paper paragraph at the end of the introduction (maps
#     all sections, disambiguates the two sevens: optic bridges vs
#     hierarchy claims A-G), and one experiment-framing sentence in each
#     computational section (verdicts; network battery). Every theorem,
#     proof, number, and section order unchanged; companion_refs_v12.bib
#     byte-identical copy.
#   - Main: unchanged (journal_manuscript_v19.tex exactly as in v22/v23).
#   - All numerical claims re-verified: audit_v29_numbers.py 349/349 PASS
#     (identical check set, companion filename retargeted);
#     pattern_sweep_v16 16/16 clean on both; tectonic companion 76 pp,
#     0 errors / 0 '??'.
# Each ZIP verified by fresh-dir tectonic compile.
set -euo pipefail
cd /home/z/my-project/metabolic-curvature-measure

STAGE=scripts/overleaf_stage_v24
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
- Keywords: 6 (BMB range 4-6): flux balance analysis; metabolic rerouting;
  active-set curvature; transcriptional regulation; translational
  buffering; epistasis.
- Author-contribution statement: included in the backmatter (CRediT
  taxonomy; single author, roles listed).
- Declaration of competing interests, funding sources, declaration of
  generative AI use, and the research-data statement: all included in the
  manuscript backmatter; the cover letter
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
cp scripts/companion_categorical_v12.tex    "$C/"
cp scripts/companion_refs_v12.bib       "$C/"
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
  document to companion_categorical_v12.tex, recompile (pdflatex + bibtex +
  pdflatex x2; Overleaf runs this automatically).
- Command line:
    pdflatex companion_categorical_v12.tex
    bibtex   companion_categorical_v12
    pdflatex companion_categorical_v12.tex
    pdflatex companion_categorical_v12.tex

## Contents
- companion_categorical_v12.tex  main source (main document)
- companion_refs_v12.bib BibTeX database (required by \bibliography)
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

## Relation to the application paper (v19 division of labor)
- The application paper (journal_manuscript_v19.tex, Bulletin of
  Mathematical Biology target) is written in measure-theoretic terms alone;
  one Discussion paragraph records the division of labor and cites this
  paper for the constructions, machine verifications, and proofs at the
  status marked per result.
- This paper is self-contained for its own claims: all categorical
  definitions, constructions, and proofs live here (the application
  paper's former brief adapted statement of them was removed in its v19
  comprehension restructure and is carried here alone).
EOF

# ---------- ZIP ----------
OUT=/home/z/my-project/metabolic-curvature-measure/download
rm -f "$OUT/submission_main_bmb.zip" "$OUT/submission_companion_tac.zip"
(cd "$STAGE/main"      && zip -qr "$OUT/submission_main_bmb.zip" .)
(cd "$STAGE/companion" && zip -qr "$OUT/submission_companion_tac.zip" .)
cd /home/z/my-project/metabolic-curvature-measure

# download PDF copies (byte-identical to the scripts builds)
cp scripts/journal_manuscript_v19.pdf download/journal_manuscript_v19.pdf
cp scripts/companion_categorical_v12.pdf download/companion_categorical_v12.pdf

echo "=== ZIP contents (main) ==="
unzip -l download/submission_main_bmb.zip
echo "=== ZIP contents (companion) ==="
unzip -l download/submission_companion_tac.zip

# ---------- Standalone compile verification (fresh dirs) ----------
rm -rf /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v24 && mkdir -p /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v24/main /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v24/companion
unzip -q download/submission_main_bmb.zip -d /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v24/main
unzip -q download/submission_companion_tac.zip -d /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v24/companion
echo "=== fresh-dir compile: main v19 ==="
(cd /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v24/main && tectonic journal_manuscript_v19.tex 2>&1 | tail -2 && \
 pdfinfo journal_manuscript_v19.pdf | grep Pages)
echo "=== fresh-dir compile: companion v12 ==="
(cd /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v24/companion && tectonic companion_categorical_v12.tex 2>&1 | tail -2 && \
 pdfinfo companion_categorical_v12.pdf | grep Pages)
echo "ALL DONE"
