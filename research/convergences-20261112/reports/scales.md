# What makes a scale special?

This report reviews the repository revisions recorded in the source ledger. It does not review later changes on main, including gravity Wave 11. Original research: gpt-forge, gpt-6-astra, requested reasoning effort ultra. Publication preparation: gpt-6.1-sol.

Several of these subjects meet at a useful question: **what stops a process from keeping up?** Wave spreading competes with loss of coherence through environmental interaction. Eddies break up until viscosity acts faster. A cooling gas changes phase before correlations can reach across it. Gravity builds structure until pressure, cooling or the available time changes what can form.

The promising connection is a way to make predictions. Change one independently measured rate, then predict how the boundary moves. Matching a length, speed or exponent at one setting is a weaker test. This report finds one established bridge worth extending, Kibble–Zurek dynamics, and several places where the repositories can distinguish a physical boundary from a chosen definition.

The small calculations reproduce the gravity repository's 185.59 km/s collapse estimate. They also show why its four nearby speeds do not yet establish a common origin. The cooling calculation selects a gas density, and one of the four quantities is a circular speed while the others include one-dimensional dispersions.

Research pass: gpt-forge, requested model gpt-6-astra, ultra reasoning, 12 November 2026. This is exploratory synthesis, not a new physical theory or an observational discovery. Existing repositories were read-only. The source ledger records support and limits for each external claim.

## The route map

There are at least four ways for a scale to become special: two physical effects balance, a system remembers its history, an observation crosses a chosen threshold, or an approximation stops applying. More than one can operate in the same example.

| Repository thread | What selects the scale? | Useful distinction or next question |
|---|---|---|
| [Critical lattice](https://github.com/Foundation-0/fractals/blob/9669f5579635c3543f145e8eca86133069ad6f27/critical/README.md#L23) | Lattice spacing below, correlation length or box size above. Temperature and field control the correlation length. | Finite driving rate introduces another upper limit even if the temperature reaches the critical value. |
| [Ordinary-fluid turbulence](https://github.com/Foundation-0/fractals/blob/9669f5579635c3543f145e8eca86133069ad6f27/turbulence/README.md#L11) | Injection at large scales and dissipation at small scales. | Constant flux, approximate power laws and intermittent bursts are different claims. |
| [Molecular-cloud turbulence](https://github.com/Foundation-0/fractals/blob/9669f5579635c3543f145e8eca86133069ad6f27/turbulence/README.md#L195) | Velocity fluctuations cross the sound speed. | This changes the cascade. It need not end the cascade or define one universal filament width. |
| [Witness Map](https://github.com/Foundation-0/fractals/blob/9669f5579635c3543f145e8eca86133069ad6f27/witness-map/model.js#L109) | Wave-spreading time compared with a separation-dependent decoherence time. | A fixed-flight-time interference experiment asks a different question and has a different threshold. |
| [Quantum paths](https://github.com/Foundation-0/fractals/blob/9669f5579635c3543f145e8eca86133069ad6f27/quantum-paths/README.md#L11) | Momentum, preparation and the timing and resolution of measurements. | The reduced Compton length marks a validity limit for this single-particle construction, not a demonstrated return to smooth physical trajectories. |
| [Gravitational atom](https://github.com/Foundation-0/fractals/blob/9669f5579635c3543f145e8eca86133069ad6f27/gravitational-atom/atom.js#L1) | Particle mass, black-hole mass, spin and dimensionless coupling. | Equal equations predict equal rescaled shapes within an approximation. Formation and survival still require time. |
| [Galaxy and group transitions](https://github.com/Foundation-0/gravity/blob/d8c7544e89388720fc1c13de816ddb7dd03d2096/CLAIMS.md#L119) | Acceleration, external field, density, velocity dispersion, thermal history and model assumptions. | A transition in acceleration is not one universal radius. A fitted onset is not automatically a phase boundary. |
| [Cosmic clustering](https://github.com/Foundation-0/fractals/blob/9669f5579635c3543f145e8eca86133069ad6f27/README.md#L25) | Growth from initial conditions, cosmological epochs and the statistic used to describe clustering. | Nonlinear mass, sound horizon and homogeneity threshold are distinct scales. |
| [Incentre-lattice statistical physics](https://github.com/Foundation-0/physics0/blob/76410c3deebf925f6c51017867dbcef29ff54e8b/AREAS.md#L74) | Connectivity, interaction strengths, dimension and sample size. | A geometric length alone does not determine the critical temperature. The interaction graph must be specified. |
| [Long-period events in archives](https://github.com/Foundation-0/astr0/blob/607a11eaa83b2ec7539e0986046c3230406d2b04/AREAS.md#L19) | Physical periods meet cadence, baseline, passband and detection thresholds. | Joining epochs can change the accessible scale without changing the source. Test recovery by injecting events through the actual window function. |

## A real bridge: a changing system selects its own correlation length

An equilibrium critical point can have correlations over arbitrarily large distances in the ideal infinite system. Reaching that state takes time. Near the transition, the time needed to adjust grows along with the correlation length. A finite-rate change therefore leaves finite domains.

Write the fractional distance from the transition as ε. With correlation length ξ = ξ₀|ε|⁻ν and relaxation time τ = τ₀|ε|⁻νz, a linear passage ε = t/τQ stops being approximately adiabatic when τ is comparable to |ε/ε̇|. This gives the Kibble–Zurek scale:

```
ξ_hat = ξ0 (τQ/τ0)^[ν/(1 + ν z)]
```

Here z is a dynamic critical exponent, not cosmological redshift. The slow-driving limit also meets the finite size of the sample. Exact prefactors and later domain growth depend on the system and protocol.

This connection has experimental content. Navon and colleagues measured coherence lengths after cooling a homogeneous Bose gas through its transition. Their exponent was 0.35 ± 0.04, consistent with the roughly 1/3 prediction and distinguishable from a mean-field 1/4. See equations 1–2 and figure 4 in [their experiment](https://arxiv.org/pdf/1410.8487).

The historical bridge to cosmology is explicit in [Zurek's 1985 proposal](https://doi.org/10.1038/317505a0): laboratory vortices can test elements of defect formation during symmetry breaking. Such a laboratory test does not establish that a specified cosmic transition occurred or that cosmic strings exist.

For the repositories, this supplies a concrete extension to static bounded fractals: the upper limit can depend on the rate of change, even at the critical temperature. The probe uses ν = 0.6717 and z = 1.5 as representative assumptions. Slowing the quench by 100 predicts a 4.67-fold longer characteristic length within the scaling regime. This is a calculation, not a simulated or measured result from this expedition.

**Strongest objection:** a shared comparison of times is too general to imply the same universality class. [Wilson's renormalization-group result](https://doi.org/10.1103/PhysRevB.4.3174) explains why some equilibrium systems lose microscopic detail under rescaling. It does not put turbulence, decoherence and galaxy formation in the Ising universality class.

**Discriminating probe:** specify a dynamic model, vary the cooling rate and sample size independently, then test the predicted crossover and scaling collapse.

The reviewed [Ising code](https://github.com/Foundation-0/fractals/blob/9669f5579635c3543f145e8eca86133069ad6f27/critical/model.js#L6) uses Wolff cluster flips to sample equilibrium efficiently. Those update counts are not physical time. A quench study needs stated dynamics, such as local stochastic spin flips, with its own dynamic exponent.

**What would change the assessment:** consistent cutoff motion and correlation-function collapse under the independently varied rate would make the extension substantive. A good-looking power law obtained by relabelling Wolff steps as seconds would not.

## Similar boundaries can answer different questions

In the small-separation limit, write the decoherence rate as Γ(Δx) = ΛΔx². The Witness Map uses t_wave = mΔx²/ℏ, so its W = 1 condition gives:

```
Δx_W = [ℏ/(mΛ)]^(1/4)
```

A simple interference experiment with fixed separation and fixed observation time instead has visibility V/V₀ = exp[−ΛΔx²t_obs]. Its e-fold threshold is:

```
Δx_visibility = [1/(Λ t_obs)]^(1/2)
```

If gas density rises by 100 at fixed temperature and scattering physics, Λ rises by 100. The first length shrinks to 0.316 of its old value. The second shrinks to 0.100. There is no contradiction: spreading before decoherence and surviving a specified flight time are different operational questions.

[Hornberger and colleagues](https://arxiv.org/pdf/quant-ph/0303093), equation 5 and figures 2–3, measured the suppression of fullerene interference with gas pressure. Their observed regime involved essentially complete localization per collision. That experiment supports pressure-dependent decoherence, not the two small-separation length exponents calculated here.

The small-separation calculation fails once an individual collision already resolves the paths. The rate then approaches a scattering rate instead of continuing as Δx². Real interferometers also have changing path separation, finite acceptance and other decoherence channels. Integrating Γ[Δx(t)] along the actual path is the useful next probe.

Even successful decoherence does not establish that many independent observers can read the result. [Riedel and Zurek](https://arxiv.org/html/1001.3419v2), equations 17–18, give an idealized isotropic-illumination counterexample. The relations route examines this distinction further. A rate for suppressing interference cannot substitute for accessible records.

The path-fractal thread offers a related warning. [Abbott and Wise](https://www.slac.stanford.edu/pubs/slacpubs/2250/slac-pub-2427.pdf) derive dimension two for an observed quantum path in a specified nonrelativistic measurement construction.

The repository explores what changes when records accumulate momentum kicks. It should retain that protocol label. Its Compton-scale interpolation is not an experimental finding about trajectories in quantum field theory.

There is an instructive reversal in ordinary Brownian motion. Inertia gives smooth motion over sufficiently short times, while random kicks produce diffusion over longer times. [Li and colleagues](https://doi.org/10.1126/science.1189403) observed the short-time ballistic regime. Equal roughness exponents can therefore sit on opposite sides of a crossover and come from different mechanisms.

## Turbulence: a crossover may change the rule without ending repetition

For an ordinary incompressible fluid, the Kolmogorov estimate compares eddy turnover with viscous diffusion. It gives η = (ν³/ε)¹⁄⁴, where ν is kinematic viscosity and ε is energy dissipation per unit mass. Increasing viscosity by 100 at fixed ε makes η 31.62 times larger. See [Kolmogorov's original scaling construction](https://www.ams.jhu.edu/~eyink/Turbulence/classics/Kolmogorov41a.pdf).

Compressible interstellar turbulence has another boundary. At the sonic scale, typical velocity fluctuations fall below the sound speed. [Federrath and colleagues](https://arxiv.org/html/2011.06238), equation 1, find ℓs/L = φs M^(−1/p), with a supersonic exponent near 0.49 and a subsonic exponent near 0.39 in their simulation. The transition spans a factor of about three in scale.

This is a change between scaling regimes, rather than the disappearance of all turbulent structure. Their coefficient also changes according to whether L means driving scale or cloud diameter. Thus a statement like “0.1 pc is special” needs the Mach number, sound speed, definition of L and cloud selection.

**Probe:** compare ℓs/L against independently measured Mach number across environments, retaining resolution and tracer differences. With p = 1/2, a tenfold Mach-number increase predicts a hundredfold smaller ℓs/L.

A fixed physical width under such changes would challenge that simple sonic explanation. Magnetic effects, gravity and sample selection need separate models.

## A cosmic boundary can partly belong to its definition

Scrimgeour and colleagues define a homogeneity scale by where the counts-in-spheres dimension D₂ approaches 3 within a chosen tolerance. With a 1% criterion they obtain roughly 70–81 h⁻¹ Mpc across their redshift bins. The criterion and tracer dependence are explicit in [sections 3.6 and 7 of the paper](https://arxiv.org/pdf/1205.6812).

This supports the end of an indefinitely fractal galaxy distribution. It does not establish a sharp universal wall at one radius. The repository's “80 to 300” wording also spans the tested exclusion range, rather than one measured transition radius.

A small analytic example makes the distinction visible. Assume the deliberately simple correlation function ξ(r) = b²(r₀/r)^γ, with γ = 1.8 and tracer bias b. Integrating it gives N(<r) proportional to r³[1 + x], where x = 3b²(r₀/r)^γ/(3−γ), and D₂ = 3−γx/(1+x).

| Required fractional distance from D₂ = 3 | Threshold radius, in units of r₀ |
|---|---:|
| 10% | 4.07 |
| 1% | 16.03 |
| 0.1% | 58.09 |

The underlying smooth model is unchanged. A different reporting threshold moves its quoted scale. This toy is not fitted to WiggleZ and omits the acoustic feature and realistic large-scale correlation shape.

Cosmic history supplies physical scales as well. Acoustic propagation and the radiation-to-matter transition imprint features in the transfer function, as developed by [Eisenstein and Hu](https://arxiv.org/abs/astro-ph/9709112).

Later nonlinear growth selects a characteristic mass through D(z)σ(M*) = δc, within the [Press–Schechter framework](https://adsabs.harvard.edu/pdf/1974ApJ...187..425P). These are distinct from a tolerance-defined homogeneity radius.

**Probe:** retain the full D₂(r) curve and covariance, then report several fixed thresholds and tracer selections. A theoretical common scale should predict these curves and their changes. Comparing only one quoted radius throws away the information that distinguishes physical evolution from a change in convention.

## The galaxy-speed coincidence survives as a question, not yet a common scale

The gravity repository compares a fitted group onset of 180–190 km/s, a collapse-based one-dimensional dispersion of 185.59 km/s, an L* circular speed of 175.82 km/s and a free-free cooling speed of 178.42 km/s. The [exact implementation](https://github.com/Foundation-0/gravity/blob/d8c7544e89388720fc1c13de816ddb7dd03d2096/wave10_covariant_jeans_unification.py#L264) states the choices that generate these numbers.

The probe reproduces 185.5881 km/s by solving the existing approximate spectrum for σ(R*) = 1.686, converting the resulting mass to a radius enclosing 200 times critical density, then taking V200/√2. Reproduction confirms the numerical calculation under these conventions. It does not derive a physical dispersion floor for a new dark field.

Three issues matter before treating the four numbers as independent evidence.

1. **The velocities differ in meaning.** The same isothermal conversion applied to the L* circular speed gives 124.32 km/s, rather than 175.82. This does not prove that conversion is correct for a real disk. It shows that common units alone do not make the observables commensurate. Galaxy Vflat, halo V200 and group line-of-sight dispersion need an explicit dynamical mapping.
2. **The cooling estimate selects a physical density.** It adopts electron density from cosmic baryon fraction times Δ = 1000 times today's critical density, and an available time H₀⁻¹. In that free-free formula, the selected speed scales linearly with both Δ and available time. These are physical assumptions, not universal constants.
3. **A population scale is being assigned to local field dynamics.** Press–Schechter M* describes a characteristic collapse mass. Its identification with a spatially widespread dark-fluid velocity floor requires a mechanism that distributes energy, equilibrates it and predicts scatter with environment and assembly history.

| Local gas overdensity Δ, in the same cooling formula | Selected speed |
|---|---:|
| 200 | 35.68 km/s |
| 500 | 89.21 km/s |
| 1000 | 178.42 km/s |
| 2500 | 446.05 km/s |

These are sensitivity calculations, not allowed error bars on one observed object. Changing Δ changes the gas environment. At low temperatures, free-free-only cooling itself becomes a poor approximation. A shorter available time changes the question from “cools within a Hubble time” to another physical criterion.

The script also varies the halo overdensity used to assign a velocity at fixed M*. It returns 165.34, 185.59 and 216.21 km/s for Δ = 100, 200 and 500. This comparison exposes convention dependence. It is not a conversion among apertures of the same realistic halo, which requires a mass profile.

As a further stress test, multiplying the spectrum's σ₈ amplitude by 0.95 or 1.05 gives 166.81 or 204.89 km/s. Those changes are illustrative, not a posterior uncertainty interval. The external cosmology is informative, but a computation using external inputs is different from a parameter-free explanation of why a local transition occurs.

[Rees and Ostriker](https://doi.org/10.1093/mnras/179.4.541) compare cooling and collapse to explain characteristic galactic masses and radii. [Voit and colleagues](https://arxiv.org/pdf/1505.03592) model how cooling and feedback can hold gas near marginal precipitation. These motivate tests of density, metallicity and assembly history alongside velocity.

For comparison, [Milgrom's proposal](https://doi.org/10.1086/161130) selects an acceleration, with characteristic radius rM = √(GM/a₀), rather than one galaxy size. The [SPARC acceleration relation](https://arxiv.org/pdf/1609.05917), equation 4, is an empirical regularity with assumptions about stellar mass. Neither a useful fit nor a nearby cosmological acceleration by itself specifies the microscopic cause.

**What would strengthen the gravity lead:** derive the velocity conversion, density and energy-transport law before fitting the target systems. Predict the transition's scatter and its response to redshift, environment and cooling physics. A match after those choices are fixed would be much more informative than the four original speeds.

## A promising branch for the persistence and unclaimed routes

The gravity notebook argues that a dark condensate without electromagnetic cooling retains shock energy. The absence of photons alone cannot establish that conclusion. [Seidel and Suen](https://arxiv.org/abs/gr-qc/9309015) demonstrate gravitational cooling in a scalar-field model, where outgoing scalar field carries away excess energy.

This counters the general premise. It is not a direct calculation for the repository's proposed AeST dynamics.

[Levkov, Panin and Tkachev](https://arxiv.org/pdf/1804.05857), equations 1 and 4, show that gravitational condensation in a highly occupied bosonic system has its own relaxation time and a restricted kinetic regime. Whether that time is shorter than a halo's lifetime can select where condensed objects appear.

[Semikoz and Tkachev](https://doi.org/10.1103/PhysRevD.55.489) study self-similar kinetic condensation. A [2025 preprint by Dmitriev and colleagues](https://arxiv.org/html/2509.02694v1) develops evolving self-similar distributions for gravitationally interacting bosons, with cutoffs and source-dependent scaling. Its equations 1–2 rescale energy and time. Its D is not a spatial fractal dimension.

That preprint neglects mean spatial inhomogeneity and uses an approximate kinetic collision integral. It is a lead for comparing controlled equations, not evidence that galaxies have the same cascade as a laboratory fluid. The next question is whether the proposed dark field permits comparable energy export, and on what time and length scales. The persistence and unclaimed routes can take that deeper branch.

## Reproducible work and preserved questions

Run the standard-library probe from any directory:

```sh
python3 ../probes/scales/scale_probes.py
```

[The script](../probes/scales/scale_probes.py) writes [results.json](../probes/scales/results.json).

The script checks baseline reproduction and substitutes the toy homogeneity thresholds back into their defining equation. The collapse calculation reuses the repository's Eisenstein–Hu approximation. It is not an independent Boltzmann-code calculation or a refit of the astronomical catalogues.

The source snapshots were gravity `d8c7544e89388720fc1c13de816ddb7dd03d2096`, fractals `9669f5579635c3543f145e8eca86133069ad6f27`, physics0 `76410c3deebf925f6c51017867dbcef29ff54e8b` and astr0 `607a11eaa83b2ec7539e0986046c3230406d2b04`. The first two include unpublished exploratory claims. No public-site status or observational result was inferred from their tests.

The questions worth carrying forward are concrete:

- Which cutoff moves under an independent perturbation, and which only moves when its definition changes?
- Can the static critical-lattice study be extended to finite-rate dynamics with a stated physical clock?
- Can the Witness Map display separate spreading, interference-survival and accessible-record questions?
- Do claimed galaxy-group transitions correlate more tightly with acceleration, potential depth, cooling time or assembly history after selections are matched?
- Can a proposed dark-field action produce the needed local energy transport without contradicting its early-universe behavior?
- Which features survive changing instruments and cadence, as opposed to changing the physical system?

The recommended next step is a comparison of cutoff responses, with independently specified controls and observables. Kibble–Zurek dynamics supplies a well-tested example. The galaxy-speed and quantum-threshold probes identify where the same discipline would materially improve the present repository questions.
