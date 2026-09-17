#!/usr/bin/env python3
"""Create audit_v18_numbers.py from audit_v17_numbers.py.

Retargets the audit to the Gemini-alignment round: main
journal_manuscript_v9.tex -> journal_manuscript_v10.tex and companion
companion_categorical_v7.tex -> companion_categorical_v8.tex. The
text changes are accessibility grafts only (intro lead, LP setup,
wall-crossing / boundary-impedance glosses, partial-correlation
motivation, protein-layer central question, discussion sentences,
labeled Limitations list; companion: narrative abstract opening at a
net word budget under 265, closed-cycle example, intuitive glosses,
stabilization question, application-bridge numbers, Conclusion
section). Every numerical claim is unchanged from v9/v7; the only
newly stated numbers in the companion (r = +0.395, n = 424, r =
-0.083, n = 366) are the application paper's audited values.
"""
import re

src = open("audit_v17_numbers.py").read()

# 1. Path retargets (main v9 -> v10)
src = src.replace(
    'tex2 = open(os.path.join(BASE, "scripts",\n'
    '                         "journal_manuscript_v9.tex")).read()',
    'tex2 = open(os.path.join(BASE, "scripts",\n'
    '                         "journal_manuscript_v10.tex")).read()')
src = src.replace('"journal_manuscript_v9_bmb_refs" in tex2',
                  '"journal_manuscript_v10_bmb_refs" in tex2')
src = src.replace(
    'bmb_refs = open(os.path.join(BASE, "scripts",\n'
    '                 "journal_manuscript_v9_bmb_refs.tex")).read()',
    'bmb_refs = open(os.path.join(BASE, "scripts",\n'
    '                 "journal_manuscript_v10_bmb_refs.tex")).read()')

# 2. Main docstring retarget (before the global companion replace,
#    which also touches the docstring text)
old_doc = '''Numeric consistency audit of journal_manuscript_v9.tex +
companion_categorical_v7.tex (post-synthesis flow-polish round: the
main paper's abstract subject-repetition smoothed and the
Reproducibility sentence recast as an automated suite of 301 numeric
checks; every numerical claim unchanged; extends the v16
audit) extends the v11 audit'''
new_doc = '''Numeric consistency audit of journal_manuscript_v10.tex +
companion_categorical_v8.tex (Gemini-alignment round: accessibility
grafts from the evaluated Gemini humanization attempts -- main: intro
lead, LP setup, wall-crossing and boundary-impedance glosses,
partial-correlation motivation, protein-layer central question,
discussion window and objective-invisibility sentences, labeled
Limitations list; companion: narrative abstract opening (264 words,
cap kept), closed-cycle example, intuitive glosses, stabilization
question, application-bridge numbers, Conclusion section; every
numerical claim unchanged from v9/v7; extends the v17
audit) extends the v11 audit'''
assert old_doc in src, "v17 docstring anchor not found"
src = src.replace(old_doc, new_doc)

# 3. Companion retargets (v7 -> v8): every occurrence, including the
#    open() calls and the human-readable claim/artifact strings.
src = src.replace("companion_categorical_v7.tex", "companion_categorical_v8.tex")
src = src.replace("companion_categorical_v7", "companion_categorical_v8")

# 4. Output ledger paths
src = src.replace('"v17_number_audit.json"', '"v18_number_audit.json"')
src = src.replace('"v17_number_audit.md"', '"v18_number_audit.md"')
src = src.replace('download/deepseek_bridge/v17_number_audit.json',
                  'download/deepseek_bridge/v18_number_audit.json')
src = src.replace('download/deepseek_bridge/v17_number_audit.md',
                  'download/deepseek_bridge/v18_number_audit.md')
src = src.replace("v17_number_audit", "v18_number_audit")

# 5. Verify no stale version references remain
leftovers_v9 = re.findall(r'journal_manuscript_v9', src)
leftovers_v7 = re.findall(r'companion_categorical_v7', src)
assert not leftovers_v9, f"stale v9 references: {leftovers_v9}"
assert not leftovers_v7, f"stale v7 references: {leftovers_v7}"

open("audit_v18_numbers.py", "w").write(src)
print("audit_v18_numbers.py written:",
      len(src), "bytes;",
      "v9 refs left:", len(leftovers_v9),
      "v7 refs left:", len(leftovers_v7))
