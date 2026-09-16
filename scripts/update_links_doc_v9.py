#!/usr/bin/env python3
"""Prepend the v8-round revision note to SUBMISSION_PACKAGE_LINKS.md
(newest-first convention) and refresh the PDF-row revision stacks."""
import re

P = ("/home/z/my-project/metabolic-curvature-measure/download/"
     "SUBMISSION_PACKAGE_LINKS.md")
s = open(P).read()

note = """Revision note (2026-09-16, formal-tone revision + figure repair + v8
package round): (1) New manuscript versions as separate files, prior
versions untouched: scripts/journal_manuscript_v5.tex (main, BMB;
from v4) and scripts/companion_categorical_v4.tex (companion, TAC;
from v3); both compiled tectonic-clean (main 27 pp; companion 74 pp;
zero undefined references) with the v5/v4 PDF copies refreshed in
download/. (2) Formal-journal-tone revision of both manuscripts per
the author's directive: declarations rewritten as brief single
sentences (Funding: none; competing interests: none; AI declaration:
GLM (Z.ai) and DeepSeek AI assisted with development and
documentation of analysis code, all AI-assisted content reviewed,
verified, and edited by the author, who takes responsibility for the
final content; ethics approval: not applicable; author
contributions: A.A. conceived the study design, developed the
methodology and analysis code, performed the data analysis, and
drafted and revised the manuscript); meta-commentary and
self-referential prose removed (main: the categorical-subsection
self-description, division-of-labor editorializing, "locked"
internal jargon -> "declared"/"fixed", "after the discovery of" ->
"resolving", a duplicated sentence fragment in the active-set bridge
paragraph repaired; companion: the Status note below the abstract,
"Medium audit" remark retitled "Medium construction and the
wild-type optima" with correction-history phrasing removed,
"iron/phosphate round" and audit-diary phrasing rewritten as
scientific observation, "the external novelty assessment explicitly
asked for" removed, "honestly reported" removed, the "X is the sole
author" placeholder replaced by A.A.); proofs left at full length.
(3) Figure repair: Fig 3 (primary association) panel (b) bar
annotations no longer collide with the panel title (explicit y-axis
headroom); the same fix applied to the path-robustness figure panel
(b2) and to a clipped annotation in the event-measure-stabilization
figure panel (d); all six main-paper figures regenerated without
internal experiment codes (V5/E22/E24/V7/V6/V8/E32/M4b/M1/AX-8c/9/10
labels replaced by manuscript terminology); regeneration was
artifact-driven or a deterministic re-run with all data artifacts
byte-identical (e32 differs only in the wall-clock runtime_s field).
(4) Audits re-run on the new versions: audit_v5_numbers.py 98/98
PASS (main) and audit_v13_numbers.py 301/301 PASS (companion);
cover letters' cross-referenced filenames updated; submission ZIPs
rebuilt via build_submission_zips_v8.sh with fresh-dir standalone
compiles verified (main BMB 27 pp; companion TAC 74 pp).

"""

anchor = "Revision note (2026-09-16, author-finalization"
i = s.find(anchor)
if i == -1:
    raise SystemExit("anchor not found")
s = s[:i] + note + s[i:]

# refresh the generated-date line
s = s.replace(
    "Generated 2026-09-16 (author-finalization + journal-guideline-"
    "compliance + v7\npackage round).",
    "Generated 2026-09-16 (formal-tone revision + figure repair + v8\n"
    "package round).")

open(P, "w").write(s)
print("links doc updated; new note prepended at", i)
