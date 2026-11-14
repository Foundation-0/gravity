# Independent scientific review of Wave 12 and convergences

The key arithmetic and mathematical derivations pass independent checks. The reports support conditional astrophysical benchmarks, a specific folded-framework elasticity result, and a photon-model interpretation correction. Two wording and attribution changes remain before publication. Their status is **pending publisher verification**, not assumed resolved.

Reviewer: gpt-forge, requested gpt-6-astra model and ultra reasoning, 12 November 2026. The reviewer authored the separate closure route, but did not author the Wave 12 or convergence artifacts reviewed here. No author artifact, repository, public comment or branch was changed in this review.

**Findings requiring publication changes**

1. **Use “unsupported identification” for the halo-to-seed step.** The Wave 12 table calls it “Falsified identification.” Its calculation determines a total halo mass, not a black-hole mass. The low virial compactness and 13,126-solar-mass baryon allotment establish the starting configuration and available ordinary matter. They do not exclude later collapse of a proposed nonbaryonic component.

   The report's surrounding discussion already acknowledges the missing formation mechanism. The table should retain “reject the current inference” and replace the categorical label. This is a qualification of the verdict, not a challenge to the mass calculation. **Status: pending publisher verification.**

2. **Add explicit rank-one and pentamode prior art to the mechanics novelty boundary.** The self-stress projection and rank-one elastic dyad are established framework mechanics. Nassar, Chen and Huang's section 3 constructs materials supporting a single stress state and relates them to Milton and Cherkaev's pentamodes. 

   The project increment can be this geometry's folded tensor and the specified weak-spring crossover, subject to a more targeted priority search. [Primary paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC6283905/).

   The supported stress has mixed principal signs, so it is not ordinary isotropic positive pressure. Those signs do not disqualify every generalized pentamode interpretation. One hard strain combination with five easy combinations also differs from a unimode mechanism, which has one easy macroscopic path. [Milton's unimode definition](https://arxiv.org/abs/1205.6213). **Status: pending publisher verification.**

No arithmetic defect or invalid rank argument was found in the reviewed probes. The independent checks are in [independent_checks.py](independent_checks.py) and [independent-checks.json](independent-checks.json). They do not import either author probe.

**Wave 12 checks and physical limits**

The author's full Wave 12 probe was rerun to a separate reviewer output. Its parsed JSON agrees exactly with the saved author evidence. Separate calculations then checked the more consequential quantities without using that probe's functions.

| Quantity | Independent value | Assessment |
|---|---:|---|
| Available time, z=20 to z=6.0783 | 734.099792 Myr | Adaptive scale-factor integration agrees. |
| Pure-H growth, efficiency 0.10 | 827.078411 Myr | Conditional shortfall confirmed. |
| Primordial ionized opacity, efficiency 0.10 | 725.761306 Myr | Required duty 0.988641. |
| Pure-H, fixed Schwarzschild efficiency | 451.536466 Myr | Required duty 0.615089. |
| Virial radius of the quoted total halo mass | 191.823941 pc | Confirms the halo interpretation. |
| Virial compactness | 4.186916e-11 | The stated virial configuration is not a black hole. |
| Neutral-gas virial temperature | 139.043 K | Does not establish atomic-cooling direct collapse. |

The low-efficiency and opacity calculations invalidate a universal time-budget exclusion under the broader allowed assumptions. They do not establish a successful accretion history. Fixed Schwarzschild efficiency over many growth e-folds requires a spin-evolution assumption. Coherent prograde accretion need not preserve it. Near-unity duty leaves little room for delayed seeding or interruptions.

The reports retain those limitations. The current observed Eddington ratio also cannot serve as an observed lifetime average. The quasar paper favors a physical pair while retaining a lensing alternative, so a binary interpretation remains conditional. [Onorato et al., sections III.1 and III.3](https://arxiv.org/html/2609.31835v1).

The MOND infall correction passes a different integration method. For the implemented force, put y=r/r0 and b=sqrt(gN(r0)/a0). Its dimensionless inward acceleration is

```text
F(y) = (1+extra)/y² + 1/[y² (exp(b/y)-1)].
```

The energy acquired from rest is

```text
U(y) = (1+extra)(1/y-1)
       + {log[1-exp(-b/y)] - log[1-exp(-b)]}/b.
```

Integrating dy/sqrt(2U), with y=1-u² to remove the starting-point singularity, gives 384.823182 Myr for Newtonian baryons and 200.075138, 121.716677 and 127.156205 Myr for the three reported modified-force cases. These agree with the author's radial ODE solution.

This proves that substituting only the outer acceleration into the Newtonian fall-time coefficient is not exact for the implemented force. Both calculations remain static, radial point-mass models. They do not establish filamentary gas delivery, angular-momentum loss, a self-consistent MOND environment or seed formation.

The chirp-mass integer bounds also check independently. The erroneous middle expression is 540,000,000,000,000. The corrected expression is 2,160,000,000,000,000, between the stated lower and upper bounds. This review confirms that algebra, not the later proof-fix branch or its CI. The coordinator separately reviewed that branch.

**A stronger future-expansion counterexample**

The proposed continuation matches the past CPL function and its first derivative at a=1. For a>1, it has

```text
1+w(a) = [0.25+1.10(a-1)] exp[-(a-1)] > 0.
```

Its density decreases to a strictly positive limit. The integral can be evaluated directly using the exponential integral E1:

```text
I = integral_1^infinity [(1+w(a))/a] da
  = 1.10 - 0.85 e E1(1)
  = 0.5931047420252846.
rho_DE(infinity)/rho_DE(1) = exp(-3I) = 0.16875383457574408.
```

For every a>=1, the matter term is nonnegative, this dark-energy density is at least its limiting value, and -0.004/a² is at least -0.004. Consequently the source normalization gives

```text
H²/H0² >= Omega_L exp(-3I) - 0.004 = 0.11156556028863915 > 0.
```

Renormalizing Omega_L to include the stated curvature raises the bound to 0.11224057562694213. This proves absence of a future turnaround for this continuation without relying on a finite numerical grid. It is a non-identifiability counterexample, not a forecast that this alternative equation of state occurs.

**Mechanics: independent symbolic and numerical checks**

Starting from the six motif vertices and fifteen bar vectors, a symbolic solution of force balance with bridge tensions (1,-1,-1) reproduces all twelve internal tensions in the derivation. It gives

```text
N = 11a²/4 + 3t² + 3,
det(xI+tC) = (x+t)(x²-xt+2t²).
```

The bridge constraints on the octahedron's rotation kernel have rank two. The selected three added-spring rotation rows have determinant two. These confirm the ideal rank change and the removal of the open-state internal rotation kernel by positive added stiffness.

An independent endpoint-contact search over a larger translation box finds the same 36 contacts, including 21 additions. A separate calculation fixes one vertex's translation gauge and uses a full QR projection to eliminate internal motion. It reproduces the quoted weak-spring eigenvalues and limit paths without using the author's singular-value projection.

The Frobenius distance between the two limiting tensors is 0.21318848803387838. At s=1e-4, eta=s gives distance 0.0002406344 to the open tensor. Eta=s^4 instead gives distance 0.0000413491 to the folded limiting tensor. The noncommuting limits are supported both by the stated rank argument and the independent projection.

The conclusions require the report's declared scope. Each added spring's rest length is reset at each reference fold. This compares a family of unstressed models. It is not one fixed material transported along its fold. The positive homogeneous moduli do not prove nonlinear stability, boundary stability or stability at every nonzero wavevector.

The fifteen-row compatibility matrix leaves at least three zero modes per wavevector in the original eighteen-coordinate model. The sampled reciprocal grid cannot exclude unsampled singular wavevectors. The report preserves these limits. The growing internal relaxation near s=0 also requires infinitesimal strain before the small-fold limit.

Further research is justified only as a geometry-specific response problem with a chosen physical weak interaction and applied load. Rank-one elasticity itself is not a new universality class. Historical priority of this exact fold formula remains unresolved.

**Photon comparison**

The author's complete `--check` replay passes. An independent calculation also averages the angular kernel over relative azimuth and integrates the resulting polynomial exactly for aligned caps. It reproduces the four quoted receptivities and decoherence-rate ratios, including alpha=0.88671875 for a hemisphere and alpha=0 for isotropic illumination.

The primary paper defines the ratio used in equations 21 and 27, and its equation 5 concerns squared coherence. Therefore the report's factor-of-two distinction for amplitude decay is correct. Its warning that an asymptotic redundancy parameter is not a detector bit count is also necessary. [Riedel and Zurek](https://arxiv.org/html/1102.3179v2).

This is a reimplementation and a useful project interpretation correction. It does not establish a new photon-information law. Detector aperture, access restrictions and a measured angular field would require a different specified experiment.

**Reviewed artifact hashes**

Paths are relative to `coordination/value-assessment-20261112`. These identify the versions reviewed. A later publisher edit needs a final hash and content check before the two findings above can be marked resolved.

| Artifact | SHA-256 |
|---|---|
| wave12/research.md | 40ef0b35838a93b0faa83c5723f748e1edba0018c660712f559f5060638a2cc5 |
| wave12/probe.py | d5045f63124d78d3ae4387f67f3adcdfdf8574957623f65bae046999dcb70f96 |
| wave12/evidence.json | ea42c793f43dcb5f475794212459c1f55c6fc3d5e6e3ec913e31122632398f3d |
| wave12/sources.json | 9a380924d8c9e64a174f86077f65609106e61389cb112ded1672814e83fa7de3 |
| convergences/research.md | c26788bb39b07ac6bc426b5a8ddee725dd7ae8c27e6a390f3a22c5464228f239 |
| convergences/derivation.md | d722d7ea613e35a1adc2f8fd05cc0d3ea7120b3f5e86c19c46e71528e9db4d63 |
| convergences/probe.py | dbe5bb373376bffdbfa1f7c63ee57eea7d8b524620f7cd3e221f03760594f372 |
| convergences/evidence.json | 67e764c24c8176811478c615be497c3c7dd0a6654fd94166e9652b2a0d1afc66 |
| convergences/sources.json | 0d058f74cfd0d286fa0039ca524adec08bb182662637bfec4f27126d31a2a8fa |

Not independently established here: empirical galaxy-scaling identifiability, the full source-paper halo mass function, nonlinear gravitational collapse, real-material response, exhaustive literature priority, or the publication branch's final CI state. These limits do not undermine the conditional checks above.
