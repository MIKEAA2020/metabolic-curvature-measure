#!/usr/bin/env python3
"""Create audit_v22_numbers.py from audit_v21_numbers.py.

Retargets the audit to the abstract cap round: main
journal_manuscript_v13.tex -> journal_manuscript_v14.tex. Companion
stays at companion_categorical_v9.tex (zero companion edits this
round). The text change is the abstract only (trimmed under the
author's 255-word cap: 269 -> 254 audit-style words, register kept on
Gemini's abstract, every number kept); the body is untouched, so every
numerical claim is unchanged from v13/v9.
"""
import re

src = open("audit_v21_numbers.py").read()

# 1. Path retargets (main v13 -> v14)
old_tex2 = ('tex2 = open(os.path.join(BASE, "scripts",\n'
            '                         "journal_manuscript_v13.tex")).read()')
new_tex2 = ('tex2 = open(os.path.join(BASE, "scripts",\n'
            '                         "journal_manuscript_v14.tex")).read()')
assert old_tex2 in src, "tex2 open anchor not found"
src = src.replace(old_tex2, new_tex2)

old_chk = '"journal_manuscript_v13_bmb_refs" in tex2'
new_chk = '"journal_manuscript_v14_bmb_refs" in tex2'
assert old_chk in src, "bmb_refs check anchor not found"
src = src.replace(old_chk, new_chk)

old_bmb = ('bmb_refs = open(os.path.join(BASE, "scripts",\n'
           '                 "journal_manuscript_v13_bmb_refs.tex")).read()')
new_bmb = ('bmb_refs = open(os.path.join(BASE, "scripts",\n'
           '                 "journal_manuscript_v14_bmb_refs.tex")).read()')
assert old_bmb in src, "bmb_refs open anchor not found"
src = src.replace(old_bmb, new_bmb)

# 2. Main docstring retarget (the v21 round-description block)
old_doc = '''Numeric consistency audit of journal_manuscript_v13.tex +
companion_categorical_v9.tex (abstract round: the main-paper abstract
rebuilt on Gemini's abstract -- two-paragraph theory/biology structure,
narrative connectives, in-words glosses for h and L_var, plain
field-level closer, protein-layer dissociation numbers now quoted
(r = -0.083, n = 366, both audited body claims); body untouched;
companion unchanged; every numerical claim unchanged from v12/v9;
extends the v20
audit) extends the v11 audit'''
new_doc = '''Numeric consistency audit of journal_manuscript_v14.tex +
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
assert old_doc in src, "v21 docstring anchor not found"
src = src.replace(old_doc, new_doc)

# 3. Companion stays at v9: no companion replace this round.

# 4. Output ledger paths
for old, new in [('"v21_number_audit.json"', '"v22_number_audit.json"'),
                 ('"v21_number_audit.md"', '"v22_number_audit.md"'),
                 ('download/deepseek_bridge/v21_number_audit.json',
                  'download/deepseek_bridge/v22_number_audit.json'),
                 ('download/deepseek_bridge/v21_number_audit.md',
                  'download/deepseek_bridge/v22_number_audit.md'),
                 ('"v21_number_audit"', '"v22_number_audit"')]:
    if old in src:
        src = src.replace(old, new)

# 5. Verify no stale version references remain
leftovers_v13 = re.findall(r'journal_manuscript_v13', src)
assert not leftovers_v13, f"stale v13 references: {leftovers_v13}"

open("audit_v22_numbers.py", "w").write(src)
print("audit_v22_numbers.py written:",
      len(src), "bytes;",
      "v13 refs left:", len(leftovers_v13))
