#!/usr/bin/env python3
"""Create audit_v24_numbers.py from audit_v23_numbers.py.

Retargets the audit to the universal Gemini-adoption round: main
journal_manuscript_v15.tex -> journal_manuscript_v16.tex. Companion
stays at companion_categorical_v9.tex (companion edits this round are
a separate version, companion_categorical_v10, audited by its own
completeness check; the 301-check ledger is main-paper numbers).
The text change is Gemini-prose adoption (external_audits/humanized/
gemini,grok humanized.txt lines 1-532 adopted verbatim where provided:
abstract rebuilt on Gemini's abstract at the 255-word cap opening with
Gemini's first sentence, title/keywords, intro opening + five-findings
claim list, Sec. 2 definitions and glosses, coupling theorem statement,
Sec. 3 bridge/TV/holonomy, Sec. 4 validation narratives, Sec. 5
association/tie-break/path/protein narratives, Discussion restructured
into Gemini's three subsections, Methods leads). Numeric changes:
re-quotes of audited body claims in the claim list and Discussion
(+0.395, 2.6e-17, 424, 0.083, 366, 66, 11/12) and identifier digits
(iML1515/iJO1366, citation keys); the abstract drops the M3D mention
per Gemini's own abstract. Every audited number kept.
"""
import re

src = open("audit_v23_numbers.py").read()

# 1. Path retargets (main v15 -> v16)
old_doc = """Numeric consistency audit of journal_manuscript_v15.tex +
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
audit) extends the v11 audit"""
new_doc = """Numeric consistency audit of journal_manuscript_v16.tex +
companion_categorical_v9.tex (universal Gemini-adoption round:
Gemini's rewrite external_audits/humanized/gemini,grok humanized.txt
lines 1-532 adopted verbatim wherever it provides text -- abstract
rebuilt on Gemini's own abstract at the 255-word cap, opening with
Gemini's first sentence; title and keywords; intro opening and
five-findings claim list; Sec. 2 setup/definitions/glosses; the
value--flux coupling statement; Sec. 3 opening, TV-failure
explanation, and holonomy proposition; Sec. 4 validation narratives;
Sec. 5 association/tie-break/path-robustness/protein-layer
narratives; Discussion restructured into Gemini's three subsections;
Methods leads. Gemini's proof variants not adopted (v15 proofs
retained in full). Gemini's unaudited numbers (decile dispersions,
PaxDb p-value, model sizes, noise-floor compression, 100.0000 token
form) excluded per the v15-round adjudication; every audited number
kept. New tokens are re-quotes of audited body claims (claim list +
Discussion: +0.395, 2.6e-17, 424, 0.083, 366, 66, 11/12) and
identifier digits (iML1515/iJO1366, citation keys); the abstract
drops the M3D mention per Gemini's own abstract. Companion unchanged
in this ledger (its v10 round is audited by verify_v10_completeness);
every numerical claim unchanged from v15/v9;
extends the v23
audit) extends the v11 audit"""
assert old_doc in src, "v23 docstring anchor not found"
src = src.replace(old_doc, new_doc)

reps = [
    ('"journal_manuscript_v15.tex"', '"journal_manuscript_v16.tex"'),
    ('"journal_manuscript_v15_bmb_refs" in tex2',
     '"journal_manuscript_v16_bmb_refs" in tex2'),
    ('"journal_manuscript_v15_bmb_refs.tex"',
     '"journal_manuscript_v16_bmb_refs.tex"'),
]
for old, new in reps:
    if old in src:
        src = src.replace(old, new)
    else:
        print(f"[WARN] anchor not found: {old[:60]}")

# 2. Ledger output paths
for old, new in [('"v23_number_audit.json"', '"v24_number_audit.json"'),
                 ('"v23_number_audit.md"', '"v24_number_audit.md"'),
                 ('download/deepseek_bridge/v23_number_audit.json',
                  'download/deepseek_bridge/v24_number_audit.json'),
                 ('download/deepseek_bridge/v23_number_audit.md',
                  'download/deepseek_bridge/v24_number_audit.md'),
                 ('"v23_number_audit"', '"v24_number_audit"')]:
    if old in src:
        src = src.replace(old, new)

# 3. Verify no stale version references remain
leftovers = re.findall(r'journal_manuscript_v15', src)
assert not leftovers, f"stale v15 references: {leftovers}"

open("audit_v24_numbers.py", "w").write(src)
print("audit_v24_numbers.py written:", len(src), "bytes")
