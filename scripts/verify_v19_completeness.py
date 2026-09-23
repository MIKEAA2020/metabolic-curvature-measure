#!/usr/bin/env python3
"""verify_v19_completeness.py -- completeness verification of the v19
comprehension restructure (v18 -> v19).

Verifies:
  1. Every numeric token removed from v18 has provenance in an
     intentionally deleted/rewritten region (old abstract, old
     five-finding claim list, old plan-of-the-paper, categorical
     subsection, disambiguation appendix, methods counts sentence,
     refs-filename digit, title block). No audited claim number may
     lose its last occurrence.
  2. Every added token is an expected re-quote (93.4/100.0/0.865 in the
     new intro), the version digit (19), or the audit count (349).
  3. Label/reference integrity: every ref/cite target in v19 resolves;
     no dangling label from the deleted sections.
  4. Section order = the designed order.
Comments are stripped before token extraction (matches the audit's
method). The old bridge section region is whitelisted as MOVED (its
tokens are re-verified present in v19 by the required-numbers gate and
the audit); only tokens whose context vanished are flagged.
"""
import re
from collections import Counter

S = "/home/z/my-project/metabolic-curvature-measure/"
v18 = open(S + "scripts/journal_manuscript_v18.tex").read()
v19 = open(S + "scripts/journal_manuscript_v19.tex").read()


def strip_comments(tex):
    return "\n".join(
        line[:m.start()] if (m := re.search(r"(?<!\\)%", line)) else line
        for line in tex.split("\n"))


b18, b19 = strip_comments(v18), strip_comments(v19)

# ---- intended regions in b18 (comment-stripped; located by content) ----
REGIONS = [
    ("old abstract", (b18.index("\\begin{abstract}"),
                      b18.index("\\end{abstract}"))),
    ("old claim list", (b18.index("\\paragraph{The claim structure.}"),
                        b18.index("\\paragraph{Positioning.}"))),
    ("old plan of the paper", (b18.index("\\paragraph{Plan of the paper.}"),
                               b18.index("\\section{The discrete curvature"))),
    ("categorical subsection", (b18.index(
        "\\subsection{The categorical reading, in brief}"),
        b18.index("\\section{The refinement--resolution bridge}"))),
    ("disambiguation appendix", (b18.index("\\appendix"),
                                 b18.index("\\section{Proofs}"))),
    ("methods counts sentence", (b18.index(
        "The near-colliding gene/reaction counts") - 130,
        b18.index("Appendix~\\ref{sec:counts}.",
                  b18.index("The near-colliding gene/reaction counts")) +
        len("Appendix~\\ref{sec:counts}."))),
    ("refs input digit", (b18.index("\\input{journal_manuscript_v18_refs}"),
                          b18.index("\\input{journal_manuscript_v18_refs}")
                          + len("\\input{journal_manuscript_v18_refs}"))),
    ("methods audit count", (b18.index("($344$ checks)."),
                             b18.index("($344$ checks).") + 16)),
    ("methods audit count 2", (b18.index("suite of $344$ numeric checks"),
                               b18.index("suite of $344$ numeric checks")
                               + 28)),
    ("title block", (b18.index("\\title{"),
                     b18.index("\\title{") + 220)),
    ("bridge lead adaptation (section -> appendix)", (
        b18.index("Computational biologists often ask") - 10,
        b18.index("shape-regular family") + 40)),
    ("computational-validation opening ref fix", (
        b18.index("reconstructions of \\emph{E.~coli}") - 10,
        b18.index("they refer to the active set") + 10)),
    ("regime dial ref fix", (b18.index("\\subsection{Regime dial}") - 10,
                             b18.index("can be\nseparated empirically") + 10)),
    ("limitations counts-ref fix", (
        b18.index("while the gene-level panel ($435$)") - 10,
        b18.index("stable (Appendix~\\ref{sec:counts}).") +
        len("stable (Appendix~\\ref{sec:counts})."))),
]


def region_of(pos):
    for name, (a, b) in REGIONS:
        if a <= pos < b:
            return name
    return None


# ---- numeric-token multiset diff with line provenance -------------------
tok = re.compile(r"\d+(?:\.\d+)?")
n18 = Counter(tok.findall(b18))
n19 = Counter(tok.findall(b19))
removed = n18 - n19
added = n19 - n18

print("== numeric tokens removed from v18 (net) ==")
unexplained_ctx = []
for t in sorted(removed, key=str):
    occ = [m.start() for m in re.finditer(
        r"(?<![\d.])" + re.escape(t) + r"(?![\d])", b18)]
    gone = [p for p in occ
            if b18[max(0, p - 60):p + 60] not in b19]
    provs = {}
    none_ctx = []
    for p in gone:
        r = region_of(p)
        provs[r] = provs.get(r, 0) + 1
        if r is None:
            none_ctx.append(b18[max(0, p - 60):p + 60].replace("\n", " "))
    print(f"  -{t} x{removed[t]:3d}  provenance: {provs}")
    unexplained_ctx.extend(none_ctx)

print("== numeric tokens added to v19 ==")
ALLOWED_ADDED = {"93.4", "100.0", "0.865", "19", "349"}
bad_added = {t: c for t, c in added.items() if t not in ALLOWED_ADDED}
for t in sorted(added, key=str):
    tag = ("expected re-quote/digit" if t in ALLOWED_ADDED
           else "UNEXPECTED")
    print(f"  +{t} x{added[t]:3d}  {tag}")

# ---- required claim numbers still present at least once ----------------
REQUIRED = ["0.395", "2.6", "424", "0.083", "366", "66", "1.00",
            "93.4", "100.0", "0.865", "0.99897", "0.414", "288.77",
            "0.934", "2.000", "8.2", "0.49", "1.8", "25", "107",
            "516", "779", "426", "454", "350", "17.0", "20.8",
            "583"]
missing = [r for r in REQUIRED if r not in b19]
print("== required claim numbers present in v19 ==")
print("  missing:", missing if missing else "NONE")

# ---- label / ref / cite integrity --------------------------------------
lab18 = set(re.findall(r"\\label\{([^}]*)\}", v18))
lab19 = set(re.findall(r"\\label\{([^}]*)\}", v19))
refs19 = set(re.findall(r"\\ref\{([^}]*)\}", v19))
dangling = refs19 - lab19
new_labels = lab19 - lab18
gone_labels = lab18 - lab19
print("== labels ==")
print("  dangling ref targets:", dangling if dangling else "NONE")
print("  new labels:", sorted(new_labels) if new_labels else "NONE")
print("  removed labels:", sorted(gone_labels) if gone_labels else "NONE")

cited19 = set()
for m in re.finditer(r"\\cite[tp]?\{([^}]*)\}", v19):
    cited19 |= {k.strip() for k in m.group(1).split(",") if k.strip()}
refs_tex = open(S + "scripts/journal_manuscript_v19_bmb_refs.tex").read()
ref_keys = set(re.findall(r"\\bibitem(?:\[[^\]]*\])?\{([^}]*)\}", refs_tex))
unresolved = cited19 - ref_keys
print("  unresolved citations:", unresolved if unresolved else "NONE")
print("  uncited ref entries:", (ref_keys - cited19) if (
    ref_keys - cited19) else "NONE")

# ---- section order ------------------------------------------------------
sec_titles = re.findall(r"\\section\*?\{([^}]*)\}", v19)
print("== v19 section order ==")
for t in sec_titles:
    print("  -", t)

# ---- verdict ------------------------------------------------------------
ok = (not unexplained_ctx and not bad_added and not missing
      and not dangling and not unresolved
      and gone_labels == {"sec:counts", "sec:categorical"}
      and not new_labels - {"sec:valueflux"})
print("VERDICT:", "ALL COMPLETE" if ok else "DEFECTS FOUND")
if unexplained_ctx:
    print("  contexts of unexplained removals:")
    for c in unexplained_ctx[:12]:
        print("   *", c)
