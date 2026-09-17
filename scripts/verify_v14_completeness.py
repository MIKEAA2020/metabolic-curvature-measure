#!/usr/bin/env python3
"""Abstract-cap-round completeness verification (v14 vs v13).

Checks that the main manuscript (journal_manuscript_v14.tex) differs
from journal_manuscript_v13.tex ONLY in the abstract (plus the
mechanical version bump: header filenames, the new header note, and
the \\input filename), with nothing lost:
  1. Body identity outside the abstract environment and the header
     comment block (byte-identical after removing those regions and
     normalizing the \\input filename).
  2. Numeric-token multiset diff: the ONLY expected delta is the
     version digit in the \\input filename (13 -> 14). The abstract
     trim keeps every number, so the abstract-swap numeric deltas
     must both be EMPTY (this round is stricter than the v13 check,
     which allowed the two re-quoted body numbers).
  3. Label census       (\\label{...} multisets identical)
  4. Citation census    (\\cite keys identical)
  5. Environment census (theorem/definition/... counts identical)
  6. Section census     (\\section/\\subsection counts identical)
  7. Bibliography identity (v14 vs v13 bmb_refs, byte-identical)
"""
import re
from collections import Counter


def num_tokens(s):
    s = re.sub(r"(?<!\\)%.*", "", s)
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


def strip_abstract(s):
    m = re.search(r"\\begin\{abstract\}.*?\\end\{abstract\}", s, re.S)
    return s[:m.start()] + s[m.end():]


def strip_header_comment(s):
    m = re.search(r"^%.*?\\documentclass", s, re.S | re.M)
    return s[m.end() - len("\\documentclass"):] if m else s


def load(p):
    return open(p).read()


base = "/home/z/my-project/metabolic-curvature-measure/scripts/"
v14 = load(base + "journal_manuscript_v14.tex")
v13 = load(base + "journal_manuscript_v13.tex")
refs14 = load(base + "journal_manuscript_v14_bmb_refs.tex")
refs13 = load(base + "journal_manuscript_v13_bmb_refs.tex")

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


# 1. Body identity outside abstract + header + input filename
body14 = strip_abstract(strip_header_comment(v14)).replace(
    "journal_manuscript_v14_bmb_refs", "REFS")
body13 = strip_abstract(strip_header_comment(v13)).replace(
    "journal_manuscript_v13_bmb_refs", "REFS")
report("body identity outside abstract/header/input", None, None,
       "byte-identical" if body14 == body13 else "DIFFERS")
if body14 != body13:
    fail += 1

# 2. Number multiset: v14 vs v13
n14, n13 = num_tokens(v14), num_tokens(v13)
missing = n13 - n14
added = n14 - n13
print(f"[INFO] number multiset v14 vs v13 raw diff: "
      f"missing={dict(missing)} added={dict(added)}")

# The abstract swap must keep every number: both deltas must be EMPTY
ABSTRACT = re.search(r"\\begin\{abstract\}.*?\\end\{abstract\}",
                     v14, re.S).group(0)
OLD_ABSTRACT = re.search(r"\\begin\{abstract\}.*?\\end\{abstract\}",
                         v13, re.S).group(0)
abs_delta_add = num_tokens(ABSTRACT) - num_tokens(OLD_ABSTRACT)
abs_delta_del = num_tokens(OLD_ABSTRACT) - num_tokens(ABSTRACT)
print("\nAbstract-swap number deltas (both must be empty):")
print("  abstract adds:  ", dict(abs_delta_add))
print("  abstract drops:", dict(abs_delta_del))

unexplained_add = {}
for tok, cnt in added.items():
    if tok == "14" and cnt >= 1:
        continue  # input filename bump
    if abs_delta_add.get(tok, 0) >= cnt:
        continue
    unexplained_add[tok] = cnt - abs_delta_add.get(tok, 0)
unexplained_del = {}
for tok, cnt in missing.items():
    if tok == "13" and cnt >= 1:
        continue  # input filename bump
    if abs_delta_del.get(tok, 0) >= cnt:
        continue
    unexplained_del[tok] = cnt - abs_delta_del.get(tok, 0)
report("number multiset fully explained by version bump only",
       unexplained_del, unexplained_add)
report("abstract kept every number (empty swap deltas)",
       abs_delta_del, abs_delta_add)

# 3-6. Structural censuses
report("label census", labels(v13) - labels(v14), labels(v14) - labels(v13))
report("citation census", citekeys(v13) - citekeys(v14),
       citekeys(v14) - citekeys(v13))
report("environment census", environments(v13) - environments(v14),
       environments(v14) - environments(v13))
report("section census", sections(v13) - sections(v14),
       sections(v14) - sections(v13))

# 7. Bibliography identity
report("bmb_refs bibliography identity", None, None,
       "byte-identical" if refs14 == refs13 else "DIFFERS")
if refs14 != refs13:
    fail += 1

print()
if fail == 0:
    print("RESULT: ALL COMPLETE -- v14 differs from v13 only in the "
          "abstract (plus the mechanical version bump); nothing lost, "
          "every number kept.")
else:
    print(f"RESULT: {fail} FAILURES -- inspect above.")
raise SystemExit(0 if fail == 0 else 1)
