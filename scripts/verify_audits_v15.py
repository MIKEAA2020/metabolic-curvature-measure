#!/usr/bin/env python3
"""Joint numeric verification of the two humanized audits (Gemini + Grok)
against journal_manuscript_v14.tex (the audited baseline).

Source file: external_audits/humanized/gemini,grok humanized.txt
  - lines 1..532:  Gemini's rewrite (digest-style, accessible register)
  - lines 533..902: Grok's rewrite (complete restructure, terse register)

Checks, per audit:
  1. Extract numeric tokens after normalization (scientific notation,
     thousands separators, LaTeX braces, percent signs).
  2. Compare against v14's token multiset (comments stripped).
  3. Report every audit token NOT present in v14, with context, for
     manual adjudication (stale / reformulated / not-an-audited-claim).
  4. Curated spot-checks of load-bearing claims across all three texts.
"""
import re
from collections import Counter

BASE = "/home/z/my-project/metabolic-curvature-measure/"
AUDIT = BASE + "external_audits/humanized/gemini,grok humanized.txt"
V14 = BASE + "scripts/journal_manuscript_v14.tex"


def strip_comments(tex):
    out = []
    for line in tex.split("\n"):
        m = re.search(r"(?<!\\)%", line)
        out.append(line[:m.start()] if m else line)
    return "\n".join(out)


def normalize_sci(s):
    """Fold scientific-notation variants to a single 'MeE' token."""
    # LaTeX: 2.6 \times 10^{-17}
    s = re.sub(r"([0-9]+(?:\.[0-9]+)?)\s*\\times\s*10\^\{?(-?[0-9]+)\}?",
               r"\1e\2", s)
    # Unicode/markdown: 2.6 × 10^-17 / 2.6x10^-17 / 2.6 × 10−17
    s = re.sub(r"([0-9]+(?:\.[0-9]+)?)\s*[×x]\s*10\^?\s?\{?(-?[0-9]+)\}?",
               r"\1e\2", s)
    # 10^{-17} bare (no mantissa) -> 1e-17
    s = re.sub(r"(?<![0-9e.])10\^\{?(-?[0-9]+)\}?", r"1e\1", s)
    s = re.sub(r"(?<![0-9e.])10\^?\s?(-?[0-9]+)\b(?![\}])", r"1e\1", s
               ) if "10^" not in s and "10^" not in s else s
    return s


def tokens(s):
    s = strip_comments(s) if "\\documentclass" in s else s
    s = normalize_sci(s)
    s = s.replace("{,}", "").replace(",", "")
    # unicode minus -> -
    s = s.replace("−", "-").replace("–", "-").replace("—", "-")
    s = s.replace("\\%", "").replace("%", "")
    # \varepsilon_mu etc. produce no digits; RR^p -> keep p
    toks = re.findall(r"(?<![a-zA-Z\\])(\d+(?:\.\d+)?(?:e-?\d+)?)", s)
    return Counter(toks)


raw = open(AUDIT, encoding="utf-8", errors="replace").read()
lines = raw.split("\n")
gem = "\n".join(lines[0:532])
grok = "\n".join(lines[532:902])
v14 = strip_comments(open(V14).read())

tv = tokens(v14)
report = {}
for name, sec in [("GEMINI", gem), ("GROK", grok)]:
    t = tokens(sec)
    missing = t - tv
    print(f"\n===== {name}: {sum(t.values())} numeric tokens, "
          f"{sum(missing.values())} not found in v14 =====")
    # group by token with first context
    ctxs = {}
    for m in re.finditer(r"(?<![a-zA-Z\\])\d+(?:\.\d+)?(?:e-?\d+)?",
                         normalize_sci(sec.replace("{,}", "")
                                       .replace(",", ""))):
        tok = m.group(0)
        if tok in missing and tok not in ctxs:
            a, b = max(0, m.start() - 55), min(len(sec), m.end() + 55)
            ctxs[tok] = " ".join(sec[a:b].split())
    for tok in sorted(ctxs, key=lambda x: (len(x), x)):
        print(f"  [{name}] '{tok}' x{missing[tok]}: ...{ctxs[tok]}...")
    report[name] = missing

# Curated spot-checks: load-bearing claims present in v14.
spot = [
    ("primary r", r"\+0\.395"), ("p", r"2\.6\s*\\?\times\s*10\^\{-17\}"),
    ("partial", r"\+0\.269"), ("Spearman panel", r"\+0\.414"),
    ("protein null", r"-0\.083"), ("transcript matched", r"\+0\.419"),
    ("epistasis rho", r"0\.865"), ("memory pct", r"66\\?%"),
    ("slope", r"1\.00"), ("mass pct", r"93\.4"),
    ("kmu mass", r"288\.77"), ("rank invariance", r"0\.99998"),
    ("tie range lo", r"\+0\.386"), ("tie range hi", r"\+0\.396"),
    ("fan area", r"0\.235"), ("fan enum", r"0\.235000068"),
    ("shadow price", r"0\.099544"), ("intercept", r"-0\.0124"),
    ("atom", r"-0\.006439"), ("atom t", r"0\.0358286"),
]
print("\n===== v14 spot-checks =====")
for label, pat in spot:
    print(f"  [{'PASS' if re.search(pat, v14) else 'FAIL'}] {label}")

print("\nSummary: GEMINI unmatched:", sum(report['GEMINI'].values()),
      "tokens |", sorted(report['GEMINI']))
print("Summary: GROK   unmatched:", sum(report['GROK'].values()),
      "tokens |", sorted(report['GROK']))
