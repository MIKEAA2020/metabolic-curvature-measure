#!/usr/bin/env python3
"""Retarget SUBMISSION_PACKAGE_LINKS.md to the merged-register round +
v18 package round (journal_manuscript_v15 + companion_categorical_v9)."""

p = "/home/z/my-project/metabolic-curvature-measure/download/SUBMISSION_PACKAGE_LINKS.md"
s = open(p).read()

# 1. Header generation line
old_head = ("Generated 2026-09-17 (abstract cap round + v17 package round:\n"
            "journal_manuscript_v14 + companion_categorical_v9). "
            "All repository links follow")
new_head = ("Generated 2026-09-17 (merged-register round + v18 package round:\n"
            "journal_manuscript_v15 + companion_categorical_v9). "
            "All repository links follow")
assert old_head in s, "header anchor not found"
s = s.replace(old_head, new_head)

# 2. New revision note inserted before the v17-round note
old_anchor = ("Revision note (2026-09-17, abstract cap round + v17 package "
              "round): the")
new_note = """Revision note (2026-09-17, merged-register round + v18 package round):
the author directive to jointly evaluate and verify the two humanized
audits (external_audits/humanized/gemini,grok humanized.txt: Gemini's
digest-style rewrite and Grok's complete restructure) and to produce v15
adopting the merged rewrite with Gemini's register primary was executed
on NEW versioned files (prior versions untouched) --
scripts/journal_manuscript_v15.tex (from v14) plus its refs copies;
companion_categorical_v9.tex unchanged. Joint evaluation findings: both
audits numerically faithful to v14's audited claims except flagged
items that were evaluated and NOT adopted (Gemini's decile
dispersions +/-0.12//+/-0.08 and PaxDb p-value 1.2e-12 -- not audited
claims; the model sizes 2,712/1,366 -- not in the audited set; the
noise-floor compression 10^-11 to 10^-14 -- looser than v14's
statement; Grok's stale "98 checks" -- the current count is 301; and
Grok's British spellings). v15 harvests the twelve remaining genuine
register deltas, Gemini-weighted: concrete rerouting triggers and the
operational-bottleneck gloss in the intro object paragraph; the
impulse image in the In-words gloss; Gemini's opening question for
the refinement bridge; the city-street analogy in the exact-
counterexample remark; the In-words toll sentence after the regime
dichotomy; the value-vs-flux guiding question; the more-than-double
decile gloss; the path-robustness question; the plain tie-break lead
and question; the active-set-architecture coda on the tie-break
findings; the translational-buffering interpretation paragraph in the
Discussion; and the protein-layer-null tightening. The abstract is
byte-identical to v14 (254 audit-style words, under the 255 cap).
Nothing lost: verify_v15_completeness.py ALL COMPLETE (number
multiset delta = the version digit, the digits of the new
\\citet{kochanowski2013} key and \\S\\ref{sec:e27} label, and the three
re-quoted audited body claims +0.419/-0.083/366; citation census =
kochanowski2013 +1; label/environment/section censuses and the
bibliography identical). Verified: audit_v23_numbers.py
(make_audit_v23.py) 301/301 PASS; pattern_sweep_v16 16/16 clean on
both; tectonic main 30 pp / companion 75 pp, 0 errors / 0 undefined
references / 0 '??'; clickable mailto + ORCID annotations verified
via qpdf; identical overfull-box profile to v14 (no new typesetting
defects); VLM CLEAN on the four edited pages (pp. 2, 8, 9, 17); ZIPs
rebuilt via build_submission_zips_v18.sh with fresh-dir standalone
compiles re-verified (30/75 pp); download copies and ZIP contents
byte-identical to scripts; TAC cover letter retargeted to v15.

""" + old_anchor
assert old_anchor in s, "revision-note anchor not found"
s = s.replace(old_anchor, new_note)

# 3. Retarget current-package rows (main) v14 -> v15
old_pdf_row_desc = ("universal Gemini-register revision of narrative prose "
                    "throughout, clickable email and ORCID, "
                    "brevity round applied, abstract rebuilt on Gemini's "
                    "abstract and trimmed under the author's 255-word cap; "
                    "prior versions retained as separate files")
new_pdf_row_desc = ("universal Gemini-register revision of narrative prose "
                    "throughout, clickable email and ORCID, "
                    "brevity round applied, abstract rebuilt on Gemini's "
                    "abstract and trimmed under the author's 255-word cap, "
                    "merged-register round applied (joint Gemini/Grok audit "
                    "evaluation, Gemini-weighted); "
                    "prior versions retained as separate files")
assert old_pdf_row_desc in s, "pdf row description anchor not found"
s = s.replace(old_pdf_row_desc, new_pdf_row_desc)

for a, b in [("journal_manuscript_v14.pdf", "journal_manuscript_v15.pdf"),
             ("journal_manuscript_v14.tex", "journal_manuscript_v15.tex"),
             ("journal_manuscript_v14_bmb_refs.tex",
              "journal_manuscript_v15_bmb_refs.tex"),
             ("journal_manuscript_v14_refs.bib",
              "journal_manuscript_v15_refs.bib")]:
    s = s.replace(a, b)

# 4. Checklist updates
s = s.replace(
    "refs, six keywords, v14 two-paragraph abstract in Gemini's register,",
    "refs, six keywords, v15 two-paragraph abstract in Gemini's register,")
s = s.replace(
    "PASS against journal_manuscript_v14.tex + companion_categorical_v9.tex;",
    "PASS against journal_manuscript_v15.tex + companion_categorical_v9.tex;")
s = s.replace("audit_v22 301/301", "audit_v23 301/301")

open(p, "w").write(s)
print("SUBMISSION_PACKAGE_LINKS.md retargeted to v15 / v18 package round")
