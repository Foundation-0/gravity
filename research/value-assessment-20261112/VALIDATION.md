# Validation record

Prepared on 12 November 2026. Publication preparation used Python 3.14 with NumPy 2.5.4 and SciPy 1.18.1 already present in the environment. No installed runtime was changed.

- The runner checks all six historical SHA-256 digests before executing any source input.
- The Wave 12 loader independently checks each executed source digest.
- Seven comparator and integrity controls pass. They cover a scientific-result change, a boolean change, malformed structure, nonfinite output, excessive roundoff residual, changed source, and loss of a small scientific signal.
- All four probes, including the 26-assertion synthetic observation design, regenerate successfully. Their scientific results match saved outputs under the documented tolerances.

The focused CI workflow reproduces this bundle. The separate broad Lean build has existing Wave 5/6/7 errors. Hosted CI status must be read from the current pull request and is not implied by these local results.

The historical Wave 12 proof is retained under `inputs/` as evidence of the audit. The corrected direct Lean check and its build limits are recorded in [the scoped correction](https://github.com/Foundation-0/gravity/pull/10). The immutable historical inputs do not incorporate that correction.

The optional independent reviewer checks also reproduce with SymPy 1.14.0. Their scientific output matches the saved review result. Their historical author-artifact hashes are retained separately from the current publication manifest.

A second independent scientific review passes the closure and observation design at the stated scope. Its source hashes and saved independent checks are preserved in `second-review.md` and `second-review-checks.json`.

The second reviewer script was rerun in a temporary copy with SymPy 1.14.0. Its independent scientific checks and temporary author replays reproduce the saved results. Historical artifact hashes are retained separately from the final publication hashes.

The first Ubuntu replay passed Wave 12 and closure, then exposed platform variation in the finite-length energy-Hessian diagnostic: 3.1972696962664237e-7 versus the saved 3.197457694573648e-7.

The runner checks those three diagnostics against the author probe's original 1e-4 bound. A regression test retains the observed pair and rejects a value above the bound. Other scientific quantities retain the strict comparison.
