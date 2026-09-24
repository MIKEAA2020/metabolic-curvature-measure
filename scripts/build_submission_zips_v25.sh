#!/bin/bash
# Build self-contained, compile-ready submission ZIPs for the v25 round
# (V20/V13 Discover Applied Mathematics alignment):
# main = journal_manuscript_v20.tex (NEW versioned file from v19 via
#   scripts/v20_main_f_fixes.py: F1-F7 light touch-up [F3 direct rank
#   correlation reported, F4 two-regime qualifier, F5 three
#   near-identity wordings corrected, F6 hedges + title narrowed, F1
#   count refreshed, F7 moot] + DAM venue alignment [numeric
#   square-bracket citations, Fig.-label captions, dam refs file]),
# companion = companion_categorical_v13.tex (NEW versioned file from
#   v12 via scripts/v13_companion_edits.py: F2 nitrogen-source
#   substitution qualifier + DAM venue alignment [abstract 248 < 250,
#   keywords 9 -> 6, numeric citations, refs title alignment]).
# v19 and v12 and all earlier versions untouched.
# Changes vs build_submission_zips_v24.sh:
#   - Main: v19 -> v20 (F-fixes + DAM formatting + 359-count refresh).
#   - Companion: v12 -> v13 (F2 + DAM formatting).
#   - Venue: both packages retargeted to Discover Applied Mathematics
#     (Snapp submission; Research article; abstract < 250 words;
#     numeric square-bracket citations; Fig. n caption labels;
#     single-anonymous review; open access), per the live-verified
#     submission guidelines (link.springer.com/journal/44585/
#     submission-guidelines, re-verified this round).
#   - ZIP names: submission_main_dam.zip / submission_companion_dam.zip
#     (the superseded BMB/TAC ZIPs are removed; git history preserves).
#   - All numerical claims re-verified: audit_v30_numbers.py 359/359
#     PASS; tectonic main 37 pp / companion 76 pp, 0 errors / 0 '??'.
# Each ZIP verified by fresh-dir tectonic compile.
set -euo pipefail
cd /home/z/my-project/metabolic-curvature-measure

STAGE=scripts/overleaf_stage_v25
rm -rf "$STAGE"
mkdir -p "$STAGE/main" "$STAGE/companion"

# ---------- MAIN (Discover Applied Mathematics) ----------
M=$STAGE/main
cp scripts/journal_manuscript_v20.tex             "$M/"
cp scripts/journal_manuscript_v20_dam_refs.tex    "$M/"
cp scripts/journal_manuscript_v20_refs.bib        "$M/"
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
  document to journal_manuscript_v20.tex, recompile. (Run twice so natbib
  citations resolve; Overleaf does this automatically.)
- Command line: pdflatex journal_manuscript_v20.tex  (x2)

## Contents
- journal_manuscript_v20.tex          main source (main document)
- journal_manuscript_v20_dam_refs.tex reference list (input by the main file)
- journal_manuscript_v20_refs.bib     underlying BibTeX database (not required
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
  square]), per the journal's reference style; figure captions use the
  journal's "Fig. 1" label form (no punctuation after the number).
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
EOF

# ---------- COMPANION (Discover Applied Mathematics) ----------
C=$STAGE/companion
cp scripts/companion_categorical_v13.tex    "$C/"
cp scripts/companion_refs_v13.bib       "$C/"
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
  document to companion_categorical_v13.tex, recompile (pdflatex + bibtex +
  pdflatex x2; Overleaf runs this automatically).
- Command line:
    pdflatex companion_categorical_v13.tex
    bibtex   companion_categorical_v13
    pdflatex companion_categorical_v13.tex
    pdflatex companion_categorical_v13.tex

## Contents
- companion_categorical_v13.tex  main source (main document)
- companion_refs_v13.bib BibTeX database (required by \bibliography)
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
  square]), per the journal's reference style.
- Review model: single-anonymous (reviewers know the author identity);
  author identity is on the paper.
- The cover letter (download/cover_letter_dam_companion.md in the
  repository) carries the disclosures; a cover letter is required by
  the journal's submission checklist.

## Relation to the application paper (v20 division of labor)
- The application paper (journal_manuscript_v20.tex, Discover Applied
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
# superseded venue packages (BMB/TAC); git history preserves them
rm -f "$OUT/submission_main_bmb.zip" "$OUT/submission_companion_tac.zip"
cd /home/z/my-project/metabolic-curvature-measure

# download PDF copies (byte-identical to the scripts builds)
cp scripts/journal_manuscript_v20.pdf download/journal_manuscript_v20.pdf
cp scripts/companion_categorical_v13.pdf download/companion_categorical_v13.pdf

echo "=== ZIP contents (main) ==="
unzip -l download/submission_main_dam.zip
echo "=== ZIP contents (companion) ==="
unzip -l download/submission_companion_dam.zip

# ---------- Standalone compile verification (fresh dirs) ----------
rm -rf /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v25 && mkdir -p /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v25/main /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v25/companion
unzip -q download/submission_main_dam.zip -d /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v25/main
unzip -q download/submission_companion_dam.zip -d /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v25/companion
echo "=== fresh-dir compile: main v20 ==="
(cd /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v25/main && tectonic journal_manuscript_v20.tex 2>&1 | tail -2 && \
 pdfinfo journal_manuscript_v20.pdf | grep Pages)
echo "=== fresh-dir compile: companion v13 ==="
(cd /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v25/companion && tectonic companion_categorical_v13.tex 2>&1 | tail -2 && \
 pdfinfo companion_categorical_v13.pdf | grep Pages)
echo "ALL DONE"
