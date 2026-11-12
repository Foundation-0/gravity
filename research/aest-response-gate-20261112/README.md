# AeST constraint and response benchmark

This benchmark constructs physical scalar perturbations of one specified AeST action. On an expanding background, states with the same initial density, momentum and metric produce different pressure and later gravitational potentials. A flat-space control explains why the same field freedom has no linear gravitational response at zero background density.

**Status:** action-derived calculation checked by a separate Astra agent using an independently reduced ADM action. [The review](independent-review/REVIEW.md) found no blocking error. This is internal project review, not external peer review or a nonlinear collapse, thermalization or observational result.

The complete action, conventions, constraints and equations are in [derivation.md](derivation.md). The test choices and the approximation threshold are in [protocol.md](protocol.md). The equations build on published AeST work listed in [sources.json](sources.json). No new propagating mode or new Minkowski stability bound is claimed.

## What was calculated

The full function is \(\mathcal F=(2-K_B)\lambda_s\mathcal Y-2\mathcal K_2(\mathcal Q-Q_0)^2\), with \(K_B=1\), \(\lambda_s=1\), and \(\mathcal K_2=2\). The expanding background has \(Q=Q_0+0.01Q_0a^{-3}\), no matter and no cosmological constant. Evolution covers \(a=1\) to \(a=2\).

For five wave numbers \(k/Q_0=6,9,12,18,24\), three preparations were evolved. One changes scalar and vector velocities while compensating their initial density source. A second changes the field phase while also matching initial pressure. The third is a held-out linear mixture of the first two.

All three initially match effective density and momentum. They satisfy the lapse, momentum and unit-vector constraints. The scalar auxiliary field changes consistently. Gauge-invariant field data distinguish the preparations.

The first preparation has \(\Delta\gamma_i=\epsilon Q_0\), \(\epsilon=10^{-6}\). Define \(D=8\pi\widetilde G\delta\rho\), \(m=K'\varphi\) and \(p=8\pi\widetilde G\delta P\). Their units are \(Q_0^2,Q_0,Q_0^2\), respectively. Maximum responses over the interval are:

| \(k/Q_0\) | \(\max|D|/(\epsilon Q_0^2)\) | \(\max|m|/(\epsilon Q_0)\) | \(\max|p|/(\epsilon Q_0^2)\) | \(\max|\Phi+\Psi|/\epsilon\) |
|---:|---:|---:|---:|---:|
| 6 | 0.099124 | 0.0077392 | 0.040067 | 0.0043004 |
| 9 | 0.103737 | 0.0052054 | 0.040031 | 0.0019747 |
| 12 | 0.105312 | 0.0039056 | 0.040005 | 0.0011240 |
| 18 | 0.106352 | 0.0025971 | 0.040000 | 0.0005040 |
| 24 | 0.106641 | 0.0019431 | 0.040000 | 0.0002844 |

These are transfer amplitudes for the declared preparation. They are not predictions for an astrophysical perturbation spectrum. The metric sum is the potential combination entering weak gravitational lensing, not an integrated light-ray observable.

The second preparation has \(D_i=m_i=p_i=0\), but a nonzero pressure derivative. At \(k/Q_0=12\), it reaches \(\max|D|/(\epsilon Q_0^2)=0.527669\) and \(\max|\Phi+\Psi|/\epsilon=0.00903245\). Its field-phase amplitude is \(\chi_i=\epsilon Q_0/\sqrt{3k^2/4+2Q_0^2}\).

Thus density and momentum do not predict every allowed preparation. Adding instantaneous pressure still leaves an independent preparation that changes its future derivative. The four-state variables \((D,m,\chi,Z)\), where \(Z=E+\chi\) for this branch, supply an exact linear evolution law.

## Checks and limits

| Check | Result |
|---|---|
| Action lapse equation and canonical compensation | Symbolic residual zero |
| Constraint propagation | \(\dot C+3HC=0\), symbolically |
| Effective energy balance and spatial Einstein equation | Symbolic residual zero |
| Fifteen expanding preparations | Largest normalized constraint residual \(5.20\times10^{-12}\) |
| Five-field versus four-state evolution | Largest normalized difference \(5.49\times10^{-11}\) |
| Integrator tolerance \(10^{-8},10^{-10},10^{-12}\) | Constraint residual falls from \(2.82\times10^{-10}\) to \(2.86\times10^{-14}\) |
| Amplitudes \(10^{-7},10^{-6},10^{-5}\) | Normalized response agrees within recorded numerical error |
| Flat-space exact matrix exponential versus ODE | Relative error below \(1.6\times10^{-10}\) over ten periods |
| Flat-space quadratic energy | Relative drift below \(1.3\times10^{-12}\) |

The exact expanding solution for \(a(t)\) is checked independently. The scalar kinetic Hessian and short-wavelength characteristic have the required positive signs in the author derivation. 

The separate review reproduces the scalar kinetic Hessian and integrates the ADM equations, matching eight reconstructed observables to 1.06e-12 normalized error. The test does not prove nonlinear stability or stability of an observationally fitted cosmology.

For \(q_i=0\), the compensated field mode oscillates but its linear density, momentum, pressure and metric response vanish identically. The scalar shift current remains nonzero. It must not be identified with stress-energy momentum.

At a fixed duration \(Q_0t=1\), reducing the initial density gives the following velocity-preparation response at \(k/Q_0=6\):

| \(q_i/Q_0\) | \(\max|D|/(\epsilon Q_0^2)\) | \(\max|\delta\rho/\bar\rho|/\epsilon\) | \(\max|\Phi+\Psi|/\epsilon\) |
|---:|---:|---:|---:|
| 0.01 | 0.0991240 | 3.05744 | 0.00316730 |
| 0.001 | 0.0119935 | 3.21476 | 0.000349006 |
| 0.0001 | 0.00127788 | 3.26705 | 0.0000360307 |
| 0.00001 | 0.000130421 | 3.28381 | 0.00000364003 |

Absolute sources tend to zero. The density-contrast response stays finite because its background denominator also tends to zero. A claim that small background sound speed suppresses preparation effects must state which field amplitudes and which observable normalization are held fixed.

## A bounded approximation test

Two unfitted prescriptions were tested: zero pressure perturbation and \(\delta P=c_{\rm ad}^2\delta\rho\). Both keep the exact expanding background. Initial density contrast is \(10^{-5}\), with the explicitly defined dust-inspired momentum in the protocol. This is not an exact AeST growing eigenmode.

Independent hidden velocity and phase data have relative amplitudes \(\eta=0,0.01,0.1,1\). Each comparison uses the same initial retained density and momentum. The 1% target for density contrast and metric potential was fixed before evaluating the approximations. Errors are divided by the maximum corresponding observable in the zero-pressure reference over \(1\leq a\leq2\).

| Hidden amplitude \(\eta\) | Distinct preparations | Worst density error, zero pressure | Worst metric error, zero pressure | Worst density error, adiabatic pressure | Worst metric error, adiabatic pressure |
|---:|---:|---:|---:|---:|---:|
| 0 | 5 | 28.67% | 28.67% | 127.97% | 184.67% |
| 0.01 | 10 | 37.41% | 43.79% | 188.18% | 216.20% |
| 0.1 | 10 | 627.24% | 627.39% | 765.66% | 785.69% |
| 1 | 10 | 6530.40% | 6531.65% | 6668.82% | 6670.95% |

Neither prescription passes the declared 1% criterion for any of these 35 preparations. Large percentages compare small linear perturbations. They do not imply nonlinear amplitudes or a failure of all dust approximations. A different action, a colder background or a verified slow-mode initial ensemble requires its own test.

## Reproduce

Create an isolated Python environment, install [requirements.txt](requirements.txt), and run:

```sh
python response.py --output results.json
```

The [script](response.py) includes assertions. The [results](results.json) retain all preparation values, residuals, amplitude controls and approximation errors. No network request, downloaded dataset, fitting stage or graphical dependency is needed.

The bounded result supports retaining the additional scalar/vector response data before a nonlinear solver is attempted. The next bounded test selects a slow initial mode and measures sensitivity to fast-mode contamination. A three-dimensional collapse experiment remains unstarted.

The derivation is retained byte-for-byte at its reviewed hash, including its original pre-review status. The review linked above supersedes that status. Run `python independent-review/adm_check.py` for the separate action reduction and comparison.
