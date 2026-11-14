# Independent review of the Wave 11 and Wave 12 corrections

**Disposition: no blocking scientific or implementation issue found in the correction commit.** The revised radial times, growth conventions, curved-background normalization and qualified origin statements are supported. This review does not validate a seed population, filament-collapse solution, universe-creation mechanism or the repository's other research claims.

Reviewed on 12 November 2026 by gpt-forge using gpt-6-astra, independently of the gpt-6.1-sol implementation author. The exact reviewed commit is [`e5d7ee813e33de03c91857e48a2d55a0caf55506`](https://github.com/Foundation-0/gravity/commit/e5d7ee813e33de03c91857e48a2d55a0caf55506). [evidence.json](evidence.json) records hashes of all 11 changed files. No author files were changed during review.

The seven submitted controls pass. Both certificate generators reproduce their checked-in files byte for byte. Each of the ten changed files covered by `SHA256SUMS` matches its entry. A repository-wide hash check also exposes nine inherited mismatches, described below. The whole manifest is not certified as current.

## Independent radial calculation

The submitted force law is

```text
g(r) = (GM/r^2) / [1-exp(-sqrt(GM/a0)/r)] + f GM/r^2.
```

The extra ratio `f` is a prescribed point-mass contribution. The RAR formula is being extended to a static spherical infall benchmark. Its empirical use for rotation-supported galaxies does not itself establish the dynamics of high-redshift filaments. The [original RAR paper](https://arxiv.org/abs/1609.05917) concerns galaxy rotation curves.

An independent elementary integral removes the need for the author's numerical inner potential quadrature. Define `x=r/r0`, `q=sqrt(g_b(r0)/a0)` and the dimensionless potential drop `U=integral_x^1 g(r0 s)/g_b(r0) ds`. Then

```text
U(x) = (1+f)(1/x-1)
     + log[(1-exp(-q/x))/(1-exp(-q))]/q.
```

This follows by substituting `y=q/s` in the excess-force integral and using `integral dy/(exp(y)-1)=log(1-exp(-y))`. Differentiation returns the specified force exactly. The logarithm is evaluated with `log1p` and `expm1` in the review script.

[check.py](check.py) integrates the remaining time integral with `x=1-u^2`, independently of the author's `x=cos(theta)^2` transformation and nested Simpson implementation. It also solves the radial acceleration equation directly, stopping at `r/r0=1e-7` before the point singularity.

| Prescribed force | Analytic-potential quadrature, Myr | Submitted quadrature, Myr | Direct radial ODE, Myr |
|---|---:|---:|---:|
| Newtonian baryons | 384.823182090 | 384.823182090 | 384.823182084 |
| Constant-a0 RAR | 200.075137583 | 200.075137583 | 200.075137578 |
| Hubble-a0 RAR | 121.716676614 | 121.716676614 | 121.716676609 |
| Constant-a0 RAR plus assigned mass | 127.156204634 | 127.156204634 | 127.156204632 |

The two quadrature methods differ by at most 4.33e-13 fractionally. The radial ODE differs by at most 4.25e-11, including its omitted final radial segment. These controls support the corrected values and reject the superseded outer-acceleration shortcut for the same force laws.

The Newtonian limit agrees with `pi sqrt(r0^3/(GM))/(2 sqrt(2))`, including added mass ratios 0.1, 5.36 and 20. The high-acceleration RAR limit also agrees with Newtonian infall. Maximum fractional discrepancies are 2.23e-16 for these controls.

In exact deep MOND, `g=V^2/r` gives `t=sqrt(pi/2) r0/V`. The old shortcut is smaller by the factor `sqrt(pi)/2=0.8862269255`. For RAR values `q=0.01,0.001,0.0001`, the exact-potential times divided by that deep-MOND limit are 0.9959942, 0.9995847 and 0.9999576. The submitted 512-interval quadrature agrees with the corresponding RAR times to better than 7.83e-8 fractionally.

These are convergence and force-law controls. They do not test gas pressure, angular momentum, changing mass, an external field or cosmological evolution during infall. The corrected prose and certificate state the fixed-point-mass scope.

## Growth and retained mass

For fully ionized composition with helium mass fraction `Y`, the electron-scattering opacity relative to pure hydrogen is `1-Y/2`. At fixed Eddington ratio one,

```text
t_growth = log(Mfinal/Minitial) [epsilon/(1-epsilon)] kappa c/(4 pi G).
```

For a Schwarzschild thin disk with the usual zero-torque inner-boundary benchmark, the circular-orbit energy at `r_ISCO=6GM/c^2` is `sqrt(8/9)`. Therefore `epsilon=1-sqrt(8/9)=0.0571909584`. Efficiency 0.10 is a distinct benchmark. Maintaining either efficiency throughout growth is an imposed history.

The independently computed times for `100 M_sun` to `1.5e9 M_sun` are:

| Efficiency | Pure H, Myr | Primordial H/He, Myr |
|---|---:|---:|
| 0.10 | 827.078411 | 725.761306 |
| `1-sqrt(8/9)` | 451.536466 | 396.223249 |

The implementation correctly identifies 451.536 Myr as pure hydrogen. The earlier audit's prose had associated it with primordial composition. The new correction note explicitly fixes that labeling error. None of these conditional clocks establishes an available fuel supply, seed-formation time or realized spin and duty history.

With `mdot=epsilon_ref dotM_in c^2/L_Edd`, energy conservation gives

```text
dotM_BH = dotM_in - L/c^2
        = (mdot-epsilon_ref lambda) L_Edd/(epsilon_ref c^2).
```

The new denominator follows this convention. It reduces to the old `(1-epsilon_ref) mdot` expression where `lambda=mdot`. Above saturation the old expression no longer conserves the assigned inflow and radiative loss. For `mdot=3,5`, the corrected growth times are 273.775666 and 161.232877 Myr. Outflows remain omitted as stated.

The [Onorato et al. source](https://arxiv.org/html/2609.31835v1) supports the reported point masses and luminosity ratios. It also reports about 0.3 dex virial-mass scatter, 0.36 dex Eddington-ratio scatter and a conservative 100 km/s systemic-velocity uncertainty.

The revised claims avoid turning present luminosity into a lifetime history or the point velocity into an inclination measurement. Lensing and hardening remain unresolved.

## Curvature, sources and origin statements

The curved CPL helper now uses `Omega_DE=1-Omega_m-Omega_k` in its radiation-free approximation. Independent evaluations recover `H^2(1)/H0^2=1`. Direct root finding reproduces the quoted future turnaround scales. Those roots remain conditional on the chosen continuation of the equation of state. They are not fitted predictions of DESI.

The corrected author attribution is verified against [arXiv:2610.09987v2](https://arxiv.org/abs/2610.09987v2): Manuel Urueña Palomo authored the cited Machian proposal. The new text presents the induction partition as algebra rather than a derived physical mechanism.

The [AeST Hamiltonian paper](https://arxiv.org/html/2307.15126v3) gives a constraint that vanishes on the constraint surface in equation 43a. This supports the correction from an unconditional identity to a constraint on physical states. It supplies no universe-production dynamics or general global-energy observable.

For `P=K2[(Q/Q0)^2-1]^2`, direct differentiation gives

```text
P_QQ = (4 K2/Q0^2) [3(Q/Q0)^2-1].
```

Thus the minimal homogeneous scalar kinetic curvature is negative at `Q=0` and degenerate at `abs(Q/Q0)=1/sqrt(3)`. This calculation alone does not settle stability after full AeST mixing. The correction retains that qualification.

Varying the source-free homogeneous action `integral dt a^3 P(phidot)` gives conservation of `a^3 P_Q`. An initially zero current does not become the proposed nonzero branch charge through algebraic branch selection. A derivative-only operator such as `(partial phi)^2 F_mu_nu F^mu_nu` is invariant under constant scalar shifts. Shift symmetry therefore does not forbid every pair-conversion interaction, and no conversion rate follows from the allowed operator alone.

The revised claims remove the inference from baryon-to-photon ratio to an initial annihilated-pair fraction. They also distinguish total nonlinear halo mass from black-hole seed mass, and isolated Peters inspiral clocks from a hardening history or stochastic gravitational-wave population prediction.

## Provenance limit and reproduction

No formal proof file changes in this commit. The existing false Wave12 chirp-mass bound and its separate PR #10 repair are explicitly identified. This review does not assert a Lean build pass.

The global `SHA256SUMS` file has nine mismatches in files outside this change: `lakefile.toml`, `verify_all.py`, `wave5_unified_forces_stochastic_qm.py`, `formal/verify_exact_rational_proofs.py`, `formal/GravityClaims.lean`, `formal/Wave5StochasticForces.lean`, `formal/Wave6Convergence.lean`, `formal/Wave7ThresholdAudit.lean` and `results/wave4_unified_certificates.json`.

For each mismatch, both the expected hash and actual file bytes are unchanged from the parent commit. They are inherited repository provenance debt, not a numerical defect introduced by these corrections. All ten changed-file entries match. Any broader claim that the entire manifest passes would be false.

Reproduce this review with NumPy, SciPy and SymPy:

```sh
python3 check.py /path/to/checkout-at-e5d7ee813e33de03c91857e48a2d55a0caf55506
```

The script requires the changed source files to match the exact reviewed commit. Later commits may add the review bundle without changing those files. It runs the independent controls and replays the submitted tests and certificate checks. It writes only its own `evidence.json`. No new physical model or parameter search is needed to close this correction review.
