# Slow-mode preparation and controlled fast-mode contamination

This test asks whether a two-variable approximation improves when the same AeST action is prepared near its growing slow mode. It retains the existing background, constants, interval and 1% accuracy criterion. It adds no fitted coefficient or cosmological data.

Protocol fixed before evaluating approximation errors, 12 November 2026. Source action and equations: the independently checked checkpoint with `response.py` SHA256 `e28c8f4ada1e41924e6317f8932de4d065307516cd57c5ff83a0cf23b72397ef`.

## Fixed state and mode selection

Set Q0=1, K_B=1, K2=2, lambda_s=1, q_i=0.01, a_i=1 and a_f=2. Test k/Q0=6,9,12,18,24. Use the four coordinates `X=(delta,theta,chi,Z)`, where `delta=D/R`, `theta=m/(QK')`, and Q0 supplies the units. The change of background normalization is included in their evolution matrix M(a).

At a=1, identify the fast complex-conjugate eigenpair of M. The two remaining eigenvalues must be real to numerical tolerance. Choose the larger real eigenvalue as the instantaneous growing slow mode and normalize its density component to one. Set its amplitude to delta_i=1e-5. If this spectral structure fails, report that failure instead of changing the selection rule.

Follow all four eigenvalues from a=1 to a=2 on 201 equally spaced scale factors. Match neighbouring eigenvalues by minimum total distance and check that the real slow pair stays separated from the fast pair. Record the smallest fast/slow spectral gap divided by H, the largest slow rate divided by fast frequency, and the fast-frequency adiabatic ratio `|omega_dot|/omega^2`.

Eigenvectors also change with time. In the fixed declared coordinate units, normalize each to unit Euclidean norm, align its phase between adjacent points, and record fast/slow mixing from `V^(-1) Vdot` divided by the associated spectral gap. Record the eigenvector condition number. These finite diagnostics qualify the word slow. They are not an invariant-manifold proof.

## Preserve the retained initial data

Let S contain the two slow eigenvectors at a=1. Normalize the fast complex vector f so its density component is one and real. For phases 0, pi/2, pi and 3pi/2, take `g=Re(exp(i*phase)*f)`. Subtract the unique slow combination matching g's initial density and momentum:

```text
w = g - S * inverse(S[delta,theta]) * g[delta,theta].
```

Then w has zero retained density and momentum and a prescribed fast spectral component. The prepared state is `delta_i*(slow_growing + eta*w)`, with eta=0,0.001,0.01,0.1. Eta=0 is counted once per wave number. The amplitude eta refers to the fast component's initial density oscillation envelope before its compensating slow contribution. It is not a probability or a fraction of energy.

There are 65 distinct preparations. Each exact run and both approximate runs start with the same retained density and momentum. This compares sensitivity to extra field information without changing the approximation's visible initial state.

## Comparison and controls

Evolve the full time-dependent four-state system from a=1 to a=2. Compare the zero-pressure and adiabatic-pressure prescriptions already tested. Normalize density-contrast and lensing-sum errors by each observable's maximum in the zero-pressure reference. Both errors must stay below 1% to pass. No mode is reselected or projected away during evolution.

Use a 2001-point scale-factor grid and a fundamental solution matrix to evaluate all linear preparations. Compare its baseline with direct state integration. Repeat the fundamental integration at tighter tolerances and use 4001 output points for the error maxima. Retain maximum absolute field and metric amplitudes so that large percentages can be distinguished from nonlinear excursions.

An instantaneous growing eigenvector is not an exact time-dependent growing solution. A passing result would support only this specified initial ensemble and leakage interval. A failure would not rule out a more accurate slow preparation, a colder background or a different observationally chosen spectrum.
