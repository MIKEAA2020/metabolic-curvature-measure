#!/usr/bin/env python3
"""V18 JTB-alignment round: build scripts/journal_manuscript_v18.tex
(from v17; v17 and all earlier versions untouched).

Per the author directive: target venue = Journal of Theoretical Biology
(Elsevier); title, abstract, keywords, sections, and package must be in
full agreement with the latest (v17) manuscript findings and with JTB's
Guide for Authors (verified live 2026-09-21):
  - abstract "does not exceed 250 words"  -> trim 254 -> 249 audit-style
    words via five word-level trims (every number, in-words gloss, and
    connective kept);
  - keywords 1-7                          -> add the seventh term
    'path dependence' (aligns indexing with the holonomy / 66%
    non-reversion / construction-order / memory findings);
  - CRediT authorship contribution        -> recast the Author
    Contributions backmatter in the CRediT taxonomy;
  - Highlights: separate editable file    -> download/highlights_jtb.docx
    (built by scripts/v18_make_highlights.js; 5 bullets, each <= 85
    characters incl. spaces);
  - article type 'Regular Article'        -> cover letter retarget.
Mechanical retargets: header comment (BMB -> JTB, stale v14/v16 refs
names fixed), reference list carried to the venue-neutral
journal_manuscript_v18_refs.tex (29 entries, byte-identical to the v17
list; the .bib database likewise copied to v18 naming).
NO number is added or removed; every v17 numerical claim is unchanged.
"""
import re
import shutil

BASE = "/home/z/my-project/metabolic-curvature-measure/"
S = BASE + "scripts/"

v17 = open(S + "journal_manuscript_v17.tex").read()
tex = v17
applied = []


def rep(old, new, tag):
    global tex
    assert old in tex, f"ANCHOR NOT FOUND for {tag}: {old[:70]!r}"
    assert tex.count(old) == 1, f"ANCHOR NOT UNIQUE for {tag}"
    tex = tex.replace(old, new)
    applied.append(tag)


# ---- 1. Header comment: venue + version + refs-name fixes ---------------
rep("%  journal_manuscript_v14.tex -- main manuscript.\n"
    "%  Target journal: Bulletin of Mathematical Biology (Springer).\n"
    "%  Author-year citations (natbib); reference list in\n"
    "%  journal_manuscript_v16_bmb_refs.tex. Long technical proofs are",
    "%  journal_manuscript_v18.tex -- main manuscript.\n"
    "%  Target journal: Journal of Theoretical Biology (Elsevier).\n"
    "%  Author-year citations (natbib); reference list in\n"
    "%  journal_manuscript_v18_refs.tex. Long technical proofs are",
    "header: venue + version + refs name")

# ---- 2. V18 round note (after the V17 note, before the v15 note) --------
V18_NOTE = """%  V18 JTB-alignment round (v17 -> v18), per the author directive to
%  target the Journal of Theoretical Biology: header retargeted from
%  BMB to JTB; the abstract trimmed 254 -> 249 audit-style words
%  under JTB's 250-word cap (five word-level trims; every number,
%  both in-words glosses, and the full connective arc kept); the
%  keyword list gains a seventh term, 'path dependence' (JTB allows
%  1-7), aligning indexing with the path-dependence findings
%  (holonomy, 66% non-reverting cycles, the construction-order rule,
%  the memory deduction); the Author Contributions backmatter is
%  recast in the CRediT taxonomy (required by JTB); the reference
%  list is carried to the venue-neutral journal_manuscript_v18_refs.tex
%  (29 entries, byte-identical to the v17 list). A separate
%  highlights file (download/highlights_jtb.docx, 5 bullets, each
%  <= 85 characters incl. spaces) accompanies the package per JTB's
%  Highlights requirement. No number added or removed; every v17
%  numerical claim unchanged (audit_v26 347/347). v17 and all
%  earlier versions untouched.
"""
rep("%  covered by audit_v25_numbers.py (344/344). v16 and all earlier\n"
    "%  versions untouched.\n",
    "%  covered by audit_v25_numbers.py (344/344). v16 and all earlier\n"
    "%  versions untouched.\n" + V18_NOTE,
    "v18 round note")

# ---- 3. Abstract trims (254 -> 249 audit-style words) -------------------
rep("abruptly at bottlenecks. Here we show that the response's true\n"
    "``curvature'' is not",
    "abruptly at bottlenecks. Here we show the response's true\n"
    "``curvature'' is not",
    "abstract trim 1: 'that' after 'we show'")
rep("not change smoothly but follow piecewise-linear trajectories, changing slope\n"
    "abruptly at bottlenecks.",
    "not change smoothly but follow piecewise-linear trajectories, changing slope\n"
    "at bottlenecks.",
    "abstract trim 2: 'abruptly'")
rep("$93.4$--$100.0\%$ of second-order adjustment concentrates at discrete\n"
    "bottleneck transitions.",
    "$93.4$--$100.0\%$ of second-order adjustment concentrates at\n"
    "bottleneck transitions.",
    "abstract trim 3: 'discrete' (second occurrence)")
rep("robust across tie-breaking rules and stress axes. Induced\n"
    "genes sit in operons of the global carbon and energy regulons;",
    "robust across tie-breaking rules and stress axes. Induced\n"
    "genes sit in operons of global carbon and energy regulons;",
    "abstract trim 4: 'the' before 'global carbon'")
rep("discrete geometry, and transcriptional regulation into an\n"
    "accessible, predictive foundation for metabolic systems biology.",
    "discrete geometry, and transcriptional regulation into a\n"
    "predictive foundation for metabolic systems biology.",
    "abstract trim 5: 'accessible'")

# ---- 4. Keywords: seventh term (JTB allows 1-7) --------------------------
rep(" pdfkeywords={flux balance analysis, metabolic rerouting,\n"
    "              active-set curvature, transcriptional regulation,\n"
    "              translational buffering, epistasis}}",
    " pdfkeywords={flux balance analysis, metabolic rerouting,\n"
    "              active-set curvature, transcriptional regulation,\n"
    "              translational buffering, epistasis, path dependence}}",
    "pdfkeywords: + path dependence")
rep("\\noindent\\textbf{Keywords:} flux balance analysis; metabolic\n"
    "rerouting; active-set curvature; transcriptional regulation;\n"
    "translational buffering; epistasis",
    "\\noindent\\textbf{Keywords:} flux balance analysis; metabolic\n"
    "rerouting; active-set curvature; transcriptional regulation;\n"
    "translational buffering; epistasis; path dependence",
    "keywords line: + path dependence")

# ---- 5. CRediT authorship contribution statement -------------------------
rep(r"""\section*{Author Contributions}
A.A. conceived the study design, developed the methodology and
analysis code, performed the data analysis, drafted and revised
the manuscript.""",
    r"""\section*{CRediT Authorship Contribution Statement}
\textbf{Amin Abaee:} \emph{Conceptualization, Methodology, Software,
Validation, Formal analysis, Investigation, Data curation, Writing --
original draft, Writing -- review and editing, Visualization.}""",
    "CRediT authorship statement")

# ---- 6. Reference list pointer: venue-neutral file name ------------------
rep(r"\input{journal_manuscript_v17_bmb_refs}",
    r"\input{journal_manuscript_v18_refs}",
    "input: v18 refs")

# ---- write v18 tex -------------------------------------------------------
open(S + "journal_manuscript_v18.tex", "w").write(tex)

# ---- 7. Refs file: venue-neutral name, header updated --------------------
refs = open(S + "journal_manuscript_v17_bmb_refs.tex").read()
old_ref_hdr = """% journal_manuscript_v17_bmb_refs.tex -- references for the v17
% revision. Content identical to the v7 reference list (itself the
% v3 list, generated by scripts/build_bmb_refs.py): all proof-literature
% sources required by the complete-proof revision (Rockafellar 1970,
% Gutierrez 2001, Borrelli et al. 2003, Ziegler 1995, Danskin 1967,
% Cheeger et al. 1984, Regge 1961, Billingsley 1999, Villani 2009,
% Alexandrov 1939) were already present among the 27 entries, so no
% additions were needed.
% Springer/BMB author-year references, ALPHABETICAL by first
% author surname, with natbib optional labels."""
new_ref_hdr = """% journal_manuscript_v18_refs.tex -- references for the v18
% JTB-alignment round. Entries byte-identical to the v17 list
% (itself the v7 list, generated by scripts/build_bmb_refs.py): the
% 27-entry v3 base + kacser1973 + heinrich1974 from the v17 MCA
% comparison. All proof-literature sources required by the
% complete-proof revision (Rockafellar 1970, Gutierrez 2001,
% Borrelli et al. 2003, Ziegler 1995, Danskin 1967, Cheeger et al.
% 1984, Regge 1961, Billingsley 1999, Villani 2009, Alexandrov 1939)
% were already present among the 27 base entries.
% Author-year references (natbib), ALPHABETICAL by first author
% surname, with optional labels; venue-neutral for the JTB target
% (Elsevier accepts any consistent style at first submission)."""
assert old_ref_hdr in refs, "refs header anchor not found"
refs18 = refs.replace(old_ref_hdr, new_ref_hdr)
open(S + "journal_manuscript_v18_refs.tex", "w").write(refs18)

# bib database copy under the v18 name
shutil.copyfile(S + "journal_manuscript_v17_refs.bib",
                S + "journal_manuscript_v18_refs.bib")

# ---- 8. download copies ---------------------------------------------------
shutil.copyfile(S + "journal_manuscript_v18.tex",
                BASE + "download/journal_manuscript_v18.tex")
shutil.copyfile(S + "journal_manuscript_v18_refs.tex",
                BASE + "download/journal_manuscript_v18_refs.tex")
shutil.copyfile(S + "journal_manuscript_v18_refs.bib",
                BASE + "download/journal_manuscript_v18_refs.bib")

# ---- 9. self-verification -------------------------------------------------
m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex, re.S)
inner = m.group(1)
nwords = len(re.findall(r"[A-Za-z0-9\\-]+",
                        re.sub(r"\\[a-zA-Z]+", " ", inner)))
kw_line = re.search(r"Keywords:\}\s*(.*?)(?:\n\n|\n\\\\bigskip)", tex,
                    re.S).group(1)
n_kw = kw_line.count(";") + 1

nums17 = re.findall(r"\d+(?:\.\d+)?",
                    re.sub(r"(?<!\\)%.*", "", v17))
nums18 = re.findall(r"\d+(?:\.\d+)?",
                    re.sub(r"(?<!\\)%.*", "", tex))
from collections import Counter
d17, d18 = Counter(nums17), Counter(nums18)
removed_nums = d17 - d18
added_nums = d18 - d17

print(f"applied edits: {len(applied)}")
for t in applied:
    print("  -", t)
print(f"abstract audit-style words: 254 -> {nwords}  (JTB cap 250)")
print(f"keywords: 6 -> {n_kw}  (JTB range 1-7)")
print(f"numeric tokens removed: {dict(removed_nums)}")
print(f"numeric tokens added:   {dict(added_nums)}")
print(f"refs entries: {refs18.count(chr(92) + 'bibitem')}")
assert nwords == 249, f"abstract word count {nwords} != 249"
assert n_kw == 7, f"keywords {n_kw} != 7"
# The ONLY permitted numeric delta is the version digit inside the
# \input filename (journal_manuscript_17_bmb_refs -> _18_refs), the
# mechanical version-bump pattern of every prior round.
assert dict(removed_nums) == {"17": 1} and dict(added_nums) == {"18": 1}, \
    f"unexpected numeric drift: {dict(removed_nums)} / {dict(added_nums)}"
assert refs18.count("\\bibitem") == 29
print("ALL V18 PATCH CHECKS PASS")
