# Independent review of the slow-subspace continuation

**Disposition: no blocking scientific or implementation issue found in the frozen checkpoint.** The original five-field equations reproduce the submitted four-state evolution for all 65 preparations. Both specified pressure closures fail the declared 1% criterion throughout this ensemble. The result concerns the declared action, background, initial-state prescription and finite interval.

Reviewed on 12 November 2026 by gpt-forge, using a separate gpt-6-astra review agent from the continuation's author. This reviewer authored the earlier field-response implementation, which had already passed a separate ADM derivation review. This review is independent of the new preparation and closure calculation. It is not a second independent derivation of the underlying action.

The frozen `probe.py` SHA256 is `af9d4443c45298d723384ad0283bb8a635944fe347fd2067e3f4699ea94b2151`. The accompanying protocol, results and evidence hashes are recorded in [evidence.json](evidence.json). The source checkpoint remained unchanged during review.

## Background normalization and physical evolution

The reviewed coordinates are `delta=D/R` and `theta=m/W`, where `W=Q K'`. The exact background identities are

```text
Rdot = -3 H W,
Wdot = -3 H W (1+c_a^2),
c_a^2 = K'/(4 Q).
```

Applying the quotient rule to the original density and momentum equations gives

```text
deltadot = 3 H (w delta-p/R) + 3(W/R) Phidot - r(W/R) theta,
thetadot = 3 H c_a^2 theta + p/W + Phi.
```

Thus the time-dependent normalization terms in the submitted generator are required and have the stated signs. [check.py](check.py) constructs this transformation symbolically. Its matrix agrees with the submitted generator to a maximum absolute discrepancy of 1.14e-13 over the checked scales and wave numbers.

The numerical comparator integrates the original five-field equations for `(v,alpha,E,Phi,gamma)`. It reconstructs the retained observables after integration and does not eliminate the density constraint during that evolution. Both approximate pressure laws are separately integrated in the unnormalized `(D,m)` variables. The comparison covers every submitted preparation on the same 2001-point scale-factor grid.

The largest full-state discrepancy, divided by the initial density contrast, is 1.27e-12. The largest independent constraint residual, divided by the initial scaled density amplitude, is 8.04e-13. The largest discrepancy in any reported closure-error fraction is 1.86e-11. Every one of the 130 preparation/closure comparisons independently fails 1%.

## Initial-state and mixing checks

Independent diagonalization confirms two complex conjugate pairs at the initial time for all five wave numbers. The retained failed real-growing-mode protocol is consistent with that spectrum. The replacement protocol explicitly selects a real two-dimensional slow spectral subspace and makes no claim to identify a physical growing solution.

The selected baseline has fast spectral-coordinate norm below 1.66e-16 per unit initial density contrast in an independently computed eigenbasis. All compensating leakage states preserve the initial density and momentum. The maximum mismatch is 2.65e-23. The initial metric is then also the same by the constraint.

The compensation adds a slow contribution as declared. The complete added state is not called a pure fast eigenmode. The leakage parameter specifies a fast-component density envelope before compensation and does not measure energy.

The eigenvector-motion diagnostic was checked without finite differences of eigenvectors. Differentiating `M v_j=lambda_j v_j` gives, for unequal eigenvalues,

```text
(V^-1 Vdot)_ij = (V^-1 Mdot V)_ij / (lambda_j-lambda_i).
```

An analytic derivative of the independently transformed generator reproduces the reported mixing directions and magnitudes. The largest slow-to-fast ratio is 0.000152426. The largest fast-to-slow ratio is 0.740564. The finite-difference estimates are 0.000152418 and 0.740570.

The large reverse ratio does not support attributing the baseline closure error to substantial generation of fast coordinates by the slow basis.

These ratios use the declared coordinate units and unit Euclidean eigenvector normalization. A time-dependent change of state variables changes the frozen generator. Neither its instantaneous slow subspace nor these mixing ratios define a unique coordinate-independent invariant manifold. The submitted report states this limit.

## Interpretation and stopping point

The baseline zero-pressure errors of 24.6% to 27.4% are supported. They show that choosing this initial slow spectral subspace does not make the two tested closures accurate on this interval. Small amplitudes and the independent constraint check support interpreting the reported differences within linear theory.

This is a negative result for two specified closure laws and a reproducible preparation ensemble. It does not exclude a different invariant slow construction, another background or an observationally motivated initial spectrum. It adds no general cosmological failure claim and supplies no reason to launch nonlinear collapse simulations.

The finite calculation and its review are complete. Further physical claims require a new stated input.

Run `python3 independent-review/check.py` from the slow-mode directory with the checkpoint's NumPy, SciPy and SymPy dependencies. The script writes only its own `independent-review/evidence.json` and verifies the author's hashes before and after the calculation.
