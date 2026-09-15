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
