# Companion manuscript — Discover Applied Mathematics (Springer Nature)
# Compile-ready standalone package

Title: A Geometric and Category-Theoretic Theory of Viability: How
Sequential Adaptations Induce Path-Dependent Risk

## How to compile
- Overleaf: upload this ZIP via New Project -> Upload Project, set the main
  document to companion_categorical_v14.tex, recompile (pdflatex + bibtex +
  pdflatex x2; Overleaf runs this automatically).
- Command line:
    pdflatex companion_categorical_v14.tex
    bibtex   companion_categorical_v14
    pdflatex companion_categorical_v14.tex
    pdflatex companion_categorical_v14.tex

## Contents
- companion_categorical_v14.tex  main source (main document)
- companion_refs_v14.bib BibTeX database (required by \bibliography)
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
  square]), per the journal's reference style; figure captions and the
  in-text references use the journal's "Fig. 1" label form (v14 aligns
  the companion with the main paper's convention).
- Review model: single-anonymous (reviewers know the author identity);
  author identity is on the paper.
- The cover letter (download/cover_letter_dam_companion.md in the
  repository) carries the disclosures; a cover letter is required by
  the journal's submission checklist.

## Relation to the application paper (v21 division of labor)
- The application paper (journal_manuscript_v21.tex, Discover Applied
  Mathematics target) is written in measure-theoretic terms alone;
  one Discussion paragraph records the division of labor and cites this
  paper for the constructions, machine verifications, and proofs at the
  status marked per result.
- This paper is self-contained for its own claims: all categorical
  definitions, constructions, and proofs live here (the application
  paper's former brief adapted statement of them was removed in its
  v19 comprehension restructure and is carried here alone).
