# Main manuscript — Bulletin of Mathematical Biology
# Compile-ready standalone package

Title: A Measure-Theoretic Discrete Curvature Framework for Metabolic Gene
Sensitivity: From Active-Set Geometry to Transcriptional Response

## How to compile
- Overleaf: upload this ZIP via New Project -> Upload Project, set the main
  document to journal_manuscript_v7.tex, recompile. (Run twice so natbib
  citations resolve; Overleaf does this automatically.)
- Command line: pdflatex journal_manuscript_v7.tex  (x2)

## Contents
- journal_manuscript_v7.tex        main source (main document)
- journal_manuscript_v7_bmb_refs.tex  reference list (input by the main file)
- journal_manuscript_v7_refs.bib   underlying BibTeX database (not required
  for compilation; included for editorial source completeness)
- m1_m3/, alexandrov_bridge/, association_robustness/  figure PNGs at the
  exact relative paths used by \includegraphics

## Formatting notes (Springer BMB submission guidelines)
- Author identity, affiliation, corresponding e-mail, and ORCID appear on
  the title page (\thanks footnote).
- Abstract: 248 words (within the 150-250 guideline).
- Keywords: 6 (guideline: 4-6).
- Continuous line numbering is enabled via the lineno package.
- The cover letter (download/cover_letter_bmb.md in the repository) carries
  the Statements and Declarations disclosures.
