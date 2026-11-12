# Acceleration evolution: evidence and continuity

Capability ID: `gravity.acceleration-evolution`. Purpose: distinguish a constant galactic acceleration scale from a scale tied to cosmic expansion using reproducible predictions and appropriately qualified observations. The purpose survives changes to implementation paths.

Human direction: investigate the relation, develop a testable model, check existing observations, and connect gravity, fractals, physics0 and astr0. The added annihilation idea is retained as a separate hypothesis. It has not been used as a premise for the acceleration model.

## Responsibilities and interfaces

| Project | Responsibility | Interface |
| --- | --- | --- |
| gravity | Model, source transcription, calculations, scientific limits | This directory is the canonical source |
| fractals | Distinguish scaling from resemblance and bound its domain | Companion note links to the canonical study |
| physics0 | Assumptions, established mechanisms and falsification | Companion note links to the model and inference protocol |
| astr0 | Observables, calibration, selection and covariance | Companion note links to the evidence input contract |

Current implementation: `model.py`, `compare.py`, `evidence.json`, `results.json`, `comparison.json` and `plot.py`. The annihilation conjecture has its own note and no derived interface to a₀(z).

## Evidence state

- Source reviewed: primary MUSE-DARK III author manuscript, published KMOS3D and Puech summaries, and the prior H-tracking reanalysis abstract. Sources and exact locations are in `evidence.json`.
- Local numerical checks: thirteen tests pass, including analytic limits, platform-rounding tolerance and stale-artifact rejection. Deterministic prediction and comparison checks pass. See `VALIDATION.md` for the baseline regression limit.
- Scientific status: published-summary diagnostic only. No observational likelihood, new fitted exponent, calibrated model-selection score or detection significance.
- Raw-data status: selected MUSE radial data and covariance not recovered. The public release server timed out. The full KMOS3D table was not recovered and its indexed schema lacks measurement errors.
- Review status: separate source/code and cross-repository documentation reviews found no actionable issues in the inspected snapshot. Final tolerance change awaiting confirmation. Human review pending. No merge or deployment claimed.

## Peer responses and composition

Research agents supplied separate observational and annihilation reviews. The observational response identified the 95% interval convention, shared-sample dependence and the lack of an effective redshift for the whole-sample fit. These findings changed the implementation from a proposed bin likelihood to an explicitly non-statistical central-curve comparison.

The numerical agent implemented prediction functions separately from the evidence transcription. A non-author source/code reviewer checked the primary equations, model, comparison and figure. A separate reviewer checked the companion documents and composed links. Both found no actionable issues in their scopes. These are agent review records, not human scientific peer review.

## Retained lesson and next action

An apparent match to H(z) depends on the reconstruction and amplitude treatment. Do not convert summary curves, broad-sample estimates or differently defined Tully–Fisher intercepts into independent precise measurements. Confidence-level conventions and galaxy-level covariance are part of the scientific input.

Next action: recover the selected MUSE measurements and modelling posteriors from the documented release, verify membership and uncertainty definitions, then follow `INFERENCE.md`. A successful numerical test establishes arithmetic and reproducibility only. Update the companion notes when the canonical evidence state changes.
