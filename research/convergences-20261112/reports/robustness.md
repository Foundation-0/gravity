The strongest connections survive because they specify what changes, what stays fixed, and what an observer can actually distinguish. The useful common idea is **observable equivalence**: different underlying states can give the same available observations. A new view becomes valuable when it separates alternatives that the old view could not.

This report reviews the repository revisions recorded in the source ledger. It does not review later changes on main, including gravity Wave 11. Original research: gpt-forge, gpt-6-astra, requested reasoning effort ultra. Publication preparation: gpt-6.1-sol.

That idea connects archive joins, quantum records, lattice models and coarse-grained physics. It transfers a way of asking questions. It does not establish that the systems share a material substance or microscopic mechanism.

This pass adds a concrete lattice result. Identical central springs on the same fifteen bars change their collective vibration spectrum during the cab-to-fcc fold, although the fixed-coupling Ising model remains unchanged. It also identifies a missing step in gravity: crossing a density slope of two is not, by itself, a derivation of a collapse threshold.

Research seat: gpt-forge. Requested and selected model: gpt-6-astra, ultra reasoning. Date: 12 November 2026. Existing source repositories were read only. The six preceding route reports were treated as proposals to examine. None is an independent authority for the others.

**What survives the changes examined here**

| Proposed connection | What survives | What does not follow | Useful discriminating change |
|---|---|---|---|
| Complementary observations reveal hidden structure | New constraints can remove ambiguities, under a specified observation model | Arbitrary views or disciplines identify a unique underlying reality | Add a channel sensitive to the remaining ambiguity, then vary the calibration assumptions |
| Decoherence connects to environment records | Both concern system-environment correlations | One reduced channel or a mutual-information plateau determines records of a specified observable | Hold the system channel fixed and change accessible environment correlations |
| A fold preserves a lattice | The specified graph and its fixed-J Ising distribution remain unchanged | Mechanical spectra, scattering patterns or real material properties remain unchanged | Keep bonds and stiffnesses fixed while changing their directions |
| Several galaxy velocities are nearby | The repository's arithmetic under its input choices | Four independent measurements establish one physical scale | Match velocity definitions, derive density and clock choices, then compare their response to redshift |
| A field has a conserved current | The action-specific continuity equation | Energy stays in a region, entropy is trapped, or fluid variables form a closed system | Track current, energy and unresolved field variables separately |
| Repeated behavior suggests a common rule | A declared operator, symmetry or scaling limit can transfer predictions | Similar slopes, pictures or names identify the mechanism | Test another observable and the leading correction away from the shared limit |

**1. Combining views and simplifying physics have a precise connection**

Let a physical model predict the probability distribution of observations. Two candidate states are equivalent for that experiment if they predict the same distribution. Forgetting detail can enlarge this class of equivalent states. Adding a complementary experiment can shrink it.

For known linear observations, this is elementary. If view i measures Aᵢθ, the unresolved differences lie in the null space of Aᵢ. Joint views leave the intersection of those null spaces unresolved:

```text
unresolved differences after joining views = intersection of ker(A_i).
```

This statement is exact for the declared linear maps. Approximate indistinguishability also depends on noise, sample size and the accuracy of the maps.

The probe uses a target y = q+b and a reference x = b, with independent readout noise. The target cannot separate signal q from offset b. One hundred further target readouts still cannot do that without additional assumptions. The reference supplies the missing direction. No prior is needed for this rank argument.

| Known observation map | Rank for two unknowns q and b |
|---|---:|
| One target readout | 1 |
| One hundred target readouts | 1 |
| Target and reference | 2 |

A shared unknown gain changes the result. If y = g(q+b) and x = gb, then q→aq, b→ab and g→g/a leave both observations unchanged. Two complementary views have not fixed the absolute scale. A calibration reference of known amplitude can break this remaining ambiguity.

This extends the evidence route's atomic-line example. Energy-difference cycles can detect inconsistent line assignments while remaining blind to a common multiplicative calibration error. More internally consistent relations need not supply an absolute anchor.

The distinction also applies to uncertainty. For n measurements of one signal with unit-variance shared offset and independent readout variance 0.01, the information about the signal is n/(n+0.01). It approaches one. Treating the offset as independently redrawn in every measurement instead gives n/1.01, which grows without bound. These are different noise models.

Gresele and colleagues' nonlinear multi-view theorem addresses a harder problem with unknown mixing functions. Its invertibility, independence and view-diversity assumptions are essential. Their two-noisy-view result identifies corrupted components, up to further transformations. It does not promise exact recovery of noiseless samples. [Theorems 1 and 5](https://proceedings.mlr.press/v115/gresele20a/gresele20a.pdf).

Our known linear calculation is neither a test nor a special implementation of that theorem. Its purpose is to expose an ambiguity that another source can remove, and an additional calibration ambiguity that it cannot.

There is a constructive connection to effective physics. Machta and colleagues show, in diffusion and Ising examples, how coarse observations lose sensitivity to many microscopic parameter combinations. Useful predictions can survive those losses. [Their primary calculation](https://arxiv.org/html/1303.6738).

Transtrum and Qiu develop model reduction for a fixed set of predictions by approaching boundaries of the space of possible model outputs. The specified predictions matter. A reduced model suitable for one measurement can fail for another. [Their model-reduction paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC4425275/).

The inference here is that simplification and evidence joining can be studied through the same observation map. One deliberately discards distinctions that do not matter for a task. The other seeks observations that recover distinctions that do matter. This is a mathematical and methodological bridge, not an identification of their physical causes.

A qualification prevents the geometry from becoming another numerical coincidence. Raw Fisher-information eigenvalues depend on parameter coordinates. In our example they are approximately 38.20 and 261.80. Rescaling the two parameter coordinates changes them to 0.005 and 2,000,000.005. The physical experiment is unchanged.

The invariant local quantity is the predicted distinguishability for the same physical displacement, dθᵀF dθ. The probe obtains 0.05 in both coordinate systems. Rank also remains unchanged under an invertible reparameterization. Eigenvalue comparisons need a declared parameter scale or metric.

An even narrower established bridge links information compression to renormalization. Gordon and colleagues derive a relation between predictive information and low-scaling-dimension operators using short-range statistical models, a separated environment, a large buffer and a controlled compression regime. [Main equations and Appendix B](https://arxiv.org/html/2012.01447).

That result gives a reason to investigate which variables retain predictive power at distance. It does not show that all useful data compression is a renormalization group, or that any information-preserving representation has discovered nature's fundamental variables.

**Strongest objection:** the observation map can be wrong. An apparent new constraint can share an unmodeled gain, selection rule or prior with the old one. A fitted low-dimensional representation can also hide alternatives that matter outside its training conditions.

**Constructive probe:** for one archive candidate, list the surviving explanations and the measurements each predicts differently. Preserve an untouched epoch or instrument for confirmation. The first deliverable should be a discrimination table with calibration and detection limits, not a new universal model.

**2. Records are robust only relative to a specified question and access**

The relations route's five-qubit example survives its central challenge: the same complete dephasing channel can coexist with different local accessibility of information. The mathematical reason is general. A unitary acting only on the environment leaves the system's partial trace unchanged, while an entangling operation can redistribute information between environment fragments.

The operation and the observer must be kept distinct. A passive basis change, with states and measurement operators transformed consistently, changes no prediction. A physical entangling operation on the environment at fixed local access can change which records an observer can read.

The independent three-qubit probe makes a further distinction. Compare these two isometries for the system's Z basis:

```text
Repeated records:  |0> -> |0>|00>,     |1> -> |1>|11>.
Encoded records:   |0> -> |0>|Phi+>,   |1> -> |1>|Phi->,
where |Phi±> = (|00> ± |11>)/sqrt(2).
```

Both erase the off-diagonal system elements and preserve its Z populations. The script verifies the channel on all four matrix units, including off-diagonal inputs. For an equal-amplitude input, each individual environment qubit has one bit of total quantum mutual information with the system in both constructions.

| Access to the environment | Information about system Z, repeated records | Information about system Z, Bell encoding |
|---|---:|---:|
| First qubit alone | 1 bit | 0 bits |
| Second qubit alone | 1 bit | 0 bits |
| Both qubits together | 1 bit | 1 bit |

Thus equal reduced dynamics and equal one-fragment mutual information do not identify a record of the selected observable. The conditional states here commute, so the quoted Z information is accessible, rather than merely an upper bound.

The Bell example has records about a different system basis for this equal-amplitude input. It does not show that every property is hidden. It shows why the observable belongs in the question. The larger error-correcting-code example in the relations route establishes the stronger absence of all system information in sufficiently small fragments.

This is consistent with established distinctions between total mutual information and accessible classical information. [Le and Olaya-Castro](https://arxiv.org/html/1803.00765v2) examine such differences in their specified environment model.

Riedel and Zurek's perfectly isotropic illumination provides a physical-model counterexample to inferring redundant records from a decoherence rate. The limiting mixed environment is special. Their paper expects ordinary nonuniform illumination to preserve substantial redundancy. [Figure 2 and equations 17–18](https://arxiv.org/html/1001.3419v2).

**Strongest objection:** an engineered three-qubit channel does not describe sunlight, gas scattering or a halo. It settles a logical implication. Applying the distinction to the Witness Map needs a particular environment, system observable and collection geometry.

**Constructive probe:** retain the existing wave-spreading comparison, add fixed-time interference visibility, then calculate accessible position information for a specified photon fragment. Change illumination directionality while controlling the scattering exposure. A useful answer would predict when those three outputs separate.

**3. The preserved lattice graph does not preserve its mechanical spectrum**

The repetition route's fixed-J Ising identity is exact: if positions do not enter the Hamiltonian, a deformation of positions cannot change that Hamiltonian. This is a useful control. It should not be counted as a physical discovery of unchanged material properties.

The same geometry supports a more revealing comparison. Put equal masses at the six motif sites and identical unstressed central springs on the fifteen original bars. All bars retain their length during the fold. A spring nevertheless resists the component of relative displacement along its own changing direction.

The compatibility matrix C maps displacements to first-order bond extensions. In units with spring constant divided by mass equal to one, D = CᵀC has squared mode frequencies as eigenvalues. This matrix relation is standard central-force mechanics. [Kane and Lubensky, equations 1–2 and preceding definitions](https://arxiv.org/html/1308.0554v2).

The probe uses the curve in the [local geometric proof](https://github.com/aska-digital/incentre-lattice/blob/abeb94b0aa5f7c59b14dab139aa380d2ce5d81e2/results/fold-continuous-fcc/PROOF.md). The cell is held fixed during each vibration calculation, and the Bloch wavevector is zero, so corresponding cells move identically. The endpoint retains only the original bars. New fcc contacts are not silently made into springs.

For t = 2s/(1+s²), direct algebra gives:

```text
sum omega_n^2 = trace(D) = 30,
sum omega_n^4 = trace(D^2) = 96 - 12 t^2.
```

The first spectral moment cannot distinguish the folds. The second can.

| Fold parameter s | Sum of squared frequencies | Sum of fourth powers | Zero modes at fixed cell and k=0 |
|---|---:|---:|---:|
| 0 | 30 | 96 | 6 |
| 0.5 | 30 | 88.32 | 4 |
| 1 | 30 | 84 | 4 |

The null counts also have an analytic explanation. The octahedron's internal bars admit only rigid translations and rotations at first order. At the open endpoint, the bridges constrain none of these rotations. For t≠0, two independent rotational constraints appear. Rotation about the axis proportional to (−1,1,1) remains an infinitesimal zero mode.

The nullity change is paired with a self-stress change, from three to one, preserving N₀−Nss = 18−15 = 3. This is a rank identity. It is not evidence that the remaining modes have topological protection or that the full material is stable.

A separate finite-displacement spring-energy calculation checks the matrix result. The corresponding directional Hessians agree within 3×10⁻⁸ in the chosen dimensionless units. No peer probe module was imported.

**Strongest objection:** actual CaB₆ has interactions and electronic structure absent from this model. Prestress, bending forces, new bonds and finite boundaries can all change its modes. A zero-wavevector calculation also does not establish stability throughout the Brillouin zone.

**What would advance the connection:** compare the fixed-J spin model, original-bar spring model and a justified interaction that turns on between approaching sites. Predict a susceptibility, a vibration spectrum and a scattering pattern separately. Their differences identify which part of the description carries the change.

**4. Gravity retains a promising question, with an additional missing stability step**

The scales route correctly flags that a circular velocity, a radial velocity dispersion, an aperture-weighted line-of-sight dispersion and a thermal speed are different observables. An independent Jeans-equation derivation shows exactly where one familiar conversion comes from.

For a spherical, steady tracer with density proportional to r⁻γ, constant radial dispersion σr and anisotropy β,

```text
d(nu sigma_r^2)/dr + 2 beta nu sigma_r^2/r = -nu Vc^2/r
implies Vc^2 = (gamma - 2 beta) sigma_r^2.
```

The conversion Vc/√2 requires γ−2β = 2. Projection into an observed aperture adds another weighting. Applying the same isothermal conversion to 175.82 km/s gives 124.32 km/s, as the scales route reports. This exposes the need for a physical mapping. It does not prescribe that mapping for a real disk.

The cooling calculation also has a well-defined scope. Independently evaluating its dimensional formula gives electron density 6.99×10⁻⁴ cm⁻³, temperature 2.31×10⁶ K and thermal dispersion 178.423 km/s. These follow from Δ=1000, cosmic baryon fraction, a Hubble-time clock, fixed composition and free-free cooling.

The cooling criterion concerns a gas environment. It is not a combination of fundamental constants alone. Metallicity, ionization and line cooling can matter, and the local density has to come from somewhere. Rees and Ostriker's original analysis explicitly compares cooling with gravitational collapse and distinguishes several evolutionary regimes. [Their paper](https://doi.org/10.1093/mnras/179.4.541).

Under the repository's free-free approximation, σff is proportional to ne times the available time. At fixed overdensity relative to critical density, ne is proportional to ΔH². A Hubble-time choice therefore gives σff proportional to ΔH. A free-fall-time choice gives σff proportional to √ΔH. Changing the clock changes the physical question.

A conditional redshift comparison turns the numerical coincidence into a possible discriminant:

| Redshift | Cooling dispersion at fixed Δ and Hubble clock, calculated here | Collapse dispersion read from repository artifact |
|---|---:|---:|
| 0 | 178.42 km/s | 185.59 km/s |
| 0.5 | 235.93 km/s | 114.36 km/s |
| 1 | 319.49 km/s | 69.92 km/s |

The collapse column was not independently recalculated with a Boltzmann solver in this route. It is the repository's approximate-spectrum result, also reproduced by the scales route. The independent calculation here is the cooling response under its stated conventions.

The curves can be close today while moving apart with epoch. This is a useful crossing question. It does not identify a common mechanism, and choosing Δ can move the crossing. A causal explanation would need to predict the relevant density and epoch before fitting the coincidence.

There is a separate issue in the [gravity notebook](https://github.com/Foundation-0/gravity/blob/d8c7544e89388720fc1c13de816ddb7dd03d2096/RESEARCH_NOTEBOOK_AND_REASONING.md). It calls γd=2 a critical isothermal core-collapse value, after deriving γd=2(σh/σ*)². That equation is hydrostatic balance in an assumed potential. It contains no perturbation growth rate or stability calculation.

For the stated power-law model with γd<3, the enclosed fraction is x^(3−γd), where x=r/R. It is smooth through γd=2:

| σh/σ* | γd | Enclosed fraction at x=0.05 | Separate imposed trapped fraction |
|---|---:|---:|---:|
| 0.99 | 1.9602 | 0.04438 | 0 |
| 1.00 | 2.0000 | 0.05000 | 0 |
| 1.01 | 2.0402 | 0.05640 | 0.01970 |

The last column uses the separate ansatz max[0,1−(σ*/σh)²]. It is not derived by the enclosed-mass formula. The slope crossing alone cannot justify that onset. It also cannot exclude a transition that a fuller model might possess.

For comparison, Bonnor's isothermal-sphere stability analysis specifies self-gravity, external pressure and allowed perturbations. Its instability criterion is derived from that boundary-value problem. This is a reminder of the missing ingredients, not an alternative criterion to insert into AeST. [Bonnor, section 3](https://articles.adsabs.harvard.edu/pdf/1956MNRAS.116..351B).

**Strongest objection to the criticism:** a nonlinear closure may indeed produce a threshold near the hydrostatic crossing. That possibility is open. The present algebra does not establish it.

**Constructive probe:** first derive a linear perturbation operator about a chosen equilibrium, with its boundary conditions and conserved quantities. Identify a mode whose growth rate changes sign. Only then compare the onset and its scatter with the proposed trapping law. A fixed external velocity scale can be an input without being a derived instability.

The four nearby speeds also need a selection-aware null. The choice of characteristic stellar mass, overdensity, cooling clock and comparison velocity can respond to the target number. Counting zero fitted parameters in one final curve does not count every choice made while searching for it. No numerical chance probability is justified without a defined search and null model.

**5. Conserved current, energy transport and a fluid analogy remain separate**

The persistence route's scalar current agrees with independent differentiation of the published AeST action. Holding metric and vector fixed gives

```text
P^mu = 2(2-KB) J^mu
       - 2[(2-KB)+F_Y] q^(mu nu) partial_nu(phi)
       - F_Q A^mu,
with nabla_mu P^mu = 0.
```

The numerical check varies both gradient invariants in a generic polynomial F at sixteen timelike-vector configurations. Direct finite differences of the Lagrangian agree within 5.5×10⁻¹⁰. The polynomial is a derivative test, not a proposed viable cosmology. [Action and definitions, equations 1–4](https://arxiv.org/html/2307.15126v3).

On the homogeneous background, this gives a³KQ constant under the definitions in the persistence report. The constant is initial data. For a bounded region, the continuity equation includes flux through its surface. Neither result supplies an entropy law or prohibits local energy export.

The original AeST paper explicitly states, after equations 9–11, that its effective pressure depends on vector perturbations and does not close in the displayed fluid variables. Its successful restricted dustlike limit does not establish a fluid equation of state through nonlinear collapse. [Original analysis](https://arxiv.org/html/2007.00082v3).

The persistence and unclaimed routes also correctly keep Schrödinger-field counterexamples separate from AeST. A standing wave can have momentum dispersion despite zero current velocity. An irrotational wave snapshot can carry angular momentum. Those examples challenge an inference from a chosen representation. They do not insert their allowed motions or transport laws into another action.

**Constructive probe:** derive modes and fluxes for one fully specified action before assigning retained heat or a dispersion floor. A calculation with reflecting boundaries can retain energy by construction. Compare it with outgoing boundaries and a closed accounting of energy and charge. The hidden-dynamics route examines what eliminating unresolved variables would require.

**6. A convergence should predict its own failure boundary**

The other routes contain several connections that remain worth pursuing. Their support comes from different kinds of evidence, which should stay visible.

| Connection retained from the other routes | Defensible scope | Extra test that would make the bridge stronger |
|---|---|---|
| Competing times select moving cutoffs | A stated rate balance predicts a response exponent within its regime | Independently vary the rate and measure a full crossover, retaining the observation protocol |
| Coulomb-form wave equations transfer shapes and spectra | Dimensionless operators agree within approximations | Compare frequency corrections, boundary conditions and loss channels |
| Critical systems forget microscopic detail | Certain long-scale statistics agree within a specified universality class | Compare several exponents and scaling functions, with finite-size and correction terms |
| A closed shape cycle can change orientation | A reconstruction variable can retain path information | Reconstruct a genuine orbit from its reduced trajectory and compare full closure |
| An object can outlive its visible signal | Appearance depends on geometry and detection | Seek another observable of continued existence and model detection completeness |

This route did not independently reproduce every theorem or calculation in that table. They remain qualified route-level findings. The counterexamples and independent calculations above test the inference patterns most consequential to the combined story.

The astronomical evidence provides an especially concrete example. ASASSN-24fw's half-period ambiguity survives the available DASCH coverage but is excluded by ASAS coverage at the discriminating phase. The absence of an eclipse is useful because the competing periods make different predictions there. [Primary analysis, section III.1](https://arxiv.org/html/2507.05367v3).

HS Hydrae supplies a different lesson: the eclipses disappeared while the binary persisted, consistent with changing orbital inclination. The published result combines old plates and modern photometry. [Davenport and colleagues](https://arxiv.org/abs/2107.10954). Neither case is a discovery made in this expedition.

This suggests a practical comparison across repositories. An astronomical archive can add a previously missing phase. A quantum observer can collect a previously missing fragment. A mechanics experiment can measure a mode absent from a spin model. Each expands what the experiment distinguishes. The physical channels and constraints remain different.

**Questions worth carrying forward**

1. Which two explanations remain indistinguishable after all current observations, and what is the smallest new observation that separates them?
2. Can a proposed common scale predict its response to an independent change of density, epoch, geometry or driving rate before those choices are fitted?
3. Which apparently fundamental variable is only sufficient for the present measurement, and which additional observable would expose the missing structure?
4. When a repeated pattern survives, is its stability supplied by symmetry, conserved flux, a boundary, continual rebuilding, or limited observational access?
5. Can an economical effective description retain its predictions across interventions, while remaining explicitly undecided about the microscopic mechanism?

The most concrete next experiment is the lattice comparison: retain the exact graph control, compute geometry-sensitive mechanics, then add one justified new interaction. For gravity, the next required derivation is a stability and transport calculation in a specified action. For astr0, the next useful evidence is whatever best separates the surviving explanations, including well-characterized non-events.

**Artifacts and scope of verification**

- [Probe script](../probes/robustness/robustness_probes.py) and [results](../probes/robustness/results.json).
- [Derivations and reproduction instructions](../probes/robustness/README.md).
- [Source and claim ledger](robustness-sources.json).
- [Initial report snapshots](../probes/robustness/input-snapshot.json).

The checks cover the spring spectrum and a direct energy derivative, the whole three-qubit dephasing channel and its accessible Z records, information rank and calibration symmetry, cooling sensitivity, the smooth hydrostatic crossing, and the AeST scalar derivative. They do not fit astronomical data or solve nonlinear AeST collapse.
