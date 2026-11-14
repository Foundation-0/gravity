# Caustic stress: the remaining research value

**Decision: pursue a finite AeST action, constraint and response test. Park the proposed three-dimensional collapse calculation until that test passes. Reject the inference that caustic smoothing plus a rising pressure proxy establishes a thermal dark fluid or a universal 185 km/s floor.**

Prepared on 12 November 2026 by gpt-forge, research model gpt-6-astra, requested reasoning effort ultra. This note assesses the read-only gravity snapshot `70a1204a536b3dca0b3053d1a056daf22601ac00`. It also reads the earlier issue-5 report and reviewed analytic checks in the verified publication snapshot `02013ae95fa5913894b829c8e2e63a3efcde9e63`. The source snapshots were not edited during the assessment.

The useful question is whether the stress left by collapse becomes predictable from a small set of large-scale variables. Stress is the momentum transported by unresolved motions and field gradients. A positive stress can exist without a temperature, an equilibrium equation of state, or efficient thermalization.

The new calculation below starts with cold infall and follows it through an actual caustic in a controlled reference problem. It tests a proposed discriminator. It does not evolve AeST.

**What the literature already supplies**

The original AeST paper explicitly states that its linear effective-fluid variables do not close: pressure depends on additional vector perturbations. Its Minkowski scalar spectrum includes a zero-frequency branch and a propagating branch. The latter has an oscillation frequency, not an established relaxation rate.

Thus a large mode frequency alone does not imply that initial excitation has been forgotten. [Skordis and Zlosnik, equations 7–12 and Stability and waves](https://arxiv.org/html/2007.00082v3).

The full Hamiltonian treatment provides six physical degrees of freedom and the constraint system for the published action. It is a starting point for constructing physical initial states. An added higher-derivative operator needs a new analysis. [Bataki, Skordis and Zlosnik](https://arxiv.org/html/2307.15126v3).

Two primary results change the value assessment. Babichev and Ramazanov show a classical complex-field completion of pressureless flow and suitable k-essence models, with restricted initial data. They distinguish this construction from a quantum ultraviolet completion.

Mocz and colleagues study the Schrödinger–Poisson correspondence with collisionless Vlasov–Poisson dynamics, including caustics and multistreaming. These results already establish that a field may smooth a caustic and still carry collisionless-like stress.

Neither is an AeST completion. [Babichev and Ramazanov, sections 2–3](https://arxiv.org/html/1704.03367v3), [Mocz et al., sections II–IV](https://arxiv.org/html/1801.03507v2).

Anisotropic stress and its relation to collapse history are also established in cosmological collisionless simulations. Merely recovering them would be a benchmark reproduction. [Buehlmann and Hahn](https://arxiv.org/abs/1812.07489).

The 2025 connection between AeST and mimetic formulations provides alternate variables and constraints under stated conditions. Its conclusion leaves the caustic question open. It does not supply a healthy regularizer, an entropy law, or a nonlinear collapse solution. [Domènech and Ganz, section VI](https://arxiv.org/html/2503.11174v1).

The remaining incremental opportunity is therefore **an AeST-specific, quantitatively controlled response law and its domain of validity**. A general claim that coarse fields can develop stress would add little to existing work.

**A cold-collapse control that the proposed entropy diagnostic can misclassify**

The reproducible [probe](caustic_control.py) uses a free complex field on a periodic interval of length \(2\pi\):

\[
i\epsilon\partial_t\psi=-\frac{\epsilon^2}{2}\partial_x^2\psi,
\qquad \psi(x,0)=\exp[i\cos x/\epsilon].
\]

Here \(\epsilon\) is a fixed physical dispersion parameter in dimensionless units. The density is initially one and the phase velocity is \(v=-\sin x\). There is no gravity, collision term, nonlinear wave interaction, bath or continuing drive. The reference cold particles obey

\[
x(q,t)=q-t\sin q,\qquad v(q,t)=-\sin q,
\]

with uniform mass per label \(q\). Their Jacobian is \(1-t\cos q\), so the first caustic occurs at \(t=1\). The particle distribution remains a well-defined multistream measure after that time. This ballistic map is not a nonlinear gravitational solution or an AeST approximation derived from its action.

The wave evolution is exact for every represented Fourier mode:

\[
\widehat\psi_k(t)=\widehat\psi_k(0)
\exp[-i\epsilon k^2t/2].
\]

No time-stepping algorithm or numerical viscosity is used. The field is smooth across the reference caustic. The momentum density and momentum flux follow directly from its equation:

\[
\rho=|\psi|^2,\qquad
j=\epsilon\operatorname{Im}(\psi^*\psi_x),\qquad
T=\epsilon^2|\psi_x|^2-\frac{\epsilon^2}{4}\rho_{xx},
\]

\[
\rho_t+j_x=0,\qquad j_t+T_x=0.
\]

For a periodic Gaussian filter with Fourier multiplier \(e^{-\ell^2k^2/2}\), measure

\[
\bar\rho=W_\ell*\rho,\quad \bar j=W_\ell*j,\quad
\tau_{xx}=W_\ell*T-\bar j^2/\bar\rho.
\]

The filtered flux includes the field-gradient contribution. Replacing it with velocity variance alone would be a different diagnostic. In this planar calculation \(\tau_{xx}\) is longitudinal stress, not an isotropic three-dimensional pressure. Define \(K_{5/3}=\tau_{xx}/\bar\rho^{5/3}\) only to test the proposed proxy. No first law or adiabatic index has been derived for it.

For \(\epsilon=0.02\), \(\ell=0.2\), at the symmetry center:

| Time | Filtered density | Longitudinal stress | \(K_{5/3}\) proxy |
|---:|---:|---:|---:|
| 0 | 1.000000 | 0.038442 | 0.038442 |
| 0.9 | 3.843709 | 1.119290 | 0.118675 |
| 1.5 | 4.790675 | 2.658210 | 0.195252 |
| 3 | 1.185239 | 0.401579 | 0.302525 |
| 6 | 0.514422 | 0.063302 | 0.191669 |

The proxy rises by 5.08 times from the initial state to \(t=1.5\). It already rises before the caustic. Its initial nonzero value comes from averaging an orderly velocity gradient over a finite spatial window. The initial microscopic flow is cold. Every Fourier occupation \(|\widehat\psi_k|^2\) is constant throughout this experiment.

There is no scattering between these modes and no relaxation to a thermal momentum distribution. The mode momentum distribution has variance 1/2 and fourth moment \(3/8+\epsilon^2/2\), also checked numerically. At \(\epsilon=0.02\), its kurtosis is 1.5008 throughout, compared with 3 for a Gaussian. This does not identify the field with a classical thermal gas.

Complex conjugation at \(t=1.5\), followed by evolution for another 1.5 time units, recovers the conjugated initial field to a relative error below \(5.5\times10^{-16}\). Conjugating once more returns the original state. Mean mass is 1 and mean energy is 0.25, conserved within \(2\times10^{-12}\). Mean momentum vanishes at the same tolerance.

The maximum relative residuals of the local mass and momentum balances are \(2.4\times10^{-12}\) and \(6.2\times10^{-10}\). The latter differentiates a flux and is more sensitive to floating-point error. All checks pass.

Time reversibility alone does not refute thermodynamics: interacting Hamiltonian systems can also have useful irreversible coarse descriptions. The decisive facts here are the noninteracting generator, its conserved mode occupations, and the collisionless reference comparison. The reversal checks that the displayed proxy increase was not caused by dissipative numerics.

Periodicity also precludes interpreting retained box energy as retention in an isolated halo. The exact recurrence at \(4\pi/\epsilon\) is a property of this control, not a prediction about astrophysical systems.

**Resolution, dispersion and filter controls**

At fixed physical \(\epsilon=0.01\), \(\ell=0.2\), doubling the grid from 2,048 to 4,096 points changes the sampled filtered density, current and stress by at most \(1.8\times10^{-15}\). The fraction of field norm above one quarter of the grid size in Fourier wave number is below \(7\times10^{-29}\). Spatial resolution is varied independently of the physical dispersion.

The classical Fourier density coefficients are \(\rho_m(t)=J_m(mt)\). For \(m>0\), current and second-moment coefficients are \(iJ'_m(mt)\) and \(-J''_m(mt)\). Their zero modes are 0 and 1/2. These formulas follow by integrating the exact particle map over \(q\). The script independently checks their filtered central moments against direct Lagrangian quadrature.

At \(t=1.5\), \(\ell=0.2\), reducing dispersion gives:

| \(\epsilon\) | Relative density error against classical moments | Relative stress error against classical moments |
|---:|---:|---:|
| 0.08 | 4.9750% | 4.5935% |
| 0.04 | 1.2264% | 1.4111% |
| 0.02 | 0.3040% | 0.3721% |
| 0.01 | 0.0758% | 0.0943% |

These are spatial \(L^2\) errors after the same filter. They establish convergence for this test and these parameters, not a general convergence theorem. Repeating with \(\ell=0.1,0.2,0.4\) is recorded in [results.json](results.json). At \(\epsilon=0.02\), the central stress is 2.47052, 2.65821 and 2.00613 respectively. The corresponding proxies are 0.195324, 0.195252 and 0.254133.

A near match at two filter choices is therefore not evidence of a universal thermodynamic state variable.

**What the control says about closure**

Use three regular cold initial sheets,

\[
x_i(q)=q-D_i\sin q,\qquad v_i(q)=-a\sin q,
\]

with \((a,D_i)=(0.75,0.75),(1,0.5),(1.5,0)\). Their initial Jacobians are positive. At the same time \(t=1\), all have the identical position map \(x=q-1.5\sin q\) and therefore the same entire density profile. At the symmetry center, all have zero mean velocity. Their stresses differ because the infall speeds differ:

| \(a\) | First caustic time | Central filtered density | Central mean velocity | Central stress at \(t=1\) |
|---:|---:|---:|---:|---:|
| 0.75 | 1/3 | 4.772108 | 0 | 1.491776 |
| 1.00 | 1/2 | 4.772108 | 0 | 2.652046 |
| 1.50 | 2/3 | 4.772108 | 0 | 5.967103 |

This is a fourfold stress range at equal local density, velocity, time and filter. It excludes a universal stress function of only those quantities for this ensemble. It does not exclude a closure that retains energy, velocity gradients or additional moments. The full velocity profiles of these preparations differ away from the center. The example does not claim otherwise.

Embedded in three spatial dimensions with no transverse motion, the classical stress eigenvalues are \((\tau_{xx},0,0)\). Its traceless part has Frobenius norm \(\sqrt{2/3}\operatorname{tr}\tau\). This is strong anisotropy, which an isotropic pressure would discard. Transverse dynamics in a different interacting theory could change that result.

Even retaining pressure need not suffice. The conserved velocity marginal generated by the uniform cold sine preparation is the arcsine distribution

\[
g(v)=\frac{1}{\pi\sqrt{1-v^2}},\qquad |v|<1.
\]

It has variance 1/2 and fourth moment 3/8. A Gaussian with the same variance has fourth moment 3/4. As a separate response control, prepare spatially homogeneous versions of each marginal, multiply by \(1+\eta\cos kx\), and evolve by free streaming. The normalized density responses are \(J_0(kt)\) and \(e^{-(kt)^2/4}\). At \(kt=2.40482556\), one is zero and the other is 0.235558.

These responses concern deliberately prepared homogeneous kinetic states. They are not a claim that the finite-time wave solution has exactly become homogeneous, nor a simulation of a perturbation applied to AeST.

The calculation verifies a necessary diagnostic distinction. Its mathematics and physical mechanism are established. Its project value is preventing a false positive in issue #5 and supplying a cheap regression case.

**The finite AeST gate**

The earlier reviewed compensated linear construction remains conditional on a full canonical initial-data check. This pass did not complete that map or run an interacting AeST model. Failure of the proxy above does not prove that AeST cannot form an approximate pressure closure. It shows that the proposed evidence would not establish one.

| Step | Deliverable and dependencies | Pass criterion | Stop or change criterion |
|---|---|---|---|
| 1. Choose one physical branch | Full \(\mathcal F(\mathcal Y,\mathcal Q)\), constants, matter sector, background, units and parameter provenance. Start with the published action before adding a regulator. Requires a theory choice, not a large codebase. | Every coefficient and derivative needed by the linear equations is fixed, and the background solves those equations. | If several inequivalent choices remain hidden under “AeST,” park the collapse task. An arbitrary convenient choice only tests that declared model. |
| 2. Construct physical states | Gauge-fixed linear state, canonical map, all constraints, and the earlier compensated pair. Needs symbolic algebra, the published Hamiltonian equations, and independent review. | Both states satisfy the linearized constraints at the retained order. Their stress difference is gauge independent and changes an observable response. | If the pair is gauge or inadmissible, withdraw it. Recompute whether any allowed hidden mode affects retained observables. |
| 3. Measure response | A small ODE solver for each Fourier mode, a wave-number grid, growing-mode and permitted extra-mode preparations. Measure density/current/stress transfer functions. No three-dimensional mesh is required. | A declared set of retained variables predicts held-out preparations over the intended scale and time interval within a tolerance chosen before fitting. Report the error of a two-variable closure and the improvement from adding the relevant mode. | Persistent preparation dependence requires an extra state variable or memory kernel. An unstable selected branch or invalid approximation stops that branch. |
| 4. Decide on collapse | Full action-derived stress and energy flux, intended cutoff and candidate regulator, with a controlled parameter range. | There is a credible interval between resolved physical dispersive scales and the effective-theory cutoff, and an explicit observable that distinguishes competing outcomes. | If omitted operators become important before or at the caustic, the continuation is completion dependent. Do not label it an AeST prediction or launch a three-dimensional production study. |

For a concrete internal acceptance target, use a 5% normalized response error over the declared domain, with numerical error at least ten times smaller. These numbers are prospective project tolerances, not laws of nature or observational constraints. Pressure errors alone are insufficient if density or lensing-related metric responses are inaccurate.

The allowed initial-mode amplitudes also require a physical preparation argument. Unrestricted large excitations could make any restricted approximation fail by construction.

One can expose the issue without guessing a pressure formula. After fixing constraints, split the linear physical state into retained variables \(x\) and omitted variables \(y\):

\[
\dot x=A_{xx}x+A_{xy}y,\qquad
\dot y=A_{yx}x+A_{yy}y.
\]

For constant coefficients, eliminating \(y\) gives

\[
\dot x(t)=A_{xx}x(t)+A_{xy}e^{A_{yy}t}y(0)
+\int_0^t A_{xy}e^{A_{yy}(t-s)}A_{yx}x(s)\,ds.
\]

The second term preserves initial preparation and the integral preserves prior evolution. In an expanding background, the exponential becomes the appropriate propagator between two times. A local approximation is earned by showing that these terms are negligible or compressible into specified extra variables over the domain of interest.

Oscillation averaging, expansion damping and nonlinear scattering are different possible reasons. The calculation must identify which one is operating.

A reasonable first allocation is two focused theory sessions for the action and constraint specification, followed by one implementation and one independent-review session for the linear response. This is a scope estimate, not a completion promise. Required software is symbolic algebra plus a small numerical ODE implementation.

Required expertise is the AeST canonical reduction and its cosmological perturbations. No new observational dataset, GPU cluster or general relativity simulation framework is needed for this gate. If the first two sessions do not yield a reviewable fixed branch and constraint map, retain the open question and stop spending on simulation infrastructure.

Only a passing gate would justify a small nonlinear experiment. Its target should be a measured stress response and lifetime after infall, with energy export and transverse effects checked in stages. Selecting a universal velocity scale requires a cosmological population calculation after that. It cannot be inferred from one periodic pancake, and the present control selects no velocity in km/s.

**Extra-dimensional interpretation**

Park this route within the current project. Five-dimensional braneworld black holes already have explicit constructions whose low-curvature brane limit reproduces four-dimensional general relativity. Their existence is not evidence that ordinary redshift or a horizon requires an extra dimension. [Figueras and Wiseman](https://arxiv.org/abs/1105.2558).

Reopen only for a specified action, geometry, boundary conditions and a calculated observable that differs from an adequate four-dimensional baseline. A dimensional reinterpretation without that difference supplies no falsifiable incremental target. This is a judgment about the formulation and research value, not a general exclusion of extra dimensions.

All new numerical evidence is in [results.json](results.json). Source scope and limitations are in [sources.json](sources.json). The probe is a validated diagnostic control. The AeST response gate remains proposed work.
