#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build companion_categorical_v10.tex from companion_categorical_v9.tex
by adopting Gemini's companion rewrite (external_audits/humanized/
companion humanized.txt, gemini section lines 1-714) as the prose
base: title, abstract, keywords, intro narrative, contribution
titles, section leads; v9 substance retained (refs, proof statuses,
six-axis battery, machine-verified claims). Grok's formulations and
own bridges only where merited. Every number kept.

Gates:
  G1  no \\label lost, none added
  G2  cite-key set identical
  G3  numeric tokens: every v9 token present (deletions whitelisted)
  G4  abstract <= 265 audit-style words, opens with Gemini's sentence
  G5  forbidden patterns absent
  G6  Gemini presence (verbatim sentences)
  G7  bibliography retargeted (companion_refs_v10.bib copied)
"""
import re
import sys
import shutil
from collections import Counter

sys.path.insert(0, "/home/z/my-project/metabolic-curvature-measure/scripts")
from v10_splices import SPLICES

BASE = "/home/z/my-project/metabolic-curvature-measure/"
V9 = BASE + "scripts/companion_categorical_v9.tex"
V10 = BASE + "scripts/companion_categorical_v10.tex"

tex = open(V9, encoding="utf-8").read()
v9 = tex
fail = 0

for name, old, new in SPLICES:
    n = tex.count(old)
    if n != 1:
        print(f"[ANCHOR-FAIL] {name}: occurs {n} times")
        fail += 1
        continue
    tex = tex.replace(old, new, 1)
    print(f"[SPLICE] {name}")

# ---------------------------------------------------- abstract trims
TRIMS = [
    ("framework that defines and quantifies this\nphenomenon: \\emph{viability-weighted curvature}, the geometric\nobject measuring this accumulation through the policy holonomy.",
     "framework defining and quantifying this\nphenomenon: \\emph{viability-weighted curvature}, measuring this\naccumulation through the policy holonomy."),
    ("The \\emph{SAVGS architecture} unifies the control base, the\nFisher--Rao policy bundle, the viability margin, the maintenance\ngraph, and a $2$-categorical boundary span into one stratified\n$G_C$-reduced bundle.",
     "The \\emph{SAVGS architecture} unifies control base, Fisher--Rao\npolicy bundle, viability margin, maintenance graph, and\n$2$-categorical boundary span into one stratified $G_C$-reduced\nbundle."),
    ("carries a lax-functorial gluing theorem and a piecewise-holonomy\nformula, with the boundary reset of a loop crossing a\nconstraint-switching wall transversally in \\emph{pairs} at its true\norder; on each constant-active-set stratum the Fisher-minimal\ntransport law (KKT projection) defines the connection, and the\nsmall-loop theorem bounds the endpoint erosion of a viability\nmargin by the viability-weighted curvature.",
     "carries a lax-functorial gluing theorem and a piecewise-holonomy\nformula, the boundary reset of loops crossing a\nconstraint-switching wall transversally in \\emph{pairs} at its\ntrue order; each stratum carries the Fisher-minimal transport law\n(KKT projection) as its connection, and the small-loop theorem\nbounds endpoint erosion of a viability margin by the\nviability-weighted curvature."),
    ("the seven domain bridges\nas optics, with per-optic Lipschitz",
     "the seven bridges as optics, with per-optic Lipschitz"),
    ("with the adapter-level optic statement and verified at scale;\nthe $\\infty$-categorical extension is developed in homotopy type\ntheory, its proof-sketch status marked.",
     "with the adapter-level optic statement, verified at scale;\nthe $\\infty$-categorical extension in homotopy type theory\ncarries proof-sketch status, marked."),
    ("adjustments can\nunexpectedly push a system into failure",
     "adjustments can push a system into failure"),
    ("environments, they constantly adjust their internal strategies to\nremain viable.",
     "environments, constantly adjusting their internal strategies to\nremain viable."),
    ("The framework rests on four pillars.",
     "It rests on four pillars."),
    ("(KKT projection) as its connection",
     "(KKT projection) as connection"),
    ("piecewise-holonomy\nformula, the boundary reset of loops crossing a\nconstraint-switching wall transversally in \\emph{pairs} at its\ntrue order",
     "piecewise-holonomy\nformula, with boundary resets at their true order for loops\ncrossing a switching wall transversally in \\emph{pairs}"),
    ("measuring this\naccumulation through the policy holonomy",
     "measuring the\naccumulation through policy holonomy"),
    ("in homotopy type theory\ncarries proof-sketch status, marked.",
     "in homotopy type theory, proof-sketch status marked."),
    ("types the seven bridges as optics",
     "types seven bridges as optics"),
    ("into one stratified $G_C$-reduced\nbundle.",
     "into one stratified bundle."),
    ("It rests on four pillars.", "Four pillars."),
]
for old_t, new_t in TRIMS:
    if tex.count(old_t) != 1:
        print(f"[TRIM-ANCHOR-FAIL] {old_t[:60]!r} count={tex.count(old_t)}")
        fail += 1
        continue
    tex = tex.replace(old_t, new_t, 1)
    print(f"[TRIM] applied: {len(old_t)} -> {len(new_t)} chars")

# bibliography retarget
tex = tex.replace("\\bibliography{companion_refs_v9}",
                  "\\bibliography{companion_refs_v10}")
shutil.copy(BASE + "scripts/companion_refs_v9.bib",
            BASE + "scripts/companion_refs_v10.bib")
shutil.copy(BASE + "download/companion_refs_v9.bib",
            BASE + "download/companion_refs_v10.bib")

open(V10, "w", encoding="utf-8").write(tex)


def num_tokens(s):
    s = re.sub(r"(?<!\\)%.*", "", s)
    s = re.sub(r"([0-9]+(?:\.[0-9]+)?)\s*\\times\s*10\^\{?(-?[0-9]+)\}?",
               r"\1e\2", s)
    return Counter(re.findall(r"\d+(?:\.\d+)?", s))


def labels(s):
    return Counter(re.findall(r"\\label\{([^}]*)\}", s))


def citekeys(s):
    out = Counter()
    for keys, k in Counter(re.findall(r"\\cite[tp]?\{([^}]*)\}", s)).items():
        for key in keys.split(","):
            out[key.strip()] += k
    return out


# G1 labels
l9, l10 = labels(v9), labels(tex)
missing_labels = l9 - l10
added_labels = l10 - l9
print(f"[{'PASS' if not missing_labels and not added_labels else 'FAIL'}] "
      f"G1 labels: missing={dict(missing_labels)} added={dict(added_labels)}")
if missing_labels or added_labels:
    fail += 1

# G2 cite keys
c9, c10 = citekeys(v9), citekeys(tex)
dropped = [k for k in c9 if c10.get(k, 0) == 0]
newkeys = [k for k in c10 if k not in c9]
print(f"[{'PASS' if not dropped and not newkeys else 'FAIL'}] "
      f"G2 cite keys: dropped={dropped} new={newkeys}")
if dropped or newkeys:
    fail += 1

# G3 numbers
n9, n10 = num_tokens(v9), num_tokens(tex)
missing = n9 - n10
added = n10 - n9
WL_DEL = {"9": 1}  # companion_refs_v9 -> v10 bibliography digit
unexp = {t: c - WL_DEL.get(t, 0) for t, c in missing.items()
         if c > WL_DEL.get(t, 0)}
print(f"[{'PASS' if not unexp else 'FAIL'}] G3 numbers: "
      f"missing={dict(missing)} (whitelist: bib version digit)")
if unexp:
    fail += 1
print(f"[INFO] G3 added tokens: {dict(added)}")

# G4 abstract
m = re.search(r"\\textbf\{Abstract\.\}(.*?)\\par\s*\n\\vspace",
              tex, re.S)
body = m.group(1)
stripped = re.sub(r"\\[a-zA-Z]+", " ", body)
nwords = len(re.findall(r"[A-Za-z0-9\-]+", stripped))
opens = "When adaptive systems navigate fluctuating" in body
print(f"[{'PASS' if nwords <= 265 and opens else 'FAIL'}] "
      f"G4 abstract: {nwords} words (cap 265), opens-with-Gemini={opens}")
if nwords > 265 or not opens:
    fail += 1

# G5 forbidden patterns
PATTERNS = [
    (r"not a smooth curvature",), (r"not a smooth [Hh]essian",),
    (r"is now a theorem",), (r"our previous(ly)?",),
    (r"previously explored",), (r"is final for",),
    (r"[Ww]hat this closes",), (r"self-contained",),
    (r"earlier drafts?",), (r"prior versions? of this",),
    (r"in this (round|revision|pass)",), (r"as requested",),
    (r"\bchat\b",), (r"the author'?s earlier",), (r"[Hh]omogenized",),
    (r"\bZai\b",),
]
stripped_tex = re.sub(r"(?<!\\)%.*", "", tex)
pat_fail = sum(1 for (p,) in PATTERNS if re.search(p, stripped_tex))
print(f"[{'PASS' if pat_fail == 0 else 'FAIL'}] G5 forbidden patterns")
fail += pat_fail

# G6 Gemini presence
GEMINI_SENTENCES = [
    "When adaptive systems navigate fluctuating",
    "path-dependent vulnerability",
    "Why has this geometric insight not been systematically applied",
    "The difficulty lies in active-set switches",
    "Rather than treating constraint switches as troublesome",
    "Our core contributions are organized as follows",
    "To ensure precision while remaining accessible across",
    "We now assemble the components into a single mathematical",
    "In classical mechanics, Noether's theorem establishes",
    "To ensure the framework provides concrete, falsifiable",
    "A central challenge in systems biology is connecting wildly",
    "Does this elaborate seven-domain feedback loop actually",
    "In a companion manuscript, this geometric framework is applied",
]
tex_plain = re.sub(r"\\cite[tp]?\{[^}]*\}", " ", tex)
tex_plain = re.sub(r"\\(emph|textbf|textit|mathbf)\{([^}]*)\}", r"\2", tex_plain)
tex_plain = re.sub(r"\\[a-zA-Z]+", " ", tex_plain)
norm = re.sub(r"\s+", " ", tex_plain).replace(" ,", ",")
miss = [s for s in GEMINI_SENTENCES
        if s not in norm and re.sub(r"\s+", " ", s) not in norm]
print(f"[{'PASS' if not miss else 'FAIL'}] G6 Gemini presence "
      f"({len(GEMINI_SENTENCES) - len(miss)}/{len(GEMINI_SENTENCES)})")
if miss:
    fail += 1
    for s in miss:
        print("  missing:", s)

# ASCII guard
if "CYCLIC ENVIRONMENTAL" in tex or "HOMEOSTASIS " in tex:
    print("[FAIL] ASCII-art leakage")
    fail += 1
else:
    print("[PASS] no ASCII-art leakage")

print()
if fail:
    print(f"FAILED with {fail} gate failure(s)")
    sys.exit(1)
print("ALL GATES PASSED -- companion_categorical_v10.tex built")
