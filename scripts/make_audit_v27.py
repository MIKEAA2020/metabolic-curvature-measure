#!/usr/bin/env python3
"""Create audit_v27_numbers.py from audit_v26_numbers.py.

Retargets the numeric audit to journal_manuscript_v19.tex (v19
comprehension restructure after the JTB desk rejection; BMB target):
manuscript + refs file names, the BMB gates (abstract 150-250
audit-style words per the live-verified Springer/BMB guideline;
keywords 4-6 terms; refs pointer journal_manuscript_v19_bmb_refs),
the V18-FM2 keyword gate recapped from JTB 7-term to BMB 6-term (the
'path dependence' term dropped), the V18-FM3 JTB-highlights gate
replaced by the V19 structural-restructure gates, and two new V19
front-matter checks (Methods counts mapping, title change). Output
ledger: v27_number_audit.{json,md}.
"""

src = open("scripts/audit_v26_numbers.py").read()

# ---- 1. header ---------------------------------------------------------
old = """Numeric consistency audit of journal_manuscript_v18.tex +
(v18 JTB-alignment round: target venue Journal of Theoretical
Biology --- abstract trimmed 254 -> 249 audit-style words under
JTB's 250-word cap, keywords 6 -> 7 with 'path dependence', the
CRediT authorship contribution statement, venue-neutral refs file
journal_manuscript_v18_refs.tex, and the required separate
highlights file download/highlights_jtb.docx; every v17 number
unchanged, so all 344 v25 checks carry over with only the
front-matter gates retargeted, plus three new V18 checks;
extends the v25 audit of) journal_manuscript_v17.tex +"""
new = """Numeric consistency audit of journal_manuscript_v19.tex +
(v19 comprehension restructure, BMB target, after the JTB desk
rejection: new plain title, bio-first abstract (243 audit-style
words, every audited number kept), keywords 6 terms, the intro
five-finding list replaced by three question-led paragraphs, the
categorical-reading subsection removed, the refinement-resolution
bridge moved to the appendix, the counts-disambiguation appendix
folded into Methods, refs carried to
journal_manuscript_v19_bmb_refs.tex; every v18 number unchanged,
so all 347 v26 checks carry over with the front-matter gates
retargeted/recapped, plus two new V19 checks;
extends the v26 audit of) journal_manuscript_v18.tex +"""
assert src.count(old) == 1
src = src.replace(old, new)

# ---- 2. main manuscript file ------------------------------------------
old = '"journal_manuscript_v18.tex")).read()'
assert src.count(old) == 1
src = src.replace(old, '"journal_manuscript_v19.tex")).read()')

# ---- 3. JP-2 gate: refs pointer name ----------------------------------
old = '''      "tableofcontents" not in tex2 and
      "journal_manuscript_v18_refs" in tex2 and
      "Author Summary" not in tex2)'''
new = '''      "tableofcontents" not in tex2 and
      "journal_manuscript_v19_bmb_refs" in tex2 and
      "Author Summary" not in tex2)'''
assert src.count(old) == 1
src = src.replace(old, new)

# ---- 4. JP-3 gate: BMB caps -------------------------------------------
old = '''check("JP-3", "JTB retarget: abstract <= 250 words (live JTB Guide "
      "for Authors); no Author Summary; keywords line with <= 7 "
      "terms (JTB range 1-7)", "v3 front matter",
      f"abstract {abs_words}w, keywords {kw_terms}",
      abs_words <= 250 and "Author Summary" not in tex2 and
      "Keywords:" in tex2 and kw_terms <= 7)'''
new = '''check("JP-3", "BMB retarget: abstract 150-250 words (Springer/BMB "
      "guideline, live-verified); no Author Summary; keywords line "
      "with 4-6 terms (BMB range)", "v3 front matter",
      f"abstract {abs_words}w, keywords {kw_terms}",
      150 <= abs_words <= 250 and "Author Summary" not in tex2 and
      "Keywords:" in tex2 and 4 <= kw_terms <= 6)'''
assert src.count(old) == 1
src = src.replace(old, new)

# ---- 5. refs file open in the JP-5 area -------------------------------
old = '''bmb_refs = open(os.path.join(BASE, "scripts",
                 "journal_manuscript_v18_refs.tex")).read()'''
new = '''bmb_refs = open(os.path.join(BASE, "scripts",
                 "journal_manuscript_v19_bmb_refs.tex")).read()'''
assert src.count(old) == 1
src = src.replace(old, new)

# ---- 6. V17-FM1 gate: file label --------------------------------------
old = '''check("V17-FM1", "abstract <= 250 audit-style words (JTB cap; "
      "v18 trims it to 249) with the bio-anchoring sentences "
      "(regulons, fork metabolites, post-translational memory)",
      "journal_manuscript_v18.tex abstract", f"{nwords17} words",'''
new = '''check("V17-FM1", "abstract <= 250 audit-style words (BMB cap; "
      "v19 rebuilds it at 243) with the bio-anchoring sentences "
      "(regulons, fork metabolites, post-translational memory)",
      "journal_manuscript_v19.tex abstract", f"{nwords17} words",'''
assert src.count(old) == 1
src = src.replace(old, new)

# ---- 7. V17-FM2 refs file open ----------------------------------------
old = '''refs17 = open(os.path.join(BASE, "scripts",
              "journal_manuscript_v18_refs.tex")).read()'''
new = '''refs17 = open(os.path.join(BASE, "scripts",
              "journal_manuscript_v19_bmb_refs.tex")).read()'''
assert src.count(old) == 1
src = src.replace(old, new)

# ---- 8. V18-FM1 label recap (CRediT kept, venue-neutral wording) ------
old = '''check("V18-FM1", "CRediT authorship contribution statement in the "
      "taxonomy form required by JTB (single author, roles listed)",
      "journal_manuscript_v18.tex backmatter", "CRediT roles",
      credit_ok)'''
new = '''check("V18-FM1", "CRediT authorship contribution statement "
      "(retained from the JTB round; Springer accepts author-"
      "contribution statements in any consistent form; single "
      "author, roles listed)",
      "journal_manuscript_v19.tex backmatter", "CRediT roles",
      credit_ok)'''
assert src.count(old) == 1
src = src.replace(old, new)

# ---- 9. V18-FM2 keyword gate: JTB 7 -> BMB 6 --------------------------
old = '''kw_line18 = re.search(r"Keywords:\\}\\s*([^\\n]*(?:\\n[^\\n\\\\]*){0,3})",
                      tex2)
kw_terms18 = kw_line18.group(1).count(";") + 1 if kw_line18 else 99
check("V18-FM2", "keywords: 7 terms (JTB 1-7) with the new term "
      "'path dependence' indexing the path-dependence findings",
      "journal_manuscript_v18.tex keywords", f"{kw_terms18} terms",
      kw_terms18 == 7 and "path dependence" in kw_line18.group(1))'''
new = '''kw_line18 = re.search(r"Keywords:\\}\\s*([^\\n]*(?:\\n[^\\n\\\\]*){0,3})",
                      tex2)
kw_terms18 = kw_line18.group(1).count(";") + 1 if kw_line18 else 99
check("V18-FM2", "keywords: 6 terms (BMB 4-6); 'path dependence' "
      "(the JTB-only 7th term) dropped in the BMB retarget",
      "journal_manuscript_v19.tex keywords", f"{kw_terms18} terms",
      kw_terms18 == 6 and
      "path dependence" not in kw_line18.group(1))'''
assert src.count(old) == 1
src = src.replace(old, new)

# ---- 10. V18-FM3 highlights gate -> V19 structural gates --------------
old = '''import zipfile as _zipf
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
      "highlights" in os.path.basename(_hz))'''
new = '''# --- V19 structural-restructure gates (comprehension round) ---
# (the JTB-specific highlights gate is retired with the JTB target;
# download/highlights_jtb.docx remains in the repo as JTB-path
# history but is not part of the BMB package)
_v19_gates = {
    "categorical subsection absent from body":
        "The categorical reading, in brief" not in tex2 and
        "ref{sec:categorical}" not in tex2,
    "value-flux dichotomy subsection carries the retained corollary":
        "\\\\subsection{Value events and flux events}" in tex2 and
        tex2.count("cor:valueflux") >= 4,
    "bridge in appendix (after \\\\appendix, before Proofs)":
        tex2.index("\\\\appendix") < tex2.index(
            "\\\\section{The refinement--resolution bridge}") <
        tex2.index("\\\\section{Proofs}"),
    "counts-disambiguation appendix folded into Methods":
        "Disambiguation of near-colliding counts" not in tex2 and
        "ref{sec:counts}" not in tex2 and
        "$435$ genes with at" in tex2 and
        "own artifact file (Data Availability)." in tex2,
    "companion citation still resolves once":
        tex2.count("zai2026categorical") >= 1,
}
check("V19-FM3", "structural restructure: categorical subsection out, "
      "corollary retained in body, bridge in appendix, counts folded "
      "into Methods, companion pointer intact",
      "journal_manuscript_v19.tex structure", "5 sub-gates",
      all(_v19_gates.values()))

check("V19-FM4", "new plain title replaces the two-clause 'Geometric "
      "Theory' title; old title absent; pdftitle aligned",
      "journal_manuscript_v19.tex front matter", "title gates",
      "A discrete curvature measure for flux balance analysis" in tex2
      and "Geometric Theory of Metabolic Flux Rerouting" not in tex2
      and "predicts transcriptional regulation and translational" in
      tex2)

check("V19-FM5", "intro claim structure rebuilt: five-finding "
      "enumeration gone, three question-led paragraphs present",
      "journal_manuscript_v19.tex intro (vs the v18 claim list)",
      "intro gates",
      "What this paper establishes." in tex2 and
      "five interconnected findings" not in tex2 and
      "does the geometry predict regulation?" in tex2)'''
assert src.count(old) == 1
src = src.replace(old, new)

# ---- 11. output ledger names -------------------------------------------
src = src.replace(
    'DB, "v26_number_audit.json"', 'DB, "v27_number_audit.json"')
src = src.replace('DB, "v26_number_audit.md"', 'DB, "v27_number_audit.md"')
src = src.replace(
    'md = ["# v12 numeric consistency audit (symmetric iJO second-engine + tie-break promotion round; v26 retarget of the v25 ledger to journal_manuscript_v18.tex + JTB gates)", "",',
    'md = ["# v12 numeric consistency audit (symmetric iJO second-engine + tie-break promotion round; v27 retarget of the v26 ledger to journal_manuscript_v19.tex + BMB gates + V19 restructure gates)", "",')

# ---- 12. V17-FM2 artifact label (cosmetic: file name) ------------------
old = '''check("V17-FM2", "refs: 29 entries with kacser1973 + heinrich1974 "
      "added; both cited in the body",
      "journal_manuscript_v18_refs.tex", f"{n17} entries",'''
new = '''check("V17-FM2", "refs: 29 entries with kacser1973 + heinrich1974 "
      "added; both cited in the body",
      "journal_manuscript_v19_bmb_refs.tex", f"{n17} entries",'''
assert src.count(old) == 1
src = src.replace(old, new)

open("scripts/audit_v27_numbers.py", "w").write(src)
print("audit_v27_numbers.py written")
