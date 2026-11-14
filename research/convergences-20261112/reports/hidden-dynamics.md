# Hidden variables, memory and effective dynamics

This report reviews the repository revisions recorded in the source ledger. It does not review later changes on main, including gravity Wave 11. Original research: gpt-forge, gpt-6-astra, requested reasoning effort ultra. Publication preparation: gpt-6.1-sol.

Leaving part of a system out of a description can make the remaining part appear to remember its past. This has a precise mathematical meaning: the omitted part evolves, receives influence from the part we kept, and can return that influence later. A local equation for the full system can therefore become an equation with memory for the smaller description.

Classical mechanics, open quantum systems and fluid reductions share this operation without sharing one microscopic theory.

The useful question for Foundation0 is: **which information must a description retain to predict what happens next?** An instantaneous density and velocity might be enough for one purpose and insufficient for another. A stored record might tell an observer about the past while having no influence on the future.

Combining observations can repair an incomplete description, but it does not by itself establish a physical memory mechanism.

The strongest result of this pass is that shared reduction methods explain a real family of convergences. They also supply a practical test: hold the proposed present state fixed, vary what the description omitted, and check whether the future changes. The scope of that test matters. Different futures refute a complete deterministic prediction from those variables.

A stochastic memory claim needs a comparison of conditional probability distributions.

Prepared by gpt-forge, 12 November 2026. Expedition model: gpt-6-astra, requested reasoning effort ultra. Existing repositories were read only. These are literature-supported connections and small mathematical examples, with no new physical law or observational discovery claimed.

**1. The distinct possibilities**

| Operation or observation | What can result | What it does not establish | Repository connection |
|---|---|---|---|
| Eliminate interacting dynamical variables | A history kernel and an influence from the hidden initial state | A new fundamental force, thermal noise or irreversible entropy production | gravity's proposed fluid reduction, fractals' turbulence |
| Replace a short response time by an instantaneous response | Effective damping, stiffness or transport coefficients | Validity during rapid changes, resonance or long-lived hidden modes | scale selection, galaxy and cluster approximations |
| Trace out a quantum environment | Reduced quantum dynamics with possible dependence on earlier controls | Accessible redundant records, or memory merely because an integral appears | Witness Map, quantum-information projects |
| Retain more state variables | A larger description with simpler time evolution | That every useful description can be made small and memoryless | physics0's preference for explicit checkable models |
| Join histories, instruments or observation channels | Better inference about hidden states or parameters | A causal influence of earlier observations on the object | astr0, evidence route |
| Eliminate a static constraint | An interaction that can be nonlocal in space | Temporal memory | quasistatic gravity, electrostatic equilibria |

Here, a *history kernel* is a rule assigning weight to earlier states when calculating the present rate of change. A *closure* supplies the influence of omitted quantities using the variables retained in a model. An exact closure can be too costly to evaluate. A convenient closure can be wrong.

**2. An exact identity underneath the comparison**

Consider a linear system divided into quantities we retain, \(x\), and quantities we omit, \(y\):

\[
\dot x=Ax+By,\qquad \dot y=Cx+Dy.
\]

Solving the second equation and substituting it into the first gives

\[
\boxed{\dot x(t)=Ax(t)+Be^{Dt}y(0)
+\int_0^t Be^{D(t-s)}C x(s)\,ds.}
\]

The three terms have different jobs. The first uses the retained present state. The second carries the hidden initial condition. The integral tracks how an earlier \(x\) changed \(y\), which then acts back on \(x\). Nothing was discarded in this algebra. The new equation gives exactly the same retained trajectory as the original pair.

This is an elementary instance of the Mori-Zwanzig projection method. That method extends the idea to nonlinear dynamics by evolving functions of the state with a linear operator and then projecting onto selected information. The resulting kernel need not be a fixed scalar function of the time difference. The choice of projection and initial ensemble matters.

Chorin, Hald and Kupferman give the nonlinear identity and its connection to conditional expectations in section 2, equations 3–7. [Primary paper, 2002](https://math.berkeley.edu/~chorin/CHK02.pdf).

The box above is independently derived by an integrating factor. It is exact for finite matrices. For fields or infinite-dimensional operators, existence, domains and boundary conditions must also be supplied. A formal elimination is not a solution of those analytical problems.

If \(y(0)\) is uncertain, its term can be treated statistically. That does not make it white noise, Gaussian noise, or thermal noise. For example, if a scalar hidden initial value has variance \(\sigma^2\), the forcing \(e^{-\gamma t}y(0)\) has covariance \(\sigma^2e^{-\gamma(t+s)}\). This depends on both times separately and is not stationary.

Equilibrium fluctuation-dissipation formulas require additional statistical and dynamical assumptions. The projection alone does not authorize them. Zwanzig's exact nonlinear Langevin construction also specifies the heat baths to which it applies. [Zwanzig, 1973, abstract](https://link.springer.com/article/10.1007/BF01008729).

There is a simple closure criterion. If the full state is \(z\), its evolution is \(\dot z=F(z)\), and the recorded state is \(x=h(z)\), an autonomous deterministic equation \(\dot x=f(x)\) requires

\[
Dh(z)F(z)=f(h(z))
\]

throughout the allowed states. In ordinary words, all full states with the same recorded state must give the same recorded derivative. This follows directly from the chain rule. A restriction to an invariant family of initial conditions can change whether the requirement holds. Knowing only a particular trajectory is a much weaker condition.

**3. A reproducible example with two levels of claim**

The local probe uses

\[
\dot x=-x+y,\qquad \dot y=-\gamma(x+y),\qquad \gamma>0.
\]

Eliminating \(y\) gives

\[
\dot x=-x+e^{-\gamma t}y(0)
-\gamma\int_0^t e^{-\gamma(t-s)}x(s)\,ds.
\]

For \(\gamma=1\), the exact solution is

\[
x(t)=e^{-t}\big[x(0)\cos t+y(0)\sin t\big].
\]

Two preparations with the same observed \(x(0)=0\) and hidden values \(y(0)=+1\) and \(-1\) give \(x(1)=+0.3095599\) and \(-0.3095599\). Thus \(x(0)\) alone cannot determine the future across those preparations. The hidden variable is a real dynamical degree of freedom in this example, not a missing row in a dataset.

The same model can be written without a history integral:

\[
\ddot x+(1+\gamma)\dot x+2\gamma x=0,
\qquad \dot x(0)=-x(0)+y(0).
\]

This equation needs an extra initial value. The missing information moved into the velocity. It did not disappear. Memory depends on which quantities count as the present state.

The probe independently integrates the original two equations with fourth-order Runge-Kutta and the scalar memory equation with trapezoidal quadrature. Both are compared against the analytic solution on \(0\leq t\leq6\), with \(x(0)=1,y(0)=-1,\gamma=1\).

| Time step | Maximum error, full equations | Maximum error, scalar memory equation |
|---|---:|---:|
| 0.04 | \(4.90\times10^{-8}\) | \(8.04\times10^{-5}\) |
| 0.02 | \(2.98\times10^{-9}\) | \(2.01\times10^{-5}\) |
| 0.01 | \(1.84\times10^{-10}\) | \(5.02\times10^{-6}\) |
| 0.005 | \(1.14\times10^{-11}\) | \(1.26\times10^{-6}\) |

The memory solver's error falls by a factor of four when the step is halved, as expected for this quadrature. These checks verify the example and its numerical implementation, not a model of gravity.

Different outcomes from the same observed value do **not**, by themselves, refute a stochastic Markov model. Ordinary memoryless random processes also have different possible futures. To test that stronger claim, the probe adds independent white driving to both equations at \(\gamma=1\):

\[
dx=(-x+y)dt+\sqrt2\,dW_x,
\qquad dy=(-x-y)dt+\sqrt2\,dW_y.
\]

This is an exactly specified continuous-time linear Gaussian model with additive independent driving. Here \(W_x,W_y\) are independent standard Wiener processes. Start the pair in its stationary Gaussian distribution, with zero means, unit variances and zero cross-covariance. Its retained covariance is \(C_x(t)=e^{-|t|}\cos t\). For three samples separated by \(\Delta=\pi/4\), direct Gaussian conditioning gives

\[
\operatorname{Cov}[x(0),x(2\Delta)\mid x(\Delta)]
=C_x(2\Delta)-C_x(\Delta)^2=-0.1039398.
\]

This nonzero value proves that the observed past still changes the distribution of the observed future after the observed present is known. The conditional mutual information is 0.0067733 nats. This is a statistical memory witness for this specified stationary process. Its full two-variable process remains Markovian.

Run with Python 3, using only its standard library:

```sh
python3 ../probes/hidden-dynamics/hidden_dynamics.py
```

The [script](../probes/hidden-dynamics/hidden_dynamics.py), [results](../probes/hidden-dynamics/results.json) and [trajectory table](../probes/hidden-dynamics/trajectories.csv) are saved locally. All built-in checks passed.

**4. When an approximation looks like a changed law**

If \(\gamma\) is large and \(x\) changes slowly compared with \(1/\gamma\), the hidden variable approximately follows \(y=-x\). Then the two equations reduce to \(\dot x\simeq-2x\). This is a useful approximation with a stated range, unlike the exact elimination above.

For the prepared initial state \((x,y)=(1,-1)\), the maximum absolute error of \(x=e^{-2t}\) on \([0,6]\) is 0.26398 at \(\gamma=1\), 0.03790 at 10, and 0.003697 at 100. Unprepared initial conditions can add a short initial transient. Fast hidden relaxation is useful only relative to the timescales and accuracy of the question being asked.

A conservative mechanical example makes the apparent-force issue explicit. Two coordinates coupled by a spring obey

\[
m\ddot x=-(k+\kappa)x+\kappa y+F,
\quad M\ddot y=-(K+\kappa)y+\kappa x.
\]

For positive masses and spring constants, eliminating \(y\) gives a sinusoidal history kernel and a term containing its initial displacement and velocity. With \(\Omega^2=(K+\kappa)/M\), that kernel is \(\kappa^2\sin(\Omega\tau)/(M\Omega)\). Under a slow forcing and negligible free hidden oscillation, the effective spring constant is

\[
k_{\rm eff}=k+\kappa-\frac{\kappa^2}{K+\kappa}.
\]

Changing the hidden mass \(M\) leaves this static stiffness unchanged but changes the transient and resonant response.

The effect can be described as a changed effective force law for \(x\), with the full two-coordinate law left intact. Because the undriven full system is conservative, eliminating one coordinate does not create irreversible energy loss. Its kernel oscillates instead of simply decaying. This is a counterexample to the claim that all elimination produces friction.

An analogous distinction occurs in effective field theory. A heavy field can generate a nonlocal expression when removed exactly. A controlled expansion at energies well below its mass gives local corrections. Burgess works through an explicit scalar model, including the propagator expansion in equation 20. [Burgess, 2007, section 2.1](https://arxiv.org/html/hep-th/0701053).

An effective action for scattering and a causal equation for an initial-value problem also require different boundary prescriptions. One cannot silently substitute a Feynman propagator for a retarded response.

These constructions do not derive MOND. Neither projection nor elimination selects an acceleration scale, a MOND interpolation law, an acceptable lensing prediction, or a stable relativistic completion. Those require an actual model and its constraints. Eliminating a nondynamical field, such as a Newtonian potential fixed by a Poisson constraint, can instead produce spatial nonlocality without temporal memory.

**5. The narrow connection to AeST and fluid closure**

The gravity repository's [claim C-26](https://github.com/Foundation-0/gravity/blob/d8c7544e89388720fc1c13de816ddb7dd03d2096/CLAIMS.md#L128) already labels its post-caustic fluid treatment a conjecture.

The [notebook](https://github.com/Foundation-0/gravity/blob/d8c7544e89388720fc1c13de816ddb7dd03d2096/RESEARCH_NOTEBOOK_AND_REASONING.md#L38) makes stronger suggestions about shock heating and retained dark-sector entropy. The persistence route identifies both the missing energy-export calculation and the limits of the fluid analogy.

AeST itself gives a precise reason for care. In linear cosmological perturbation theory, Skordis and Zlosnik define effective density and velocity variables that obey fluid-shaped evolution equations. Their pressure contrast also depends on the vector perturbations \(\alpha\) and \(E\), so it does not close in those fluid variables. See equations 7–12 and the paragraph after equation 11.

The paper also chooses the low-gradient action's functional form to obtain MOND behavior. [Skordis and Zlosnik, 2021](https://arxiv.org/html/2007.00082v3).

Our inference is that this is a concrete place to ask a reduction question. After gauge fixing and solving constraints, can the additional independent modes be removed while retaining a short, accurate pressure law? If they are dynamical and feed back, exact elimination can retain their initial conditions and history.

If they relax rapidly or are restricted by the allowed preparation, a simpler closure might work in that regime.

The published nonclosure statement does not prove that AeST has long memory in halos, that its pressure is thermal, or that its nonlinear collapse behaves like an ordinary gas. No AeST kernel or collapse solution was calculated here. Linear cosmological perturbations cannot settle post-caustic evolution.

A focused next probe is possible before a large simulation. Work with one Fourier mode in the linear, constraint-reduced theory. Identify whether two physically allowed states can have the same proposed fluid variables but different independent vector data. Evolve both. Measure the divergence of the pressure and retained variables, then compare it with the hidden-mode relaxation time.

Failure to find such allowed states would itself clarify which apparent freedoms were constraints or gauge choices. Extend to nonlinear collapse only after that accounting is clear.

There is a parallel lesson for turbulence. Parish and Duraisamy derive exact coarse equations with memory and then introduce approximations. For a specified discretization of linear advection, a particular finite-memory approximation reproduces an upwind flux correction.

They also state that formal elimination alone does not reduce computational cost, and that generic dissipativity cannot be assumed. [Parish and Duraisamy, sections 3.1, 4 and 6.3](https://arxiv.org/html/1712.09669v1). Thus a familiar effective term can arise through reduction, while its validity remains tied to the equation and approximation used.

**6. Open quantum dynamics: a record needs a return path to become feedback**

For a full quantum state evolving as \(\dot\rho=\mathcal L\rho\), choose the projection

\[
P\rho=(\operatorname{Tr}_E\rho)\otimes\rho_E^*,\qquad Q=1-P,
\]

where \(\rho_E^*\) is a fixed reference environment state. Applying the same block-elimination algebra to \(P\rho\) and \(Q\rho\) gives the Nakajima-Zwanzig equation. Its hidden-initial-state contribution vanishes when \(Q\rho(0)=0\). More general correlated projections can absorb some initial correlations into the retained description. This changes the bookkeeping, not the underlying dynamics.

Breuer gives the standard projection, memory kernel and conditions on initial states in sections II.1 and III.3. [Breuer, 2007](https://arxiv.org/html/0707.0172v1).

An integral in a chosen representation is not the definition of physical quantum memory. For a specified initial preparation family, where the reduced propagator is invertible, a time-local equation can encode non-Markovian evolution through its generator. The representation can become singular when invertibility fails.

The distinction concerns the process under possible interventions, not how the equation is typeset. [Breuer, section II.2](https://arxiv.org/html/0707.0172v1).

Pollock and colleagues test this operationally: reprepare the system in the same state, then ask whether earlier controls still change its future. Their Appendix B.3 gives a particularly small example. Begin with \(\rho_S\otimes|0\rangle\langle0|_E\), swap system and environment, reset the system to \(|0\rangle\), then swap again. The system ends in the earlier \(\rho_S\), despite the reset.

The environment starts pure and uncorrelated, both swaps are ideal, and the reset affects only the system. At the sampled steps the joint states are products. This establishes memory without requiring contemporaneous system-environment entanglement. [Pollock et al., 2018, operational criterion and Appendix B.3](https://arxiv.org/html/1801.09811v1).

The local probe reproduces the swap calculation for initial \(|0\rangle\), \(|1\rangle\) and \(|+\rangle\). The first two preparations have zero trace distance on the system after the reset and distance one after the second swap. The middle product-state defect is zero. These are exact small-matrix calculations, not claims about what happens during a particular continuous gate implementation.

The opposite direction is also informative. Suppose each interaction uses a fresh, independent environment fragment, and old fragments never interact with the system or new fragments again. The future system channel depends on its present state and the fresh fragment. Old fragments can retain readable records while providing no feedback.

Copying a classical pointer value into several outgoing fragments supplies a simple example. Here the assumptions of fresh independent inputs and no return interaction are essential.

This adds a third question to the relations route's distinction between interference and accessible records:

| Question | Quantity or test |
|---|---|
| Has interference become inaccessible in the chosen system measurement? | Specified coherence or visibility |
| Can separate environment fragments reveal the selected property? | Fragment information and record redundancy |
| Can the past influence the future through omitted degrees of freedom after the retained state is reset? | A controlled memory test |

Riedel and Zurek's isotropic-illumination limit already separates decoherence from redundant photon records. [Figure 2(b), equations 17–18](https://arxiv.org/html/1001.3419v2). The swap and fresh-fragment examples separate records from feedback. A Witness Map companion could present these cases beside each other without claiming that one number measures all three.

**7. What multiple observations can and cannot recover**

The forced classical probe has response

\[
\chi_\gamma(s)=\frac{s+\gamma}{s^2+(1+\gamma)s+2\gamma},
\]

where an external input is added to \(\dot x\) and \(s\) is the Laplace frequency. All positive \(\gamma\) give the same static response, \(\chi(0)=1/2\). At angular frequency one, the response amplitude is 0.63246 for \(\gamma=1\) and 0.45209 for \(\gamma=20\). A static measurement cannot distinguish these hidden relaxation times. A controlled changing input can.

This is a specific mathematical version of the user's intuition about bringing observations together. The extra view helps because it probes a distinction the first view missed. It need not reveal every hidden detail.

In the general linear formula, the retained response contains \(B(sI-D)^{-1}C\). A change of hidden coordinates \(y'=Ty\), with invertible \(T\), leaves this quantity unchanged when the coefficients transform with it. Adding a completely uncoupled hidden sector also leaves every retained observation unchanged.

Such added dynamics could be physically different while remaining invisible to this channel. Even perfect retained response data therefore need not identify a unique microscopic description.

The evidence route's ASASSN-24fw case is an observational counterpart with a different mechanism: DASCH alone leaves a half-period alias, while ASAS covers the discriminating epoch and excludes it. [Primary paper, section III.1](https://arxiv.org/html/2507.05367v3). That resolves missing phase coverage. It does not show a memory kernel in the star's force law.

Three uses of the word *memory* must stay separate. A physical environment can store and return influence. An observer's past data can improve inference about an unknown but fixed parameter. An archive can preserve a readable record. All involve information persisting, but only the first necessarily asserts feedback dynamics.

A statistically detected history dependence can also arise from unresolved parameters, colored measurement noise or selection. It needs a measurement model before it becomes evidence about the object's dynamics.

**8. What would strengthen or weaken the connections**

| Proposed intersection | Strongest objection or counterexample | Discriminating next probe |
|---|---|---|
| AeST's fluid analogy may hide important dynamical state | Constraints, preparation restrictions or fast relaxation might permit an accurate closure in the regime of interest | Compare allowed full states sharing the proposed fluid variables, then measure pressure and future response |
| Environmental records are a kind of dynamical memory | Outgoing records need never return. Swap memory needs no correlations at sampled times | Compare fresh fragments, recycled fragments and controlled system resets in one finite model |
| Similar effective laws can arise from different hidden systems | Equality of an equation can be only a coordinate rewriting of the same system | Vary forcing frequency and observe a second channel, then separately quotient out coordinate changes |
| Coarse dynamics explains some cross-domain repetition | Some quantities already form an exact autonomous subsystem. Some eliminations are static constraints | Test closure across matched present states and distinguish temporal from spatial nonlocality |
| A history term suggests dissipation or an arrow of time | A finite conservative oscillator bath has oscillatory memory and recurrences | Track total energy and recurrence while varying bath size, preparation and observation duration |
| More historical data reveals omitted physics | Fixed parameter uncertainty and shared instrument errors can also reward longer histories | Compare predictive gain against explicit parameter and instrument null models |

The philosophical lesson is limited but useful. A present state is a choice about what information is being retained. When that choice is too small for the intended prediction, the missing influence can reappear as a dependence on history. This does not make the past an additional force or prove that everything is fundamentally relational. It gives an operational way to ask whether a description is sufficient.

The next calculation with the clearest project value is the constrained linear AeST closure test, paired with the small Witness Map comparison of interference, records and feedback. The [source ledger](hidden-dynamics-sources.json) distinguishes established mathematical results, conditional physical models, the repository's conjectures and this pass's inferences.
