#!/usr/bin/env python3
"""Abstract-round completeness verification (v13 vs v12).

Checks that the final main manuscript (journal_manuscript_v13.tex)
differs from journal_manuscript_v12.tex ONLY in the abstract (plus the
mechanical version bump), with nothing lost:
  1. Body identity outside the abstract environment and the header
     comment block (byte-identical after removing those regions).
  2. Numeric-token multiset diff, with the expected benign deltas
     whitelisted: the \\input filename version bump and the abstract
     swap itself (the abstract's re-quoted audited body numbers
     r = -0.083 and n = 366, the M3D compendium parenthetical form,
     and dropped tokens from the compressed old abstract).
  3. Label census       (\\label{...} multisets identical)
  4. Citation census    (\\cite keys identical)
  5. Environment census (theorem/definition/... counts identical)
  6. Section census     (\\section/\\subsection counts identical)
  7. Bibliography identity (v13 vs v12 bmb_refs, byte-identical apart
     from nothing -- the file is a versioned copy)
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
v13 = load(base + "journal_manuscript_v13.tex")
v12 = load(base + "journal_manuscript_v12.tex")
refs13 = load(base + "journal_manuscript_v13_bmb_refs.tex")
refs12 = load(base + "journal_manuscript_v12_bmb_refs.tex")

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
body13 = strip_abstract(strip_header_comment(v13)).replace(
    "journal_manuscript_v13_bmb_refs", "REFS")
body12 = strip_abstract(strip_header_comment(v12)).replace(
    "journal_manuscript_v12_bmb_refs", "REFS")
report("body identity outside abstract/header/input", None, None,
       "byte-identical" if body13 == body12 else "DIFFERS")
if body13 != body12:
    fail += 1

# 2. Number multiset: v13 vs v12, whitelist the abstract-swap deltas
n13, n12 = num_tokens(v13), num_tokens(v12)
missing = n12 - n13
added = n13 - n12
# informational raw diff (the adjudicated check below is the gate)
print(f"[INFO] number multiset v13 vs v12 raw diff: "
      f"missing={dict(missing)} added={dict(added)}")

# adjudicate every token in the delta
ABSTRACT = re.search(r"\\begin\{abstract\}.*?\\end\{abstract\}",
                     v13, re.S).group(0)
OLD_ABSTRACT = re.search(r"\\begin\{abstract\}.*?\\end\{abstract\}",
                         v12, re.S).group(0)
new_abs_nums = num_tokens(ABSTRACT)
old_abs_nums = num_tokens(OLD_ABSTRACT)
abs_delta_add = new_abs_nums - old_abs_nums
abs_delta_del = old_abs_nums - new_abs_nums
print("\nAbstract-swap number deltas (must explain the multiset diff):")
print("  abstract adds:  ", dict(abs_delta_add))
print("  abstract drops: ", dict(abs_delta_del))

unexplained_add = {}
for tok, cnt in added.items():
    if tok == "13" and cnt >= 1:
        continue  # input filename bump + header comment mentions
    if abs_delta_add.get(tok, 0) >= cnt:
        continue
    unexplained_add[tok] = cnt - abs_delta_add.get(tok, 0)
unexplained_del = {}
for tok, cnt in missing.items():
    if tok == "12" and cnt >= 1:
        continue  # input filename bump + header comment mentions
    if abs_delta_del.get(tok, 0) >= cnt:
        continue
    unexplained_del[tok] = cnt - abs_delta_del.get(tok, 0)
report("number multiset fully explained by abstract swap + version bump",
       unexplained_del, unexplained_add)

# 3-6. Structural censuses
report("label census", labels(v12) - labels(v13), labels(v13) - labels(v12))
report("citation census", citekeys(v12) - citekeys(v13),
       citekeys(v13) - citekeys(v12))
report("environment census", environments(v12) - environments(v13),
       environments(v13) - environments(v12))
report("section census", sections(v12) - sections(v13),
       sections(v13) - sections(v12))

# 7. Bibliography identity
report("bmb_refs bibliography identity", None, None,
       "byte-identical" if refs13 == refs12 else "DIFFERS")
if refs13 != refs12:
    fail += 1

print()
if fail == 0:
    print("RESULT: ALL COMPLETE -- v13 differs from v12 only in the "
          "abstract (plus the mechanical version bump); nothing lost.")
else:
    print(f"RESULT: {fail} FAILURES -- inspect above.")
raise SystemExit(0 if fail == 0 else 1)
