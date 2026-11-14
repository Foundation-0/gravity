Repetition becomes useful when we can say what survives a change and predict what will break it. The most concrete connection here joins the incentre lattice to statistical physics. The lattice can fold into the positions of a close-packed crystal while its original network of interactions stays different from that crystal's full contact network.

This report reviews the repository revisions recorded in the source ledger. It does not review later changes on main, including gravity Wave 11. Original research: gpt-forge, gpt-6-astra, requested reasoning effort ultra. Publication preparation: gpt-6.1-sol.

A small exact calculation makes this distinction visible. Along the repository's cab-to-fcc motion, packing density rises by a factor of 3.31658. The original network keeps five neighbors per site. At the final position, each site touches twelve others. A spin model on the original bars and a spin model on all final contacts therefore answer different physical questions.

The broader search found several useful common rules: rescaled Coulomb wave equations, conservative linear dynamics, critical behavior after coarse-graining, conserved turbulent flux, and discrete scale repetition. They support transfers of methods and predictions. None establishes a single mechanism behind all repeated structures.

Research pass: 12 November 2026. Seat: gpt-forge. Model: requested gpt-6-astra, ultra reasoning. Existing repositories remained read-only. Source IDs and access details are in the accompanying JSON ledger.

**What kind of repetition is present?**

| Kind | What stays the same | Repository connection | Test that distinguishes it |
|---|---|---|---|
| Same equation after changing units | A dimensionless operator and its solutions, within stated approximations | fractals gravitational atom | Compare full spectra and shapes, then relativistic and horizon corrections |
| Same form of evolution | A linear conservative generator | gravity disk-wave pointer and fractals classical crowd waves | Identify what the complex amplitude measures and which inner product is conserved |
| Same limiting statistics | Critical exponents and suitably normalized functions | fractals critical model and physics0 lattice proposal | Change microscopic couplings and compare several observables near the critical point |
| Same conserved transfer | Flux through successive scales | fractals turbulence | Test a signed third-order relation and scale-dependent tails |
| Same state after a transformation | Time recurrence, particle permutation, translation or rotation | physics0 periodic orbits and lattice geometry | Remove symmetry copies, then test stability and closure |
| Repetition at selected magnifications | A discrete scaling ratio or echo period | Efimov physics and critical gravitational collapse | Predict successive resonances or logarithmic echoes under changed controls |
| Same apparent outline | A projected or thresholded image | fractals cloud edges and astr0 archival signals | Match the observation operator, resolution and null model |

**The lattice connection: geometry, connections and interaction law are separate choices.**

The physics0 survey proposes percolation and Ising calculations on the CaB6 boron net. The existing geometry project supplies an explicit continuous motion from its open cab arrangement to fcc sphere positions. Its prior framework family is documented in Borcea and Streinu's [Periodic tilings and auxetic deployments, Section 7](https://doi.org/10.1177/1081286520948116).

The paper's Section 7 was read from the NSF-hosted author manuscript. It describes bridged cross-polytopes in arbitrary dimension and an octahedral deployment in three dimensions. Its bars have a different length ratio. It supplies prior art for the framework family, without establishing the repository's particular equal-bar fcc curve.

The probe uses the repository's six-point motif, consisting of the positive and negative unit coordinate vectors. Twelve internal edges form an octahedron, and three bridges connect neighboring cells. Thus each site has four internal neighbors and one bridge neighbor. The curve moves the cell vectors while preserving these fifteen bars.

| State on the curve | Packing fraction | Original bar neighbors per site | All exact contacts per site |
|---|---:|---:|---:|
| Open, s = 0 | 0.22326612 | 5 | 5 |
| s = 0.50 | 0.34228239 | 5 | 5 |
| s = 0.90 | 0.63430089 | 5 | 5 |
| s = 0.99 | 0.72920962 | 5 | 5 |
| fcc positions, s = 1 | 0.74048049 | 5 | 12 |

These contact counts extend beyond a numerical scan. The probe checks 30 directed bar identities and 6,120 nonbar distance polynomials using exact integer pairs representing a + b√2. Each nonbar polynomial has nonnegative Bernstein coefficients, with at least one positive coefficient. The corresponding distance is strictly above contact throughout 0 < s < 1.

The source's bound on distant periodic images completes that finite check: the smallest singular value of the cell matrix is at least one, and a motif difference has length at most two. Translations with squared length at least twelve cannot make contact. At s = 1, all coordinates are integers, so the twelve-neighbor count is also exact.

Consider a scalar Ising model with the same coupling J on each original bar:

```text
H(spins; s) = -J sum_over_original_bars spin_i spin_j
Z(T; s) = sum_over_spin_states exp[-H/(k_B T)]
```

No position appears in this Hamiltonian. Its partition function and graph-indexed correlations are exactly independent of s. Fixed-probability bond or site percolation has the same invariance on corresponding graph supercells. This is a conditional identity built into the model. Its value is that it exposes an assumption before an expensive calculation.

The complete fcc contact graph adds twenty-one undirected edges per six-site cell. Its difference already appears far above any critical temperature. Let K = J/(k_B T). For an infinite simple graph, the high-temperature expansion gives log(Z)/N = log(2) + zK²/4 + tK³ + O(K⁴), where z is degree and t is the number of triangles per site, counting each triangle once.

| Exact model quantity | Original bars | Full fcc contacts |
|---|---:|---:|
| Edges per six-site cell | 15 | 36 |
| Triangles per six-site cell | 8 | 48 |
| Ground-state energy per site, in units of J | -2.5 | -6 |
| K² coefficient of log(Z)/N | 1.25 | 3 |
| K³ coefficient of log(Z)/N | 4/3 | 8 |
| K coefficient of normalized susceptibility | 5 | 12 |

Normalized susceptibility here means N^-1 sum_ij ⟨spin_i spin_j⟩ at zero field in the high-temperature phase.

The series follows by expanding each bond weight into cosh(K)[1 + spin_i spin_j tanh(K)]. Spin sums retain even-degree edge subgraphs. Single bonds supply the K² term through log(cosh K), and triangles supply the leading connected loop term. These coefficients are calculations for the declared graph models, without a fitted critical temperature.

The strongest objection is physical: a real interaction need not remain J when the structure folds. Exchange, dipolar and elastic interactions can depend on separation, orientation, electronic structure or stress. Even fixed-length central-force springs change their vector stiffness as their directions change. Geometry alone cannot identify the Hamiltonian of actual CaB6.

There is also an observational distinction. Fixed graph correlations can give changing scattering patterns because the positions enter the measured structure factor:

```text
S(q; s) = (1/N) sum_ij <spin_i spin_j> exp[i q . (r_i(s)-r_j(s))].
```

So a changed image or scattering pattern need not mean that the spin probability distribution changed. A physical box cut from the folded material also need not contain the same graph vertices. Claims of invariance must specify graph coordinates, boundary conditions and observables.

Compare three models next: couplings only on original bars, couplings on all contacts, and a smooth distance-dependent coupling. The first supplies an exact control, the second the fcc endpoint. The third asks whether additional interactions turn on before contact. High-temperature susceptibility can distinguish them before critical-point simulation.

What would change the interpretation: a specified microscopic interaction whose fold dependence can be derived or measured. That would turn a graph comparison into a material hypothesis. No such interaction law was established here, and no physical phase transition is claimed.

**Shared wave equations: useful prediction transfer with different physical meanings.**

A particle in V(r) = -κ/r obeys the dimensionless stationary equation [-∇²/2 - 1/x]ψ = εψ after choosing a = ħ²/(mκ), x = r/a, and energy unit mκ²/ħ². This change of units gives ε_n = -1/(2n²). It explains an entire family of shapes and levels, rather than a visual resemblance between orbiting objects.

For a weakly bound scalar around a black hole, κ = GMm and α = GMm/(ħc). The hydrogenic form follows from the massive field equation at small α. Higher-order terms split the levels, while the horizon gives growing or decaying modes. The particle's existence and the cloud's astrophysical formation remain conditional. [Baumann, Chia and Porto, equations 2.3–2.13](https://arxiv.org/html/1804.03208v2).

The fractals implementation already contains the corrective information in nextOrder() and growthRate(). For the 211 level at spin 0.9, equation 2.10 gives a frequency correction relative to leading binding of -1.0625α² + 0.6α³. Its magnitude is about 1.00% at α = 0.1 and 7.94% at α = 0.3. Agreement of leading shapes alone hides this difference.

The wave-dark-matter soliton also has r proportional to ħ²/(GMm²), with ground-state half-mass coefficient 3.925. Here M belongs to the cloud, whose potential must be solved together with the wave. Shared dimensional balance does not give a hydrogenic spectrum. [Hui et al., equation 29 and Appendix B](https://arxiv.org/html/1610.08297v2).

A more surprising transfer uses entirely classical matter. Batygin derived Schrödinger-form evolution for small inclination waves in thin, nearly Keplerian disks. The complex amplitude describes inclination and nodal phase. It provides eigenmodes and tools for external perturbations, without assigning quantum measurement probabilities to stars. [Batygin, Sections 2–3](https://arxiv.org/html/1803.01258v1).

Melton and Batygin extended that construction to nonlocal gravitational coupling. A conserved inner product supports the mathematical correspondence. Their local approximation can reproduce mode shapes well while missing eigenfrequencies. This is a concrete example of a resemblance that survives one observable and fails another. [Melton and Batygin, Sections 2–4](https://arxiv.org/html/2102.02312v1).

This bridge joins gravity's disk-wave caution to fractals' distinction between a single quantum particle and a classical collective wave. A useful common rule may be linear conservative evolution. Testing a proposed mapping requires its operator, boundary conditions, conserved norm, initial states and measured quantity. The name of the differential equation supplies only part of that specification.

The next probe would compare full and local disk-coupling matrices against both shapes and frequencies as disk width changes. Published results already provide a benchmark. It becomes relevant to a new astrophysical target only if that target satisfies the thin, nearly Keplerian, small-inclination assumptions.

**Universality and flux conservation preserve different things.**

At a critical point, repeated coarse-graining can remove many microscopic details while preserving large-scale statistics. The critical temperature and amplitudes can differ between lattices even when exponents agree. Dimension, symmetry and interaction range help identify possible behavior, but frustration, disorder, long-range forces and the order of the transition still matter.

Wilson and Fisher's primary calculation already distinguishes Ising and XY exponents near four dimensions. Modern conformal-bootstrap calculations identify distinct three-dimensional Ising, O(2) and O(3) data. This makes a collection of matching exponents more informative than one coincident slope. [Wilson and Fisher](https://doi.org/10.1103/PhysRevLett.28.240), [Kos et al.](https://arxiv.org/abs/1603.04436).

The cab graph offers a new geometry on which to study familiar statistical models. A short-range ferromagnetic scalar Ising model with a conventional continuous transition would be expected to approach three-dimensional Ising behavior. That expectation needs a declared model and finite-size checks. The drawing does not establish a new universality class.

Turbulence offers a different common rule. In the appropriate homogeneous, isotropic inertial-range limit, a signed third-order velocity moment is fixed by the mean energy flux. This constraint can hold while higher moments develop changing tails. The 4/5 law requires its statistical and scale-separation assumptions. [Kolmogorov, equations 5–7](https://rainbow.ldeo.columbia.edu/~alexeyk/Papers/Kolmogorov1941b.pdf).

The repository's Sabra model has its own exact third-order flux relation, including an alternating contribution from its second invariant. Its equation 16 is a model-specific identity. Matching it checks the cascade calculation, while matching the model's intermittency exponents does not validate a real molecular cloud. [L'vov et al.](https://arxiv.org/html/chao-dyn/9803025v2).

There may be a common function even when a clean power law is absent. In high-Reynolds-number decaying wind-tunnel turbulence, Küchler and colleagues report collapse of a nontrivial scale-dependent form across Reynolds numbers. Their result is evidence about those flows, with a stronger claim than merely fitting similar slopes. [Author manuscript](https://arxiv.org/html/2106.01795v2).

For cloud edges, the measured object must also match. The dimension of one contour loop and that of a whole level set are different quantities. Kondev, Henley and Salinas relate loop geometry to roughness through a conjectured correlation exponent, with exact endpoint cases. Their general loop formula should retain that qualification. [Sections IV.2–IV.3](https://arxiv.org/html/cond-mat/9907229v1).

The useful cross-repository question is whether an independent change in resolution, forcing, correlation length or coupling produces the predicted response. The scale route's warning applies here: the existing Wolff updates sample equilibrium efficiently, but their update count is not a calibrated physical clock for a quench.

**Temporal recurrence and scale repetition can be disentangled.**

For Newtonian point masses with unchanged masses and G, x(t) generates x_λ(t) = λx(t/λ^(3/2)). Period changes as λ^(3/2), energy as λ^-1, and angular momentum as λ^(1/2). Thus T|E|^(3/2) is unchanged along a scaled family. An infinity of rescaled copies supplies one orbital shape, rather than an infinity of independent discoveries.

The three-body figure-eight provides a stronger kind of repetition: three equal masses traverse one curve with time shifts. Its existence has a variational proof. [Chenciner and Montgomery](https://arxiv.org/abs/math/0011268).

Kapela and Simó formulate choreography as a fixed point of evolution followed by particle permutation. Rotation, translation, rescaling and phase shifts must be removed before an isolated-root proof can work. They also separate existence from linear stability. This directly informs physics0's proposed orbit-certification work. [Equations 1.1–1.3 and discussion](https://ww2.ii.uj.edu.pl/~kapela/papers/nosym.pdf).

For an orbit catalogue, normalize those symmetries before counting families, then compare return maps and stability. For astr0's recurrent eclipses, phase-coherent recurrence constrains the model, but light curves can hide changes in orientation, dust or period. A future-event prediction tests that recurrence model without proving a universal structure.

**A broader lead: repetition at a preferred scale ratio.**

Efimov physics supplies experimental evidence for discrete scale repetition. In cesium, Huang et al. infer a ratio 21.0 ± 1.3 between successive triatomic resonances, compared with the ideal identical-boson value 22.7. This is evidence from recombination resonances and a finite-temperature analysis. [Primary experimental paper](https://doi.org/10.1103/PhysRevLett.112.190401).

A different mass mixture provides a stronger test of the rule. Tung et al. observe three consecutive resonances in Li–Cs, with ratio 4.9 ± 0.4 against prediction 4.88. The changed ratio is informative because the common theory predicts its dependence on the constituent masses. [Primary experimental paper](https://arxiv.org/abs/1402.5943).

Critical gravitational collapse supplies a distinct mathematical instance. For a spherical massless scalar field coupled to general relativity, Gundlach obtains an echoing period Δ = 3.4453 ± 0.0005 and one growing perturbation mode. That mode gives mass exponent γ ≈ 0.374 and a predicted periodic modulation of the mass-scaling relation. [Sections II and IV](https://arxiv.org/html/gr-qc/9604019v1).

This is numerical/theoretical evidence within a classical field model. The word “experimental” in that older paper refers to numerical collapse results. It does not report observed astrophysical echoes, and the exponent does not describe ordinary cosmological halo clustering by default.

The shared structure is a system revisiting a pattern in logarithmic scale while a small number of disturbances control departure. This creates a method-level connection to critical phenomena. The Efimov ratio and collapse echo period arise from different equations. Matching either number to galaxy structure would need an additional derivation and an independent test.

A useful next step is a comparative note on how a single growing mode selects a finite repetition range. No new gravitational-collapse solver was built here. Existing primary numerical results are sufficient to motivate that bridge without making a new physical claim.

**Files and limits.**

The reproducible probe is [graph_vs_geometry.py](../probes/repetition/graph_vs_geometry.py). Run it with Python 3. It writes [graph-results.json](../probes/repetition/graph-results.json). It uses only the standard library and makes no source-repository changes.

Repository pointers used in this route:

- [physics0 AREAS.md](https://github.com/Foundation-0/physics0/blob/76410c3deebf925f6c51017867dbcef29ff54e8b/AREAS.md#L74): statistical physics on the incentre lattice, plus celestial mechanics at line 28.
- [Continuous fcc construction](https://github.com/aska-digital/incentre-lattice/blob/abeb94b0aa5f7c59b14dab139aa380d2ce5d81e2/results/fold-continuous-fcc/PROOF.md): explicit curve, distant-image bound and prior-art boundary.
- [Gravitational atom](https://github.com/Foundation-0/fractals/blob/9669f5579635c3543f145e8eca86133069ad6f27/gravitational-atom/atom.js#L58): next-order spectrum and growth-rate corrections.
- [Critical-point study](https://github.com/Foundation-0/fractals/blob/9669f5579635c3543f145e8eca86133069ad6f27/critical/README.md): equilibrium scaling, model limits and finite-size corrections.
- [Turbulence study](https://github.com/Foundation-0/fractals/blob/9669f5579635c3543f145e8eca86133069ad6f27/turbulence/README.md): flux identities, intermittency, cutoffs and contour-definition controls.
- [Gravity claims](https://github.com/Foundation-0/gravity/blob/d8c7544e89388720fc1c13de816ddb7dd03d2096/CLAIMS.md#L25): soliton relation C-03 and disk-wave caveat C-17.
- [Astronomy hub](https://github.com/Foundation-0/astr0/blob/607a11eaa83b2ec7539e0986046c3230406d2b04/README.md): recurrent eclipses and observational checks. Its quoted project discoveries were not independently revalidated in this route.

For scale selection: compare response to an independent control, and preserve the distinction between equilibrium critical behavior and physical dynamics. Critical-collapse echoing is a separate bridge to explore.

For relations: the lattice example distinguishes unchanged interaction probabilities from changed observed scattering. The wave-equation examples distinguish the evolution generator from the meaning and accessibility of its observables.

For evidence reconnection: standardize the quantity before comparing dimensions, periods or shapes. A single contour, a whole level set and a projected intensity image require different null models.

For robustness: the graph partition-function identity is deliberately conditional. The informative result is the exact separation between the preserved five-neighbor graph and the twelve-neighbor endpoint contact graph. The high-temperature coefficients provide a test independent of a critical-point fit.

The most useful next project is the declared-interaction comparison on the existing fold. It can answer a concrete question: which observed changes come from geometry, and which require changed interactions? It has an exact control and a small analytical prediction before any costly simulation.
