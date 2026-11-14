# Wave 11 and Wave 12 research value audit

The new Wave 12 establishes reproducible numerical provenance for the quoted 83,900-solar-mass scale. It does not establish a black-hole seed, a new collapse mechanism, or evidence against standard cosmology. Its formal chirp-mass theorem is false as written. The Python chirp mass is correct.

The defensible call is to reject the current seed-formation inference, retain the calculations as conditional benchmarks, and pursue only a bounded observational test with a distinct contribution beyond published work.

Audited snapshot: Foundation-0/gravity `70a1204a536b3dca0b3053d1a056daf22601ac00`. Compared with cosmic-dawn audit `5b1cc2402029a97e4ab14e4b527f64eb4f1299fe` and convergence work `02013ae95fa5913894b829c8e2e63a3efcde9e63`. Wave 10 and Wave 11 source files are unchanged from the latter snapshot. Research model: gpt-6-astra, ultra reasoning. Author: gpt-forge. Human review pending.

| Route | Status | Decision | Decisive evidence |
|---|---|---|---|
| New 83,914 halo-mass calculation | Established numerical result within its inputs | Retain as benchmark | Extended spectrum converges, with explicit host dispersion. |
| 83,900 as a black-hole seed | Unsupported identification | Reject current formulation | The quantity is total halo mass. Its adopted baryon budget is 13,126 solar masses, and compactness is 4.19e-11. |
| Near-unity condensate trapping | Conditional prescription | Park physical interpretation | The fraction is assigned by a velocity law. No kinetic capture, shock-heating, or seed-formation solution is computed. |
| Light-seed growth exclusion | Conditional, not a general exclusion | Retain parameter-dependent clock | Primordial composition at efficiency 0.10 gives duty 0.989. Fixed Schwarzschild efficiency gives duty 0.615. |
| MOND feeder free-fall numbers | Falsified as exact infall solutions | Correct or relabel estimates | Direct radial integration gives 200.08, 121.72, and 127.16 Myr instead of 182.27, 109.04, and 122.79. |
| Chirp mass and circular GW clock | Established conditional arithmetic | Retain after proof repair | Python gives 6.47351308e8 solar masses. Lean fails because one power of four is missing. |
| Quasar pairing as evidence for new gravity | Unresolved | Park | One candidate, unresolved lensing, and an extrapolated clustering baseline do not define a comparative likelihood. |
| Machian inertia and zero-energy creation | Algebra established, mechanism unresolved | Park | Critical-density substitution and arithmetic partition are not a derivation of inertia or universe creation. |
| DESI future turnaround | Conditional extrapolation | Reject as observational prediction | An equally past-compatible future equation of state has no turnaround. |
| CPT condensate origin and protected remnant | Algebra established, dynamics incomplete | Reject current mechanism claim | Negative kinetic curvature at the proposed origin, conserved-current obstruction, and allowed derivative portals. |
| Redshift evolution of acceleration scale | Conditional, observationally testable | Pursue bounded identifiability work | Large forecast separation exists, but published work already compares the simple scalings. |

**What changed since the earlier cosmic-dawn audit.** The [new source](https://github.com/Foundation-0/gravity/blob/70a1204a536b3dca0b3053d1a056daf22601ac00/wave12_cosmic_dawn_quasar_collapse.py) now uses kmax=50,000 inverse Mpc, 1,200 Simpson intervals, z=6.0783, a Carroll-Press-Turner growth approximation, and halo dispersion 250/sqrt(2) km/s.

Lines 118-145 define the spectrum. Lines 225-259 define the halo mass and trapping law.

The independent probe reproduces Mstar=83,913.9617 solar masses, sigma=0.969924 km/s, and ftrap=0.9999698959. Refining to 12,800 intervals gives 83,913.9434. Extending kmax to 100,000 has negligible further effect. Wave 12 therefore resolves the missing numerical provenance and the earlier native-grid cutoff concern for this specific root.

The earlier audit's 81,906.563 value remains valid for its different Wave 10 conventions and z=6.08. Holding Wave 12's other inputs fixed while replacing approximate growth with the integrated matter-plus-Lambda growth gives 82,232.064 at z=6.0783. The new result is numerically reproducible, but the README's word “proves” overstates a spectrum approximation.

The mass remains the Lagrangian total matter mass inside the nonlinear collapse scale. Independently converting it gives R200=191.824 pc, 2GM/(R200 c²)=4.19e-11, baryon allotment 13,126 solar masses, and neutral-gas virial temperature about 139 K. None is a black-hole formation condition.

Conventional atomic-cooling direct collapse requires a much hotter host and suppression of fragmentation. See the [primary synchronized-halo study](https://arxiv.org/abs/1406.7020). This does not exclude a different formation mechanism, but Wave 12 provides no such solution.

The z=6 halo calculation cannot be assigned a z=20 seed age. At z=20 its native radius bracket has no nonlinear-scale root. This says nothing about rare high peaks forming early halos.

The code asserts almost complete trapping in an illustrative massive host and then describes deep central potentials and Chandrasekhar friction. Those processes require a phase-space distribution, a density profile, and evolution equations. The assigned fraction alone establishes none of them.

**Growth clocks.** Wave 12 correctly obtains 734.100 Myr between z=20 and observation, and 827.078 Myr for a 100-solar-mass seed to reach 1.5e9 solar masses with pure hydrogen, efficiency 0.10, and Eddington ratio one. This is a conditional shortfall.

Its own primordial H/He opacity convention changes the required time to 725.761 Myr, or duty 0.989. Efficiency 1-sqrt(8/9)=0.057191 changes it to 451.536 Myr, or duty 0.615. The [published growth analysis](https://academic.oup.com/mnras/article/496/1/888/5851753) describes the spin-dependent efficiency and the dependence on duty and Eddington ratio.

These are counterexamples to a universal time exclusion, not evidence that either accretion history occurred. Sustained coherent accretion can change spin, feedback can interrupt fuel, and seed formation takes time. Using the current Eddington ratio as the lifetime average is an additional assumption. The source's choice 0.10 is not the Schwarzschild thin-disc efficiency.

The [discovery paper](https://arxiv.org/html/2609.31835v1) reports about 0.36 dex systematic scatter in inferred Eddington ratios, adopts a conservative systemic-velocity uncertainty of 100 km/s, and leaves lensing unresolved. Therefore the point values 1.23 and 1.07 do not prove super-Eddington luminosity, and a projection factor derived from 15 km/s is not a measured orbital inclination.

The slim-disc table also needs its mass-flow convention stated. If mdot uses a reference efficiency of 0.10, and luminosity is the assigned saturated lambda, mass conservation gives growth proportional to mdot-0.10*lambda. The code uses 0.90*mdot. These coincide below saturation but differ above it. Outflows and duty are omitted. This remains a benchmark, not a formation calculation.

**Infall counterexample.** Lines 274-277 reuse the Newtonian point-mass time coefficient while substituting the acceleration evaluated only at the starting radius. MOND changes the radial force law, so that substitution is not an exact fall-time identity.

The probe integrates r''=-g(r), starting at rest at 30 kpc around a fixed baryonic point mass of 5e10 solar masses. It reproduces the Newtonian 384.823 Myr to numerical precision. The MOND constant-a0, Hubble-a0, and additive two-branch times are 200.075, 121.717, and 127.156 Myr, respectively. The published shortcuts underestimate these by 8.9%, 10.4%, and 3.4%.

There is also an analytic check. In deep MOND, g=V²/r. Energy conservation gives tff=sqrt(pi/2) r0/V. The source shortcut gives pi*r0/(2*sqrt(2)*V), smaller by sqrt(pi)/2. Neither calculation models a real filament's angular momentum, pressure, geometry, external field, or feedback.

**Formal and binary checks.** The [Wave 12 theorem](https://github.com/Foundation-0/gravity/blob/70a1204a536b3dca0b3053d1a056daf22601ac00/formal/Wave12QuasarCollapse.lean#L43) has middle expression 15³*4²*10¹⁰=540,000,000,000,000. Its asserted lower bound is 19*647⁵=2,154,145,352,572,133. The lower bound is false. Replacing 4² with 4³ gives 2,160,000,000,000,000, which lies within the stated bounds.

`lean formal/Wave12QuasarCollapse.lean` actually exits 1 and reports that `decide` proved the proposition false. Python's 647,351,308-solar-mass chirp value is correct. Even a repaired theorem would certify literal integer bounds and assumed ratios only. It would not prove the inferred masses, lensing exclusion, trapping, or seed formation.

The circular, isolated point-mass inspiral times reproduce the familiar [Peters calculation](https://thesis.caltech.edu/4296/). The code's negligible kpc-scale GW decay is a useful check. The later 0.05-0.10 pc merger clock assumes that the pair reaches those separations. The calculation supplies neither a hardening history nor a population merger rate, so it cannot predict a NANOGrav background contribution.

**Wave 11 boundaries.** Hubble compactness GM/(Rc²)=1/2 follows directly from rho_critical and R=c/H. The induction calculation assigns Kge=1/3 and computes Kgm=2/3. Its Lean theorem verifies arithmetic. It does not derive the physical partition from a relativistic cosmological perturbation calculation.

The citation “Braun 2026, arXiv:2610.09987” is mismatched. That identifier belongs to [Manuel Urueña Palomo's Machian proposal](https://arxiv.org/abs/2610.09987). A Hamiltonian constraint, as treated in the [AeST Hamiltonian paper](https://arxiv.org/abs/2307.15126), does not by itself specify a universe-creation process or a globally observable gravitational energy balance.

The DESI-style CPL parameters are inserted, not fitted. Their future extrapolation gives the saved a_slow and recollapse values. But all existing past observations are equally compatible with the same w(a) for a<=1 and, for a>1, w=-1+[0.25+1.10(a-1)]exp[-(a-1)]. This continuation matches w and dw/da at a=1 and tends toward -1. 

The [independent review](../closure/independent-review.md) strengthens the numerical check to an analytic positive lower bound on H² for every future scale factor.

For curvature -0.004, the alternative gives H²/H0²=0.11556556 at the source's alleged turnaround a=78.8, and tends to a positive constant. It is a constructive non-identifiability example. The [DESI primary analysis](https://arxiv.org/html/2503.14738v2) constrains past expansion within a parametrization, not this future continuation.

The source also retains the flat Omega_L when adding curvature, so its H²(1)/H0² is 1+Omega_k rather than one.

For the proposed CPT polynomial, positive branch density and opposite charge are valid algebra. However, P_QQ(0)=-4K2/Q0² for K2>0. In the minimal homogeneous scalar kinetic sector, the proposed origin has negative kinetic curvature. A continuous path to the stable branch passes a kinetic degeneracy at |u|=1/sqrt(3). Full AeST mixing could change stability, but no such analysis is supplied.

Moreover, source-free homogeneous shift symmetry gives a³P_Q=constant. Starting at u=0 gives zero current. Finite positive dust charge on each later sheet requires a specified boundary, source, or quantum-production prescription. Manually evaluating u=±(1+epsilon) does not derive that transition.

The [Scherrer model](https://arxiv.org/html/astro-ph/0402316v3) already supplies known near-extremum dust-like behavior, not this bifurcation.

The notebook's statement that shift symmetry forbids all pair annihilation is also too strong. The operator (partial_phi)² F_mu_nu F^mu_nu respects a constant shift and can permit scalar-pair conversion to photons. No portal coefficient or rate is specified. The baryon-to-photon ratio likewise does not directly measure the fraction of initial quark-antiquark pairs that annihilated.

The [Boyle-Finn-Turok model](https://arxiv.org/abs/1803.08928) is an existing CPT cosmology with a different particle-production mechanism. Citation to it does not derive this repository's two-sheet condensate or dark-to-baryon abundance.

**Remaining research value.** The useful observational distinction is a0 tracking H(z), sqrt(rho_DE), or a constant. Wave 11's two dynamic tracks differ by a factor 1.771 at z=1, or 0.248 dex in acceleration and about 15.4% in asymptotic speed at fixed baryon mass. This is a substantial conditional separation.

However, [MUSE-DARK III](https://doi.org/10.1051/0004-6361/202659230) already reports redshift evolution from 79 galaxies, and [Alcock's follow-up](https://doi.org/10.1093/mnras/stag1485) already compares constant, Hubble, and matter-density scalings with those binned measurements. Repeating the simple curve comparison has limited research value.

A justified next probe would jointly model individual-galaxy pressure support, inclination, baryonic mass calibration, redshift-dependent selection, and shared covariance, then compare the three explicit forecast families with a free common normalization.

First establish access to the required data and test identifiability on mocks. Stop if plausible nuisance evolution absorbs the forecast difference. A surviving result would test a scaling law, not establish Machian inertia or a condensate origin.

**Reproduction.** `probe.py` reads the pinned sources without writing to the repository. It records spectrum convergence, growth counterexamples, direct infall, exact integer bounds, and the future-continuation example in `evidence.json`. It requires existing NumPy and SciPy. `sources.json` records primary URLs and their roles. `checks.json` and `lean-build.log` record actual checks.

Both Python certificate checks pass byte-for-byte. Wave 11 Lean passes. A full `lake build` on a temporary copy fails in Wave 12 and in pre-existing Wave 5, 6, and 7 duplicate/syntax defects. GravityClaims passes, and Wave 10 builds with one unused-variable warning. No audited snapshot, branch, commit, or public artifact was changed.
