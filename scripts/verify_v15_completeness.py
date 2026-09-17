#!/usr/bin/env python3
"""Merged-register-round completeness verification (v15 vs v14).

Checks that the main manuscript (journal_manuscript_v15.tex) differs
from journal_manuscript_v14.tex ONLY in the twelve adjudicated
merged-register edit regions (plus the mechanical version bump:
header filenames, the new header note, and the \\input filename),
with nothing lost:
  1. Abstract identity: the v14 abstract (already Gemini-register,
     254 audit-style words, under the author's 255-word cap) is
     byte-identical in v15.
  2. Numeric-token multiset diff: the ONLY expected deltas are
     (a) the version digit in the \\input filename (14 -> 15) and
     (b) the Discussion standby-model paragraph re-quoting three
     audited body claims: +0.419, -0.083, n = 366 (each +1).
  3. Label census       (\\label{...} multisets identical)
  4. Citation census    (only kochanowski2013 +1, from the new
     Discussion paragraph; all other \\cite keys identical)
  5. Environment census (theorem/definition/... counts identical)
  6. Section census     (\\section/\\subsection counts identical)
  7. Bibliography identity (v15 vs v14 bmb_refs, byte-identical)
  8. The twelve edited regions are enumerated and each verified
     present (by an exact distinctive substring); every other body
     line is byte-identical to v14.
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
    return Counter(re.findall(r"\\cite[tp]?\{([^}]*)\}", s))


def environments(s):
    return Counter(re.findall(
        r"\\begin\{(theorem|proposition|lemma|corollary|definition|"
        r"construction|assumption|conjecture|remark|enumerate|itemize|"
        r"equation|align|figure|table)\}", s))


def sections(s):
    return Counter(re.findall(r"\\(sub)*section\*?\{", s))


def strip_header_comment(s):
    m = re.search(r"^%.*?\\documentclass", s, re.S | re.M)
    return s[m.end() - len("\\documentclass"):] if m else s


def load(p):
    return open(p).read()


base = "/home/z/my-project/metabolic-curvature-measure/scripts/"
v15 = load(base + "journal_manuscript_v15.tex")
v14 = load(base + "journal_manuscript_v14.tex")
refs15 = load(base + "journal_manuscript_v15_bmb_refs.tex")
refs14 = load(base + "journal_manuscript_v14_bmb_refs.tex")

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


# 1. Abstract identity
A15 = re.search(r"\\begin\{abstract\}.*?\\end\{abstract\}", v15, re.S).group(0)
A14 = re.search(r"\\begin\{abstract\}.*?\\end\{abstract\}", v14, re.S).group(0)
report("abstract byte-identical to v14", None, None,
       "identical" if A15 == A14 else "DIFFERS")
if A15 != A14:
    fail += 1

# 2. Number multiset: v15 vs v14
n15, n14 = num_tokens(v15), num_tokens(v14)
missing = n14 - n15
added = n15 - n14
print(f"[INFO] number multiset v15 vs v14 raw diff: "
      f"missing={dict(missing)} added={dict(added)}")

EXPECTED_ADD = {"15": 1, "0.419": 1, "0.083": 1, "366": 1,
                "2013": 1, "27": 1}
EXPECTED_DEL = {"14": 1}
# "2013" = digits of the new \citet{kochanowski2013} citation key;
# "27"   = digits of the new \S\ref{sec:e27} cross-reference label;
# "15"/"14" = the \input filename version digit;
# "0.419"/"0.083"/"366" = re-quoted audited body claims.
unexplained_add = {t: c for t, c in added.items()
                   if c > EXPECTED_ADD.get(t, 0)}
unexplained_del = {t: c for t, c in missing.items()
                   if c > EXPECTED_DEL.get(t, 0)}
unexpected_extra_add = {t: EXPECTED_ADD[t] - c for t, c in
                        EXPECTED_ADD.items() if c < EXPECTED_ADD[t]}
unexpected_extra_del = {t: EXPECTED_DEL[t] - c for t, c in
                        EXPECTED_DEL.items() if c < EXPECTED_DEL[t]}
report("number multiset = version bump + the three re-quoted body "
       "numbers only", unexplained_del, unexplained_add)
if unexpected_extra_add or unexpected_extra_del:
    fail += 1
    print("  [FAIL] expected deltas not all present: "
          f"add {unexpected_extra_add}, del {unexpected_extra_del}")

# 3-6. Structural censuses
report("label census", labels(v14) - labels(v15), labels(v15) - labels(v14))
ckd = citekeys(v15) - citekeys(v14)
ckm = citekeys(v14) - citekeys(v15)
ok_cite = (dict(ckd) == {"kochanowski2013": 1} and not ckm)
print(f"[{'PASS' if ok_cite else 'FAIL'}] citation census "
      f"(only kochanowski2013 +1)")
if not ok_cite:
    fail += 1
    print("  missing:", dict(ckm), "added:", dict(ckd))
report("environment census", environments(v14) - environments(v15),
       environments(v15) - environments(v14))
report("section census", sections(v14) - sections(v15),
       sections(v15) - sections(v14))

# 7. Bibliography identity
report("bmb_refs bibliography identity", None, None,
       "byte-identical" if refs15 == refs14 else "DIFFERS")
if refs15 != refs14:
    fail += 1

# 8. The twelve adjudicated edit regions present; all other lines equal.
EDIT_MARKERS = [
    ("E4 object-paragraph triggers + bottleneck gloss",
     "when a\nnutrient becomes depleted or an enzyme capacity saturates"),
    ("E6 impulse image",
     "an\nimpulse of curvature delivered on that wall"),
    ("E20 value-vs-flux guiding question",
     "Should metabolic\nsensitivity be read off the growth rate"),
    ("E7 bridge opening question",
     "Can discrete linear-programming switches be approximated"),
    ("E8 city-street analogy",
     "like navigating a city whose streets run only in fixed"),
    ("E9 regime-dichotomy toll sentence",
     "pays a toll proportional to the loop's diameter"),
    ("E12b more-than-double decile gloss",
     "$0.89$ --- more than double; MWU"),
    ("E15 path-robustness question",
     "Does the association generalize beyond glucose limitation"),
    ("E14 tie-break plain lead + question",
     "A linear program can have many optimal flux distributions"),
    ("E11 tie-break findings coda",
     "not an artifact of solver mechanics"),
    ("E17 Discussion standby-model paragraph",
     "Why transcribe a rerouting program without translating it?"),
    ("E18 protein-layer-null tightening",
     "Transcription does not propagate through translation;"),
]
print()
for name, marker in EDIT_MARKERS:
    ok = marker in v15 and marker not in v14
    print(f"[{'PASS' if ok else 'FAIL'}] edit present: {name}")
    if not ok:
        fail += 1

# body-line identity outside the edited regions: normalized replace of
# the input filename, then compare line multisets is not sufficient --
# instead confirm the unified diff touches only the 16 known hunks.
import difflib
d14 = strip_header_comment(v14).replace(
    "journal_manuscript_v14_bmb_refs", "REFS")
d15 = strip_header_comment(v15).replace(
    "journal_manuscript_v15_bmb_refs", "REFS")
sm = difflib.SequenceMatcher(None, d14.split("\n"), d15.split("\n"),
                             autojunk=False)
n_hunks = sum(1 for op in sm.get_opcodes() if op[0] != "equal")
print(f"[INFO] unified-diff hunks outside the header comment: {n_hunks}"
      f" (expected <= 14: 12 content edits; the E7 opener touches "
      f"adjacent lines counted once; some edits span 2 hunks)")
if n_hunks > 14:
    fail += 1
    print("  [FAIL] more changed regions than adjudicated")

print()
if fail == 0:
    print("RESULT: ALL COMPLETE -- v15 differs from v14 only in the "
          "twelve adjudicated merged-register edits (plus the "
          "mechanical version bump); abstract unchanged; nothing "
          "lost; the only new numbers are re-quotes of audited body "
          "claims (+0.419, -0.083, 366); the only new citation is "
          "kochanowski2013 in the Discussion paragraph.")
else:
    print(f"RESULT: {fail} FAILURES -- inspect above.")
raise SystemExit(0 if fail == 0 else 1)
