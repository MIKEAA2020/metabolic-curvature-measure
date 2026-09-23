#!/usr/bin/env python3
"""v19 post-audit patch: set the two Methods audit-count mentions to the
final audit_v27 count (349), recompile-verify stays with tectonic after.
Also refreshes the download copies. v19 is a new file (no overwrite of
earlier versions); this edits the v19 file itself before commit."""
import shutil

S = "/home/z/my-project/metabolic-curvature-measure/"
p = S + "scripts/journal_manuscript_v19.tex"
tex = open(p).read()

N = 349
old1 = "described under Reproducibility\n($344$ checks)."
new1 = f"described under Reproducibility\n(${N}$ checks)."
old2 = "An automated suite of $344$ numeric checks"
new2 = f"An automated suite of ${N}$ numeric checks"

for old, new, tag in [(old1, new1, "methods counts mention 1"),
                      (old2, new2, "methods counts mention 2")]:
    assert old in tex, f"anchor not found: {tag}"
    assert tex.count(old) == 1, f"anchor not unique: {tag}"
    tex = tex.replace(old, new)
    print("patched:", tag, "->", N)

open(p, "w").write(tex)
shutil.copyfile(p, S + "download/journal_manuscript_v19.tex")
print("download copy refreshed")
