#!/usr/bin/env python3
"""Create audit_v25_numbers.py from audit_v24_numbers.py.

Retargets the audit to the V17 enrichment round: main
journal_manuscript_v16.tex -> journal_manuscript_v17.tex (refs
v16 -> v17 with kacser1973 + heinrich1974 added, 27 -> 29 entries).
The new manuscript content (worked example, wall coordinates,
interior architecture, construction order, anatomy of one switch,
MCA comparison, memory-substrate deduction, bio-anchored abstract)
is audited by the spliced V17 check block
(scripts/v17_audit_block.py) against
download/v17_insight_substantiation.json (commit 74934d0) and
download/v17_worked_example_verification.json
(scripts/v17_worked_example_verify.py). Every pre-existing
numerical claim is unchanged; the v16 audit's 301 checks carry
over unchanged.
"""
import re

src = open("audit_v24_numbers.py").read()
block = open("v17_audit_block.py").read()

# 1. docstring header update
old_doc_head = "Numeric consistency audit of journal_manuscript_v16.tex +"
new_doc_head = ("Numeric consistency audit of journal_manuscript_v17.tex "
                "+\n(v17 enrichment round: implements the V17 revision "
                "plan\n(commits 4776f2d + 74934d0) --- Sec. 2 worked "
                "example, Sec. 4\nwall coordinates + interior architecture "
                "+ construction order,\nSec. 5 anatomy of one switch, "
                "Discussion MCA + memory substrate,\nbio-anchored "
                "abstract at the 255 cap; all new numbers from\n"
                "download/v17_insight_substantiation.json and\n"
                "download/v17_worked_example_verification.json, audited "
                "by the\nV17 check block; every v16 number unchanged. "
                "Extends the v24\naudit of journal_manuscript_v16.tex +")
assert old_doc_head in src
src = src.replace(old_doc_head, new_doc_head, 1)

# 2. tex + refs path retargets
reps = [
    ('"journal_manuscript_v16.tex"', '"journal_manuscript_v17.tex"'),
    ('"journal_manuscript_v16_bmb_refs" in tex2',
     '"journal_manuscript_v17_bmb_refs" in tex2'),
    ('"journal_manuscript_v16_bmb_refs.tex"',
     '"journal_manuscript_v17_bmb_refs.tex"'),
    ('n_bib == 27', 'n_bib == 29'),
    ('"BMB-style references: 27 entries',
     '"BMB-style references: 29 entries'),
]
for old, new in reps:
    assert old in src, f"anchor not found: {old[:60]!r}"
    src = src.replace(old, new)

# 3. ledger output paths v24 -> v25
for old, new in [('"v24_number_audit.json"', '"v25_number_audit.json"'),
                 ('"v24_number_audit.md"', '"v25_number_audit.md"'),
                 ('"v24_number_audit.md"', '"v25_number_audit.md"'),
                 ('v24_number_audit.md', 'v25_number_audit.md'),
                 ('"v24_number_audit"', '"v25_number_audit"')]:
    if old in src:
        src = src.replace(old, new)

# 4. splice the V17 check block BEFORE the output/summary section so
#    the V17 checks count toward the ledger totals
out_anchor = 'out = {"experiment": "v12 numeric consistency audit'
assert out_anchor in src
src = src.replace(out_anchor, block + "\n\n" + out_anchor, 1)

# 5. verify no stale v16 references remain in live code
leftovers = re.findall(r'journal_manuscript_v16', src)
print("stale v16 refs (header comments only expected):", len(leftovers))

open("audit_v25_numbers.py", "w").write(src)
print("audit_v25_numbers.py written:", len(src), "bytes")
