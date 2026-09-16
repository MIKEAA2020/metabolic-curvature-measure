# External Humanization Attempts — Evaluation, Verification, and Merged Synthesis Implementation Plan

**Scope.** Evaluation of the three external files in `external_audits/humanized/`:
`qwen abstract.txt` (an assessment of the older main-paper abstract), `curvature humanized.txt`
(three humanization attempts of the main paper), and `companion humanized.txt` (two attempts of
the companion paper). The five attempts were produced by Qwen, Gemini, and Grok:

| File | Attempt | Lines | Coverage |
|---|---|---|---|
| curvature humanized.txt | Qwen | 1–717 | Partial: Sections 1–3 only (through the mpLP conjecture); no validation, empirical, methods, appendices, or references |
| curvature humanized.txt | Gemini | 718–1704 | Complete draft: abstract, Sections 1–7, Appendix A (counts), Appendix B (nine proofs), references |
| curvature humanized.txt | Grok | 1705–2070 | Condensed restructure of the current v7; truncated mid-proof of Proposition 4 |
| companion humanized.txt | Gemini | 1–714 | Accessible survey-level rewrite; heavy content loss |
| companion humanized.txt | Grok | 715–1159 | Condensed restructure of the current v6 through §6.1; truncated mid-Lemma 2 |

**Baselines.** The latest in-repo versions are `download/journal_manuscript_v7.tex` (main, 28 pp)
and `download/companion_categorical_v6.tex` (companion, 75 pp), both landmark-calibrated in the
preceding round, audit_v15 301/301 PASS, zero undefined references.

**Verification method.** Every quantitative claim in each attempt was checked against the current
`.tex` sources and the deposited artifacts by pattern search (33-point numeric battery for the
main paper; structural battery for the companion). Register was assessed against the
landmark-style calibration (`research/landmark_style_digest.md`) and the author's standing
directives (formal journal register; no meta-commentary, changelog tone, previous-version
references, or phantom/naive strawmen; proofs uncondensed; new version files, never overwrites).

---

## Part 1 — The `qwen abstract.txt` assessment

The assessment targets the **older abstract** (the v5/v6-era text that opened with a definition,
carried the defensive parenthetical cluster, and closed with "unifies three distinct sensitivity
objects"). Its six diagnoses are all correct for that text and were verified against it.

**Status in v7 (already adopted).** The current v7 abstract already implements most of the
assessment's recommendations: it opens on the biological situation rather than a definition
("When a cell's environment changes, its metabolic network reroutes..."), it glosses the
technical carrier in words ("concentrated on the boundaries where the network switches between
active constraint sets"), the protein-buffering punchline stands as its own sentence, the
closing sentence is specific ("unifies the atomic measure, its smooth coarse-grainings, and its
trajectory integrals as one object at different resolutions"), and the journal tier is fixed
(Bulletin of Mathematical Biology, 150–250-word guideline; v7 is within cap per audit_v15).

**Still adoptable (into the v8 plan).**
- **A1 — robustness-clause compression.** v7 still carries the inline cluster "invariant under
  the metric's lexicographic definition (ρ = 0.99998), stable across five selection rules, and
  its event measures stabilize at the Glivenko–Cantelli rate." This is the residual of exactly
  the pattern the assessment flags as preemptive rebuttal. Plan: compress to one sentence, e.g.
  "All reported associations are robust to the tie-breaking rule, the reference-level control,
  and panel resampling (Sections 5.5–5.7)." The numbers stay in the body where they are already
  fully reported.
- **A2 — punchline placement audit.** Keep the transcription/translation decoupling sentence
  immediately after the primary association figures, ahead of the epistasis/loop material
  (v7 already does this; the plan locks it as an acceptance criterion).
- **A3 — technical-term budget.** Re-count defined-in-abstract terms; move any that exceed the
  budget to the introduction (v7 is close to compliant; the Glivenko–Cantelli clause is the
  first candidate for relocation under A1).

**Rejected (with reasons).**
- The re-sketch's framing sentences — "the geometry of that rerouting is intrinsically
  singular ... **not a smooth curvature tensor**" and "The singular measure, **not a smooth
  Hessian**, is the geometric object a cell navigates" — are precisely the phantom-negation
  (strawman) construction the author has ruled out. The v7 form ("slope 1.00; a smooth map
  would scale quadratically") states the same contrast as a measured fact without the negation.
- The "pick a broad-journal why-should-anyone-care framing" is out of scope: the venue is fixed
  (BMB), and the biological question is already the abstract's opening.

**Note.** The assessment's own praise of "cells transcribe rerouting potential while buffering
its translation" as a potential anchor sentence confirms v7's retained sentence; no change needed.

---

## Part 2 — `curvature humanized.txt`: three attempts

### 2.1 Qwen attempt (partial, Sections 1–3)

**Strengths.**
- Clean LaTeX-native prose with a disciplined introduction architecture: `\paragraph{The
  object.}` / `\paragraph{The claim structure.}` / `\paragraph{Positioning.}` — the claim list
  (i)–(v) with section pointers is a good compression of the contribution inventory.
- The Kochanowski positioning paragraph ("Our question is different...") is well-shaped and
  nearly matches v7's.
- All checked numbers faithful: mass 288.77; ρ = 0.99998; r ∈ [+0.386, +0.396]; fan area
  0.235 vs 0.235000068; |c^T Δv′| ≤ 1.51e-7 against flux jumps 1.6e4; λ·h_max = 0.500;
  product/atom median 3.296; the 3−1/n and 1.4−1/n TV ratios; 2.9922/1.3922 at n = 128.

**Weaknesses (disqualifying as a base).**
- **Incomplete:** ends at the mpLP conjecture. No Section 4 (computational validation), no
  Section 5 (empirical association), no methods, no appendices, no references.
- **Contains the exact forbidden meta-commentary sentence**: "The measure-theoretic development
  above is self-contained. Nothing in this section uses categorical language, and the reader may
  take κμ exactly as defined." This is the sentence the author quoted as the example of
  unacceptable self-referential prose.
- Changelog tense: "the controlled relation between the value layer and the flux layer **is now**
  a theorem."
- Process-flavored remark titles ("What this closes").
- Register is denser than v7 — a compression, not a humanization.

**Verdict.** Mine for micro-phrasing only (claim-list formatting, the positioning paragraph).

### 2.2 Gemini attempt (complete draft)

**Strengths.**
- The only attempt whose register is genuinely reader-oriented throughout, matching the
  landmark-calibrated target: plain-language glosses at every load-bearing definition
  ("reflects the organism's maximum theoretical fitness (e.g., maximum growth rate)"; the
  visibility dichotomy explained in words; "Strikingly, 11 of the 12 active-set events were
  completely invisible to the biomass objective...").
- **Complete mathematics:** all nine appendix proofs present at full length (respects the
  no-condensation directive), the counts-disambiguation table (Appendix A), the five-result
  introduction, the full tie-break table (TB0–TB4 with per-variant r, partial r, ρ_S, reassigned
  genes), and a well-organized Limitations list.
- **Numbers verified:** every checked value matches v7 (93.4–100.0% concentration; r = +0.395,
  p = 2.6e-17, ρ_S = 0.414, partial r = +0.269; deciles 1.92 vs 0.89; P1/P2 r = +0.318/+0.223
  and cross-correlations +0.378/+0.391; shadow-price arm r = +0.032, partial −0.013, p = 0.93,
  n = 51; PaxDb +0.334; Schmidt protein r = −0.083 vs transcript +0.419; transcript–protein
  r = +0.020, n = 799; PRECISE r = −0.044; dΦ/dq_glc = 0.099544; counts 438/433/424/426/454/
  537/525/4/350/25,107/1,516/2,779; 40 synthetic-lethal isozyme pairs; ρ_S = 0.865;
  J_support = 0.800; 66% non-reverting, median holonomy ≈ 110; 4,000 cuts; crossover window
  2.45–4.11 median 3.1; regime dial 8.9 vs ±1884.6; Danskin 6–7 digits; iML1515 cut 12 events /
  4 clusters / error 0.0; 150 LPs at 1.1e-13; 60/60 at 2.0e-13; boxes at 6.4e-16).
- Methods provenance section (M3D build 6, 4,297 probes × 907 arrays; PRECISE TPM; Schmidt 22
  conditions; PaxDb) matches v7.

**Weaknesses.**
- **Hallucinated cross-citation author:** "Zai, A. (2026)" for the companion paper (the
  citation-key stem leaked into the author field). The author is Abaee. This error must never
  enter the manuscripts; v7's bib is already corrected.
- **Changelog remnant:** "Rank agreement between κμ and **our previously explored geometric
  metric** κ^lex..." — a reference to an earlier metric explored in prior manuscript versions;
  exactly the forbidden previous-version reference. v7 phrases the same fact as invariance under
  the declared lexicographic definition.
- **Five ASCII-art diagram blocks** (chamber/facet pipeline; validation flow; log-D² sketch;
  transcription/protein split; scatter sketch). Not usable in a journal LaTeX submission;
  at most one should be converted to a real TikZ/PGF figure.
- **Markdown–LaTeX hybrid** (`#` headings, `**bold**`, `*italics*`, fenced code, `\citep`
  inside markdown) — requires full conversion; not a `.tex`-compilable artifact.
- Reference list includes entries not cited in its own text (e.g., faith2007, lewis2010,
  danskin1967, ziegler1995, villani2009 as cited but check faith2007) and one fabricated-author
  entry; v7's audited bibliography supersedes it entirely.

**Verdict.** The best *register model* of the three. Harvest glosses, explanation sentences, and
Discussion phrasing; never adopt as a base (format errors, author error, changelog remnant).

### 2.3 Grok attempt (condensed restructure, truncated)

**Strengths.**
- **Complete numerical fidelity to v7.** A 33-point numeric battery returned matches on
  essentially every claim, including deep details (0.69-reaction vertex flips; the
  presolve-disabled retry; 1.7e-6 value/flux mass ratio; 0.0100↔1e-13 follower flip; P0/P1/P2
  mass ratios 1.5e-3/2.4e-4/5.5e-4; folded Wasserstein 0.058→0.0039 and mass ratio
  0.939→1.0009; GC tail slope −0.492 vs null −0.506; FPC √((13−k)/12); "98 checks";
  M3D switch arms +0.195/+0.166/+0.175/+0.206; PRECISE per-condition +0.126/+0.130/+0.099/
  −0.088; platform-by-class +0.196/+0.298/+0.191/+0.345 with signed arms −0.22 to −0.32;
  b2097; −0.063/+0.084 panel-level κ values; "No new measure-theoretic theorem is claimed"
  scoping paragraph — all present in v7).
- Preserves v7's full section inventory, including §5.8 platform-by-class, the tie-break table,
  the stabilization analysis, and the appendix proof architecture with delegated technical
  arguments (Appendix C), matching the author's proof policy ("Where an argument would repeat
  textbook material, the standard source is cited in lieu of reproduction").

**Weaknesses.**
- **Truncated:** the file ends mid-proof (Proposition 4, sec-law proof incomplete).
- **Broken numbering:** "Theorem 3" appears with no Theorem 2; propositions run 1, 2, 3, 6, 7
  before 4, 5. Cross-references use hardcoded section numbers that match no actual document.
- **Abstract regression:** its abstract is the pre-v7 text, including the vague closer
  ("unifies three distinct sensitivity objects") that the current v7 had already replaced with
  the specific form. A reminder that any synthesis must be checked against the **latest**
  version, not an older cached one.
- **Density increased, not decreased:** §4.1 becomes a single 300-word paragraph with a dozen
  parentheticals — the opposite of the humanization goal.
- Minor process phrasing ("Status of the definition... is final"; "resolves the value–flux
  layer relation") that v7 already phrases factually.

**Verdict.** Use as a **fidelity checklist** confirming v7's content inventory; not a style
model, and not adoptable (truncation + numbering).

---

## Part 3 — `companion humanized.txt`: two attempts

### 3.1 Gemini attempt (accessible survey rewrite)

**Strengths.**
- The strongest accessibility writing of all five attempts, exactly on the landmark target:
  - the autopoiesis/homeostasis contrast in one concrete pair (a thermostat cannot rebuild its
    own compressor; a cell synthesizes the enzymes that perform its maintenance);
  - "In intuitive terms: κ ignores harmless rotations, zeroing in exclusively on directional
    policy shifts that actively consume the system's remaining buffer of survival";
  - "Why a Boundary Transition Rule is Essential" with its three-bullet breakdown of what fails
    at a switching wall;
  - the optic "anatomy" explanation and the single-sentence physical reading of the seven-optic
    composition;
  - the four-level falsification roadmap.
- **Correct on the corrected Claim-F structure:** SO(2) abelian at n = 3 (commutator
  identically zero, non-abelian signature unobservable) vs SO(3) non-abelian at n = 4 — matches
  the current v6 Remark (the n = 3 → n = 4 transition) and the joint-assessment correction.
- Banach arithmetic verified: (0.92)^6 × 1.15 ≈ 0.697 < 1; box-invariance argument consistent.
- Seven-claim hierarchy constants preserved (a_rev = 1.0; c₂ = √(5ν)/2; R² ≥ 0.90/0.95;
  ratio ≥ 5; Zeno α ≈ 2 vs classical α ≈ 1); the closure test steps (i)–(v) with the
  x_thresh > 0 threshold rationale.

**Weaknesses.**
- **Severe content loss.** Dropped relative to v6: the six-axis validation battery detail, the
  ATPM near-tie floor, the five-loop-geometry × three-structure-group machine verifications
  (tolerances 1e-13/1e-10; pentagon (5/2)ε²sin(2π/5); ellipse πε²/2), the proof-status
  apparatus, the filtered-colimit RAF construction and its proof, the HoTT extension beyond a
  mention, the operational network battery, the open-problem section, and nearly all proofs
  (one-line sketches at best). For this paper — whose contribution is precisely the
  constructions and their verified status — that is a disqualifying loss under the
  no-condensation directive.
- **Hallucinated cross-citation author** ("Zai, A." for the application paper) — same critical
  error as in its curvature attempt.
- ASCII diagrams and markdown–LaTeX hybrid (not journal-usable).
- Reference list with possibly-uncited entries (arimoto1972, bhattacharyya1943, chentsov1982,
  noether1918, vereshchagin2010rate) and the fabricated-author entry.
- Occasional mild editorializing ("a profound physical dichotomy", "a striking physiological
  dissociation") that sits above the factual register fixed for the paper.

**Verdict.** Gold mine for targeted accessibility grafts (gloss sentences and intuition
remarks); never as a base.

### 3.2 Grok attempt (condensed restructure, truncated)

**Strengths.**
- Faithful condensation of the current v6 §1–§6.1: the SAVGS assembly, StCon(B) with the
  O1–O4 axioms, the gluing theorem with its descent proof-status remark, the piecewise-holonomy
  formula with the two-crossing small-loop form, the Fisher-minimal KKT transport law and its
  proof, the projected differential inclusion at boundaries, the square-root embedding, the
  intervention-based closure test with viability-theoretic reading (kernel/capture-basin), the
  Bregman–Noether correspondence with its falsifiable precondition check, the seven-claim
  hierarchy with the fluctuation-status remark (envelope convention; c₂ = 0.0500 at ν = 0.002
  vs the derivation's ν = 0.1), the typed-endo-optic composition with the endofunctor caveat,
  and the per-optic Lipschitz analysis (α = 0.40, s = 1.00, ρ = 0.80, λ₂ = 1.15).
- The abstract matches the current v6 abstract nearly verbatim, six-axis sentence intact.
- All checked constants and structure match v6 (x_thresh = 0.1 default; a_rev = 1; Remark
  "three objects, one family"; "status conventions" paragraph; Remark 17's operational-curvature
  circularity argument).

**Weaknesses.**
- **Truncated mid-Lemma 2** (per-optic Lipschitz proof cut off). Missing: the rest of §6.1, the
  CPTP/Zeno contraction theorem, the RAF filtered-colimit section, the HoTT §7 development, the
  network battery, the application section, conclusion/open problems, references.
- Same density-increase problem as its curvature attempt.

**Verdict.** Fidelity checklist only; v6 already contains everything it preserves.

---

## Part 4 — Cross-cutting findings

1. **"Zai, A." author hallucination** appears in both Gemini attempts (both cross-citations).
   The manuscripts' bibs already carry Abaee; any harvested sentence must be checked so this
   never migrates in.
2. **The two forbidden prose patterns recur in the inputs themselves:** the Qwen attempt
   contains the exact flagged meta-commentary sentence; the qwen re-sketch contains the exact
   flagged strawman negations. Synthesis must filter both pattern families explicitly.
3. **ASCII art is Gemini's signature** (7+ blocks across the two attempts); none is
   journal-usable. At most one conceptual schematic (chamber → facet → atom) merits conversion
   to TikZ, and only if the figure budget allows.
4. **No attempt achieved accessible + complete simultaneously.** The accessible attempts
   (Gemini) drop or blur content; the faithful attempts (Grok) raise density; the partial
   attempt (Qwen) stops at Section 3. The current v7/v6 remain the only complete, audited,
   format-clean bases.
5. **Grok's abstract regression** (pre-v7 text with the vague closer) shows the hazard of
   re-basing on cached older text — always verify against the latest version.
6. **Found during this verification:** v7's Reproducibility section states "(98 checks)" while
   the current audit suite runs 301 checks (audit_v15). This should be reconciled in the next
   revision (state the numeric-verification count accurately, or distinguish numeric checks
   from journal-package checks).

---

## Part 5 — Merged synthesis implementation plan

### 5.0 Design principles (merged from all sources, including our own)

- **P1 — Graft, don't rewrite.** v7/v6 are the bases: complete, numerically audited (301/301),
  format-clean, already landmark-calibrated. The synthesis applies targeted grafts harvested
  from the attempts; it does not re-base.
- **P2 — Register target.** Formal and reader-oriented with minimal jargon: v7/v6's current
  register, reinforced with Gemini's gloss techniques and qwen's abstract discipline.
- **P3 — Versioning.** All outputs are NEW files: `journal_manuscript_v8.tex` (plus
  `journal_manuscript_v8_bmb_refs.tex` and `journal_manuscript_v8_refs.bib`) and
  `companion_categorical_v7.tex` (plus `companion_refs_v7.bib`). Nothing is overwritten.
- **P4 — Numbers immutable.** Every numerical claim stays byte-identical in meaning; the audit
  is retargeted (audit_v16) and must pass 301/301 on both papers.
- **P5 — Proof policy unchanged.** No condensation; only citation-replacement of textbook
  repetition (already implemented in v7/v6's appendix structure).
- **P6 — Pattern filter.** Before delivery, both new files are swept for the forbidden pattern
  families: meta-commentary/self-reference, changelog tense ("now", "previously", "final",
  "closes"), previous-version references, strawman negations, chat register. Exact pattern list
  in 5.5.

### 5.1 Main paper — work items (journal_manuscript_v8.tex)

| ID | Source | Item |
|---|---|---|
| M1 | qwen A1/A3 | Abstract final pass: compress the robustness clauses (ρ = 0.99998 / five rules / Glivenko–Cantelli) into one sentence; verify technical-term budget; keep hook, all primary numbers, the protein-buffering punchline position, and the specific closer. Re-verify BMB cap (≤ 250 words). |
| M2 | Gemini | Harvest plain-language glosses where v7 is still terse: (a) "maximum theoretical fitness (e.g., maximum growth rate)" at the first appearance of Φ; (b) the one-sentence explanation of objective-invisibility in the coupling section (v7's Remark covers it; graft the "zero-cost pathway substitutions" phrasing if absent); (c) Discussion sentence pattern "This explains why gene expression changes correlate with the flux-layer metric κμ (r = +0.395) but show no association with value-layer derivatives (r = +0.032)". |
| M3 | Gemini (optional) | One TikZ schematic of the chamber → facet → atom pipeline (converting the ASCII block). Decision point: default **defer** — the paper has six figures and the pipeline is already stated in words; implement only if the author wants the added visual. |
| M4 | qwen/Grok pathologies | Meta/strawman sweep of v8 with the Part 5.5 pattern list (the inputs demonstrate the recurrences to filter: "is now a theorem", "our previously explored metric", "is final", "What this closes", "not a smooth curvature tensor"). |
| M5 | This audit | Reconcile the Reproducibility sentence "(98 checks)" with the current 301-check audit suite (state the split accurately: numeric-claim checks vs journal-package checks). |
| M6 | Standing | Panel phrasing: keep the disambiguation (424 = evaluated genes with κμ > 0); make the abstract's "(M3D microarrays, n = 424)" unambiguous — it is 424 genes, and the parenthetical should read e.g. "(n = 424 evaluated genes; M3D compendium)". |
| M7 | Standing | Build (Tectonic, 0 errors / 0 undefined references, expected ~28 pp), retarget audit_v16 → 301/301 PASS, rebuild submission ZIPs (v11 package), retarget cover letters and SUBMISSION_PACKAGE_LINKS.md rows to v8/v7. |

### 5.2 Companion paper — work items (companion_categorical_v7.tex)

| ID | Source | Item |
|---|---|---|
| C1 | Gemini | Insert 3–6 one-sentence intuition glosses at the highest-jargon points, inside existing remarks (no new sections): (a) viability depth vs curvature ("a loop-averaged deficit: it carries no orientation and no path-order"); v6's Definition 1 remark already says this — tighten toward Gemini's phrasing only if it loses nothing; (b) the autopoiesis/homeostasis contrast in one formal sentence (thermostat vs cell, recast without chatty register); (c) the single-sentence physical reading of the seven-optic composition (v6's Remark 23 already has it — verify and keep). |
| C2 | Gemini | "Why a boundary transition rule is essential": v6's Remark 4 already carries the argument; graft Gemini's three-bullet breakdown (sensitivity coefficients jump; smooth horizontal subspaces cease; curvature integrals undefined) as a compact plain-language sentence if not already present in that form. |
| C3 | Grok | No structural adoption (v6 already contains everything it preserves); used only as the fidelity checklist for the C1/C2 edits. |
| C4 | Standing | Meta/strawman sweep of v7 with the 5.5 pattern list. |
| C5 | Standing | Build (0 errors / 0 undefined references, ~75 pp), abstract ≤ 265 words re-check after any edit, audit_v16 301/301, ZIPs v11, links/cover-letter retarget. |

### 5.3 Explicitly rejected items (with reasons)

| Item | Reason |
|---|---|
| qwen re-sketch sentences "not a smooth curvature tensor" / "The singular measure, not a smooth Hessian, is the object a cell actually navigates" | Phantom-negation strawman; the author's flagged artifact family. The v7 factual contrast (slope 1.00 vs quadratic) already covers the content. |
| Qwen §2.5 opening ("self-contained... nothing in this section uses categorical language") | The exact forbidden self-referential meta-commentary. v7's corresponding subsection is already factual. |
| Gemini's "our previously explored geometric metric κ^lex" phrasing | Previous-version reference; v7 states the same fact as metric invariance under the declared definition. |
| All ASCII art blocks | Not journal-usable; conceptual content already in prose (see M3 for the single candidate). |
| Gemini's reference lists | Superseded by the audited v7/v6 bibs; contain the "Zai, A." fabrication and uncited entries. |
| Gemini's Appendix B as a wholesale replacement | Its arguments are fine, but v7's proofs are audit-anchored and include the Fourier–Motzkin construction for Lemma 1 that Gemini's version replaces with a probabilistic-uniqueness argument — silently swapping proof arguments is forbidden; any proof change requires explicit verification. |
| Grok's condensed paragraph style; Grok's numbering scheme | Anti-accessibility; broken cross-references. |
| Gemini's "profound dichotomy / striking dissociation" adverbial register | Above the factual register fixed for both papers; v7/v6 phrasing stands. |

### 5.4 Execution order

1. Create `journal_manuscript_v8.tex` (+ refs files) from v7; apply M1, M2, M5, M6; run M4 sweep.
2. Create `companion_categorical_v7.tex` (+ `companion_refs_v7.bib`) from v6; apply C1, C2; run C4 sweep.
3. Decision point (author): M3 TikZ schematic — yes/no.
4. Tectonic builds; fix any overfull/undefined issues.
5. Retarget the number audit to v8/v7 (audit_v16_numbers.py from v15); require 301/301 PASS.
6. Rebuild submission ZIPs (v11), retarget cover letters and links doc rows.
7. Commit and push (new PAT); report full paths of the latest packages.

### 5.5 Acceptance criteria (per paper)

- Tectonic: 0 errors, 0 undefined references; page counts ~28 (main) / ~75 (companion).
- audit_v16: 301/301 PASS, all numbers byte-identical to v7/v6 in meaning.
- Abstracts: main ≤ 250 words (BMB), companion ≤ 265 words; hook/punchline/closer structure per Part 1.
- Forbidden-pattern sweep returns zero hits on the following list (case-insensitive):
  "not a smooth curvature", "not a smooth Hessian", "is now a theorem", "our previously",
  "previously explored", "is final for", "what this closes", "self-contained" (as a
  self-description), "earlier drafts", "prior versions of this", "homogenized",
  "in this round/revision/pass", "chat", "as requested", "the author's earlier".
- No "Zai" author string anywhere; cross-citations read Abaee.
- Reproducibility check-count sentence reconciled with the audit suite.
- All files are new versioned artifacts; no existing file modified.

---

## Appendix — verification evidence (summary)

**Main-paper numeric battery (33 patterns run against v7):** 30 direct PASS; 3 explained —
(1) "rho 0.932" is figure-level (Fig. 3), not body text; (2) "1.7×10⁻⁶" present with LaTeX
spacing (manual context check PASS); (3) "98 checks" present in v7 (reconciliation item M5).
All Gemini/Grok numbers listed in Parts 2–3 verified present in v7, including the tie-break
table, PRECISE per-condition values, platform-by-class values, and the appendix tolerances.

**Companion structural battery (v6):** six-axis sentence in abstract (carbon, oxygen, nitrogen,
phosphate, iron, non-medium maintenance stress; canonical-selection invariance; declared
tie-break closing its near-degeneracy boundary); ATPM/near-tie content present (20 hits);
tie-break content (8 hits); n = 3 → n = 4 transition remark with SO(2)/SO(3)/CO(r) precision;
five loop geometries (rectangle, triangle, pentagon, circle, ellipse) and three structure
groups (U(1), SO(3), CO(3)); 375-configuration grid; 0.697 contraction; Krasnoselskii–Mann
averaging; Zeno (39 hits); proof-status conventions; x_thresh = 0.1 default; a_rev = 1;
"three objects, one family" remark; fluctuation-status/envelope-convention remark (c₂ =
0.0500 at ν = 0.002 vs derivation ν = 0.1); operational-curvature circularity remark;
recommended experimental ordering. Author fields: Abaee present in both manuscripts and all
three bib files; zero "Zai, A." remnants.
