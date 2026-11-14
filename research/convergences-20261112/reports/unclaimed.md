# What a cycle, a swirl and a resting place can conceal

This report reviews the repository revisions recorded in the source ledger. It does not review later changes on main, including gravity Wave 11. Original research: gpt-forge, gpt-6-astra, requested reasoning effort ultra. Publication preparation: gpt-6.1-sol.

A system can return to the same shape and still have turned. It can carry angular momentum without containing a vortex. It can contain vortices while its total angular momentum is zero. A place where every force balances can fail to hold anything there.

These established distinctions open three useful paths across the repositories: geometric phase, circulation and angular-momentum transport, and the mechanisms that support a configuration. They ask what motion is allowed and what a description leaves out. They do not require one theory behind all the examples.

The most revealing calculation is a triangle of three masses that completes a shape cycle and turns through **27 degrees**, with total angular momentum zero throughout. A second calculation separates angular momentum from vortex winding. A third shows an unstable static field becoming confining when driven within a suitable frequency range.

Research pass: 12 November 2026. Seat: gpt-forge. Requested model: gpt-6-astra, ultra reasoning. Existing clones were read-only. The probes reproduce known mechanics and wave kinematics. They establish no new astronomical phenomenon. Source status, reading scope and exact links are in the accompanying ledger.

**The distinct paths**

| Path | Missing question | Repository connections | Useful consequence |
|---|---|---|---|
| Geometric phase | What can change after the visible or internal variables return? | physics0 periodic orbits, fractals wave states, astr0 orientation and recurring events | Test closure of shape, orientation and phase separately |
| Circulation and angular momentum | What carries rotational motion, and how can it move elsewhere? | gravity scalar/condensate assumptions, fractals superfluid turbulence, physics0 relative equilibria | Separate local curl, winding, total angular momentum and its flux |
| Support mechanisms | Which permitted disturbances destroy a balanced configuration? | physics0 charge equilibria, gravity bound structures, fractals gravitational atom | State the degrees of freedom and the mechanism supplying confinement |

The first path extends the repetition route with an actual reconstruction law. The second extends the persistence route's energy-transport question with independent angular-momentum and topology constraints. The third uses a theorem already recognized by point-charges to connect its mathematics to physical support. It is not a defect newly found in that project.

**1. A closed shape cycle can produce a real turn**

Imagine three masses connected by an internally powered mechanism. They change their separations and angles, then return to their original triangle. With no external torque and zero total angular momentum, their final triangle can nevertheless point in a different direction. The mechanism spends energy moving its parts. Conservation of angular momentum still holds.

Shapere and Wilczek formulate this as a connection over the possible shapes of a deformable body. Their equations 2.1–2.6 explain how a path through shapes determines a net orientation change. Its value is unchanged by re-timing the prescribed path. [Their primary treatment](https://www-thphys.physics.ox.ac.uk/talks/CMTjournalclub/sources/Shapere_Wilczek_1989.pdf).

Montgomery gives a reconstruction formula for the three-body problem itself, with separate dynamical and geometric terms. Sections 1.1–1.2 explain the return of a triangle's shape and its accumulated rotation. Section 2.6 identifies zero-angular-momentum deformations with the horizontal directions of the connection. [Primary paper](https://arxiv.org/pdf/dg-ga/9510005).

The local probe makes the kinematics explicit. Use mass-weighted Jacobi vectors for three equal masses with fixed center of mass. Let one vector have unit length, the other length r, their internal angle be φ, and their common orientation be θ. In these coordinates,

```text
L = (1 + r²) θ_dot + r² φ_dot.

At L = 0:
dθ = -[r² / (1 + r²)] dφ.
```

Turn the internal angle by π/2 with r = 1, increase r to 2, undo the angle change, then return r to 1. The two angle changes have different rotational weights:

```text
Δθ = (4/5 - 1/2) × π/2 = 3π/20 = 27 degrees.
```

The chosen angle runs from π/4 to 3π/4, avoiding collinear triangles. The code reconstructs all three positions and velocities. It checks their center of mass, angular momentum and final pairwise distances. Reversing the loop gives −27 degrees. Retracing an angle change at fixed r gives zero.

This is a prescribed internally actuated motion. It is not a new free gravitational orbit. A Newtonian orbit must produce its shape path through its own equations of motion. The useful transfer to physics0 is a closure check: a closed curve in reduced shape space may require a rotation to reconstruct the full orbit.

There is a related wave question. Berry's adiabatic calculation shows that an isolated eigenstate can acquire a circuit-dependent phase after the Hamiltonian returns to its starting value. The phase can be measured relative to a reference through interference.

Sections 1–2, especially equations 3–10, state the assumptions and distinguish it from the dynamical phase. [Berry's original paper](https://michaelberryphysics.wordpress.com/wp-content/uploads/2013/07/berry120.pdf).

For fractals, this suggests a companion to comparing wave shapes: compare what happens when the parameters follow a closed path. A density image alone can miss the phase. The repository's gravitational-atom model would require a specified perturbation, spectral gaps, coherence time and treatment of degeneracies before this becomes an astrophysical prediction.

For astr0, recurring eclipse timing and return of the complete orbital geometry are separate questions. The evidence route already has a concrete inclination-change example. Geometric phase supplies a mathematical reason to track the reconstruction variables, but it is not an explanation of that star's eclipse cessation. Nodal precession needs its own dynamical model.

**Strongest objection:** geometric phase is established and the actuated triangle does not prove that a candidate astronomical system follows such a loop. That limits the new contribution to a cross-project method and a revealing example.

**What would change the assessment:** an actual candidate orbit whose reduced shape closes while its reconstructed orientation fails the proposed closure tolerance. Conversely, if the target already certifies full position-and-velocity closure, this adds understanding rather than a missing validation step.

**Next probe:** take one existing numerical three-body trajectory, remove translation and scale, record its shape curve, then independently reconstruct its orientation and compare with the original trajectory. Preserve particle labels and any allowed final permutation. No new orbit search is needed for that comparison.

**2. Angular momentum, local curl and vortex winding are different constraints**

The gravity notebook describes a single-valued irrotational scalar condensate when discussing collapse. The fractals turbulence study describes quantized circulation in superfluid helium. These statements raise a concrete question: what does “irrotational” forbid, and where does that description cease to apply?

For a nonrelativistic complex scalar with a Schrödinger kinetic term, write ψ = √n exp(iS). Where n is nonzero and S is smooth,

```text
v = (ℏ/m) ∇S,             curl(v) = 0.
```

Around a zero of ψ, the phase can wind. A loop enclosing such a defect can have circulation 2πkℏ/m, with integer k, even though the curl vanishes everywhere along the loop. The failed assumption is smooth phase over the entire spanning surface. This is a topological restriction on a field description.

Hui, Joyce, Landry and Li study these interference defects in a gravitationally coupled scalar with negligible self-interaction. Their sections 2 and 5 derive the winding condition and test vortex formation numerically.

Section 7 explicitly separates vortices from halo angular momentum: their zero-net-angular-momentum examples contain vortex rings, and they construct angular-momentum-carrying states without vortices. [Primary paper, equations 2.3–2.4 and 7.1](https://arxiv.org/html/2004.01188v2).

The earlier Rindler-Daller and Shapiro calculation asks a different question: when does a vortex lower the energy of a rotating condensate halo in specified equilibrium models? It requires sufficient angular momentum and interaction strength.

Section 3.2 also describes non-axisymmetric irrotational figures carrying angular momentum. Its equilibrium criterion is compatible with transient interference defects in another regime. [Primary paper, equations 85–100 and section 4](https://arxiv.org/pdf/1106.1256).

The local calculation supplies finite, normalizable examples in two dimensions. Set ℏ = m = 1 and divide angular momentum by the integral of |ψ|². These are valid wave snapshots, with no claim that either is a stationary halo.

| Snapshot | Velocity or phase property | Vortex winding | Angular momentum per particle |
|---|---|---|---:|
| Anisotropic Gaussian with phase S = αxy, a = 2, b = 1, α = 1/2 | v = α(y,x), so curl(v) = 0 everywhere | No zeros, zero winding on closed loops | 0.75 |
| Gaussian times x² + y² − 1 + 2iy | Zeros at (1,0) and (−1,0) | +1 and −1 around the individual zeros | 0, within numerical roundoff |

For the first field, the density weights x and y differently. Its angular momentum is α(a²−b²)/2 even though its phase is smooth and its flow has zero curl. For the second, reflection symmetry makes the total angular momentum vanish while each defect has a nonzero winding. The code verifies the integrals and loop windings separately.

Thus “it has angular momentum,” “its flow has vorticity,” “it contains phase defects” and “its figure rotates” need separate measurements. A phase defect does not itself prove thermal equilibrium or energy dissipation. The examples also show why total angular momentum alone cannot specify internal motion.

There is an independent obstacle to assembling a compact object. In a Newtonian point-mass potential, dissipating orbital energy at fixed specific angular momentum j favors the circular radius

```text
r_circ = j² / (GM).
```

To settle much further inward, that matter must transfer angular momentum to something else. An energy-cooling argument alone does not identify the torque or stress responsible. This elementary result supplies a second question for the gravity notebook's collapse proposal, alongside the persistence route's work on possible energy export.

**Strongest objection:** the Schrödinger/Poisson and Gross–Pitaevskii examples do not derive the behavior of AeST or a ghost-condensate action. A smooth real scalar, its effective complex envelope and a superfluid order parameter can have different allowed defects and conserved quantities. The report transfers a question and diagnostic, not a vortex mechanism into AeST.

**What would change the assessment:** a derivation from the intended action showing which circulation laws and defect configurations are allowed, followed by nonlinear evolution with an explicit angular-momentum balance. If that theory excludes the illustrated phase defects, the examples remain useful comparison cases only.

**Next probe:** extend a justified collapse experiment beyond a one-dimensional pancake by including a specified small angular momentum or tidal torque. Track total angular momentum, boundary flux, local circulation and any phase zeros separately. A one-dimensional calculation cannot decide the rotational part of the proposed mechanism.

**3. A force balance needs a support mechanism**

The point-charges project already states that its potential is harmonic away from its sources and has no local maxima or minima there. Its certificates include Morse indices, which count negative curvature directions at an equilibrium. The [project note, sections 1 and 4](https://raw.githubusercontent.com/Foundation-0/point-charges/main/NOTE.md) preserves this distinction.

The useful bridge is from those indices to the original question of how gravity and motion build structures. At a static electrostatic equilibrium in empty space,

```text
trace(Hessian V) = Laplacian(V) = 0.
```

A nonzero Hessian therefore cannot have all positive eigenvalues. If the quadratic term vanishes, harmonicity's maximum principle still rules out a strict local minimum. Flipping the sign for a Newtonian gravitational potential does not make an empty-space minimum. The argument concerns a test object in a fixed source field and unrestricted three-dimensional displacement.

Three equal positive charges at the vertices of a unit-radius equilateral triangle give a simple example. At the center the dimensionless potential Hessian has eigenvalues (1.5, 1.5, −3). A positive test charge has restoring motion within the triangle's plane and an unstable direction perpendicular to it. A constraint restricting motion to the plane changes the physical question.

Motion can also supply confinement. Wolfgang Paul's primary lecture derives alternating quadrupole fields and their Mathieu stability regions. Pages 603–610 explain the static saddle, the stable driven motion and the distinction between secular motion and micromotion. [Paul's Nobel lecture](https://www.physik.fu-berlin.de/studium/lehre/fortgeschrittenenpraktikum/unterlagen_fp_bachelor/Quadrupol-Massenfilter_2.pdf).

The probe integrates the linear equations for the dimensionless imposed potential U = cos(Ωt)(x²+y²−2z²)/2. Its Laplacian is zero at every instant. Floquet multipliers measure how a small displacement changes after one drive period.

| Drive | Transverse multiplier magnitudes | Vertical multiplier magnitudes | Linear result |
|---|---|---|---|
| Ω = 4 | 1, 1 | 1, 1 | Bounded in all three directions |
| Ω = 2 | 1, 1 | 0.41319, 2.42020 | Vertical disturbance grows |

The stable case has distinct multipliers on the unit circle. This is an ideal linear calculation, without finite electrode boundaries or noise. Halving the numerical step changes the quoted vertical monodromy traces by less than 4.1 × 10⁻¹². A static-saddle control matches its analytic exponential growth.

For the gravitational atom, confinement instead involves the wave kinetic term together with attraction. For an ordinary orbit, kinetic motion matters. A pressure-supported star or halo needs its stress terms. These are different mechanisms. Merely counting places where the force vanishes does not select one of them.

**Strongest objection:** much of this is familiar mechanics, and point-charges already records the relevant distinction. Its value here is a productive connection between exact mathematical certificates and the physical question of support.

**What would change the assessment:** a candidate configuration with specified constraints and dynamics whose perturbations are bounded in the physically allowed directions. An equilibrium count by itself cannot settle that question. A proof of nonlinear stability would support a stronger conclusion than the linear checks here.

**Next probe:** reuse a certified charge equilibrium and its Hessian to compare unconstrained motion with a declared constraint or periodic drive. For orbital projects, preserve separate statements for existence, linear stability and long-time nonlinear behavior.

**What remains worth asking**

- Can an apparently completed cycle leave a measurable orientation or relative phase, and which variable would reveal it?
- Which allowed motions disappear when a field is compressed into a smooth-fluid description?
- What carries angular momentum away when gravity assembles a compact structure?
- Which constraints or dynamics make a configuration physically supportable, and which merely make it look balanced in a restricted description?

These questions keep the original concerns about motion, creation and repeated structure available. They supply no derivation in which gravity is the opposite of creation, or annihilation implies a universe collision. Their contribution is to identify what an actual mechanism would have to specify.

The first follow-up I recommend is the three-body reconstruction comparison. It has a clear known answer and uses an existing trajectory. For gravity, the useful handoff is an angular-momentum and circulation audit of the proposed nonlinear model, coordinated with the persistence route's energy and closure checks.

**Artifacts and verification**

- [Reproducible probe](../probes/unclaimed/constraint_probes.py).
- [Computed results](../probes/unclaimed/results.json).
- [Probe assumptions and instructions](../probes/unclaimed/README.md).
- [Sources and claim status](unclaimed-sources.json).

The script uses Python's standard library. Internal checks cover analytic rotation, reverse and retraced loops, full position/velocity reconstruction, wave normalization, angular-momentum integrals, defect winding, static growth and Floquet step convergence. It fits no observations and changes no source repository.

| Repository | Revision read |
|---|---|
| gravity | `d8c7544e89388720fc1c13de816ddb7dd03d2096` |
| fractals | `9669f5579635c3543f145e8eca86133069ad6f27` |
| physics0 | `76410c3deebf925f6c51017867dbcef29ff54e8b` |
| astr0 | `607a11eaa83b2ec7539e0986046c3230406d2b04` |

The linked point-charges README and note were read live on 12 November 2026. Their certificates were not rerun in this route. No archive discovery, public-site state or proposed dark-matter mechanism was independently established here.
