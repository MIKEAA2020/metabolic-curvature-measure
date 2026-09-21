# V17 Venue Evaluation — Best Journal Fit and the BMB Resubmission Question

**Date:** September 21, 2026
**Manuscript:** journal_manuscript_v17.tex (38 pp, audit_v25 344/344 PASS)
**Question posed:** (1) What is the best journal fit for the paper as
it now stands, after the V17 enrichment? (2) Can we resubmit to the
Bulletin of Mathematical Biology (BMB), which desk-rejected the
earlier version?

---

## 1. What changed since the BMB desk rejection

The BMB desk verdict was: *"biological impact and implications … not
sufficiently strong for our readership."* That verdict was rendered
on the v16 manuscript: a geometry framework whose biological
evidence was statistical (a correlation and a dissociation) with
regulators and metabolites present but not named as findings.

v17 changes exactly that dimension, with computed substance rather
than assertion:

| Dimension | v16 state | v17 state |
|---|---|---|
| Regulatory anchoring | 1 regulon/TF mention | Named regulator table: 11 regulons enriched at BH q < 0.10, led by CRP (56/89 targets in the top curvature quartile, fold 2.43, q = 8.6e-16); induction-specific split (activation p = 0.0016, repression p = 0.43) |
| Genetic architecture | operons unmentioned | 7 whole operons in the top quartile (nuo 13/13, atp 9/9, sdh-suc 8/8, cyo 4/4); near-uniform within-operon curvature surviving the GPR disjoint-reaction control |
| Chemical observability | none named | Wall-coordinate table: 20 branch metabolites carry 59.7% of curvature mass (F6P 8.1%, GAP 6.9%, G6P 5.5%, DHAP 4.9%, PEP 4.5%); 98.6% branch/currency-adjacent — a targeted-metabolomics readout |
| Mechanistic deduction | buffering as a finding bullet | Memory-substrate deduction: protein layer carries at most 0.7% of variance vs 66% non-reverting cycles, so the carrier of metabolic memory is forced to be fast post-translational state |
| Engineering use | none | Construction-order design rule (rho = 0.442, sign 59/66, binomial p = 2.4e-11) with the honest null (overlap does not predict order) |
| Architecture | none | Conserved-interior architecture: exchange interface flat (92.6%), walls on internal branch-point chemistry (75.4% of mass, five central subsystems 73.3%) |
| Pedagogy | no toy network | Hand-checkable worked example (machine-verified), MCA positioning subsection |

Every number is computed from deposited artifacts and covered by the
344-check audit. The BMB criticism is now answerable point by point.

## 2. Can we resubmit to BMB?

**Mechanically: yes. Strategically: not as a blind resubmission.**

The facts:

1. **A desk rejection is an editorial (scope/fit) decision, not a
   peer-review verdict.** BMB desk-rejected without review. Springer
   journals accept new submissions of previously rejected manuscripts
   in principle — there is no formal ban — and the submission system
   will not block it.
2. **The desk will recognize it.** Same title, same author, same
   framing; v17 adds five subsections but does not change the paper's
   identity. The most likely reader of a new submission at BMB's
   editorial office is the same person who wrote the prior verdict.
3. **The stated reason is now addressed, but the underlying fit
   question is not obviously changed.** BMB is the Society for
   Mathematical Biology's journal; its readership balance leans
   mathematical. v17 makes the paper *more* biological (named regulons,
   metabolites, design rules) on the same classical-mathematics
   chassis. It is genuinely arguable that the paper has moved *further*
   from "mathematical biology" toward "computational/systems biology,"
   even as it answers the specific criticism.
4. **Expected outcomes.** A blind resubmission most plausibly gets a
   second desk rejection (the prior stands; no reviewers were involved
   whose opinion could be overturned), at the cost of 1–2 weeks and a
   slightly irritated editor. The probability of a different outcome is
   not zero — the revision is substantial and directly on-point — but
   it is not the maximizing play.

**The professional path to BMB, if the author wants it: a
pre-submission inquiry.** One email to the Editor-in-Chief that (a)
transparently references the prior desk decision, (b) summarizes the
substantial revision in four sentences, and (c) asks whether a
resubmission would be considered. This either produces an invitation
(a resubmission with a real chance, since the editor asked for it) or
a fast, informative "not for us" at zero submission cost. A draft is
provided in Section 5.

## 3. Best-fit assessment of the alternatives

**Journal of Theoretical Biology (JTB) — primary recommendation.**
- Scope match: regulatory-FBA lineage is core JTB material — the
  precedent is direct (Covert, Schilling & Palsson, "Regulation of
  gene expression in flux balance models of metabolism," JTB 213:73–88,
  2001; the regulatory-integration line descends from it). The v17
  additions (case study, design rule, architecture) read as normal JTB
  substance, not as venue-specific reframing.
- All six insight lines fit as-is; the theory/proofs sections are
  unexceptional there.
- Elsevier subscription route: no mandatory APC; single-blind;
  Editorial Manager; review expectations moderate.
- Cost/risk: lowest. Biology ceiling: middle — JTB readers accept
  gene-level findings but the paper would not be a "highlight" there.

**PLOS Computational Biology — the biology-maximizing option.**
- Scope match: the gene-expression × constraint-based-models genre is
  an established PLOS CB staple (e.g., Machado & Herrgård 2014,
  "Systematic evaluation of methods for integration of gene expression
  data into constraint-based models," PLOS Comput Biol 10:e1003800).
  v17's named-biology findings (regulon/operon enrichment, branch-
  metabolite coordinates, memory substrate) are exactly the journal's
  "biological insight from computation" remit; the BMB criticism is
  answered most forcefully here.
- Methods + Findings article types both plausible; no length trauma at
  38 pp; the reproducibility package (344-check audit, public repo)
  aligns with PLOS's data-availability culture.
- Cost: APC ≈ US$2,400–2,500 (fee assistance exists); verify the
  current schedule at submission time.
- Risk: methodological review can be demanding; the paper's LP-machinery
  novelty claims must survive PLOS CB's standards for "new method vs
  known method applied well" — the MCA-comparison subsection (v17)
  is the right defense, already in place.

**Mathematical Biosciences — zero-risk mathematical backup.**
Adequate fit, adequate readership, no APC; use only if both primary
paths fail. The v17 biology adds nothing there that JTB would not
reward more.

**Bioinformatics (methods track) — not recommended.** The paper's
center of gravity is a finding (regulation reads rerouting geometry)
carried by a method, not a tool; the methods-track framing would
shrink the biology that v17 just built.

**TAC (companion) — unaffected by this round.** The companion remains
targeted at Theory and Applications of Categories (Transmitting
Editor Prof. Michael Shulman, verified on the live board); no change.

## 4. Recommendation

1. **Primary: submit v17 to JTB** if the priority is a fast, no-cost,
   well-fitted home with the six insight lines intact.
2. **Alternative: submit v17 to PLOS Computational Biology** if the
   priority is maximal biological reach and the APC is acceptable —
   this is the venue where the BMB verdict's criticism is most
   completely overturned, and the strongest "rebuttal-in-advance."
3. **BMB: do not blind-resubmit.** If the author wants BMB, send the
   pre-submission inquiry below first; resubmit only on invitation.
4. **Either way, the ZIP package is venue-neutral**
   (download/submission_main_bmb.zip, v20 build): it compiles
   identically for all three venues; only the cover letter changes.

## 5. Pre-submission inquiry draft (BMB, send to the
Editor-in-Chief via the journal's contact address)

> **Subject:** Pre-submission inquiry — substantially revised
> manuscript previously desk-rejected (geometric theory of metabolic
> flux rerouting)
>
> Dear Professor [Editor-in-Chief],
>
> In [month] 2026 you kindly considered "A Geometric Theory of
> Metabolic Flux Rerouting: How Active-Set Curvature Predicts
> Transcriptional Regulation and Protein-Layer Buffering" and declined
> it at the desk, noting that the biological impact and implications
> were not sufficiently strong for the journal's readership. That
> judgment was fair, and I have spent the interval doing exactly the
> work it implied.
>
> The manuscript has been substantially revised. It now identifies, by
> name, the biology the curvature measure predicts: the induced genes
> sit in eleven enriched regulons led by CRP (Benjamini–Hochberg
> q = 8.6 × 10⁻¹⁶) at whole-operon granularity (nuo, atp, sdh–suc,
> cyo); the rerouting mass concentrates on twenty named branch
> metabolites of central carbon (59.7% of mass; F6P/GAP/G6P/DHAP/PEP
> foremost), giving the theory a targeted-metabolomics readout; the
> protein-layer buffering null is developed into a quantitative
> deduction that metabolic memory must be carried in fast
> post-translational state; and a construction-order rule for strain
> design is derived from the same geometry (Spearman ρ = 0.442,
> sign agreement 59/66, binomial p = 2.4 × 10⁻¹¹). Every new number is
> computed from deposited artifacts under a 344-check reproducibility
> audit. A hand-checkable worked example and a metabolic-control-
> analysis comparison section have been added for the journal's
> readership.
>
> May I ask whether a resubmission of the revised manuscript would be
> considered by the Bulletin? I would of course flag the prior
> submission in the cover letter and make both versions available to
> the editors.
>
> With thanks for your time,
> Amin Abaee

## 6. If resubmitting anyway (against recommendation)

- Flag the prior submission and the desk verdict in sentence one of
  the cover letter; never let the desk discover it.
- The cover letter should quote the original verdict verbatim and
  respond to it point by point (the table in Section 1 is the
  response).
- Expect the same editor; do not appeal the original decision in the
  same breath as resubmitting — the inquiry route and the appeal route
  are different letters.
- Update the letter's date, version pointers (v17, 38 pp, 344 checks),
  and the companion-disclosure paragraph (companion v10 for TAC).

---

**Sources consulted (live, 2026-09-21):** BMB/Springer journal pages
(SMB affiliation, scope, Editorial Manager); PLOS CB journal
information and fee pages; JTB scope and the Covert–Schilling–Palsson
2001 precedent (JTB 213:73–88); PLOS CB genre precedent (Machado &
Herrgård 2014, PLOS Comput Biol 10:e1003800); editorial-practice
guidance on desk-rejection resubmission (Editage; academia
discussions). The BMB desk-rejection wording is quoted from the
decision letter of record.
