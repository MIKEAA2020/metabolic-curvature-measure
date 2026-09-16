#!/usr/bin/env python3
"""Create audit_v16_numbers.py from audit_v15_numbers.py.

Retargets the audit to the v8 (main) / v7 (companion) synthesis-round
manuscripts, updates the header docstring, and retargets the output
ledger paths. The frozen journal_manuscript.tex (v21 legacy) anchor is
left untouched.
"""
import re

src = open("audit_v15_numbers.py").read()

# 1. Path retargets
src = src.replace(
    'tex2 = open(os.path.join(BASE, "scripts",\n'
    '                         "journal_manuscript_v7.tex")).read()',
    'tex2 = open(os.path.join(BASE, "scripts",\n'
    '                         "journal_manuscript_v8.tex")).read()')
src = src.replace('"journal_manuscript_v7_bmb_refs" in tex2',
                  '"journal_manuscript_v8_bmb_refs" in tex2')
src = src.replace(
    'bmb_refs = open(os.path.join(BASE, "scripts",\n'
    '                 "journal_manuscript_v7_bmb_refs.tex")).read()',
    'bmb_refs = open(os.path.join(BASE, "scripts",\n'
    '                 "journal_manuscript_v8_bmb_refs.tex")).read()')
src = src.replace(
    'companion = open(os.path.join(BASE, "scripts", "companion_categorical_v6.tex"),',
    'companion = open(os.path.join(BASE, "scripts", "companion_categorical_v7.tex"),')
src = src.replace(
    'tex = open(os.path.join(BASE, "scripts",\n'
    '                        "companion_categorical_v6.tex")).read()',
    'tex = open(os.path.join(BASE, "scripts",\n'
    '                        "companion_categorical_v7.tex")).read()')
src = src.replace('"companion_categorical_v6.tex (abstract + Keio section)"',
                  '"companion_categorical_v7.tex (abstract + Keio section)"')
src = src.replace('"companion_categorical_v6.tex:prop:poincare-averaging + tab:network-battery"',
                  '"companion_categorical_v7.tex:prop:poincare-averaging + tab:network-battery"')
src = src.replace('"companion_categorical_v6.tex abstract"',
                  '"companion_categorical_v7.tex abstract"')

# 2. Output ledger paths
src = src.replace('"v15_number_audit.json"', '"v16_number_audit.json"')
src = src.replace('"v15_number_audit.md"', '"v16_number_audit.md"')

# 3. Header docstring
old_doc = '''Numeric consistency audit of journal_manuscript_v7.tex +
companion_categorical_v6.tex (reader-oriented prose revision round:
abstract/intro/section-lead rewrites informed by landmark-paper style
study; all numerical claims unchanged; extends the v14 audit) extends the v11 audit'''
new_doc = '''Numeric consistency audit of journal_manuscript_v8.tex +
companion_categorical_v7.tex (merged-synthesis round: targeted
accessibility grafts from the evaluated external humanization attempts
-- abstract robustness-clause compression with the numbers kept in
the body, glosses at the value-function / coupling / discussion
sites, the 98->301 check-count reconciliation, n=424 gene-count
disambiguation, three forbidden-pattern prose fixes in the main paper,
and the boundary-rule / thermostat / Zeno / proof-provenance grafts in
the companion; every numerical claim unchanged; extends the v15
audit) extends the v11 audit'''
assert old_doc in src, "v15 docstring anchor not found"
src = src.replace(old_doc, new_doc)

src = src.replace(
    'Outputs: download/deepseek_bridge/v8_number_audit.json (full ledger)\n'
    '          download/deepseek_bridge/v8_number_audit.md (readable table)',
    'Outputs: download/deepseek_bridge/v16_number_audit.json (full ledger)\n'
    '          download/deepseek_bridge/v16_number_audit.md (readable table)')

# 4. Output-side filename constants inside the writer (they use the
#    DB path with literal v15 names -- covered by step 2; verify none left)
leftovers = re.findall(r'journal_manuscript_v7|companion_categorical_v6', src)
print("leftover v7/v6 manuscript references:", leftovers)

open("audit_v16_numbers.py", "w").write(src)
print("audit_v16_numbers.py written; length", len(src))
