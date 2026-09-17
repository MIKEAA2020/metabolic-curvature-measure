#!/usr/bin/env python3
"""Create audit_v17_numbers.py from audit_v16_numbers.py.

Retargets the audit to the v9 (main) flow-polish revision; the
companion stays at v7 (no text changes this round). The only v8->v9
text changes are: the abstract's 'The association does not
propagate' -> 'It does not propagate' flow fix, and the
Reproducibility sentence recast as 'An automated suite of 301
numeric checks'. Every numerical claim is unchanged.
"""
import re

src = open("audit_v16_numbers.py").read()

# 1. Path retargets (main v8 -> v9; companion v7 stays)
src = src.replace(
    'tex2 = open(os.path.join(BASE, "scripts",\n'
    '                         "journal_manuscript_v8.tex")).read()',
    'tex2 = open(os.path.join(BASE, "scripts",\n'
    '                         "journal_manuscript_v9.tex")).read()')
src = src.replace('"journal_manuscript_v8_bmb_refs" in tex2',
                  '"journal_manuscript_v9_bmb_refs" in tex2')
src = src.replace(
    'bmb_refs = open(os.path.join(BASE, "scripts",\n'
    '                 "journal_manuscript_v8_bmb_refs.tex")).read()',
    'bmb_refs = open(os.path.join(BASE, "scripts",\n'
    '                 "journal_manuscript_v9_bmb_refs.tex")).read()')

# 2. Output ledger paths
src = src.replace('"v16_number_audit.json"', '"v17_number_audit.json"')
src = src.replace('"v16_number_audit.md"', '"v17_number_audit.md"')

# 3. Header docstring
old_doc = '''Numeric consistency audit of journal_manuscript_v8.tex +
companion_categorical_v7.tex (merged-synthesis round: targeted
accessibility grafts from the evaluated external humanization attempts
-- abstract robustness-clause compression with the numbers kept in
the body, glosses at the value-function / coupling / discussion
sites, the 98->301 check-count reconciliation, n=424 gene-count
disambiguation, three forbidden-pattern prose fixes in the main paper,
and the boundary-rule / thermostat / Zeno / proof-provenance grafts in
the companion; every numerical claim unchanged; extends the v15
audit) extends the v11 audit'''
new_doc = '''Numeric consistency audit of journal_manuscript_v9.tex +
companion_categorical_v7.tex (post-synthesis flow-polish round: the
main paper's abstract subject-repetition smoothed and the
Reproducibility sentence recast as an automated suite of 301 numeric
checks; every numerical claim unchanged; extends the v16
audit) extends the v11 audit'''
assert old_doc in src, "v16 docstring anchor not found"
src = src.replace(old_doc, new_doc)

src = src.replace(
    'Outputs: download/deepseek_bridge/v16_number_audit.json (full ledger)\n'
    '          download/deepseek_bridge/v16_number_audit.md (readable table)',
    'Outputs: download/deepseek_bridge/v17_number_audit.json (full ledger)\n'
    '          download/deepseek_bridge/v17_number_audit.md (readable table)')

# 4. Verify no stale v8 main references remain (companion v7 stays)
leftovers = re.findall(r'journal_manuscript_v8', src)
print("leftover v8 manuscript references:", leftovers)

open("audit_v17_numbers.py", "w").write(src)
print("audit_v17_numbers.py written; length", len(src))
