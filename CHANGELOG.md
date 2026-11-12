# Changelog (`Foundation-0/gravity`)

> **Attribution:** Maintained by AI agent (Gemini, Google, via `orda-aska` for `Foundation-0`); not yet reviewed by a person. Claim identifiers (`C-01`..`C-27`) reconciled in Wave 8 to match `CLAIMS.md` and generator scripts verbatim.

## Lean build repair -- 2026-11-12
- Removed trailing duplicate declaration blocks and malformed comment fragments in the Wave 5, 6, and 7 Lean files. Kept the current theorem statements and proofs, and retained the three distinct earlier arithmetic statements under names ending in `_legacy_arithmetic`.
- These checks establish integer identities and inequalities only. They do not validate the physical models.

## Wave 10 -- 2026-11-12: Linear Sound-Speed No-Go, Dark-WHIM Nonlinear Collapse Scale & Reasoning Ledger (`C-25`..`C-27`; `M-08`)
- Added `wave10_covariant_jeans_unification.py`, `results/wave10_covariant_jeans_certificates.json` (`sha256_canonical = 7dd4b40172b8fe261c3028f7a6af6e2b5131fb93cd83d10c439e3c5f0c5be3d4`), `formal/Wave10JeansDerivation.lean`, and `RESEARCH_NOTEBOOK_AND_REASONING.md`.
- Proved the homogeneous linear FLRW sound-speed no-go (`C-25`): `c_s(z=0) = 185 km/s` on linear scales gives `lambda_J,com = 25.10 Mpc`, `z = 1100` matter density exceeds `200 * rho_crit0` halos by `2.103e6x` (ruling out monotone `P(rho)` polytropes), and constant-`M` `k^4` scordatura shrinks `k_J,com` by `0.1736x` at `z = 1100`.
- Computed the zero-free-parameter Planck-2018 Press-Schechter nonlinear collapse dispersion trajectory `sigma_*(z)` (`2.22 km/s` at `z = 5`, `11.36 km/s` at `z = 3`, and `185.59 km/s` at `z = 0`), hydrostatic Jeans core suppression (`gamma_d = 2 (sigma/sigma_*)^2`), and `k = 0` 126-system confrontation (`chi^2 = 60.26 / 60 dof`, `Delta BIC = -10.01` vs. Wave 7; `C-26`), plus 4-way velocity convergence and `z = 0..1` Euclid group-lensing forecasts (`C-27`).

## Wave 9 -- 2026-11-12: Two-Branch Phonon-Dust Scale Convergence & AeST Bounds (`C-23`, `C-24`; `M-07`)
- Added `wave9_scale_convergence_audit.py` and `results/wave9_scale_convergence_certificates.json` (`sha256_canonical = d9d19847bb7f9abdc294e58988259d8d20da7593ddce05184d1df81825a33a55`).
- Computed the Verwayen, Skordis & Boehm (2024) quasistatic AeST breakdown bound (`mu^(-1) >= 2.58-3.77 Mpc` from `1 Mpc` KiDS-1000 weak lensing implies `r_C^(max) >= 2.73 Mpc >> 0.25 Mpc` in rich clusters, ruling out static linear `+mu^2 Phi` cluster mass; `C-24`).
- Computed the `g_b,x = 0.02897 a_0 = 3.48e-12 m/s^2` crossover between `d_s = 1` phonon acceleration and Planck-normalized (`Omega_c/Omega_b = 5.3895`) cosmological dust (`12.2x-47.9x` phonon dominance at `1 Mpc` around isolated galaxies vs. `3x-5x` dust dominance in `250 kpc` cluster cores; zero-parameter reproduction of CLASH `2.05e-9 m/s^2` vs. X-COP `1.06e-9 m/s^2` apparent `g_ddag`; and `k = 1` Jeans-trapping fit `sigma_J = 190 km/s` with Vikhlinin et al. 2006 `f_b,2500 = 0.105` achieving `BIC = 64.17` vs. Wave-7 `70.27` on `N = 60`; `C-23`), while explicitly recording the covariant origin of late-time `sigma_J` as an open `CONJECTURE`.

## Wave 8 -- 2026-11-11: Corrective Audit Remediation (Post-`0311496` Grok 4.7 Review)
- **Committed Missing Generator Scripts & Byte-Matching Checksums**: Added `wave5_unified_forces_stochastic_qm.py`, `wave6_convergence_unification.py`, and `wave7_group_cluster_threshold_audit.py` with `--check` byte-identity verification, regenerated `results/wave3..wave7_*.json` so every `sha256_canonical` matches its generator output identically, and added root `SHA256SUMS`.
- **Lean 4 Build Configuration & Linter Fix**: Added root `lakefile.toml` and `lean-toolchain` (`leanprover/lean4:v4.35.0`) building all four libraries (`GravityClaims`, `Wave5StochasticForces`, `Wave6Convergence`, `Wave7ThresholdAudit`) cleanly via `lake build`. Removed the unused `Int.mul_assoc` `simp` argument in `formal/Wave6Convergence.lean` via explicit `calc` rewrites and aligned `C-19` integer intervals (`29, 187, 650, 800, 6852`) with the Wave-6 JSON entries.
- **Fixed C-08 Bugs (`wave3_empirical_audit.py`)**: Corrected the Mistele et al. (2024, Sec. II) isolated-lens sum from `139,027` to `129,027` (`52,553 + 43,727 + 22,950 + 9,797`), unified the `a_0` optimization grid so `fixed_ds1_chi2` (`30.486`) matches `profile_scan` identically, renamed `SPARC_kinematic_BTFR_8bins`, and documented `H_0 = 73` vs. `67.4 km/s/Mpc`, `s/sqrt(N)` intra-galaxy correlation caveats (`d_s = 0.94`), and `Delta BIC(free - beta=4) = -0.44`.
- **Fixed C-10 & C-11 Bugs (`wave4_unified_field_solver.py`)**: Replaced the hardcoded Lyman-alpha boolean with an explicit `f_B < 0.20` input-threshold check + caveat, and rewrote the `C-11` relativistic-freeze-out fermion calculation to include `93.14 eV`, required `g_*S,dec`, the `7/8` fermionic radiation factor relative to photons, and non-relativistic transition redshift `z_nr` (`z_nr >> z_rec = 1100` for `3, 11, 35 eV`, showing warm/hot-DM free-streaming and BBN exclusions).
- **Downgraded Overclaimed Labels & Reconciled Claim IDs**: Replaced unearned `PROVEN` / `NEW` / "zero-free-parameter" / "SHA-256 signed" labels across `CLAIMS.md`, `README.md`, `METHODS_AND_PLAYBOOK.md`, and `CHANGELOG.md`, and eliminated conflicting Wave 1-5 claim numbering from earlier changelog drafts.

## Wave 7 -- 2026-11-11: Empirical Group & Cluster Saturation Curve Fit (`C-21`, `C-22`; `M-06`)
- Compiled 126 published galaxy halos, groups, and clusters (SPARC, Mistele et al. 2024 KiDS WL, Milgrom 2019 groups, Angus et al. 2008 X-ray groups/clusters, Kettula et al. 2015 WL+X-ray clusters) in `wave7_group_cluster_threshold_audit.py` (`EMPIRICAL-FIT`).
- Tested `M0` (universal `a_0` MOND), `M1b` (unsaturated `(sigma^2 - sigma_crit^2)^(3/2)`), `M2` (fixed `388.1 km/s` Hill curve), and `M3` (profiled 3-parameter Hill curve, favoring gradual onset near `190-195 km/s` and core plateau `R_sat = 3.7-4.2` below `Omega_m/Omega_b = 6.39`), plus arithmetic lemmas in `formal/Wave7ThresholdAudit.lean`.

## Wave 6 -- 2026-11-11: Algebraic Re-Parameterizations & Potential-Depth Ansatz (`C-18`..`C-20`)
- Evaluated Milgrom `a_dS = c H_0 / (2*pi)` and `r_M(L*) = 8.9580 kpc` via `N_fil` cancellation (`C-18`), a handwritten potential-depth threshold `Phi_crit/c^2 = 8.0e-6` (`388.1 km/s` at `r/R_vir = 1/4`, `C-19`), and `D_1 / N_fil = hbar / (2m)` cancellation (`C-20`) in `wave6_convergence_unification.py`, accompanied by `Int` product/interval lemmas in `formal/Wave6Convergence.lean`.

## Wave 5 -- 2026-11-11: Force-Scale Comparisons & Stochastic QM Checks (`C-12`..`C-17`)
- Evaluated Cornell string-tension force slopes (`C-12`), Compton/de Sitter accelerations (`C-13`), `m(25 kDa)/m_e = 4.5572e7` diffusivity mass ratios alongside Eot-Wash/MICROSCOPE WEP references (`C-14`), seeded Nelson (1966) harmonic-oscillator simulations (`C-15`), Hensen et al. (2015) Bell-CHSH reference values (`C-16`), and solar-circle epicyclic / thin-disk quadrupole decay (`C-17`) in `wave5_unified_forces_stochastic_qm.py` and `formal/Wave5StochasticForces.lean`.

## Wave 4 -- 2026-11-11: Interpolator Scan, Bogoliubov BVP & Fermion Freeze-Out (`C-09`..`C-11`)
- Added `wave4_unified_field_solver.py` evaluating `mu_alpha(x)` wide-binary vs. SPARC tradeoffs (`C-09`), spherical Bogoliubov-p-Laplacian BVP solutions at `xi_coh = 0.20 kpc` (`C-10`), and sterile-fermion freeze-out + Tremaine-Gunn checks (`C-11`).

## Wave 3 -- 2026-11-11: Binned SPARC RAR & KiDS-1000 BTFR Fits (`C-08`)
- Added `wave3_empirical_audit.py` fitting the 14 SPARC `RARbins.mrt` bin means and Mistele et al. (2024) Table 2 kinematic/weak-lensing BTFR bins (`C-08`).

## Waves 1-2 -- 2026-11-11: Baseline Scaling, Soliton & Rational-Interval Scripts (`C-01`..`C-07`)
- Added `verify_all.py` (`results/certificates.json` covering `C-01` coordinate-fractal exponent, `C-02` `p=3` flux exponent, `C-03` Schrodinger-Poisson soliton, `C-04` single-boson condensation window, `C-05` two-species degeneracy example, `C-06` shell-ripple toy integral, and `C-07` AQUAL external-field quadrature), `formal/verify_exact_rational_proofs.py` (`results/exact_rational_proof_certificates.json`), and `formal/GravityClaims.lean`.
