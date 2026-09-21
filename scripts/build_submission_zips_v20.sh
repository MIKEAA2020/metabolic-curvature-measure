#!/bin/bash
# Build self-contained, compile-ready submission ZIPs for the v20 round:
# main = journal_manuscript_v17.tex, companion = companion_categorical_v10.tex (TAC).
# Changes vs build_submission_zips_v18.sh (v17 round):
#   - Main: new versioned file journal_manuscript_v16.tex (from v15)
#     plus its refs copies. Universal Gemini-prose adoption round per the
#     author directive: Gemini's rewrite (external_audits/humanized/
#     gemini,grok humanized.txt lines 1-532) adopted verbatim wherever it
#     provides text -- abstract rebuilt on Gemini's abstract at the
#     255-word cap opening with Gemini's first sentence; title and
#     keywords (Gemini's, merged to the 6-term BMB cap); intro opening +
#     five-findings claim list; Sec. 2 setup/definitions/glosses; the
#     value-flux coupling statement; Sec. 3 opening/TV explanation/
#     holonomy proposition; Sec. 4 validation narratives; Sec. 5
#     association/tie-break/path-robustness/protein-layer narratives;
#     Discussion restructured into Gemini's three subsections; Methods
#     leads. Gemini's proof variants NOT adopted; unaudited Gemini
#     numbers excluded per the v15-round adjudication.
#   - Companion: new versioned file companion_categorical_v10.tex (from
#     v9): Gemini's companion rewrite (companion humanized.txt lines
#     1-714) adopted as the register base -- title, abstract (four-pillar
#     narrative, 264 words under the 265 cap, six-axis sentence intact),
#     keywords, intro problem/obstruction/solution narrative, bold
#     contribution titles, section leads, application-bridge opening;
#     v9 substance retained verbatim (refs, proof statuses, machine-
#     verifications); bibliography pointer to companion_refs_v10.bib.
#   - All numerical claims re-verified: audit_v25_numbers.py 344/344
#     PASS (301 carried + 43 new v17 checks); pattern_sweep_v16 16/16 clean; verify_v16_completeness.py +
#     verify_v10_completeness.py ALL COMPLETE; tectonic 33 pp / 76 pp, 0 undefined / 0 '??'; clickable
#     mailto + ORCID via qpdf; VLM spot checks CLEAN on the changed pages.
# Each ZIP verified by fresh-dir tectonic compile.
set -euo pipefail
cd /home/z/my-project/metabolic-curvature-measure

STAGE=scripts/overleaf_stage_v20
rm -rf "$STAGE"
mkdir -p "$STAGE/main" "$STAGE/companion"

# ---------- MAIN (Bulletin of Mathematical Biology) ----------
M=$STAGE/main
cp scripts/journal_manuscript_v17.tex          "$M/"
cp scripts/journal_manuscript_v17_bmb_refs.tex "$M/"
cp scripts/journal_manuscript_v17_refs.bib     "$M/"
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

Title: A Geometric Theory of Metabolic Flux Rerouting: How Active-Set
Curvature Predicts Transcriptional Regulation and Protein-Layer Buffering

## How to compile
- Overleaf: upload this ZIP via New Project -> Upload Project, set the main
  document to journal_manuscript_v17.tex, recompile. (Run twice so natbib
  citations resolve; Overleaf does this automatically.)
- Command line: pdflatex journal_manuscript_v17.tex  (x2)

## Contents
- journal_manuscript_v17.tex        main source (main document)
- journal_manuscript_v17_bmb_refs.tex  reference list (input by the main file)
- journal_manuscript_v17_refs.bib   underlying BibTeX database (not required
  for compilation; included for editorial source completeness)
- m1_m3/, alexandrov_bridge/, association_robustness/  figure PNGs at the
  exact relative paths used by \includegraphics

## Target venue
- Venue per download/V17_Venue_Evaluation.md (in the repository): JTB is
  the primary recommendation; BMB return only via pre-submission inquiry;
  PLOS Comp Bio the bio-first alternative (APC). The package itself is
  venue-neutral and compiles identically for any of them.

## Formatting notes (Springer BMB submission guidelines, where applicable)
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
rm -f "$OUT/submission_main_bmb.zip" "$OUT/submission_companion_tac.zip"
(cd "$STAGE/main"      && zip -qr "$OUT/submission_main_bmb.zip" .)
(cd "$STAGE/companion" && zip -qr "$OUT/submission_companion_tac.zip" .)
cd /home/z/my-project/metabolic-curvature-measure

echo "=== ZIP contents (main) ==="
unzip -l download/submission_main_bmb.zip
echo "=== ZIP contents (companion) ==="
unzip -l download/submission_companion_tac.zip

# ---------- Standalone compile verification (fresh dirs) ----------
rm -rf /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v20 && mkdir -p /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v20/main /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v20/companion
unzip -q download/submission_main_bmb.zip -d /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v20/main
unzip -q download/submission_companion_tac.zip -d /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v20/companion
echo "=== fresh-dir compile: main v17 ==="
(cd /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v20/main && tectonic journal_manuscript_v17.tex 2>&1 | tail -2 && \
 pdfinfo journal_manuscript_v17.pdf | grep Pages)
echo "=== fresh-dir compile: companion v10 ==="
(cd /home/z/my-project/metabolic-curvature-measure/scripts/zipcheck_v20/companion && tectonic companion_categorical_v10.tex 2>&1 | tail -2 && \
 pdfinfo companion_categorical_v10.pdf | grep Pages)
echo "ALL DONE"
