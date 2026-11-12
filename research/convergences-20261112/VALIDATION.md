# Probe validation

All nine authored probes reproduced their saved scientific results during publication preparation on 2026-11-12. The check regenerated ten artifacts, including the hidden-dynamics trajectory CSV, in a temporary directory. No scientific values changed.

From the repository root:

```sh
python3 -m venv .venv-convergences
.venv-convergences/bin/python -m pip install -r research/convergences-20261112/requirements.txt
.venv-convergences/bin/python research/convergences-20261112/check.py
```

A fresh virtual environment installed the pinned requirements and passed the same check. The publication check used Python 3.14.6, NumPy 2.5.4 and SymPy 1.14.0. NumPy is used by relations and robustness. SymPy is used by issue-5. The other probes use the Python standard library, including the historical gravity modules imported by scales.

The checker compares every generated JSON field and every trajectory CSV cell against the committed artifacts. Strings, structure and Boolean values must match exactly. Numbers must be finite and agree within relative tolerance 1e-9 or absolute tolerance 1e-12. Interpreter and library version labels are excluded from scientific comparisons.

The relations script also offers its original stricter `--check` comparison with absolute tolerance 1e-12. Robustness retains its own `--check` comparison with relative tolerance 1e-9 and a unit absolute floor.

The saved JSON artifacts retain the original run's version labels. The original absolute interpreter path is replaced by `python3`. Historical input paths are replaced by bundle-relative paths. These are metadata changes. The scales and robustness formulas, constants, seeded inputs, assertions and saved numerical values are unchanged.

The exact wave10 source, its wave7 import dependency and the wave10 certificate are bundled with digests. Their bytes match gravity commit `d8c7544e89388720fc1c13de816ddb7dd03d2096`. The certificate supplies the robustness collapse-dispersion column, which remains explicitly identified as reused. The manifest prevents a changed historical input from silently passing the check.

The scoped GitHub Actions workflow runs only for bundle or workflow changes. Hosted CI results are separate evidence from this local check. No downloaded papers, extracted paper text, HTML reading copies, rendered page images, private coordination files or local operations snapshots are included.
