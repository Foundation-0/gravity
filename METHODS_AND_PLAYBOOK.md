# Methods, Parameter Assumptions & Reproducibility Playbook (`Foundation-0/gravity`)

> **Attribution & Review Disclosure:** Written by an AI agent (Gemini, Google, via `orda-aska` for `Foundation-0`); **not yet reviewed by a person**. Updated in Wave 8 to remove parameter-free overclaims and align all checksums with committed generator scripts.
> **Licenses:** Apache-2.0 (code) / CC-BY-4.0 (documentation).

## Explicit Parameter & Modeling Assumptions

None of the numerical suites in this repository are parameter-free. Every script evaluates chosen scaling laws under explicit inputs or fitted parameters:

1. **Wave 1-2 (`verify_all.py`)**: Fixes `a_0 = 1.20e-10 m/s^2` (McGaugh et al. 2016 convention), synthetic disk scale `R_b propto M_b^0.28`, fixed fractal length `l_* = 3 kpc` (`C-01`), `L*` baryonic mass `6e10 M_sun`, outer NFW density factor `0.08` and Bullet Cluster `sigma_cl = 1000 km/s` at `250 kpc` (`C-04`), illustrative two-species masses `0.05 eV` / `3.0 eV` (`C-05`), `5%` ripple threshold (`C-06`), and Planck 2018 `H_0 = 67.4 km/s/Mpc`, `Omega_Lambda = 0.6847` (`C-07`).
2. **Wave 3 (`wave3_empirical_audit.py`)**: Profiles `a_0` on a `0.001e-10 m/s^2` grid across 14 SPARC `RARbins.mrt` bin means using `sem = sd / sqrt(N)` (which ignores intra-galaxy radial correlations and prefers `d_s = 0.94`), adopts `0.02 dex` statistical and `0.10 dex` systematic mass uncertainties on the 4 Mistele et al. (2024) weak-lensing bins (`129,027` isolated lenses evaluated at `H_0 = 73.0 km/s/Mpc`), and fits slopes/intercepts (`k = 1` or `2`).
3. **Wave 4 (`wave4_unified_field_solver.py`)**: Adopts `2%` wide-binary velocity boost as an input comparison threshold (`C-09`), sets healing length `xi_coh = 0.20 kpc` and boson fraction `f_B = 0.025` by hand (`C-10`), and evaluates relativistic Fermi-Dirac freeze-out (`Omega_F h^2 = 0.117`, `g_F = 2`) at `m_F = 3, 11, 35 eV` (`C-11`).
4. **Wave 5 (`wave5_unified_forces_stochastic_qm.py`)**: Uses textbook lattice QCD string tension `sigma = 0.18 GeV^2`, `m_W = 80.377 GeV`, `25 kDa` macromolecule mass (`Fein et al. 2019`), seeded harmonic oscillator (`seed = 20261111`), and solar-circle `sigma_R = 35 km/s`, `R_b = 2.97 kpc`.
5. **Wave 6 (`wave6_convergence_unification.py`)**: Defines `N_fil = 2*pi*m*c*R_H/hbar` (making `hbar`, `m`, and `R_H(z)` cancel algebraically in `C-18` and `C-20`), places threshold `Phi_crit/c^2 = 8.0e-6` by hand between logarithmic MOND galaxy potentials and the Bullet Cluster (`C-19`), and postulates a non-thermal `T = 0` condensate (`Delta N_eff = 0.0`).
6. **Wave 7 (`wave7_group_cluster_threshold_audit.py`)**: Fits 3 parameters `(sigma_crit, sigma_half, R_sat)` across 126 published systems assuming `M*/L_K = 0.80 M_sun/L_sun` for optical groups, linear gas-fraction ramp in rich groups, and core cluster baryon fraction `f_bar = 0.130` at `250 kpc`.
7. **Wave 9 (`wave9_scale_convergence_audit.py`)**: Fixes `a_0 = 1.20e-10 m/s^2` (Lelli et al. 2017), Planck 2018 `Omega_c / Omega_b = 5.3895`, and Chandra `R_2500` core baryon fraction `f_b,2500 = 0.105` (Vikhlinin et al. 2006) externally, and fits `k = 1` virial Jeans dispersion `sigma_J` (`180-190 km/s`) across the 126-system Wave-7 catalog while stating the covariant UV/linear-`P(k)` origin of `sigma_J` as an open `CONJECTURE`.
8. **Wave 10 (`wave10_covariant_jeans_unification.py`)**: Replaces the `k = 1` fitted `sigma_J` of Wave 9 with the zero-free-parameter (`k = 0`) Planck-2018 spherical-collapse velocity dispersion `sigma_*(z=0) = 185.59 km/s` (`sigma_lin(R_*, z) = 1.686` evaluated via Eisenstein & Hu 1998 transfer functions), while explicitly flagging the post-caustic Eulerian fluid closure of AeST as an open 3+1D PDE `CONJECTURE`.
9. **Wave 11 (`wave11_machian_pairing_unification.py`)**: Adopts illustrative DESI thawing CPL inputs (`w_0 = -0.75, w_a = -0.85`), spatial curvature benchmarks (`Omega_k = -0.001, -0.004, -0.010`), and dimensionless Mexican-hat offset `eps = 10^-6` (`Lambda_DE / K_2 = 2.0`), separating exact polynomial/Friedmann identities from open Machian and CPT-cogenesis `CONJECTURES`.
10. **Wave 12 (`wave12_cosmic_dawn_quasar_collapse.py`)**: Uses published `J1602+4228AB` observables from Onorato et al. (2026, ApJL 1011, L59, arXiv:2609.31835), Planck 2018 flat `LCDM + Omega_r` background integrals, fixed point-mass test parameters (`M_b = 5e10 M_sun` at `30 pkpc`, enclosed `1.5e11 M_sun` within `5.56 pkpc`), and Abramowicz et al. (1988) logarithmic slim-disk photon-trapping benchmarks (`mdot = 1..5`), noting the `~2x` virial mass systematic and pending foreground-lens model.

## Methodological Notes (`M-01` through `M-10`)

- **M-01 (Hypothesis Re-Parameterization Map)**: Tracks how failed or tensioned parameterizations (`C-01` fixed length `l_*`, `C-04` single thermal boson, `C-11` thermal eV fermion, `C-14` mass-independent diffusion `D_ext`) were replaced by alternative parameterizations (`C-02` acceleration scale `a_0`, `C-19` handwritten potential-depth threshold `Phi_crit/c^2`, `C-20` `1/N_fil` definition). *Caveat:* `M-01` maps label and ansatz changes across waves; it is not a list of first-principles derivations.
- **M-02 (Exact Rational Interval Arithmetic)**: Uses `fractions.Fraction` (`formal/verify_exact_rational_proofs.py`) and Lean 4 `QPos`/`Int` (`formal/*.lean`) to check specific algebraic inequalities without float rounding. *Caveat:* Certifies only the stated arithmetic expression under assumed input intervals.
- **M-03 (Log-Radial Tridiagonal Newton-Raphson BVP)**: Solves `-(xi_coh^2/r)(u'' - u' - 2u) + u^2/a_0 = r^2 g_N(r)` on `s = ln r` (`550` nodes, `1 AU` to `1 Mpc`) to machine precision (`~10^-14`).
- **M-04 (Multi-Probe Binned & Catalog Cross-Checks)**: Compares kinematic rotation curves, stacked galaxy weak lensing, X-ray hydrostatic masses, and cluster weak lensing while tracking `H_0` and `f_bar` conventions explicitly.
- **M-05 (Deterministic Canonical JSON Checksums)**: Every generator script supports `--check`, verifying assertions, `sha256_canonical` (computed on `json.dumps(obj_without_sha, sort_keys=True, separators=(",", ":"))`), and exact byte-for-byte identity against `results/*.json`.
- **M-06 (Virial `sigma^4` Orthogonal-Distance Regression)**: Accounts for correlated `delta log10 R_MOND = +alpha * delta log10 sigma` measurement noise (`alpha = 4` in virial group estimators, `alpha = 2` in isothermal X-ray HSE, `alpha = 0` in weak lensing) via 2D Mahalanobis errors-in-variables quadrature in `wave7_group_cluster_threshold_audit.py`.
- **M-07 (Two-Branch Acceleration Crossover & BIC Parsimony Audit)**: Tests whether apparent multi-scale anomalies (`1 Mpc` galaxy weak lensing vs. `250 kpc` cluster cores, and CLASH vs. X-COP `g_ddag` shifts) arise from summing two established branches at fixed cosmic abundance before introducing extra free shape parameters, penalizing fitted parameters via `BIC = chi^2 + k ln N`.
- **M-08 (Cross-Epoch Cosmological Consistency & Ancillary Fluid Mapping)**: Tests candidate halo Jeans mechanisms simultaneously at `z = 1100` (CMB), `z = 3` (Lyman-alpha forest), and `z = 0` (dwarfs, `L*` spirals, groups, clusters), and maps non-radiative scalar-condensate caustics onto established WHIM / intracluster entropy-floor hydrodynamics (`Cen & Ostriker 1999`; `Voit, Kay & Bryan 2005`).
- **M-09 (Current and Origin Limits)**: Checks the selected polynomial's opposite charges and equal positive dust densities on the supercritical branches `abs(u)>1`. Source-free homogeneous evolution conserves `a^3 P_Q`, so selecting charged branches does not produce them from zero current.

  Negative kinetic curvature at the symmetric origin and a kinetic degeneracy obstruct the minimal proposed transition. Full mixing stability is unresolved.

  Constant shift symmetry allows derivative portals. No annihilation rate or relic abundance is calculated. The baryon-to-photon ratio is not an initial annihilated-pair fraction. Thermal mode counting does not establish the abundance either.

- **M-10 (Conditional Observation Benchmarks)**: Separates uncertain observed inputs from model-dependent growth, halo and binary clocks. Efficiency 0.10 is a benchmark, not the Schwarzschild value. Pure H and primordial H/He opacity give different clocks. The fixed Schwarzschild counterexamples are reported separately.

  Radial infall integrates the complete force around a fixed point mass. Modified-force times are 200.08, 121.72 and 127.16 Myr. The assigned slim-disk luminosity subtracts radiated energy from the inflow, yielding 273.78 and 161.23 Myr at mdot three and five. No filament evolution, seed formation, capture, friction or merger hardening is established.

  The curved CPL models use `Omega_DE=1-Omega_m-Omega_k`. Their future onset and turnaround are conditional on an unmeasured continuation. No observed future recollapse or origin mechanism follows.

## Canonical JSON Payload Checksums (`sha256_canonical`)

| Certificate File | Generator Script | `sha256_canonical` |
|---|---|---|
| `results/certificates.json` | `verify_all.py` | `040a757f5b4a01e735d1c4a55bca639e79bf8c64ef92588ce290d931f614320a` |
| `results/exact_rational_proof_certificates.json` | `formal/verify_exact_rational_proofs.py` | `2d58555197467b3e870b72379ed919ff19536700af531ed40bc53fb25570c5d6` |
| `results/wave3_empirical_certificates.json` | `wave3_empirical_audit.py` | `75f6df7cf8e64082a3d6097ddd4723b57ce87d75013d857f24447237b1856b93` |
| `results/wave4_unified_certificates.json` | `wave4_unified_field_solver.py` | `1a7f2ff0182b66d1a081e59e750b493afa6beaab0d976c5af2c6c72652d4452d` |
| `results/wave5_forces_stochastic_certificates.json` | `wave5_unified_forces_stochastic_qm.py` | `5abd85ab08e9d951a248184acb77a8fa8e3164efc73bd523186097e9638c0b76` |
| `results/wave6_convergence_certificates.json` | `wave6_convergence_unification.py` | `49996c541b68290c5512a390b5fcc2ebb7f31b99f349fb74409b974e84bae3bf` |
| `results/wave7_group_cluster_certificates.json` | `wave7_group_cluster_threshold_audit.py` | `4db35ebcfb7b3cfc6b825e0e62c549435fa7ebdf9e31339e2bbb70482fcc08a9` |
| `results/wave9_scale_convergence_certificates.json` | `wave9_scale_convergence_audit.py` | `d9d19847bb7f9abdc294e58988259d8d20da7593ddce05184d1df81825a33a55` |
| `results/wave10_covariant_jeans_certificates.json` | `wave10_covariant_jeans_unification.py` | `7dd4b40172b8fe261c3028f7a6af6e2b5131fb93cd83d10c439e3c5f0c5be3d4` |
| `results/wave11_machian_pairing_certificates.json` | `wave11_machian_pairing_unification.py` | `4786fa9822b8b99edfd2c11ac922ca589065403e4881f5bf72d415481644692b` |
| `results/wave12_cosmic_dawn_quasar_certificates.json` | `wave12_cosmic_dawn_quasar_collapse.py` | `40a770d70d19ec3a9d7e9e5e770d0454d94595f7e7abb75e92efa351672354c9` |

Raw file digests (for `sha256sum -c SHA256SUMS`) are stored in root `SHA256SUMS`.
