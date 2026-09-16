#!/usr/bin/env python3
"""Retarget SUBMISSION_PACKAGE_LINKS.md to the v8/v7 + v11-package round."""

p = "/home/z/my-project/metabolic-curvature-measure/download/SUBMISSION_PACKAGE_LINKS.md"
s = open(p).read()

# 1. Header generation line
s = s.replace(
    "Generated 2026-09-16 (reader-oriented prose revision + v10 package\n"
    "round: journal_manuscript_v7 + companion_categorical_v6).",
    "Generated 2026-09-17 (merged-synthesis revision + v11 package\n"
    "round: journal_manuscript_v8 + companion_categorical_v7).")

# 2. New revision note inserted after the "revision note" anchor line's
#    known predecessor (insert before the 2026-09-16 note)
old_anchor = ("Revision note (2026-09-16, reader-oriented prose revision + v10\n"
              "package round):")
new_note = """Revision note (2026-09-17, merged-synthesis revision + v11 package
round): new manuscript versions as separate files, prior versions
untouched -- scripts/journal_manuscript_v8.tex (main, BMB; from v7)
and scripts/companion_categorical_v7.tex (companion, TAC; from v6).
The revision implements the merged synthesis plan built from the
evaluated external humanization attempts (plan at
download/Humanized_Versions_Evaluation_and_Synthesis_Plan.md):
main -- the abstract's robustness clauses compressed to one sentence
with the numbers kept in the body (238 words, within the 150-250
guideline; hook, primary numbers, punchline placement, and specific
closer unchanged; the n=424 parenthetical disambiguated to "424
evaluated genes"); a growth-rate gloss at the value function's first
appearance; a zero-cost-substitution gloss inside the coupling
theorem; a Discussion sentence tying the transcription--value-layer
dissociation to the coupling structure; the Reproducibility
check-count reconciled (98 -> 301); two process-flavored remark
titles recast factually. Companion -- the boundary-rule
three-fold-failure breakdown in the 2-categorical-span remark; the
thermostat/cell contrast making the autopoiesis--homeostasis
distinction concrete; a physical reading of the Zeno
self-measurement schedule; two proof-provenance phrasings recast.
All numerical claims unchanged: audit_v16_numbers.py 301/301 PASS;
builds: main 29 pp, companion 74 pp, zero errors / zero undefined
references; ZIPs rebuilt via build_submission_zips_v11.sh with
fresh-dir standalone tectonic compiles verified (29/74 pp); cover
letters retargeted to the new version filenames.

"""
assert old_anchor in s
s = s.replace(old_anchor, new_note + old_anchor, 1)

# 3. Main-paper rows v7 -> v8
s = s.replace(
    "| Manuscript PDF (28 pp, full proofs in appendices, declarations in backmatter; reader-oriented prose revision: plain-problem abstract, glossed definitions, plan of the paper, restructured Limitations; prior versions retained as separate files) | [download/journal_manuscript_v7.pdf]",
    "| Manuscript PDF (29 pp, full proofs in appendices, declarations in backmatter; merged-synthesis revision: compressed abstract robustness clause, glossed value function and coupling, reconciled check count; prior versions retained as separate files) | [download/journal_manuscript_v8.pdf]")
s = s.replace(
    "| LaTeX source | [scripts/journal_manuscript_v7.tex]",
    "| LaTeX source | [scripts/journal_manuscript_v8.tex]")
s = s.replace(
    "| Reference list (BMB alphabetical, 27 entries) | [scripts/journal_manuscript_v7_bmb_refs.tex]",
    "| Reference list (BMB alphabetical, 27 entries) | [scripts/journal_manuscript_v8_bmb_refs.tex]")
s = s.replace(
    "| BibTeX database | [scripts/journal_manuscript_v7_refs.bib]",
    "| BibTeX database | [scripts/journal_manuscript_v8_refs.bib]")
s = s.replace(
    "files, upload them together with `journal_manuscript_v7_bmb_refs.tex` and",
    "files, upload them together with `journal_manuscript_v8_bmb_refs.tex` and")
s = s.replace(
    "contains the .tex, the input'ed reference list, the .bib database, and all\nsix figures at the exact relative subpaths the .tex expects — verified to\ncompile standalone, 28 pp, 0 errors)",
    "contains the .tex, the input'ed reference list, the .bib database, and all\nsix figures at the exact relative subpaths the .tex expects — verified to\ncompile standalone, 29 pp, 0 errors)")
# blob/raw URL tails for the swapped rows
for a, b in [("journal_manuscript_v7.pdf", "journal_manuscript_v8.pdf"),
             ("journal_manuscript_v7.tex", "journal_manuscript_v8.tex"),
             ("journal_manuscript_v7_bmb_refs.tex",
              "journal_manuscript_v8_bmb_refs.tex"),
             ("journal_manuscript_v7_refs.bib",
              "journal_manuscript_v8_refs.bib")]:
    s = s.replace(f"blob/main/download/{a})", f"blob/main/download/{b})")
    s = s.replace(f"raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/{a})",
                  f"raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/{b})")
    s = s.replace(f"blob/main/scripts/{a})", f"blob/main/scripts/{b})")
    s = s.replace(f"raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/{a})",
                  f"raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/{b})")

# 4. Companion rows v6 -> v7
s = s.replace(
    "| Manuscript PDF (75 pp; reader-oriented prose revision: plain-problem abstract opening, glossed introduction, section leads; prior versions retained as separate files) | [download/companion_categorical_v6.pdf]",
    "| Manuscript PDF (74 pp; merged-synthesis revision: boundary-rule breakdown, autopoiesis contrast, Zeno physical reading; prior versions retained as separate files) | [download/companion_categorical_v7.pdf]")
s = s.replace(
    "| LaTeX source | [scripts/companion_categorical_v6.tex]",
    "| LaTeX source | [scripts/companion_categorical_v7.tex]")
s = s.replace(
    "| BibTeX database | [scripts/companion_refs_v6.bib]",
    "| BibTeX database | [scripts/companion_refs_v7.bib]")
for a, b in [("companion_categorical_v6.pdf", "companion_categorical_v7.pdf"),
             ("companion_categorical_v6.tex", "companion_categorical_v7.tex"),
             ("companion_refs_v6.bib", "companion_refs_v7.bib")]:
    s = s.replace(f"blob/main/download/{a})", f"blob/main/download/{b})")
    s = s.replace(f"raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/{a})",
                  f"raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/{b})")
    s = s.replace(f"blob/main/scripts/{a})", f"blob/main/scripts/{b})")
    s = s.replace(f"raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/{a})",
                  f"raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/{b})")

# 5. Checklist audit line
s = s.replace(
    "audit_v14 301/301\nPASS against journal_manuscript_v7.tex + companion_categorical_v6.tex;",
    "audit_v16 301/301\nPASS against journal_manuscript_v8.tex + companion_categorical_v7.tex;")

# 6. Paper-2 header page count
s = s.replace("Curvature (Research Article; 74 pp; electronic-only, free — no author charges).",
              "Curvature (Research Article; 74 pp current build; electronic-only, free — no author charges).")

open(p, "w").write(s)
import re
left = re.findall(r"journal_manuscript_v7|companion_categorical_v6|companion_refs_v6", s)
print("leftover stale refs (expected: none in current-package rows; historical notes may keep theirs):", len(left))
