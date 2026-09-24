#!/usr/bin/env python3
"""Zip-visibility round (2026-09-25): make the CURRENT submission packages
unambiguously findable.

Context: the user reported that 'the .zip files on repo hold older manuscript
versions'. Live verification showed:
  - GitHub main (commit 27ddf15) DOES hold the current v27 packages
    (submission_main_dam.zip contains journal_manuscript_v22.tex, MD5
    04d10994cded754c13b3869452618ddf; submission_companion_dam.zip contains
    companion_categorical_v15.tex, MD5 482b92eb44f2de5653e08c7653683877).
  - The two Zenodo version DOIs hold the v26 ARCHIVAL snapshots
    (journal_manuscript_v21.tex / companion_categorical_v14.tex), exactly as
    recorded in the manuscripts' data availability statements.
  - The confusion vector: the GitHub zip filenames are reused by every build
    round, and the Zenodo deposits are one archive-generation behind.

Fix (repo-side discoverability only; no manuscript, PDF, or package byte
changes): version-named byte-identical zip copies were added
(download/submission_main_dam_v22.zip, download/
submission_companion_dam_v15.zip); this script records them and the
'where the current zips live' clarifier in SUBMISSION_PACKAGE_LINKS.md via
anchored in-place edits (the established pattern for this document).
"""

from pathlib import Path

DOC = Path("/home/z/my-project/metabolic-curvature-measure/download/SUBMISSION_PACKAGE_LINKS.md")

text = DOC.read_text()

def edit(old: str, new: str, label: str) -> None:
    global text
    n = text.count(old)
    assert n == 1, f"[{label}] anchor count = {n} (expected 1)"
    text = text.replace(old, new, 1)
    print(f"[{label}] OK")

# --- Edit 1: header generation line gains the 2026-09-25 update marker ------
edit(
    "Generated 2026-09-24 (V22/V15 Zenodo-archive round + v27 package round: journal_manuscript_v22 + companion_categorical_v15;\n",
    "Generated 2026-09-24 (V22/V15 Zenodo-archive round + v27 package round: journal_manuscript_v22 + companion_categorical_v15;\nzip-visibility update 2026-09-25 (version-named zip copies + where-to-find\nclarifier); no manuscript, PDF, or package byte changes;\n",
    "header-generation-line",
)

# --- Edit 2: 'WHERE THE CURRENT ZIPS LIVE' clarifier before the V22/V15 note
WHERE_BLOCK = """WHERE THE CURRENT ZIPS LIVE (added 2026-09-25, zip-visibility round,
all links byte-verified against the live GitHub main branch this round):
- CURRENT packages (the ones to download and submit): the two GitHub
  files -- download/submission_main_dam.zip (v27 build; contains
  journal_manuscript_v22.tex; MD5 04d10994cded754c13b3869452618ddf) and
  download/submission_companion_dam.zip (v27 build; contains
  companion_categorical_v15.tex; MD5 482b92eb44f2de5653e08c7653683877).
- Version-named byte-identical copies (added this round, because the
  unversioned filenames are reused by every build round):
  download/submission_main_dam_v22.zip and
  download/submission_companion_dam_v15.zip.
- ARCHIVAL snapshots (one generation behind by design): the two Zenodo
  version DOIs 10.5281/zenodo.22941018 and 10.5281/zenodo.22940820 hold
  the v26 packages (journal_manuscript_v21.tex /
  companion_categorical_v14.tex), exactly as recorded in the manuscripts'
  data availability statements. If the deposits are refreshed with the
  v27 packages, the concept DOIs (10.5281/zenodo.22941017 /
  10.5281/zenodo.22940819) resolve to the latest version.

"""
edit(
    "Repository\nis public, so every link is directly accessible.\n\nRevision note (2026-09-24, V22/V15 Zenodo-archive round + v27\n",
    "Repository\nis public, so every link is directly accessible.\n\n"
    + WHERE_BLOCK
    + "Revision note (2026-09-24, V22/V15 Zenodo-archive round + v27\n",
    "where-zips-live-block",
)

# --- Edit 3: main package table row for the version-named copy -------------
MAIN_ROW_OLD = "| **One-file upload ZIP (compile-ready, DAM README; v27 build, fresh-dir verified 37 pp)** | — | [download/submission_main_dam.zip](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/submission_main_dam.zip) |\n"
MAIN_ROW_NEW = MAIN_ROW_OLD + "| **Version-named copy of the one-file upload ZIP (byte-identical to submission_main_dam.zip; v27 build containing journal_manuscript_v22.tex; added 2026-09-25 for unambiguous version identification)** | — | [download/submission_main_dam_v22.zip](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/submission_main_dam_v22.zip) |\n"
edit(MAIN_ROW_OLD, MAIN_ROW_NEW, "main-package-row")

# --- Edit 4: companion package table row for the version-named copy --------
COMP_ROW_OLD = "| **One-file upload ZIP (compile-ready, DAM README; v27 build, fresh-dir verified 76 pp)** | — | [download/submission_companion_dam.zip](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/submission_companion_dam.zip) |\n"
COMP_ROW_NEW = COMP_ROW_OLD + "| **Version-named copy of the one-file upload ZIP (byte-identical to submission_companion_dam.zip; v27 build containing companion_categorical_v15.tex; added 2026-09-25 for unambiguous version identification)** | — | [download/submission_companion_dam_v15.zip](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/submission_companion_dam_v15.zip) |\n"
edit(COMP_ROW_OLD, COMP_ROW_NEW, "companion-package-row")

DOC.write_text(text)
print(f"\nWrote {DOC} ({len(text)} chars)")
print("Sanity: mentions of submission_main_dam_v22.zip =",
      text.count("submission_main_dam_v22.zip"))
print("Sanity: mentions of submission_companion_dam_v15.zip =",
      text.count("submission_companion_dam_v15.zip"))
print("Sanity: 'WHERE THE CURRENT ZIPS LIVE' present =",
      "WHERE THE CURRENT ZIPS LIVE" in text)
