# Reconnecting evidence

This report reviews the repository revisions recorded in the source ledger. It does not review later changes on main, including gravity Wave 11. Original research: gpt-forge, gpt-6-astra, requested reasoning effort ultra. Publication preparation: gpt-6.1-sol.

gpt-forge, route 5. Research model: gpt-6-astra, ultra reasoning. 12 November 2026.

A useful connection can reveal something that neither observation establishes alone. The clearest astronomical example here joins old eclipses with uneventful observations at other times: the eclipses suggest several possible periods, while a well-placed observation of normal brightness eliminates an alternative.

Another connection works through error. A reference star can help reveal a target's variation because both share an instrumental disturbance.

These are established routes to discovery that fit A's intent without requiring one theory of everything. The immediate opportunity for astr0 is to search for observations that distinguish the remaining explanations of a candidate. For physics0, atomic line networks and historical seismograms offer related opportunities, with different physical assumptions.

This pass produced reproducible synthetic calculations and source-grounded next investigations. It did not discover an astronomical object or validate a repository claim.

**The distinct possibilities**

| Connection | What becomes visible | Repository entry point | Main limit |
|---|---|---|---|
| Old events + modern coverage | Period alternatives that one archive cannot distinguish | [astr0: plate archives](https://github.com/Foundation-0/astr0/blob/607a11eaa83b2ec7539e0986046c3230406d2b04/AREAS.md#L17), [long periods](https://github.com/Foundation-0/astr0/blob/607a11eaa83b2ec7539e0986046c3230406d2b04/AREAS.md#L56) | Missing coverage is different from an informative normal-brightness measurement |
| A target + reference measurements | A signal separated from shared calibration error | [astr0: independent remeasurement](https://github.com/Foundation-0/astr0/blob/607a11eaa83b2ec7539e0986046c3230406d2b04/README.md#L44) | A reference containing target light can remove the signal |
| Historic eclipses + evolving viewing geometry | A surviving binary that stops appearing to eclipse | [astr0: lost-eclipses](https://github.com/Foundation-0/astr0/blob/607a11eaa83b2ec7539e0986046c3230406d2b04/README.md#L23) | Blending, sensitivity changes and incorrect matches can imitate disappearance |
| Rejected detections + a different scientific question | Binaries or unusual variables rejected by a planet search | [astr0: by-products](https://github.com/Foundation-0/astr0/blob/607a11eaa83b2ec7539e0986046c3230406d2b04/AREAS.md#L73) | Rejection reasons and the parent sample determine what can be inferred |
| Several atomic lines + known level differences | A proposed energy level constrained by several transitions | [physics0: atomic spectra](https://github.com/Foundation-0/physics0/blob/76410c3deebf925f6c51017867dbcef29ff54e8b/AREAS.md#L155) | Dense spectra allow accidental combinations and shared calibration errors |
| Old seismic noise + modern wave measurements | Past ocean conditions encoded in a different physical channel | [physics0: microseisms](https://github.com/Foundation-0/physics0/blob/76410c3deebf925f6c51017867dbcef29ff54e8b/README.md#L18) | The conversion depends on instrument response and wave generation/propagation |
| Weather bulletins + assimilation provenance | New observations, or an independent test of a reconstruction | [physics0: climate rescue](https://github.com/Foundation-0/physics0/blob/76410c3deebf925f6c51017867dbcef29ff54e8b/AREAS.md#L131) | Agreement is partly circular if the reconstruction already used the observation |

**1. Archives reveal alternatives, including alternatives to persistence**

For ASASSN-24fw, Zakamska and colleagues combine the modern dimming with historical events in 1937 and 1981. Their reported period is 15,999 ± 2 days. DASCH alone cannot exclude half that period because it lacks observations at the required phase.

ASAS observations cover that phase and show normal brightness. The join removes an ambiguity, while the analysis retains uncertainty about the physical occulter. [Primary paper, section III.1 and figures 5–6](https://arxiv.org/html/2507.05367v3).

The synthetic probe makes this logic explicit. Events at invented days 0 and 120 allow periods 120, 60, 40, 30, 24 and 20 days under the chosen discrete prior. An event at day −440 leaves 40 and 20 days.

No detected eclipse at day 20 favors 40 days, but only if the observation could reliably have detected one. With 95% detection completeness, the posterior probability of 40 days becomes 95.24%. With 5% completeness, it reaches only 51.28%.

Before taking that exposure, its expected information about the two aliases is 0.855 bits at 95% completeness. An equally sensitive observation at a phase where both aliases predict the same outcome contributes zero information about this ambiguity. This does not make that exposure useless for eclipse depth, calibration or another question. Information value depends on the unresolved question.

An archival search therefore has two productive directions: recover past events, and recover observations at which competing periods disagree. An upper limit on stellar flux, evidence of a dim state, must also be distinguished from an upper limit on eclipse depth, evidence that a detectable eclipse did not occur.

An instructive counterexample to a fixed-period, fixed-shape search is HS Hydrae. Davenport and colleagues combine more than 125 years of observations, including DASCH and TESS, to trace eclipses fading as the inner orbit changes inclination under a third body's influence.

A later TESS sector showed the predicted absence of eclipses. The stars and their orbit persist while the eclipsing appearance disappears. [Primary paper, sections 2–4 and final paragraph before acknowledgments](https://arxiv.org/pdf/2107.10954).

That case connects the relations and persistence routes to observable astronomy. The same object across epochs need not have the same appearance. A search that insists on identical eclipse depths could discard the very evolution it seeks.

**2. A second view can help by measuring the disturbance**

Schölkopf and colleagues developed half-sibling regression for settings where a target contains a desired signal plus an unwanted contribution, and another channel measures the unwanted contribution. Recovery up to the signal's mean requires an additive model, independence of signal and reference, and complete predictability of the disturbance.

Incomplete prediction leaves residual error. The method assumes a causal structure rather than discovering it. [Primary paper, section 2, proposition 1 and incomplete-information analysis](https://proceedings.mlr.press/v37/scholkopf15.pdf).

Our calculation uses a known Gaussian measurement model:

\[
y_i=q+b+e_i,\qquad x=b+\eta,
\]

where signal \(q\) and shared offset \(b\) have independent unit-variance Gaussian priors. Readout noises \(e_i\) and \(\eta\) are independent, with variance 0.01. All measurement equations and variances are assumed known.

| Data available | Posterior variance of the signal |
|---|---:|
| One target measurement | 0.502488 |
| One hundred exact copies of that measurement | 0.502488 |
| One hundred fresh target readouts sharing the same offset | 0.500025 |
| One hundred measurements with independent offsets | 0.009999 |
| One target measurement plus one reference measuring its offset | 0.019513 |

The reference alone has zero information about the signal because they are independent. Conditional on the target measurement, it supplies 2.343 bits. The posterior variance falls by a factor of 25.75, equivalent to a factor of 5.07 in posterior standard deviation. A seeded simulation of 100,000 draws agrees with the analytical calculation.

If the shared offset in the 100-readout case is falsely treated as 100 independent errors, nominal 95% intervals cover the true signal only 15.69% of the time, averaged over this model's signal and offset priors. This number describes the constructed example. It is not an estimated failure rate for DASCH or TESS.

There is a corresponding failure case. Replace the reference with \(x=\alpha q+b+\eta\). If \(\alpha=1\), it is another noisy copy of the mixture. Correctly modeling it barely resolves the ambiguity. Blindly regressing it out leaves only about 0.5% of the target's signal response in the residual. Signal injection and recovery are therefore essential when a comparison source could contain blended target light.

DASCH already performs several calibrations. Its official guide identifies source splitting, blending and time-clustered low-resolution series as real problems. A new correction must demonstrate improvement beyond those existing reductions. [DASCH reduction guide](https://dasch.cfa.harvard.edu/dr7/reduce-lightcurve/).

Reference-star, local-calibration and quality metadata provide a starting point for choosing and auditing controls. They can also identify calibration information shared between measurements. [Photometric calibration metadata](https://dasch.cfa.harvard.edu/dr7/photcal-asdf-contents/).

The practical question is narrower than whether two pipelines agree: which parts of their error are independent? Two programs measuring the same damaged plate can agree about the same defect. A separate plate can add different evidence, while a nearby constant star on the original plate can help diagnose its calibration.

**3. What the Rosetta Stone theorem establishes**

Gresele and colleagues prove conditional identifiability results for matched views of common independent latent components. Their model requires smooth invertible mixing functions, component-wise corruption, independent noise components and independence between source and noise.

A technical derivative-rank condition supplies sufficiently distinct views. The contrastive-learning results use an infinite-data limit and universal approximation capacity.

With one noiseless view, components can be recovered up to component-wise invertible transformations and permutation. With two noisy views, the general result recovers corrupted components, not exact noiseless samples.

The infinitely-many-view result adds assumptions, including additive corruption and a residual-dependence restriction stronger than observable independence. [Main paper, sections 3.1–3.3, theorems 1, 5 and 8](https://proceedings.mlr.press/v115/gresele20a/gresele20a.pdf).

The supplement gives Gaussian conditional corruption as a failure of the diversity condition in the multicomponent setting and shows why deterministically related views undermine this contrastive construction. [Supplement, appendices B–C](https://proceedings.mlr.press/v115/gresele20a/gresele20a-supp.pdf).

This supports a limited proposition: combining suitable observations can remove ambiguities that separate analyses retain. It supplies no guarantee that arbitrary disciplines, arbitrary catalogues or correlated instruments identify physical reality.

Our Gaussian probe uses known equations and is not an implementation of this nonlinear ICA theorem. Historical epochs also need an evolution model before they can be treated as views of a common state.

**4. Atomic spectra connect by constraints, not visual resemblance**

An observed line measures an energy difference. Several lines involving an unknown level can constrain one common value. Ding and colleagues represent levels as graph nodes and transitions as edges.

Their algorithm requires at least two matching lines for a proposed level and uses line density and uncertainty to estimate the number of candidates. Their examples still permit accidental alternatives. [Primary preprint, sections 2.2–2.3, equation 5](https://arxiv.org/html/2509.16184v1).

The useful extension for physics0 is a withheld-line test. Infer a known level from a selected subset of transitions, then predict additional observed transitions that were excluded from the fit. Compare against a null that preserves local line density, wavelength uncertainty, allowed quantum numbers and the search range. A uniform random spectrum could make success look too easy.

The probe includes a four-level difference graph with energies 0, 3, 8 and 12 in arbitrary units. Four measurements give the cycle relation \(3+5+4-12=0\). Changing the last line to 12.5 breaks it. Multiplying all measurements by 1.02 preserves the relation exactly.

Closure tests line consistency but cannot detect every shared calibration error. The extra line adds a model check even though it adds no new parameter dimension.

This is a bridge between physical spectroscopy and physics0's certificate habit: preserve the proposed level, the supporting measurements and the constraints that reject alternatives. An arithmetic certificate cannot establish that a line belongs to the claimed ion or that the calibration is correct. Those remain experimental questions.

**5. Seismic noise and rescued weather records provide another physical channel**

Bromirski's 2023 study reconstructs California winter wave conditions from microseisms over 1931–2021. It combines digitized seismograms, instrument-response work and a modern relation between seismic spectra and buoy observations.

Sampling limits affect the reconstructed extremes. Some extreme-wave peaks can be underestimated. [Primary paper, section 2 and appendix A](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2023JC019722).

The physical bridge is ocean waves transferring energy into seismic motion. Its interpretation depends on wave direction, source location, seafloor coupling and propagation, so a single amplitude is not a universal storm gauge. Ardhuin and colleagues distinguish source classes and show how changing contributions can limit a storm-climate proxy. [Primary modeling paper](https://doi.org/10.1029/2011JC006952).

This makes a short common-time calibration experiment more useful than immediately digitizing decades. Select one station with recoverable instrument metadata and a documented comparison interval. Test whether a conversion learned from some modern storms predicts withheld storms with different directions. A failure locates the missing physical dependence before a historical trend is inferred.

Weather bulletins offer a complementary check. The 20CRv3 reconstruction assimilates surface-pressure observations while prescribing other boundary information. Its evaluation explicitly uses independent observations. [Slivinski et al., 2021](https://repository.library.noaa.gov/view/noaa/31016/noaa_31016_DS1.pdf).

For physics0's rescue project, agreement with 20CRv3 is stronger evidence when the particular station observations were absent from its inputs. An assimilation-provenance check is needed before calling that comparison independent.

**6. Rejected signals become useful when the question changes**

A false positive for a planetary transit can be a real eclipsing binary. The rejection label encodes the original question, not a universal judgment about the observation. astr0 already proposes recovering these by-products. A useful first pass would inspect the rejection taxonomy and a small stratified sample, retaining the original detection statistic, rejection reason, parent sample and measurements.

The first output should be an interpretable sample with known selection, rather than an occurrence rate for the underlying sky. Population inference needs the probability of entering the sample, including its normalization. [Mandel, Farr and Gair, sections 2–4](https://arxiv.org/pdf/1809.02063). A second pipeline reusing the same candidates and measurements is not an independent discovery sample.

Joining archives also requires establishing which observations belong to the same source. Probabilistic cross-identification can incorporate positional uncertainties and physical properties. [Budavári and Szalay](https://arxiv.org/abs/0707.1611).

Proper motion matters when matching widely separated epochs. This uncertainty belongs in the evidence, especially for purported vanished or newly appeared objects. [Kerekes et al.](https://arxiv.org/abs/1006.2096).

**Small investigations worth doing next**

| Investigation | Concrete first deliverable | Strongest objection or counterexample | What would make it worth extending |
|---|---|---|---|
| Rank existing exposures by period discrimination | For one published benchmark, a table of surviving periods and exposures whose predictions differ, with completeness estimates | Eclipse shapes or timing may evolve, invalidating a fixed template | Recovery of the published alias exclusion, followed by a genuinely withheld epoch |
| Audit comparison sources for one plate candidate | One event and control set, spanning plate series, with injected dimmings and leave-one-series-out checks | Common calibration or target leakage can survive agreement between pipelines | Retained injection depths and a candidate surviving a different plate or measurement channel |
| Reproduce HS Hya as a lost-eclipse benchmark | A compact epoch-by-epoch depth and sensitivity record, including the known disappearance | Passband, dilution or ephemeris drift can mimic changing depth | Known evolution is recovered without labeling quiet epochs as missing data |
| Test one atomic level with withheld lines | Recovered known level, held-out predictions, structured null distribution and common-scale perturbation | Chance matches, ion contamination and theory-guided selection | Predictions beat the null and survive a calibration or exposure change |
| Calibrate one seismic archive segment | A short overlap comparison with station response and buoy information | The transfer relation may change with wave direction or station history | Successful prediction across withheld source conditions |

No new pipeline has been run on the repository candidates. In particular, the ASASSN-21co historical dates, RS Oph flag and TESS candidate count in the hub remain repository reports. Rowan and colleagues' published ASASSN-21co study supports the earlier 11.9-year interpretation from modern data, not independent confirmation of Foundation0's later plate claims. [Published study](https://arxiv.org/abs/2107.00662).

**Questions and handoffs**

- Relations and persistence: HS Hya separates survival of the system from survival of its observational appearance. The quantum environment-record and lattice-geometry results are useful comparisons, with distinct mechanisms.
- Robustness: test whether each purported second source adds an independent error channel, a new constraint, a new epoch, or simply a repeated measurement. Redundant constraints can still expose model failure.
- Scale selection: a long time baseline changes which frequencies and evolutionary rates are identifiable. Survey cadence and coverage create observational scales that should be separated from physical scales.
- Atomic spectra: which held-out lines would discriminate a proposed level from its nearest competing assignment, rather than merely add more easy matches?
- Archives: can exposure-level expected information guide retrieval while preserving an untouched confirmation set? Selecting the most discriminating evidence is useful, but selecting only favorable outcomes would distort the result.

[Reproducible probe and assumptions](../probes/evidence/README.md), [numeric results](../probes/evidence/results.json), and [source ledger](evidence-sources.json).
