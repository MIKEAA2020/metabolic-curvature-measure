#!/usr/bin/env python3
"""Update SUBMISSION_PACKAGE_LINKS.md for the 3rd-wave repair round:
main v3 -> v4 (28 pp), companion v2 -> v3 (63 pp), figure directory
renamed deepseek_bridge -> association_robustness, new revision note.
Every URL string keeps the repo/blob/main pattern that the links doc
verifies live."""
import sys

F = "download/SUBMISSION_PACKAGE_LINKS.md"
src = open(F).read()
n = 0


def rep(old, new, what, count=1):
    global src, n
    c = src.count(old)
    if c != count:
        print(f"FAIL [{what}]: found {c} (expected {count})")
        sys.exit(1)
    src = src.replace(old, new)
    n += 1
    print(f"ok   [{what}] x{c}")


# Header: generation date + revision note.
rep("""Generated 2026-09-03. All repository links verified live (HTTP 200 at `main`,
latest `main`); all journal links verified against the official journal or
society pages. Repository is public, so every link is directly accessible.""",
    """Generated 2026-09-14 (3rd-wave repair round). All repository links follow
the repo/blob/main pattern verified live in the 2026-09-03 pass; journal
links verified against the official journal or society pages. Repository
is public, so every link is directly accessible.

Revision note (2026-09-14): main is now `journal_manuscript_v4.tex`
(28 pp) and the companion is `companion_categorical_v3.tex` (63 pp).
The companion implements the eight-item repair set of the external
audit's synthesized ledger (one optic formalism, corrected
optic-colimit scope, one Hordijk-Steel catalysis condition, gluing
hypothesis alignment, Lévy-area normalization, enlarged contraction
box, battery-table consistency, restricted envelope domination),
restores the six audit-mandated citations (Hirota, Segura, Dittrich,
Handorf, Becker, Bravetti), and adds the external-data closures
(Keio E12/E15/E16; the COT/NE structural benchmark). The main paper
carries the four line-level corrections of its cross-check (bridge
sentence softened, generic-weights uniqueness step, semiconvexity
law, label/title fixes) plus the selection-rule count harmonization;
its figure directory is renamed `association_robustness/` (was
`deepseek_bridge/`).""",
    "links: header + revision note")

# Main paper section: version, pages, figure dir.
rep("""(Original Research Article; 27 pp; subscription route — no author charges).""",
    """(Original Research Article; 28 pp; subscription route — no author charges).""",
    "links: main pages 27->28")
rep("download/journal_manuscript_v3.pdf", "download/journal_manuscript_v4.pdf", "links: main PDF v4", count=3)
rep("scripts/journal_manuscript_v3.tex", "scripts/journal_manuscript_v4.tex", "links: main tex v4", count=3)
rep("""| Manuscript PDF (27 pp, full proofs in appendices, declarations in backmatter) |""",
    """| Manuscript PDF (28 pp, full proofs in appendices, declarations in backmatter) |""",
    "links: main PDF page count")
rep("download/deepseek_bridge/v5_e24_recalibration.png",
    "download/association_robustness/v5_e24_recalibration.png",
    "links: fig dir rename 1", count=2)
rep("download/deepseek_bridge/v7_path_robustness.png",
    "download/association_robustness/v7_path_robustness.png",
    "links: fig dir rename 2", count=2)
rep("download/deepseek_bridge/v8_tiebreak_robustness.png",
    "download/association_robustness/v8_tiebreak_robustness.png",
    "links: fig dir rename 3", count=2)
rep("download/deepseek_bridge/e32_event_measure_stabilization.png",
    "download/association_robustness/e32_event_measure_stabilization.png",
    "links: fig dir rename 4", count=2)
rep("""contains the .tex, the input'ed reference list, the .bib database, and all
six figures at the exact relative subpaths the .tex expects — verified to
compile standalone, 27 pp, 0 errors). If instead you upload individual
files, upload them together with `journal_manuscript_v3_bmb_refs.tex` and
the three figure subfolders (`m1_m3/`, `alexandrov_bridge/`,
`deepseek_bridge/`) so the paths resolve; the .tex now searches both the""",
    """contains the .tex, the input'ed reference list, the .bib database, and all
six figures at the exact relative subpaths the .tex expects — verified to
compile standalone, 28 pp, 0 errors). If instead you upload individual
files, upload them together with `journal_manuscript_v3_bmb_refs.tex` and
the three figure subfolders (`m1_m3/`, `alexandrov_bridge/`,
`association_robustness/`) so the paths resolve; the .tex now searches both the""",
    "links: main build note (28 pp, renamed dir)")

# Companion section: version, pages.
rep("""Curvature (Research Article; 57 pp; electronic-only, free — no author charges).""",
    """Curvature (Research Article; 63 pp; electronic-only, free — no author charges).""",
    "links: companion page count")
rep("download/companion_categorical_v2.pdf", "download/companion_categorical_v3.pdf",
    "links: companion PDF v3", count=3)
rep("scripts/companion_categorical_v2.tex", "scripts/companion_categorical_v3.tex",
    "links: companion tex v3", count=3)
rep("companion_categorical_v2.tex", "companion_categorical_v3.tex",
    "links: any remaining companion v2 mentions")

# Any remaining deepseek_bridge mention (e.g. notes rows).
rep("deepseek_bridge/", "association_robustness/", "links: residual dir mentions")

open(F, "w").write(src)
print(f"\nlinks doc updated: {n} edits")
