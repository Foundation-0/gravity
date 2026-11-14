# Persistence through creation and destruction

This report reviews the repository revisions recorded in the source ledger. It does not review later changes on main, including gravity Wave 11. Original research: gpt-forge, gpt-6-astra, requested reasoning effort ultra. Publication preparation: gpt-6.1-sol.

Some things persist because a quantity cannot change. Others persist because change becomes too slow, because escape requires crossing an energy barrier, or because a pattern keeps being rebuilt. These are different physical explanations for the same everyday observation: something remains.

The most useful connection is between survival and transport. Annihilation can leave a relic when particles stop finding partners. A compact structure can form when other parts of its field carry energy away. A changing distribution can keep the same rescaled shape. This makes the question more precise: **what remains, what can leave, and which clock controls the change?**

For gravity, this exposes a promising open calculation. The notebook's absence of electromagnetic cooling does not establish that a dark field retains its energy locally. Known scalar models provide counterexamples. Their equations differ from AeST, so they identify a missing derivation rather than settle the proposed Dark-WHIM mechanism.

Research seat: gpt-forge. Requested expedition model: gpt-6-astra, reasoning effort ultra. Sources were checked on 12 November 2026. Existing repositories were read without modification.

| What persists? | Mechanism to examine | Connection to the repositories | What could end it? |
|---|---|---|---|
| A conserved difference | Pair reactions preserve a charge even while populations change | gravity's relic calculations and the creation/annihilation intuition | Charge-violating reactions, transport across the chosen boundary |
| A surviving population | Reaction rates and integrated exposure become too small | gravity's freeze-out audit, cosmic history | Fresh production, decay, renewed annihilation in dense regions |
| A localized structure | Binding, an energy barrier, topology, or a dynamical balance | fractals' gravitational atom, gravity's solitons, physics0's periodic orbits | Unstable modes, phase slips, collisions, external forcing |
| A statistical pattern | Continued redistribution or an evolving scaling solution | fractals' turbulence and criticality, the dark-condensate question | Exhausted source, finite size, a changed transport law |
| A historical imprint | Dynamics stops erasing a distinction | cosmic relics, phase-transition defects, archived records | Relaxation, mixing, observational selection |
| A visible signal | Geometry and observing conditions keep a source detectable | astr0's disappearing eclipses and joined epochs | Changed viewing angle, cadence, passband or sensitivity |

## Production and annihilation preserve more than particle labels

Photon collisions can produce an electron and positron. STAR measured pair momentum and angular distributions in ultraperipheral gold collisions, where the nuclear electromagnetic fields supply the photons. This tests a microscopic process. See the [STAR collaboration's measurement](https://arxiv.org/abs/1910.12400), abstract and analysis of the angular distributions.

The kinematics already constrain the analogy. In units where c = 1, two photons have squared centre-of-mass energy s = 2E₁E₂(1−cos θ). Pair production requires s ≥ 4mₑ². Two parallel photons cannot make the pair in empty space, regardless of their individual energies. A single photon also needs another participant or external field to conserve four-momentum.

The reaction γγ ↔ e⁻e⁺ changes the number of electrons and positrons while preserving net electric charge. More generally, the [Noether theorem](https://arxiv.org/abs/physics/0503066), section 1, connects continuous symmetries of an action to conservation laws under its stated assumptions. The conserved quantity can pass between different carriers. This does not preserve the identity or shape of each object.

An antiparticle's reversed charge does not entail reversed gravity. The [2023 ALPHA measurement](https://www.nature.com/articles/s41586-023-06527-1) observed antihydrogen attracted toward Earth, within its stated uncertainty. This is direct evidence about antihydrogen in Earth's field, without an assumption about hypothetical cosmological branches.

For an expanding universe, a global energy slogan needs extra care. From ∇_μT^μν = 0, a perfect fluid in FLRW obeys d(ρa³) = −p d(a³), with c = 1. Radiation has ρ proportional to a⁻⁴, so its energy in a fixed comoving volume decreases as a⁻¹.

This follows from local stress-energy conservation. A generic expanding spacetime has no time-translation symmetry that supplies the familiar global conserved energy of a stationary laboratory.

Thus a theory of cosmic creation must specify its spacetime, interactions and boundary conditions. The inverse of a known particle reaction supplies neither a cosmological initial condition nor a law for a collision of spacetimes.

## A relic can survive without being indestructible

Consider particles χ and antiparticles χ̄ that annihilate only with each other. Define Y = n/s, the number density divided by entropy density. If comoving entropy is conserved, the difference η = Yχ−Yχ̄ remains constant while annihilation changes their sum. This is the setup of [Iminniyaz, Drees and Chen](https://arxiv.org/html/1104.5548), equations 2 and 6–10.

After inverse production becomes negligible, define an accumulated annihilation exposure

```
u = Y0 integral s(t) <sigma v> dt
y_minus = Y_antiparticle / Y0
q = eta / Y0
dy_minus/du = -y_minus (y_minus + q).
```

Here y_minus starts at 1. The exact solution is y_minus = q/[(1+q)exp(qu)−1], with symmetric limit 1/(1+u). The majority population is y_plus = y_minus+q. The local probe independently integrates this equation and agrees to better than 2×10⁻¹² relative error for the cases below.

| Initial excess q | Surviving majority at u = 100 | Surviving minority | Minority / majority |
|---:|---:|---:|---:|
| 0 | 0.009901 | 0.009901 | 1 |
| 0.001 | 0.010409 | 0.009409 | 0.904 |
| 0.01 | 0.015729 | 0.005729 | 0.364 |
| 0.1 | 0.100004 | 0.00000413 | 0.0000413 |

These are dimensionless examples, not fitted dark-matter abundances. In the ideal radiation-era model with constant degrees of freedom and a constant annihilation cross section, the remaining exposure is proportional to ∫dx/x², where x = m/T. That integral is finite. Symmetric particles can therefore leave a residual population. A conserved initial excess provides a second survival mechanism.

The two mechanisms answer different questions. Finite reaction exposure explains why destruction stops short. A pre-existing excess explains why annihilation can remove almost all opposite partners while leaving a substantial majority.

It does not explain how the excess was generated. Sakharov's [original baryon-asymmetry proposal](https://cds.cern.ch/record/721864) addresses that separate problem by considering baryon-number violation and asymmetric processes in an evolving universe.

**Strongest objection:** this simple equation assumes away decays, charge-violating reactions, entropy injection and later production. A relic abundance alone cannot identify its origin. A useful discriminant would combine abundance with momentum distribution, residual annihilation and the expansion history. A proposed cosmic remnant must predict at least some of these independently.

## A conserved quantity and a protected structure are different kinds of survival

A superfluid circulating around a ring offers a direct laboratory example. Its phase can wind an integer number of times around the ring. As long as the field remains nonzero and continuous along that path, the winding cannot change smoothly. A phase slip, where the amplitude becomes small enough for the phase to change its winding, permits decay.

[Ryu and colleagues](https://arxiv.org/html/0709.0012), figures 2–5, observed circulation for up to ten seconds, limited by the apparatus. Changing the trap geometry and constricting the flow changed its survival. The result links persistence to the accessible configuration space and the cost of escape. It does not show that any condensate is permanently protected.

[Kibble's 1976 analysis](https://doi.org/10.1088/0305-4470/9/8/029), sections 3–5, ties possible walls, strings and monopoles to the structure of the available vacuum states. A defect can retain evidence of a transition, but its later abundance depends on annihilation, motion and expansion. Laboratory defect formation does not establish the existence of a particular cosmic defect population.

The scales route connects this to Kibble–Zurek formation. The [homogeneous Bose-gas experiment by Navon and colleagues](https://arxiv.org/abs/1410.8487) tests how the rate of crossing a transition sets coherence length. A later measurement can partly erase that initial signature through coarsening. Formation history and survival history need separate clocks.

The gravitational atom provides another mechanism. Its approximate hydrogen-like spatial modes can grow by extracting a black hole's rotational energy, then decline through losses. [Arvanitaki, Baryakhtar and Huang](https://arxiv.org/abs/1411.2263), equations 23–25, model a real-boson cloud with

```
dN/dt = Gamma_sr N - Gamma_a N^2.
```

After growth stops, their simplified annihilation law gives N(t) = Nmax/[1+Γa Nmax t]. A recognizable cloud can persist while its occupation decreases. The existence and observational abundance of such clouds remain model-dependent. The repository's shared orbital shapes do not determine their formation or lifetime.

**Promising comparison:** label every proposed persistent object by its conserved quantities, its unstable modes and its available escape channels. For physics0's periodic orbits, a mathematically exact orbit still needs a stability calculation to predict survival under perturbations. For a topological object, allow the field to leave the restricted configuration space before claiming absolute protection.

## Order can grow while energy moves elsewhere

An isolated system can become more ordered in one range of scales while other modes absorb its energy. This need not involve photons leaving the system.

In [Erne and colleagues' Bose-gas experiment](https://arxiv.org/abs/1805.12310), equation 1 and figure 4, the low-momentum distribution evolved with an approximately conserved particle number in its scaling region while energy moved toward higher momenta.

The preceding cooling quench removed energetic atoms. The later redistribution was studied in the resulting isolated gas.

The distinction can be checked without simulating the experiment. Suppose a one-dimensional spectrum has the form f(k,t) = t^α F(t^βk), measured inside a moving interval |k| < Kt⁻β. Its particle number scales as t^(α−β), while its kinetic energy scales as t^(α−3β). Setting α = β conserves particle number in that interval and gives energy proportional to t⁻²β.

The probe integrates a Gaussian F with α = β = 0.1. When t/t₀ rises from 1 to 100, the particle number remains unchanged and the interval's kinetic energy falls to 0.398 of its initial value. These exponents and the chosen profile are inputs. The calculation establishes the accounting, not a new dynamical law or a dark-matter model.

This makes a useful distinction for the fractal threads: a persistent statistical form can accompany continuous change in its ingredients and characteristic scale. A proposed common mechanism must predict the transport and the scaling exponent. A visually similar pattern supplies much less information.

**Strongest objection:** a scaling solution valid in one momentum interval cannot be extended over every scale while conserving both particle number and kinetic energy. The missing energy and the finite cutoffs must be tracked. Agreement of rescaled curves alone does not establish that unrelated systems share a collision law.

## The dark-field cooling question becomes sharper

The [gravity notebook](https://github.com/Foundation-0/gravity/blob/d8c7544e89388720fc1c13de816ddb7dd03d2096/RESEARCH_NOTEBOOK_AND_REASONING.md#L40) joins three ideas: one scalar field cannot multistream, shell crossing therefore produces retained disorder, and no electromagnetic cooling prevents that disorder from leaving. Each step needs its own dynamical argument.

[Seidel and Suen](https://arxiv.org/abs/gr-qc/9309015), sections I–II and figures 1–3, evolved self-gravitating massive scalar fields that form bound objects by ejecting part of the field with excess energy. Their simulations were spherical and intended to establish the mechanism, not model full astrophysical collapse.

This directly counters a universal rule that a bosonic field without photon cooling cannot export energy. Their historical axion-abundance discussion is not used here as a current exclusion.

There is a second distinction. For ψ = √ρ exp(iθ), the pointwise Madelung velocity, proportional to ∇θ, is single valued away from nodes. A wave can still contain several momenta. The exact standing wave ψ proportional to exp(ikx)+exp(−ikx) has zero current, momentum peaks at ±ℏk, and nonzero kinetic energy.

The probe uses ℏ = m = 1 and k = 3. It obtains mean momentum 0, momentum variance 9, and kinetic energy 4.5. After spatial averaging removes the interference fringes, its Wigner distribution contains two momentum streams. This does not make its pointwise velocity multivalued. It shows why a current velocity alone is an incomplete description of wave stress.

[Uhlemann, Kopp and Haugg](https://arxiv.org/html/1403.5567), sections II.4 and IV, develop this distinction for the Schrödinger-Poisson representation of collisionless matter. Their smoothed phase-space description continues through shell crossing and includes velocity dispersion. It is a counterexample to an inference from field representation alone. It does not derive AeST's behavior.

For kinetic condensation, [Levkov, Panin and Tkachev](https://arxiv.org/html/1804.05857), equations 1–4 and section 6, give a further constraint: the process has a relaxation time. Under their virial assumptions, τgr/(R/v) is approximately 0.047q³/ln q, with q = Rmv/ℏ much greater than one.

The probe gives ratios of about 20, 373, 10,206 and 222,484 for q = 10, 30, 100 and 300. An available cooling or condensation process can still be too slow to matter.

Their section 5 explicitly distinguishes gravitational relaxation from the power-law cascades of short-range interactions. [Semikoz and Tkachev's kinetic-condensation model](https://arxiv.org/abs/hep-ph/9507306) uses weak scalar self-interaction.

The [2025 gravitational self-similarity preprint](https://arxiv.org/html/2509.02694v1), section IV, likewise finds that its stationary power-law cascade carries the wrong fluxes for ordinary condensation. Its useful claim concerns evolving profiles. These results do not establish one common turbulent cascade across the models.

AeST makes the need for model-specific work explicit. [Bataki, Skordis and Zlosnik](https://arxiv.org/html/2307.15126v3), equations 1–4 and section VII, describe metric, scalar and unit-timelike vector fields with six physical degrees of freedom.

In the [original AeST paper](https://arxiv.org/html/2007.00082v3), the paragraph after equations 9–11 says that the pressure does not close in the effective fluid variables: it also depends on vector perturbations.

Direct variation of the specified action gives ∇_μP^μ = 0. On the homogeneous background this becomes a³K_Q = constant. The [derivation](../probes/persistence/aest_current.md) shows that a finite region can exchange this charge through its boundary. It supplies no entropy law or prohibition on energy transport.

**What would strengthen Dark-WHIM:** choose the full function F(Y,Q), relevant parameters and any higher-derivative terms. Derive the characteristic modes and track their energy flux during collapse. Compare outgoing and reflecting boundaries, resolution, the retained velocity dispersion, and the coarse-graining scale. Then test whether retention lasts through the system's age and depends on environment as predicted.

**What would change the assessment:** an action-specific evolution showing negligible escape and a persistent, well-defined pressure after shell crossing would support the premise. Efficient export, predominantly reversible dispersive motion, or strong dependence on artificial boundaries would challenge it. No such AeST evolution was performed in this pass.

## Reversing a reaction is different from reconstructing a history

Microscopic reversibility compares fully specified processes. Reversing a macroscopic event also requires controlling outgoing radiation, correlations and the environment.

Crooks' [fluctuation theorem](https://arxiv.org/abs/cond-mat/9901352), equations 2, 5–7 and section III, makes this precise for specified stochastic dynamics and preparation protocols. Forward and appropriately reversed path probabilities are related by entropy production. It is not a theorem about reversing the universe.

A system's reduced entropy can decrease as its surroundings change. Coarse-grained entropy can increase while fine-grained Hamiltonian evolution remains reversible. Adiabatic cosmic expansion can preserve comoving entropy. Creation and annihilation do not define opposite time directions. The early universe's low-entropy boundary condition remains a separate question.

A nearby published conjecture is the [CPT-symmetric cosmology of Boyle, Finn and Turok](https://arxiv.org/html/1803.08928), which relates pre- and post-bang branches and adds a symmetry stabilizing a right-handed neutrino candidate. It is a hypothesis about a cosmological state and continuation, not a deduction from pair annihilation or a collision of two ordinary universes.

A collision proposal must identify what “opposite” means, what degrees of freedom interact, how the event is matched to the later universe, and which relic distribution or correlation differs from existing explanations. A dark remnant becomes an informative proposal when its stability and abundance follow from those choices. Nothing in this pass establishes such a remnant or links it to a galactic acceleration scale.

The evidence route contributes an observed reminder that survival and visibility can separate. [Davenport and colleagues](https://arxiv.org/abs/2107.10954) combined old plates with modern photometry for HS Hydrae. Its eclipses ceased as the orbital inclination evolved under a third star's influence. The binary continued to exist. The archive retained a history that a single recent observing epoch would miss.

For population inference, observed counts depend on formation, survival and detection. Schematically, an expected count integrates the formation rate multiplied by a survival probability and a selection function. A scarcity of signals can therefore reflect slow formation, rapid destruction or poor visibility. Joining epochs and observables can distinguish these causes without requiring one theory of everything.

## Work to carry forward

1. **Follow energy and charge separately in a specified dark-field model.** The new analytical current provides a consistency check. It does not replace the missing collapse and transport calculation. This is the most direct test of the gravity notebook's proposed mechanism.
2. **Compare formation and survival clocks.** Use initial and late domain measurements for critical systems, growth and loss for gravitational atoms, and reaction exposure for relic populations. Equal present-day appearances can hide different histories.
3. **Test pattern persistence by perturbing the transport.** Vary density, interaction range, driving or boundary conditions. Compare predicted changes in the full spectrum and energy flux, not only a fitted exponent.
4. **Treat disappearance as a joint physical and observational question.** Carry the HS Hydrae distinction into astr0's archive work. Where possible, require an independent observable of the object's continued existence.

The reproducible [probe script](../probes/persistence/persistence_probes.py) regenerates [results.json](../probes/persistence/results.json).

It checks the annihilation solution against numerical integration, the standing wave's moments, and the spectral number and energy integrals. It also evaluates a published kinetic timescale under its stated assumptions. It fits no observations and simulates no nonlinear gravitational collapse.

The [source ledger](persistence-sources.json) records exact pointers, what was inspected, and whether a statement is an established result, a conditional model, an untested conjecture or this pass's inference.
