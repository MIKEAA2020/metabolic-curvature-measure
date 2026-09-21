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
