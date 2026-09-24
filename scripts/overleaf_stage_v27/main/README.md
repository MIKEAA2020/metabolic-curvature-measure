# Main manuscript — Discover Applied Mathematics (Springer Nature)
# Compile-ready standalone package

Title: A discrete curvature measure for flux balance analysis predicts
transcriptional regulation in Escherichia coli

## How to compile
- Overleaf: upload this ZIP via New Project -> Upload Project, set the main
  document to journal_manuscript_v22.tex, recompile. (Run twice so natbib
  citations resolve; Overleaf does this automatically.)
- Command line: pdflatex journal_manuscript_v22.tex  (x2)

## Contents
- journal_manuscript_v22.tex          main source (main document)
- journal_manuscript_v22_dam_refs.tex reference list (input by the main file)
- journal_manuscript_v22_refs.bib     underlying BibTeX database (not required
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
  square]), per the journal's reference style; figure captions and the
  in-text references use the journal's "Fig. 1" label form.
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
- Data availability: the complete bundle (generation scripts, result
  artifacts, genome-scale models, SHA-256 manifests, verification
  scripts) is at github.com/MIKEAA2020/metabolic-curvature-measure,
  and this submission package is archived on Zenodo at
  DOI 10.5281/zenodo.22941018 (CC-BY 4.0).
- v22 Zenodo-archive round: the availability statement records the
  archival DOI; the same-gene transcript correlation is quoted
  as +0.419 everywhere (one audited value), and the protein-layer
  robustness sentence names its provenance (the per-gene path metric);
  every numerical claim is unchanged and re-verified by the 372-check
  numeric audit (372/372 PASS).
