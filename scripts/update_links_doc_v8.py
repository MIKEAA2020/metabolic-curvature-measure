#!/usr/bin/env python3
"""Update SUBMISSION_PACKAGE_LINKS.md for the author-finalization +
journal-guideline-compliance + v7 package round: new revision note,
author identity + BMB compliance items in the main row, TAC indexing
keywords + AMS class in the companion row, and verified review-model
notes for both journals (BMB single-blind; TAC non-anonymized)."""
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO)

n = 0


def rep(path, old, new, what, count=1):
    global n
    src = open(path).read()
    c = src.count(old)
    if c != count:
        print(f"FAIL [{what}]: found {c} (expected {count}) in {path}")
        sys.exit(1)
    open(path, "w").write(src.replace(old, new))
    n += 1
    print(f"ok   [{what}] x{c}")


F = "download/SUBMISSION_PACKAGE_LINKS.md"

# ---- 1. header stamp (already applied in the failed first run) ----

# ---- 2. new revision note (newest first) -------------------------------
rep(F, "Revision note (2026-09-16, final proof-read + alignment audit "
    "+ v6\npackage round):",
    """Revision note (2026-09-16, author-finalization +
journal-guideline-compliance + v7 package round): (1) Author identity
finalized in both manuscripts and both cover letters: Amin Abaee,
Independent Researcher, Tehran, Iran; amin_abaee@ut.ac.ir; ORCID
0000-0002-0019-1842 (main paper: \\author + \\thanks title-page
footnote, Author Contributions, pdfauthor; companion: title block,
pdfauthor; cover letters: signature block and date filled). (2) BMB
guideline compliance for the main paper, re-verified against the
Springer submission guidelines: abstract trimmed to 245 words
(guideline 150-250; was 291 rendered), six keywords re-selected for
discoverability (flux balance analysis; discrete curvature; active
set; parametric linear programming; flux rerouting; epistasis --
flux balance analysis and epistasis added as non-title search
handles; transcriptional response and carbon depletion dropped as
title/abstract-indexed duplicates), and continuous line numbering
enabled (lineno package) per the instructions to authors. (3) TAC
indexing requirements for the companion: visible Keywords line
(optic category; stratified connection; 2-category; filtered
colimit; homotopy type theory; applied category theory) and AMS
2020 Subject Classification (18D05; 18N99; 92B05) added below the
abstract; review-model facts re-verified from the official pages
(BMB single-blind per the SMB society page; TAC non-anonymized --
no anonymized-review option, submission by email to a named
Editorial Board member). (4) Rebuilt and verified: both PDFs
recompiled tectonic-clean (main 28 pp with line numbers; companion
74 pp, zero undefined references), audit_v4 98/98 PASS and
audit_v12 301/301 PASS re-run after the edits, submission ZIPs
rebuilt via build_submission_zips_v7.sh with fresh-dir standalone
compiles verified, and the download PDF copies refreshed.

Revision note (2026-09-16, final proof-read + alignment audit + v6
package round):""",
    "new revision note")

# ---- 3. main row: v7 revision ------------------------------------------
rep(F, "Manuscript PDF (28 pp, full proofs in appendices, declarations "
    "in backmatter)",
    "Manuscript PDF (28 pp, full proofs in appendices, declarations in "
    "backmatter, + v7 author-finalization/BMB-compliance revision: "
    "author identity, affiliation, e-mail, and ORCID on the title page; "
    "abstract 245 words within the Springer 150-250 guideline; six "
    "discoverability-optimized keywords; continuous line numbering "
    "enabled)",
    "main PDF row")

# ---- 4. companion row: prepend v7 revision ------------------------------
rep(F, "Manuscript PDF (74 pp, + final proof-read/alignment/v6-package "
    "revision:",
    "Manuscript PDF (74 pp, + author-finalization revision: Amin Abaee / "
    "Independent Researcher, Tehran, Iran / ORCID 0000-0002-0019-1842 in "
    "the title block, TAC indexing keywords (optic category; stratified "
    "connection; 2-category; filtered colimit; homotopy type theory; "
    "applied category theory) and AMS 2020 Subject Classification "
    "(18D05; 18N99; 92B05) added below the abstract, + "
    "final proof-read/alignment/v6-package revision:",
    "companion PDF row")

# ---- 5. BMB section: review model note ----------------------------------
rep(F, "> Portal code verified as **bmab**",
    "> Review model (verified via the SMB society page): single-blind "
    "peer review -- the author identity is known to reviewers, and the "
    "name, affiliation, corresponding e-mail, and ORCID are on the "
    "title page as the Springer Title Page guideline requires.\n>\n"
    "> Portal code verified as **bmab**",
    "BMB review-model note")

# ---- 6. TAC section: review model note -----------------------------------
rep(F, "only after acceptance.\n\n### Package files (GitHub)",
    """only after acceptance. Review model: **not anonymized** -- the
author information page (fetched and verified in full) contains no
anonymization provisions, and submissions go by email to a named
Editorial Board member, so the author identity is on the paper; TAC
also asks that the final accepted source include keywords and an AMS
2020 Subject Classification for external indexing (both now present
below the abstract of the submitted PDF).

### Package files (GitHub)""",
    "TAC review-model note")

print(f"\n{n} edits applied.")
