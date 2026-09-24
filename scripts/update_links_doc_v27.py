#!/usr/bin/env python3
"""Retarget SUBMISSION_PACKAGE_LINKS.md to the V22/V15 Zenodo-archive
round (v27 packages): header + newest-first revision note, package
table rows (PDF/source/refs/bib pointers), Zenodo archive rows for
both papers, build notes, and the pre-submission checklist. Anchored,
count-asserted edits.
"""
import os

P = "/home/z/my-project/metabolic-curvature-measure/download/SUBMISSION_PACKAGE_LINKS.md"
t = open(P, encoding="utf-8").read()
n_repl = 0


def rep(old, new, label, count=1):
    global t, n_repl
    found = t.count(old)
    assert found == count, f"{label}: expected {count}, found {found}"
    t = t.replace(old, new)
    n_repl += 1


# --- 1. header ---
rep("Generated 2026-09-24 (V21/V14 final-prose round + v26 package round: journal_manuscript_v21 + companion_categorical_v14;\n"
    "supersedes the V20/V13 Discover Applied Mathematics + v25 package round).",
    "Generated 2026-09-24 (V22/V15 Zenodo-archive round + v27 package round: journal_manuscript_v22 + companion_categorical_v15;\n"
    "supersedes the V21/V14 final-prose + v26 package round).",
    "header")

# --- 2. newest-first revision note ---
rep("Revision note (2026-09-24, V21/V14 final-prose round + v26\n"
    "package round, the final read-through pass of both manuscripts' prose):",
    "Revision note (2026-09-24, V22/V15 Zenodo-archive round + v27\n"
    "package round): the two archival DOIs wired into both data\n"
    "availability statements on NEW versioned files -- scripts/\n"
    "journal_manuscript_v22.tex (from v21; v21 and all earlier versions\n"
    "untouched, via scripts/v22_v15_zenodo_doi.py) and scripts/\n"
    "companion_categorical_v15.tex (from v14; v14 and all earlier\n"
    "versions untouched, same script). MAIN: the 'Data, Software, and\n"
    "Code Availability' statement now records the archival deposit of\n"
    "the compile-ready submission package on Zenodo (version DOI\n"
    "10.5281/zenodo.22941018 -- the deposited file is the v26\n"
    "submission ZIP, MD5 8e7e367183a8f84493e65796bc7ebad4, CC-BY 4.0,\n"
    "concept DOI 10.5281/zenodo.22941017; the deposit byte-verified\n"
    "against the live Zenodo record this round); the two Reproducibility\n"
    "count sites refreshed to the v32 ledger. COMPANION: the 'Data and\n"
    "code availability' paragraph records its archive (version DOI\n"
    "10.5281/zenodo.22940820 -- the v26 submission ZIP, MD5\n"
    "6fa2d8d08386daeef563328fdfafad63, CC-BY 4.0, concept DOI\n"
    "10.5281/zenodo.22940819). No theorem, proof, number, figure, or\n"
    "reference changed; refs/bib side files carried (29 entries,\n"
    "byte-identical). VERIFIED: audit_v32_numbers.py 372/372 PASS (the\n"
    "v31 ledger carried + 6 V22 gates, including byte-exact\n"
    "reverse-edit minimal-diff verification); tectonic main 37 pp /\n"
    "companion 76 pp, 0 errors / 0 '??'; v27 ZIPs\n"
    "(build_submission_zips_v27.sh) fresh-dir verified 37/76 pp; DAM\n"
    "cover letters retargeted (372/372, Zenodo DOIs in the\n"
    "data-availability disclosures). NOTE: the two Zenodo deposits\n"
    "currently hold the v26 packages (the v21/v14 PDFs as archived at\n"
    "deposit time); the manuscripts cite the version DOIs as the\n"
    "archival record. If the deposits are refreshed with the v27\n"
    "packages, the concept DOIs (22941017 / 22940819) resolve to the\n"
    "latest version.\n"
    "\n"
    "Revision note (2026-09-24, V21/V14 final-prose round + v26\n"
    "package round, the final read-through pass of both manuscripts' prose):",
    "revision note prepend")

# --- 3. global filename retargets (links + link texts) ---
rep("journal_manuscript_v21.pdf", "journal_manuscript_v22.pdf",
    "main pdf pointer", 3)
rep("journal_manuscript_v21.tex", "journal_manuscript_v22.tex",
    "main tex pointer", 3)
rep("journal_manuscript_v21_dam_refs.tex",
    "journal_manuscript_v22_dam_refs.tex", "refs pointer", 5)
rep("journal_manuscript_v21_refs.bib", "journal_manuscript_v22_refs.bib",
    "refs bib pointer", 3)
rep("companion_categorical_v14.pdf", "companion_categorical_v15.pdf",
    "companion pdf pointer", 3)
rep("companion_categorical_v14.tex", "companion_categorical_v15.tex",
    "companion tex pointer", 3)
rep("companion_refs_v14.bib", "companion_refs_v15.bib",
    "companion bib pointer", 3)

# --- 4. description rewordings ---
rep("v21 final-prose round: the read-through pass applied -- the Discussion memory subsection's same-gene transcript correlation harmonized to +0.419 (one audited value everywhere), the protein-layer robustness sentence's provenance named (the per-gene path metric of 5.7), and the six in-text figure references normalized to the 'Fig. n' form; every number unchanged from v20, audit_v31 366/366",
    "v22 Zenodo-archive round: the Data, Software, and Code Availability statement records the archival DOI 10.5281/zenodo.22941018 (CC-BY 4.0) and the two Reproducibility count sites are refreshed to the v32 ledger; every number unchanged from v21, audit_v32 372/372",
    "paper-1 PDF row description")
rep("v21 title, 366/366 audit",
    "v22 title, 372/372 audit, Zenodo DOI in the availability disclosure",
    "paper-1 cover-letter row")
rep("v21 naming, entries byte-identical to the v20 list",
    "v22 naming, entries byte-identical to the v21 list",
    "paper-1 refs row")
rep("all articles published open access. The v21 package",
    "all articles published open access. The v22 package",
    "paper-1 compliance note")
rep("(`\\graphicspath{{./}{../download/}}`). The v21 package: 37 pp.",
    "(`\\graphicspath{{./}{../download/}}`). The v22 package: 37 pp.",
    "paper-1 build note")
rep("Upload `journal_manuscript_v22_dam_refs.tex` (not the v20 refs\nname) together with the .tex.",
    "Upload `journal_manuscript_v22_dam_refs.tex` (not the v21 refs\nname) together with the .tex.",
    "paper-1 upload note")
rep("V14 final-prose round -- the read-through pass applied: the where-clause of the piecewise-holonomy formula restored to its equation, the two-contractions remark's state space corrected to the theorem's box X = [-1.5,1.5]^d, an Ito-proof punctuation repair, and the figure-label convention aligned with the journal's 'Fig. n' form; every theorem, proof, and number unchanged from v13 (audit_v31 366/366)",
    "V15 Zenodo-archive round -- the Data and code availability paragraph records the archival DOI 10.5281/zenodo.22940820 (CC-BY 4.0); every theorem, proof, and number unchanged from v14 (audit_v32 372/372)",
    "paper-2 PDF row description")
rep("v14 title", "v15 title, Zenodo DOI in the availability disclosure",
    "paper-2 cover-letter row")
rep("V14: byte-identical to the v13 database; no reference changes in the final-prose round",
    "V15: byte-identical to the v14 database; no reference changes in the Zenodo-archive round",
    "paper-2 bib row")

# --- 5. Zenodo archive rows + v27 ZIP-row stamps ---
rep("| **One-file upload ZIP (compile-ready, DAM README; fresh-dir verified 37 pp)** |",
    "| **One-file upload ZIP (compile-ready, DAM README; v27 build, fresh-dir verified 37 pp)** |",
    "paper-1 zip row stamp")
rep("| **One-file upload ZIP (compile-ready, DAM README; fresh-dir verified 76 pp)** |",
    "| **One-file upload ZIP (compile-ready, DAM README; v27 build, fresh-dir verified 76 pp)** |",
    "paper-2 zip row stamp")
rep("| Highlights file (JTB-path history only; not part of the BMB package)",
    "| **Zenodo archive of the submission package (version DOI 10.5281/zenodo.22941018; concept DOI 10.5281/zenodo.22941017; CC-BY 4.0; deposit = the v26 ZIP, MD5 8e7e367183a8f84493e65796bc7ebad4, byte-verified live; cited in the manuscript's Data, Software, and Code Availability statement)** | — | https://doi.org/10.5281/zenodo.22941018 |\n"
    "| Highlights file (JTB-path history only; not part of the BMB package)",
    "paper-1 zenodo row")
rep("| Manuscript PDF (76 pp; V15 Zenodo-archive round",
    "| **Zenodo archive of the submission package (version DOI 10.5281/zenodo.22940820; concept DOI 10.5281/zenodo.22940819; CC-BY 4.0; deposit = the v26 ZIP, MD5 6fa2d8d08386daeef563328fdfafad63, byte-verified live; cited in the manuscript's Data and code availability declaration)** | — | https://doi.org/10.5281/zenodo.22940820 |\n"
    "| Manuscript PDF (76 pp; V15 Zenodo-archive round",
    "paper-2 zenodo row")

# --- 6. checklist prepend ---
rep("Resolved (V21/V14 final-prose round, 2026-09-24): the final\n"
    "read-through pass of both manuscripts' prose applied on NEW",
    "Resolved (V22/V15 Zenodo-archive round, 2026-09-24): the two\n"
    "archival DOIs (main 10.5281/zenodo.22941018, companion\n"
    "10.5281/zenodo.22940820; both byte-verified against the live\n"
    "Zenodo records, CC-BY 4.0) wired into both data availability\n"
    "statements on NEW versioned files (main v22 from v21, companion\n"
    "v15 from v14; the earlier versions untouched); refs/bib side\n"
    "files carried; audit_v32_numbers.py 372/372 PASS; tectonic 37/76\n"
    "pp, 0 errors / 0 '??'; v27 ZIPs fresh-dir verified; cover\n"
    "letters retargeted (372/372, DOIs disclosed). Earlier rounds\n"
    "resolved: the V21/V14 final-prose round, 2026-09-24: the\n"
    "final\nread-through pass of both manuscripts' prose applied on NEW",
    "checklist prepend")

open(P, "w", encoding="utf-8").write(t)
print(f"SUBMISSION_PACKAGE_LINKS.md updated ({n_repl} anchored edits).")

# sanity: no stale current-round pointers (historical line-wrapped
# notes like 'journal_manuscript_\\nv21.tex' are exempt by design)
assert "journal_manuscript_v21_dam_refs.tex" not in t
assert "companion_refs_v14.bib" not in t
assert "audit_v31 366/366" not in t
print("Sanity checks passed.")
