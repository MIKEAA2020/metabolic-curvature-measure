#!/usr/bin/env python3
"""V17 enrichment completeness verification (v17 vs v16).

Checks that journal_manuscript_v17.tex differs from
journal_manuscript_v16.tex ONLY in the v17 enrichment regions (plus
the mechanical version bump: header note, \\input filename, audit
count 344), with nothing lost:
  1. Abstract: bio-anchored rebuild, <= 255 audit-style words,
     every v16-abstract number still present somewhere in v17.
  2. Numeric-token multiset: removed tokens exactly the expected
     three (the abstract's partial-r 0.269 re-quote drop and the
     two audit-count 301s); added tokens confined to the v17
     fragment texts and replacement regions (the audit_v25 ledger
     separately verifies every added number against the JSON
     artifacts).
  3. Label census: v16 labels all present; new labels exactly the
     nine v17 ones.
  4. Citation census: v16 keys unchanged; + kacser1973,
     + heinrich1974.
  5. Environment census: +2 table (tab:walls, tab:regulons).
  6. Section census: same \\section count; +7 \\subsection.
  7. Bibliography: v17 refs = v16 refs + the two MCA entries.
  8. v16 body preservation: every v16 line survives verbatim in v17
     outside the replaced regions (abstract, plan paragraph,
     limitations tail, two Methods sentences, refs pointer).
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


v16 = load("journal_manuscript_v16.tex")
v17 = load("journal_manuscript_v17.tex")
r16 = load("journal_manuscript_v16_bmb_refs.tex")
r17 = load("journal_manuscript_v17_bmb_refs.tex")

fail = 0


def report(name, ok, note=""):
    global fail
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" +
          (f" ({note})" if note else ""))
    if not ok:
        fail += 1


# ---- 1. Abstract -------------------------------------------------------
A16 = re.search(r"\\begin\{abstract\}.*?\\end\{abstract\}", v16,
                re.S).group(0)
A17 = re.search(r"\\begin\{abstract\}.*?\\end\{abstract\}", v17,
                re.S).group(0)
inner = A17[len("\\begin{abstract}"):-len("\\end{abstract}")]
nwords = len(re.findall(r"[A-Za-z0-9\-]+", re.sub(r"\\[a-zA-Z]+", " ",
                                                   inner)))
missing_abs = set(num_tokens(A16)) - set(num_tokens(v17))
report("abstract: <= 255 words, bio-anchored", nwords <= 255 and
       "regulons" in A17 and "fork metabolites" in A17 and
       "post-translational" in A17, f"{nwords} words")
report("abstract: every v16-abstract number survives in v17",
       not missing_abs, f"missing={sorted(missing_abs)}")

# ---- 2. Numeric-token multiset ----------------------------------------
n16, n17 = num_tokens(v16), num_tokens(v17)
removed = n16 - n17
added = n17 - n16
report("numbers: removed tokens exactly the expected three "
       "(abstract partial-r re-quote + two 301 audit counts)",
       dict(removed) == {"0.269": 1, "301": 2},
       f"removed={dict(removed)}")

expected_src = [load("v17_frag_abstract_full.tex"),
                load("v17_frag_worked_example.tex"),
                load("v17_frag_walls_interior.tex"),
                load("v17_frag_order.tex"),
                load("v17_frag_anatomy.tex"),
                load("v17_frag_mca.tex"),
                load("v17_frag_memory.tex"),
                "\\input{journal_manuscript_v17_bmb_refs}",
                # plan-of-the-paper replacement delta text
                """works a hand-checkable example, and records the categorical
reading in brief. --- where the curvature mass sits chemically, the
interior architecture it defines, and a construction-order rule for
genotype design --- the empirical association, the anatomy of one
switch, and the protein-layer decision. positions the framework
against smooth sensitivity theory, develops the memory-substrate
deduction, and""",
                # limitations item 8
                """Enrichment and prediction provenance. The regulon and
operon enrichment of \\S\\ref{sec:anatomy} is correlational and
shares the parent association's confound structure; the
metabolomics, cross-species, and effector statements of
\\S\\S\\ref{sec:walls}--\\ref{sec:memory} are predictions, labeled as
such and untested here.""",
                # Methods statistical-protocols insert
                """The enrichment statistics of
\\S\\ref{sec:anatomy} use Fisher exact tests of the top-$\\kmu$
quartile against PRECISE regulatory annotations with the panel as
background, Benjamini--Hochberg corrected across the testable sets
($31$ regulons, $31$ operons, $18$ iModulons); the
within-versus-across-operon curvature gap and its disjoint-reaction
GPR control use $5{,}000$-fold label permutation ($p$ reported as
$< 2 \\times 10^{-4}$). The wall-coordinate, class-share, and
order-rule statistics of \\S\\S\\ref{sec:walls}--\\ref{sec:order}
aggregate the deposited per-reaction curvature masses of the eleven
boundary-crossing M1 sweeps (each normalized by its own total) and
the deposited M3 double-mutant panels, with $10^4$-fold class-label
permutation for the class shares. The worked example of
\\S\\ref{sec:example} is machine-verified by LP re-solves at
wall-straddling parameter values under both tie-break variants.""",
                "($344$ checks)", "suite of $344$ numeric checks"]
expected = num_tokens("\n".join(expected_src))
unexpected = added - expected
report("numbers: added tokens confined to the v17 fragments and "
       "replacement regions", not unexpected,
       f"unexpected={dict(unexpected)}")

# ---- 3. Labels ---------------------------------------------------------
l16, l17 = labels(v16), labels(v17)
new_labels = set(l17) - set(l16)
lost_labels = set(l16) - set(l17)
expected_new = {"sec:example", "sec:walls", "tab:walls", "sec:interior",
                "sec:order", "sec:anatomy", "tab:regulons", "sec:mca",
                "sec:memory"}
report("labels: v16 labels all kept; new labels exactly the nine v17",
       not lost_labels and new_labels == expected_new,
       f"new={sorted(new_labels)}, lost={sorted(lost_labels)}")

# ---- 4. Citations ------------------------------------------------------
c16, c17 = citekeys(v16), citekeys(v17)
new_cites = set(c17) - set(c16)
lost_cites = set(c16) - set(c17)
report("citations: v16 keys kept; + kacser1973 + heinrich1974",
       not lost_cites and new_cites == {"kacser1973", "heinrich1974"},
       f"new={sorted(new_cites)}, lost={sorted(lost_cites)}")

# ---- 5. Environments ---------------------------------------------------
e16, e17 = environments(v16), environments(v17)
delta = {k: e17[k] - e16[k] for k in e17 if e17[k] != e16.get(k, 0)}
report("environments: +2 table (tab:walls, tab:regulons), rest "
       "identical", delta == {"table": 2}, f"delta={delta}")

# ---- 6. Sections -------------------------------------------------------
sec16 = len(re.findall(r"\\section\{", v16))
sec17 = len(re.findall(r"\\section\{", v17))
sub16 = len(re.findall(r"\\subsection\{", v16))
sub17 = len(re.findall(r"\\subsection\{", v17))
report("sections: same section count; +7 subsections",
       sec16 == sec17 and sub17 == sub16 + 7,
       f"sections {sec17} (v16 {sec16}), subsections {sub17} "
       f"(v16 {sub16})")

# ---- 7. Bibliography ---------------------------------------------------
new_bibs = set(
    re.findall(r"\\bibitem(?:\[[^\]]*\])?\{([^}]*)\}", r17)) - set(
    re.findall(r"\\bibitem(?:\[[^\]]*\])?\{([^}]*)\}", r16))
report("bibliography: exactly + kacser1973 + heinrich1974 (29 total)",
       new_bibs == {"kacser1973", "heinrich1974"} and
       r17.count("\\bibitem") == 29,
       f"new={sorted(new_bibs)}")

# ---- 8. v16 body preservation ------------------------------------------
replaced_exact = {
    "\\input{journal_manuscript_v16_bmb_refs}",
    "single workstation. An automated suite of $301$ numeric checks",
}
kept = 0
lost_lines = []
for line in v16.split("\n"):
    s = line.strip()
    if s == "" or s.startswith("%"):
        continue
    if line in replaced_exact or line.strip() in replaced_exact:
        continue
    if any(line in rep or line.strip() in rep
           for rep in [A16, A17,
                       re.search(r"\\paragraph\{Plan of the paper\.\}"
                                 r".*?complete the paper\.", v16,
                                 re.S).group(0),
                       re.search(r"\\paragraph\{Plan of the paper\.\}"
                                 r".*?complete the paper\.", v17,
                                 re.S).group(0),
                       "protocol with TPM log-fold changes. Every "
                       "manuscript number traces\nto a deposited "
                       "artifact file and is re-derived by the "
                       "automated\nnumeric verification described "
                       "under Reproducibility ($301$\nchecks)."]):
        continue
    if line not in v17:
        lost_lines.append(line)
    else:
        kept += 1
report("v16 body lines preserved verbatim (outside the replaced "
       "regions)", not lost_lines,
       f"kept={kept}, lost={lost_lines[:6]}")

print()
if fail == 0:
    print("ALL COMPLETE: v17 = v16 + the audited V17 enrichment only.")
else:
    print(f"{fail} FAILURES")
    raise SystemExit(1)
