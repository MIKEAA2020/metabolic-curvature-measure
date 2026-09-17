#!/usr/bin/env python3
"""Create audit_v21_numbers.py from audit_v20_numbers.py.

Retargets the audit to the abstract round: main
journal_manuscript_v12.tex -> journal_manuscript_v13.tex. Companion
stays at companion_categorical_v9.tex (zero companion edits this
round). The text change is the abstract only (rebuilt on Gemini's
abstract: two-paragraph structure, narrative connectives, in-words
glosses, plain field-level closer, protein-layer numbers now quoted);
the body is untouched, so every numerical claim is unchanged from
v12/v9 (the abstract's added numbers r = -0.083 and n = 366 are
themselves audited body claims re-quoted from the protein-layer null).
"""
import re

src = open("audit_v20_numbers.py").read()

# 1. Path retargets (main v12 -> v13)
src = src.replace(
    'tex2 = open(os.path.join(BASE, "scripts",\n'
    '                         "journal_manuscript_v12.tex")).read()',
    'tex2 = open(os.path.join(BASE, "scripts",\n'
    '                         "journal_manuscript_v13.tex")).read()')
src = src.replace('"journal_manuscript_v12_bmb_refs" in tex2',
                  '"journal_manuscript_v13_bmb_refs" in tex2')
src = src.replace(
    'bmb_refs = open(os.path.join(BASE, "scripts",\n'
    '                 "journal_manuscript_v12_bmb_refs.tex")).read()',
    'bmb_refs = open(os.path.join(BASE, "scripts",\n'
    '                 "journal_manuscript_v13_bmb_refs.tex")).read()')

# 2. Main docstring retarget (before the companion replace)
old_doc = '''Numeric consistency audit of journal_manuscript_v12.tex +
companion_categorical_v9.tex (brevity round: two register tightenings
in the main paper -- the Positioning paragraph's "We find that it
does." shortened to "It does." with the dependent "We also find
that" connective dropped, and the "at this point" filler removed from
the protein-layer central question; companion unchanged; every
numerical claim unchanged from v11/v9; extends the v19
audit) extends the v11 audit'''
new_doc = '''Numeric consistency audit of journal_manuscript_v13.tex +
companion_categorical_v9.tex (abstract round: the main-paper abstract
rebuilt on Gemini's abstract -- two-paragraph theory/biology structure,
narrative connectives, in-words glosses for h and L_var, plain
field-level closer, protein-layer dissociation numbers now quoted
(r = -0.083, n = 366, both audited body claims); body untouched;
companion unchanged; every numerical claim unchanged from v12/v9;
extends the v20
audit) extends the v11 audit'''
assert old_doc in src, "v20 docstring anchor not found"
src = src.replace(old_doc, new_doc)

# 3. Companion stays at v9: no companion replace this round.

# 4. Output ledger paths
src = src.replace('"v20_number_audit.json"', '"v21_number_audit.json"')
src = src.replace('"v20_number_audit.md"', '"v21_number_audit.md"')
src = src.replace('download/deepseek_bridge/v20_number_audit.json',
                  'download/deepseek_bridge/v21_number_audit.json')
src = src.replace('download/deepseek_bridge/v20_number_audit.md',
                  'download/deepseek_bridge/v21_number_audit.md')
src = src.replace("v20_number_audit", "v21_number_audit")

# 5. Verify no stale version references remain
leftovers_v12 = re.findall(r'journal_manuscript_v12', src)
assert not leftovers_v12, f"stale v12 references: {leftovers_v12}"

open("audit_v21_numbers.py", "w").write(src)
print("audit_v21_numbers.py written:",
      len(src), "bytes;",
      "v12 refs left:", len(leftovers_v12))
