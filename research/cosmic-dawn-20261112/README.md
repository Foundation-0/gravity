# Cosmic dawn: a quasar pair and a collapse-scale audit

This research note separates a new quasar observation from what the repository's Wave 10 calculation predicts. It includes a reproducible numerical probe and a proposed test for a separate question about extra dimensions.

**Status:** research audit, not a new theory or an observational validation. Research: gpt-forge, three agents using gpt-6-astra at ultra reasoning. Publication preparation: gpt-6.1-sol. Human review pending.

## What the observation establishes

[Onorato et al.](https://arxiv.org/html/2609.31835v1) report a physical quasar-pair candidate at redshifts 6.0781 and 6.0785, with a projected separation of 5.56 kpc. Lensing is not excluded. The paper appeared in *The Astrophysical Journal Letters*, 1011, L59, on November 10, 2026 ([DOI](https://doi.org/10.3847/2041-8213/aeb11f)).

The estimated black hole masses are 1.53 billion and 399 million solar masses. These are virial estimates, with systematic uncertainty of about 0.3 dex, or roughly a factor of two. They are not seed masses measured at formation.

One companion was found in 199 fields. The inferred small-scale clustering exceeds extrapolated large-scale fits by about 100 to 1,000 times. Section III.4 explicitly warns that such extrapolation is unreliable where both objects occupy one halo. One pair is not a definitive test of LambdaCDM, the standard cosmological model with a cosmological constant and cold dark matter.

The result motivates better population models and more observations. It does not quantitatively reject standard hierarchical growth or light black hole seeds. This note makes no inference of an 83,900-solar-mass seed.

## What Wave 10 actually computes

The audited source is [Wave 10 at commit 8f904ba](https://github.com/Foundation-0/gravity/blob/8f904ba3aad22ce727e92b96bf0c12e229173f8f/wave10_covariant_jeans_unification.py). Its file is unchanged from publication commit `02013ae95fa5913894b829c8e2e63a3efcde9e63`.

Lines 29–45 set cosmological inputs. Lines 111–165 build the spectrum and growth function. Lines 173–198 compute the collapse scale. Lines 219–233 apply the trapping prescription. Lines 288–300 make a group forecast.

The calculation solves `sigma_linear(R,0) D(z) = 1.686`. It assigns the total halo mass `M_star = (4 pi/3) rho_mean R^3`, then defines a virial radius at 200 times critical density and `sigma_star = sqrt(G M_star/(2 R200))`. This halo mass is not a black hole seed mass.

The assumed law `f_trap = max(0, 1 - (sigma_star/sigma_halo)^2)` describes a model fraction. It is not an event-horizon condition. The spectrum uses an Eisenstein–Hu cold dark matter approximation normalized to Planck parameters. Consequently this computation is not an independent prediction that rejects LambdaCDM. “No newly fitted shape parameter” does not mean no assumptions.

## Reproduced values and a numerical limit

The following fractions use illustrative halo dispersions. The halo dispersion used in the original quoted calculation is unknown.

| Spectrum grid | z | Total halo mass, solar masses | sigma_star, km/s | f_trap at 150 km/s | f_trap at 200 km/s |
|---|---:|---:|---:|---:|---:|
| Native: kmax 300, 1,600 steps | 0 | 6.2405 × 10^12 | 185.588 | 0 | 0.138926 |
| Native | 6.08 | 57,809 | 0.856435 | 0.999967401 | 0.999981663 |
| Extended: kmax 100,000, 12,800 steps | 6.08 | 81,907 | 0.961912 | 0.999958877 | 0.999976868 |

Wavenumbers are in inverse Mpc. Extending the high-wavenumber limit raises the mass by about 42% relative to the native result. The native result is about 29% below the extended result. The extended compactness `2GM/(R200 c^2)` is only `4.12e-11`, far from the Schwarzschild horizon value of one.

The native redshift grid ends at 5. This probe extends it explicitly to 6.08 and 7. At z = 7 the native radius bracket contains no root. The existing solver does not check that bracket and can return a boundary instead. The probe reports `no_root_in_bracket` and leaves Wave 10 unchanged.

At fixed cutoff 300, refining from 1,600 to 12,800 steps changes the z = 6.08 mass from 57,808.97 to 57,807.88 solar masses, about 0.0019%. This separates the larger cutoff effect from quadrature resolution.

The 10,000 and 100,000 cutoffs test numerical convergence under the same spectrum and growth assumptions. Numerical convergence does not validate nonlinear AeST physics or a black hole formation mechanism.

Run from the repository root with Python 3 and its standard library:

```sh
python3 -B research/cosmic-dawn-20261112/audit.py
python3 -B research/cosmic-dawn-20261112/audit.py --check
```

The probe checks the source hash, extracts constants and the spectrum factory through Python's syntax tree, and changes only two checked literals in memory. It never runs the catalogue or the root script's main function.

The native literals preserve the original spectrum arithmetic. `results.json` records inputs, assumptions, roots and failed brackets. `--check` regenerates in memory and checks all saved values and statuses with relative numerical tolerance `1e-9` and absolute tolerance `1e-14`.

## Does falling into a black hole require a fifth dimension?

Intrinsic curvature does not require an ambient dimension. A funnel picture embeds a two-dimensional spatial slice for visualization. It is not evidence that four-dimensional spacetime bends into a physical fifth dimension.

In four-dimensional general relativity, a falling clock crosses a regular horizon in finite proper time. See the [MIT relativity lectures](https://ocw.mit.edu/courses/8-033-introduction-to-relativity-and-spacetime-physics-fall-2024/mit8_033_f24_lec_full.pdf) and [Cambridge general relativity notes](https://www.damtp.cam.ac.uk/user/us248/Lectures/Notes/gwnr.pdf).

A concrete alternative exists: [Randall–Sundrum II brane black holes](https://arxiv.org/abs/1105.2558) can behave four-dimensionally at low curvature and five-dimensionally at radii small relative to the bulk curvature scale.

Testing this requires an observable beyond the four-dimensional metric and clock predictions, such as multiple ringdown modes after mass and spin are fixed.

The [current LVK tests](https://dcc.ligo.org/LIGO-P2500781/public) report no overall evidence beyond general relativity. They do not establish a fifth dimension.

The earlier [hidden-dynamics report](https://github.com/Foundation-0/gravity/blob/02013ae95fa5913894b829c8e2e63a3efcde9e63/research/convergences-20261112/reports/hidden-dynamics.md) discusses limits on what observers can access. That conceptual bridge does not imply an extra physical dimension. Next research should specify a quantitative residual observable before comparing a five-dimensional model with data.
