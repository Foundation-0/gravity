# Claims Ledger (`Foundation-0/gravity`)

> **Attribution & Disclosure:** Written by AI agent (Gemini, Google, via `orda-aska` for `Foundation-0`); **not yet reviewed by a person**. Audited at `0311496` by an external Cursor / Grok 4.7 review and remediated in Wave 8.
> **Licenses:** Code Apache-2.0; documentation and results CC-BY-4.0.

## Epistemic Status Taxonomy

Every claim separates its **physical status** from any **arithmetic lemma**:
- **`COMPUTED (KNOWN-FRAMEWORK)`**: Reproducible numerical evaluation or ODE/BVP solve of an established published equation (Milgrom 1983; Nelson 1966; Berezhiani & Khoury 2015; Hui et al. 2017) under chosen inputs. Not new physics.
- **`EMPIRICAL-FIT`**: Parameterized statistical fit to published astronomical tables, stating fitted parameter count and error caveats.
- **`CONJECTURE`**: Unproven hypothesis, heuristic analogy, or hand-placed phenomenological threshold.
- **`KNOWN-LITERATURE-VALUE`**: Direct comparison against published experimental measurements.
- **`PROVEN (ARITHMETIC-LEMMA)`**: Restricted **solely** to the literal integer or rational goal checked in `formal/*.lean` or `formal/verify_exact_rational_proofs.py`. Never applied to physical interpretations.

## Waves 1-2: Baseline Scaling, Solitons & EFE (`verify_all.py`)

- **C-01 (Coordinate-Fractal Scaling vs. BTFR)** -- `COMPUTED (KNOWN-FRAMEWORK)`
  - *Computation & Inputs:* Evaluates `g propto (G M_b / r^2)(1 + r/l_*)^(3 - D_f)` with chosen `l_* = 3 kpc`, `R_b propto M_b^0.28`, `a_0 = 1.2e-10 m/s^2` (`beta = 2.0186`, RMS `0.6234 dex` vs. McGaugh RAR function on synthetic galaxies). Reproduces Milgrom (1983, ApJ 270, 365): a fixed length scale cannot give both flat curves and `M_b propto v^4`. Briscese & Calcagni (2026, arXiv:2603.24593) fix Hausdorff dimension equal to topological dimension and do not propose this rotation law.
  - *Lean Arithmetic Lemma (`PROVEN (ARITHMETIC-LEMMA)` in `formal/GravityClaims.lean`):* `2 - Df = 0 <-> Df = 2` and `(2 : Int) != 4`. Does not derive a force law.

- **C-02 (p-Laplacian Flux Exponent for Flat Rotation Curves)** -- `COMPUTED (KNOWN-FRAMEWORK)`
  - *Computation & Inputs:* Under the Berezhiani & Khoury (2015, PRD 92, 103510, arXiv:1507.01019) phonon flux ansatz `4*pi*r^2 |theta'|^(1 + d_s) propto M_b` (cf. Son & Wingate 2006, Ann. Phys. 321, 197 for `X^(5/2)`), flat curves fix `d_s = 1`, `q = 3/2`, `p = 3`, `beta = 4`. `0.0096 dex` compares two analytical MOND interpolators at shared `a_0 = 1.2e-10 m/s^2` (not SPARC data; see C-08 where SPARC prefers `d_s = 0.94`). CDT (Ambjorn et al. 2005, PRL 95, 171301) and asymptotic safety (Lauscher & Reuter 2005, JHEP 10, 050) random-walk spectral dimensions are distinct objects.
  - *Lean Arithmetic Lemma (`PROVEN (ARITHMETIC-LEMMA)` in `formal/GravityClaims.lean`):* `(ds - 1 = 0 /\ 2*(1 + ds) = 4 /\ 2 + ds = 3) <-> ds = 1` and `1 + 1/2 = 3/2`.

- **C-03 (Ground-State Schrodinger-Poisson Soliton)** -- `COMPUTED (KNOWN-FRAMEWORK)`
  - *Computation & Inputs:* RK4 + bisection (`h = 0.0025`) reproduces the Hui, Ostriker, Tremaine & Witten (2017, PRD 95, 043541, Eq. 29) ground-state invariant `M r_{1/2} = 3.9251 hbar^2 / (G m^2)` and Keplerian outer slope `-0.4994` (cf. Schive et al. 2014; Chavanis 2018).
  - *Lean Arithmetic Lemma:* None.

- **C-04 (Single-Boson Condensation Window: 1 Mpc Halo vs. Bullet Cluster)** -- `COMPUTED (KNOWN-FRAMEWORK, MODEL-DEPENDENT)`
  - *Computation & Inputs:* Evaluates `n lambda_th^3 >= zeta(3/2)` assuming `M_b = 6e10 M_sun`, `a_0 = 1.2e-10 m/s^2`, `sigma_gal = v_flat / sqrt(2)`, an `0.08` NFW factor at `1 Mpc`, and Bullet Cluster `sigma_cl = 1000 km/s` at `250 kpc` (Clowe et al. 2006; Berezhiani & Khoury 2015), giving `1.0306 < 1.9379 < 2.3015 eV`.
  - *Lean Arithmetic Lemma (`PROVEN (ARITHMETIC-LEMMA)` in `formal/GravityClaims.lean`):* Checks isothermal interval bound `4 * 105^4 * 10^7 / (65536 * 66740 * 6 * 19884 * 115) < 1/12 < 1` (`0.081021 < 1`; excludes `0.08` NFW factor).

- **C-05 (Two-Species Degeneracy Example)** -- `COMPUTED (KNOWN-FRAMEWORK) / CONJECTURE`
  - *Computation & Inputs:* Evaluates `N_deg` at chosen `m_L = 0.05 eV`, `f_L = 0.02`, `m_H = 3.0 eV`, `f_H = 0.98` (`N_L = 9432.49`, `N_H = 0.8867`), illustrating two-phase ideas in Berezhiani & Khoury (2015), Berezhiani, Famaey & Khoury (2018, arXiv:1711.05748), Hodson et al. (2017, A&A 607, A108), and Skordis & Zlosnik (2021, PRL 127, 161302). Cluster phonon screening is conjectured.
  - *Lean Arithmetic Lemma:* None.

- **C-06 (Geometric-Shell Soliton Ripple Toy Integral)** -- `COMPUTED (TOY-MODEL)`
  - *Computation & Inputs:* Stacks `(1 + 0.091 u^2)^(-8)` shells against a chosen `5%` ripple ceiling (`b = 6` gives `4.561%`; `b = 7` gives `6.084%`). Arvanitaki et al. (2010, PRD 81, 123530) motivate discrete axion spectra qualitatively but do not state this ripple bound.
  - *Lean Arithmetic Lemma:* None.

- **C-07 (External-Field Quadrature & Horizon Accelerations)** -- `COMPUTED (KNOWN-FRAMEWORK)`
  - *Computation & Inputs:* Evaluates Bekenstein & Milgrom (1984) AQUAL quadrature at `e_MW = 1.8101` (`+18.31%` RAR vs. `+3.16%` exponential interpolator; Gaia wide binaries remain debated, e.g. Banik et al. 2024, arXiv:2311.03436) and compares `c H_0 / (2*pi)` (Milgrom 1983; arXiv:2001.09729) and `c H_0 / 6` (Verlinde 2017, arXiv:1611.02269) using Planck 2018 `H_0 = 67.4 km/s/Mpc`, `Omega_Lambda = 0.6847` (arXiv:1807.06209).
  - *Lean Arithmetic Lemma:* None.

## Wave 3: Binned SPARC & KiDS Fits (`wave3_empirical_audit.py`)

- **C-08 (SPARC RAR 14-Bin & KiDS-1000 4-Bin BTFR Fits)** -- `EMPIRICAL-FIT (KNOWN-FRAMEWORK)`
  - *Computation & Caveats:* Fits 14 SPARC `RARbins.mrt` bin means (2,630 points; Lelli et al. 2017, ApJ 836, 152; McGaugh et al. 2016, PRL 117, 201101) using `sem = sd / sqrt(N)`, which treats points within the same galaxy as independent; profiling `a_0` gives best fit `d_s = 0.94` (`[0.92, 0.96]`, `chi^2 = 25.890`) vs. `d_s = 1.00` (`a_0 = 1.179e-10 m/s^2`, `chi^2 = 30.486`). Fits 8 SPARC kinematic BTFR bins (`beta = 3.83`) and 4 KiDS-1000 stacked WL bins (`52,553 + 43,727 + 22,950 + 9,797 = 129,027` isolated lenses in Mistele et al. 2024, ApJL 969, L3, arXiv:2406.09685 Sec. II & Table 2, adopting `H_0 = 73.0 km/s/Mpc` and an assumed `0.02 dex` mass error; `beta = 4.00`, `chi^2 = 0.634`). Combined 12-bin fit (`0.10 dex` WL systematic) yields `beta = 3.83` with `Delta BIC(free - beta=4) = -0.44`.
  - *Lean Arithmetic Lemma:* None.

## Wave 4: Interpolator Scan, Bogoliubov BVP & Fermion Audit (`wave4_unified_field_solver.py`)

- **C-09 (Interpolator Family Tradeoff vs. Assumed 2% Wide-Binary Ceiling)** -- `COMPUTED (MODEL-FAMILY-SCAN)`
  - *Computation & Inputs:* Scans `mu_alpha(x) = (1 - exp(-x^alpha))^(1/alpha)` on the 14 SPARC bins (`chi^2_min = 20.381`): within `Delta chi^2 <= 25`, minimum wide-binary boost is `12.91%`; enforcing input ceiling `<= 2%` costs `Delta chi^2 = 311.37`.
  - *Lean Arithmetic Lemma (`PROVEN (ARITHMETIC-LEMMA)` in `formal/GravityClaims.lean`):* For stipulated `mu <= 76/100` and `L <= 40/100`, checks `9375 / 6859 > (51 / 50)^4`.

- **C-10 (Spherical Bogoliubov-p-Laplacian BVP Solver)** -- `COMPUTED (BVP-SOLVER)`
  - *Computation & Inputs:* For chosen inputs `xi_coh = 0.20 kpc` (`m_B = 3.8556e-23 eV`) and `f_B = 0.025` (`f_B < 0.20` is a simple rule-of-thumb check against Kobayashi et al. 2017, PRD 96, 123514, not a forest transfer-function solve), solves `-(xi_coh^2/r)(u'' - u' - 2u) + u^2/a_0 = r^2 g_N(r)` across 1 AU to 1 Mpc (`g_ph/g_N = 1.175e-7` at 20 kAU; `99.994%` recovery of deep-MOND limit at 100 kpc).
  - *Lean Arithmetic Lemma:* None.

- **C-11 (Relativistic-Freeze-Out Sterile Fermion Audit)** -- `COMPUTED (KNOWN-FRAMEWORK)`
  - *Computation & Inputs:* For `g_F = 2` saturating `Omega_F h^2 = 0.117` via `(g_F/2)(T_F/T_nu)^3(m_F / 93.14 eV) = 0.117`, computes required `T_F/T_nu`, `g_*S,dec = 10.75/(T_F/T_nu)^3`, BBN `Delta N_eff^BBN = (g_F/2)(T_F/T_nu)^4`, UV photon ratio `rho_F/rho_gamma = (7/8)(4/11)^(4/3) Delta N_eff^BBN` (with the `7/8` fermionic radiation factor), and non-relativistic redshift `z_nr` at `m_F = 3, 11, 35 eV` (`Delta N_eff^BBN = 5.584, 0.988, 0.211`; `z_nr = 3.69e3, 2.09e4, 9.77e4 > z_rec = 1100`). Shows `3` and `11 eV` fail BBN `Delta N_eff` (`3 eV` also needs `g_*S,dec = 2.96 < 10.75`), while all three are non-relativistic by recombination and excluded by warm-DM free-streaming (`m_WDM >= 3 keV`).
  - *Lean Arithmetic Lemma:* None.

## Wave 5: Force-Scale & Stochastic QM Checks (`wave5_unified_forces_stochastic_qm.py`)

- **C-12 (Force-Law Exponent Comparison)** -- `COMPUTED (KNOWN-FRAMEWORK) / CONJECTURE`
  - *Computation:* Textbook Cornell string tension `sigma = 0.18 GeV^2` -> `1.4615e5 N` (Eichten et al. 1978) gives log-slopes `-1.9129` (`0.05 fm`) and `-0.0470` (`2.0 fm`). Does not derive galactic phonons or the BCJ double copy (Bern, Carrasco & Johansson 2008/2010).
  - *Lean Arithmetic Lemma (`PROVEN (ARITHMETIC-LEMMA)` in `formal/Wave5StochasticForces.lean`):* `claim_c12_log_slope_relation` checks `-2 + 0 = 2 * (-1)` and `-2 < -1 < 0`.

- **C-13 (Compton & Horizon Accelerations)** -- `COMPUTED (KNOWN-FRAMEWORK) / CONJECTURE`
  - *Computation:* Evaluates `a = c^2 / L_gap` at `m_W`, `sqrt(sigma_QCD)`, and `a_dS = c H_0 / (2*pi) = 1.0422e-10 m/s^2` (Milgrom 1983). Hypothetical dark SU(2) `alpha_UV = 0.00603` vs. QCD `0.02003` (ratio `3.322`) is an algebraic one-loop inversion; no dark beta-function is integrated.
  - *Lean Arithmetic Lemma:* None (`formal/Wave5StochasticForces.lean` has no C-13 theorem).

- **C-14 (Diffusivity Mass Ratio `m / m_e` vs. Gravitational WEP)** -- `COMPUTED (MASS-RATIO ARITHMETIC)`
  - *Computation:* `m(25 kDa) / m_e = 4.5572e7` is a particle mass ratio showing only that `D_ext = const` differs from `D_QM = hbar / (2m)` across electrons and 25 kDa oligoporphyrins (Fein et al. 2019, Nature Physics 15, 1242 measured interference fringes, not WEP violation; cf. Calogero 1997, PLA 228, 335). True gravitational WEP bounds are Eot-Wash `eta = (0.3 +/- 1.8)e-13` (Wagner et al. 2012) and MICROSCOPE `eta = (-1.5 +/- 2.7)e-15` (Touboul et al. 2022).
  - *Lean Arithmetic Lemma (`PROVEN (ARITHMETIC-LEMMA)` in `formal/Wave5StochasticForces.lean`):* `claim_c14_mass_ratio_bound` checks `45570000 * 91095 < 415125 * 10^7`.

- **C-15 (Nelson Diffusion Simulation)** -- `COMPUTED (KNOWN-FRAMEWORK)`
  - *Computation:* Seeded (`20261111`) harmonic-oscillator check (`heating_ratio = 6.263`, stationary `Var(x) = 0.4961` vs. `0.5`) illustrating established results of Nelson (1966, Phys. Rev. 150, 1079), Abbott & Wise (1981, AJP 49, 37), and Wallstrom (1994, PRA 49, 1613).
  - *Lean Arithmetic Lemma:* None (`formal/Wave5StochasticForces.lean` has no C-15 theorem).

- **C-16 (Bell-CHSH Literature Benchmark)** -- `KNOWN-LITERATURE-VALUE`
  - *Context:* Records Hensen et al. (2015, Nature 526, 682) `S = 2.42 +/- 0.20` above `2` and below Tsirelson's `2*sqrt(2) = 2.828427`. Tests quantum spin entanglement, **not** classical galactic N-body noise or dark-matter halos.
  - *Lean Arithmetic Lemma (`PROVEN (ARITHMETIC-LEMMA)` in `formal/Wave5StochasticForces.lean`):* `claim_c16_bell_chsh_bounds` checks `4 * 2500 < 14641 /\ (4 : Int) < 8`.

- **C-17 (Solar-Circle Epicyclic Scale & Thin-Disk Quadrupole)** -- `COMPUTED (KNOWN-FRAMEWORK)`
  - *Computation:* Evaluates `lambda_epi = sigma_R / kappa = 0.8604 kpc` and classical quadrupole decay `(3/2)(R_b/r)^2 g_N(r)` (`1.3231e-3` at `100 kpc`, `1.3231e-5` at `1 Mpc` vs. RAR boost `119.79`). Batygin (2018, MNRAS 475, 5070) applies to quasi-Keplerian disks, not outer galactic halos.
  - *Lean Arithmetic Lemma:* None (`formal/Wave5StochasticForces.lean` has no C-17 theorem).

## Wave 6: Algebraic Re-Parameterizations & Potential Ansatz (`wave6_convergence_unification.py`)

- **C-18 (Milgrom Horizon Acceleration & MOND Radius Identity)** -- `COMPUTED (KNOWN-FRAMEWORK) / CONJECTURE`
  - *Computation:* `a_dS = c H_0 / (2*pi) = 1.0422e-10 m/s^2` is Milgrom's (1983) relation and `8.9580 kpc` is `r_M = sqrt(G M_b / a_dS)` for `6e10 M_sun`. `hbar` cancels by definition of `N_fil`; `1.815e-16` is float64 rounding; `d_s = 1.0` is postulated (no percolation calculation exists).
  - *Lean Arithmetic Lemma (`PROVEN (ARITHMETIC-LEMMA)` in `formal/Wave6Convergence.lean`):* `c18_hbar_cancels_identically` checks commutative-ring rearrangement over `Int`.

- **C-19 (Handwritten Potential-Depth Threshold Ansatz)** -- `CONJECTURE / PHENOMENOLOGICAL-ANSATZ`
  - *Computation:* Places `Phi_crit/c^2 = 8.0e-6` by hand between logarithmic MOND galaxy potentials (`1.8658e-6` at `10 kpc`, Keplerian `2.8712e-7` at `1 Mpc`, `6.4938e-6` for `300 km/s`) and an isothermal Bullet Cluster potential (`6.8527e-5` at `250 kpc`, quotients `36.73` and `238.67`; cf. Berezhiani & Khoury 2015; Hodson et al. 2017). `388.1 km/s` solves `2*(sigma/c)^2*(1 + ln 4) = 8.0e-6`; `Delta N_eff = 0.0` is assumed via a non-thermal `T = 0` condensate.
  - *Lean Arithmetic Lemma (`PROVEN (ARITHMETIC-LEMMA)` in `formal/Wave6Convergence.lean`):* `c19_potential_depth_clean_window` checks `29 < 187 < 650 < 800`, `8*800 < 6852`, `36*187 < 6852`, `236*29 < 6852`.

- **C-20 (Algebraic Cancellation in `D_1 / N_fil`)** -- `COMPUTED (ALGEBRAIC-IDENTITY) / CONJECTURE`
  - *Computation:* `m` and `R_H(z)` cancel by definition of `N_fil = 2*pi*m*c*R_H(z)/hbar`. Not a redshift calculation, and `2.341e-16` is float64 rounding rather than an Eotvos WEP parameter `eta`.
  - *Lean Arithmetic Lemma (`PROVEN (ARITHMETIC-LEMMA)` in `formal/Wave6Convergence.lean`):* `c20_centroid_diffusion_epoch_and_mass_invariant` checks `(piVal * c * RH * hbar) * (2 * m) = (2 * piVal * m * c * RH) * hbar`.

## Wave 7: Empirical Group & Cluster Curve Fit (`wave7_group_cluster_threshold_audit.py`)

- **C-21 (Multi-Catalog 3-Parameter Saturation Fit Across 126 Systems)** -- `EMPIRICAL-FIT`
  - *Computation:* Fits `(sigma_crit, sigma_half, R_sat)` across 126 systems (SPARC, Mistele et al. 2024 KiDS WL, Milgrom 2019 groups, Angus et al. 2008 X-ray, Kettula et al. 2015 WL+X-ray; cf. Sanders 2003; Tian et al. 2020; Li et al. 2024). Gradual onset near `sigma_crit = 190-195 km/s` is preferred over a sharp `388.1 km/s` step (`Delta chi^2 = 15.36` on the 60-system zero-covariance subset; `19.43` on `150-1200 km/s`), with 50% midpoint `372.2 km/s` (`199.1 km/s` on `150-1200 km/s`).
  - *Lean Arithmetic Lemma (`PROVEN (ARITHMETIC-LEMMA)` in `formal/Wave7ThresholdAudit.lean`):* Checks `152 < 190 < 283 < 388` and `365^2 < 190^2 + 320^2 < 390^2`.

- **C-22 (Core Plateau vs. Unsaturated `(sigma^2 - sigma_crit^2)^(3/2)` Growth)** -- `EMPIRICAL-FIT`
  - *Computation:* Unsaturated `(sigma^2 - sigma_crit^2)^(3/2)` growth fails on `9-14 keV` WL clusters (`Delta chi^2 = 153.20` on `150-1200 km/s`), whereas core mass ratios plateau around `R_sat = 3.7-4.2` below cosmic `Omega_m / Omega_b = 6.39`.
  - *Lean Arithmetic Lemma (`PROVEN (ARITHMETIC-LEMMA)` in `formal/Wave7ThresholdAudit.lean`):* Checks `11 * (1000^2 - 388^2)^3 < (1494^2 - 388^2)^3` and `(x + s) + (rSat - 1)*x < rSat*(x + s)` (`0 < s`, `1 < rSat`).

## Wave 9: Two-Branch Phonon-Dust Crossover & AeST Oscillation Bounds (`wave9_scale_convergence_audit.py`)

- **C-23 (Phonon-Dust Baryonic-Acceleration Crossover, CLASH/X-COP Scale Dependence & 1-Parameter Jeans Fit)** -- `COMPUTED (KNOWN-FRAMEWORK) & EMPIRICAL-FIT`
  - *Computation & External Inputs:* Evaluates an additive two-branch acceleration `g_tot(r) = g_RAR(g_b; a_0) + f_trap(sigma) * R_cdm_to_bar * g_b(r)` motivated by relativistic two-branch superfluid/AeST completions (Berezhiani & Khoury 2015, arXiv:1507.01019; Skordis & Zlosnik 2021, PRL 127, 161302, arXiv:2007.00082) using fixed `a_0 = 1.20e-10 m/s^2` (Lelli et al. 2017) and Planck 2018 `Omega_c / Omega_b = 5.3895`.
    1. *Crossover (`COMPUTED`):* `g_RAR(g_b) - g_b = 5.3895 * g_b` occurs at `g_b,x = 0.02897 a_0 = 3.476e-12 m/s^2` (`r_x = 5.88 r_M = 49.05 kpc` for `6e10 M_sun` vs. `1001.2 kpc` for a `2.5e13 M_sun` cluster). At `1 Mpc` around isolated KiDS-1000 galaxies (Mistele et al. 2024), phonon acceleration exceeds the entire `5.39 M_b` cosmic dust budget by `12.24x` to `47.87x` (`<= 3.95%` circular-velocity shift even if `f_trap = 1`), whereas at `250 kpc` inside rich clusters (`g_b ~ 0.3-1.5 a_0 >> g_b,x`), cosmic dust exceeds phonon boost by `3x-5x`.
    2. *CLASH vs. X-COP Apparent `g_ddag` (`COMPUTED`, zero fitted parameters):* Evaluating `g_RAR(g_b; a_0) + 5.3895 g_b` yields apparent `g_ddag = 2.049e-9 m/s^2` (log-slope `0.891`) at `g_b = 4.0e-11 m/s^2` vs. Tian et al. (2020, ApJ 896, 70) `(2.02 +/- 0.11)e-9 m/s^2`, `g_ddag = 1.062e-9 m/s^2` (log-slope `0.845`) at `g_b = 1.6e-11 m/s^2` vs. Pradyumna et al. (2021, PDU 31, 100765) `(1.12 +/- 0.11)e-9 m/s^2`, and `0.412e-9 m/s^2` at `g_b = 3.0e-12 m/s^2` (cf. Eckert et al. 2022, A&A 662, A123).
    3. *1-Parameter Virial Jeans Fit (`EMPIRICAL-FIT`, `k = 1`):* Using unsegregated global `Omega_c/Omega_b = 5.39` at `250 kpc` underpredicts cluster cores (`chi^2 = 112.38` on `N = 60`); adopting the published Chandra `R_2500` intracluster gas-depletion factor `f_b,2500 = 0.105` (Vikhlinin et al. 2006, ApJ 640, 691, giving `(1 - f_b,2500)/f_b,2500 = 8.5238`) and fitting one Jeans dispersion `sigma_J = 190 km/s` in `f_trap = max(0, 1 - sigma_J^2 / sigma^2)` gives `chi^2 = 60.07` (`59 dof`, `BIC = 64.17` vs. Wave-7 3-parameter `BIC = 70.27`, `Delta BIC = -6.10` on `N = 60`; `BIC = 152.97` vs. `156.83`, `Delta BIC = -3.86` on `N = 126` at `sigma_J = 180 km/s`). *Open theoretical problem (`CONJECTURE`):* deriving late-time `sigma_J ~ 180-190 km/s` from a covariant condensate action without linear `P(k)` damping at `z >= 1` remains unsolved.
  - *Lean Arithmetic Lemma:* None.

- **C-24 (Quasistatic AeST Linear Mass-Term Oscillation Bound)** -- `COMPUTED (KNOWN-FRAMEWORK)`
  - *Computation & Inputs:* Evaluates the Verwayen, Skordis & Boehm (2024, MNRAS 531, 272, arXiv:2304.05134, Eq. 35 & 50) quasistatic AeST breakdown radius `r_C^(max) = (18 r_M / mu^2)^(1/3)` (cf. Mistele, McGaugh & Hossenfelder 2023, arXiv:2301.03499). Requiring `r_C^(max) >= 1.0 Mpc` across the Mistele et al. (2024) KiDS-1000 bins forces `mu^(-1) >= 2.579 Mpc` (`L*`) to `3.774 Mpc` (Bin 1), which sets `r_C^(max) >= 2.733 Mpc >> 0.25 Mpc` for a `2.5e13 M_sun` cluster -- ruling out static linear `+mu^2 Phi` terms as the source of `250 kpc` cluster missing mass.
  - *Lean Arithmetic Lemma:* None.

## Wave 10: Homogeneous Sound-Speed No-Go, Dark-WHIM Nonlinear Scale & 4-Way Convergence (`wave10_covariant_jeans_unification.py`)

- **C-25 (Homogeneous FLRW Adiabatic Sound-Speed & Scordatura No-Go Bound)** -- `COMPUTED (LINEAR-COSMOLOGY NO-GO)`
  - *Computation & Inputs:* Evaluates why a `185 km/s` halo Jeans scale cannot reside on the homogeneous linear FLRW background: (i) any homogeneous `c_s(z=0) = 185 km/s` yields comoving Jeans wavelength `lambda_J,com(z=0) = 25.10 Mpc` (`k_J = 0.2504 Mpc^-1`), damping linear galaxy/group clustering; (ii) cosmic matter density at recombination (`z = 1100`) is `4.207e8 * rho_crit0`, exceeding `z = 0` virialized halo density (`200 * rho_crit0`) by `2.103e6x`, so monotone-increasing barotropic polytropes `P propto rho^gamma` (`gamma > 1`) have much higher sound speed at `z = 1100` than inside `z = 0` halos; (iii) constant-`M` `k^4` ghost-condensate scordatura scales as `k_J,com(z) / k_J,com(0) = (1 + z)^(-1/4) = 0.1736` at `z = 1100`; and (iv) shift-symmetric `K(Q) = Lambda^4 ((Q - Q_0)/Q_0)^p` (`p = 2..32`, cf. Scherrer 2004, PRL 93, 011301) interpolates between `w(z=1100) = 0.939` (`p = 2`) and the `lambda_J,com(0) = 25.10 Mpc` linear floor (`p -> infinity`).
  - *Lean Arithmetic Lemma (`PROVEN (ARITHMETIC-LEMMA)` in `formal/Wave10JeansDerivation.lean`):* Checks `315 * 1101^3 > 1000 * 200 * 2090000` and `(4 - alpha4 = 3) <-> alpha4 = 1`.

- **C-26 (Zero-Parameter Planck-2018 Nonlinear Collapse Scale `sigma_*(z)` & `k = 0` Group/Cluster Test)** -- `COMPUTED (KNOWN-FRAMEWORK) & CONJECTURE`
  - *Computation & External Inputs:* Evaluates the Planck 2018 linear power spectrum (Eisenstein & Hu 1998, ApJ 496, 605; Planck Collaboration 2020, arXiv:1807.06209) at spherical-collapse threshold `sigma_lin(R_*, z) = 1.686` with **zero free parameters**: `sigma_1D(M_*(z))` grows forward in time from `2.22 km/s` (`z = 5`) and `11.36 km/s` (`z = 3`, preserving Lyman-alpha forest structure, `> 65x` colder than an adiabatic thermal relic) to **`sigma_*(z=0) = 185.59 km/s`** (`R_* = 3.3483 Mpc`, `M_* = 6.24e12 M_sun`, `V_200 = 262.46 km/s`). In hydrostatic Jeans equilibrium (`gamma_d = -d ln rho_d / d ln r = 2 (sigma_halo / sigma_*)^2`), `gamma_d` reaches the isothermal core-collapse slope `2` at `sigma_halo = 185.59 km/s`, suppressing enclosed dust inside `5 kpc` of a `50 km/s` dwarf to `0.19%` of `M_b` and inside `10 kpc` of an `L*` spiral to `0.83%` of `M_b`. Fixing `sigma_J = 185.59 km/s` (`k = 0` fitted parameters, alongside external `a_0 = 1.20e-10 m/s^2`, Planck `Omega_c/Omega_b = 5.3895`, and Vikhlinin `f_b,2500 = 0.105`) gives `chi^2 = 60.26` for `60 dof` (`chi^2/dof = 1.004`, `BIC = 60.26`), improving over Wave-7's 3-parameter Hill fit by `Delta BIC = -10.01` (`-8.62` on all 126 systems; cf. X-ray entropy floors in Ponman, Cannon & Navarro 1999, arXiv:astro-ph/9810359; Voit, Kay & Bryan 2005, arXiv:astro-ph/0511252; WHIM shocks in Cen & Ostriker 1999/2006).
  - *Explicit Conjecture Scope:* Treating the post-caustic AeST / ghost-condensate dust branch as an entropy-conserving non-radiative fluid (`Lambda_cool^dark = 0`) rather than collisionless Vlasov particles requires 3+1D nonlinear AeST PDE verification (Bataki, Skordis & Zlosnik 2024, arXiv:2307.15126; Mistele et al. 2023, arXiv:2301.03499) and is labeled `CONJECTURE`.
  - *Lean Arithmetic Lemma (`PROVEN (ARITHMETIC-LEMMA)` in `formal/Wave10JeansDerivation.lean`):* Checks `0 <= sigSq < sigStarSq -> 2*sigSq < 2*sigStarSq /\ 3*sigStarSq - 2*sigSq > sigStarSq` and `1136 < 1500 /\ 60 * 1136 < 4 * 18559`.

- **C-27 (Four-Way `~185 km/s` Scale Convergence & Euclid/LSST High-`z` Discriminating Forecast)** -- `COMPUTED / CONJECTURE`
  - *Computation:* Compares four independently defined velocity scales at `z = 0`: Wave-9 empirical group onset (`180-190 km/s`), Planck-2018 nonlinear collapse `sigma_*(0) = 185.59 km/s`, Milgrom `L*` rotation speed `(G M_b* a_0)^(1/4) = 175.82 km/s`, and QED bremsstrahlung Hubble-time cooling at `Delta = 1000` (`178.42 km/s`, Rees & Ostriker 1977). Contrasts dynamic Dark-WHIM shock heating against a constant Lorentz-norm scale `Q_0^(-1) = 2 c sigma_* / a_0 = 30.052 Mpc` in `X = Q^2 - Y`: for `sigma = 200 km/s` groups, dynamic `sigma_*(z)` predicts `f_trap` rises from `0.1389` (`z = 0`) to `0.6730` (`z = 0.5`) and `0.8778` (`z = 1.0`), whereas constant `Q_0` predicts `f_trap = 0.1389` at all redshifts.
  - *Lean Arithmetic Lemma:* None.

## Wave 11: Machian Horizon Inertia, DESI Turnaround & CPT Pair-Condensate Audit (`wave11_machian_pairing_unification.py`)
- **C-28 (Machian Horizon Frame-Dragging Induction vs. Relativistic Lensing & Non-Locality)** -- `COMPUTED (KNOWN-FRAMEWORK) / CONJECTURE`
- *Computation & Literature:* Critical density and `R_H = c/H` imply Hubble-sphere compactness `1/2` and the selected potential integral `3/4`. An illustrative partition assigns `K_gm = 2/3` and `K_ge = 1/3`. Manuel Urueña Palomo (2026), arXiv:2610.09987v2, presents a related Machian proposal. These substitutions do not derive inertia here.
- *Limits:* The quoted Unruh-de Sitter acceleration is a known benchmark. Lensing consistency, a covariant action and multi-body momentum conservation require separate analysis. Arithmetic partition checks establish no physical mechanism.
- *Lean Arithmetic Lemma (`PROVEN (ARITHMETIC-LEMMA)` in `formal/Wave11MachianZeroEnergy.lean`):* Checks `2 + 1 = 3` and `2 * 1 = 2`.
- 
- **C-29 (Hamiltonian Constraint and Conditional CPL Turnaround)** -- `COMPUTED (FRIEDMANN-IDENTITIES)`
  - *Computation & Inputs:* Records a Hamiltonian constraint under stated boundary and gauge conditions, not a measurable global energy balance or universe-creation process. For chosen CPL inputs `w_0 = -0.75`, `w_a = -0.85`, the flat model gives `a_slow = 1.3897`. Closed models now use `Omega_DE = 1 - Omega_m - Omega_k`, so `H^2(a=1)/H_0^2 = 1`.

  Turnaround near `a = 315.18, 78.80, 31.52` is conditional on extending that equation of state into the unmeasured future. Past-compatible continuations need not recollapse. The parameters are inserted here, not fitted to DESI.
  - *Lean Arithmetic Lemma:* None.

- **C-30 (CPT-Symmetric Kinetic Mexican-Hat Pair Bifurcation & Condensate Cogenesis Remnant)** -- `COMPUTED (ALGEBRAIC-MODEL) & CONJECTURE`
  - *Computation & Literature:* Evaluates the chosen polynomial `P(u) = K_2 (u^2 - 1)^2 - Lambda_DE`. Algebraically, the states `u = +/- (1 + eps)` have opposite shift charges and equal positive dust densities. This does not derive their production from `u = 0`.

  The minimal homogeneous scalar sector has `P_QQ(0) = -4 K_2 / Q_0^2`, and a source-free homogeneous solution conserves `a^3 P_Q`. Starting with zero current cannot produce nonzero branch charge without an additional source, boundary condition or production prescription.
  - *Limits:* Full AeST mixing stability is not solved. Constant shift symmetry allows derivative portals such as `(partial_phi)^2 F_mu_nu F^mu_nu`, so it does not forbid all pair conversion. `eta_B` is a baryon-to-photon ratio, not the fraction of initial pairs annihilated. No portal rate, origin mechanism or relic abundance is established.

  Scherrer (2004), Boyle, Finn and Turok (2018) and Co and Harigaya (2020) provide prior frameworks, not proofs of this transition.
  - *Lean Arithmetic Lemma (`PROVEN (ARITHMETIC-LEMMA)` in `formal/Wave11MachianZeroEnergy.lean`):* Proves over `Int` for all `u, q0` that `noetherJ (-u) q0 + noetherJ u q0 = 0`, `legendreRho (-u) q0 = legendreRho u q0`, and `0 <= q0Sq < uSq -> 0 < (uSq - q0Sq)*(3*uSq + q0Sq)`.
## Wave 12: Cosmic-Dawn Compact Quasar Pair `J1602+4228AB` (`Napowawa'enakaulua`) Audit (`wave12_cosmic_dawn_quasar_collapse.py`)

- **C-31 (Cosmic-Dawn Dual-Quasar Salpeter Duty-Cycle Wall & Clustering Excess)** -- `COMPUTED (KNOWN-FRAMEWORK)`
  - *Computation & Observed Inputs:* Uses the reported `J1602+4228AB` point values from Onorato et al. (2026), arXiv:2609.31835. The `z = 20` growth budget is `734.10 Myr`. A `100 M_sun` seed growing to `1.5e9 M_sun` at fixed Eddington ratio one and efficiency `0.10` needs `827.08 Myr` for pure H, but `725.76 Myr` for primordial H/He.

  Efficiency `0.10` is not the Schwarzschild thin-disk value. At fixed `1 - sqrt(8/9)`, the respective times are `451.54` and `396.22 Myr`. These are conditional growth clocks, not an exclusion of all light seeds or evidence that any history occurred.
  - *Limits:* Formation delays, spin evolution, fuel supply and duty histories are omitted. Current luminosity is not a lifetime average. Virial masses, Eddington ratios and systemic velocities are uncertain. Lensing remains unresolved. Clustering excess over an extrapolated baseline does not by itself compare cosmological likelihoods.
  - *Lean Arithmetic Lemma (`PROVEN (ARITHMETIC-LEMMA)` in `formal/Wave12QuasarCollapse.lean`):* Checks `(1 * 4) * 9 = 9 * 4` and `2 * 4 < 9` (`eps/(1-eps)` jumps by `9/4 > 2` from `eps = 0.1` to `0.2`).

- **C-32 (Cosmic-Dawn Dark-WHIM Trapping Inversion `sigma_*(z=6.08) = 0.97 km/s` & Phonon Free-Fall Speedup)** -- `COMPUTED (MODEL-COMPARISON) & CONJECTURE`
  - *Computation & Inputs:* The chosen spectrum and growth approximation give `M_* = 8.39e4 M_sun` and `sigma_* = 0.97 km/s` at `z = 6.0783`. This is total nonlinear halo mass, not a black-hole seed. The value `f_trap = 0.99997` is an assigned trapping prescription, not a capture solution.
  - *Corrected radial benchmark:* For release from rest at `30 pkpc` around a fixed `5e10 M_sun` baryonic point mass, energy-conserving integration gives `384.82 Myr` for Newtonian baryons, `200.08 Myr` for constant-a0 RAR, `121.72 Myr` for Hubble-a0 RAR and `127.16 Myr` for constant-a0 RAR plus the assigned condensate force.

  Earlier `182.27`, `109.04` and `122.79 Myr` values substituted the outer acceleration into a Newtonian formula and are superseded. No filament pressure, geometry, angular momentum, cooling or friction is solved.
  - *Lean Arithmetic Lemma (`PROVEN (ARITHMETIC-LEMMA)` in `formal/Wave12QuasarCollapse.lean`):* Checks `2^2 < 177^2 < 185^2` and `9998 * 177^2 < 10000 * (177^2 - 2^2)`.

- **C-33 (Slim-Disk Photon-Trapping Super-Eddington Growth, `5.56 pkpc` Orbital Projection & NANOGrav Chirp Mass)** -- `COMPUTED (KNOWN-FRAMEWORK)`
  - *Computation & Inputs:* With `mdot = 0.10 dotM_in c^2 / L_Edd`, the assigned luminosity is `lambda = mdot` below two and `2(1 + ln(mdot/2))` above. Mass conservation gives retained growth proportional to `mdot - 0.10 lambda`, not `0.90 mdot` above saturation. With no outflows and constant coefficients, `mdot = 3, 5` gives `273.78, 161.23 Myr` for a `100 M_sun` seed to reach `1.5e9 M_sun`.
  - *Binary limits:* The projection `0.0438` uses a point velocity and assumed enclosed mass, not a measured inclination. The chirp mass is `6.4735e8 M_sun`. Circular isolated Peters clocks at `0.05-0.10 pc` are `3.19-50.99 Myr`. Reaching those separations and predicting a stochastic background require hardening and population models that are absent.
  - *Lean Arithmetic Lemma (`PROVEN (ARITHMETIC-LEMMA)` in `formal/Wave12QuasarCollapse.lean`):* Checks `100 < 123`, `100 < 107`, and `19 * 647^5 < 15^3 * 4^3 * 10^10 < 19 * 648^5`.
