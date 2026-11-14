# Which convergences still justify research?

The lattice fold supports one bounded mathematical investigation. Its ideal spring response changes discontinuously when an arbitrarily small fold is allowed, and an explicit weak-interaction control shows why the order of limits matters. The photon-record connection supports a correction to the Witness Map's interpretation. It does not presently support a separate new-physics programme.

Research date: 12 November 2026. Researcher: gpt-forge, using the requested gpt-6-astra model with ultra reasoning. No observation was collected and no material was measured. The four repository snapshots stayed read-only. Numerical evidence and source provenance are recorded in the adjacent JSON files.

The existing [nine-route convergence study](https://github.com/Foundation-0/gravity/tree/02013ae95fa5913894b829c8e2e63a3efcde9e63/research/convergences-20261112) already separates geometric repetition, fixed interaction graphs, readable records, feedback, transport and observation. Repeating its illustrative examples would not answer whether further research is warranted.

| Connection | What remains after the earlier probes | Decision in this pass |
|---|---|---|
| Geometry and interaction graph | Does the exact fold change a specified mechanical response in a way that survives weak additional forces? | Pursue one bounded mechanics question. The ideal result and one sensitivity control are now calculated. |
| Decoherence and readable records | Does the Witness Map supply enough input to calculate both rates? | Pursue a bounded interpretation correction. Park a separate research programme. |
| Memory and fluid closure | Does one specified gravity theory admit the proposed reduced variables and preparation? | Keep with the gravity analysis. Another generic memory toy would add little. |
| Finite scaling ranges, criticality and caustics | Does a predicted scale or onset survive changed controls in the specified equations? | No new cross-repository mechanism established here. A matching slope or scale remains insufficient. |
| Archive joins and nuisance removal | Can an actual held-out event or calibration exposure separate the alternatives? | Retain as an empirical method. No new data were acquired in this route. |
| Fixed-graph Ising statistics along the fold | The Hamiltonian has no fold parameter when every original bond keeps the same scalar coupling. | Reject geometry-induced thermodynamic change in that formulation. |

**The fold changes the rank of the relaxed elastic response.**

The current [incentre-lattices source](https://github.com/Foundation-0/incentre-lattices/blob/2d374fff2a59cc9331566733043a4bb25c1040bf/papers/source/main.tex) already proves the open configuration's zero-mode count and elastic constants. Its exact path to fcc supplies the geometry used here.

Extensive rigid-unit modes in related bridged structures are prior work: [Goodwin's 2006 primary abstract](https://doi.org/10.1103/PhysRevB.74.134302) explicitly includes the Prussian-blue topology. Their existence is not this pass's contribution. That article's full text was inaccessible, so this comparison does not settle priority of the folded elastic formula.

The declared model has six point joints per periodic cell, twelve octahedron edges and three bridges to neighbouring cells. Each of the fifteen bars is an unstressed central spring with unit stiffness and rest length √2. The cell and motif are placed at a selected fold parameter. Internal displacements then relax linearly under a homogeneous strain. Energy is divided by the current cell volume.

This is an ideal framework calculation. Real CaB₆ has chemical interactions absent from this model. The endpoint remains the original fifteen-bond model even when its joint positions coincide with fcc packing.

Write the six strain components in an orthonormal Mandel basis. If R maps internal joint displacements u to bar extensions and B maps homogeneous strain e to extensions, then

```text
E(u,e) = (1/2) ||R u + B e||²
K = Bᵀ Pss B / V
```

Here Pss projects onto the self-stresses, ker Rᵀ. This is standard compatibility-matrix mechanics, using the rank-nullity relation described by [Kane and Lubensky, Eqs. 1–2](https://arxiv.org/html/1308.0554v2). A self-stress is an algebraic equilibrium tension pattern, not an applied prestress in this model.

The open configuration has three self-stresses and three nonzero elastic eigenvalues. Every fold with 0 < s ≤ 1 has one self-stress and exactly one nonzero elastic eigenvalue. The remaining five homogeneous strain combinations have zero quadratic energy after linear internal relaxation.

| Fold parameter s | Zero modes at zero wavevector | Self-stresses | Nonzero homogeneous elastic eigenvalues |
|---:|---:|---:|---|
| 0 | 6 | 3 | 0.0976311, 0.0976311, 0.1952621 |
| 0.00001 | 4 | 1 | 0.1033741 |
| 0.1 | 4 | 1 | 0.1077795 |
| 0.5 | 4 | 1 | 0.1684544 |
| 1 | 4 | 1 | 0.1805556 |

These numbers use unit spring stiffness and the motif radius as the length unit. They are not measured moduli. The earlier convergence probe reported the zero-wavevector vibration spectrum. The new quantity here is the elastic tensor after homogeneous strain and internal relaxation.

Rank-one elastic response and pentamode constructions are established prior work. [Nassar, Chen and Huang, section 3](https://pmc.ncbi.nlm.nih.gov/articles/PMC6283905/) describes frameworks supporting one stress state and relates them to Milton and Cherkaev. The possible increment here is the tensor for this particular fold and its specified weak-spring crossover. Historical priority remains unresolved.

The mixed stress signs exclude ordinary isotropic positive pressure, but do not exclude every generalized pentamode interpretation. Five easy strain combinations also differ from a unimode mechanism, which has one easy macroscopic path. [Milton defines that distinction](https://arxiv.org/abs/1205.6213).

The rank change has a short analytic explanation. An isolated triangulated octahedron is infinitesimally rigid. Its cell-periodic motions are three translations and three rotations. At s = 0 the bridges constrain none of those rotations to first order. At s > 0 the three bridge constraints have rank two on the rotation space. Hence rank R rises from 12 to 14, leaving one self-stress among fifteen bonds.

There is also a closed expression for the tensor. Define

```text
a = √2(1-s²)/(1+s²),     t = 2s/(1+s²)
C = [[0,-1,-1], [1,0,-1], [1,-1,0]]
L = (2+a)I + tC,        D = aI + tC
T = diag(1,-1,-1),      M = Dᵀ T L / √2
N = (11a² + 12t² + 12)/4
K(s) = mandel(M) mandel(M)ᵀ / (N det L),   0 < s ≤ 1
```

The bridge tensions of the surviving self-stress are proportional to (1,−1,−1). The script lists all twelve internal tensions and checks force balance. M is the corresponding macroscopic stress tensor. Its two negative and one positive principal values rule out interpreting this response as an ordinary fluid-like bulk modulus.

The explicit formula agrees with independent singular-value projections to 3.4 × 10⁻¹³ across the tested folds. Direct changes in spring lengths reproduce the predicted quadratic energy within 3.2 × 10⁻⁷ relative error in three small-strain checks. These checks do not establish nonlinear stability or global minimization over finite flexes.

The original bars also leave at least three zero modes at every wavevector because R has fifteen rows and eighteen columns. A 216-point reciprocal grid at each of four folds confirms that lower bound. Away from the open endpoint, only the zero wavevector has an extra zero mode on these grids. The grid is not a proof excluding every additional singular wavevector.

**Weak additional forces remove the discontinuity at fixed stiffness.**

The strain relaxation becomes singular near the open configuration. Under unit xx strain, the minimum-norm internal displacement grows approximately as 1.00418/s. Its norm is 100.4 at s = 0.01 and 1004.2 at s = 0.001. Infinitesimal strain must therefore precede the small-fold limit. A finite imposed strain cannot be kept fixed while trusting this linear displacement indefinitely.

The sensitivity control adds exactly twenty-one extra central springs per cell, on pairs that become the additional fcc contacts. Every added spring has stiffness η. Its rest length is set to its separation at the selected reference fold. This is an explicit comparison family, not one unchanged material followed through its motion. It introduces no hidden prestress or constraint pinning a joint to space.

All eighteen tested combinations of six folds and three positive η values have six positive homogeneous moduli. At fixed nonzero fold, the five formerly zero moduli become small positive values as η decreases. Near the open configuration, two of them grow relative to η because the ideal relaxation needed such large internal motion.

The added-force control tests homogeneous strain only. It does not certify the completed models' spectrum at nonzero wavevector, boundary stability or nonlinear stability. Positive homogeneous moduli alone would not establish those properties.

For s = 0.01:

| Added stiffness η | Six elastic eigenvalues, ascending |
|---:|---|
| 10⁻⁸ | 2.57×10⁻⁹, 6.07×10⁻⁹, 1.13×10⁻⁸, 1.21×10⁻⁵, 2.65×10⁻⁵, 0.103 |
| 10⁻⁶ | 2.57×10⁻⁷, 6.07×10⁻⁷, 1.13×10⁻⁶, 0.00120, 0.00261, 0.103 |
| 10⁻⁴ | 2.57×10⁻⁵, 6.07×10⁻⁵, 0.000113, 0.0547, 0.0904, 0.129 |

At fixed η = 10⁻⁶, the internal-response norm is 422.4 at s = 0.001, 99.0 at s = 0.01 and 10.05 at s = 0.1. It stays finite as s approaches zero. Thus a large response survives over part of the parameter range, while the ideal 1/s divergence does not survive at fixed positive added stiffness.

The two iterated limits differ. Let L₀ = 2 + √2 and v = (1,−1,−1,0,0,0) in Mandel coordinates. Taking s to zero before η gives the open tensor, whose normal-strain block is (3I + J)/(9L₀), where J is the all-ones matrix. The shear block vanishes as η then vanishes. Taking η to zero before s gives 2vvᵀ/(17L₀). Their Frobenius distance is 0.213188488.

The numerical paths resolve this difference without setting either parameter exactly to zero:

| Path at s = 10⁻⁴ | η | Distance to open tensor | Distance to folded limiting tensor |
|---|---:|---:|---:|
| η = s | 10⁻⁴ | 0.0002406 | 0.2133188 |
| η = s⁴ | 10⁻¹⁶ | 0.2131885 | 0.00004135 |

This control rejects the claim that a geometric fold alone robustly produces an abrupt physical stiffness transition. It supports the narrower question of which weak forces and imposed loads set the observable crossover. A bend-energy law, a chosen fabrication geometry or an atomistic force model would be different declared models and would require their own checks.

**Verdict: pursue bounded mechanics. Park material and fundamental claims.** The current evidence warrants an independently reviewed derivation of the folded elastic tensor and its response under one physically specified weak interaction. It does not warrant calling the structure a stable fluid analogue, a new universality class or a prediction for CaB₆.

Stop the broader research claim if the folded tensor and its regularization are already in the relevant framework literature, or if a physically chosen interaction erases every useful range of enhanced response. A failed priority search still leaves a useful implementation check. Progress would mean a reproducible crossover or load response tied to an actual design, with finite-strain and stability limits stated.

**The photon connection has a known answer and a specific project use.**

The Witness Map's photon populations specify temperature and dilution, but no angular state. Its `info(k,dx)` factor enters a decoherence-rate approximation. Those inputs cannot determine the rate of readable records. Dilution and angular mixing are different physical changes.

[Riedel and Zurek's 2011 scattering calculation](https://arxiv.org/html/1102.3179v2) supplies a receptivity α between zero and one, with redundancy-rate parameter α/τD. Its assumptions include elastic dipole scattering, negligible recoil, initially independent photons and a specified uniformly illuminated sky region.

The probe integrates their angular kernel for eighteen caps and orientations. This is a reimplementation of established theory.

For a cap aligned with the position separation, the calculated values are:

| Fraction of sky illuminated | Decoherence rate relative to isotropic illumination | α |
|---:|---:|---:|
| 0.25 | 0.353125 | 0.988692 |
| 0.50 | 0.500000 | 0.886719 |
| 0.99 | 0.979328 | 0.021109 |
| 1.00 | 1.000000 | 0 |

Angular quadrature refinement changes these results by at most 1.3 × 10⁻¹⁵. An analytic integral checks the denominator. Equalising the decoherence rates by dimming the brighter cases leaves α unchanged, so the same interference-decay clock can accompany different record rates. The ideal isotropic case is a limiting model, not a measurement of a real room.

The paper's τD governs squared coherence. The interference amplitude decays at half that rate. Any companion to the map must retain this convention and must not present the asymptotic redundancy parameter as a detector's bit count. The arbitrary photon fragments in the model also differ from a specified finite-aperture instrument.

**Verdict: pursue the bounded interpretation correction. Park new research here.** A useful companion would distinguish decoherence, spreading competition and accessible records, with an explicit radiation model.

A new physics investigation needs a specified illumination or detector configuration whose prediction is absent from existing work. Reproducing the isotropic counterexample again would not meet that threshold.

To reproduce the calculations, run `python3 probe.py`, then `python3 probe.py --check`, in this directory. NumPy is the only external dependency. The check compares against the saved output in the same numerical environment. The analytic and energy assertions specify the scientific tolerances independently of exact JSON replay. The assessed source snapshots and installed runtime were not changed.
