# Slow initial data do not rescue these two closures

Selecting the initial slow spectral subspace does not bring the zero-pressure or adiabatic-pressure prescription within 1% accuracy for this fixed AeST benchmark. With no initial fast component, the zero-pressure errors remain 24.6% to 27.4%. This is a result for one action, background, coordinate convention and finite interval.

Status: finite calculation, independent review pending. The underlying action and four-state response passed a separate ADM review. That review does not automatically verify this added preparation test. No observational or general cold-dark-matter failure is claimed.

## The first selection rule failed

The original [growing-mode protocol](GROWING-MODE-PROTOCOL.md) required one fast conjugate pair and two real slow eigenvalues. At a=1, every tested wave number instead has two conjugate pairs. The slow pair has frequency 0.07694 to 0.08850 in Q0 units, while the fast frequency is 5.39289 to 20.83462. [selection-failure.json](selection-failure.json) retains this result.

No closure error was evaluated under that failed rule. The separately declared [continuation protocol](PROTOCOL.md) uses the two-dimensional slow spectral subspace. Its unique real initial state matches the original dust-inspired density and momentum. It is not called an instantaneous growing mode.

Both calculations use Q0=1, K_B=1, lambda_s=1, K2=2, q_i=0.01 and a=1 to a=2. No constant, background or approximation coefficient was fitted after inspecting errors.

## The controlled comparison

The state is `(delta,theta,chi,Z)`, with `delta=D/R` and `theta=m/(QK')`. The evolution matrix includes derivatives of those background normalizations. The initial density contrast is 1e-5 and theta is `-H_i*delta_i/k^2`.

The two slow eigenvectors determine chi and Z at that fixed retained state. The full time-dependent equations then evolve freely. There is no later projection, reselection or suppression of a mode. The two approximate laws begin with the same retained state and keep the exact background.

Errors are maxima over the interval, divided by the maximum corresponding observable in the zero-pressure reference. The declared pass threshold is 1% for both density contrast and the metric-potential sum.

| k/Q0 | Zero-pressure density error | Zero-pressure metric error | Adiabatic-pressure density error | Adiabatic-pressure metric error |
|---:|---:|---:|---:|---:|
| 6 | 24.603% | 24.576% | 117.584% | 117.568% |
| 9 | 26.193% | 26.180% | 129.154% | 151.239% |
| 12 | 26.806% | 26.798% | 120.441% | 166.308% |
| 18 | 27.263% | 27.259% | 112.881% | 179.572% |
| 24 | 27.427% | 27.425% | 129.110% | 185.409% |

Removing the initial fast spectral component reduces the previous worst zero-pressure error from about 28.7% to 27.4%. It does not meet the stated accuracy target. An instantaneous spectral subspace still differs from an invariant subspace of the evolving equations.

## Sensitivity to unobserved initial data

Four phases of a fast component were added at each nonzero leakage amplitude eta. A compensating slow component preserves the initial density and momentum. Eta is the fast component's density-oscillation envelope relative to the baseline initial density before compensation. It is not an energy fraction.

| eta | Distinct preparations | Worst zero-pressure error in either observable | Worst adiabatic-pressure error |
|---:|---:|---:|---:|
| 0 | 5 | 27.43% | 185.41% |
| 0.001 | 20 | 32.48% | 187.84% |
| 0.01 | 20 | 78.00% | 209.71% |
| 0.1 | 20 | 533.23% | 638.80% |

All 65 preparations fail the 1% criterion for both prescriptions. The largest exact density contrast is 0.0001165 and the largest metric-potential sum is 2.36e-8. Large error percentages therefore compare small linear perturbations.

## What the slow label establishes

The fast and slow spectral subspaces remain separated on the 201-point diagnostic grid. Their smallest separation ranges from 45.9H to 179.2H across the tested wave numbers. The maximum slow-rate to fast-frequency ratio is 0.0143.

Eigenvectors also change and the matrix is not normal. In the declared coordinate norm, the largest fast/slow eigenvector-mixing ratio is 0.741 at k/Q0=6 and 0.0270 at k/Q0=24. 
The large mixing value is from fast into slow coordinates. The reverse ratio, which describes forcing of fast coordinates by a slow basis, is at most 0.000153 on these grids. The evidence records both directions, the eigenvector condition numbers and the frequency-variation ratio. A large spectral gap alone does not prove adiabatic decoupling.

The frozen-generator spectrum depends on the declared time-dependent state coordinates. These results identify a reproducible initial ensemble. They do not define a unique physical growing solution, prove that every slow preparation fails, or constrain an observational perturbation spectrum.

## Checks and remaining limit

[probe.py](probe.py) evolves a fundamental solution matrix and compares its baseline with direct state integration. A second calculation at k/Q0=12 tightens tolerance and doubles the output grid to 4001 points. The maximum change in reported error fraction is 4.17e-6. The direct and fundamental solutions agree below 1e-7 after division by the initial density amplitude.

[evidence.json](evidence.json) records every preparation, the spectral diagnostics, the amplitude bounds and the numerical controls. Run `python3 probe.py` with NumPy and SciPy to reproduce it. Run `python3 selection_failure.py` to reproduce the failed real-eigenvalue gate.

This test closes the stated same-action preparation question with a negative result for these two closures. Choosing a different cosmology, a physically motivated initial spectrum or an exact invariant slow construction requires an additional assumption. None is supplied by these calculations.
