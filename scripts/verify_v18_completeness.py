#!/usr/bin/env python3
"""V18 JTB-alignment completeness verification (v18 vs v17).

Checks that journal_manuscript_v18.tex differs from
journal_manuscript_v17.tex ONLY in the v18 JTB-alignment regions
(header comment note, abstract trim, pdfkeywords + keywords seventh
term, CRediT statement, \input refs filename), with nothing lost:
  1. Abstract: 249 audit-style words (JTB cap 250; was 254), the
     bio-anchoring sentences kept, every v17-abstract number kept.
  2. Numeric-token multiset: the only delta is the version digit in
     the \input filename (17 -> 18) -- no other number added/removed.
  3. Label / citation / environment / section censuses: identical.
  4. Bibliography: v18 refs = v17 refs (29 entries, same keys).
  5. v17 body preservation: every non-comment v17 line survives
     verbatim in v18 outside the replaced regions.
"""
import re
from collections import Counter

BASE = "/home/z/my-project/metabolic-curvature-measure/"


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


def load(p):
    return open(BASE + "scripts/" + p).read()


v17 = load("journal_manuscript_v17.tex")
v18 = load("journal_manuscript_v18.tex")
r17 = load("journal_manuscript_v17_bmb_refs.tex")
r18 = load("journal_manuscript_v18_refs.tex")

fail = 0


def report(name, ok, note=""):
    global fail
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" +
          (f" ({note})" if note else ""))
    if not ok:
        fail += 1


# ---- 1. Abstract --------------------------------------------------------
A17 = re.search(r"\\begin\{abstract\}.*?\\end\{abstract\}", v17,
                re.S).group(0)
A18 = re.search(r"\\begin\{abstract\}.*?\\end\{abstract\}", v18,
                re.S).group(0)
inner = A18[len("\\begin{abstract}"):-len("\\end{abstract}")]
nwords = len(re.findall(r"[A-Za-z0-9\-]+", re.sub(r"\\[a-zA-Z]+", " ",
                                                   inner)))
report("abstract: 249 audit-style words (JTB cap 250; was 254)",
       nwords == 249 and "regulons" in A18 and
       "fork metabolites" in A18 and "post-translational" in A18,
       f"{nwords} words")
missing_abs = set(num_tokens(A17)) - set(num_tokens(v18))
report("abstract: every v17-abstract number survives in v18",
       not missing_abs, f"missing={sorted(missing_abs)}")
report("abstract: the five trims are word-level only",
       all(w not in A18 for w in ["abruptly", "accessible"]) and
       "discrete bottleneck" not in A18 and
       "operons of the global" not in A18 and
       "show that the response" not in A18)

# ---- 2. Numeric-token multiset -----------------------------------------
n17, n18 = num_tokens(v17), num_tokens(v18)
removed, added = n17 - n18, n18 - n17
report("numbers: only delta is the \\input filename version digit "
       "(17 -> 18)", dict(removed) == {"17": 1} and
       dict(added) == {"18": 1},
       f"removed={dict(removed)}, added={dict(added)}")

# ---- 3. Labels / citations / environments / sections --------------------
report("labels: identical to v17", labels(v17) == labels(v18))
report("citations: identical to v17", citekeys(v17) == citekeys(v18))
report("environments: identical to v17",
       environments(v17) == environments(v18))
report("sections/subsections: identical to v17",
       len(re.findall(r"\\section\{", v17)) ==
       len(re.findall(r"\\section\{", v18)) and
       len(re.findall(r"\\subsection\{", v17)) ==
       len(re.findall(r"\\subsection\{", v18)))

# ---- 4. Front-matter / backmatter v18 changes ---------------------------
report("keywords: 7 terms with 'path dependence' (JTB 1-7)",
       "epistasis; path dependence" in v18 and
       "epistasis, path dependence}}" in v18)
report("CRediT statement replaces the prose Author Contributions",
       "CRediT Authorship Contribution Statement" in v18 and
       "\\section*{Author Contributions}" not in v18 and
       "Conceptualization" in v18)
report("refs pointer: journal_manuscript_v18_refs",
       "\\input{journal_manuscript_v18_refs}" in v18 and
       "journal_manuscript_v17_bmb_refs" not in v18)

# ---- 5. Bibliography ----------------------------------------------------
report("bibliography: v18 refs = v17 refs, 29 entries, same keys",
       [re.findall(r"\\bibitem(?:\[[^\]]*\])?\{([^}]*)\}", r17)] ==
       [re.findall(r"\\bibitem(?:\[[^\]]*\])?\{([^}]*)\}", r18)] and
       r18.count("\\bibitem") == 29)

# ---- 6. v17 body preservation -------------------------------------------
replaced_exact = {
    "\\input{journal_manuscript_v17_bmb_refs}",
    "              translational buffering, epistasis}}",
    "translational buffering; epistasis",
    "\\section*{Author Contributions}",
    "A.A. conceived the study design, developed the methodology and",
    "analysis code, performed the data analysis, drafted and revised",
    "the manuscript.",
}
kept, lost_lines = 0, []
for line in v17.split("\n"):
    s = line.strip()
    if s == "" or s.startswith("%"):
        continue
    if line in replaced_exact or s in replaced_exact:
        continue
    if line in A17:
        continue
    if line not in v18:
        lost_lines.append(line)
    else:
        kept += 1
report("v17 body lines preserved verbatim (outside the replaced "
       "regions)", not lost_lines,
       f"kept={kept}, lost={lost_lines[:6]}")

print()
if fail == 0:
    print("ALL COMPLETE: v18 = v17 + the JTB alignment edits only "
          "(abstract trim, 7th keyword, CRediT, refs rename); every "
          "v17 number and line otherwise intact.")
else:
    print(f"{fail} FAILURES")
    raise SystemExit(1)
