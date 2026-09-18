#!/usr/bin/env python3
"""Companion v10 completeness verification (v10 vs v9).

Checks that companion_categorical_v10.tex differs from
companion_categorical_v9.tex ONLY in the Gemini-register adoption
regions (title/abstract/keywords, intro narrative, contribution
titles, section leads, application-bridge opening, bibliography
pointer), with nothing lost:
  1. Numeric-token multiset: only the bibliography version digit
     (v9 -> v10) may change on the deletion side; additions
     whitelisted (none expected).
  2. Label census identical.
  3. Citation key set identical.
  4. Environment census identical.
  5. Section census identical.
  6. Bibliography pointer retargeted; companion_refs_v10.bib
     byte-identical to companion_refs_v9.bib.
  7. Abstract: Gemini opening, <= 265 audit-style words, six-axis
     sentence intact.
"""
import re
from collections import Counter


def num_tokens(s):
    s = re.sub(r"(?<!\\)%.*", "", s)
    s = re.sub(r"([0-9]+(?:\.[0-9]+)?)\s*\\times\s*10\^\{?(-?[0-9]+)\}?",
               r"\1e\2", s)
    return Counter(re.findall(r"\d+(?:\.\d+)?", s))


def labels(s):
    return Counter(re.findall(r"\\label\{([^}]*)\}", s))


def citekeys(s):
    out = Counter()
    for keys, n in Counter(re.findall(r"\\cite[tp]?\{([^}]*)\}", s)).items():
        for k in keys.split(","):
            out[k.strip()] += n
    return out


def environments(s):
    return Counter(re.findall(
        r"\\begin\{(theorem|proposition|lemma|corollary|definition|"
        r"construction|assumption|conjecture|remark|enumerate|itemize|"
        r"equation|align|figure|table)\}", s))


base = "/home/z/my-project/metabolic-curvature-measure/"
v10 = open(base + "scripts/companion_categorical_v10.tex").read()
v9 = open(base + "scripts/companion_categorical_v9.tex").read()

fail = 0


def report(name, ok, note=""):
    global fail
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" ({note})" if note else ""))
    if not ok:
        fail += 1


n9, n10 = num_tokens(v9), num_tokens(v10)
missing = n9 - n10
added = n10 - n9
WL_DEL = {"9": 1}   # \bibliography{companion_refs_v9} -> v10
unexp_del = {t: c - WL_DEL.get(t, 0) for t, c in missing.items()
             if c > WL_DEL.get(t, 0)}
report("number multiset: deletions = bib version digit only",
       not unexp_del, f"missing={dict(missing)} added={dict(added)}")

l9, l10 = labels(v9), labels(v10)
report("label census identical", l9 == l10,
       f"missing={dict(l9 - l10)} added={dict(l10 - l9)}")

c9, c10 = citekeys(v9), citekeys(v10)
dropped = [k for k in c9 if c10.get(k, 0) == 0]
new = [k for k in c10 if k not in c9]
report("citation key set identical", not dropped and not new,
       f"dropped={dropped} new={new}")

e9, e10 = environments(v9), environments(v10)
report("environment census identical", e9 == e10,
       f"delta +{dict(e10 - e9)} -{dict(e9 - e10)}")

s9 = Counter(re.findall(r"\\(sub)*section\*?\{", v9))
s10 = Counter(re.findall(r"\\(sub)*section\*?\{", v10))
report("section census identical", s9 == s10,
       f"delta +{dict(s10 - s9)} -{dict(s9 - s10)}")

b9 = open(base + "scripts/companion_refs_v9.bib").read()
b10 = open(base + "scripts/companion_refs_v10.bib").read()
report("bibliography byte-identical", b9 == b10)
report("bibliography pointer retargeted",
       "\\bibliography{companion_refs_v10}" in v10 and
       "\\bibliography{companion_refs_v9}" not in v10)

m = re.search(r"\\textbf\{Abstract\.\}(.*?)\\par\s*\n\\vspace", v10, re.S)
body = m.group(1)
six_axis = ("carbon, oxygen, nitrogen, phosphate, and iron supply" in
            body.replace("\n", " "))
stripped = re.sub(r"\\[a-zA-Z]+", " ", body)
nwords = len(re.findall(r"[A-Za-z0-9\-]+", stripped))
report("abstract: Gemini opening + <= 265 words + six-axis intact",
       "When adaptive systems navigate fluctuating" in body and
       nwords <= 265 and six_axis,
       f"{nwords} words, six-axis={six_axis}")

print()
if fail:
    print(f"FAILED with {fail} check(s)")
    raise SystemExit(1)
print("ALL COMPLETE: v10 = v9 + Gemini-register adoption, nothing lost")
