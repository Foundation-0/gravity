# Validation record

Checked 12 November 2026 with Python 3.14.6 on macOS. Numerical runtime has no external dependencies. Plot rendering used Matplotlib 3.11.2 in an isolated environment. The figure was visually inspected for labels, source boundaries and the absence of implied confidence bands.

## New study

| Check | Result |
| --- | --- |
| Unit tests discovered in this directory | 13 passed |
| Prediction artifact `--check` | Passed |
| Source-bound comparison `--check` | Passed |
| Relative and composed cross-repository links | Resolved against the four local branch trees |
| Prose check on the scientific/companion documents | Passed |
| Independent scientific source/code review | Approved scientific candidate 83809b8, including the final tolerance change |
| Independent companion-document review | No actionable findings in the inspected snapshot |

The checks validate computation and the stated evidence boundaries. They do not establish that H tracking is true or validate the original galaxy measurements. The workflow runs the numerical checks on Python 3.12 and 3.14. Hosted results are separate from the local record.

## Existing repository checks

Seven existing generators passed their `--check` mode: `verify_all.py`, Waves 3, 5, 6, 7, 9 and 10. Wave 4 failed with `Canonical SHA-256 mismatch on disk`.

The Wave 4 failure was confirmed in baseline commit `7f388db49ca8a8f37b9140704391de0eb3968aed` and persists unchanged after the documentation-only main update to `cb0de90`. Its `results/wave4_unified_certificates.json` lacks the `sha256_canonical` field required by the verifier. The file in this branch is byte-identical to that baseline blob. No existing certificate or generator was changed by this study.

This is a pre-existing reproducibility issue for that certificate. Passing the new study's tests does not make the whole repository's verification suite pass. Repair and independent regeneration of the Wave 4 certificate remain outside this contribution.

## Review scope

The source/code reviewer checked Ciocan Eq. 2, Eq. 4 and Eq. 14, error coverage, sample dependence, model equations, units, BTFR signs, the comparison and figure. The companion reviewer checked epistemic status, inference assumptions and links. The latter did not independently review its own annihilation note or the numerical code.

No human scientific review, full galaxy-data reanalysis, merge or deployment is claimed. The next empirical step remains recovery of the selected measurements and their uncertainty products.
