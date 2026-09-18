#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build journal_manuscript_v16.tex from journal_manuscript_v15.tex by
UNIVERSAL verbatim adoption of Gemini's rewrite (external_audits/
humanized/gemini,grok humanized.txt, lines 1-532), per the author
directive: wherever Gemini provides text, use Gemini's actual
sentences; fill substance gaps from v15; keep every audited number.

Engine: anchored splices (v16_splices_a/b/c), each hard-failing on
anchor drift. Gates after assembly:
  G1  every v15 \\label present in v16; no new labels
  G2  cite-key set identical (no key dropped, no new key)
  G3  every v15 numeric token present in v16 (multiset missing = 0)
  G4  abstract <= 255 audit-style words, opens with Gemini's sentence
  G5  forbidden patterns absent (pattern_sweep_v16 list)
  G6  Gemini-presence check (distinctive verbatim sentences present)
  G7  \\input refs file retargeted; v16_bmb_refs.tex copied
  G8  ASCII-art guard: no verbatim/code blocks from the audit
"""
import re
import sys
from collections import Counter

sys.path.insert(0, "/home/z/my-project/metabolic-curvature-measure/scripts")
from v16_splices_a import SPLICES_A
from v16_splices_b import SPLICES_B
from v16_splices_c import SPLICES_C

BASE = "/home/z/my-project/metabolic-curvature-measure/"
V15 = BASE + "scripts/journal_manuscript_v15.tex"
V16 = BASE + "scripts/journal_manuscript_v16.tex"
REFS15 = BASE + "scripts/journal_manuscript_v15_bmb_refs.tex"
REFS16 = BASE + "scripts/journal_manuscript_v16_bmb_refs.tex"

ALL = SPLICES_A + SPLICES_B + SPLICES_C

tex = open(V15, encoding="utf-8").read()
fail = 0

# ---------------------------------------------------------------- splicing
for name, old, new in ALL:
    n = tex.count(old)
    if n != 1:
        print(f"[ANCHOR-FAIL] {name}: start-anchor occurs {n} times")
        fail += 1
        continue
    tex = tex.replace(old, new, 1)
    print(f"[SPLICE] {name}: {len(old)} -> {len(new)} chars")

# ------------------------------------------------------ refs-file retarget
tex = tex.replace("journal_manuscript_v15_bmb_refs",
                  "journal_manuscript_v16_bmb_refs")
refs = open(REFS15, encoding="utf-8").read()
refs = refs.replace("journal_manuscript_v15_bmb_refs",
                    "journal_manuscript_v16_bmb_refs")
refs = refs.replace("journal_manuscript_v15.tex",
                    "journal_manuscript_v16.tex")
open(REFS16, "w", encoding="utf-8").write(refs)

# ---------------------------------------------------------------- write out
open(V16, "w", encoding="utf-8").write(tex)

# ---------------------------------------------------------------- gates
def num_tokens(s):
    s = re.sub(r"(?<!\\)%.*", "", s)
    s = re.sub(r"([0-9]+(?:\.[0-9]+)?)\s*\\times\s*10\^\{?(-?[0-9]+)\}?",
               r"\1e\2", s)
    return Counter(re.findall(r"\d+(?:\.\d+)?", s))

def labels(s):
    return Counter(re.findall(r"\\label\{([^}]*)\}", s))

def citekeys(s):
    return Counter(re.findall(r"\\cite[tp]?\{([^}]*)\}", s))

def environments(s):
    return Counter(re.findall(
        r"\\begin\{(theorem|proposition|lemma|corollary|definition|"
        r"construction|assumption|conjecture|remark|enumerate|itemize|"
        r"equation|align|figure|table)\}", s))

v15 = open(V15, encoding="utf-8").read()

# G1 labels
lv15, lv16 = labels(v15), labels(tex)
missing_labels = lv15 - lv16
added_labels = lv16 - lv15
print(f"[{'PASS' if not missing_labels and not added_labels else 'FAIL'}] "
      f"G1 labels: missing={dict(missing_labels)} added={dict(added_labels)}")
if missing_labels or added_labels:
    fail += 1

# G2 cite keys
cv15, cv16 = citekeys(v15), citekeys(tex)
# flatten multi-key cites
def flat(c):
    out = Counter()
    for keys, n in c.items():
        for k in keys.split(","):
            out[k.strip()] += n
    return out
fv15, fv16 = flat(cv15), flat(cv16)
dropped = {k: fv15[k] - fv16.get(k, 0) for k in fv15 if fv16.get(k, 0) < fv15[k]}
newkeys = [k for k in fv16 if k not in fv15]
print(f"[{'PASS' if not dropped and not newkeys else 'FAIL'}] "
      f"G2 cite keys: dropped={dropped} new={newkeys}")
if dropped or newkeys:
    fail += 1

# G3 numeric tokens
nv15, nv16 = num_tokens(v15), num_tokens(tex)
missing = nv15 - nv16
added = nv16 - nv15
# Whitelisted deltas (mirrors verify_v16_completeness.py):
#   '15' : the \input refs filename version digit (v15 -> v16)
#   '3'  : the "(M3D compendium)" mention in the v15 abstract, dropped
#          per Gemini's own abstract (M3D named in the body)
WL_DEL = {"15": 1, "3": 1}
unexplained_del = {t: c - WL_DEL.get(t, 0) for t, c in missing.items()
                   if c > WL_DEL.get(t, 0)}
print(f"[{'PASS' if not unexplained_del else 'FAIL'}] G3 numbers: "
      f"missing={dict(missing)} (whitelisted: {WL_DEL})")
if unexplained_del:
    fail += 1
print(f"[INFO] G3 added tokens (for the v16 whitelist): {dict(added)}")

# G4 abstract
m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex, re.S)
body = m.group(1)
stripped = re.sub(r"\\[a-zA-Z]+", " ", body)
nwords = len(re.findall(r"[A-Za-z0-9\-]+", stripped))
opens = "Constraint-based models such as flux balance analysis (FBA) predict" in body
print(f"[{'PASS' if nwords <= 255 and opens else 'FAIL'}] "
      f"G4 abstract: {nwords} audit-style words (cap 255), "
      f"opens-with-Gemini={opens}")
if nwords > 255 or not opens:
    fail += 1

# G5 forbidden patterns (pattern_sweep_v16 list)
PATTERNS = [
    ("strawman: not a smooth curvature", r"not a smooth curvature", False),
    ("strawman: not a smooth Hessian", r"not a smooth [Hh]essian", False),
    ("changelog: is now a theorem", r"is now a theorem", False),
    ("changelog: our previously", r"our previous(ly)?", False),
    ("changelog: previously explored", r"previously explored", False),
    ("changelog: is final for", r"is final for", False),
    ("changelog: What this closes", r"[Ww]hat this closes", False),
    ("meta: self-contained self-description", r"self-contained", False),
    ("meta: earlier drafts", r"earlier drafts?", False),
    ("meta: prior versions of this", r"prior versions? of this", False),
    ("meta: in this round/revision/pass",
     r"in this (round|revision|pass)", False),
    ("chat register: as requested", r"as requested", False),
    ("chat register: chat", r"\bchat\b", True),
    ("meta: the author's earlier", r"the author'?s earlier", False),
    ("homogenized", r"[Hh]omogenized", False),
    ("author guard: Zai", r"\bZai\b", True),
]
stripped_tex = re.sub(r"(?<!\\)%.*", "", tex)
pat_fail = 0
for label, pat, wb in PATTERNS:
    flags = 0 if not wb else re.WORD_BOUNDARY if hasattr(re, "WORD_BOUNDARY") else 0
    if re.search(pat, stripped_tex):
        print(f"  [PATTERN] {label}")
        pat_fail += 1
print(f"[{'PASS' if pat_fail == 0 else 'FAIL'}] G5 forbidden patterns")
fail += pat_fail

# G6 Gemini presence
GEMINI_SENTENCES = [
    "predict cellular metabolic states by solving linear optimization",
    "not an ordinary function but a discrete measure concentrated",
    "the natural mathematical language for metabolic rerouting",
    "creates a profound blind spot",
    "the fundamental carrier of a network's",
    "In simple terms: because the gradient is constant",
    "We next analyzed whether active-set geometry explains genetic",
    "To test whether active-set curvature predicts real biological",
    "To confirm that the biological findings do not depend on",
    "Does the transcriptional response propagate downstream to change",
    "For decades, mathematical modeling in systems biology has been",
    "Regulatory networks are organized to manage internal pathway",
    "highlights an elegant cellular survival strategy",
    "To ensure that optimal flux trajectories are unique",
    "The predictor variable was evaluated as",
    "Because linear programs can possess multiple alternative",
    "This manuscript establishes five interconnected findings",
]
miss = []
norm = re.sub(r"\s+", " ", tex)
for s in GEMINI_SENTENCES:
    if s not in norm and re.sub(r"\s+", " ", s) not in norm:
        miss.append(s)
print(f"[{'PASS' if not miss else 'FAIL'}] G6 Gemini presence "
      f"({len(GEMINI_SENTENCES) - len(miss)}/{len(GEMINI_SENTENCES)})")
if miss:
    fail += 1
    for s in miss:
        print("  missing:", s)

# G8 ASCII-art guard
if "PARAMETER SPACE" in tex or "MICROSCOPIC" in tex or "Flux v_i" in tex:
    print("[FAIL] G8 ASCII-art leakage")
    fail += 1
else:
    print("[PASS] G8 no ASCII-art leakage")

# environment census (informational)
e15, e16 = environments(v15), environments(tex)
print(f"[INFO] environment census delta v15->v16: "
      f"+{dict(e16 - e15)} -{dict(e15 - e16)}")

print()
if fail:
    print(f"FAILED with {fail} gate failure(s); v16 written for inspection")
    sys.exit(1)
print("ALL GATES PASSED -- journal_manuscript_v16.tex built")
