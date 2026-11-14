#!/usr/bin/env python3
"""Replay the failed real-growing-mode gate without changing its rule."""
import hashlib,json
from pathlib import Path
import numpy as np
import probe
p=Path(__file__).resolve().parent
rows=[]
for k in (6.,9.,12.,18.,24.):
    probe.KVAL=k
    ee=np.linalg.eigvals(probe.matrix(1.))
    rows.append({'k':k,'eigenvalues':[[float(e.real),float(e.imag)] for e in ee],
                 'positive_imaginary_pairs':int(sum(ee.imag>1e-8))})
assert all(r['positive_imaginary_pairs']==2 for r in rows)
result={'original_protocol_sha256':hashlib.sha256((p/'GROWING-MODE-PROTOCOL.md').read_bytes()).hexdigest(),
        'result':'Real growing/decaying pair assumption fails at all five initial wave numbers. No closure errors were evaluated under this rule.',
        'rows':rows}
(p/'selection-failure.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
