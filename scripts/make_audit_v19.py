#!/usr/bin/env python3
"""Create audit_v19_numbers.py from audit_v18_numbers.py.

Retargets the audit to the universal Gemini-register revision round:
main journal_manuscript_v10.tex -> journal_manuscript_v11.tex and
companion companion_categorical_v8.tex -> companion_categorical_v9.tex.
The text changes are prose-register only (universal adoption of the
evaluated Gemini humanization register across narrative prose: intro
lead, section leads, result narratives, discussion, methods; companion:
abstract connective polish, SAVGS/verdicts/conclusion leads, clickable
email/ORCID in both). Every numerical claim is unchanged from v10/v8;
number-integrity multiset diff confirms zero missing/added numeric
tokens except the ORCID link digits.
"""
import re

src = open("audit_v18_numbers.py").read()

# 1. Path retargets (main v10 -> v11)
src = src.replace(
    'tex2 = open(os.path.join(BASE, "scripts",\n'
    '                         "journal_manuscript_v10.tex")).read()',
    'tex2 = open(os.path.join(BASE, "scripts",\n'
    '                         "journal_manuscript_v11.tex")).read()')
src = src.replace('"journal_manuscript_v10_bmb_refs" in tex2',
                  '"journal_manuscript_v11_bmb_refs" in tex2')
src = src.replace(
    'bmb_refs = open(os.path.join(BASE, "scripts",\n'
    '                 "journal_manuscript_v10_bmb_refs.tex")).read()',
    'bmb_refs = open(os.path.join(BASE, "scripts",\n'
    '                 "journal_manuscript_v11_bmb_refs.tex")).read()')

# 2. Main docstring retarget (before the global companion replace)
old_doc = '''Numeric consistency audit of journal_manuscript_v10.tex +
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
new_doc = '''Numeric consistency audit of journal_manuscript_v11.tex +
companion_categorical_v9.tex (universal Gemini-register round:
register-level revision of narrative prose across both papers -- main:
intro lead, section leads, result narratives, discussion, methods
connectives; companion: abstract connective polish, SAVGS and
verdicts leads, conclusion; clickable email and ORCID in both; every
numerical claim unchanged from v10/v8 per the number-integrity
multiset diff; extends the v18
audit) extends the v11 audit'''
assert old_doc in src, "v18 docstring anchor not found"
src = src.replace(old_doc, new_doc)

# 3. Companion retargets (v8 -> v9): every occurrence
src = src.replace("companion_categorical_v8.tex", "companion_categorical_v9.tex")
src = src.replace("companion_categorical_v8", "companion_categorical_v9")

# 4. Output ledger paths
src = src.replace('"v18_number_audit.json"', '"v19_number_audit.json"')
src = src.replace('"v18_number_audit.md"', '"v19_number_audit.md"')
src = src.replace('download/deepseek_bridge/v18_number_audit.json',
                  'download/deepseek_bridge/v19_number_audit.json')
src = src.replace('download/deepseek_bridge/v18_number_audit.md',
                  'download/deepseek_bridge/v19_number_audit.md')
src = src.replace("v18_number_audit", "v19_number_audit")

# 5. Verify no stale version references remain
leftovers_v10 = re.findall(r'journal_manuscript_v10', src)
leftovers_v8 = re.findall(r'companion_categorical_v8', src)
assert not leftovers_v10, f"stale v10 references: {leftovers_v10}"
assert not leftovers_v8, f"stale v8 references: {leftovers_v8}"

open("audit_v19_numbers.py", "w").write(src)
print("audit_v19_numbers.py written:",
      len(src), "bytes;",
      "v10 refs left:", len(leftovers_v10),
      "v8 refs left:", len(leftovers_v8))
