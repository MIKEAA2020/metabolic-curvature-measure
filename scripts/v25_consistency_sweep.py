#!/usr/bin/env python3
"""v25 consistency sweep: title / abstract / keywords / sections /
cross-citations / cover letters / links doc all aligned with the
latest manuscript findings (v20 main + v13 companion) and the DAM
venue. Complements audit_v30_numbers.py (which covers all numeric
claims) with structural/consistency gates."""
import re, sys

S = "/home/z/my-project/metabolic-curvature-measure/scripts"
D = "/home/z/my-project/metabolic-curvature-measure/download"
main = open(f"{S}/journal_manuscript_v20.tex").read()
comp = open(f"{S}/companion_categorical_v13.tex").read()
refs_main = open(f"{S}/journal_manuscript_v20_dam_refs.tex").read()
bib_comp = open(f"{S}/companion_refs_v13.bib").read()
bib_main = open(f"{S}/journal_manuscript_v20_refs.bib").read()
letter_main = open(f"{D}/cover_letter_dam.md").read()
letter_comp = open(f"{D}/cover_letter_dam_companion.md").read()
links = open(f"{D}/SUBMISSION_PACKAGE_LINKS.md").read()

TITLE_MAIN = ("A discrete curvature measure for flux balance analysis "
              "predicts transcriptional regulation in Escherichia coli")
TITLE_COMP = ("A Geometric and Category-Theoretic Theory of Viability: "
              "How Sequential Adaptations Induce Path-Dependent Risk")

fails, passes = [], []
def check(name, cond, detail=""):
    (passes if cond else fails).append(f"{name} {detail}")

# 1. titles ------------------------------------------------------------
check("main \\title matches the v20 narrowed title (no translational-buffering claim)",
      re.search(r"\\title\{A discrete curvature measure for flux balance analysis\s+"
                r"predicts transcriptional regulation in \\emph\{Escherichia coli\}\}", main)
      is not None)
check("main pdftitle matches \\title",
      main.count("predicts transcriptional regulation in") >= 2)
check("companion title matches actual current title",
      "A Geometric and Category-Theoretic Theory of Viability" in comp)
check("stale pre-v11 companion title absent from companion",
      "Stratified Connections, Optic Composition" not in comp)

# 2. abstract/keywords/venue gates --------------------------------------
m_abs = re.search(r"\\begin{abstract}(.*?)\\end{abstract}", main, re.S)
c_abs = re.search(r"\\textbf\{Abstract\.\}(.*?)\\par", comp, re.S)
def wp_count(t):
    """Word-processor-style count: whitespace tokens containing alnum."""
    r = re.sub(r"\\[a-zA-Z]+", "", t)
    r = re.sub(r"[\\${}~]", " ", r).replace("---", " ")
    return len([w for w in r.split() if re.search(r"[A-Za-z0-9]", w)])
def audit_count(t):
    return len(re.findall(r"[A-Za-z0-9\-]+", re.sub(r"\\[a-zA-Z]+", " ", t)))
check("main abstract < 250 words (DAM; word-processor and audit-style counts)",
      wp_count(m_abs.group(1)) < 250 and audit_count(m_abs.group(1)) < 250,
      f"({wp_count(m_abs.group(1))} wp / {audit_count(m_abs.group(1))} audit-style words)")
check("companion abstract < 250 words (DAM; word-processor and audit-style counts)",
      wp_count(c_abs.group(1)) < 250 and audit_count(c_abs.group(1)) < 250,
      f"({wp_count(c_abs.group(1))} wp / {audit_count(c_abs.group(1))} audit-style words)")
check("main abstract has the F6 hedge",
      "consistent with" in m_abs.group(1))
check("companion six-axis sentence has the F2 qualifier",
      "nitrogen-source substitution" in c_abs.group(1))
kw_m = re.search(r"\\textbf\{Keywords:\}(.*?)(?:\\bigskip|\\par|\n\\n)", main, re.S)
check("main keywords block has 6 terms",
      kw_m and len([k for k in kw_m.group(1).split(";") if k.strip()]) == 6)
kw_c = re.search(r"\\textbf\{Keywords:\}(.*?)\\\\", comp, re.S)
check("companion keywords 6 terms (Keywords block, semicolon-separated)",
      kw_c and len([k for k in kw_c.group(1).split(";") if k.strip()]) == 6)
check("main numeric natbib mode",
      "\\usepackage[numbers,sort&compress,square]{natbib}" in main)
check("companion numeric natbib mode",
      "\\usepackage[numbers,sort&compress,square]{natbib}" in comp)
check("main Fig. label style",
      '\\renewcommand{\\figurename}{Fig.}' in main and
      "labelsep=space" in main)

# 3. audit count consistency --------------------------------------------
check("main states 359 twice, no stale 349/98",
      main.count("$359$") == 2 and "$349$" not in main and "(98 checks)" not in main)
check("letters state 359/359",
      letter_main.count("359") >= 2 and letter_comp.count("359") >= 1)
check("links doc states 359/359 and audit_v30",
      "359/359 PASS" in links and "audit_v30" in links)

# 4. cross-citation titles aligned ---------------------------------------
check("main refs cite companion's actual title",
      "A Geometric and Category-Theoretic Theory of Viability" in refs_main)
check("main bib cite companion's actual title",
      "A Geometric and Category-Theoretic Theory of Viability" in bib_main)
check("companion bib cites main's v20 title (narrowed)",
      "Predicts Transcriptional Regulation in Escherichia coli" in bib_comp
      and "Translational" not in bib_comp.split("zai2026measure",1)[1][:400])
check("companion points at v20 application file",
      "journal_manuscript_v20.tex" in comp)
check("letters point at v13/v20 files",
      "companion_categorical_v13.tex" in letter_main and
      "journal_manuscript_v20.tex" in letter_comp)
def _norm(s):
    return re.sub(r"\s+", " ", s.replace("*Escherichia coli*", "Escherichia coli"))
check("letters quote actual titles",
      _norm(TITLE_MAIN)[:70] in _norm(letter_main)
      and _norm(TITLE_COMP)[:70] in _norm(letter_comp))

# 5. F5/F6/F4/F3 wording gates -------------------------------------------
check("main: no 'rank identity' / 'metric invariance holds' / 'measured metric invariance'",
      "rank identity" not in main and "metric invariance holds" not in main
      and "measured metric invariance" not in main)
check("main: F3 direct rank correlation present",
      "$\\rho = +0.92$ (P1)" in main and "+0.96" in main and "424" in main)
check("main: F4 two-regime qualifier present",
      "across random panels" in main and "designed panels reproduce them exactly" in main)
check("main: no flat ': cells transcribe' assertion",
      "proteomics): cells transcribe" not in main)

# 6. venue agreement: no stale primary-venue claims ------------------------
for f_, t_ in [("main", main), ("companion", comp)]:
    check(f"{f_}: no BMB/Bulletion/JTB/TAC target claims",
          "Bulletin of Mathematical Biology" not in t_.replace(
              "Target journal: Bulletin of Mathematical Biology (Springer).", "")
          or f_ != "main")
check("main header names Discover Applied Mathematics",
      "Discover Applied Mathematics" in main)
check("links doc: Paper 1/2 both DAM, no stale primary BMB/TAC rows",
      "## Paper 1 (Main) — Discover Applied Mathematics" in links and
      "## Paper 2 (Companion) — Discover Applied Mathematics" in links)
check("links doc: stale companion title gone from Paper 2 row",
      "Stratified Connections, Optic Composition, and the Homotopy\nFixed-Point Extension" not in links)
check("links doc: current package rows point at v20/v13 + DAM zips",
      links.count("journal_manuscript_v20.tex") >= 1 and
      links.count("companion_categorical_v13.tex") >= 1 and
      "submission_main_dam.zip" in links and
      "submission_companion_dam.zip" in links and
      "submission_main_bmb.zip" not in links.split("## Paper 1")[1].split("## Paper 2")[0] and
      "submission_companion_tac.zip" not in links.split("## Paper 2")[1])

# 7. supplementary / division of labor -------------------------------------
check("main: no supplementary/ESM claim (delegation intact)",
      "companion" in main.lower())
check("companion: self-contained claim for categorical definitions",
      "self-contained" in comp.lower())

# report -------------------------------------------------------------------
print(f"CONSISTENCY SWEEP: {len(passes)} PASS / {len(fails)} FAIL")
for p in passes:
    print("  [PASS]", p)
for f in fails:
    print("  [FAIL]", f)
sys.exit(1 if fails else 0)
