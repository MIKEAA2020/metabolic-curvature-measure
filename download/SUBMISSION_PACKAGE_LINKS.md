# Submission Package Links — Two-Paper Package

Generated 2026-09-17 (abstract cap round + v17 package round:
journal_manuscript_v14 + companion_categorical_v9). All repository links follow
the repo/blob/main pattern verified live in the 2026-09-03 pass; journal
links verified against the official journal or society pages. Repository
is public, so every link is directly accessible.

Revision note (2026-09-17, abstract cap round + v17 package round): the
author directive to keep the abstract close to Gemini's register while
not exceeding 255 words (the v13 abstract stood at 269 audit-style
words) was executed as an abstract-only trim on NEW versioned files
(prior versions untouched) -- scripts/journal_manuscript_v14.tex (from
v13) plus its refs copies. The register and structure are kept exactly
as rebuilt in the abstract round (two paragraphs; definition -> "We
measure how this map bends" -> evidence -> refinement--resolution
bridge -> "From this measure" -> "Strikingly" -> "Finally" -> "Our
results unify"; in-words glosses for h and L_var). The 15-word trim
removes only Gemini-side redundancy and statistics conventions: the
M1 sweep qualifier after the 93.4-100.0% range (the range itself
already encodes the sweep variability; Gemini's sentence ends there),
"n = 424 evaluated genes" -> "424 genes" (Gemini's own plain form),
"fails in general" -> "fails generically" (Gemini's exact word), the
boundaries gloss compressed to "the boundaries between active
constraint sets", "the measured window" -> "the window", and two
function words tightened. Result: 254 audit-style words (~238
rendered), under the 255 cap. Nothing lost: the body is
byte-identical to v13 outside the abstract (verify_v14_completeness.py:
body identity; number multiset delta = the version digit only, the
abstract swap changed zero numeric tokens; label/citation/environment/
section censuses and the bibliography all identical). Verified:
audit_v22_numbers.py (make_audit_v22.py) 301/301 PASS;
pattern_sweep_v16 16/16 clean on both; tectonic main 30 pp /
companion 75 pp, 0 errors / 0 undefined references; clickable mailto
+ ORCID annotations verified via qpdf; ZIPs rebuilt via
build_submission_zips_v17.sh with fresh-dir standalone compiles
re-verified (30/75 pp); download copies and ZIP contents
byte-identical to scripts; TAC cover letter retargeted to v14.

Revision note (2026-09-17, abstract round + v16 package round): the
author directive that the main-paper abstract was still too
jargon-heavy, highly technical, and inaccessible to a broad
readership, and should adopt Gemini's abstract more faithfully, was
executed as an abstract-only rebuild on NEW versioned files (prior
versions untouched) -- scripts/journal_manuscript_v13.tex (from v12)
plus its refs copies. The abstract now follows Gemini's abstract
(external_audits/humanized/curvature humanized.txt L721-725) in
structure and register: two paragraphs (theory; biology), its
definition -> "We measure how this map bends" -> evidence ->
refinement--resolution bridge -> "From this measure" -> "Strikingly"
-> "Finally" -> "Our results unify" arc, in-words glosses for h and
L_var, full-sentence connectives replacing the compressed
telegraphic clauses, and the plain field-level closer (multi-
parametric linear programming, discrete differential geometry,
transcriptional regulation). The protein-layer dissociation now
carries its measured numbers (r = -0.083 across 366 genes, matched
quantitative proteomics); robustness stays one non-defensive
sentence per the M1 adjudication; every number is an audited body
claim (269 audit-style words; the audit's JP-3 gate is <= 300).
Nothing lost: the body is byte-identical to v12 outside the
abstract (verify_v13_completeness.py: body identity, number
multiset fully explained -- only the two re-quoted body numbers
added -- and label/citation/environment/section censuses plus the
bibliography all identical). Verified: audit_v21_numbers.py
(make_audit_v21.py) 301/301 PASS; pattern_sweep_v16 16/16 clean on
both; tectonic main 30 pp / companion 75 pp, 0 errors / 0 undefined
references; clickable mailto + ORCID annotations verified via qpdf;
VLM render checks of pages 1-2 CLEAN (two-paragraph abstract, no
typographic defects, blue underlined contacts); ZIPs rebuilt via
build_submission_zips_v16.sh with fresh-dir standalone compiles
re-verified (30/75 pp); download copies and ZIP contents
byte-identical to scripts; TAC cover letter retargeted to v13.

Revision note (2026-09-17, brevity round + v15 package round): the
author directive to tighten "We find that it does." and adopt Gemini's
prose throughout with brevity, without sacrificing substance, was
executed as a full sweep of both manuscripts against the Gemini
sources (curvature humanized.txt L718-1704; companion humanized.txt
L1-714). Outcome: MAIN only, as new versioned files (prior versions
untouched) -- scripts/journal_manuscript_v12.tex (from v11) plus its
refs copies: (i) the Positioning paragraph's "We find that it does."
shortened to "It does." with the dependent "We also find that"
connective dropped; (ii) the "at this point" filler removed from the
protein-layer central question. COMPANION: zero edits (already at the
brevity-tight register; the two "present article/operationalization"
sites are legitimate technical or adjudicated provenance usages). No
substance lost: verified by the completeness censuses against the
pre-humanized v10 -- number multiset (content tokens identical; only
the \input filename bump, the ORCID link digits, and the v11-round
audited digit reshuffles), label census, citation-key census,
environment census, section census, and the 27-entry bibitem list all
identical. Verified: audit_v20_numbers.py 301/301 PASS;
pattern_sweep_v16 16/16 clean on both; tectonic main 30 pp /
companion 75 pp, 0 errors / 0 undefined references; ZIPs rebuilt via
build_submission_zips_v15.sh with fresh-dir standalone compiles
re-verified (30/75 pp); download copies and ZIP contents
byte-identical to scripts; TAC cover letter retargeted to v12.

Revision note (2026-09-17, smooth-calculus positioning compression +
perimeter artifact sweep, same versioned files): the "why smooth
calculus cannot describe rerouting" framing introduced with the
accessible-motivation lead was adjudicated and compressed to its
load-bearing, citation-complete form in both papers (edits in place --
a positioning edit, not a new manuscript version). MAIN
journal_manuscript_v10.tex: the intro lead keeps the plain-problem
opening and the FBA/phenotype-phase-plane lineage
(varma1994/orth2010/lewis2010 + edwards2001/ibarra2002) but replaces
the gap-claim framing ("has remained largely unaddressed, and for a
structural reason"), the "smooth calculus cannot describe rerouting"
strawman sentence, and the "natural language" flourish with the
precise statement (classical second derivative vanishes away from
the constraint boundaries and is undefined at them; the second-order
response concentrates at the active-set transitions and is carried
by a measure -- the distributional second derivative, in the
language of geometric measure theory); the "The object" paragraph is
completed with the degeneracy argument (value layer visible to
classical sensitivity via Danskin envelopes, danskin1967; degenerate
reroutings invisible; flux map selection-dependent; deterministic
lexicographic tie-break declared as part of the metric ->
Remark rem:lock). COMPANION companion_categorical_v8.tex: the
smooth-connection breakdown is now stated once, in the introduction
(§1), where it is now cited (aubin2011) at the claim site; the
remark "Why the 2-categorical span is needed" (rem:2cat-span) no
longer re-argues the breakdown (the three-fold-failure enumeration
is absorbed into the cross-reference to §1) and keeps only the
boundary-specification necessity, the resolution, forward pointers,
and the operational requirement; the mathematically precise
hypothesis-failure statement (rem:pdi) is retained unchanged. Swept
the package perimeter: the stale orphaned PLOS Comp Bio cover letter
removed from download/ (it predated the venue decision and still
carried the "rather than any smooth curvature" negation, the
"replacing earlier total-variation claims" changelog phrase, an
unfilled [Submission date], a [Corresponding author name] block, the
pre-rename repository URL, the stale 98-check audit count, and
multi-author phrasing on a sole-author paper; it was referenced by no
package component). Verified: pattern_sweep_v16 16-pattern clean on
both; audit_v18_numbers.py 301/301 PASS; tectonic builds main 29 pp
/ companion 75 pp, zero undefined references; ZIPs rebuilt via
build_submission_zips_v13.sh with fresh-dir standalone compiles
re-verified (29/75 pp).

Revision note (2026-09-17, Gemini-alignment revision + v13 package
round): both papers revised toward the accessible register of the
evaluated Gemini humanization attempts, as new versioned files (prior
versions untouched) -- scripts/journal_manuscript_v10.tex (from v9)
and scripts/companion_categorical_v8.tex (from v7), plus their refs
files. MAIN v10: an accessible-motivation lead paragraph opens the
Introduction (the rerouting question, why smooth calculus cannot
answer it, geometric measure theory as the natural language); a
self-contained parametric-FBA setup with the LP display and the
chamber-complex reading opens Section 2; wall-crossing and
integrated-boundary-impedance glosses in the categorical subsection;
the partial-correlation motivation (baseline-expression confound) at
the primary association; the protein-layer central question and a
buffering close at the abundance/change dissociation; discussion
sentences for the resolution-window breakdown and the
objective-invisibility of most rerouting; Limitations restructured as
a labeled list with every item kept. COMPANION v8: a narrative
harm-in-sequence abstract opening (264 words, under the 265 cap; the
six-axis sentence intact); the concrete closed-cycle example
(temperature/nutrients) in the Introduction; the intuitive gloss at
the viability-weighted-curvature definition; an in-words gloss at the
optic-category definition; the stabilization question at the head of
the Lipschitz section; the application-bridge numbers (r = +0.395,
n = 424; r = -0.083, n = 366) in the Introduction; a compact
Conclusion section before Future directions. The Gemini attempts'
defects remain rejected (fabricated "Zai, A." author, changelog
remnants, ASCII art, adverbial register, proof-argument swaps, and the
companion attempt's content loss). All numerical claims unchanged:
audit_v18_numbers.py 301/301 PASS; builds: main 29 pp, companion
75 pp, zero errors / zero undefined references; ZIPs rebuilt via
build_submission_zips_v13.sh with fresh-dir standalone tectonic
compiles verified (29/75 pp); cover letters retargeted to the new
filenames.

Revision note (2026-09-17, universal Gemini-register revision + v14
package round): both papers carry the evaluated Gemini register
universally across their narrative prose, as new versioned files
(prior versions untouched) -- scripts/journal_manuscript_v11.tex
(from v10) and scripts/companion_categorical_v9.tex (from v8), plus
their refs files. The email (mailto:) and ORCID
(https://orcid.org/0000-0002-0019-1842) are now CLICKABLE in both
papers (main: author footnote; companion: title block; verified as
URI annotations in both built PDFs). MAIN v11: register-level
revision of the narrative prose -- intro lead, section leads and
interstitial prose of Sections 2-4, the computational-validation and
empirical result narratives (M1 sweeps, epistasis, regime dial, value
carrier, primary association with the partial-correlation motivation,
panel construction, platform 2x2, protein abundance/change and the
protein-layer null with the buffering close), discussion, methods
connectives, and the positioning paragraph recast in Gemini's
short-sentence form; every number, proof, citation, and the
compressed smooth-calculus statement unchanged. COMPANION v9:
abstract connective polish (word count kept under the 265 cap),
Preliminaries / SAVGS / Empirical-Verdicts section leads, the
four-point Conclusion opener, and the clickable author block; the
bibliography pointer retargeted to companion_refs_v9.bib. Verified:
number-integrity multiset diff (zero missing/added numeric tokens
beyond the ORCID link digits); pattern_sweep_v16 16/16 clean on
both; audit_v19_numbers.py 301/301 PASS; tectonic main 30 pp /
companion 75 pp, 0 errors / 0 undefined references; ZIPs rebuilt via
build_submission_zips_v14.sh with fresh-dir standalone compiles
re-verified (30/75 pp); cover letters retargeted to v11/v9.

Revision note (2026-09-17, Gemini-alignment revision + v13 package
round): both papers revised toward the accessible register of the
evaluated Gemini humanization attempts, as new versioned files (prior
versions untouched) -- scripts/journal_manuscript_v10.tex (from v9)
and scripts/companion_categorical_v8.tex (from v7), plus their refs
files. MAIN v10: an accessible-motivation lead paragraph opens the
Introduction (the rerouting question, why smooth calculus cannot
answer it, geometric measure theory as the natural language); a
self-contained parametric-FBA setup with the LP display and the
chamber-complex reading opens Section 2; wall-crossing and
integrated-boundary-impedance glosses in the categorical subsection;
the partial-correlation motivation (baseline-expression confound) at
the primary association; the protein-layer central question and a
buffering close at the abundance/change dissociation; discussion
sentences for the resolution-window breakdown and the
objective-invisibility of most rerouting; Limitations restructured as
a labeled list with every item kept. COMPANION v8: a narrative
harm-in-sequence abstract opening (264 words, under the 265 cap; the
six-axis sentence intact); the concrete closed-cycle example
(temperature/nutrients) in the Introduction; the intuitive gloss at
the viability-weighted-curvature definition; an in-words gloss at the
optic-category definition; the stabilization question at the head of
the Lipschitz section; the application-bridge numbers (r = +0.395,
n = 424; r = -0.083, n = 366) in the Introduction; a compact
Conclusion section before Future directions. The Gemini attempts'
defects remain rejected (fabricated "Zai, A." author, changelog
remnants, ASCII art, adverbial register, proof-argument swaps, and the
companion attempt's content loss). All numerical claims unchanged:
audit_v18_numbers.py 301/301 PASS; builds: main 29 pp, companion
75 pp, zero errors / zero undefined references; ZIPs rebuilt via
build_submission_zips_v13.sh with fresh-dir standalone tectonic
compiles verified (29/75 pp); cover letters retargeted to the new
filenames.

Revision note (2026-09-17, post-synthesis flow polish + v12 package
round): new main version as a separate file, prior versions untouched
-- scripts/journal_manuscript_v9.tex (from v8); companion_categorical_v7.tex
stands unchanged. The round closed the five post-synthesis directives:
(1) flow -- the abstract's subject repetition smoothed ("The association
does not propagate" -> "It does not propagate"; 249 words, within the
150-250 guideline) and the Reproducibility sentence recast as "An
automated suite of 301 numeric checks re-derives every manuscript
number..."; (2) remnant/redundancy -- the 16-pattern forbidden-list
sweep clean on both papers, rendered-PDF scans clean (duplicate
sentences, placeholders, punctuation artifacts: all extraction
false-positives, verified in context); (3) error check -- the
humanizing-turn diffs re-audited line by line, every grafted number
re-verified against the body and artifacts; (4) content-loss scan
against the pre-humanized baselines (v6 main / v5 companion) -- no
substantive loss found: every item removed from the abstracts is fully
reported in the introduction/body (rho = 0.99998, five selection rules,
Glivenko-Cantelli rate, boundary-reset true-order, codimension-one
strata, thirteen sweeps, all Limitations items), and the standing
rejections from the humanized-file evaluation remain correct; (5) the
cover letters finalized: dates filled (September 17, 2026) and the TAC
board-member choice made -- Prof. Christina Vasilakopoulou (NTUA),
Transmitting Editor, cc tac@mta.ca, per TAC's author information
(submit to any Editorial Board member except the Managing Editor or
TeXnical editors). All numerical claims unchanged:
audit_v17_numbers.py 301/301 PASS; builds: main 29 pp, companion
74 pp, zero errors / zero undefined references; ZIPs rebuilt via
build_submission_zips_v12.sh with fresh-dir standalone tectonic
compiles verified (29/74 pp).

Revision note (2026-09-17, merged-synthesis revision + v11 package
round): new manuscript versions as separate files, prior versions
untouched -- scripts/journal_manuscript_v8.tex (main, BMB; from v7)
and scripts/companion_categorical_v7.tex (companion, TAC; from v6).
The revision implements the merged synthesis plan built from the
evaluated external humanization attempts (plan at
download/Humanized_Versions_Evaluation_and_Synthesis_Plan.md):
main -- the abstract's robustness clauses compressed to one sentence
with the numbers kept in the body (238 words, within the 150-250
guideline; hook, primary numbers, punchline placement, and specific
closer unchanged; the n=424 parenthetical disambiguated to "424
evaluated genes"); a growth-rate gloss at the value function's first
appearance; a zero-cost-substitution gloss inside the coupling
theorem; a Discussion sentence tying the transcription--value-layer
dissociation to the coupling structure; the Reproducibility
check-count reconciled (98 -> 301); two process-flavored remark
titles recast factually. Companion -- the boundary-rule
three-fold-failure breakdown in the 2-categorical-span remark; the
thermostat/cell contrast making the autopoiesis--homeostasis
distinction concrete; a physical reading of the Zeno
self-measurement schedule; two proof-provenance phrasings recast.
All numerical claims unchanged: audit_v16_numbers.py 301/301 PASS;
builds: main 29 pp, companion 74 pp, zero errors / zero undefined
references; ZIPs rebuilt via build_submission_zips_v11.sh with
fresh-dir standalone tectonic compiles verified (29/74 pp); cover
letters retargeted to the new version filenames.

Revision note (2026-09-16, reader-oriented prose revision + v10
package round): new manuscript versions as separate files, prior
versions untouched -- scripts/journal_manuscript_v7.tex (main, BMB;
from v6) and scripts/companion_categorical_v6.tex (companion, TAC;
from v5). The revision is a style pass informed by a landmark-paper
study (Orth/Edwards-Palsson/Segre/Lewis/Baba/Mahadevan on the
metabolic side; Shannon, Baez-Stay, Baez-Fong, Leinster on the
formal side; digest at research/landmark_style_digest.md). Main: the
abstract now opens from the plain problem (piecewise-linear, not
smooth; all numbers kept, 248 words, within the 150-250 guideline);
the introduction's "object" paragraph glosses active set and strata
in words and a plan-of-the-paper paragraph is added; plain-language
openers precede the core definitions and follow the key displayed
equations; the Limitations paragraph is restructured from one
sentence into readable items; the "safe regime" remark is retitled.
Companion: the abstract opens from the plain problem (264 words,
under the 265-word cap, with the six-axis sentence and required
phrases intact); the introduction glosses policy/connection/holonomy
and optics at first use; one-sentence leads are added to the
Preliminaries, Noether, hierarchy, composition, and
filtered-colimit sections. All numerical claims unchanged:
audit_v15_numbers.py 301/301 PASS; builds: main 28 pp, companion
75 pp, zero undefined references; ZIPs rebuilt via
build_submission_zips_v10.sh with fresh-dir standalone tectonic
compiles verified (28/75 pp); cover letters retargeted (also: the
BMB letter's stale 98-check audit count corrected to 301, its
"rather than any smooth curvature" phrasing and
"replacing earlier total-variation claims" changelog phrasing made
factual, and the stale section 3.5 pointer corrected to 2.5).

Revision note (2026-09-16, formal-style completion + cross-citation
authorship + v9 package round): new manuscript versions as separate
files, prior versions untouched -- scripts/journal_manuscript_v6.tex
(main, BMB; from v5) and scripts/companion_categorical_v5.tex
(companion, TAC; from v4). (1) Main: the abstract now states the
discrete-carrier finding factually (the self-referential "not a smooth
curvature" negation removed; 240 words, within the Springer 150-250
guideline); remaining process vocabulary purged ("precursor" ->
"geometric" at all eight sites including the Fig 3 caption; the
Discussion's undefined kappa_flux/kappa_time phantom objects replaced
by the framework's own resolution objects; "is now a theorem" ->
"is a theorem"; "the recalibrated predictor" sentence recast); the
author-contribution sentence matches the author's declared wording.
(2) Companion: "earlier drafts" references (two sites), the uncited
"prior formulations"/"prior work" strawman framing (two sites), the
"fluctation" typo, "named by the novelty assessment" (two sites),
"whose retirement ... records", "Homogenized" (two sites), "deepest
degeneracy yet recorded", "now"-tense sites (four), the "Rigorous"
subsection title, "The decisive prediction", the duplicated
designed-progression passage, and the "same conflation" remark (now
aligned with the main paper's rewritten Discussion) all fixed; the
label rem:fba-kappa-superseded renamed rem:operational-curvature.
(3) Cross-citation authorship: the "X" placeholder author in the
zai2026categorical and zai2026measure entries replaced by Abaee in
journal_manuscript_v6_bmb_refs.tex, journal_manuscript_v6_refs.bib,
and the companion's new companion_refs_v5.bib (the previous package
had shipped the X-author bib). (4) Fig 3 regenerated with "geometric"
labels (scripts/fig3_v6_regen.py; values unchanged and re-verified).
(5) audit_v14_numbers.py: 301/301 PASS against the new files; builds:
main 27 pp, companion 74 pp, zero undefined references; ZIPs rebuilt
via build_submission_zips_v9.sh with fresh-dir standalone tectonic
compiles verified (27/74 pp); cover letters retargeted; all file
rows below retargeted to the current versions.

Revision note (2026-09-16, formal-tone revision + figure repair + v8
package round): (1) New manuscript versions as separate files, prior
versions untouched: scripts/journal_manuscript_v5.tex (main, BMB;
from v4) and scripts/companion_categorical_v4.tex (companion, TAC;
from v3); both compiled tectonic-clean (main 27 pp; companion 74 pp;
zero undefined references) with the v5/v4 PDF copies refreshed in
download/. (2) Formal-journal-tone revision of both manuscripts per
the author's directive: declarations rewritten as brief single
sentences (Funding: none; competing interests: none; AI declaration:
GLM (Z.ai) and DeepSeek AI assisted with development and
documentation of analysis code, all AI-assisted content reviewed,
verified, and edited by the author, who takes responsibility for the
final content; ethics approval: not applicable; author
contributions: A.A. conceived the study design, developed the
methodology and analysis code, performed the data analysis, and
drafted and revised the manuscript); meta-commentary and
self-referential prose removed (main: the categorical-subsection
self-description, division-of-labor editorializing, "locked"
internal jargon -> "declared"/"fixed", "after the discovery of" ->
"resolving", a duplicated sentence fragment in the active-set bridge
paragraph repaired; companion: the Status note below the abstract,
"Medium audit" remark retitled "Medium construction and the
wild-type optima" with correction-history phrasing removed,
"iron/phosphate round" and audit-diary phrasing rewritten as
scientific observation, "the external novelty assessment explicitly
asked for" removed, "honestly reported" removed, the "X is the sole
author" placeholder replaced by A.A.); proofs left at full length.
(3) Figure repair: Fig 3 (primary association) panel (b) bar
annotations no longer collide with the panel title (explicit y-axis
headroom); the same fix applied to the path-robustness figure panel
(b2) and to a clipped annotation in the event-measure-stabilization
figure panel (d); all six main-paper figures regenerated without
internal experiment codes (V5/E22/E24/V7/V6/V8/E32/M4b/M1/AX-8c/9/10
labels replaced by manuscript terminology); regeneration was
artifact-driven or a deterministic re-run with all data artifacts
byte-identical (e32 differs only in the wall-clock runtime_s field).
(4) Audits re-run on the new versions: audit_v5_numbers.py 98/98
PASS (main) and audit_v13_numbers.py 301/301 PASS (companion);
cover letters' cross-referenced filenames updated; submission ZIPs
rebuilt via build_submission_zips_v8.sh with fresh-dir standalone
compiles verified (main BMB 27 pp; companion TAC 74 pp).

Revision note (2026-09-16, author-finalization +
journal-guideline-compliance + v7 package round): (1) Author identity
finalized in both manuscripts and both cover letters: Amin Abaee,
Independent Researcher, Tehran, Iran; amin_abaee@ut.ac.ir; ORCID
0000-0002-0019-1842 (main paper: \author + \thanks title-page
footnote, Author Contributions, pdfauthor; companion: title block,
pdfauthor; cover letters: signature block and date filled). (2) BMB
guideline compliance for the main paper, re-verified against the
Springer submission guidelines: abstract trimmed to 245 words
(guideline 150-250; was 291 rendered), six keywords re-selected for
discoverability (flux balance analysis; discrete curvature; active
set; parametric linear programming; flux rerouting; epistasis --
flux balance analysis and epistasis added as non-title search
handles; transcriptional response and carbon depletion dropped as
title/abstract-indexed duplicates), and continuous line numbering
enabled (lineno package) per the instructions to authors. (3) TAC
indexing requirements for the companion: visible Keywords line
(optic category; stratified connection; 2-category; filtered
colimit; homotopy type theory; applied category theory) and AMS
2020 Subject Classification (18D05; 18N99; 92B05) added below the
abstract; review-model facts re-verified from the official pages
(BMB single-blind per the SMB society page; TAC non-anonymized --
no anonymized-review option, submission by email to a named
Editorial Board member). (4) Rebuilt and verified: both PDFs
recompiled tectonic-clean (main 28 pp with line numbers; companion
74 pp, zero undefined references), audit_v4 98/98 PASS and
audit_v12 301/301 PASS re-run after the edits, submission ZIPs
rebuilt via build_submission_zips_v7.sh with fresh-dir standalone
compiles verified, and the download PDF copies refreshed.

Revision note (2026-09-16, final proof-read + alignment audit + v6
package round): (1) Final proof-read of the deterministic tie-break
paragraph: every number verified against the deposited artifacts --
keio_atpm_lex_pilot.json (the 105-gene stratified sample = 57 + 48
with anchors b0870/ltaE and b4036/lamB; cross-engine kV 5.98e-11 ->
the paragraph's 6e-11; 40/40 floor collapse in both engines -> the
"80 randomly drawn floor genes"; max |db| 6.4e-8 -> 6e-8; verdict
PROMOTE) and keio_atpm_lex_full_sweep.json (r +0.9534/+0.9686/
+0.9440/+0.9510; AUC 0.9919/0.9920/0.9844/1.0000; labels kappa =
1.000 vs the deposit at all four levels; floor census 6/1/1/0 with
lamB at kV 200.0 at every iML1515 level, the dhaKLM/fsaA/fsaB
block 193.6 -> 298.8 -> 427.2, and the iJO1366 floor-level
parallel-routing block pfkB/fbaB/ydjI at 89.8 and fsaA/fsaB/dhaKLM
at 68.9 -> the paragraph's "kV 69-90"); the rendered paragraph
(Companion pp. 65-66) compiles clean with zero undefined references.
(2) Cross-manuscript alignment audit: the main paper's declared rule
(TB0 in its Section on tie-break robustness: w ~ U(0.5, 1.5), seed
20240901, min w^T v, the three-stage split-variable lexicographic
engine solved with HiGHS) is IDENTICAL to the companion's declared
tie-break convention; the companion's description of the main paper
(five-rule stage-3 battery, declared plus four variants; explicit
protein-layer null) matches the main paper's Section v8 and abstract
exactly; and the companion's patch-J corrections share no numbers
with the main paper (the six-axis Keio battery is companion-internal)
-- the main paper requires no changes and its PDF (28 pp, Sep 14) is
current. (3) One companion-internal alignment gap found and closed:
the abstract's pre-closure phrasing "up to a measured near-degeneracy
boundary" -> "the declared tie-break closing its near-degeneracy
boundary" (net-zero words: 264 < 265; mirrors the body's own
"acquires -- then closes -- its measured boundary" phrasing).
(4) Rebuilt and verified: companion tectonic 0 errors / 0 undefined
(74 pp), audit_v12 re-run 301/301 PASS, submission ZIPs rebuilt via
build_submission_zips_v6.sh with fresh-dir standalone compiles
verified (main BMB 28 pp; companion TAC 74 pp), and the download PDF
copy refreshed.

Revision note (2026-09-16, symmetric iJO second-engine +
deterministic tie-break promotion round): the engine-invariance
audit completed symmetrically and the near-tie boundary closed
constructively. (1) The symmetric iJO1366 re-run
(scripts/atpm_ijo_second_engine.py, keio_atpm_ijo_second_engine.json):
all four ATPM levels re-solved under stateless cold-start
scipy/HiGHS with the probe's exact conventions -- labels fully
engine-invariant (kappa = 1.000 at all four levels, zero flips, max
|db| 1.2e-7, essential counts 298/298/299/331 identical), the
canonical restoration itself engine-invariant (r within 0.002 at
the three deeper levels; +0.9685 -> +0.9496 at the mildest level,
whose massive 961-of-971 kV~200 floor collapses to one gene -- the
mirror of the iML1515 finding, the one genuine floor gene in both
models being lamB, b4036). (2) The deterministic tie-break
promotion, gated by a PRE-REGISTERED merit pilot
(scripts/atpm_lex_tiebreak_pilot.py, keio_atpm_lex_pilot.json,
verdict PROMOTE): the declared three-stage lexicographic rule
(stage 3 = min w^T v over the parsimony-pinned face, fixed seeded
weights U(0.5,1.5)) returns the SAME vertex under the GLPK
warm-start path and stateless HiGHS -- maximum cross-engine vertex
distance 6e-11 on the 105-gene stratified sample + WT at the two
worst levels -- collapses the floor for 40/40 random floor genes in
both engines, and preserves labels (max |db| 6.4e-8). The pilot's
instructive contrast: the stateless two-stage reading keeps lamB at
kV = 200 on iJO1366 while the declared rule returns 0 -- even a
stateless engine's vertex is a path; only a declared rule makes the
statistic well posed. (3) The full declared-rule sweeps at the four
floor-affected levels (scripts/atpm_lex_full_sweep.py,
keio_atpm_lex_full_sweep.json): iML1515 ATPM 60/80/100 read
+0.9534/+0.9686/+0.9440 and iJO1366 ATPM 40 reads +0.9510 (labels
kappa = 1.000 vs the deposit at all four; floors collapse to the
rule-determined rerouting sets: lamB 200.0 at every iML1515 level,
the dhaKLM/fsaA/fsaB block deepening 194 -> 427 with maintenance
demand, the iJO1366 floor level carrying the parallel-routing block
pfkB/fbaB/fsaA/fsaB/dhaKLM/ydjI at kV 69-90). (4) Patch J
(scripts/companion_v3_patch_j.py, 6 anchored edits): the
deterministic-tie-break paragraph in the canonical-selection
subsection (the promotion proper), the prop:keio-atpm engine-bracket
sentence extended with the symmetric iJO confirmation and the
declared-rule readings, rem:canonical-protocol's third requirement
closed constructively, the tab caption and rem:keio-multiaxis
clauses, and the latent feature-count defect fixed ('Four
features matter' -> 'Five features'; five listed since patch H).
audit_v12: 301/301 PASS (v11's 285 + 16 new checks P-15..P-30).
Companion 74 pp, 0 errors / 0 undefined / 0 overfull.

Revision note (2026-09-16, proof-read + second-engine round): final
proof-read of the sixth-axis prop against every deposited artifact.
One numeric defect corrected (the supply-axis PGI at-optimum range
45-202 -> 45-201; max deposited width 201.492, with the previously
unrecorded iML1515 nh4_-2.5 cell certified at 158.316 by
scripts/iml_nh4_pgi_width_check.py); the fifth-feature compensable
count updated to the post-integrity-patch census (782 of 1,127); and
the nitrogen 4-panel figure restored byte-identical after the
sixth-axis probe import re-clobbered it with the legacy module-level
chart (the phosphate-round defect, reintroduced and caught again).
The engine-invariance audit: a full stateless scipy/HiGHS re-run of
the three iML1515 ATPM levels (scripts/atpm_iml_second_engine.py,
keio_atpm_iml_second_engine.json) shows the labels fully
engine-invariant (kappa = 1.000 at all three levels, zero flips,
max |db| 9.1e-8) and the near-tie itself engine-invariant (WT L1
reproduced to 1.1e-5), while the kV~200 floor is the deposited
simplex path's realization: the stateless engine collapses it to the
one genuinely forced knockout (lamB, kV = 200.0) plus a five-gene
dhaKLM/fsaA/fsaB rerouting block (kV 162-416), and restores the
transitive association to +0.952/+0.968/+0.943 -- the measured
engine bracket is [+0.475, +0.943]. The near-tie passages in
prop:keio-atpm, sec 13.6, and rem:canonical-protocol amended
accordingly (patch I); audit_v11: 285/285 PASS. Companion 73 pp,
0 errors / 0 undefined / 0 overfull.

Revision note (2026-09-14): main is now `journal_manuscript_v4.tex`
(28 pp) and the companion is `companion_categorical_v3.tex` (70 pp).
The companion implements the eight-item repair set of the external
audit's synthesized ledger (one optic formalism, corrected
optic-colimit scope, one Hordijk-Steel catalysis condition, gluing
hypothesis alignment, Lévy-area normalization, enlarged contraction
box, battery-table consistency, restricted envelope domination),
restores the six audit-mandated citations (Hirota, Segura, Dittrich,
Handorf, Becker, Bravetti), and adds the external-data closures
(Keio E12/E15/E16; the COT/NE structural benchmark). The main paper
carries the four line-level corrections of its cross-check (bridge
sentence softened, generic-weights uniqueness step, semiconvexity
law, label/title fixes) plus the selection-rule count harmonization;
its figure directory is renamed `association_robustness/` (was
`association_robustness/`).

Revision note (2026-09-14, second perturbation probe round): the
companion adds the oxygen-limited medium probe (the second
perturbation axis, beyond the carbon-source correction): a four-
level dose response on iJO1366 (EX_o2_e at −10/−5/−2.5) plus the
cross-rebuild and non-degenerate anaerobic endpoint on iML1515
(−5 and 0). Labels are invariant at every non-anaerobic level in
both reconstructions (zero flips; κ = 1.000) with the association
degrading only gracefully (held-out AUC ≥ 0.971, 0.9999 at −10);
the anaerobic endpoint re-stratifies 7/1516 labels (lower
glycolysis + hemN gained; fabZ lost), and the iJO1366 anaerobic
zero-growth is disclosed as a model-level degeneracy. The abstract
promotes the medium-robustness finding (262 words).

Revision note (2026-09-14, third perturbation axis round): the
companion adds the nitrogen-source probe (the third medium axis):
an ammonium-limitation gradient (EX_nh4_e at −10/−5/−2.5 on
iJO1366; −2.5 on iML1515) plus full nitrogen-source substitution
(ammonium closed; sole donor L-glutamate at −10 — nitrogen flux
matched to the NH4 −10 level, both optima 0.9259 — or L-arginine
at −10, a four-nitrogen carbon co-substrate with optimum 1.2595,
28% above the glucose-minimal baseline). Labels are invariant along
the entire limitation gradient (289/289 and 286/286; zero flips;
κ = 1.000; WT down 76%); substitution re-stratifies exactly the
assimilation module, losses only (glutamate −5 iJO / −7 iML:
gltA, acnA, acnB, icd, amtB, + gltB/gltD on iML; arginine −14/−15:
those plus the eight arginine-biosynthesis genes and astC), every
rescue substitution-mediated (closing the donor returns all 41
backgrounds to zero growth). The plain-FBA association collapses on
the nitrogen-limited levels — diagnosed by at-optimum FVA
(phosphoglucose-isomerase range 45–177 vs 0.0 at baseline, 4.3
under oxygen limitation) as flux-solution degeneracy, not biology —
and canonical (parsimonious FBA) vertex selection restores it
everywhere (r ≥ +0.872, AUC ≥ 0.979; baseline sharpened
r +0.603 → +0.945). The abstract now carries the three-axis
medium-robustness statement (263 words, under the 265 cap).
audit_v7: 143/143 PASS. Companion 66 → 67 pp, 0 errors /
0 undefined / 0 overfull.

Revision note (2026-09-14, fourth axis + canonical-selection round):
the companion adds the phosphate-limitation probe (the fourth
medium axis, chosen over sulfur by a dose-response pre-screen:
baseline phosphate uptake 0.948/0.793 mmol/gDW/h gives a three-level
gradient spanning 47–89% growth reduction, where sulfur's 0.25
uptake compresses to one informative level). Labels are invariant
at every level in both reconstructions (289/289/289 on iJO1366,
286/286 on iML1515; zero flips; κ = 1.000) — the supply side of
the invariance claim is now closed on all four classical
macronutrient axes (carbon source, electron acceptor, nitrogen,
phosphate). The reported association statistics are homogenized
under canonical (parsimonious) vertex selection across all four
axes (new subsection with an 18-level table): canonical r in
[+0.87, +0.95], held-out AUC ≥ 0.979, labels κ = 1.000 at every
level, the baselines sharpened (iJO r +0.603 → +0.945; iML
+0.875 → +0.937), and the iML1515 anaerobic endpoint restored
across the regime switch itself (r +0.258 → +0.949) — the switch
moves labels only. The homogenization audit surfaced and corrected
eight solver-tolerance artifacts (all trace-quota genes — the
biotin and ubiquinone-side-chain drains scale with growth and fall
to 2–3×10⁻⁷ mmol/gDW/h at low optima, within ~2× of the simplex's
primal feasibility tolerance): the deposited anaerobic fabZ "loss"
(the corrected endpoint is 286 → 292, six gains, no losses; fabZ
is essential in every regime through OGMEACPD/OPMEACPD) and seven
calls at the phosphate −0.1 levels, all re-adjudicated with an
independent LP engine (HiGHS two-stage split-variable pFBA) and
cross-checked to 0 discrepancies in 24,282 gene-level comparisons
across 17 levels. The abstract now carries the four-axis
medium-robustness statement (264 words, under the 265 cap).
audit_v8: 226/226 PASS. Companion 67 → 70 pp, 0 errors /
0 undefined / 0 overfull.

Revision note (2026-09-15, sixth-axis round, merged): the companion
adds the non-medium ATPM-maintenance-stress probe (the
temperature-style surrogate, selected over proton-leak forcing by
pre-screen) with plain + canonical arms in both reconstructions, and
extends the trace-ququota integrity protocol to the new axis: six
corrupted calls at the -90% endpoints (plain fabZ/bioH iJO; plain
bioD/fabZ and canonical bioF/fabI iML) settled at biomass exactly
zero by the independent HiGHS engine and corrected -- the endpoint
re-stratification is purely one-directional (energy-transduction
gains only, atp/cyo/nuo operons, OXPHOS enriched eight-fold) and
the plain-vs-canonical arm agreement is kappa 1.000 at all seven
levels. The canonical-selection subsection gains the measured
near-tie boundary (iML ATPM L1 near-ties, dL1 1.2e-6 relative,
782/1129 compensables at the ~200.01 floor) and the sixth feature;
tab:canonical-selection extended to six axes; the nh4_-5 canonical
level restored (r +0.922). Companion 71 -> 73 pp, 0 errors / 0
undefined / 0 overfull; abstract six-axis, 264 words < 265;
audit_v10 271/271 PASS. New artifacts: keio_atpm_stress_e12/e16,
keio_atpm_pfba_control[_iml]_atpm_*, keio_atpm_stress_summary.txt,
keio_nonmedium_prescreen.json,
keio_atpm_integrity_adjudication.json,
keio_atpm_neartie_measurement.json, keio_floor_tolerance_check.json,
multiaxis_canonical_table.json/.txt,
keio_multiaxis_canonical_response.png (scripts
atpm_stress_keio_probe.py, atpm_integrity_adjudication.py,
atpm_integrity_fix.py, multiaxis_table.py, multiaxis_figure.py,
sixth_axis_artifacts.py; audit_v10_numbers.py).

Revision note (2026-09-15, fifth axis + arginine symmetry round): the
companion adds the iron-limitation probe (the trace-metal fifth
axis, chosen over zinc and manganese by a dose-response pre-screen;
iron pinned to the single ferrous channel, the ferric exchange
closed — the closure leaves the wild-type optimum unchanged to
solver noise): iJO1366 EX_fe2_e at −0.01/−0.005/−0.0025 (37/68/84%
WT reduction) and iML1515 at −0.005/−0.0025 (62/81%). The pre-screen
finds the iron dose response identical on both reconstructions to
six decimals (shared quota; b = fe2/0.0161) — the purest supply
axis of the battery. Labels are invariant at every level (289/289
and 286/286; zero flips; κ = 1.000); the plain-FBA statistics
collapse with the degeneracy signature (PGI FVA width up to 192;
plain r down to −0.037) and canonical vertex selection restores
them everywhere (r +0.800 to +0.957, AUC 0.986–0.988, MCC
0.904–0.965). The arginine-substitution levels re-run under
canonical selection complete the axis × selection table symmetry
(25 levels; iJO +0.802 → +0.953, iML +0.915 → +0.850 with AUC
0.997 / MCC 0.993 — the plain reading was already well posed there,
so the declared rule is reported uniformly rather than
cherry-picked). Integrity: a cross-arm scan of the iron levels
(7,133 gene comparisons, max |Δb| 6×10⁻⁸, no false-viability-band
calls at WT 0.156, just above the 0.14 tolerance boundary); one
GLPK simplex hang (b0887, the cysteine/glutathione ABC-exporter
ATPase) disclosed and settled by the HiGHS engine with the row
marked as an engine substitution; a patch-F rendering defect
(double-escaped \emph / \S\ref commands) caught and fixed.
audit_v9: 251/251 PASS. Companion 70 → 71 pp, 0 errors / 0
undefined / 0 overfull.

- Repository: https://github.com/MIKEAA2020/metabolic-curvature-measure
  (renamed 2026-09-03 from the earlier internal name; GitHub redirects
  the old URLs, but the links below already use the new name)
- Blob links open the GitHub file viewer (PDFs render in-browser; "Download"
  button on the right of each viewer page). Raw links download directly.

---

## Paper 1 (Main) — Bulletin of Mathematical Biology

**Title:** A Measure-Theoretic Discrete Curvature Framework for Metabolic Gene
Sensitivity: From Active-Set Geometry to Transcriptional Response
(Original Research Article; 29 pp; subscription route — no author charges).


### Journal / submission-portal links (all verified)

| Resource | Link |
|---|---|
| Journal home (Springer) | https://link.springer.com/journal/11538 |
| Submission guidelines | https://link.springer.com/journal/11538/submission-guidelines |
| How to publish with us | https://link.springer.com/journal/11538/how-to-publish-with-us |
| Submission portal (Editorial Manager) | https://www.editorialmanager.com/bmab |
| Society page (SMB, official journal of the society) | https://smb.org/Bulletin-of-Mathematical-Biology |

> Review model (verified via the SMB society page): single-blind peer review -- the author identity is known to reviewers, and the name, affiliation, corresponding e-mail, and ORCID are on the title page as the Springer Title Page guideline requires.
>
> Portal code verified as **bmab** (via the SMB society page and multiple
> journal directories). Do not confuse with `editorialmanager.com/jomb`,
> which is the *Journal of Mathematical Biology* — a different Springer journal.

### Package files (GitHub)

| Item | View (blob) | Direct download (raw) |
|---|---|---|
| **One-file upload ZIP (compile-ready)** | — | [download/submission_main_bmb.zip](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/submission_main_bmb.zip) |
| Manuscript PDF (30 pp, full proofs in appendices, declarations in backmatter; universal Gemini-register revision of narrative prose throughout, clickable email and ORCID, brevity round applied, abstract rebuilt on Gemini's abstract and trimmed under the author's 255-word cap; prior versions retained as separate files) | [download/journal_manuscript_v14.pdf](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/journal_manuscript_v14.pdf) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/journal_manuscript_v14.pdf) |
| Cover letter (with declarations, companion disclosure) | [download/cover_letter_bmb.md](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/cover_letter_bmb.md) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/cover_letter_bmb.md) |
| LaTeX source | [scripts/journal_manuscript_v14.tex](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/scripts/journal_manuscript_v14.tex) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/journal_manuscript_v14.tex) |
| Reference list (BMB alphabetical, 27 entries) | [scripts/journal_manuscript_v14_bmb_refs.tex](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/scripts/journal_manuscript_v14_bmb_refs.tex) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/journal_manuscript_v14_bmb_refs.tex) |
| BibTeX database | [scripts/journal_manuscript_v14_refs.bib](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/scripts/journal_manuscript_v14_refs.bib) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/journal_manuscript_v14_refs.bib) |
| Reference-list generator (audit-checked) | [scripts/build_bmb_refs.py](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/scripts/build_bmb_refs.py) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/build_bmb_refs.py) |

Figures (embedded in the PDF; source PNGs if the portal requests separate files):

| Figure | Link |
|---|---|
| Fig. M1 summary (active-set sweep) | [download/m1_m3/fig_m1_summary.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/m1_m3/fig_m1_summary.png) |
| Coupling figures (Alexandrov bridge) | [download/alexandrov_bridge/coupling_figures.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/alexandrov_bridge/coupling_figures.png) |
| Primary association (metric comparison) | [download/association_robustness/v5_e24_recalibration.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/association_robustness/v5_e24_recalibration.png) |
| V7 path robustness | [download/association_robustness/v7_path_robustness.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/association_robustness/v7_path_robustness.png) |
| V8 tie-break robustness (E-V8) | [download/association_robustness/v8_tiebreak_robustness.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/association_robustness/v8_tiebreak_robustness.png) |
| E32 event-measure stabilization | [download/association_robustness/e32_event_measure_stabilization.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/association_robustness/e32_event_measure_stabilization.png) |

Build note: for Overleaf or any standalone compiler, upload **the ZIP** (it
contains the .tex, the input'ed reference list, the .bib database, and all
six figures at the exact relative subpaths the .tex expects — verified to
compile standalone, 30 pp, 0 errors). If instead you upload individual
files, upload them together with `journal_manuscript_v14_bmb_refs.tex` and
the three figure subfolders (`m1_m3/`, `alexandrov_bridge/`,
`association_robustness/`) so the paths resolve; the .tex searches both the
upload directory and the repository layout
(`\graphicspath{{./}{../download/}}`).

---

## Paper 2 (Companion) — Theory and Applications of Categories

**Title:** Stratified Connections, Optic Composition, and the Homotopy
Fixed-Point Extension: A Categorical Framework for Viability-Weighted
Curvature (Research Article; 75 pp current build; electronic-only, free — no author charges).

### Journal / submission links (all verified)

| Resource | Link |
|---|---|
| Journal home | http://www.tac.mta.ca/tac/ |
| Author information (format for submission) | http://www.tac.mta.ca/tac/authinfo.html |
| Editorial board / general info | http://www.tac.mta.ca/tac/geninfo.html |
| Managing Editor contact | tac@mta.ca |
| Chosen Transmitting Editor | Prof. Christina Vasilakopoulou, NTUA — cvasilak@math.ntua.gr |

Submission route (from the official author information, fetched and verified):
submit the article as **a PDF compiled from TeX source to any member of the
Editorial Board except the Managing Editor or TeXnical editors**, copying
every submission to the Managing Editor at **tac@mta.ca**; an article may be
submitted to only one Editor; TeX source plus a compiled PDF are required
only after acceptance. Review model: **not anonymized** -- the
author information page (fetched and verified in full) contains no
anonymization provisions, and submissions go by email to a named
Editorial Board member, so the author identity is on the paper; TAC
also asks that the final accepted source include keywords and an AMS
2020 Subject Classification for external indexing (both now present
below the abstract of the submitted PDF).

### Package files (GitHub)

| Item | View (blob) | Direct download (raw) |
|---|---|---|
| **One-file upload ZIP (compile-ready)** | — | [download/submission_companion_tac.zip](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/submission_companion_tac.zip) |
| Manuscript PDF (75 pp; universal Gemini-register revision of narrative leads and conclusion, clickable email and ORCID; prior versions retained as separate files) | [download/companion_categorical_v9.pdf](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/companion_categorical_v9.pdf) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/companion_categorical_v9.pdf) |
| Cover letter | [download/cover_letter_tac.md](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/cover_letter_tac.md) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/cover_letter_tac.md) |
| LaTeX source | [scripts/companion_categorical_v9.tex](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/scripts/companion_categorical_v9.tex) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/companion_categorical_v9.tex) |
| BibTeX database | [scripts/companion_refs_v9.bib](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/scripts/companion_refs_v9.bib) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/companion_refs_v9.bib) |

Figures (embedded in the PDF; source PNGs):

| Figure | Link |
|---|---|
| Per-optic Lipschitz constants | [download/lipschitz_constants_per_optic.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/lipschitz_constants_per_optic.png) |
| CPTP Zeno contraction | [download/cptc_zeno_contraction.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/cptc_zeno_contraction.png) |
| Inverse-limit RAF Hasse diagram | [download/inverse_limit_raf_hasse.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/inverse_limit_raf_hasse.png) |
| Extended Hasse diagram | [download/inverse_limit_raf_extended_hasse.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/inverse_limit_raf_extended_hasse.png) |
| Claim F holonomy (commuting-control test) | [download/claim_f_holonomy_plot.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/claim_f_holonomy_plot.png) |
| Claims A--E in the n=4 non-abelian regime | [download/claims_ae_n4_nonabelian.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/claims_ae_n4_nonabelian.png) |
| Claim D heavy-tail stress test | [download/claim_d_heavytail_stress.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/claim_d_heavytail_stress.png) |
| Levy 3/2 derivation (exact kernel constant) | [download/levy_stable_3half_derivation.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/levy_stable_3half_derivation.png) |
| Claim G Zeno scaling | [download/claim_g_zeno_plot.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/claim_g_zeno_plot.png) |
| T-iteration convergence | [download/t_iteration_convergence_plot.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/t_iteration_convergence_plot.png) |
| T-iteration robustness (axis-aligned) | [download/t_iteration_robustness_extension_axis_aligned.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/t_iteration_robustness_extension_axis_aligned.png) |
| T-iteration robustness (rotated) | [download/t_iteration_robustness_extension_rotated.png](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/t_iteration_robustness_extension_rotated.png) |

---

## Supporting documentation (GitHub)

| Item | Link |
|---|---|
| Two-paper submission package evaluation | [download/Two_Paper_Submission_Package_Evaluation.md](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/Two_Paper_Submission_Package_Evaluation.md) |
| Declarations & final scan evaluation | [download/Declarations_and_Final_Scan_Evaluation.md](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/Declarations_and_Final_Scan_Evaluation.md) |
| Journal submission pass evaluation | [download/Journal_Submission_Pass_Evaluation.md](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/Journal_Submission_Pass_Evaluation.md) |
| Package-repo browsing: `download/` directory | https://github.com/MIKEAA2020/metabolic-curvature-measure/tree/main/download |
| Package-repo browsing: `scripts/` directory | https://github.com/MIKEAA2020/metabolic-curvature-measure/tree/main/scripts |

---

## Pre-submission checklist (already resolved / remaining)

Resolved: BMB-formatted main paper (natbib author-year, 27 alphabetical
refs, six keywords, v14 two-paragraph abstract in Gemini's register,
trimmed under the author's 255-word cap at 254 audit-style words
(the audit's JP-3 gate remains <= 300) -- continuous line numbering,
brief declarations in backmatter, cover letter
with companion disclosure); self-contained TAC companion (no v21 pointers,
proof statuses labeled, keywords + AMS 2020 MSC, brief declarations, cover
letter); zero cross-paper verbatim prose overlap; author metadata (Amin
Abaee, Independent Researcher, Tehran, Iran; amin_abaee@ut.ac.ir; ORCID
0000-0002-0019-1842) at all authorship sites including the cross-citations;
formal-journal prose with no meta-commentary, changelog, version
references, or strawman constructions in either paper; audit_v22 301/301
PASS against journal_manuscript_v14.tex + companion_categorical_v9.tex;
no-fee venue for both.

Remaining at submission time: register/log in at the BMB Editorial
Manager portal. Resolved this round: the cover-letter dates are filled
(September 17, 2026, both letters) and the TAC receiving board member
is selected -- Prof. Christina Vasilakopoulou (NTUA), Transmitting
Editor, with the submission emailed to her and copied to tac@mta.ca
per TAC's author information (any Editorial Board member except the
Managing Editor or TeXnical editors).

Repository rename COMPLETED (2026-09-03): the repository is now
`metabolic-curvature-measure`; the URL string has been updated in both
manuscripts (Data Availability), both cover letters, and this document.

Formal cleanup executed (2026-09-02): all "Artifact: ... .png/.json"
caption lines removed (source-data linkage now carried by the Data
Availability statement); all internal experiment codes (E-V5, M4b, V8,
Route 5, RC6, BT1, D-N1...), bracketed block tags, changelog/diary
references to predecessor versions, and self-commentary wording removed
from both papers; the Reproducibility and counts-appendix sections were
reworded to formal conventions; the audit passes 98/98 after the edits
(main then 21 pp, companion 35 pp, 0 errors, 0 undefined refs).

Restoration revision executed (2026-09-03), on new frozen-lineage files
(journal_manuscript_v3.tex + journal_manuscript_v3_bmb_refs.tex;
companion_categorical_v3.tex — the v2 main and v1 companion are frozen
and untouched at tag manuscript-v2-final): full proofs for every main-
paper result (two long technical proofs in a second appendix, textbook
material cited); companion restoration of the lost empirical battery —
Claims F/G verdicts, the n=4 non-abelian regime, the Claim D heavy-tail
stress test, the Levy 3/2 derivation REPAIRED to the exact kernel
constant C_fat = sqrt(5 nu)/2 (verified against the frozen Monte-Carlo
data to 1.5%; the figure regenerated with the corrected theoretical
curve), the CPTP-Zeno lift with the Holevo ensemble correction, the
375-configuration contraction battery, the P4-repaired smooth-envelope
chain, the terminal-coalgebra characterization of the maximal RAF
(deflationary closure operator, full proof in the appendix, the
functorial-realization statement demoted to a conjecture), and the
network closure-test battery (A--K summary, RAF-to-Zeno transfer bound,
persistent-homology Phase III test, fixed-model essentiality validation
at kappa = 0.835). Main then 27 pp, companion 57 pp; both compiled with
0 errors and 0 undefined refs; the v3 audit passed 98/98; every
restored number was artifact-traced; ZIPs rebuilt and standalone-
reverified. Remaining script-name mentions in the companion were
formalized to deposited-artifact conventions.

3rd-wave repair round executed (2026-09-14), on new frozen-lineage
files (journal_manuscript_v4.tex; companion_categorical_v3.tex — the
v3 main and v2 companion are frozen and untouched): the companion
implements the external audit's eight-item repair set (one optic
formalism via Riley pairs + a strict feedback representative form;
the optic-colimit theorem restated in corrected scope — Set-level
union, adapter-level (colimit, limit) form, general case open; one
Hordijk-Steel catalysis condition via the food-closure across
definition, operator, and appendix; the gluing hypothesis aligned
with the (O3) gauge transform and the piecewise-F remainder
relabeled O(eps^2); the Levy-area normalization corrected to
Var(X2) = 1/4 with the fluctuation-language restatement of Claims
C/D; the contraction box enlarged to [-1.5, 1.5]^d with K
instantiated; the battery table/AcCoA remark made consistent
(conversions at H and I, not G) and the step-(v) protocol gap
disclosed; the envelope domination restricted to active
surrogates), restores the six audit-mandated citations (Hirota,
Segura, Dittrich, Handorf, Becker, Bravetti; plus Bousfield-Kan),
and adds the external-data closures: the Keio anchor (E12
transitive, E15 direct, E16 cross-rebuild, with the medium-audit
note) and the COT/NE structural benchmark (E14). The main paper
carries the four line-level corrections of the cross-check plus
framing edits, and its figure directory is renamed
association_robustness/. Main now 28 pp, companion 65 pp; both
compile with 0 errors and 0 undefined refs; the v5 audit passes
110/110 (the v4 audit's 98 plus the 12 new Keio-section checks); the RAF enumeration was re-verified under the corrected
catalysis condition (16 RAFs / 21 inclusions / R_max unchanged);
ZIPs rebuilt as the v4 round and standalone-reverified (28 / 65
pp).

Follow-up round (same files, amended in place on the live heads;
frozen lineage untouched): the glucose-only Keio re-run executed
with the trehalose exchange closed as the sole change — both
in-silico essentiality sets unchanged (289/1367 and 286/1516, zero
label changes), every rank-level association strengthened (E12
Pearson 0.370→0.603, held-out AUC 0.953→0.977, MCC 0.719→0.882;
E15 Pearson 0.085→0.230, AUC 0.713→0.737), and the E16
cross-rebuild negative verdict reversed as a medium artifact
(Pearson −0.018→+0.376, AUC 0.428→0.813) — plus the T7b
viability-kernel bridge (closure test as a finite-time,
feedback-certifying probe of kernel/capture-basin membership) and
the T7c Poincare/averaging bridge (occupation fraction as a
phase-invariant orbit statistic); companion 63→65 pp, 0 errors/0
undefined/0 overfull; audit_v5 110/110 PASS; new artifacts
download/keio_glucose_only_e12/e15/e16 (csv/txt/json/png).

Second-probe round (same files, amended in place on the live heads;
frozen lineage untouched): the oxygen-limited medium probe executed
on the electron-acceptor axis (glucose-only medium retained, EX_o2_e
tightened) — iJO1366 dose response at −10/−5/−2.5 with wild-type
optima 0.711/0.491/0.367 (overflow, then fermentation physiology) and
289/1367 essential at every level (zero label changes, κ = 1.000;
calibration r +0.775/+0.607/+0.519, held-out AUC 0.9999/0.980/0.971,
MCC 0.993/0.939/0.887, P@200 = 1.0 at −10); iML1515 at −5 (WT 0.353,
286/1516 unchanged, r +0.559, AUC 0.994, direct AUC 0.818) and at
the anaerobic endpoint 0 (WT 0.134): 286→291 labels (+6/−1: eno,
pgk, gapA, gpmA, gpmM, hemN gained; fabZ lost; κ = 0.985, 5/7 flips
glycolysis-enriched), calibration r +0.260/AUC 0.672, direct
+0.118/AUC 0.673, model gaps unchanged at 13; the iJO1366 anaerobic
zero-growth disclosed as a model-level degeneracy (OPHHX + PDX5POi
lack anaerobic alternatives in that reconstruction; 0.01 mmol/gDW/h
O₂ restores 0.231; iML1515 carries the O₂-free OPHHX3 route);
landed as prop:keio-o2-limited + rem:keio-o2-invariance; abstract
promoted to the medium-robustness statement (262 words < 265);
companion 65→66 pp, 0 errors/0 undefined/0 overfull; audit_v6
125/125 PASS (the v5 audit's 110 plus 15 new O2 checks; two
rounding defects found and fixed: iML −5 AUC 0.995→0.994, WT
reduction 62%→63%); new artifacts download/keio_o2_limited_e12/
e16 (sweep csv + results json), keio_o2_limited_summary.txt,
keio_o2_limited_dose_response.png, keio_o2_anaerobic_diagnostic.json
(scripts o2_limited_keio_probe.py + o2_anaerobic_diagnostic.py).
