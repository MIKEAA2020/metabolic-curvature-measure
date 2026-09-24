# Final Read-Through Pass of Both Manuscripts' Prose — Evaluation

Date: 2026-09-24
Scope: journal_manuscript_v20.tex (main, 2,969 lines, 37 pp) and
companion_categorical_v13.tex (companion, 6,181 lines, 76 pp), read
end to end at the prose level; findings applied as the V21/V14
final-prose round on NEW versioned files (never overwriting earlier
versions).

Questioned asked: "run a final read-through pass of both manuscript's
prose."

## Method

Both manuscripts were read in full, front matter to backmatter, at the
language level (grammar, sentence flow, terminology consistency,
cross-reference conventions, stale numbers, and internal consistency of
reported values). This pass is deliberately distinct from the earlier
causal-coherence and math-prose-alignment reviews (which verified the
hypothesis→model→math→empirics chain and every load-bearing gloss):
here the unit of inspection is the sentence. Every finding below was
traced to its underlying artifact before any fix was applied, and every
fix preserves logical precedence — the numbers, theorem statements,
proofs, section order, tables, and figures are untouched in both
papers.

## Findings — main paper (v20)

**M1 (consistency of a reported value, Discussion "Where metabolic
memory lives").** The paper quotes the same-gene transcript correlation
as +0.419 twice — §5.9 ("directly opposing the strong transcriptional
correlation ($r = +0.419$)") and the buffering subsection ("transcript
$+0.419$ against protein $r = -0.083$ on the same $366$ genes") — but
the memory subsection says "while transcripts on the same genes carry
$r = +0.420$". Traced to the artifacts: the +0.419 is the e27 primary
arm (novelty_v20_e27_schmidt_replication.csv arm
e24-transfc-on-schmidt-subset, 0.4186, n = 365 — the value the audit
E27-1 recomputes and gates), while +0.420 is the v17-ledger
recomputation of the same quantity (v17_insight_substantiation.json,
transcript_M3D_on_protein_subset, 0.4197) at slightly different gene
matching. Same conceptual quantity, two artifacts, two three-decimal
roundings — an apparent numerical inconsistency to any reviewer. Fixed
by harmonizing to +0.419 (the primary artifact value, matching the
other two sites and the audit gate).

**M2 (unexplained terminology, same sentence).** "under the locked
$\kmu$ metric the picture is unchanged (protein $r = -0.098$,
$p = 0.06$; transcript $r = +0.339$)". The word "locked" appears nowhere
else in the paper, and the phrase contradicts §5.9, which attributes
the −0.083 flatly to $\kmu$. Traced: the −0.098/+0.339 pair is the
per-gene $\kmu$ of the V7 P0 deposits (v17 ledger arms
protein_exhaustion_kappa_mu / transcript_M3D_kappa_mu, sourced from the
per-gene path artifacts), i.e. an independent per-gene instantiation of
the same declared metric — not a "locked" variant of something
previously unlocked. Fixed by naming the actual provenance: "the
picture is unchanged under the per-gene path metric of §5.7". Numbers
unchanged.

**M3 (venue label convention).** All six in-text figure references read
"Fig 1" (source `Fig~\ref{...}`, no period), while the captions carry
the journal's "Fig. n" label form. Springer/DAM style is "Fig. 1" in
text as well. All six normalized to `Fig.~\ref{...}`.

**Comment-level (non-prose).** The header comment still pointed to the
companion as v9 (stale since the v10 round); refreshed to v14 in the
new version's comment block. The audit-count text (two sites: Methods
"($359$ checks)" and Reproducibility "suite of $359$ numeric checks")
was refreshed to the new v31 ledger size (366).

## Findings — companion (v13)

**C1 (displaced clause, Theorem stratified-holonomy).** After the
displayed equation (eq:piecewise-F), an inserted regime-qualification
paragraph ("For affine wall transitions ... (Open Problem 1).") had
come between the equation and its where-clause, so the paragraph read
"... (Open Problem 1). where $F_\pm$ are the curvature $2$-forms ..." —
a lowercase sentence fragment. Fixed by transposing the where-clause
back to immediately follow the equation; both blocks keep their exact
content, only their order is restored.

**C2 (factual self-contradiction, Remark two-contractions).** The
remark says Theorem unconditional-banach establishes contraction "on
the operational state space $X=[0,1]^{d}$" — but the theorem, the
realization definition, and the KM-instantiation remark all use
$X=[-1.5,1.5]^{d}$, and the box-invariance paragraph explicitly states
that the smaller box $[0,1]^{d}$ FAILS the hypothesis (the chain's
image exceeds it). Corrected to the theorem's box.

**C3 (punctuation artifact, Lemma ito-expand proof).** The variance
parenthetical ended "... not the free-Brownian-motion Lévy-area
variance.); and the ..." — a sentence-final period inside the
parenthesis followed by ");". Made an inline lowercase clause
("(the value $1/12$ is ... variance); and the ...").

**C4 (venue label convention).** The companion's figure captions
rendered as "Figure N:" (article default) while the main paper's carry
the journal's "Fig. n" form, and the in-text references were mixed
(3× "Figure~\ref", 1× "Fig.~\ref"). Aligned with the main paper and
the journal: caption package with labelsep=space plus
figurename=Fig. in the preamble, and the three "Figure~" references
normalized to "Fig.~" — the companion's captions and in-text
references now match the main paper exactly.

## What was checked and found clean

The full read covered: title/abstract/keywords vs body claims (both
papers); the main paper's three-question intro and plan-of-paper
section map (accurate); all in-words glosses (μ as matrix-valued Radon
measure, κ^μ as parameter-free rerouting burden, the coupling identity
dichotomy, the resolution window, the anatomy/tie-break/path-robustness
narratives, the MCA comparison, the memory deduction, the limitations
list — internally consistent and consistent with the companion's
restatement of the division of labor); every cross-reference and
citation form (numeric square-bracket natbib throughout; DAM refs list
29 entries; the companion's bibliography and 12 figure paths); the
companion's abstract (248 words, six-axis sentence covering all three
body categories), plan-of-the-paper two-sevens disambiguation, proof-
status markings, verdict tables (n=4 battery, stress grid, network
battery A–K, canonical-selection table), Keio arm bookkeeping (E12/
E15/E16/glucose-only/O2/N/Pi/Fe/ATPM), and declarations. No further
defects were found: every number quoted in prose matches its artifact
(M1 was the single exception), terminology is used consistently
(M2/C2 the exceptions), and the sentence-level grammar is otherwise
clean (C1/C3 the exceptions).

## Application and verification

Applied on new versioned files via scripts/v21_v14_final_prose_fixes.py
(main v20 → v21; companion v13 → v14; earlier versions untouched), with
side files carried (journal_manuscript_v21_dam_refs.tex — 29 entries
byte-identical to the v20 list; journal_manuscript_v21_refs.bib;
companion_refs_v14.bib — byte-identical to v13). Verification:

- audit_v31_numbers.py: **366/366 PASS** (the full v30 ledger carried —
  all 359 numeric/artifact checks unchanged — plus seven new V21 gates:
  M1/M2 tokens, M3 Fig.-label form, C1 where-clause order, C2 state
  space, C3 punctuation, C4 companion figure labels, and the refs/bib
  carry check; the audit-count self-consistency gate confirms the
  manuscript states 366).
- tectonic: main 37 pp / companion 76 pp, 0 errors, 0 unresolved "??";
  companion captions render "Fig. 1" with no "Figure N:" remaining.
- v26 ZIPs rebuilt (build_submission_zips_v26.sh) with fresh-dir
  compile verification (37/76 pp); PDF copies deposited in download/.
- DAM cover letters retargeted (v21/v14 file pointers; 366/366 audit
  statement); SUBMISSION_PACKAGE_LINKS.md updated (15 anchored edits).

## Verdict

Both manuscripts' prose is now clean at the sentence level. The pass
found seven actionable defects (one value-harmonization, one
terminology-provenance fix, one self-contradiction in a technical
remark, one displaced clause, one punctuation artifact, two
figure-label convention alignments) — none touching any result, proof,
or number. The packages are submission-ready for Discover Applied
Mathematics: journal_manuscript_v21.tex (37 pp) and
companion_categorical_v14.tex (76 pp).
