#!/usr/bin/env python3
"""Create build_submission_zips_v20.sh from the v19 script.

Retargets the main package to journal_manuscript_v17.tex (refs v17),
the fresh-dir verification dirs to zipcheck_v20, and adds the
venue-neutral target-venue note to the main README.
"""

src = open("scripts/build_submission_zips_v19.sh").read()

old_hdr = """#!/bin/bash
# Build self-contained, compile-ready submission ZIPs for the v19 round:
# main = journal_manuscript_v16.tex (BMB), companion = companion_categorical_v10.tex (TAC)."""
new_hdr = """#!/bin/bash
# Build self-contained, compile-ready submission ZIPs for the v20 round:
# main = journal_manuscript_v17.tex, companion = companion_categorical_v10.tex (TAC)."""
assert old_hdr in src
src = src.replace(old_hdr, new_hdr)

src = src.replace('STAGE=scripts/overleaf_stage_v19', 'STAGE=scripts/overleaf_stage_v20')
src = src.replace('cp scripts/journal_manuscript_v16.tex          "$M/"',
                  'cp scripts/journal_manuscript_v17.tex          "$M/"')
src = src.replace('cp scripts/journal_manuscript_v16_bmb_refs.tex "$M/"',
                  'cp scripts/journal_manuscript_v17_bmb_refs.tex "$M/"')
src = src.replace('cp scripts/journal_manuscript_v16_refs.bib     "$M/"',
                  'cp scripts/journal_manuscript_v17_refs.bib     "$M/"')
src = src.replace('document to journal_manuscript_v16.tex, recompile. (Run twice so natbib',
                  'document to journal_manuscript_v17.tex, recompile. (Run twice so natbib')
src = src.replace('- Command line: pdflatex journal_manuscript_v16.tex  (x2)',
                  '- Command line: pdflatex journal_manuscript_v17.tex  (x2)')
src = src.replace('- journal_manuscript_v16.tex        main source (main document)',
                  '- journal_manuscript_v17.tex        main source (main document)')
src = src.replace('- journal_manuscript_v16_bmb_refs.tex  reference list (input by the main file)',
                  '- journal_manuscript_v17_bmb_refs.tex  reference list (input by the main file)')
src = src.replace('- journal_manuscript_v16_refs.bib   underlying BibTeX database (not required',
                  '- journal_manuscript_v17_refs.bib   underlying BibTeX database (not required')
src = src.replace("- Abstract: 255 words (within the author's 255-word cap), in two paragraphs",
                  "- Abstract: 254 words (within the author's 255-word cap), in two paragraphs")
src = src.replace('zipcheck_v19', 'zipcheck_v20')
src = src.replace('echo "=== fresh-dir compile: main v16 ==="',
                  'echo "=== fresh-dir compile: main v17 ==="')
src = src.replace('tectonic journal_manuscript_v16.tex 2>&1 | tail -2 && \\\n pdfinfo journal_manuscript_v16.pdf | grep Pages)',
                  'tectonic journal_manuscript_v17.tex 2>&1 | tail -2 && \\\n pdfinfo journal_manuscript_v17.pdf | grep Pages)')
src = src.replace("""## Formatting notes (Springer BMB submission guidelines)""",
                  """## Target venue
- Venue per download/V17_Venue_Evaluation.md (in the repository): JTB is
  the primary recommendation; BMB return only via pre-submission inquiry;
  PLOS Comp Bio the bio-first alternative (APC). The package itself is
  venue-neutral and compiles identically for any of them.

## Formatting notes (Springer BMB submission guidelines, where applicable)""")
src = src.replace('#   - All numerical claims re-verified: audit_v24_numbers.py 301/301\n#     PASS;',
                  '#   - All numerical claims re-verified: audit_v25_numbers.py 344/344\n#     PASS (301 carried + 43 new v17 checks);')

open("scripts/build_submission_zips_v20.sh", "w").write(src)
print("build_submission_zips_v20.sh written")
