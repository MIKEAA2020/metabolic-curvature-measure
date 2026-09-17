#!/usr/bin/env python3
"""Create audit_v23_numbers.py from audit_v22_numbers.py.

Retargets the audit to the merged-register round: main
journal_manuscript_v14.tex -> journal_manuscript_v15.tex. Companion
stays at companion_categorical_v9.tex (zero companion edits this
round). The text change is register-only: twelve adjudicated
merged-register edits from the joint evaluation of the two humanized
audits (external_audits/humanized/gemini,grok humanized.txt), Gemini
weighted first; the abstract is untouched; the only new numbers are
re-quotes of audited body claims (+0.419, -0.083, n = 366) in the
Discussion standby-model paragraph; the only new citation is
kochanowski2013 in that paragraph.
"""
import re

src = open("audit_v22_numbers.py").read()

# 1. Path retargets (main v14 -> v15)
old_tex2 = ('tex2 = open(os.path.join(BASE, "scripts",\n'
            '                         "journal_manuscript_v14.tex")).read()')
new_tex2 = ('tex2 = open(os.path.join(BASE, "scripts",\n'
            '                         "journal_manuscript_v15.tex")).read()')
assert old_tex2 in src, "tex2 open anchor not found"
src = src.replace(old_tex2, new_tex2)

old_chk = '"journal_manuscript_v14_bmb_refs" in tex2'
new_chk = '"journal_manuscript_v15_bmb_refs" in tex2'
assert old_chk in src, "bmb_refs check anchor not found"
src = src.replace(old_chk, new_chk)

old_bmb = ('bmb_refs = open(os.path.join(BASE, "scripts",\n'
           '                 "journal_manuscript_v14_bmb_refs.tex")).read()')
new_bmb = ('bmb_refs = open(os.path.join(BASE, "scripts",\n'
           '                 "journal_manuscript_v15_bmb_refs.tex")).read()')
assert old_bmb in src, "bmb_refs open anchor not found"
src = src.replace(old_bmb, new_bmb)

# 2. Main docstring retarget (the v22 round-description block)
old_doc = '''Numeric consistency audit of journal_manuscript_v14.tex +
companion_categorical_v9.tex (abstract cap round: the main-paper
abstract trimmed under the author's 255-word cap, 269 -> 254
audit-style words, with the register kept on Gemini's abstract -- the
M1 sweep qualifier and the statistics conventions "n ="/"evaluated"
dropped per Gemini's own plain forms, "fails in general" -> "fails
generically" (Gemini's exact word), the boundaries gloss compressed
to "the boundaries between active constraint sets", and function
words tightened; every number kept; body untouched; companion
unchanged; every numerical claim unchanged from v13/v9;
extends the v21
audit) extends the v11 audit'''
new_doc = '''Numeric consistency audit of journal_manuscript_v15.tex +
companion_categorical_v9.tex (merged-register round: joint
evaluation of the two humanized audits
external_audits/humanized/gemini,grok humanized.txt with Gemini's
prose and tone weighted first, Grok's sharpenings second, and v14 as
the completeness skeleton -- twelve surgical register edits
(concrete rerouting triggers and the operational-bottleneck gloss in
the intro object paragraph; the impulse image in the In-words gloss;
Gemini's opening question for the refinement bridge; the city-street
analogy in the exact-counterexample remark; the In-words toll
sentence after the regime dichotomy; the value-vs-flux guiding
question; the more-than-double decile gloss; the path-robustness
question; the plain tie-break lead and question; the
active-set-architecture coda; the translational-buffering
interpretation paragraph in the Discussion; the protein-layer-null
tightening); abstract untouched (still 254 audit-style words under
the 255-word cap); the only new numbers are re-quotes of audited
body claims (+0.419, -0.083, n = 366) in the Discussion paragraph;
companion unchanged; every numerical claim unchanged from v14/v9;
extends the v22
audit) extends the v11 audit'''
assert old_doc in src, "v22 docstring anchor not found"
src = src.replace(old_doc, new_doc)

# 3. Companion stays at v9: no companion replace this round.

# 4. Output ledger paths
for old, new in [('"v22_number_audit.json"', '"v23_number_audit.json"'),
                 ('"v22_number_audit.md"', '"v23_number_audit.md"'),
                 ('download/deepseek_bridge/v22_number_audit.json',
                  'download/deepseek_bridge/v23_number_audit.json'),
                 ('download/deepseek_bridge/v22_number_audit.md',
                  'download/deepseek_bridge/v23_number_audit.md'),
                 ('"v22_number_audit"', '"v23_number_audit"')]:
    if old in src:
        src = src.replace(old, new)

# 5. Verify no stale version references remain
leftovers_v14 = re.findall(r'journal_manuscript_v14', src)
assert not leftovers_v14, f"stale v14 references: {leftovers_v14}"

open("audit_v23_numbers.py", "w").write(src)
print("audit_v23_numbers.py written:",
      len(src), "bytes;",
      "v14 refs left:", len(leftovers_v14))
