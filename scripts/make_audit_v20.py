#!/usr/bin/env python3
"""Create audit_v20_numbers.py from audit_v19_numbers.py.

Retargets the audit to the brevity round: main
journal_manuscript_v11.tex -> journal_manuscript_v12.tex. Companion
stays at companion_categorical_v9.tex (zero companion edits this
round). The text changes are two register tightenings only (the
Positioning paragraph's "We find that it does." -> "It does." with
the dependent "We also find that" connective dropped, and the "at
this point" filler removed from the protein-layer central
question); every numerical claim is unchanged from v11.
"""
import re

src = open("audit_v19_numbers.py").read()

# 1. Path retargets (main v11 -> v12)
src = src.replace(
    'tex2 = open(os.path.join(BASE, "scripts",\n'
    '                         "journal_manuscript_v11.tex")).read()',
    'tex2 = open(os.path.join(BASE, "scripts",\n'
    '                         "journal_manuscript_v12.tex")).read()')
src = src.replace('"journal_manuscript_v11_bmb_refs" in tex2',
                  '"journal_manuscript_v12_bmb_refs" in tex2')
src = src.replace(
    'bmb_refs = open(os.path.join(BASE, "scripts",\n'
    '                 "journal_manuscript_v11_bmb_refs.tex")).read()',
    'bmb_refs = open(os.path.join(BASE, "scripts",\n'
    '                 "journal_manuscript_v12_bmb_refs.tex")).read()')

# 2. Main docstring retarget (before the companion replace)
old_doc = '''Numeric consistency audit of journal_manuscript_v11.tex +
companion_categorical_v9.tex (universal Gemini-register round:
register-level revision of narrative prose across both papers -- main:
intro lead, section leads, result narratives, discussion, methods
connectives; companion: abstract connective polish, SAVGS and
verdicts leads, conclusion; clickable email and ORCID in both; every
numerical claim unchanged from v10/v8 per the number-integrity
multiset diff; extends the v18
audit) extends the v11 audit'''
new_doc = '''Numeric consistency audit of journal_manuscript_v12.tex +
companion_categorical_v9.tex (brevity round: two register tightenings
in the main paper -- the Positioning paragraph's "We find that it
does." shortened to "It does." with the dependent "We also find
that" connective dropped, and the "at this point" filler removed from
the protein-layer central question; companion unchanged; every
numerical claim unchanged from v11/v9; extends the v19
audit) extends the v11 audit'''
assert old_doc in src, "v19 docstring anchor not found"
src = src.replace(old_doc, new_doc)

# 3. Companion stays at v9: no companion replace this round.

# 4. Output ledger paths
src = src.replace('"v19_number_audit.json"', '"v20_number_audit.json"')
src = src.replace('"v19_number_audit.md"', '"v20_number_audit.md"')
src = src.replace('download/deepseek_bridge/v19_number_audit.json',
                  'download/deepseek_bridge/v20_number_audit.json')
src = src.replace('download/deepseek_bridge/v19_number_audit.md',
                  'download/deepseek_bridge/v20_number_audit.md')
src = src.replace("v19_number_audit", "v20_number_audit")

# 5. Verify no stale version references remain
leftovers_v11 = re.findall(r'journal_manuscript_v11', src)
assert not leftovers_v11, f"stale v11 references: {leftovers_v11}"

open("audit_v20_numbers.py", "w").write(src)
print("audit_v20_numbers.py written:",
      len(src), "bytes;",
      "v11 refs left:", len(leftovers_v11))
