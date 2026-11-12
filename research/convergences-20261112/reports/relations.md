# Relations and properties

This report reviews the repository revisions recorded in the source ledger. It does not review later changes on main, including gravity Wave 11. Original research: gpt-forge, gpt-6-astra, requested reasoning effort ultra. Publication preparation: gpt-6.1-sol.

Two objects can be indistinguishable when inspected separately and behave differently when coupled to the same surroundings. This is established quantum physics, with a particularly clear example in collective light emission. A second distinction is useful for the repository's Witness Map: losing visible quantum interference does not guarantee that the surroundings contain many readable records.

Those are separate questions about the same interaction.

The most promising connection across these projects is therefore a question we can make concrete: **what information about arrangement, correlations, surroundings and history is missing when we describe a thing by its individual properties?** This gives several testable bridges. It does not establish that everything is relational, or that the different bridges share one mechanism.

Research pass: 12 November 2026. Seat: gpt-forge, expedition route 2. Model requested and selected for this expedition: gpt-6-astra, ultra reasoning. Existing project clones were read only. The calculations below reproduce consequences of known models. They are not a new physical discovery.

**The map of possibilities**

| Meaning of a relationship | What can change | What stays distinct | Repository connection |
|---|---|---|---|
| A reference system, such as a clock or ruler | The description of position, time or a quantum state | Changing the description alone is different from changing the physical experiment | physics0 relative equilibria, orbital shapes and quantum reference frames |
| Interaction with the surroundings | Interference, decay, available excitations | Decoherence, energy loss and readable records are different quantities | fractals Witness Map and crowd-wave discussion |
| Correlations among constituents | Emission, protected states, collective response | A list of individual states need not determine a joint state | physics0 quantum-information codes, fractals collective waves |
| Geometry, connectivity and boundary conditions | Vibrational modes, stiffness, phase transitions | The graph, its embedding and the interaction strengths are separate inputs | physics0 incentre lattice, fractals criticality |
| External gravitational field | In some gravity models, internal dynamics even when the external field is nearly uniform | A uniform field, tidal gradients and a shared formation history must be separated | gravity AQUAL/external-field calculations |
| Cosmic background and history | Structure formation, effective medium properties, candidate acceleration scales | Present expansion, curvature, cosmological constant and accumulated heating are not interchangeable | gravity cosmic-epoch and Dark-WHIM proposals |
| Observation geometry and selection | Whether an event enters a catalogue | An event becoming invisible need not mean the physical system disappeared | astr0 lost eclipses, plate eclipses and rejected transit signals |

The operational distinction is between changing a description, changing an interaction, changing a joint state and changing which evidence is accessible. They can occur together, but none implies all the others.

**1. The surroundings can erase interference without making an object publicly readable**

The Witness Map compares a spreading time with a decoherence time. Its model variable is `W = m Δx² Γ(Δx)/ħ`. This answers a useful, specified competition of timescales. It does not include a measure of how many separate observers could infer the selected property by collecting different fragments of the environment.

The relevant repository passages are:

- [Witness Map introduction](https://github.com/Foundation-0/fractals/blob/9669f5579635c3543f145e8eca86133069ad6f27/README.md#L45).
- [Collective-wave distinction](https://github.com/Foundation-0/fractals/blob/9669f5579635c3543f145e8eca86133069ad6f27/README.md#L147).
- [Model code](https://github.com/Foundation-0/fractals/blob/9669f5579635c3543f145e8eca86133069ad6f27/witness-map/model.js#L109).

An overlooked example already appears in a paper cited by the repository. Riedel and Zurek calculate scattered photons from directional and isotropic illumination. Directional illumination can create many copies of position information.

In the ideal case of perfectly isotropic illumination, decoherence still occurs, but the photon directional states begin fully mixed and do not produce redundant records. Their Figure 2(b) and equations 17–18 show the mutual information of any proper photon fragment tending to zero at long times. Real illumination need not satisfy that limiting case.

The example establishes that a decoherence rate alone cannot specify record redundancy. [Riedel and Zurek, 2010](https://arxiv.org/html/1001.3419v2).

This also introduces time into the relationship. Interactions within an environment can redistribute initially readable records into correlations that require access to large fractions of the environment. The system can stay decohered while small fragments become less informative. [Riedel, Zurek and Zwolak, 2012, sections 3–4](https://arxiv.org/html/1205.3197v2).

Total quantum mutual information can include correlations that are not independently readable classical information. An information plateau needs interpretation. It is not by itself a universal certificate of objectivity. [Le and Olaya-Castro, 2018](https://doi.org/10.1103/PhysRevA.98.032103).

I made this distinction explicit with a six-qubit calculation. One qubit is the system, and five form the environment. The first state is

\[
 |\Psi_R\rangle=(|0\rangle|00000\rangle+|1\rangle|11111\rangle)/\sqrt2.
\]

The second replaces the two environmental strings with the logical states of the standard five-qubit error-correcting code:

\[
 |\Psi_C\rangle=(|0\rangle|0_L\rangle+|1\rangle|1_L\rangle)/\sqrt2.
\]

Both have exactly the same reduced system state, `ρS = I/2`. In fact, replacing `1/√2` by any amplitudes `α, β` gives the same complete dephasing channel on the system in both constructions. Every individual environmental qubit also has the same state in the two examples. What differs is where information resides.

| Environment fragment size | Classical pointer information, repeated records | Classical pointer information, code | Total quantum mutual information, repeated records | Total quantum mutual information, code |
|---:|---:|---:|---:|---:|
| 0 | 0 bits | 0 bits | 0 bits | 0 bits |
| 1 | 1 bit | 0 bits | 1 bit | 0 bits |
| 2 | 1 bit | 0 bits | 1 bit | 0 bits |
| 3 | 1 bit | 1 bit | 1 bit | 2 bits |
| 4 | 1 bit | 1 bit | 1 bit | 2 bits |
| 5 | 1 bit | 1 bit | 2 bits | 2 bits |

All 32 environment subsets were evaluated for each state, so these are not averages hiding exceptional subsets. For the code construction, every one- or two-qubit fragment is uncorrelated with the system. Any three qubits suffice to recover its full encoded quantum partner.

For repeated records, each separate qubit reveals the selected classical bit, while the phase of the original superposition remains in global correlations. In neither example has unitary quantum mechanics destroyed the global information.

The code is established prior work. The probe uses its cyclic stabilizer representation and independently checks every one- and two-qubit Pauli operator on the code space. [Laflamme, Miquel, Paz and Zurek, 1996](https://arxiv.org/abs/quant-ph/9602019), [Knill and Laflamme, 1996/1997](https://arxiv.org/abs/quant-ph/9604034).

The comparison and its application to the Witness Map are this expedition's illustrative construction.

This suggests a direct link from **fractals' environment records to physics0's error-correcting codes**. Robust classical information can be repeated locally. Robust quantum information can be protected by making small local pieces uninformative. The common question is how the information is distributed. Their physical goals differ.

The strongest objection is that the code environment is engineered. It proves a logical distinction, not that natural sunlight commonly encodes information this way. The isotropic-scattering model and the environment-mixing calculation supply physical mechanisms worth examining separately.

What would change the practical conclusion is a calculation showing that the particular environments represented by the map always generate accessible records on a known timescale. That would justify an additional model-specific inference, not a general identification of decoherence with records.

A useful extension would expose three separate outputs: `Γ(Δx)t` for an experiment's interference visibility, the existing `W` for spreading versus decoherence, and a specified information measure for fragments. The scale-selection route independently finds that a fixed-time visibility threshold and a `W=1` threshold even scale differently with gas pressure. No edit to the existing map was made in this pass.

**2. An apparently intrinsic lifetime belongs partly to the shared field**

An excited atom's lifetime looks like a property of that atom. Cavity experiments show otherwise. Hulet, Hilfer and Kleppner changed the available electromagnetic modes with conducting planes and measured a Rydberg-state lifetime increase of at least a factor of 20. [Their 1985 experiment](https://doi.org/10.1103/PhysRevLett.55.2137).

A resonant cavity can also shorten the lifetime. [Goy, Raimond, Gross and Haroche, 1983](https://doi.org/10.1103/PhysRevLett.50.1903). These are observations of environmental control, not merely interpretive claims about observation.

There is a still sharper collective example. Consider two identical atoms with one shared excitation:

\[
 |+\rangle=(|eg\rangle+|ge\rangle)/\sqrt2,\qquad
 |-\rangle=(|eg\rangle-|ge\rangle)/\sqrt2.
\]

Each atom separately has the same state in both cases: half ground, half excited. In the ideal limit where the field couples to the collective lowering operator `J− = σ−1 + σ−2`, the symmetric state emits at `2Γ`. The antisymmetric state has zero emission through this channel. The incoherent equal mixture emits at `Γ`.

This is the elementary Dicke bright/dark distinction. [Dicke, 1954](https://doi.org/10.1103/PhysRev.93.99).

The second calculation in the probe varies the common-field coupling. With off-diagonal decay coefficient `Γ12 = ηΓ`, the initial photon emission rates are:

| Correlation of the field at the two atoms, η | Symmetric state | Antisymmetric state | Incoherent mixture |
|---:|---:|---:|---:|
| 0 | Γ | Γ | Γ |
| 0.5 | 1.5Γ | 0.5Γ | Γ |
| 0.9 | 1.9Γ | 0.1Γ | Γ |
| 1 | 2Γ | 0 | Γ |

Both the joint atomic state and the field's spatial correlations matter. Two-ion experiments observed changes in emission rate with ion separation, supporting the collective mechanism. They did not realize every ideal endpoint of this toy table. [DeVoe and Brewer, 1996](https://doi.org/10.1103/PhysRevLett.76.2049).

This reverses an easy intuition: stronger exposure to a common environment need not make every collective state decay faster. Some combinations couple strongly and others cancel in that channel. More generally, protected subspaces depend on the symmetry of the coupling. [Lidar, Chuang and Whaley, 1998](https://doi.org/10.1103/PhysRevLett.81.2594).

The strongest limit is equally concrete: independent noise, unequal atoms, changing separation and additional decay channels remove exact darkness. These results do not imply that arbitrary macroscopic objects can be kept coherent by adding more surroundings.

A promising bridge to the lattice work is to calculate the relevant interaction matrix, not only the geometry. Its eigenvectors say which collective patterns the surroundings can excite or distinguish. This could connect mechanical modes, optical brightness and protected quantum states without claiming that their microscopic mechanisms are the same.

**3. A lattice's geometry is an input to physics, not a complete physical model**

The [physics0 survey](https://github.com/Foundation-0/physics0/blob/76410c3deebf925f6c51017867dbcef29ff54e8b/AREAS.md#L74) proposes percolation, Ising and lattice-sum studies on the incentre/CaB₆ network. Each asks about a different relation. Site or bond percolation needs a graph and an occupation rule. A fixed-coupling Ising model needs a graph and its spin interactions.

Mechanical response also needs bond directions, stiffnesses, masses and boundary conditions. A real compound needs additional electronic and chemical information.

For a central-force spring model, a compatibility matrix `C` maps site displacements to bond extensions. Its dynamical matrix has the form `D = M^(-1/2) Cᵀ K C M^(-1/2)`. Thus an unchanged connectivity graph can acquire different mechanical spectra when bond directions change.

Kane and Lubensky connect this matrix structure to protected boundary modes, with the count `N0 − Nss = dNs − Nb` and a further topological contribution to spatially resolved mode counts. Their result applies to the specified spring frameworks. It does not infer material properties from a drawing alone. [Kane and Lubensky, 2014, equations 1–2 and 6–7](https://arxiv.org/html/1308.0554v2).

The repetition route is independently probing a lattice fold with a fixed graph versus a graph defined by new contacts. The immediate handoff is to compare three models explicitly: fixed graph with fixed `J`, geometry-dependent `J(r)`, and contacts added at a distance threshold. If only the latter two change, the source of the new behavior is identified.

If the central-force spectrum changes while the fixed-`J` Ising model does not, that is an informative difference between kinds of relationship.

This is an inference for a future study, not a computed result for the incentre lattice in this route. The physical material could also change bonding during a deformation, invalidating both simplified models. Measuring or deriving its interaction law would determine which model deserves further work.

**4. A relational description is different from a relational force**

There are at least three ideas often grouped under “relational quantum physics.”

First, an observable can be a relation between physical readings: where one body is relative to another, or the value of a field when a clock reads a chosen value. Rovelli's distinction between partial and complete observables addresses this, including generally covariant systems. [Rovelli, 2002, sections II–III](https://arxiv.org/abs/gr-qc/0110035).

Second, the reference frame itself can be a quantum system. Giacomini, Castro-Ruiz and Brukner give explicit unitary transformations between such frames. Features such as entanglement can change with the frame and associated subsystem split, while consistently transformed states and measurements preserve outcome probabilities.

This does not permit removing an observed Bell violation by relabeling coordinates. [Their 2019 construction, results I.1–I.2 and measurement methods](https://arxiv.org/html/1712.07207v2).

Third, relational quantum mechanics proposes an interpretation in which values or events are relative to interacting physical systems. This is a philosophical and foundational position with a developed technical literature. It is not an experimentally selected consequence of the first two constructions.

No consciousness is required in the original proposal: the interacting systems may be ordinary physical systems. [Rovelli, 1996](https://arxiv.org/abs/quant-ph/9609002).

The usable connection is modest but deep: claims about a quantum property need the observable, subsystem split and physical reference system. The stronger claim that reality contains only relations remains open at the level of interpretation. It should not be treated as having been measured by a decoherence experiment.

**5. External gravity: an unusually clean distinction between present coupling and shared history**

The [gravity code](https://github.com/Foundation-0/gravity/blob/d8c7544e89388720fc1c13de816ddb7dd03d2096/verify_all.py#L300) evaluates an external-field limit of AQUAL, a particular MOND theory. Its nonlinear field equation is

\[
 \nabla\cdot\left[\mu(|\nabla\Phi|/a_0)\nabla\Phi\right]=4\pi G\rho.
\]

Linearizing the internal potential `φ` about a nearly uniform external field along `z` gives

\[
 \mu_e\,[\partial_x^2\phi+\partial_y^2\phi+(1+L_e)\partial_z^2\phi]=4\pi G\rho,
 \quad L_e=\left. d\ln\mu/d\ln x\right|_{g_e/a_0}.
\]

This follows directly by differentiating the flux in the nonlinear equation. The internal response depends on the external field's magnitude and direction even as its tidal gradient approaches zero. In the regime `g_internal ≪ g_external ≪ a0`, its scale is roughly Newtonian with enhanced `G/μe`, with anisotropy retained.

This is a conditional prediction of the theory, not an established law of nature. [Bekenstein and Milgrom, 1984, field equation and external-field analysis](https://doi.org/10.1086/162570).

Newtonian gravity and general relativity permit ordinary tidal effects. A uniform field is removable in the local freely falling description, with curvature and gradients setting its limits. Environmental histories can also change a galaxy's mass distribution. These are not the uniform-field dependence above.

Chae and colleagues report an external-field signal using SPARC rotation curves and environment estimates. [Chae et al., 2020](https://arxiv.org/abs/2009.11525).

Paranjape and Sheth construct a counterexample to the inference that any such correlation proves new gravity: correlated halo properties in a cold-dark-matter population generate an environmental correlation without violating the strong equivalence principle.

Their mocks predict a different correlation sign in relevant comparisons, making the sign useful, although it is not a theorem about every possible galaxy-formation model. They also identify uncertainty and reconstruction issues in the observational comparison. [Paranjape and Sheth, 2022, sections 2–4](https://arxiv.org/html/2112.00026v2).

A useful next comparison would predefine a rotation-curve residual and compare matched galaxies while keeping separate estimates of external field, tidal tensor, baryonic distribution and assembly proxies. The same catalogue selection and field-estimation procedure must be applied to simulated populations.

Field orientation and predicted anisotropy may add information beyond a density-bin comparison. This is a proposed probe, not an observational result from this pass.

I would take the uniform-field interpretation more seriously if its sign, amplitude and angular dependence survived those controls and independent field reconstructions. A correlation that disappears after matching halo history would instead favor a common cause. Cosmic-web location alone does not distinguish them.

**6. Cosmic context is a real source of questions, with several different possible meanings**

The gravity notebook proposes that a characteristic velocity arises from the growth of nonlinear structure and its heating history. That is a different relation from a constant in a fundamental action. It connects to familiar environmental physics through history-dependent collective response.

But the [notebook's Dark-WHIM bridge](https://github.com/Foundation-0/gravity/blob/d8c7544e89388720fc1c13de816ddb7dd03d2096/RESEARCH_NOTEBOOK_AND_REASONING.md#L30) still requires a derivation of its dark component's coarse-grained behavior.

A scalar field's inability to maintain a single-valued fluid velocity through a caustic does not by itself prove thermalization, a universal dispersion floor or trapped nonradiating entropy. The [claims ledger](https://github.com/Foundation-0/gravity/blob/d8c7544e89388720fc1c13de816ddb7dd03d2096/CLAIMS.md#L133) correctly retains a conjecture boundary here.

Milgrom's vacuum-inertia idea is another route. In de Sitter space a uniformly accelerated detector has temperature proportional to `sqrt(a²+aΛ²)`, where `aΛ = c² sqrt(Λ/3)`. Subtracting the inertial detector's temperature gives a low-acceleration dependence proportional to `a²/(2aΛ)`, reminiscent of MOND scaling.

The paper explicitly says this does not supply an inertia mechanism and highlights the difficulty of extending it to circular motion. It also distinguishes expansion, curvature and Λ away from de Sitter space. [Milgrom, 1999, sections III–IV, equations 6–11](https://arxiv.org/html/astro-ph/9805346v2).

The worthwhile question is what physical response, if any, links the cosmological state to local dynamics. A similarity between two acceleration scales is a lead. Choosing a particular temperature subtraction and calling it a force introduces a new assumption. A viable model must specify the coupling and recover the correct response for ordinary trajectories, not only a special detector path.

**7. Gravity can record some collective properties while barely resolving others**

The fractals crowd-wave section contains a useful case of selectivity. Allali and Hertzberg calculate gravitational decoherence of dark-matter density superpositions through scattering by ordinary matter. A later relativistic calculation finds that, in their Milky Way axion model, a field-phase superposition is much more resistant than a spatial superposition. These are conditional model results.

They do not establish the identity or quantum state of actual dark matter. [Allali and Hertzberg, 2020](https://arxiv.org/abs/2005.12287), [2021](https://arxiv.org/abs/2103.15892).

Thus the question “is the halo quantum?” is incomplete. One must say which superposition, which collective variable, which recorder and which duration. Ordinary interference within a classical field configuration is also different from a quantum superposition of macroscopically different configurations.

This distinction is already partly preserved in the repository and should be carried into comparisons with superfluid and gravity models.

Horizon-induced decoherence is a further theoretical example: Danielson, Satishchandran and Wald calculate which-path information entering a black hole through field degrees of freedom. A horizon is not a conscious observer, and the result does not require one. The proposed mechanism is not an experimental detection of quantum gravity. [Their 2022 paper](https://arxiv.org/abs/2205.06279v2).

**What the intersections support, and what they leave open**

| Intersection | Why it is worth following | Strongest limit or counterexample | What would advance it |
|---|---|---|---|
| Witness Map × quantum error correction | Separates lost interference from locally readable information | Engineered codes need not describe natural environments | Calculate fragment information for one existing photon/gas model |
| Collective emission × lattice modes | The interaction matrix selects bright, dark, stiff or soft collective patterns | Similar linear algebra does not establish a shared microscopic cause | Compare specific eigenmodes under fixed geometry, coupling and boundary changes |
| External-field tests × cosmic-web history | Offers a distinction between present environmental coupling and a common formation cause | Selection and halo correlations can mimic a statistical effect | Matched observations and simulations using the same estimators |
| Cosmic background × inertia | Makes the acceleration-scale coincidence into a mechanism question | Detector temperature is not an inertial force law | Derive a causal response for several trajectories and backgrounds |
| Archived events × observer geometry | An eclipse is a relation among a source, an occulter and a sightline | Instrument sensitivity can mimic a changed configuration | Join epochs, geometries and selection functions before asserting disappearance |

The last row connects directly to [astr0's lost-eclipses and archive projects](https://github.com/Foundation-0/astr0/blob/607a11eaa83b2ec7539e0986046c3230406d2b04/README.md#L23). This route has not established a nodal-precession explanation for any target. It preserves a useful alternative to treating catalogue absence as object absence.

The philosophical result I would retain is a question rather than a doctrine: **which properties remain unchanged when we alter the surroundings, the collective state or the reference system, and which were properties of that relationship all along?** The calculations show that this can be asked precisely.

They do not show that all intrinsic parameters are illusory, that measurement requires consciousness, or that a single relational theory unifies the projects.

The next action with the strongest support is a small Witness Map companion example separating interference, spreading and accessible records. The verified isotropic-scattering limit and the finite-dimensional probe already provide known-answer and counterexample cases. A second, independent action is to carry the field-strength/tidal-history distinction into gravity's proposed environment comparisons.

**Artifacts and provenance**

- [Source and claim ledger](relations-sources.json).
- [Reproducible calculations](../probes/relations/correlation_probe.py) and [numerical results](../probes/relations/results.json).
- [Probe explanation and limits](../probes/relations/README.md).

| Clone | Revision read |
|---|---|
| gravity | `d8c7544e89388720fc1c13de816ddb7dd03d2096` |
| fractals | `9669f5579635c3543f145e8eca86133069ad6f27` |
| physics0 | `76410c3deebf925f6c51017867dbcef29ff54e8b` |
| astr0 | `607a11eaa83b2ec7539e0986046c3230406d2b04` |

These identifiers locate repository proposals. They do not certify the proposals' physical truth. No new astronomical dataset was acquired or fitted.
