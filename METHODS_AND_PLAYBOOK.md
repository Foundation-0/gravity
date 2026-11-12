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

## Methodological Notes (`M-01` through `M-07`)

- **M-01 (Hypothesis Re-Parameterization Map)**: Tracks how failed or tensioned parameterizations (`C-01` fixed length `l_*`, `C-04` single thermal boson, `C-11` thermal eV fermion, `C-14` mass-independent diffusion `D_ext`) were replaced by alternative parameterizations (`C-02` acceleration scale `a_0`, `C-19` handwritten potential-depth threshold `Phi_crit/c^2`, `C-20` `1/N_fil` definition). *Caveat:* `M-01` maps label and ansatz changes across waves; it is not a list of first-principles derivations.
- **M-02 (Exact Rational Interval Arithmetic)**: Uses `fractions.Fraction` (`formal/verify_exact_rational_proofs.py`) and Lean 4 `QPos`/`Int` (`formal/*.lean`) to check specific algebraic inequalities without float rounding. *Caveat:* Certifies only the stated arithmetic expression under assumed input intervals.
- **M-03 (Log-Radial Tridiagonal Newton-Raphson BVP)**: Solves `-(xi_coh^2/r)(u'' - u' - 2u) + u^2/a_0 = r^2 g_N(r)` on `s = ln r` (`550` nodes, `1 AU` to `1 Mpc`) to machine precision (`~10^-14`).
- **M-04 (Multi-Probe Binned & Catalog Cross-Checks)**: Compares kinematic rotation curves, stacked galaxy weak lensing, X-ray hydrostatic masses, and cluster weak lensing while tracking `H_0` and `f_bar` conventions explicitly.
- **M-05 (Deterministic Canonical JSON Checksums)**: Every generator script supports `--check`, verifying assertions, `sha256_canonical` (computed on `json.dumps(obj_without_sha, sort_keys=True, separators=(",", ":"))`), and exact byte-for-byte identity against `results/*.json`.
- **M-06 (Virial `sigma^4` Orthogonal-Distance Regression)**: Accounts for correlated `delta log10 R_MOND = +alpha * delta log10 sigma` measurement noise (`alpha = 4` in virial group estimators, `alpha = 2` in isothermal X-ray HSE, `alpha = 0` in weak lensing) via 2D Mahalanobis errors-in-variables quadrature in `wave7_group_cluster_threshold_audit.py`.
- **M-07 (Two-Branch Acceleration Crossover & BIC Parsimony Audit)**: Tests whether apparent multi-scale anomalies (`1 Mpc` galaxy weak lensing vs. `250 kpc` cluster cores, and CLASH vs. X-COP `g_ddag` shifts) arise from summing two established branches at fixed cosmic abundance before introducing extra free shape parameters, penalizing fitted parameters via `BIC = chi^2 + k ln N`.

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

Raw file digests (for `sha256sum -c SHA256SUMS`) are stored in root `SHA256SUMS`.
