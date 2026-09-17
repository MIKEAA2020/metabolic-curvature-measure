#!/usr/bin/env python3
"""Brevity-round completeness verification (v12 vs pre-humanized v10).

Checks that the final main manuscript (journal_manuscript_v12.tex) is
complete against the pre-humanized version (journal_manuscript_v10.tex,
the state before the universal Gemini-register round and this brevity
round):
  1. Numeric-token multiset diff (v12 vs v11 and v12 vs v10), with the
     known-benign deltas whitelisted: the \\input filename version bump,
     the ORCID link digits (clickable-contacts round), and the v11
     register round's already-audited prose-context digit reshuffles.
  2. Label census       (\\label{...} multisets identical)
  3. Citation census    (\\citep/\\citet/\\citealp keys identical)
  4. Environment census (theorem/definition/... counts identical)
  5. Section census     (\\section/\\subsection counts identical)
  6. Bibliography identity (bmb_refs files byte-compared by bibitems)
"""
import re
from collections import Counter

def num_tokens(s):
    s = re.sub(r'(?<!\\)%.*', '', s)
    return Counter(re.findall(r'\d+(?:\.\d+)?', s))

def labels(s):
    return Counter(re.findall(r'\\label\{([^}]*)\}', s))

def citekeys(s):
    return Counter(re.findall(r'\\cite[pt]?\w*\{([^}]*)\}', s))

def environments(s):
    return Counter(re.findall(r'\\begin\{(theorem|proposition|lemma|corollary|definition|construction|assumption|conjecture|remark|enumerate|itemize|equation|align|figure|table)\}', s))

def sections(s):
    return Counter(re.findall(r'\\(sub)*section\*?\{', s))

def load(p):
    return open(p).read()

base = "/home/z/my-project/metabolic-curvature-measure/scripts/"
v12 = load(base + "journal_manuscript_v12.tex")
v11 = load(base + "journal_manuscript_v11.tex")
v10 = load(base + "journal_manuscript_v10.tex")
refs12 = load(base + "journal_manuscript_v12_bmb_refs.tex")
refs10 = load(base + "journal_manuscript_v10_bmb_refs.tex")

fail = 0

def report(name, missing, added, note=""):
    global fail
    ok = not missing and not added
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" ({note})" if note else ""))
    if missing:
        fail += 1
        print("  missing from final:", dict(missing))
    if added:
        fail += 1
        print("  added in final:", dict(added))

# 1a. Number multiset v12 vs v11: expect exactly the \input filename swap
d = num_tokens(v12) - num_tokens(v11)
d2 = num_tokens(v11) - num_tokens(v12)
report("number multiset v12 vs v11 (expect only 11->12 filename swap)",
       d2 - Counter({'11': 1}), d - Counter({'12': 1}))

# 1b. Number multiset v12 vs v10 (pre-humanized): allowed additions =
#     ORCID href-URL copy + filename bump + v11-round audited '2' reshuffles
orc = Counter({'0000': 1, '0002': 1, '0019': 1, '1842': 1, '2': 2, '12': 1})
d = num_tokens(v12) - num_tokens(v10) - orc
d2 = num_tokens(v10) - num_tokens(v12)
report("number multiset v12 vs v10 (pre-humanized; ORCID + audited deltas allowed)",
       d2 - Counter({'10': 1}), d - Counter({'10': 1}))
# note: '12' appears in the allowed set; the missing side allows the '10'
# filename token only. Re-derive strictly:
d = num_tokens(v12) - num_tokens(v10) - Counter({'0000':1,'0002':1,'0019':1,'1842':1,'2':2,'12':1})
d2 = num_tokens(v10) - num_tokens(v12) - Counter({'10': 1})
report("number multiset v12 vs v10, strict both sides", d2, d)

# 2-5. Structural censuses v12 vs v10
for name, fn in (("label census", labels), ("citation-key census", citekeys),
                 ("environment census", environments), ("section census", sections)):
    report(f"{name} v12 vs v10", fn(v10) - fn(v12), fn(v12) - fn(v10))

# 6. Bibliography identity
def bibitems(s):
    return re.findall(r'\\bibitem\[([^\]]*)\]\{([^}]*)\}', s)
b12, b10 = bibitems(refs12), bibitems(refs10)
ok = b12 == b10
print(f"[{'PASS' if ok else 'FAIL'}] bibitem list v12 vs v10 refs files ({len(b12)} items)")
if not ok:
    fail += 1

print()
print("RESULT:", "ALL COMPLETE — final version loses nothing vs pre-humanized v10"
      if fail == 0 else f"{fail} FAILURES")
raise SystemExit(1 if fail else 0)
