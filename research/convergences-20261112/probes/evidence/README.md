# Evidence joins: reproducible synthetic probes

These calculations show three ways measurements can help each other, and the limits of each. They contain no new astronomical observations and do not validate a repository candidate.

Run with Python 3, using only its standard library:

```sh
python3 research/convergences-20261112/probes/evidence/evidence_join.py
```

The script writes `results.json` beside itself. It performs analytical consistency checks and checks the Gaussian posterior calculations against 100,000 seeded simulations. Seed: 20261112.

1. **A control that measures the error.** The target measurement is `y = q + b + e`, with independent unit-variance Gaussian signal `q` and calibration offset `b`. Readout noise `e` has variance 0.01. A reference channel `x = b + eta` measures the same offset with noise variance 0.01. The control alone has zero information about `q`, but it helps separate `q` from `b` when paired with `y`. Repeated observations share one offset unless the case explicitly says otherwise.
2. **Which eclipse period survives?** Two invented event times allow six discrete periods. An archival event leaves two. A measurement where those two periods disagree can resolve them, depending on its detection completeness. A measurement at a phase they share adds no information about this particular ambiguity. The likelihood assumes fixed eclipse shape, exact event times, no false alarms, known completeness and a uniform prior over the displayed aliases.
3. **A cycle of energy differences.** A four-level difference graph has a consistency check. An incorrectly assigned line breaks it. Multiplying every measured line by the same calibration factor preserves it. This is an algebraic example with alternating possible parities, not a validated atomic transition system.

The Gaussian calculation assumes the measurement equations and distributions are known. It does not test the nonlinear ICA identifiability theorem, whose unknown mixing functions and diversity conditions pose a different problem. The nominal interval coverage calculation averages over repeated draws of both the signal and the calibration offset from the stated prior.

The control-leakage cases distinguish two operations. The `known_model_posterior_variance` correctly includes signal leakage into the reference channel. The `blind_regression_signal_response` shows how much target signal remains if that reference is instead treated as signal-free and regressed out. These are different estimators.
