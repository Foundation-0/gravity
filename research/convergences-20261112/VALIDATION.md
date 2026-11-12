# Probe validation

All nine authored probes reproduced their saved scientific results during publication preparation on 2026-11-12. The check regenerated ten artifacts, including the hidden-dynamics trajectory CSV, in a temporary directory. No scientific values changed.

From the repository root:

```sh
python3 -m venv .venv-convergences
.venv-convergences/bin/python -m pip install -r research/convergences-20261112/requirements.txt
.venv-convergences/bin/python research/convergences-20261112/check.py
```

A fresh virtual environment installed the pinned requirements and passed the same check. The publication check used Python 3.14.6, NumPy 2.5.4 and SymPy 1.14.0. NumPy is used by relations and robustness. SymPy is used by issue-5. The other probes use the Python standard library, including the historical gravity modules imported by scales.

The checker compares every generated JSON field and every trajectory CSV cell against the committed artifacts. Strings, structure and Boolean values must match exactly. Except for the six finite-difference residuals described below, numbers must be finite and agree within relative tolerance 1e-9 or absolute tolerance 1e-12. Interpreter and library version labels are excluded from scientific comparisons.

The five `robustness/results.json` fields `mechanics.rows[i].energy_hessian_discrepancy` measure error in an independent Hessian check. They compare the symmetric finite-displacement spring energy at step 1e-4 with the matrix quadratic form. Both saved and regenerated residuals must be nonnegative, finite and strictly below 3e-8, matching the original probe assertion.

These residuals include truncation and rounding error, so their final digits are not scientific predictions. Hosted Linux produced 7.631495435589386e-10 where the original Mac run saved 7.645866162420134e-10. The difference slightly exceeds the general absolute tolerance. The field-specific bound preserves the original accuracy requirement.

The sixth diagnostic is exactly `robustness/results.json.aest_current.maximum_absolute_component_error`. It compares the analytic scalar-action derivative with centered differences at step 1e-5 over sixteen seeded points. Both saved and regenerated errors must be finite, nonnegative and strictly below the native 1e-7 bound. Linux produced 5.862759167030163e-10 versus the saved Mac 5.410445425013677e-10. These are derivative-check errors, not predictions about AeST viability.

`test_check.py` checks both observed platform differences, rejects every diagnostic at or above its original bound, rejects Boolean or null diagnostic substitutions on either side, and rejects unrelated changed outputs. Boolean outputs also reject integer substitutions. CI runs these negative controls before regeneration. Saved scientific values and probe assertions are unchanged.

The relations script also offers its original stricter `--check` comparison with absolute tolerance 1e-12. Robustness retains its own `--check` comparison with relative tolerance 1e-9 and a unit absolute floor.

The saved JSON artifacts retain the original run's version labels. The original absolute interpreter path is replaced by `python3`. Historical input paths are replaced by bundle-relative paths. These are metadata changes. The scales and robustness formulas, constants, seeded inputs, assertions and saved numerical values are unchanged.

The exact wave10 source, its wave7 import dependency and the wave10 certificate are bundled with digests. Their bytes match gravity commit `d8c7544e89388720fc1c13de816ddb7dd03d2096`. The certificate supplies the robustness collapse-dispersion column, which remains explicitly identified as reused. The manifest prevents a changed historical input from silently passing the check.

The scoped GitHub Actions workflow runs only for bundle or workflow changes. Hosted CI results are separate evidence from this local check. No downloaded papers, extracted paper text, HTML reading copies, rendered page images, private coordination files or local operations snapshots are included.

## Audit of all nine numerical outputs

Only the six exact paths above have special bounds. The full output audit retained the general comparison policy for every other field:

| Route | Error and residual fields reviewed | Comparison decision |
| --- | --- | --- |
| Evidence | Posterior error variances, seeded Monte Carlo error estimates, graph cycle residuals | Scientific model outputs stay strict, including the deliberately wrong line assignment. |
| Hidden dynamics | RK4 and Volterra error curves, step-halving ratios, closure approximation errors, coordinate and swap defects | Error curves and convergence rates are results. Native finest-step bounds and convergence assertions still run. |
| Issue 5 | Symbolic equation and Burgers residuals | Exact strings remain exact. |
| Persistence | Four RK4 relative errors, about 8e-14 to 1e-12 | General absolute floor suffices. Native errors must remain below 1e-8. |
| Relations | Channel, fragment and emission checks | Scientific matrices and rates stay strict. Native analytic assertions still run. |
| Repetition | Seven maximum squared-bar-length errors, at most 9e-16 | General absolute floor suffices. Native maximum must remain below 1e-12. |
| Robustness | Five Hessian residuals, one derivative error, channel matrix-unit residual | Only the six identified finite differences use native bounds. The channel residual stays strict and must be below 1e-13 natively. |
| Scales | Model curves and sensitivity calculations | Scientific values stay strict. No finite-difference diagnostic exception. |
| Unclaimed | Geometry reconstruction residuals, analytic Hessian, two step-halving trace differences | Values stay strict. Trace differences are about 4e-12 and 2e-13, with a native bound below 1e-9. Floquet traces, multipliers and stability results stay strict. |

No reference artifact was edited during this audit. A changed error curve, variance, spectrum, stability classification, derivative formula, structure or result status remains a check failure under the existing policy.
