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
