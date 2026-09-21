#!/usr/bin/env python3
"""Create audit_v26_numbers.py from audit_v25_numbers.py.

Retargets the numeric audit to journal_manuscript_v18.tex (JTB
alignment round): manuscript + refs file names, the JTB gates
(abstract <= 250 words per the live JTB Guide for Authors; keywords
<= 7 terms; refs pointer journal_manuscript_v18_refs), the V17-FM
front-matter checks, and three new V18 checks (CRediT statement,
7-term keyword list, the required Highlights file with 3-5 bullets
of <= 85 characters). Output ledger: v26_number_audit.{json,md}.
"""

src = open("scripts/audit_v25_numbers.py").read()

# ---- 1. header -------------------------------------------------------
old = """Numeric consistency audit of journal_manuscript_v17.tex +"""
new = """Numeric consistency audit of journal_manuscript_v18.tex +
(v18 JTB-alignment round: target venue Journal of Theoretical
Biology --- abstract trimmed 254 -> 249 audit-style words under
JTB's 250-word cap, keywords 6 -> 7 with 'path dependence', the
CRediT authorship contribution statement, venue-neutral refs file
journal_manuscript_v18_refs.tex, and the required separate
highlights file download/highlights_jtb.docx; every v17 number
unchanged, so all 344 v25 checks carry over with only the
front-matter gates retargeted, plus three new V18 checks;
extends the v25 audit of) journal_manuscript_v17.tex +"""
assert src.count(old) == 1
src = src.replace(old, new)

# ---- 2. main manuscript file ----------------------------------------
old = '"journal_manuscript_v17.tex")).read()'
assert src.count(old) == 1
src = src.replace(old, '"journal_manuscript_v18.tex")).read()')

# ---- 3. JP-3 gate: JTB caps ------------------------------------------
old = '''      "tableofcontents" not in tex2 and
      "journal_manuscript_v17_bmb_refs" in tex2 and
      "Author Summary" not in tex2)'''
new = '''      "tableofcontents" not in tex2 and
      "journal_manuscript_v18_refs" in tex2 and
      "Author Summary" not in tex2)'''
assert src.count(old) == 1
src = src.replace(old, new)

old = '''check("JP-3", "BMB retarget: abstract <= 300 words; no Author Summary; "
      "keywords line with <= 6 terms", "v3 front matter",
      f"abstract {abs_words}w, keywords {kw_terms}",
      abs_words <= 300 and "Author Summary" not in tex2 and
      "Keywords:" in tex2 and kw_terms <= 6)'''
new = '''check("JP-3", "JTB retarget: abstract <= 250 words (live JTB Guide "
      "for Authors); no Author Summary; keywords line with <= 7 "
      "terms (JTB range 1-7)", "v3 front matter",
      f"abstract {abs_words}w, keywords {kw_terms}",
      abs_words <= 250 and "Author Summary" not in tex2 and
      "Keywords:" in tex2 and kw_terms <= 7)'''
assert src.count(old) == 1
src = src.replace(old, new)

# ---- 4. refs file open in the JP-4 area -------------------------------
old = '''bmb_refs = open(os.path.join(BASE, "scripts",
                 "journal_manuscript_v17_bmb_refs.tex")).read()'''
new = '''bmb_refs = open(os.path.join(BASE, "scripts",
                 "journal_manuscript_v18_refs.tex")).read()'''
assert src.count(old) == 1
src = src.replace(old, new)

# ---- 5. V17-FM1/FM2 front-matter checks -------------------------------
old = '''check("V17-FM1", "abstract <= 255 audit-style words with the "
      "bio-anchoring sentences (regulons, fork metabolites, "
      "post-translational memory)",
      "journal_manuscript_v17.tex abstract", f"{nwords17} words",
      nwords17 <= 255 and "regulons" in m_abs17.group(1) and'''
new = '''check("V17-FM1", "abstract <= 250 audit-style words (JTB cap; "
      "v18 trims it to 249) with the bio-anchoring sentences "
      "(regulons, fork metabolites, post-translational memory)",
      "journal_manuscript_v18.tex abstract", f"{nwords17} words",
      nwords17 <= 250 and "regulons" in m_abs17.group(1) and'''
assert src.count(old) == 1
src = src.replace(old, new)

old = '''refs17 = open(os.path.join(BASE, "scripts",
              "journal_manuscript_v17_bmb_refs.tex")).read()
n17 = len(re.findall(r"\\\\bibitem", refs17))
check("V17-FM2", "refs: 29 entries with kacser1973 + heinrich1974 "
      "added; both cited in the body",
      "journal_manuscript_v17_bmb_refs.tex", f"{n17} entries",'''
new = '''refs17 = open(os.path.join(BASE, "scripts",
              "journal_manuscript_v18_refs.tex")).read()
n17 = len(re.findall(r"\\\\bibitem", refs17))
check("V17-FM2", "refs: 29 entries with kacser1973 + heinrich1974 "
      "added; both cited in the body",
      "journal_manuscript_v18_refs.tex", f"{n17} entries",'''
assert src.count(old) == 1
src = src.replace(old, new)

# ---- 6. three new V18 checks (after V17-FM2, before `out =`) -----------
old = '''out = {"experiment": "v12 numeric consistency audit (symmetric iJO '''
new = '''# --- V18 JTB alignment gates ---
credit_ok = ("CRediT Authorship Contribution Statement" in tex2 and
             "Conceptualization" in tex2 and "Writing --" in tex2 and
             "Amin Abaee" in tex2)
check("V18-FM1", "CRediT authorship contribution statement in the "
      "taxonomy form required by JTB (single author, roles listed)",
      "journal_manuscript_v18.tex backmatter", "CRediT roles",
      credit_ok)

kw_line18 = re.search(r"Keywords:\\}\\s*([^\\n]*(?:\\n[^\\n\\\\]*){0,3})",
                      tex2)
kw_terms18 = kw_line18.group(1).count(";") + 1 if kw_line18 else 99
check("V18-FM2", "keywords: 7 terms (JTB 1-7) with the new term "
      "'path dependence' indexing the path-dependence findings",
      "journal_manuscript_v18.tex keywords", f"{kw_terms18} terms",
      kw_terms18 == 7 and "path dependence" in kw_line18.group(1))

import zipfile as _zipf
import html as _html
_hz = os.path.join(BASE, "download", "highlights_jtb.docx")
with _zipf.ZipFile(_hz) as _zf:
    _hx = _zf.read("word/document.xml").decode("utf-8")
_paras = re.findall(r"<w:p\\b.*?</w:p>", _hx, re.S)
def _ptext(_p):
    return _html.unescape("".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>",
                                             _p)))
_bul = [_ptext(_p) for _p in _paras]
_bul = [b for b in _bul
        if b and b != "Highlights" and not b.startswith("Manuscript:")]
check("V18-FM3", "highlights file (separate editable .docx, 'highlights' "
      "in the file name): 3-5 bullets, each <= 85 characters incl. "
      "spaces, featuring biological applications + theory",
      "download/highlights_jtb.docx",
      f"{len(_bul)} bullets, lengths {sorted(len(b) for b in _bul)}",
      3 <= len(_bul) <= 5 and all(len(b) <= 85 for b in _bul) and
      "highlights" in os.path.basename(_hz))

out = {"experiment": "v12 numeric consistency audit (symmetric iJo '''
assert src.count(old) == 1
src = src.replace(old, new)

# ---- 7. output ledger names --------------------------------------------
src = src.replace('DB, "v25_number_audit.json"', 'DB, "v26_number_audit.json"')
src = src.replace('DB, "v25_number_audit.md"', 'DB, "v26_number_audit.md"')
src = src.replace(
    'md = ["# v12 numeric consistency audit (symmetric iJO second-engine + tie-break promotion round)", "",',
    'md = ["# v12 numeric consistency audit (symmetric iJO second-engine + tie-break promotion round; v26 retarget of the v25 ledger to journal_manuscript_v18.tex + JTB gates)", "",')

open("scripts/audit_v26_numbers.py", "w").write(src)
print("audit_v26_numbers.py written")
