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
