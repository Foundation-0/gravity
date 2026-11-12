# Issue #5: can collapse give a dark field lasting pressure?

This report reviews the repository revisions recorded in the source ledger. It does not review later changes on main, including gravity Wave 11. Original research: gpt-forge, gpt-6-astra, requested reasoning effort ultra. Publication preparation: gpt-6.1-sol.

Issue #5 is promising because it asks how a microscopic field could acquire a useful large-scale fluid description. There is a real laboratory precedent: energy in an orderly condensate flow can move into smaller turbulent excitations, making its averaged shock resemble a dissipative fluid. That connects the gravity proposal to the expedition's questions about persistence, hidden information and scale selection.

The next useful step is a small model and closure test. A large collapse code would currently mix an unspecified AeST model, an added dispersive operator and an assumed meaning of entropy. A smooth numerical pancake could then answer a different question from the one intended.

Prepared by gpt-forge with gpt-6-astra, requested reasoning effort ultra, 12 November 2026. The four research clones remained read only. This pass produced analytic checks and a simulation specification, with no new astrophysical fit or nonlinear AeST simulation.

**1. The strongest case for pursuing it**

Mossman and colleagues drove a piston through a Bose–Einstein condensate. Experiments and conservative three-dimensional Gross–Pitaevskii simulations agreed. Transverse instability broke large excitations into vortices, which the authors interpret as a reservoir receiving energy from the large flow. See sections I.1–I.3 and Methods of [their 2018 paper](https://arxiv.org/html/1712.06689).

This is a concrete example of effective dissipation arising after averaging a conservative field. The piston continuously supplied energy, the trap confined the system, and the field was a complex condensate. The coarse viscous comparison also used fitted quantities, including an effective sound speed and filtering choices. It did not establish undriven retention, thermal equilibrium or an AeST entropy law.

The constructive question is therefore: **does a specified AeST model transfer infall energy into modes that remain locally useful as stress, for long enough to affect later collapse?** The amount of retained stress, its lifetime and its response to a disturbance are more informative than whether the result looks like a shock.

**2. The proposed regularizer has a known blind spot**

In a related ghost-condensate truncation, a planar profile

\[
\pi(x,t)=\frac{x^2}{2(T-t)}
\]

focuses at time T. Its second spatial derivative diverges, but its fourth derivative is zero. Thus the proposed spatial term proportional to \((\partial_x^2\pi)^2\) supplies no restoring force for this profile. This is the perfect-caustic example in [Arkani-Hamed and colleagues, section 3.5, equations 3.36–3.44](https://arxiv.org/pdf/hep-ph/0507120).

The local calculation was reproduced symbolically. Its special symmetry and unsuitable global halo boundaries matter. It is a regression benchmark for an operator's limits, not a result about full AeST. At the singularity the truncated effective theory loses validity, so continuing it numerically does not establish the physical continuation.

Scordatura means a controlled change of a theory's derivative structure. Motohashi and Mukohyama demonstrate it for a scalar-tensor model, excluding an additional high-energy branch from the low-energy description. Their operator is \(-\alpha(\Box\phi)^2/(2M^2)\). Its cutoff checks do not automatically apply to AeST. [Equations 36–37 and 53–54](https://arxiv.org/html/1912.00378v2).

In AeST, a coordinate Laplacian, a derivative projected perpendicular to the aether, and the covariant wave operator define different nonlinear additions. The sign, normalization, scale M, permitted modes and boundary data must be fixed. A physical higher-derivative extension also differs from numerical smoothing that vanishes with grid spacing.

**3. The first physical test can be smaller than a pancake**

AeST contains a metric, a scalar and a unit timelike vector. Its Hamiltonian formulation supplies constraints, not a closed scalar gas law. The full function \(\mathcal F(\mathcal Y,\mathcal Q)\) remains a model choice. [Bataki, Skordis and Zlosnik, equations 1–4 and sections IV–VII](https://arxiv.org/html/2307.15126v3).

The original linear cosmological equations express a pressure contrast Π using density δ and additional vector data. The paper explicitly states that these fluid variables do not close. [Skordis and Zlosnik, equations 7–12](https://arxiv.org/html/2007.00082v3).

Our new algebraic construction changes a vector velocity and compensates it with a scalar velocity. It leaves initial effective density, velocity and Einstein density/momentum sources equal, while changing pressure and the immediate acceleration. The symbolic identities pass. A full canonical implementation must still verify that both states satisfy every constraint and are distinct physical preparations.

This gives the smallest next test: implement one Fourier mode of the chosen linear model, validate that matched pair, and measure the extra mode's response time. A two-variable fluid law cannot predict both preparations if their later evolution differs. A restricted growing-mode preparation or a rapid relaxation limit could still admit an accurate approximation.

The effect can also be small when the background sound speed is small. Its existence therefore does not settle the error of an approximate dust model. The independent reviews preserve that distinction.

The [technical specification](../probes/issue-5/model-and-tests.md) gives the action, exact compensated pair, caustic check and initial-condition path. It also explains what must be specified before nonlinear evolution.

**4. What would make a collapse calculation interpretable**

| Requirement | Smallest useful evidence | Why it changes the conclusion |
|---|---|---|
| Complete model | Full action, function F, constants, matter coupling, background and higher operators | Different choices may give different collapse outcomes |
| Valid dynamics | Constraint propagation, physical mode count and stability in the backgrounds actually visited | A converged numerical instability is not necessarily a physical one |
| Pressure measurement | Filter the action-derived momentum stress, separating bulk transport, anisotropy and field-gradient stress | Velocity variance alone misses field stress and does not establish an equation of state |
| Energy and charge | Separate balances, outgoing flux and expansion or gravitational work | No electromagnetic radiation does not imply no energy export |
| Persistence | Stop externally imposed driving and follow stress over several local dynamical times | A driven plateau may disappear once its source stops |
| Numerical control | Refine the grid at fixed physical coefficients, resolve dispersive scales and monitor cutoff occupation | Numerical dissipation can create a false pressure or entropy floor |
| Coarse description | Vary filter scale within a resolved interval and compare repeated preparations | A fitted pressure may depend on hidden modes or the averaging convention |
| Physical scope | Test transverse perturbations after a planar result | Strict symmetry removes possible relaxation and escape channels |

For a kinetic control, the averaged stress is

\[
\tau_{ij}=\overline{\rho u_i u_j}
-\bar\rho\widetilde u_i\widetilde u_j,
\qquad\widetilde u_i=\overline{\rho u_i}/\bar\rho.
\]

An AeST calculation must derive the corresponding total stress from its action, including vector and gradient terms. Its split into effective density and pressure needs a stated frame and approximation. In spherical symmetry, retain radial and tangential stresses separately.

Even when a positive effective density is available, \(P/\rho\) is not automatically the sound speed squared. The latter is a response derivative under a specified closure. A small imposed density perturbation can test whether pressure response depends on frequency, wavelength or previous preparation.

The probe compares two free-streaming distributions with equal initial density, mean velocity and pressure. Equal-speed counterstreams retain an oscillating density mode. A Gaussian distribution with the same variance phase mixes that mode away. This exact toy shows why measuring pressure alone cannot establish thermalization. It is not an AeST prediction.

**5. Distinguish stress, dissipation and entropy**

A coherent wave train, collisionless multistreaming, an anisotropic bound field and an equilibrated gas can all carry stress. The issue's choice between an entropy floor and passage without pressure omits these intermediate outcomes. A single-valued current velocity also does not prohibit several momenta in a wave description, as the persistence route's standing-wave example shows.

Record spectra, stress correlations and energy transfer between resolved scales. Check whether a claimed shock has expanding oscillatory edges or a roughly stationary averaged width, and whether its jump conditions match the proposed closure. Condensate experiments already distinguish these structures. [Hoefer and colleagues, 2006](https://arxiv.org/abs/cond-mat/0603389).

A rise in \(K=P/\rho^\gamma\) is only an entropy diagnostic after γ, the state variables and the relevant first law have been justified. A coarse distribution can become broader through reversible phase mixing. Likewise, numerical damping can imitate irreversible heating.

Thermalization would need stronger evidence: reproducible statistics after different small-scale preparations, loss of relevant phase correlations, an appropriate equilibrium distribution and predictive response to further forcing. An effective fluid might be useful before full thermal equilibrium, but its additional state variables and error must then be retained.

Energy carried out by scalar or vector waves must be counted. In a stationary weak-gravity approximation, use its derived energy balance. In an expanding spacetime, include the work terms instead of demanding an inappropriate globally constant energy. Shift charge, gravitational energy and thermodynamic entropy are distinct quantities.

**6. What 1D can establish, and what it cannot**

A planar calculation can locate breakdown, test a regularizer, follow longitudinal stress and compare coherent passage with mixing. A spherical calculation can test radial retention and outgoing radiation. These are valuable early tests.

Strict planar or spherical symmetry cannot establish a three-dimensional isotropic pressure law. It excludes transverse wavevectors, generic tidal torques and vortex-loop dynamics. Spherical symmetry sets angular momentum and its flux to zero, so it cannot test rotational transport. A later three-dimensional experiment must record angular momentum and its flux as well as energy and charge.

The laboratory precedent makes this limitation consequential: the mechanism involved transverse instability. A negative strict-1D result cannot rule out that type of route. AeST's real shift scalar is also not automatically a complex condensate with quantized vortices. The relevant AeST transverse modes and their instabilities would have to be derived.

A manageable bridge is a planar solution with small transverse perturbations in a narrow two-dimensional domain, followed by a three-dimensional test only if those modes grow and materially alter the stress. This follows a promising mechanism without assuming that every field has the same turbulence.

**7. A local collapse test cannot select a universal 185 km/s floor**

The scales route reproduced the repository's 185.59 km/s from its spectrum, collapse threshold and halo-radius conventions. Its sensitivity tests also show that those choices affect the result. This is a characteristic population scale under the chosen cosmology. An individual pancake has its own wavelength, infall speed, environment and history.

First predict a dimensionless retention or stress relation against those controls. Then ask whether a cosmological ensemble yields the observed transition and its scatter. This requires either a self-consistent AeST spectrum or an explicitly conditional use of the external spectrum. Matching a preselected speed in one collapse does not derive the population law.

Zero fitted shape parameters in the repository's comparison does not remove the physical model choices. The action, its dispersive scale and the initial field state still need specification.

The robustness route also shows that the notebook's density-slope crossing at 2 is not a demonstrated dynamical stability threshold. A true instability claim requires a growing mode or another specified stability criterion. Neither that slope nor the fitted trapped fraction should be inserted as a boundary condition for the proposed test.

**8. Decision path**

| Result | Interpretation and next action |
|---|---|
| The compensated linear mode persists | Retain extra variables or a measured memory response before using a fluid closure |
| The model reaches its cutoff before a controlled continuation | The collapse outcome depends on omitted physics. Specify a better completion |
| Nonzero stress survives but depends on phase/history | Develop a nonthermal stress model and test its predictive response |
| Energy escapes efficiently or pressure tracks artificial boundaries | The proposed local retention mechanism is weakened in that regime |
| Stress survives loss of driving and is robust to resolution/filter changes | Test transverse stability and compare independent preparations |
| A predictive three-dimensional closure emerges | Proceed to an ensemble calculation of redshift, environment and transition scatter |

The unknown regularization and omitted modes may decide the result. Yet conservative fields have shown a route from ordered flow to effective dissipative stress in a different, measured system. The next action is to specify one AeST branch and validate its linear compensated mode, keeping the perfect caustic as a regularization benchmark.

The [reproducible script](../probes/issue-5/issue5_checks.py) checks the caustic, linear pressure difference and free-streaming comparison. Its [results](../probes/issue-5/results.json) record each identity.

The [source ledger](issue-5-sources.json) separates measured precedents, conditional field theories, repository conjectures and this pass's calculations.
