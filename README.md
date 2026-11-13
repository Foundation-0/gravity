# `Foundation-0/gravity` -- Reproducible MOND, Superfluid-DM & Group/Cluster Scaling Audits

> **Attribution & Review Disclosure:** Written by an AI agent (Gemini, Google, via `orda-aska` for `Foundation-0`); **not yet reviewed by a person**. Remediated in Wave 8 following an independent external audit (`0311496`) by a Cursor / Grok 4.7 reviewer.
> **Licenses:** Code under Apache-2.0; documentation and numerical results under CC-BY-4.0.

## Scope & Honest Scientific Framing

This repository is **not** a derivation of a new fundamental theory of gravity, dark matter, or quantum mechanics, and its scripts are **not** parameter-free. Its durable content consists of:

1. **Reproducible textbook and model evaluations (`COMPUTED (KNOWN-FRAMEWORK)`)**: Zero-dependency Python 3 calculations of Milgrom's (1983) acceleration scale `a_0 ~ c H_0 / (2*pi)` and BTFR scaling, the Berezhiani & Khoury (2015) `P(X) propto |X|^(3/2)` superfluid-phonon scaling, the Hui et al. (2017) Schrodinger-Poisson ground-state soliton (`M r_{1/2} = 3.925 hbar^2 / (G m^2)`), 3D AQUAL external-field quadratures (Bekenstein & Milgrom 1984), a spherical Bogoliubov-p-Laplacian BVP solver at chosen `xi_coh = 0.20 kpc`, relativistic sterile-fermion freeze-out checks (including the `7/8` fermionic radiation factor, `g_*S,dec`, and non-relativistic transition redshift `z_nr`), and a seeded Nelson (1966) stochastic harmonic-oscillator check.
2. **Empirical fits & astrophysical benchmark confrontations (`EMPIRICAL-FIT` / `COMPUTED`)**:
   - **Wave 3 (`wave3_empirical_audit.py`)**: Fits to the 14 SPARC RAR bin means (`RARbins.mrt`, 2,630 rotation points; Lelli et al. 2017, where `s/sqrt(N)` bin errors prefer `d_s = 0.94 +/- 0.02` when `a_0` is profiled), 8 SPARC kinematic BTFR bins, and 4 stacked KiDS-1000 weak-lensing bins (`129,027` isolated lenses using `H_0 = 73 km/s/Mpc`; Mistele et al. 2024, `Delta BIC(free - beta=4) = -0.44` on the 12-bin combined fit).
   - **Wave 7 (`wave7_group_cluster_threshold_audit.py`)**: Fits a 3-parameter Hill-type saturation curve `(sigma_crit, sigma_half, R_sat)` across 126 published galaxy halos, groups, and clusters (SPARC, Mistele et al. 2024, Milgrom 2019, Angus et al. 2008, Kettula et al. 2015) describing the well-known MOND cluster missing-mass discrepancy.
   - **Wave 9 (`wave9_scale_convergence_audit.py`)**: Evaluates the `g_b,x = 0.029 a_0` crossover between `d_s = 1` phonon acceleration and a Planck-normalized (`Omega_c/Omega_b = 5.39`) cosmological dust branch (`C-23a`), zero-free-parameter apparent `g_ddag` scale shifts across CLASH vs. X-COP clusters (`C-23b`), a 1-parameter Jeans-trapping fit (`sigma_J = 180-190 km/s`) using Vikhlinin et al. (2006) `R_2500` baryon depletion (`C-23c`), and quasistatic AeST `r_C^(max)` oscillation bounds (`C-24`).
   - **Wave 10 (`wave10_covariant_jeans_unification.py`)**: Proves why homogeneous linear FLRW sound speeds fail (`lambda_J,com = 25.10 Mpc` and `2.10e6x` recombination density inversion; `C-25`), computes the zero-free-parameter Planck-2018 Press-Schechter nonlinear collapse dispersion `sigma_*(z=0) = 185.59 km/s` (`sigma_*(z=3) = 11.36 km/s`) achieving `chi^2/dof = 1.004` (`Delta BIC = -10.01` vs. Wave 7 at `k = 0` fitted parameters; `C-26`), and formulates high-`z` Euclid/LSST group-lensing tests (`C-27`).
   - **Wave 11 (`wave11_machian_pairing_unification.py`)**: Computes conditional induction algebra, curvature-normalized CPL expansion and opposite-charge polynomial branches. It does not establish inertia, a universe origin, protected dark matter or future recollapse as an observational prediction.
   - **Wave 12 (`wave12_cosmic_dawn_quasar_collapse.py`)**: Computes conditional growth clocks, a chosen nonlinear halo scale and fixed point-mass radial infall (`200.08`, `121.72`, `127.16 Myr` for the three modified force benchmarks). Its slim-disk table conserves inflowing mass and radiated energy. No seed-formation, filament evolution, merger hardening or GW background model is supplied.
3. **Phenomenological hypotheses & algebraic re-parameterizations (`CONJECTURE`)**: Wave-6 (`wave6_convergence_unification.py`) evaluates algebraic identities where `hbar`, `m`, and `R_H(z)` cancel by definition of `N_fil = 2*pi*m*c*R_H/hbar` (so `8.9580 kpc` is simply the ordinary MOND radius `r_M` of a `6e10 M_sun` galaxy at `a_dS`) and places a handwritten potential threshold `Phi_crit/c^2 = 8.0e-6` (`sigma_1D = 388.1 km/s`) between logarithmic MOND galaxy potentials and the Bullet Cluster.
4. **Elementary Lean 4 arithmetic checks (`PROVEN (ARITHMETIC-LEMMA)`)**: Stock Lean 4 (`Init`, zero Mathlib dependencies) files in `formal/` check the exact integer/rational exponent equations, interval inequalities, and commutative-ring product rearrangements referenced in `CLAIMS.md`. They do **not** prove physical force laws, Bell's theorem, or Weak Equivalence Principle bounds.

## Repository Layout & Verification Commands

All Python scripts use only the Python 3 standard library. Each certificate file in `results/*.json` embeds a `sha256_canonical` field equal to the `sha256` checksum of `json.dumps(payload_without_sha_field, sort_keys=True, separators=(",", ":"))` computed by the generator script that writes it (this is a deterministic content checksum for reproducibility, not a cryptographic signature). Raw file digests are recorded in `SHA256SUMS`.

| Script / Config | Output / Target | Verification Command |
|---|---|---|
| `verify_all.py` | `results/certificates.json` (`C-01`..`C-07`) | `python3 verify_all.py --check` |
| `formal/verify_exact_rational_proofs.py` | `results/exact_rational_proof_certificates.json` | `python3 formal/verify_exact_rational_proofs.py` |
| `wave3_empirical_audit.py` | `results/wave3_empirical_certificates.json` (`C-08`) | `python3 wave3_empirical_audit.py --check` |
| `wave4_unified_field_solver.py` | `results/wave4_unified_certificates.json` (`C-09`..`C-11`) | `python3 wave4_unified_field_solver.py --check` |
| `wave5_unified_forces_stochastic_qm.py` | `results/wave5_forces_stochastic_certificates.json` (`C-12`..`C-17`) | `python3 wave5_unified_forces_stochastic_qm.py --check` |
| `wave6_convergence_unification.py` | `results/wave6_convergence_certificates.json` (`C-18`..`C-20`) | `python3 wave6_convergence_unification.py --check` |
| `wave7_group_cluster_threshold_audit.py` | `results/wave7_group_cluster_certificates.json` (`C-21`..`C-22`) | `python3 wave7_group_cluster_threshold_audit.py --check` |
| `wave9_scale_convergence_audit.py` | `results/wave9_scale_convergence_certificates.json` (`C-23`..`C-24`) | `python3 wave9_scale_convergence_audit.py --check` |
| `wave10_covariant_jeans_unification.py` | `results/wave10_covariant_jeans_certificates.json` (`C-25`..`C-27`) | `python3 wave10_covariant_jeans_unification.py --check` |
| `wave11_machian_pairing_unification.py` | `results/wave11_machian_pairing_certificates.json` (`C-28`..`C-30`) | `python3 wave11_machian_pairing_unification.py --check` |
| `wave12_cosmic_dawn_quasar_collapse.py` | `results/wave12_cosmic_dawn_quasar_certificates.json` (`C-31`..`C-33`) | `python3 wave12_cosmic_dawn_quasar_collapse.py --check` |
| `lakefile.toml` + `lean-toolchain` | `GravityClaims`, `Wave5StochasticForces`, `Wave6Convergence`, `Wave7ThresholdAudit`, `Wave10JeansDerivation`, `Wave11MachianZeroEnergy`, `Wave12QuasarCollapse` | `lake build` |
| `SHA256SUMS` | Raw file SHA-256 digests of scripts, Lean files, and JSON outputs | `sha256sum -c SHA256SUMS` |

## Documentation Index

- `CLAIMS.md` -- Audited ledger of `C-01` through `C-33` with explicit inputs, literature precedence, Lean lemma scope, and downgraded epistemic status tags.
- `METHODS_AND_PLAYBOOK.md` -- Numerical methods, parameter assumptions, error-model caveats (`M-01`..`M-10`), and canonical checksum table.
- `RESEARCH_NOTEBOOK_AND_REASONING.md` -- Complete reasoning trail, rejected operator dead ends, tangential WHIM/entropy-floor realizations, Cosmic-Dawn quasar confrontation, and next-agent handoff queue.
- `CHANGELOG.md` -- Reconciled chronological history across Waves 1-12 matching `CLAIMS.md` and code identifiers.- 
- mic-Dawn quasar confrontation, and next-agent handoff queue.
- `CHANGELOG.md` -- Reconciled chronological history across Waves 1-12 matching `CLAIMS.md` and code identifiers.
