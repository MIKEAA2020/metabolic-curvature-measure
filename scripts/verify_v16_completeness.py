#!/usr/bin/env python3
"""Universal Gemini-adoption completeness verification (v16 vs v15).

Checks that journal_manuscript_v16.tex differs from
journal_manuscript_v15.tex ONLY in the Gemini-prose adoption regions
(plus the mechanical version bump: header filenames, the new header
note, and the \\input filename), with nothing lost:
  1. Abstract: rebuilt on Gemini's abstract (opens with Gemini's
     first sentence), <= 255 audit-style words, and every v15-abstract
     number present (the M3D mention is the only drop, per Gemini's
     own abstract).
  2. Numeric-token multiset: the ONLY expected deltas are the
     whitelisted ones below (version digit, citation-key digits,
     model-identifier digits, re-quotes of audited body claims).
  3. Label census       (\\label{...} multisets identical)
  4. Citation census    (same key set; counts may gain re-citations)
  5. Environment census (+1 itemize from the epistasis bullet list;
     +3 \\subsection from Gemini's Discussion structure)
  6. Section census     (same \\section count; +3 subsections)
  7. Bibliography identity (v16_bmb_refs vs v15_bmb_refs,
     byte-identical except the version-comment)
  8. Gemini-presence: the verbatim adoption sentences present.
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


def sections(s):
    return Counter(re.findall(r"\\(sub)*section\*?\{", s))


def load(p):
    return open(p).read()


base = "/home/z/my-project/metabolic-curvature-measure/scripts/"
v16 = load(base + "journal_manuscript_v16.tex")
v15 = load(base + "journal_manuscript_v15.tex")
refs16 = load(base + "journal_manuscript_v16_bmb_refs.tex")
refs15 = load(base + "journal_manuscript_v15_bmb_refs.tex")

fail = 0


def report(name, ok, note=""):
    global fail
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" ({note})" if note else ""))
    if not ok:
        fail += 1


# 1. Abstract: word cap, Gemini opening, number preservation
A16 = re.search(r"\\begin\{abstract\}.*?\\end\{abstract\}", v16, re.S).group(0)
A15 = re.search(r"\\begin\{abstract\}.*?\\end\{abstract\}", v15, re.S).group(0)
inner16 = A16[len("\\begin{abstract}"):-len("\\end{abstract}")]
stripped = re.sub(r"\\[a-zA-Z]+", " ", inner16)
nwords = len(re.findall(r"[A-Za-z0-9\-]+", stripped))
opens = A16.strip().startswith("\\begin{abstract}\n\\noindent\nConstraint-based models such as flux balance analysis (FBA) predict")
na16, na15 = num_tokens(A16), num_tokens(A15)
abs_missing = na15 - na16
report("abstract: Gemini opening + <= 255 words",
       opens and nwords <= 255, f"{nwords} words, opens={opens}")
report("abstract numbers preserved (M3D '3' whitelisted)",
       set(abs_missing) <= {"3"},
       f"missing={dict(abs_missing)}")

# 2. Number multiset (document-wide, comments stripped)
n16, n15 = num_tokens(v16), num_tokens(v15)
missing = n15 - n16
added = n16 - n15
# Whitelisted deletions:
#   '15'  : the \input refs filename version digit (v15 -> v16)
#   '3'   : the M3D compendium mention in the v15 abstract (per
#           Gemini's own abstract; M3D named in the body)
#   '2001','2002' : citation-key digits of \citep{edwards2001, ibarra2002}
#           removed from the intro opening (both keys still cited:
#           rem:layersep, fitness-envelope, scope)
#   '0'   : one prose restatement of "Sv = 0" in the Sec. 2.1 lead
#           (the equation itself keeps it)
#   '1','2' : the tie-break table caption's "(stage-2 \ell_1, s_2)"
#           naming (kept in the body text and findings)
WL_DEL = {"15": 1, "3": 1, "2001": 1, "2002": 1, "0": 1, "1": 1, "2": 2}
unexp_del = {t: c - WL_DEL.get(t, 0) for t, c in missing.items()
             if c > WL_DEL.get(t, 0)}
report("number multiset: deletions all whitelisted", not unexp_del,
       f"missing={dict(missing)}")
if unexp_del:
    print("  unexplained deletions:", dict(unexp_del))
# Whitelisted additions:
#   '16'  : \input filename version digit
#   '11','12'     : Discussion 6.2 re-quote of the 11-of-12 invisible events
#   '424','2.6','17','0.083','366','66' : claim-list re-quotes of
#                   audited body claims (Sec. 1 five-findings list)
#   '2003','2017','2011' : citation-key digits of new \citep occurrences
#                   (borrelli2003 in the intro; monk2017/orth2011 in
#                   the Sec. 4 opening)
#   '1515','1366' : model identifiers (iML1515/iJO1366) named in the
#                   Sec. 4 opening and the Methods models paragraph
#   '1'   : "(p = 1)" in the In-words gloss (p=1 also in rem:support)
#   '2'   : D^2 Phi / D^2 v* in the claim list + log2-fold wording
#   '0'   : "h -> 0" in the bridge opening/thm item; "\neq 0" in the
#           coupling theorem
WL_ADD = {"16": 1, "11": 1, "12": 1, "424": 1, "2.6": 1, "17": 1,
          "0.083": 1, "366": 1, "66": 1, "2003": 1, "2017": 1,
          "2011": 1, "1515": 2, "1366": 2, "1": 1, "2": 1, "0": 2}
unexp_add = {t: c - WL_ADD.get(t, 0) for t, c in added.items()
             if c > WL_ADD.get(t, 0)}
report("number multiset: additions all whitelisted", not unexp_add,
       f"added={dict(added)}")
if unexp_add:
    print("  unexplained additions:", dict(unexp_add))

# 3. Labels
l15, l16 = labels(v15), labels(v16)
report("label census identical", l15 == l16,
       f"missing={dict(l15 - l16)} added={dict(l16 - l15)}")

# 4. Citation keys (set identity; count gains = re-citations)
c15, c16 = citekeys(v15), citekeys(v16)
dropped = [k for k in c15 if c16.get(k, 0) == 0]
new = [k for k in c16 if k not in c15]
report("citation key set identical", not dropped and not new,
       f"dropped={dropped} new={new}")

# 5. Environment census
e15, e16 = environments(v15), environments(v16)
env_ok = (e16 - e15) == Counter({"itemize": 1}) and \
         (e15 - e16) == Counter()
report("environment census: +1 itemize only", env_ok,
       f"+{dict(e16 - e15)} -{dict(e15 - e16)}")

# 6. Section census
s15, s16 = sections(v15), sections(v16)
sec_ok = (s16 - s15) == Counter({"sub": 3}) and \
         (s15 - s16) == Counter()
report("section census: +3 subsections (Gemini Discussion)", sec_ok,
       f"+{dict(s16 - s15)} -{dict(s15 - s16)}")

# 7. Bibliography identity (ignoring the version-comment line)
r15l = [ln for ln in refs15.split("\n") if "journal_manuscript_v1" not in ln]
r16l = [ln for ln in refs16.split("\n") if "journal_manuscript_v1" not in ln]
report("bibliography byte-identical (outside version comment)",
       r15l == r16l)

# 8. Gemini verbatim presence (whitespace-normalized)
GEMINI_SENTENCES = [
    "Constraint-based models such as flux balance analysis (FBA) predict",
    "not an ordinary function but a discrete measure concentrated",
    "the natural mathematical language for metabolic rerouting",
    "creates a profound blind spot",
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
    "work bridges this divide by providing an explicit geometric",
]
norm16 = re.sub(r"\s+", " ", v16)
miss = [s for s in GEMINI_SENTENCES if s not in norm16]
report(f"Gemini verbatim presence ({len(GEMINI_SENTENCES) - len(miss)}"
       f"/{len(GEMINI_SENTENCES)})", not miss)
if miss:
    print("  missing:", miss)

# 9. v15's proofs untouched (the proofs section byte-identical)
p15 = v15[v15.find("\\section{Proofs}"):]
p16 = v16[v16.find("\\section{Proofs}"):]
# v16 proofs region extends to the same backmatter; compare up to
# the Data Availability section
end15 = p15.find("\\section*{Data, Software, and Code Availability}")
end16 = p16.find("\\section*{Data, Software, and Code Availability}")
report("proofs + techproofs + backmatter byte-identical to v15",
       p15[:end15] == p16[:end16])

print()
if fail:
    print(f"FAILED with {fail} check(s)")
    raise SystemExit(1)
print("ALL COMPLETE: v16 = v15 + universal Gemini prose adoption, "
      "nothing lost")
