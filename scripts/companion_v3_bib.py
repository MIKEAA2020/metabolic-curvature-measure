#!/usr/bin/env python3
"""Append the 10 new bibliography entries (6 P0 citations + the Keio
trio + Bousfield-Kan) to scripts/journal_manuscript_refs.bib, the
companion's bibliography file. Data transcribed from the frozen v1's
embedded bibliography (journal_manuscript.tex L10758-10832) plus the
standard Bousfield-Kan reference; the v1's 'Cited in ...' commentary
is dropped."""
import sys

F = "scripts/journal_manuscript_refs.bib"
src = open(F).read()

entries = """
@article{hirota2023alife,
  author = {Hirota, R. and Saigo, H. and Taguchi, S.},
  title = {Reformalizing the notion of autonomy as closure through
           category theory as an arrow-first mathematics},
  journal = {Artificial Life (ALIFE 2023)},
  year = {2023},
  note = {arXiv:2305.15279}
}

@article{segura2026topos,
  author = {Segura, J.},
  title = {Autopoiesis as viability-localized self-production in a
           topos},
  journal = {SSRN},
  year = {2026},
  note = {SSRN 6265619 / PubMed 42107485}
}

@article{dittrich2007cot,
  author = {Dittrich, P. and Speroni di Fenizio, P.},
  title = {Chemical organisation theory},
  journal = {Bulletin of Mathematical Biology},
  volume = {69},
  number = {4},
  pages = {1199--1231},
  year = {2007},
  note = {arXiv:q-bio/0501016}
}

@article{handorf2005network,
  author = {Handorf, T. and Ebenh{\\"o}h, O.},
  title = {Expanding metabolic networks: scopes of compounds,
           reactions and enzymes},
  journal = {Bioinformatics},
  volume = {21},
  number = {9},
  pages = {2078--2080},
  year = {2005}
}

@article{becker2021zeno,
  author = {Becker, S. and D'Aurelio, M. and Jex, I.},
  title = {Quantum Zeno effect in open quantum systems},
  journal = {Physical Review A},
  year = {2021}
}

@article{bravetti2023noether,
  author = {Bravetti, A. and de León, M. and Marrero, J. C. and
            Padrón, E. and Diego, D.},
  title = {Thermodynamic entropy as a Noether invariant from contact
           geometry},
  journal = {Physical Review Letters},
  year = {2023}
}

@article{orth2011ijo1366,
  author = {Orth, J. D. and Conrad, T. M. and Na, J. and Lerman, J. A.
            and Lerman, J. and and Feist, A. M. and Palsson, B. {\O}.
            and others},
  title = {A comprehensive genome-scale reconstruction of
           {\\emph{Escherichia coli}} metabolism---2011},
  journal = {Molecular Systems Biology},
  volume = {7},
  pages = {535},
  year = {2011},
  note = {PMID 21846834}
}

@article{baba2006keio,
  author = {Baba, T. and Ara, T. and Hasegawa, M. and Takai, Y. and
            Okumura, Y. and Baba, M. and Datsenko, K. A. and Tomita, M.
            and Wanner, B. L. and Mori, H.},
  title = {Construction of {\\emph{Escherichia coli}} K-12 in-frame,
           single-gene knockout mutants: the Keio collection},
  journal = {Molecular Systems Biology},
  volume = {2},
  pages = {2006.0011},
  year = {2006}
}

@article{monk2017iml1515,
  author = {Monk, J. M. and Lloyd, C. J. and Brunk, E. and Mih, N. and
            Saad, A. and Ebrahim, B. R. and Palsson, B. O.},
  title = {{iML1515}, a knowledgebase that computes
           {\\emph{Escherichia coli}} traits},
  journal = {Nature Biotechnology},
  volume = {35},
  pages = {904--908},
  year = {2017}
}

@book{bousfield1972,
  author = {Bousfield, A. K. and Kan, D. M.},
  title = {Homotopy Limits, Completions and Localizations},
  series = {Lecture Notes in Mathematics},
  volume = {304},
  publisher = {Springer},
  year = {1972}
}
"""

# orth2011ijo1366: fix the doubled "and and" author glitch
entries = entries.replace(
    "Lerman, J. A.\n            and Lerman, J. and and Feist",
    "Lerman, J. A. and Feist")

new_keys = ["hirota2023alife", "segura2026topos", "dittrich2007cot",
            "handorf2005network", "becker2021zeno", "bravetti2023noether",
            "orth2011ijo1366", "baba2006keio", "monk2017iml1515",
            "bousfield1972"]
for k in new_keys:
    if k in src:
        print(f"FAIL: key {k} already present in {F}")
        sys.exit(1)

if not src.endswith("\n"):
    src += "\n"
src += entries
open(F, "w").write(src)
print(f"ok: appended {len(new_keys)} entries to {F}")
