# A test that separates evolution from calibration

This protocol is proposed. The raw-data fit has not been performed. Its purpose is to compare constant and H-tracking acceleration scales using the same data, nuisance parameters and selection model. See the [study](README.md) for the current published-summary result.

## Required observations

For every galaxy, retain a stable survey identifier, redshift, sample-membership decision and original selection cuts. For every accepted radial point, retain radius, observed velocity, baryonic components, errors and shared nuisance-parameter draws. Include inclination, distance, stellar mass-to-light ratio, gas normalization, beam smearing and pressure support.

Prefer the velocity data cubes and their observational model when practical. A RAR extracted under a chosen halo profile is conditional on that profile. Refitting the extracted relation does not automatically provide a model-independent test of gravity. Retain alternate halo and MOND reconstructions as sensitivity analyses of the same sample.

The MUSE release must identify the 79 selected galaxies, the r > 2 kpc cut, four bin definitions and original posterior samples or covariance. A table of marginal best fits is insufficient to restore correlations between radii or between the two acceleration axes. A global fit over a broad redshift range needs its actual galaxy redshifts, not an invented effective redshift.

## A common likelihood

For galaxy i and radius j, predict the total acceleration from the baryonic component and a₀(zi) = A E(zi)^q. In log space, model the measured acceleration vector around that prediction with intrinsic scatter and its full measurement covariance. Treat uncertain baryonic acceleration as a latent quantity, or propagate joint posterior draws through the observational model.

Shared galaxy parameters must be sampled or marginalized together. Independent radial error bars are not a substitute. If the original posterior has already used the tested RAR as a prior, account for that prior explicitly or refit the original measurements to avoid circular inference.

Compare q = 0 and q = 1 with identical positive-amplitude priors and nuisance terms. Then fit free q to test the fixed forms. Report likelihood or predictive scores only after validating the statistical model. A confidence or credible interval must be labelled with its definition. Do not change a 95% interval into a 1σ error merely because a plotting routine expects one.

Two calibrations answer different questions:

1. A floating A compares shapes. It does not test the absolute equality a₀(0) = cH₀/(2π).
2. A local-anchor prior compares shape and normalization. Use the local calibration's systematic uncertainty and any covariance shared with the distant sample. A fixed canonical number with zero uncertainty is only a benchmark.

The fiducial background is flat matter plus constant Λ. Propagate cosmological uncertainty and report alternate E(z) histories as named sensitivity analyses. An acceleration scale tied to a changing dark-energy component is a different hypothesis and needs its own equations. Equality to a Hubble-scale number at z = 0 does not identify which cosmic quantity is involved.

## Controls before interpreting q

- Refit with and without each galaxy. Resample galaxies, not individual radii, when using a bootstrap.
- Match or model stellar mass, surface brightness, physical radial coverage, inclination and gas fraction across redshift. Redshift trends in sample composition can mimic a₀ evolution.
- Repeat the fit under the documented alternate mass and kinematic models. Include common calibration shifts and redshift-dependent shifts separately.
- Keep repeated analyses of MHUDF, KMOS and other parent surveys in the same dependence group. Cross-match identifiers before combining studies.
- For a baryonic Tully–Fisher cross-check, use consistently defined total baryonic masses and asymptotic Vflat. A peak-velocity proxy needs a separately validated mapping, with its uncertainty propagated.
- Recover injected q = 0 and q = 1 samples through the full observational and selection procedure. Quantify bias and interval coverage before interpreting real-data model selection.

## Falsification and interpretation

Before looking at the final fitted exponent, freeze the sample, likelihood, priors, covariance handling and sensitivity range in a versioned analysis record. Use a calibrated interval with a declared coverage level. A 95% interval excluding q = 1 is a conditional rejection of H tracking only if the recovery tests and specified systematic checks retain valid coverage.

A disagreement that disappears after a plausible mass-calibration or selection correction does not robustly falsify the physical law. A constant scale rejected within one reconstruction is evidence against that constant reconstruction, without identifying the cause.

An evolving baryon–halo relation can also produce an evolving empirical acceleration scale within ordinary gravity.

Replication requires an independently selected galaxy sample or a justified independent observable. Reanalysing the same bins, or switching reconstruction methods for the same galaxies, tests robustness rather than replication.

Agreement with q = 1 would support this parameterization over alternatives in its tested range. It would not establish a unique mechanism, a new fundamental theory, or a cosmic origin scenario.

## Retrieval checkpoint

The MUSE release index was accessible on 12 November 2026. Its linked data server timed out. The KMOS3D CDS table was also unavailable in bounded attempts. The indexed schema contains redshift, masses, peak circular speed and dispersion but no individual errors or covariance. The author HTML supplies only five example rows.

The immediate next action is a read-only retry of the documented releases in [evidence.json](evidence.json), followed by a schema and sample-selection audit. If the required covariance or posterior products are absent, retain that limit. Author contact would be a separate action requiring authorization to send a message.
