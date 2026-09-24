#!/usr/bin/env python3
"""Build audit_v30_numbers.py from audit_v29_numbers.py (the v29 file is
never modified) for the V20/V13 Discover Applied Mathematics round:

1. Functional retargets: journal_manuscript_v19_bmb_refs ->
   journal_manuscript_v20_dam_refs; journal_manuscript_v19 ->
   journal_manuscript_v20; companion_categorical_v12 ->
   companion_categorical_v13 (reads and labels).
2. Venue-gate updates: companion abstract caps 265 -> 250 (DAM 'less
   than 250'); JP-3 main abstract 150-249; JP-2 natbib gate round ->
   numbers,sort&compress,square (DAM numeric citations); V17-FM1 cap
   label; V19-FM4 title gate -> the narrowed v20 title.
3. New V20-family checks: F3 (direct rank correlation vs
   v20_path_rank_stability.json), F4 (random-panels qualifier), F5
   (rank agreement / five-decimal agreement wording), F6 (hedges +
   narrowed title), F2 (nitrogen-source substitution qualifier), DAM
   formatting gates (numeric citations both files, Fig. labels,
   companion keywords 6), cross-citation title alignments, and the
   audit-count self-consistency check (the manuscript's stated suite
   size equals the v30 ledger size).
4. Outputs: v30_number_audit.json / v30_number_audit.md.
"""
import os

S = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(S, "audit_v29_numbers.py")
DST = os.path.join(S, "audit_v30_numbers.py")

t = open(SRC).read()
n_repl = 0


def rep(old, new, label, count=1):
    global t, n_repl
    found = t.count(old)
    assert found == count, f"{label}: expected {count}, found {found}"
    t = t.replace(old, new)
    n_repl += 1


# --- docstring head ---
rep(
    'Numeric consistency audit of journal_manuscript_v19.tex +\n'
    'companion_categorical_v12.tex (V12 companion comprehension round:',
    'Numeric consistency audit of journal_manuscript_v20.tex +\n'
    'companion_categorical_v13.tex (V20/V13 Discover Applied Mathematics\n'
    'round: the causal-coherence/prose-alignment review findings F2-F6\n'
    'applied as a light touch-up -- F3 the direct trajectory rank\n'
    'correlation (rho = +0.92 P1 / +0.96 P2) reported and artifact-checked,\n'
    'F4 the random-panels qualifier, F5 five-decimal agreement wording,\n'
    'F6 hedged buffering + narrowed title, F2 the nitrogen-source-\n'
    'substitution qualifier; DAM venue gates: abstract < 250 words both\n'
    'papers, numeric square-bracket citations, Fig. labels, companion\n'
    'keywords 6 terms, cross-citation titles aligned. Extends the v29\n'
    'audit of the V12 companion comprehension round:',
    "docstring head")

# --- functional retargets (refs first, then the plain names) ---
rep("journal_manuscript_v19_bmb_refs", "journal_manuscript_v20_dam_refs",
    "refs filename retarget", 5)
rep("journal_manuscript_v19", "journal_manuscript_v20",
    "main filename retarget", 8)
rep("companion_categorical_v12", "companion_categorical_v13",
    "companion filename retarget", 19)

# --- JP-2: DAM numeric-citation gate ---
rep(
    'check("JP-2", "BMB retarget: author-year citations (natbib round); no "\n'
    '      "table of contents; generated BMB reference list input; no "\n'
    '      "Author Summary (PLOS-era block removed)",\n'
    '      "v3 preamble/backmatter", "all present",\n'
    '      "[round]{natbib}" in tex2 and',
    'check("JP-2", "DAM retarget: numeric square-bracket citations "\n'
    '      "(natbib numbers mode); no table of contents; generated "\n'
    '      "reference list input; no Author Summary (PLOS-era block "\n'
    '      "removed)",\n'
    '      "v3 preamble/backmatter", "all present",\n'
    '      "[numbers,sort&compress,square]{natbib}" in tex2 and',
    "JP-2 natbib gate")

# --- JP-3: DAM abstract cap ---
rep(
    'check("JP-3", "BMB retarget: abstract 150-250 words (Springer/BMB "\n'
    '      "guideline, live-verified); no Author Summary; keywords line "\n'
    '      "with 4-6 terms (BMB range)", "v3 front matter",\n'
    '      f"abstract {abs_words}w, keywords {kw_terms}",\n'
    '      150 <= abs_words <= 250 and "Author Summary" not in tex2 and',
    'check("JP-3", "DAM retarget: abstract 150-249 words (Discover "\n'
    '      "Applied Mathematics: \'an abstract of less than 250 words\', "\n'
    '      "live-verified); no Author Summary; keywords line with 4-6 "\n'
    '      "terms (Springer range)", "v3 front matter",\n'
    '      f"abstract {abs_words}w, keywords {kw_terms}",\n'
    '      150 <= abs_words <= 249 and "Author Summary" not in tex2 and',
    "JP-3 DAM cap")

# --- companion abstract caps 265 -> 250 (three gates) ---
rep('check("O2-15", "prop:keio-o2-limited + rem:keio-o2-invariance in companion; "\n'
    '      "abstract promotes the probe and stays under 265 words",',
    'check("O2-15", "prop:keio-o2-limited + rem:keio-o2-invariance in companion; "\n'
    '      "abstract promotes the probe and stays under 250 words (DAM cap)",',
    "O2-15 label")
rep('and _nwords < 265) else "FAIL")', 'and _nwords < 250) else "FAIL")',
    "O2-15 condition")
rep('f"O2-15: abstract promotion present, word count {_nwords} < 265")',
    'f"O2-15: abstract promotion present, word count {_nwords} < 250")',
    "O2-15 print")
rep('check("R8-ABS-wordcount",\n'
    '      "abstract under the 265-word cap",',
    'check("R8-ABS-wordcount",\n'
    '      "abstract under the 250-word Discover Applied Mathematics cap",',
    "R8-ABS label")
rep('      nwords < 265)', '      nwords < 250)', "R8-ABS condition")
rep('check("S-14", "six-axis abstract word count < 265",',
    'check("S-14", "six-axis abstract word count < 250 (DAM cap)",',
    "S-14 label")
rep('      _nwS < 265)', '      _nwS < 250)', "S-14 condition")

# --- V17-FM1: cap label + condition (main abstract, now 245) ---
rep('check("V17-FM1", "abstract <= 250 audit-style words (BMB cap; "\n'
    '      "v19 rebuilds it at 243) with the bio-anchoring sentences "\n'
    '      "(regulons, fork metabolites, post-translational memory)",',
    'check("V17-FM1", "abstract <= 249 audit-style words (DAM cap; "\n'
    '      "v20 carries it at 245) with the bio-anchoring sentences "\n'
    '      "(regulons, fork metabolites, post-translational memory)",',
    "V17-FM1 label")
rep('      nwords17 <= 250 and "regulons" in m_abs17.group(1) and',
    '      nwords17 <= 249 and "regulons" in m_abs17.group(1) and',
    "V17-FM1 condition")

# --- V19-FM4: title gate -> narrowed v20 title ---
rep(
    'check("V19-FM4", "new plain title replaces the two-clause \'Geometric "\n'
    '      "Theory\' title; old title absent; pdftitle aligned",\n'
    '      "journal_manuscript_v20.tex front matter", "title gates",\n'
    '      "A discrete curvature measure for flux balance analysis" in tex2\n'
    '      and "Geometric Theory of Metabolic Flux Rerouting" not in tex2\n'
    '      and "predicts transcriptional regulation and translational" in\n'
    '      tex2)',
    'check("V19-FM4", "plain title retained; v20 narrows it to the measured "\n'
    '      "claim (\'predicts transcriptional regulation\' alone -- the "\n'
    '      "translational-buffering mechanism stays hedged and "\n'
    '      "keyword-indexed); old titles absent; pdftitle aligned",\n'
    '      "journal_manuscript_v20.tex front matter", "title gates",\n'
    '      "A discrete curvature measure for flux balance analysis" in tex2\n'
    '      and "Geometric Theory of Metabolic Flux Rerouting" not in tex2\n'
    '      and "predicts transcriptional regulation in" in tex2\n'
    '      and "regulation and translational" not in tex2)',
    "V19-FM4 title gate")

# --- outputs ---
rep('with open(os.path.join(DB, "v29_number_audit.json"), "w") as f:',
    'with open(os.path.join(DB, "v30_number_audit.json"), "w") as f:',
    "json output")
rep('with open(os.path.join(DB, "v29_number_audit.md"), "w") as f:',
    'with open(os.path.join(DB, "v30_number_audit.md"), "w") as f:',
    "md output")
rep('md = ["# v12 numeric consistency audit (symmetric iJO second-engine + '
    'tie-break promotion round; v27 retarget of the v26 ledger to '
    'journal_manuscript_v20.tex + BMB gates + V19 restructure gates)", "",',
    'md = ["# V20/V13 numeric consistency audit (Discover Applied '
    'Mathematics round: F2-F6 light touch-up + venue gates; v29 ledger '
    'retargeted to journal_manuscript_v20.tex + companion_categorical_v13'
    '.tex)", "",',
    "md header")
rep('out = {"experiment": "v12 numeric consistency audit (symmetric iJo "\n'
    '                     "second-engine + deterministic tie-break promotion round; extends v11)",',
    'out = {"experiment": "V20/V13 numeric consistency audit (Discover "\n'
    '                     "Applied Mathematics round; extends the v29 audit)",',
    "out experiment string")

# --- V20-family checks, inserted before the out-dict write ---
NEW_BLOCK = '''
# =====================================================================
# V30 section. V20/V13 round gates: review findings F2-F6 + DAM venue
# =====================================================================
f3rs = json.load(open(os.path.join(
    DB, "v20_path_rank_stability.json")))
c_f3_1 = f3rs["comparisons"]["P0_vs_P1"]
c_f3_2 = f3rs["comparisons"]["P0_vs_P2"]
check("V20-1", "F3: direct trajectory rank correlation reported "
      "(rho = +0.92 P1 / +0.96 P2 over 424 shared nonzero genes) and "
      "matches the computed artifact",
      "v20_path_rank_stability.json + journal_manuscript_v20.tex",
      "artifact %.4f / %.4f (n %d)" % (
          c_f3_1["spearman_both_nonzero"],
          c_f3_2["spearman_both_nonzero"],
          c_f3_1["n_both_nonzero"]),
      close(c_f3_1["spearman_both_nonzero"], 0.92, 0.005) and
      close(c_f3_2["spearman_both_nonzero"], 0.96, 0.005) and
      c_f3_1["n_both_nonzero"] == 424 and
      "$\\\\rho = +0.92$ (P1) and $+0.96$" in tex2 and
      "$424$ genes nonzero on both paths" in tex2,
      "F3: the previously indirect 'largely trajectory-independent' "
      "inference is now backed by the direct statistic computed from "
      "the deposited v7 path CSVs (both-nonzero panel)")

check("V20-2", "F4: intro Glivenko--Cantelli sentence carries the "
      "two-regime qualifier",
      "journal_manuscript_v20.tex intro",
      "qualifier present: %s" % ("across random panels" in tex2),
      "Glivenko--Cantelli rate across random panels" in tex2 and
      "(designed panels reproduce them exactly)" in tex2)

check("V20-3", "F5: 'rank identity' -> 'rank agreement'; 'metric "
      "invariance holds' -> 'agree to five decimals' (rho = 0.99998 "
      "is near-identity, not identity)",
      "journal_manuscript_v20.tex",
      "old forms absent: %s" % ("rank identity" not in tex2),
      "rank agreement" in tex2 and "rank identity" not in tex2 and
      "agree to five decimals" in tex2 and
      "metric invariance holds" not in tex2)

m_abs_v20 = re.search(r"\\\\begin{abstract}(.*?)\\\\end{abstract}",
                      tex2, re.S)
check("V20-4", "F6: translation-buffering mechanism hedged at both "
      "remaining flat sites (abstract + intro 'consistent with'); no "
      "flat ': cells transcribe' assertion outside the body's hedged "
      "'consistent with a model in which' framing",
      "journal_manuscript_v20.tex abstract + intro",
      "abstract hedge: %s" % ("consistent with" in m_abs_v20.group(1)),
      "consistent with" in m_abs_v20.group(1) and
      "proteomics): cells transcribe" not in tex2 and
      "consistent with cells transcribing" in tex2)

check("V20-5", "DAM formatting: numeric square-bracket citations in "
      "both manuscripts; Fig.-label captions in the main",
      "journal_manuscript_v20.tex + companion_categorical_v13.tex",
      "natbib/caption gates",
      "[numbers,sort&compress,square]{natbib}" in tex2 and
      "[numbers,sort&compress,square]{natbib}" in companion and
      "labelsep=space" in tex2 and
      "\\\\renewcommand{\\\\figurename}{Fig.}" in tex2)

check("V20-6", "F2: companion six-axis sentence covers all three "
      "body categories -- the nitrogen-source substitution qualifier "
      "added",
      "companion_categorical_v13.tex abstract",
      "qualifier present: %s" % ("nitrogen-source substitution" in companion),
      "regime switches and" in companion and
      "nitrogen-source substitution" in companion)

_kw13_seg = companion[companion.find("\\\\textbf{Keywords:}"):
                      companion.find("AMS 2020")]
_kw13_terms = _kw13_seg.count(";") + 1 if _kw13_seg else 99
check("V20-7", "companion keywords: 6 terms (Springer 4-6 range); "
      "2-category / information geometry / autopoiesis dropped from "
      "the 9-term TAC-era list; AMS MSC retained",
      "companion_categorical_v13.tex keywords", f"{_kw13_terms} terms",
      _kw13_terms == 6 and "autopoiesis" not in _kw13_seg and
      "AMS 2020 Subject Classification" in companion)

refs_v20 = open(os.path.join(BASE, "scripts",
                 "journal_manuscript_v20_dam_refs.tex")).read()
bib_v13 = open(os.path.join(BASE, "scripts",
                "companion_refs_v13.bib")).read()
check("V20-8", "cross-citation titles aligned: the main cites the "
      "companion's actual title; the companion cites the main's v20 "
      "title",
      "journal_manuscript_v20_dam_refs.tex + companion_refs_v13.bib",
      "both aligned",
      "A Geometric and Category-Theoretic Theory of Viability: How" in
      refs_v20 and
      "Sequential Adaptations Induce Path-Dependent Risk." in refs_v20
      and
      "Predicts Transcriptional Regulation in Escherichia coli" in bib_v13
      and "Measure-Theoretic Discrete Curvature Framework" not in bib_v13)

_expected_total = len(checks) + 2  # V20-9 (self) + V20-10 (refs count)
check("V20-9", "Reproducibility text: the stated audit-suite size "
      "equals the v30 ledger size (no stale check count)",
      "journal_manuscript_v20.tex Reproducibility + this audit",
      f"stated == ${_expected_total}$",
      f"${_expected_total}$ numeric checks" in tex2)

check("V20-10", "v20 refs list: 29 entries preserved (kacser1973 + "
      "heinrich1974 still present; only the cross-citation title "
      "changed)",
      "journal_manuscript_v20_dam_refs.tex", "entry census",
      len(re.findall(r"\\\\bibitem", refs_v20)) == 29 and
      "kacser1973" in refs_v20 and "heinrich1974" in refs_v20)

'''
rep('out = {"experiment": "V20/V13 numeric consistency audit (Discover "\n'
    '                     "Applied Mathematics round; extends the v29 audit)",',
    NEW_BLOCK + 'out = {"experiment": "V20/V13 numeric consistency audit (Discover "\n'
    '                     "Applied Mathematics round; extends the v29 audit)",',
    "V20 checks block inserted")

with open(DST, "w") as f:
    f.write(t)

print(f"audit_v30_numbers.py written ({n_repl} transformations + "
      "V20 checks block).")
print("NOTE: V20-9 self-consistency gate expects the manuscript to "
      "state the final ledger size; run once, then patch the "
      "Reproducibility count in journal_manuscript_v20.tex.")
