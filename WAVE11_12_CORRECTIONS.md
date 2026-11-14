# Wave 11 and Wave 12 corrections

These changes implement reviewed numerical and interpretation findings for conditional benchmarks. They do not introduce a new physical model. Prepared by gpt-forge using GPT-6.1 Sol. Independent implementation review is pending.

The [prior public audit](https://github.com/Foundation-0/gravity/pull/11) records the independent derivations and sources. The chirp-mass Lean repair remains a separate change. No Lean files change here.

## Radial infall

For release from rest, energy conservation gives `v(r)^2 = 2 integral_r^r0 g(s) ds` and `t = integral_0^r0 dr/v(r)`. The earlier code substituted `g(r0)` into the Newtonian point-mass formula. That formula's coefficient depends on the full inverse-square force law.

The corrected calculation separates the Newtonian potential analytically. It integrates the RAR excess in log radius, where the scaled integrand `y/expm1(y)` is bounded by one. The outer substitution `r/r0 = cos(theta)^2` removes both time-integral endpoint singularities. Adaptive Simpson quadrature raises an error if it exhausts its depth. The outer integral uses composite Simpson quadrature.

| Fixed force at all radii | Earlier shortcut, Myr | Integrated time, Myr |
|---|---:|---:|
| Newtonian baryonic point mass | 384.823 | 384.823 |
| RAR, constant a0 | 182.27 | 200.075 |
| RAR, Hubble-scaled a0 at the observation epoch | 109.04 | 121.717 |
| Constant-a0 RAR plus the assigned condensate force | 122.79 | 127.156 |

The baryonic point mass is `5e10 M_sun`. The initial radius is `30 pkpc`. Newtonian infall agrees with `pi sqrt(r0^3/(GM))/(2 sqrt(2))`. In deep MOND, `g = V^2/r` gives `t = sqrt(pi/2) r0/V`. The earlier shortcut divided by that exact result is `sqrt(pi)/2`. A separate test approaches this limit with a small Newtonian core.

Constant-a0 results at 64, 128 and 256 outer intervals agree within `2e-9 Myr`. This is a numerical control for a fixed point-mass model. It does not describe a filament, evolving halo, pressure, angular momentum, cooling, seed formation or dynamical friction.

## Growth and mass flow

The growth budget from z=20 is still `734.100 Myr`. At fixed Eddington ratio one, a `100 M_sun` seed needs the following time to reach `1.5e9 M_sun`:

| Fixed radiative efficiency | Pure H, Myr | Primordial H/He, Myr |
|---|---:|---:|
| 0.10 benchmark | 827.078 | 725.761 |
| `1 - sqrt(8/9)` Schwarzschild thin disk | 451.536 | 396.223 |

The prior audit's prose associated `451.536 Myr` with primordial composition. That value is the pure-H result. Both conventions are explicit here. These counterexamples concern conditional clocks. They do not establish any realized accretion history. Fixed spin, efficiency, opacity, duty and fuel are assumptions.

The slim-disk convention is `mdot = epsilon_ref dotM_in c^2/L_Edd`, with `epsilon_ref=0.10`. The assigned luminosity is `lambda=mdot` below two and `lambda=2(1+ln(mdot/2))` above. Conservation gives `dotM_BH=(mdot-epsilon_ref lambda)L_Edd/(epsilon_ref c^2)`. The old `0.90 mdot` prescription agrees only in the unsaturated regime. Outflows are omitted.

## Curvature and interpretation

Each curved CPL example now uses `Omega_DE = 1 - Omega_m - Omega_k`. Its present value is therefore `H^2(1)/H0^2 = 1`. The extrapolated equation of state remains a chosen future continuation, not a fit or an observed recollapse prediction.

The cited arXiv identifier 2610.09987v2 belongs to [Manuel Urueña Palomo](https://arxiv.org/abs/2610.09987v2), not Braun. The induction partition and critical-density substitution are algebraic benchmarks. A Hamiltonian constraint does not establish universe creation or a globally observable energy cancellation.

The polynomial's symmetric origin has `P_QQ(0)=-4 K2/Q0^2` in its minimal scalar sector. Source-free homogeneous shift symmetry conserves `a^3 P_Q`. Algebraically selecting nonzero opposite-charge branches does not derive their production from zero current. Full mixing stability remains unsolved. Constant shift symmetry allows derivative portals, so it does not forbid every conversion process. No portal rate is calculated.

## Certificate changes and checks

Both certificate schemas advance from 1.0 to 1.1. Wave 11 renames `unbroken_creation_state_u0` to `symmetric_polynomial_state_u0`, removes the inferred annihilated-pair fraction, and adds curvature closure and origin limitations. Wave 12 renames `feeder_filament_30pkpc_5e10Msun_infall` to `fixed_point_mass_30pkpc_5e10Msun_radial_infall`, adds growth counterexamples and convergence data, and labels the orbital projection as illustrative.

Only the two affected certificates are regenerated. Existing unchanged hash entries are retained. Updated entries cover changed tracked files, with new entries for these two generators, certificates, controls and this note.

```sh
python3 -m unittest test_wave11_12_corrections.py
python3 wave11_machian_pairing_unification.py --check
python3 wave12_cosmic_dawn_quasar_collapse.py --check
```

The seven tests cover Newtonian and deep-MOND limits, convergence, mass conservation, low-inflow equivalence, opacity and efficiency counterexamples, curved density closure and the polynomial's kinetic curvature. They do not verify an origin mechanism, observational likelihood or unmodified Lean build.
