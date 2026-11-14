# Can acceleration evolution be separated from calibration?

**Pursue a calibrated test using individual galaxies. Park a new fit to published redshift bins. Reject the
claim that these bins, by themselves, identify a cosmological law of gravity.** The useful question is whether
a change in the radial acceleration relation remains after independently constraining changes in baryonic
mass, kinematics and selection. This note derives what that test can identify and supplies reproducible
counterexamples. No new observational fit has been performed.

The calculation applies to the empirical radial acceleration relation (RAR), which compares acceleration
inferred from rotation to that predicted from visible matter. It does not assume that the relation has a
unique explanation. A changing relation between baryons and dark matter can also change its fitted
acceleration scale. The original RAR paper explicitly distinguishes its fitting function from a theory of
gravity. [McGaugh, Lelli and Schombert, 2016](https://arxiv.org/html/1609.05917v1)

## The unresolved empirical distinction

MUSE-DARK III studies 79 galaxies at 0.33 < z < 1.44, mainly at low acceleration. Both acceleration axes come
from a dynamical reconstruction. Its authors compare alternative halo and MOND models and check stellar masses
against photometric estimates. They discuss gas uncertainties and the mass shifts needed to remove the trend.
These checks deserve weight. An abstract degeneracy does not establish that the required drift exists in their
observations. [MUSE-DARK III, sections 2–3 and appendices B–E](https://arxiv.org/html/2604.22613v1)

The broad research question and the need to handle calibration are established. Tully–Fisher evolution was
used to compare Hubble and dark-energy scalings in 2008. Alcock already compares constant, Hubble and
matter-density laws using the MUSE bins, with explicit qualifications about confidence conventions and
correlated calibration. Repeating that comparison would add little. [Limbach, Psaltis and Özel,
2008](https://arxiv.org/abs/0809.2790), [Alcock, 2026](https://arxiv.org/pdf/2609.38796)

Joint inference of galaxy distance, inclination and mass-to-light ratios is also prior work. Desmond shows why
treating shared galaxy parameters as independent errors at each radius changes the inference. The contribution
here is a compact identifiability audit, with testable calibration requirements and stopping rules. No
priority claim is made for the underlying mathematics. [Desmond, 2023](https://arxiv.org/html/2303.11314v2)

## An explicit observation model

Let g be the nominal baryonic acceleration. Define

\[
f(g,a)=\frac{g}{1-\exp[-\sqrt{g/a}]},\qquad
a(z)=A E(z)^q,\qquad b(z)=B E(z)^s,
\]

where E(z) = H(z)/H(0). The true baryonic acceleration is **b g**: b is actual divided by nominal at fixed
geometry. Thus b > 1 means the nominal mass budget is too small. A convention using nominal divided by actual
reverses the sign of s. In the first calculation the measured total acceleration is f(b g,a).

For numerical examples only, E(z) = [0.315(1+z)^3 + 0.685]^(1/2). This matches the previous project study's
chosen background. Radiation is neglected over the tested interval. The reference acceleration 1.2 × 10^-10 m
s^-2 sets units. The fit amplitude A is free. The assumed cosmology is not an observational result from this
probe.

With x = sqrt(b g/a), differentiation gives

\[
t=\frac{\partial\ln f}{\partial\ln a}
 =\frac{x}{2(e^x-1)},\qquad
\frac{\partial\ln f}{\partial\ln b}=1-t.
\]

For parameters (ln A, ln B, q, s), one row of the Jacobian, the matrix of sensitivities, is

\[
\big(t,\;1-t,\;t\ln E,\;(1-t)\ln E\big).
\]

In the exact low-acceleration limit t = 1/2 and

\[
g_{\rm true}^2 = AB\,g E^{q+s}.
\]

Only the product AB and the sum q+s can be identified. The change q → q+δ, s → s−δ leaves these predictions
unchanged. At finite acceleration this is an approximation, not an exact symmetry of the full fitting
function. Small departures from the limit can technically restore rank while leaving the fit too weak to be
useful.

On the high-acceleration branch t tends to zero. There the response measures b with little dependence on a.
Data spanning both branches and multiple redshifts can separate q and s **if total-acceleration calibration is
controlled**. A high-acceleration sample alone loses sensitivity to a. A local sample alone loses sensitivity
to evolution. Broad ranges listed separately are insufficient if their joint coverage leaves x nearly constant
or prevents comparison across redshifts.

## A stronger ambiguity survives the full curve

Allow a measured-to-true acceleration factor k(z) = C E(z)^u:

\[
g_{\rm measured}=k(z) f\big(b(z)g,a(z)\big).
\]

The fitting function is homogeneous: f(λg,λa) = λ f(g,a). Therefore the transformation

\[
(q,s,u)\longrightarrow(q+\delta,s+\delta,u-\delta)
\]

leaves every predicted acceleration unchanged, including points on the Newtonian branch. There is a separate
amplitude symmetry (A,B,C) → (λA,λB,C/λ). In this model the full curve measures combinations such as A/B, BC,
q−s and s+u, rather than all six parameters independently. This homogeneity holds for any relation g ν(g/a),
including other choices of interpolation function.

A direct counterexample uses the same A, B = 1 and C = 1 at redshift zero. Physical Hubble tracking (q,s,u) =
(1,0,0) predicts exactly the same measured curve as (0,−1,1). In the latter, the physical acceleration scale
is constant, b = E^-1 and k = E. This is a deliberately unconstrained calibration alternative. It does not
show that actual data permit those drifts.

A perfect local normalization anchor does not distinguish these cases because E(0) = 1. Even fixing all three
amplitudes leaves only two independent exponent combinations. An independent constraint on either s or u can
remove the remaining exponent symmetry when the full curve has useful acceleration coverage. In the exact deep
limit only q+s+2u is measured, so both nuisance contributions must be constrained, or their combined effect
bounded.

## Reproducible controls

[probe.py](probe.py) generates all observations synthetically. It reads no catalogue and uses no reported MUSE
uncertainties. The broad and narrow designs each contain 128 artificial independent rows at 16 redshifts, with
eight acceleration values at each redshift. A 0.05 dex error is assigned solely to compare the information
carried by different designs. A dex is a base-10 logarithmic unit. The table is a design calculation, not a
forecast for 128 observations or for 79 galaxies.

| Controlled case | Computed result | Meaning |
| --- | --- | --- |
| Exact deep limit, free A/B/q/s | Rank 2 of 4 | Only normalization product and slope sum are measured |
| Finite deep range g/A_ref = 10^-6 to 10^-4, k fixed | Rank 4, toy standard error on q = 34.34 | Mathematical rank alone is a poor feasibility criterion |
| Broad range 10^-4 to 10^2, k fixed | Rank 4, toy standard error on q = 0.185 | Shape variation can separate mass drift from evolution under controlled k |
| Same broad range, free A/B/C/q/s/u | Rank 4 of 6 | Two exact symmetries remain |
| Add z = 0 rows to the six-parameter case | Rank remains 4 | A local anchor leaves the exponent symmetry intact |
| Fix amplitudes, leave q/s/u free | Rank 2 of 3 | Perfect normalization does not calibrate evolution |
| Fix amplitudes and k, leave q/s free | Rank 2 of 2 | A positive control restores identifiability |
| Hold g_true/a fixed across redshift | Rank 2 of 4 | This selection of support removes the shape information |

The numerical rank threshold is 10^-10 relative to the largest singular value. The analytic null vectors
establish the exact deficiencies independently of that threshold. Finite differences agree with the analytic
derivatives to the recorded tolerance. Full details and parameter order appear in
[results.json](results.json).

A noiseless injection with q = 0 and s = 1, fitted while wrongly fixing s = 0, returns q = 1 in the exact deep
limit. The finite deep sample returns q = 1.0043 with a maximum residual of 0.00109 dex. Predictions from that
wrong fit miss held-out high-acceleration points by as much as 0.360 dex. Fitting q and s together on the
broad sample with k known recovers the injected values. The exact mass-plus-kinematics counterexample remains
indistinguishable across the full curve to numerical precision.

Negative controls recover zero evolution from a constant parent relation. A constant mass offset changes only
the fitted amplitude in the exact deep limit. This confirms the distinction between a common normalization
error and a calibration drift. The 26 assertions also test the local anchor, analytic symmetries, recovery of
an injected physical trend and the connection to the baryonic Tully–Fisher relation.

## Selection and covariance can create false precision

Selection on a predictor such as g, with an otherwise correct conditional model and no relevant measurement
error, need not create a spurious redshift trend. Selection that depends on noisy kinematics or on unmodelled
properties can do so. The probe constructs a deliberate counterexample: a non-evolving parent has Gaussian
scatter of 0.10 dex in measured log acceleration. A changing lower detection threshold shifts the retained
mean by exactly the amount corresponding to apparent q = 1. Retained fractions fall from 97.7% to 17.5% across
z = 0.33–1.44. This is an existence proof, not the actual survey selection function.

The appropriate selected-data likelihood includes its normalization:

\[
p(d\mid\theta,S=1)
=\frac{p(d\mid\theta)\,P(S=1\mid d,\theta)}
 {\int p(d'\mid\theta)P(S=1\mid d',\theta)\,\mathrm{d}d'}.
\]

Conditioning on measured covariates or latent galaxy properties must be specified consistently in both
numerator and denominator. A simulation that starts after selection cannot establish that the original
selection is harmless. Recovery tests must pass through the measured quantities and the selection procedure.

Radial points from one galaxy share inclination, distance and mass parameters. As a simple covariance check,
eight radial points with independent scatter 0.05 dex and a shared 0.10 dex shift have a mean error of 0.1016
dex. Treating their marginal errors as independent gives 0.0395 dex, understating the uncertainty by a factor
of 2.57. Actual observations require their own covariance or joint posterior draws. These illustrative numbers
cannot repair missing survey covariance.

## How accurate must calibration be?

In the deep limit, a fit that sets b = k = 1 measures

\[
a_{\rm apparent}=k^2 b a,
\qquad q_{\rm apparent}=q+s+2u.
\]

For a redshift pair, let L = log10[E(z_high)/E(z_low)]. Then

\[
q=\frac{\Delta\log_{10}a_{\rm apparent}
-\Delta\log_{10}b-2\Delta\log_{10}k}{L}.
\]

If the three measured differences have independent Gaussian errors, the numerator variance is σ_app² + σ_b² +
4σ_k². Correlated calibration requires the full covariance. A nominal 95% interval centred on q = 1 excludes q
= 0 only if its total standard error is smaller than 1/1.96. This is a necessary precision target for that
particular result, not a guarantee of valid coverage or a forecast of an observed exclusion.

| Interval | Difference in log10 a between q = 0 and q = 1 | Maximum σ of differential log10 b, if it is the only error | Maximum σ of differential log10 velocity, if it is the only error |
| --- | --- | --- | --- |
| z = 0 to 1 | 0.2529 dex | 0.1290 dex | 0.03226 dex, about 7.4% |
| z = 0.33 to 1.44 | 0.2835 dex | 0.1446 dex | 0.03616 dex, about 8.3% |

Other errors consume this budget. These are uncertainties in a systematic difference between epochs, not
errors that automatically shrink with the number of radial points. With bounded biases rather than Gaussian
priors, a robust exclusion requires the lower bound on Δ log10 a_app to exceed the allowed positive
contribution from Δ log10 b + 2Δ log10 k.

For scale, H tracking from z = 0 to 1 raises a by a factor 1.790 in this background. The same deep-limit
signal can arise from a baryonic correction b = 1.790, an acceleration correction k = 1.338, or a velocity
correction of 15.7%, each acting alone. At fixed distance and line-of-sight velocity, a true inclination of 60
degrees inferred as 48.5 degrees supplies that velocity factor. These are equivalent signal sizes, not
evidence for such errors.

In a photometric mass model with fixed angular geometry, inferred mass scales as D² and physical radius as D,
so g_bar is approximately distance independent while g_obs scales as D^-1. Consequently a_app scales as D^-2
in the deep limit. A distance underestimate by a factor 0.747 would reproduce the same signal. This simplified
scaling does not apply unchanged to a fully coupled dynamical reconstruction. Pressure support, inclination
and beam corrections can also change radial shape, so one scalar k is an identifiability probe rather than a
complete observational model.

The deep-limit statistic g_obs²/g_bar becomes V_flat^4/(G M_bar) under the usual outer circular-orbit
approximation. Recasting the same masses and velocities as a baryonic Tully–Fisher measurement adds no
independent algebraic information. A separate survey can add evidence, but its selection, gas estimates and
velocity definition must be cross-calibrated.

## Source and data checkpoint

A relevant author preprint by Rusishvili already investigates evolving gas and stellar-mass estimates. Its
earlier version uses 89 objects and states that two cuts needed to reproduce the 79-galaxy sample are
unavailable in its inputs. Its gas correction uses a population scaling relation, with limitations stated for
the mass range. Its Zenodo ZIP contains the manuscript, TeX source and figures, but no galaxy tables or
analysis code. These claims have not been independently replicated here. They make an independent audit
useful, while preventing a claim that baryonic calibration is a newly noticed concern. [Rusishvili, DOI
21623517](https://doi.org/10.5281/zenodo.21623517)

The later preprint's PDF was downloaded from Zenodo and checked against its recorded checksum. Page 3 states a
sample of 89 but lists bin counts totalling 93. That mismatch was verified in the rendered PDF. Its code and
exact selection are described as available on request. The manuscript's numerical correction should remain a
hypothesis for replication until the inputs and selection are reconciled. [Rusishvili, DOI
21644662](https://doi.org/10.5281/zenodo.21644662)

The official DARK index is reachable. Its linked dynamical-data server timed out in bounded HTTPS and HTTP
attempts. Paper I describes released best-fit parameters with 95% intervals and points to DARK. Those
intervals do not by themselves establish access to joint covariance. The alternative AMUSED UDF page describes
the parent catalogue and public cubes, variance products and PSF information. That page supports a possible
future refit, but does not itself identify the selected 79 or provide their joint dynamical posteriors. [DARK
releases](https://dark.univ-lyon1.fr/data-releases/), [MUSE-DARK I, section
8](https://arxiv.org/html/2506.19721v3), [AMUSED UDF](https://amused.univ-lyon1.fr/project/UDF/)

No individual radial data or joint posterior set for the 79 galaxies was acquired. This records access from
this environment, not global absence of the data. No author was contacted. The original retrieval record is
preserved in [retrieval.json](retrieval.json). Additional attempts and downloaded-source hashes are in
[retrieval-addendum.json](retrieval-addendum.json) and [sources.json](sources.json).

## Acceptance and stopping conditions

The next worthwhile action is a data sufficiency audit, followed by a frozen recovery protocol. It must satisfy all of these conditions before a physical evolution claim:

1. **Reproduce membership.** Recover stable IDs for the selected sample, parent exclusions, radial cuts and
   redshift assignments. A different set may support a new analysis, but cannot be labelled a replication of
   the original 79.
2. **Recover measurement dependence.** Obtain joint posterior draws, a usable joint likelihood, or the
   original cubes and calibration products needed to reconstruct them. Do not infer independent radial errors
   from marginal intervals.
3. **Constrain the relevant drift.** Establish independent stellar and gas information plus kinematic
   calibration, or show that their joint allowed bias cannot absorb q = 0 versus q = 1. A local anchor alone
   fails this condition. Matching only stellar mass does not control gas fraction, physical radial coverage,
   resolution or inclination.
4. **Demonstrate useful information.** Inspect the sensitivities after nuisance projection on the actual joint
   distribution of acceleration and redshift. A technically full-rank matrix is insufficient. Fix a target
   uncertainty or predictive separation before the final fit, with a declared systematic-error budget.
5. **Calibrate false positives.** Inject q = 0 and q = 1, calibration drift, realistic gas gradients and no
   physical evolution through the full observational and selection procedure. Predeclare the interval coverage
   and false-positive tolerances, then verify them on simulations independent of model tuning.
6. **Challenge the result.** Compare alternative baryonic and kinematic reconstructions, leave out whole
   galaxies, and hold out a genuinely independent survey where available. If a gravity mechanism is claimed,
   specify its external-field and cosmological predictions and compare relevant ordinary-gravity alternatives.

**Park** the empirical fit if membership, covariance or independent calibration cannot be recovered, or if the
posterior for q follows the nuisance priors over the tested range. **Reject the current formulation** if it
treats free q as identifiable while leaving the exact nuisance symmetry unconstrained, treats same-data
Tully–Fisher as replication, or interprets an empirical RAR change as a unique mechanism. **Pursue** once the
data audit shows that an actual calibrated measurement can separate the competing explanations. A null result
that exposes a calibration floor is itself a useful outcome. It should be reported at that scope.

The retained project lesson is that normalization agreement at one epoch cannot identify a cosmological
scaling. The next action is to reconcile the selected galaxies and independent calibration products before
spending effort on another exponent fit.
